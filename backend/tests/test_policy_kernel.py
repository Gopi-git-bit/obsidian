"""Deterministic policy kernel checks."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.outbox_model import EventOutbox
from app.models.policy_model import PolicyDecision
from conftest import auth_headers


client = TestClient(app)


def _payload(**overrides):
    base = {
        "agent_code": "FIN",
        "entity_type": "settlement",
        "entity_id": str(uuid4()),
        "requested_action": "settlement.release",
        "decision_reason": "Finance agent recommends release after controls pass",
        "trace_id": f"trace-{uuid4()}",
        "idempotency_key": f"policy-{uuid4()}",
        "confidence_score": 0.91,
        "evidence_refs": ["trip:verified-pod", "otp:verified"],
        "payload": {"route_zone": "TN_TO_KA", "proposed_margin_pct": 12.5, "vehicle_supply_pct": 20},
    }
    base.update(overrides)
    return base


def _decision_count(idempotency_key: str) -> int:
    db = SessionLocal()
    try:
        return db.query(PolicyDecision).filter(PolicyDecision.idempotency_key == idempotency_key).count()
    finally:
        db.close()


def test_valid_policy_check_approved_and_recorded():
    headers = auth_headers(client, "finance_admin", username=f"policy-finance-{uuid4()}")
    payload = _payload()
    response = client.post("/api/v1/policy/check", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["approved"] is True
    assert body["result"] == "approved"
    assert body["reason_code"] == "POLICY_APPROVED"
    assert body["policy_version"] == "1.0"

    db = SessionLocal()
    try:
        decision = db.query(PolicyDecision).filter(PolicyDecision.decision_id == UUID(body["decision_id"])).one()
        assert decision.agent_code == "FIN"
        assert decision.trace_id == payload["trace_id"]
        assert decision.idempotency_key == payload["idempotency_key"]
    finally:
        db.close()


def test_missing_trace_id_rejected_and_durable():
    headers = auth_headers(client, "finance_admin", username=f"policy-missing-trace-{uuid4()}")
    response = client.post("/api/v1/policy/check", json=_payload(trace_id=None), headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["result"] == "rejected"
    assert response.json()["reason_code"] == "TRACE_ID_REQUIRED"


def test_missing_idempotency_key_rejected_and_durable():
    headers = auth_headers(client, "finance_admin", username=f"policy-missing-idem-{uuid4()}")
    response = client.post("/api/v1/policy/check", json=_payload(idempotency_key=None), headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["result"] == "rejected"
    assert response.json()["reason_code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_wrong_role_blocked():
    headers = auth_headers(client, "customer", username=f"policy-wrong-{uuid4()}")
    response = client.post("/api/v1/policy/check", json=_payload(), headers=headers)
    assert response.status_code == 403


def test_low_confidence_triggers_hold_review_and_outbox_event():
    headers = auth_headers(client, "finance_admin", username=f"policy-low-conf-{uuid4()}")
    payload = _payload(confidence_score=0.5)
    response = client.post("/api/v1/policy/check", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["result"] == "hold"
    assert body["reason_code"] == "LOW_CONFIDENCE_REVIEW_REQUIRED"
    assert body["requires_human_review"] is True

    db = SessionLocal()
    try:
        assert db.query(EventOutbox).filter(EventOutbox.event_type == "policy.check_hold").count() >= 1
    finally:
        db.close()


def test_invalid_state_transition_rejected():
    headers = auth_headers(client, "ops_admin", username=f"policy-state-{uuid4()}")
    payload = _payload(
        agent_code="OMS",
        entity_type="order",
        requested_action="order.transition",
        confidence_score=0.9,
        payload={"from_state": "CREATED", "to_state": "COMPLETED"},
    )
    response = client.post("/api/v1/policy/check", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["result"] == "rejected"
    assert response.json()["reason_code"] == "INVALID_STATE_TRANSITION"


def test_forbidden_agent_action_rejected():
    headers = auth_headers(client, "finance_admin", username=f"policy-forbidden-{uuid4()}")
    payload = _payload(agent_code="FIN", requested_action="pod.verify")
    response = client.post("/api/v1/policy/check", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    assert response.json()["result"] == "rejected"
    assert response.json()["reason_code"] == "FORBIDDEN_AGENT_ACTION"


def test_duplicate_idempotency_key_returns_existing_decision():
    headers = auth_headers(client, "finance_admin", username=f"policy-dupe-{uuid4()}")
    key = f"policy-dupe-{uuid4()}"
    payload = _payload(idempotency_key=key)
    first = client.post("/api/v1/policy/check", json=payload, headers=headers)
    assert first.status_code == 200, first.text
    second_payload = _payload(idempotency_key=key, confidence_score=0.1)
    second = client.post("/api/v1/policy/check", json=second_payload, headers=headers)
    assert second.status_code == 200, second.text
    assert second.json()["decision_id"] == first.json()["decision_id"]
    assert second.json()["result"] == first.json()["result"]
    assert _decision_count(key) == 1
