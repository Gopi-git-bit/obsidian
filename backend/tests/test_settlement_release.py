"""Settlement release guardrails and MVP golden path."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.auth_model import UserAccount
from app.models.flow_model import GSTInvoiceRecord, JournalEntry, SettlementRecord, Trip, TripMilestone
from app.models.outbox_model import EventOutbox
from app.models.policy_model import PolicyDecision
from app.models.supervisor_model import SettlementHold
from app.models.vehicle_model import VehicleModel
from conftest import auth_headers


client = TestClient(app)


ORDER = {
    "shipper_name": "Settlement Customer",
    "shipper_phone": "9876543210",
    "shipper_email": "settlement@example.com",
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
        return str(db.query(UserAccount).filter(UserAccount.username == username).one().id)
    finally:
        db.close()


def _seed_vehicle() -> str:
    db = SessionLocal()
    try:
        vehicle = VehicleModel(
            manufacturer="Settlement Motors",
            model_name=f"LCV Settlement {uuid4()}",
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


def _settlement_payload(idempotency_key: str | None = None) -> dict:
    key = idempotency_key or f"settlement-{uuid4()}"
    return {
        "amount": 18000,
        "commission_amount": 1800,
        "gst_amount": 324,
        "driver_payable_amount": 16200,
        "currency": "INR",
        "idempotency_key": key,
        "trace_id": f"settlement-trace-{uuid4()}",
        "confidence_score": 0.91,
        "decision_reason": "Finance settlement release preflight",
        "evidence_refs": ["pod:verified", "otp:verified"],
    }


def _transition(headers: dict[str, str], order_id: str, to_state: str, event: str, *, actor_role: str = "OMS", payload: dict | None = None):
    response = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": to_state,
            "event": event,
            "payload": payload or {},
            "actor_role": actor_role,
            "idempotency_key": str(uuid4()),
            "trace_id": f"settlement-{uuid4()}",
        },
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()


def _create_verified_trip(*, driver_username: str | None = None, verify_with_role: str = "supervisor", assert_driver_verify_blocked: bool = False) -> tuple[str, str, dict[str, str]]:
    admin = auth_headers(client, "super_admin", username=f"settlement-admin-{uuid4()}")
    customer = auth_headers(client, "customer", username=f"settlement-customer-{uuid4()}")
    driver_username = driver_username or f"settlement-driver-{uuid4()}"
    driver = auth_headers(client, "driver", username=driver_username)
    vehicle_id = _seed_vehicle()

    order = client.post("/api/v1/orders", json=ORDER, headers=customer)
    assert order.status_code == 201, order.text
    order_id = order.json()["id"]

    _transition(
        admin,
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
    matches = client.get(f"/api/v1/orders/{order_id}/match?limit=20&min_score=0", headers=admin)
    assert matches.status_code == 200, matches.text
    match = next(item for item in matches.json()["matches"] if item["vehicle_id"] == vehicle_id)
    accepted = client.post(f"/api/v1/matches/{match['match_id']}/accept", json={}, headers=admin)
    assert accepted.status_code == 200, accepted.text
    trip = client.get(f"/api/v1/orders/{order_id}/trip", headers=admin)
    assert trip.status_code == 200, trip.text
    trip_id = trip.json()["trip_id"]

    assigned = client.post(f"/api/v1/trips/{trip_id}/assign-driver", json={"driver_id": _user_id(driver_username)}, headers=admin)
    assert assigned.status_code == 200, assigned.text

    _transition(admin, order_id, "EN_ROUTE_TO_PICKUP", "driver_started_pickup", actor_role="DRIVER")
    _transition(admin, order_id, "AT_PICKUP_WAITING", "driver_arrived_pickup", actor_role="DRIVER")
    _transition(
        admin,
        order_id,
        "LOADING",
        "shipment_doc_scanned",
        actor_role="DRIVER",
        payload={"driver_id": driver_username, "vehicle_id": vehicle_id, "doc_type": "loading_photo", "doc_url": "s3://docs/loading.jpg", "scan_exif": {}},
    )
    _transition(admin, order_id, "DEPARTED_FOR_DELIVERY", "loading_completed", actor_role="DRIVER")
    _transition(admin, order_id, "AT_DELIVERY_WAITING", "driver_arrived_delivery", actor_role="DRIVER")

    pod = client.post(
        f"/api/v1/trips/{trip_id}/pod",
        json={"pod_url": "s3://docs/pod.jpg", "consignee_otp": "123456", "pod_exif": {}, "uploaded_by": driver_username, "idempotency_key": f"pod-{uuid4()}"},
        headers=driver,
    )
    assert pod.status_code == 201, pod.text

    if assert_driver_verify_blocked:
        blocked_pod = client.post(f"/api/v1/trips/{trip_id}/pod/verify", json={"verified_by": driver_username, "idempotency_key": f"podv-{uuid4()}"}, headers=driver)
        assert blocked_pod.status_code == 403
        blocked_otp = client.post(f"/api/v1/trips/{trip_id}/otp/verify", json={"otp": "123456", "verified_by": driver_username, "idempotency_key": f"otp-{uuid4()}"}, headers=driver)
        assert blocked_otp.status_code == 403

    verifier = auth_headers(client, verify_with_role, username=f"settlement-verifier-{uuid4()}")
    pod_verified = client.post(f"/api/v1/trips/{trip_id}/pod/verify", json={"verified_by": verify_with_role, "idempotency_key": f"podv-{uuid4()}"}, headers=verifier)
    assert pod_verified.status_code == 200, pod_verified.text
    otp_verified = client.post(f"/api/v1/trips/{trip_id}/otp/verify", json={"otp": "123456", "verified_by": verify_with_role, "idempotency_key": f"otp-{uuid4()}"}, headers=verifier)
    assert otp_verified.status_code == 200, otp_verified.text
    return order_id, trip_id, admin


def _audit_count(trip_id: str, milestone_type: str, status: str | None = None) -> int:
    db = SessionLocal()
    try:
        query = db.query(TripMilestone).filter(TripMilestone.trip_id == UUID(trip_id), TripMilestone.milestone_type == milestone_type)
        if status:
            query = query.filter(TripMilestone.status == status)
        return query.count()
    finally:
        db.close()


def _outbox_events(event_type: str, aggregate_id: str | None = None) -> list[EventOutbox]:
    db = SessionLocal()
    try:
        query = db.query(EventOutbox).filter(EventOutbox.event_type == event_type)
        if aggregate_id:
            query = query.filter(EventOutbox.aggregate_id == UUID(aggregate_id))
        return list(query.all())
    finally:
        db.close()


def _policy_decisions(idempotency_key: str) -> list[PolicyDecision]:
    db = SessionLocal()
    try:
        return list(db.query(PolicyDecision).filter(PolicyDecision.idempotency_key == idempotency_key).all())
    finally:
        db.close()


def _settlement_mutation_count(order_id: str) -> int:
    db = SessionLocal()
    try:
        order_uuid = UUID(order_id)
        return (
            db.query(SettlementRecord).filter(SettlementRecord.order_id == order_uuid).count()
            + db.query(JournalEntry).filter(JournalEntry.order_id == order_uuid).count()
            + db.query(GSTInvoiceRecord).filter(GSTInvoiceRecord.order_id == order_uuid).count()
        )
    finally:
        db.close()


def test_settlement_release_blocked_by_fraud_hold_and_audited():
    order_id, trip_id, _admin = _create_verified_trip()
    supervisor = auth_headers(client, "supervisor", username=f"fraud-supervisor-{uuid4()}")
    held = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "fraud risk"}, headers=supervisor)
    assert held.status_code == 200, held.text

    finance = auth_headers(client, "finance_admin", username=f"fraud-finance-{uuid4()}")
    payload = _settlement_payload()
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["blocker"] == "fraud_hold"
    replayed = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert replayed.status_code == 409
    assert _audit_count(trip_id, "settlement_release_blocked", "blocked") == 1
    events = _outbox_events("settlement.release_blocked", trip_id)
    assert len(events) == 1
    assert events[0].payload["blocker_code"] == "FRAUD_HOLD_ACTIVE"


def test_settlement_release_blocked_by_settlement_hold_then_released_after_supervisor_clearance():
    _order_id, trip_id, _admin = _create_verified_trip()
    supervisor = auth_headers(client, "supervisor", username=f"settlement-hold-supervisor-{uuid4()}")
    held = client.post(f"/api/v1/supervisor/trips/{trip_id}/settlement-hold", json={"reason": "settlement review"}, headers=supervisor)
    assert held.status_code == 200, held.text
    assert held.json()["settlement_holds"][0]["trip_id"] == trip_id

    finance = auth_headers(client, "finance_admin", username=f"settlement-hold-finance-{uuid4()}")
    payload = _settlement_payload()
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["blocker"] == "settlement_hold"
    replayed = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert replayed.status_code == 409
    blocked_events = [event for event in _outbox_events("settlement.release_blocked", trip_id) if event.payload["blocker_code"] == "SETTLEMENT_HOLD_ACTIVE"]
    assert len(blocked_events) == 1
    assert len(_outbox_events("settlement.hold_created", trip_id)) == 1

    cleared = client.post(f"/api/v1/supervisor/settlements/{trip_id}/release-hold", json={"reason": "cleared"}, headers=supervisor)
    assert cleared.status_code == 200, cleared.text
    assert len(_outbox_events("settlement.hold_cleared", trip_id)) == 1
    released = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert released.status_code == 201, released.text
    assert released.json()["status"] == "released"
    assert _audit_count(trip_id, "settlement_released", "released") == 1


def test_wrong_role_cannot_release_settlement():
    _order_id, trip_id, _admin = _create_verified_trip()
    wrong = auth_headers(client, "ops_admin", username=f"wrong-finance-{uuid4()}")
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=_settlement_payload(), headers=wrong)
    assert blocked.status_code == 403


def test_settlement_release_creates_policy_decision_before_release():
    _order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"policy-release-finance-{uuid4()}")
    payload = _settlement_payload()

    released = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert released.status_code == 201, released.text

    decisions = _policy_decisions(payload["idempotency_key"])
    assert len(decisions) == 1
    assert decisions[0].requested_action == "settlement.release"
    assert decisions[0].result == "approved"
    assert decisions[0].trace_id == payload["trace_id"]


def test_settlement_policy_hold_blocks_before_accounting_mutations():
    order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"policy-hold-finance-{uuid4()}")
    payload = _settlement_payload()
    payload["confidence_score"] = 0.5

    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["detail"]["reason_code"] == "LOW_CONFIDENCE_REVIEW_REQUIRED"
    assert _settlement_mutation_count(order_id) == 0
    decisions = _policy_decisions(payload["idempotency_key"])
    assert len(decisions) == 1
    assert decisions[0].result == "hold"
    assert len(_outbox_events("policy.check_hold", trip_id)) == 1


def test_settlement_policy_reject_blocks_before_accounting_mutations():
    order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"policy-reject-finance-{uuid4()}")
    payload = _settlement_payload()
    payload.update({"route_zone": "TN_TO_KA", "proposed_margin_pct": 1, "vehicle_supply_pct": 100})

    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["detail"]["reason_code"] == "ROUTE_MARGIN_FLOOR_VIOLATION"
    assert _settlement_mutation_count(order_id) == 0
    decisions = _policy_decisions(payload["idempotency_key"])
    assert len(decisions) == 1
    assert decisions[0].result == "rejected"
    assert len(_outbox_events("policy.check_rejected", trip_id)) == 1


def test_settlement_release_missing_trace_and_idempotency_are_policy_rejections():
    order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"policy-meta-finance-{uuid4()}")

    missing_trace = _settlement_payload()
    missing_trace["trace_id"] = None
    blocked_trace = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=missing_trace, headers=finance)
    assert blocked_trace.status_code == 409, blocked_trace.text
    assert blocked_trace.json()["detail"]["reason_code"] == "TRACE_ID_REQUIRED"
    assert _policy_decisions(missing_trace["idempotency_key"])[0].result == "rejected"

    missing_idem = _settlement_payload()
    missing_idem.pop("idempotency_key")
    blocked_idem = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=missing_idem, headers=finance)
    assert blocked_idem.status_code == 409, blocked_idem.text
    assert blocked_idem.json()["detail"]["reason_code"] == "IDEMPOTENCY_KEY_REQUIRED"
    assert _settlement_mutation_count(order_id) == 0


def test_duplicate_settlement_release_is_idempotent_and_does_not_double_post_accounting():
    order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"duplicate-finance-{uuid4()}")
    key = f"settlement-duplicate-{uuid4()}"
    payload = _settlement_payload(key)

    first = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert first.status_code == 201, first.text
    second = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=payload, headers=finance)
    assert second.status_code == 201, second.text
    assert second.json()["settlement_id"] == first.json()["settlement_id"]
    assert second.json()["status"] == "released"

    db = SessionLocal()
    try:
        order_uuid = UUID(order_id)
        assert db.query(SettlementRecord).filter(SettlementRecord.idempotency_key == key).count() == 1
        assert db.query(JournalEntry).filter(JournalEntry.order_id == order_uuid).count() == 1
        assert db.query(GSTInvoiceRecord).filter(GSTInvoiceRecord.order_id == order_uuid).count() == 1
        assert db.query(PolicyDecision).filter(PolicyDecision.idempotency_key == key).count() == 1
    finally:
        db.close()
    assert _audit_count(trip_id, "settlement_released", "released") == 1
    assert _audit_count(trip_id, "settlement_release_replayed", "released") == 1
    settlement_id = first.json()["settlement_id"]
    assert len(_outbox_events("settlement.released", settlement_id)) == 1
    assert len(_outbox_events("finance.journal_created", settlement_id)) == 1
    assert len(_outbox_events("finance.gst_invoice_created", settlement_id)) == 1


def test_full_mvp_golden_path_with_hold_clearance_and_audit_trail():
    driver_username = f"golden-driver-{uuid4()}"
    order_id, trip_id, _admin = _create_verified_trip(driver_username=driver_username, verify_with_role="supervisor", assert_driver_verify_blocked=True)
    supervisor = auth_headers(client, "supervisor", username=f"golden-supervisor-{uuid4()}")
    finance = auth_headers(client, "finance_admin", username=f"golden-finance-{uuid4()}")

    fraud_hold = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "golden fraud review"}, headers=supervisor)
    assert fraud_hold.status_code == 200, fraud_hold.text
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=_settlement_payload(), headers=finance)
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["blocker"] == "fraud_hold"

    cleared = client.post(f"/api/v1/supervisor/cases/{fraud_hold.json()['case']['case_id']}/approve", json={"reason": "cleared for payment"}, headers=supervisor)
    assert cleared.status_code == 200, cleared.text
    released = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=_settlement_payload(), headers=finance)
    assert released.status_code == 201, released.text

    db = SessionLocal()
    try:
        trip = db.query(Trip).filter(Trip.trip_id == UUID(trip_id)).one()
        assert trip.order_id == UUID(order_id)
        assert db.query(SettlementHold).filter(SettlementHold.trip_id == UUID(trip_id), SettlementHold.is_active == True).count() == 0
        audit_types = {
            row.milestone_type
            for row in db.query(TripMilestone).filter(TripMilestone.trip_id == UUID(trip_id)).all()
        }
        assert {"pod_uploaded", "pod_verified", "otp_verified", "settlement_release_blocked", "settlement_released"}.issubset(audit_types)
    finally:
        db.close()


def test_finance_settlement_queue_requires_finance_role_and_shows_blocker():
    order_id, trip_id, _admin = _create_verified_trip()
    supervisor = auth_headers(client, "supervisor", username=f"queue-supervisor-{uuid4()}")
    held = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "queue fraud review"}, headers=supervisor)
    assert held.status_code == 200, held.text

    wrong = auth_headers(client, "ops_admin", username=f"queue-wrong-{uuid4()}")
    assert client.get("/api/v1/finance/settlements", headers=wrong).status_code == 403

    finance = auth_headers(client, "finance_admin", username=f"queue-finance-{uuid4()}")
    listed = client.get("/api/v1/finance/settlements", headers=finance)
    assert listed.status_code == 200, listed.text
    item = next(row for row in listed.json()["settlements"] if row["trip_id"] == trip_id)
    assert item["order_id"] == order_id
    assert item["blocker_code"] == "FRAUD_HOLD_ACTIVE"
    assert item["blocker_reason"] == "queue fraud review"
    assert item["release_eligible"] is False


def test_finance_settlement_detail_returns_released_accounting_and_audit():
    _order_id, trip_id, _admin = _create_verified_trip()
    finance = auth_headers(client, "finance_admin", username=f"detail-finance-{uuid4()}")
    released = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=_settlement_payload(), headers=finance)
    assert released.status_code == 201, released.text

    detail = client.get(f"/api/v1/finance/settlements/{trip_id}", headers=finance)
    assert detail.status_code == 200, detail.text
    body = detail.json()
    assert body["release_status"] == "released"
    assert body["settlement"]["settlement_id"] == released.json()["settlement_id"]
    assert body["journal_created"] is True
    assert body["gst_invoice_created"] is True
    assert body["journal_id"]
    assert body["gst_invoice_id"]
    assert "settlement_released" in {item["milestone_type"] for item in body["audit_trail"]}
    assert "settlement.released" in {item["event_type"] for item in body["outbox_events"]}


def test_outbox_read_rbac_and_mark_status_controls():
    order_id, trip_id, _admin = _create_verified_trip()
    supervisor = auth_headers(client, "supervisor", username=f"outbox-supervisor-{uuid4()}")
    held = client.post(f"/api/v1/supervisor/orders/{order_id}/fraud-hold", json={"reason": "outbox fraud"}, headers=supervisor)
    assert held.status_code == 200, held.text
    finance = auth_headers(client, "finance_admin", username=f"outbox-finance-{uuid4()}")
    blocked = client.post(f"/api/v1/trips/{trip_id}/settlements/release", json=_settlement_payload(), headers=finance)
    assert blocked.status_code == 409

    wrong = auth_headers(client, "customer", username=f"outbox-wrong-{uuid4()}")
    assert client.get("/api/v1/outbox/events", headers=wrong).status_code == 403

    finance_events = client.get("/api/v1/outbox/events", headers=finance)
    assert finance_events.status_code == 200, finance_events.text
    finance_types = {event["event_type"] for event in finance_events.json()["events"]}
    assert "settlement.release_blocked" in finance_types
    assert "fraud.hold_created" not in finance_types

    supervisor_events = client.get("/api/v1/outbox/events", headers=supervisor)
    assert supervisor_events.status_code == 200, supervisor_events.text
    supervisor_types = {event["event_type"] for event in supervisor_events.json()["events"]}
    assert "fraud.hold_created" in supervisor_types
    assert "settlement.release_blocked" in supervisor_types

    super_admin = auth_headers(client, "super_admin", username=f"outbox-admin-{uuid4()}")
    all_events = client.get("/api/v1/outbox/events", headers=super_admin)
    assert all_events.status_code == 200
    event_id = next(event["event_id"] for event in all_events.json()["events"] if event["event_type"] == "settlement.release_blocked")

    dispatched = client.post(f"/api/v1/outbox/events/{event_id}/mark-dispatched", json={}, headers=super_admin)
    assert dispatched.status_code == 200, dispatched.text
    assert dispatched.json()["status"] == "dispatched"
    assert dispatched.json()["dispatched_at"]

    failed = client.post(f"/api/v1/outbox/events/{event_id}/mark-failed", json={"error": "worker timeout"}, headers=super_admin)
    assert failed.status_code == 200, failed.text
    assert failed.json()["status"] == "failed"
    assert failed.json()["attempts"] == 1
    assert failed.json()["last_error"] == "worker timeout"
