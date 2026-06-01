"""Supervisor exception and hold controls."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.auth_model import UserAccount
from app.models.flow_model import Trip
from app.models.vehicle_model import VehicleModel
from conftest import auth_headers

client = TestClient(app)


ORDER = {
    "shipper_name": "Supervisor Case",
    "shipper_phone": "9876543210",
    "origin_city": "Tiruppur",
    "origin_state": "Tamil Nadu",
    "destination_city": "Chennai",
    "destination_state": "Tamil Nadu",
    "cargo_type": "general",
    "weight_kg": 1200,
    "num_packages": 12,
    "vehicle_category_preference": "Tractor",
    "estimated_distance_km": 460,
    "offered_price": 18000,
}


def _user_id(username: str) -> str:
    db = SessionLocal()
    try:
        return str(db.query(UserAccount).filter(UserAccount.username == username).one().id)
    finally:
        db.close()


def _seed_vehicle() -> str:
    db = SessionLocal()
    try:
        vehicle = VehicleModel(
            manufacturer="Supervisor Motors",
            model_name=f"Tractor {uuid4()}",
            category="Tractor",
            body_type="open",
            gvw_kg=3500,
            payload_kg=2000,
            mileage_kmpl=12,
            price_ex_showroom=1200000,
            is_active=True,
        )
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        return str(vehicle.id)
    finally:
        db.close()


def _setup_trip(driver_id: str | None = None) -> tuple[str, str]:
    admin = auth_headers(client, "super_admin", username=f"sup-admin-{uuid4()}")
    vehicle_id = _seed_vehicle()
    order = client.post("/api/v1/orders", json=ORDER, headers=admin)
    assert order.status_code == 201, order.text
    order_id = order.json()["id"]
    confirmed = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": "CONFIRMED",
            "event": "order_submitted",
            "payload": {"payment_mode": "advance", "topay_consent_status": "not_required", "material_type": "general_goods", "body_type_required": "open"},
            "actor_role": "OMS",
            "idempotency_key": str(uuid4()),
            "trace_id": f"sup-{uuid4()}",
        },
        headers=admin,
    )
    assert confirmed.status_code == 200, confirmed.text
    matches = client.get(f"/api/v1/orders/{order_id}/match?limit=20&min_score=0", headers=admin)
    assert matches.status_code == 200, matches.text
    match = next(item for item in matches.json()["matches"] if item["vehicle_id"] == vehicle_id)
    accepted = client.post(f"/api/v1/matches/{match['match_id']}/accept", json={}, headers=admin)
    assert accepted.status_code == 200, accepted.text
    trip = client.get(f"/api/v1/orders/{order_id}/trip", headers=admin)
    assert trip.status_code == 200, trip.text
    trip_id = trip.json()["trip_id"]
    if driver_id:
        assigned = client.post(f"/api/v1/trips/{trip_id}/assign-driver", json={"driver_id": driver_id}, headers=admin)
        assert assigned.status_code == 200, assigned.text
    return order_id, trip_id


def test_supervisor_unauthenticated_and_wrong_role_fail():
    assert client.get("/api/v1/supervisor/cases").status_code == 401
    wrong = client.post(
        f"/api/v1/supervisor/orders/{uuid4()}/fraud-hold",
        json={"reason": "not allowed"},
        headers=auth_headers(client, "customer", username=f"sup-wrong-{uuid4()}"),
    )
    assert wrong.status_code == 403


def test_supervisor_can_manage_cases_and_admin_can_view():
    order_id, _trip_id = _setup_trip()
    sup = auth_headers(client, "supervisor", username=f"supervisor-{uuid4()}")
    hold = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "POD anomaly"}, headers=sup)
    assert hold.status_code == 200, hold.text
    case_id = hold.json()["case"]["case_id"]
    assert hold.json()["case"]["status"] == "held"

    cases = client.get("/api/v1/supervisor/cases", headers=auth_headers(client, "super_admin"))
    assert cases.status_code == 200
    assert case_id in {item["case"]["case_id"] for item in cases.json()["cases"]}

    rejected = client.post(f"/api/v1/supervisor/cases/{case_id}/reject", json={"reason": "reject test"}, headers=sup)
    assert rejected.status_code == 200
    assert rejected.json()["case"]["status"] == "rejected"
    approved = client.post(f"/api/v1/supervisor/cases/{case_id}/approve", json={"reason": "cleared"}, headers=sup)
    assert approved.status_code == 200
    assert approved.json()["audit_trail"]


def test_driver_cannot_verify_own_pod_or_otp_and_supervisor_can():
    username = f"driver-supervisor-{uuid4()}"
    driver = auth_headers(client, "driver", username=username)
    order_id, trip_id = _setup_trip(_user_id(username))
    admin = auth_headers(client, "super_admin", username=f"sup-admin2-{uuid4()}")
    trip = SessionLocal()
    try:
        vehicle_id = str(trip.query(Trip).filter(Trip.trip_id == UUID(trip_id)).one().vehicle_id)
    finally:
        trip.close()
    for to_state, event, payload in [
        ("EN_ROUTE_TO_PICKUP", "driver_started_pickup", {}),
        ("AT_PICKUP_WAITING", "driver_arrived_pickup", {}),
        ("LOADING", "shipment_doc_scanned", {"driver_id": username, "vehicle_id": vehicle_id, "doc_type": "loading_photo", "doc_url": "s3://docs/loading.jpg", "scan_exif": {}}),
        ("DEPARTED_FOR_DELIVERY", "loading_completed", {}),
        ("AT_DELIVERY_WAITING", "driver_arrived_delivery", {}),
    ]:
        response = client.post(
            f"/api/v1/orders/{order_id}/transition",
            json={"to_state": to_state, "event": event, "payload": payload, "actor_role": "DRIVER", "idempotency_key": str(uuid4()), "trace_id": f"sup-{uuid4()}"},
            headers=admin,
        )
        assert response.status_code == 200, response.text
    pod = client.post(f"/api/v1/trips/{trip_id}/pod", json={"pod_url": "s3://docs/pod.jpg", "consignee_otp": "123456", "pod_exif": {}, "uploaded_by": username, "idempotency_key": f"pod-{uuid4()}"}, headers=driver)
    assert pod.status_code == 201, pod.text
    assert client.post(f"/api/v1/trips/{trip_id}/pod/verify", json={"verified_by": username, "idempotency_key": f"podv-{uuid4()}"}, headers=driver).status_code == 403
    sup = auth_headers(client, "supervisor", username=f"pod-supervisor-{uuid4()}")
    assert client.post(f"/api/v1/trips/{trip_id}/pod/verify", json={"verified_by": "supervisor", "idempotency_key": f"podv-{uuid4()}"}, headers=sup).status_code == 200
    assert client.post(f"/api/v1/trips/{trip_id}/otp/verify", json={"otp": "123456", "verified_by": "supervisor", "idempotency_key": f"otp-{uuid4()}"}, headers=sup).status_code == 200


def test_finance_cannot_release_settlement_under_fraud_hold_until_cleared():
    order_id, trip_id = _setup_trip()
    sup = auth_headers(client, "supervisor", username=f"hold-supervisor-{uuid4()}")
    held = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "fraud risk"}, headers=sup)
    assert held.status_code == 200, held.text
    finance = auth_headers(client, "finance_admin", username=f"finance-hold-{uuid4()}")
    payload = {"amount": 18000, "commission_amount": 1800, "gst_amount": 324, "driver_payable_amount": 16200, "currency": "INR", "idempotency_key": f"settle-{uuid4()}"}
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert blocked.status_code == 409
    cleared = client.post(f"/api/v1/supervisor/cases/{held.json()['case']['case_id']}/approve", json={"reason": "cleared"}, headers=sup)
    assert cleared.status_code == 200
