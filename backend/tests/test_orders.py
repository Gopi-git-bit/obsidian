"""Tests for canonical order state machine, matches, and bids."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.order_model import AgentDLQMessage, VehicleReservation

client = TestClient(app)

SAMPLE_ORDER = {
    "shipper_name": "Rajesh Kumar",
    "shipper_phone": "9876543210",
    "shipper_email": "rajesh@example.com",
    "origin_city": "Mumbai",
    "origin_state": "Maharashtra",
    "destination_city": "Delhi",
    "destination_state": "Delhi",
    "cargo_type": "general",
    "weight_kg": 5000.0,
    "volume_cbm": 25.0,
    "num_packages": 10,
    "vehicle_category_preference": "HCV",
    "is_interstate": True,
    "estimated_distance_km": 1400.0,
    "offered_price": 25000.0,
}


def create_order(extra: dict | None = None) -> str:
    payload = SAMPLE_ORDER | (extra or {})
    response = client.post("/api/v1/orders", json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["shipper_name"] == "Rajesh Kumar"
    assert data["status"] == "CREATED"
    assert data["current_state"] == "CREATED"
    assert data["origin_city"] == "Mumbai"
    assert data["destination_city"] == "Delhi"
    assert data["weight_kg"] == 5000.0
    return data["id"]


def transition(
    order_id: str,
    to_state: str,
    event: str,
    *,
    actor_role: str = "OMS",
    payload: dict | None = None,
    idempotency_key: str | None = None,
    endpoint_prefix: str = "/api/v1",
):
    return client.post(
        f"{endpoint_prefix}/orders/{order_id}/transition",
        json={
            "to_state": to_state,
            "event": event,
            "payload": payload or {},
            "actor_role": actor_role,
            "idempotency_key": idempotency_key or str(uuid4()),
            "trace_id": f"trace-{uuid4()}",
        },
    )


def confirm(order_id: str, payload: dict | None = None):
    return transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        }
        | (payload or {}),
    )


def test_create_order():
    create_order()


def test_list_orders():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "orders" in data
    assert isinstance(data["orders"], list)


def test_list_orders_with_filters_accepts_uppercase_canonical_state():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders?status=CREATED&origin_city=Mumbai")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_get_order():
    order_id = create_order()
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_order_not_found():
    response = client.get("/api/v1/orders/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_order_status_rejected():
    order_id = create_order()
    response = client.patch(
        f"/api/v1/orders/{order_id}", json={"status": "CONFIRMED"}
    )
    assert response.status_code == 422


def test_mandate_transition_alias_is_available():
    order_id = create_order()
    response = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
        endpoint_prefix="/api",
    )
    assert response.status_code == 200, response.text
    assert response.json()["current_state"] == "CONFIRMED"


def test_legal_happy_path_through_full_lifecycle():
    order_id = create_order()
    vehicle_id = str(uuid4())

    assert confirm(order_id).json()["current_state"] == "CONFIRMED"
    assert (
        transition(
            order_id,
            "RINGING",
            "vehicle_reserved",
            actor_role="TMS",
            payload={
                "vehicle_id": vehicle_id,
                "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
            },
        ).json()["current_state"]
        == "RINGING"
    )
    assert (
        transition(
            order_id,
            "ASSIGNED",
            "driver_response",
            actor_role="DRIVER",
            payload={"driver_id": "driver-1", "vehicle_id": vehicle_id, "action": "ACCEPT"},
        ).json()["current_state"]
        == "ASSIGNED"
    )

    for state, event in [
        ("EN_ROUTE_TO_PICKUP", "driver_started_pickup"),
        ("AT_PICKUP_WAITING", "driver_arrived_pickup"),
    ]:
        response = transition(order_id, state, event, actor_role="DRIVER")
        assert response.status_code == 200, response.text

    response = transition(
        order_id,
        "LOADING",
        "shipment_doc_scanned",
        actor_role="DRIVER",
        payload={
            "driver_id": "driver-1",
            "vehicle_id": vehicle_id,
            "doc_type": "invoice",
            "doc_url": "s3://docs/invoice.jpg",
            "scan_exif": {"lat": 19.07},
        },
    )
    assert response.status_code == 200, response.text

    for state, event in [
        ("DEPARTED_FOR_DELIVERY", "loading_completed"),
        ("AT_DELIVERY_WAITING", "driver_arrived_delivery"),
    ]:
        response = transition(order_id, state, event, actor_role="DRIVER")
        assert response.status_code == 200, response.text

    response = transition(
        order_id,
        "DELIVERED_PENDING_SETTLEMENT",
        "pod_scanned",
        actor_role="DRIVER",
        payload={
            "driver_id": "driver-1",
            "pod_url": "s3://docs/pod.jpg",
            "consignee_otp": "123456",
            "verification_status": "VERIFIED",
            "pod_exif": {"lat": 28.61},
        },
    )
    assert response.status_code == 200, response.text

    response = transition(
        order_id,
        "COMPLETED",
        "payment_captured",
        actor_role="FIN",
        payload={"payment_id": "pay-1", "amount": 25000, "currency": "INR"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["current_state"] == "COMPLETED"


def test_illegal_skipped_transition_blocked_and_dlq_written():
    order_id = create_order()
    before = _dlq_count()
    response = transition(
        order_id,
        "ASSIGNED",
        "skip_matching",
        actor_role="TMS",
    )
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == "INVALID_INPUT"
    assert _dlq_count() == before + 1


def test_role_transition_blocked():
    order_id = create_order()
    response = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        actor_role="CUSTOMER",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"]["error_code"] == "POLICY_VIOLATION"


def test_topay_blocked_until_accepted_consent():
    order_id = create_order()
    blocked = confirm(
        order_id,
        {
            "payment_mode": "topay",
            "topay_consent_status": "pending",
        },
    )
    assert blocked.status_code == 409

    allowed = confirm(
        order_id,
        {
            "payment_mode": "topay",
            "topay_consent_status": "accepted",
        },
    )
    assert allowed.status_code == 200, allowed.text


def test_pharma_blocked_unless_closed_body():
    order_id = create_order()
    blocked = confirm(
        order_id,
        {
            "material_type": "pharma",
            "body_type_required": "open",
        },
    )
    assert blocked.status_code == 409

    allowed = confirm(
        order_id,
        {
            "material_type": "pharma",
            "body_type_required": "closed",
        },
    )
    assert allowed.status_code == 200, allowed.text


def test_event_specific_payload_validation():
    order_id = create_order()
    assert confirm(order_id).status_code == 200
    response = transition(
        order_id,
        "RINGING",
        "vehicle_reserved",
        actor_role="TMS",
        payload={"vehicle_id": str(uuid4())},
    )
    assert response.status_code == 422


def test_transition_idempotency_replay():
    order_id = create_order()
    idempotency_key = str(uuid4())
    payload = {
        "payment_mode": "advance",
        "topay_consent_status": "not_required",
        "material_type": "general_goods",
        "body_type_required": "open",
    }
    first = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload=payload,
        idempotency_key=idempotency_key,
    )
    second = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload=payload,
        idempotency_key=idempotency_key,
    )
    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert second.json()["current_state"] == "CONFIRMED"


def test_transition_idempotency_mismatch_blocked():
    order_id = create_order()
    idempotency_key = str(uuid4())
    first = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
        idempotency_key=idempotency_key,
    )
    second = transition(
        order_id,
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "full",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
        idempotency_key=idempotency_key,
    )
    assert first.status_code == 200, first.text
    assert second.status_code == 409
    assert second.json()["detail"]["error_code"] == "CONFLICT"


def test_driver_doc_and_pod_schema_validation():
    order_id = create_order()
    vehicle_id = str(uuid4())
    assert confirm(order_id).status_code == 200
    assert (
        transition(
            order_id,
            "RINGING",
            "vehicle_reserved",
            actor_role="TMS",
            payload={
                "vehicle_id": vehicle_id,
                "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
            },
        ).status_code
        == 200
    )
    bad_driver = transition(
        order_id,
        "ASSIGNED",
        "driver_response",
        actor_role="DRIVER",
        payload={"driver_id": "driver-1", "vehicle_id": vehicle_id, "action": "MAYBE"},
    )
    assert bad_driver.status_code == 422


def test_active_vehicle_reservation_blocks_double_booking_until_expired():
    vehicle_id = str(uuid4())
    order_one = create_order()
    order_two = create_order()
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()

    assert confirm(order_one).status_code == 200
    assert confirm(order_two).status_code == 200
    first = transition(
        order_one,
        "RINGING",
        "vehicle_reserved",
        actor_role="TMS",
        payload={"vehicle_id": vehicle_id, "expires_at": expires_at},
    )
    assert first.status_code == 200, first.text

    blocked = transition(
        order_two,
        "RINGING",
        "vehicle_reserved",
        actor_role="TMS",
        payload={"vehicle_id": vehicle_id, "expires_at": expires_at},
    )
    assert blocked.status_code == 409

    db = SessionLocal()
    try:
        db.query(VehicleReservation).filter(
            VehicleReservation.vehicle_id == UUID(vehicle_id)
        ).update(
            {
                VehicleReservation.expires_at: datetime.now(timezone.utc)
                - timedelta(minutes=1)
            },
            synchronize_session=False,
        )
        db.commit()
    finally:
        db.close()

    released = transition(
        order_two,
        "RINGING",
        "vehicle_reserved",
        actor_role="TMS",
        payload={"vehicle_id": vehicle_id, "expires_at": expires_at},
    )
    assert released.status_code == 200, released.text


def test_transition_event_written():
    order_id = create_order()
    response = confirm(order_id)
    assert response.status_code == 200, response.text

    events = client.get(f"/api/v1/orders/{order_id}/events")
    assert events.status_code == 200
    data = events.json()
    assert data["total"] >= 1
    assert data["events"][-1]["to_state"] == "CONFIRMED"
    assert data["events"][-1]["event_name"] == "order_submitted"


def test_cancel_order():
    order_id = create_order()
    response = client.post(f"/api/v1/orders/{order_id}/cancel")
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "CANCELLED"


def test_order_stats():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_orders" in data
    assert "by_status" in data


def test_create_order_invalid_cargo():
    invalid_order = SAMPLE_ORDER.copy()
    invalid_order["cargo_type"] = "invalid_type"
    response = client.post("/api/v1/orders", json=invalid_order)
    assert response.status_code == 400


def test_list_matches():
    response = client.get("/api/v1/matches")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "matches" in data


def test_match_stats():
    response = client.get("/api/v1/matches/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_matches" in data
    assert "by_status" in data


def _dlq_count() -> int:
    db = SessionLocal()
    try:
        return db.query(AgentDLQMessage).count()
    finally:
        db.close()
