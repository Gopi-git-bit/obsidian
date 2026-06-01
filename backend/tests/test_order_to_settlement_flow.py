"""End-to-end order-to-settlement flow contract."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.flow_model import GSTInvoiceRecord, JournalEntry, SettlementRecord
from app.models.vehicle_model import VehicleModel
from conftest import auth_headers


client = TestClient(app)
client.headers.update(auth_headers(client, "super_admin"))


def _seed_vehicle() -> str:
    db = SessionLocal()
    try:
        vehicle = VehicleModel(
            manufacturer="Test Motors",
            model_name=f"LCV Flow {uuid4()}",
            category="LCV",
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


def _create_order() -> dict:
    response = client.post(
        "/api/v1/orders",
        json={
            "shipper_name": "Flow Customer",
            "shipper_phone": "9876543210",
            "shipper_email": "flow@example.com",
            "origin_city": "Tiruppur",
            "origin_state": "Tamil Nadu",
            "destination_city": "Chennai",
            "destination_state": "Tamil Nadu",
            "cargo_type": "general",
            "weight_kg": 1200,
            "num_packages": 12,
            "vehicle_category_preference": "LCV",
            "is_interstate": False,
            "estimated_distance_km": 460,
            "offered_price": 18000,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _transition(order_id: str, to_state: str, event: str, *, actor_role="OMS", payload=None):
    response = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": to_state,
            "event": event,
            "payload": payload or {},
            "actor_role": actor_role,
            "idempotency_key": str(uuid4()),
            "trace_id": f"flow-{uuid4()}",
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_customer_order_to_settlement_accounting_flow():
    vehicle_id = _seed_vehicle()

    # Customer creates order.
    order = _create_order()
    order_id = order["id"]
    assert order["current_state"] == "CREATED"

    # Quote generated.
    quote = client.post(f"/api/v1/orders/{order_id}/quote")
    assert quote.status_code == 201, quote.text
    assert quote.json()["status"] == "generated"
    assert quote.json()["total_amount"] > 0

    # Vehicle matched.
    _transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
    )
    matches = client.get(f"/api/v1/orders/{order_id}/match?limit=1&min_score=0")
    assert matches.status_code == 200, matches.text
    match_id = matches.json()["matches"][0]["match_id"]
    assert matches.json()["matches"][0]["vehicle_id"] == vehicle_id

    # Trip created.
    accepted = client.post(f"/api/v1/matches/{match_id}/accept", json={"notes": "accept test match"})
    assert accepted.status_code == 200, accepted.text
    trip = client.get(f"/api/v1/orders/{order_id}/trip")
    assert trip.status_code == 200, trip.text
    trip_id = trip.json()["trip_id"]

    # Advance payment recorded.
    advance = client.post(
        f"/api/v1/orders/{order_id}/payments/advance",
        json={
            "amount": 9000,
            "currency": "INR",
            "provider_ref": "razorpay-advance-test",
            "idempotency_key": f"advance-{uuid4()}",
        },
    )
    assert advance.status_code == 201, advance.text
    assert advance.json()["payment_type"] == "advance"

    _transition(order_id, "EN_ROUTE_TO_PICKUP", "driver_started_pickup", actor_role="DRIVER")
    _transition(order_id, "AT_PICKUP_WAITING", "driver_arrived_pickup", actor_role="DRIVER")
    _transition(
        order_id,
        "LOADING",
        "shipment_doc_scanned",
        actor_role="DRIVER",
        payload={
            "driver_id": "driver-flow",
            "vehicle_id": vehicle_id,
            "doc_type": "loading_photo",
            "doc_url": "s3://docs/loading.jpg",
            "scan_exif": {"lat": 11.1085, "lng": 77.3411},
        },
    )

    # Loading photo uploaded.
    loading_photo = client.post(
        f"/api/v1/trips/{trip_id}/loading-photo",
        json={
            "photo_url": "s3://docs/loading.jpg",
            "uploaded_by": "driver-flow",
            "idempotency_key": f"loading-photo-{uuid4()}",
        },
    )
    assert loading_photo.status_code == 201, loading_photo.text

    # Trip milestone updated.
    _transition(order_id, "DEPARTED_FOR_DELIVERY", "loading_completed", actor_role="DRIVER")
    milestone = client.post(
        f"/api/v1/trips/{trip_id}/milestones",
        json={
            "milestone_type": "in_transit",
            "status": "recorded",
            "payload": {"eta": (datetime.now(timezone.utc) + timedelta(hours=7)).isoformat()},
            "idempotency_key": f"milestone-{uuid4()}",
        },
    )
    assert milestone.status_code == 201, milestone.text

    _transition(order_id, "AT_DELIVERY_WAITING", "driver_arrived_delivery", actor_role="DRIVER")

    # POD uploaded.
    pod = client.post(
        f"/api/v1/trips/{trip_id}/pod",
        json={
            "pod_url": "s3://docs/pod.jpg",
            "consignee_otp": "123456",
            "pod_exif": {"lat": 13.0827, "lng": 80.2707},
            "uploaded_by": "driver-flow",
            "idempotency_key": f"pod-{uuid4()}",
        },
    )
    assert pod.status_code == 201, pod.text
    assert pod.json()["order_state"] == "DELIVERED_PENDING_SETTLEMENT"

    # POD verified.
    pod_verified = client.post(
        f"/api/v1/trips/{trip_id}/pod/verify",
        json={"verified_by": "rag-ocr", "idempotency_key": f"pod-verify-{uuid4()}"},
    )
    assert pod_verified.status_code == 200, pod_verified.text
    assert pod_verified.json()["verification_status"] == "verified"

    # OTP verified.
    otp = client.post(
        f"/api/v1/trips/{trip_id}/otp/verify",
        json={"otp": "123456", "verified_by": "consignee", "idempotency_key": f"otp-{uuid4()}"},
    )
    assert otp.status_code == 200, otp.text
    assert otp.json()["otp_verified"] is True

    # Settlement released, journal entry created, GST invoice record created.
    settlement = client.post(
        f"/api/v1/trips/{trip_id}/settlements/release",
        json={
            "amount": 18000,
            "commission_amount": 1800,
            "gst_amount": 324,
            "driver_payable_amount": 16200,
            "currency": "INR",
            "idempotency_key": f"settlement-{uuid4()}",
        },
    )
    assert settlement.status_code == 201, settlement.text
    body = settlement.json()
    assert body["status"] == "released"
    assert body["journal_entry_id"]
    assert body["gst_invoice_id"]

    db = SessionLocal()
    try:
        order_uuid = UUID(order_id)
        assert db.query(SettlementRecord).filter(SettlementRecord.order_id == order_uuid).count() == 1
        assert db.query(JournalEntry).filter(JournalEntry.order_id == order_uuid).count() == 1
        assert db.query(GSTInvoiceRecord).filter(GSTInvoiceRecord.order_id == order_uuid).count() == 1
    finally:
        db.close()
