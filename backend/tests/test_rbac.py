"""Role-based access control smoke tests."""

from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.auth_model import UserAccount
from app.models.vehicle_model import VehicleModel
from conftest import auth_headers


client = TestClient(app)


ORDER_PAYLOAD = {
    "shipper_name": "RBAC Customer",
    "shipper_phone": "9876543210",
    "shipper_email": "rbac@example.com",
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
}


def _user_id(username: str) -> str:
    db = SessionLocal()
    try:
        user = db.query(UserAccount).filter(UserAccount.username == username).one()
        return str(user.id)
    finally:
        db.close()


def _seed_vehicle(category: str) -> str:
    db = SessionLocal()
    try:
        vehicle = VehicleModel(
            manufacturer="RBAC Motors",
            model_name=f"LCV RBAC {uuid4()}",
            category=category,
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


def _create_assigned_trip(driver_id: str) -> str:
    admin_headers = auth_headers(client, "super_admin", username=f"driver-setup-admin-{uuid4()}")
    category = "Tractor"
    _seed_vehicle(category)
    order = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD | {"vehicle_category_preference": category},
        headers=admin_headers,
    )
    assert order.status_code == 201, order.text
    order_id = order.json()["id"]
    transition = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": "CONFIRMED",
            "event": "order_submitted",
            "payload": {
                "payment_mode": "advance",
                "topay_consent_status": "not_required",
                "material_type": "general_goods",
                "body_type_required": "open",
            },
            "actor_role": "OMS",
            "idempotency_key": str(uuid4()),
            "trace_id": f"driver-rbac-{uuid4()}",
        },
        headers=admin_headers,
    )
    assert transition.status_code == 200, transition.text
    matches = client.get(f"/api/v1/orders/{order_id}/match?limit=1&min_score=0", headers=admin_headers)
    assert matches.status_code == 200, matches.text
    match_id = matches.json()["matches"][0]["match_id"]
    accepted = client.post(f"/api/v1/matches/{match_id}/accept", json={}, headers=admin_headers)
    assert accepted.status_code == 200, accepted.text
    trip = client.get(f"/api/v1/orders/{order_id}/trip", headers=admin_headers)
    assert trip.status_code == 200, trip.text
    trip_id = trip.json()["trip_id"]
    assigned = client.post(
        f"/api/v1/trips/{trip_id}/assign-driver",
        json={"driver_id": driver_id},
        headers=admin_headers,
    )
    assert assigned.status_code == 200, assigned.text
    return trip_id


def test_unauthenticated_request_is_rejected():
    response = client.get("/api/v1/orders")
    assert response.status_code == 401


def test_wrong_role_is_rejected():
    response = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD,
        headers=auth_headers(client, "driver"),
    )
    assert response.status_code == 403


def test_correct_role_succeeds():
    response = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD,
        headers=auth_headers(client, "customer"),
    )
    assert response.status_code == 201, response.text
    assert response.json()["current_state"] == "CREATED"
    assert response.json()["customer_id"]


def test_customer_only_sees_own_orders():
    first_headers = auth_headers(client, "customer", username=f"customer-one-{uuid4()}")
    second_headers = auth_headers(client, "customer", username=f"customer-two-{uuid4()}")

    first_order = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD | {"shipper_name": "First Customer"},
        headers=first_headers,
    )
    assert first_order.status_code == 201, first_order.text
    second_order = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD | {"shipper_name": "Second Customer"},
        headers=second_headers,
    )
    assert second_order.status_code == 201, second_order.text

    listed = client.get("/api/v1/orders", headers=first_headers)
    assert listed.status_code == 200, listed.text
    order_ids = {order["id"] for order in listed.json()["orders"]}
    assert first_order.json()["id"] in order_ids
    assert second_order.json()["id"] not in order_ids

    blocked = client.get(
        f"/api/v1/orders/{second_order.json()['id']}",
        headers=first_headers,
    )
    assert blocked.status_code == 404


def test_customer_safe_flow_blocks_other_customer_order():
    first_headers = auth_headers(client, "customer", username=f"flow-customer-one-{uuid4()}")
    second_headers = auth_headers(client, "customer", username=f"flow-customer-two-{uuid4()}")
    order = client.post("/api/v1/orders", json=ORDER_PAYLOAD, headers=second_headers)
    assert order.status_code == 201, order.text

    blocked = client.get(
        f"/api/v1/orders/{order.json()['id']}/customer-flow-summary",
        headers=first_headers,
    )
    assert blocked.status_code == 404

    allowed = client.get(
        f"/api/v1/orders/{order.json()['id']}/customer-flow-summary",
        headers=second_headers,
    )
    assert allowed.status_code == 200, allowed.text
    assert allowed.json()["order_id"] == order.json()["id"]


def test_customer_cannot_call_admin_or_finance_actions():
    headers = auth_headers(client, "customer")
    order = client.post("/api/v1/orders", json=ORDER_PAYLOAD, headers=headers)
    assert order.status_code == 201, order.text

    quote = client.post(f"/api/v1/orders/{order.json()['id']}/quote", headers=headers)
    assert quote.status_code == 403

    settlement = client.post(
        f"/api/v1/trips/{uuid4()}/settlements/release",
        json={
            "amount": 18000,
            "commission_amount": 1800,
            "gst_amount": 324,
            "driver_payable_amount": 16200,
            "currency": "INR",
            "idempotency_key": f"customer-settlement-{uuid4()}",
        },
        headers=headers,
    )
    assert settlement.status_code == 403


def test_finance_route_rejects_ops_and_accepts_finance_role_guard():
    trip_id = uuid4()
    payload = {
        "amount": 18000,
        "commission_amount": 1800,
        "gst_amount": 324,
        "driver_payable_amount": 16200,
        "currency": "INR",
        "idempotency_key": f"rbac-settlement-{uuid4()}",
    }

    wrong = client.post(
        f"/api/v1/trips/{trip_id}/settlements/release",
        json=payload,
        headers=auth_headers(client, "ops_admin"),
    )
    assert wrong.status_code == 403

    correct = client.post(
        f"/api/v1/trips/{trip_id}/settlements/release",
        json=payload,
        headers=auth_headers(client, "finance_admin"),
    )
    assert correct.status_code == 404


def test_driver_trip_access_is_assigned_driver_only():
    driver_one_username = f"driver-one-{uuid4()}"
    driver_two_username = f"driver-two-{uuid4()}"
    driver_one_headers = auth_headers(client, "driver", username=driver_one_username)
    driver_two_headers = auth_headers(client, "driver", username=driver_two_username)
    trip_id = _create_assigned_trip(_user_id(driver_one_username))

    listed = client.get("/api/v1/driver/trips", headers=driver_one_headers)
    assert listed.status_code == 200, listed.text
    assert trip_id in {item["trip"]["trip_id"] for item in listed.json()["trips"]}

    blocked_read = client.get(f"/api/v1/driver/trips/{trip_id}", headers=driver_two_headers)
    assert blocked_read.status_code == 404

    blocked_update = client.post(
        f"/api/v1/trips/{trip_id}/milestones",
        json={
            "milestone_type": "wrong_driver_update",
            "status": "recorded",
            "payload": {},
            "idempotency_key": f"wrong-driver-{uuid4()}",
        },
        headers=driver_two_headers,
    )
    assert blocked_update.status_code == 404


def test_driver_role_cannot_call_admin_or_finance_routes():
    driver_headers = auth_headers(client, "driver", username=f"driver-blocked-{uuid4()}")
    trip_id = uuid4()
    order = client.post("/api/v1/orders", json=ORDER_PAYLOAD, headers=driver_headers)
    assert order.status_code == 403

    assign = client.post(
        f"/api/v1/trips/{trip_id}/assign-driver",
        json={"driver_id": str(uuid4())},
        headers=driver_headers,
    )
    assert assign.status_code == 403

    settlement = client.post(
        f"/api/v1/trips/{trip_id}/settlements/release",
        json={
            "amount": 18000,
            "commission_amount": 1800,
            "gst_amount": 324,
            "driver_payable_amount": 16200,
            "currency": "INR",
            "idempotency_key": f"driver-settlement-{uuid4()}",
        },
        headers=driver_headers,
    )
    assert settlement.status_code == 403


def _create_company_order_and_match(company_headers: dict[str, str], category: str) -> tuple[str, str, str]:
    admin_headers = auth_headers(client, "super_admin", username=f"transport-admin-{uuid4()}")
    vehicle = client.post(
        "/api/v1/vehicles",
        json={
            "manufacturer": "Transport RBAC",
            "model_name": f"Company Vehicle {uuid4()}",
            "category": category,
            "body_type": "tipper" if category == "Tipper" else "open",
            "gvw_kg": 3500,
            "payload_kg": 2000,
            "mileage_kmpl": 12,
            "price_ex_showroom": 1200000,
        },
        headers=company_headers,
    )
    assert vehicle.status_code == 201, vehicle.text
    order = client.post(
        "/api/v1/orders",
        json=ORDER_PAYLOAD | {"vehicle_category_preference": category},
        headers=admin_headers,
    )
    assert order.status_code == 201, order.text
    order_id = order.json()["id"]
    transition = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": "CONFIRMED",
            "event": "order_submitted",
            "payload": {
                "payment_mode": "advance",
                "topay_consent_status": "not_required",
                "material_type": "general_goods",
                "body_type_required": "open",
            },
            "actor_role": "OMS",
            "idempotency_key": str(uuid4()),
            "trace_id": f"transport-rbac-{uuid4()}",
        },
        headers=admin_headers,
    )
    assert transition.status_code == 200, transition.text
    matches = client.get(f"/api/v1/orders/{order_id}/match?limit=1&min_score=0", headers=company_headers)
    assert matches.status_code == 200, matches.text
    return vehicle.json()["id"], order_id, matches.json()["matches"][0]["match_id"]


def test_transport_company_owns_vehicles_matches_and_trips():
    company_one_headers = auth_headers(client, "transport_company", username=f"company-one-{uuid4()}")
    company_two_headers = auth_headers(client, "transport_company", username=f"company-two-{uuid4()}")

    vehicle_id, _order_id, match_id = _create_company_order_and_match(company_one_headers, "Tipper")

    blocked_vehicle = client.get(f"/api/v1/vehicles/{vehicle_id}", headers=company_two_headers)
    assert blocked_vehicle.status_code == 404

    listed_matches = client.get("/api/v1/matches", headers=company_one_headers)
    assert listed_matches.status_code == 200, listed_matches.text
    assert match_id in {item["id"] for item in listed_matches.json()["matches"]}

    blocked_accept = client.post(f"/api/v1/matches/{match_id}/accept", json={}, headers=company_two_headers)
    assert blocked_accept.status_code == 404

    accepted = client.post(f"/api/v1/matches/{match_id}/accept", json={}, headers=company_one_headers)
    assert accepted.status_code == 200, accepted.text

    trips = client.get("/api/v1/transport-company/trips", headers=company_one_headers)
    assert trips.status_code == 200, trips.text
    trip_id = trips.json()["trips"][0]["trip"]["trip_id"]

    blocked_trip = client.get(f"/api/v1/transport-company/trips/{trip_id}", headers=company_two_headers)
    assert blocked_trip.status_code == 404


def test_transport_company_wrong_role_and_admin_finance_blocks():
    customer_headers = auth_headers(client, "customer", username=f"not-company-{uuid4()}")
    assert client.get("/api/v1/matches", headers=customer_headers).status_code == 403

    company_headers = auth_headers(client, "transport_company", username=f"company-blocked-{uuid4()}")
    quote = client.post(f"/api/v1/orders/{uuid4()}/quote", headers=company_headers)
    assert quote.status_code == 403
    settlement = client.post(
        f"/api/v1/trips/{uuid4()}/settlements/release",
        json={
            "amount": 18000,
            "commission_amount": 1800,
            "gst_amount": 324,
            "driver_payable_amount": 16200,
            "currency": "INR",
            "idempotency_key": f"company-settlement-{uuid4()}",
        },
        headers=company_headers,
    )
    assert settlement.status_code == 403
