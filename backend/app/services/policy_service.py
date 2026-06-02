"""Deterministic policy validation kernel."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.order_model import OrderStatus
from app.models.policy_model import (
    ComplianceDocumentRule,
    ConfidenceThreshold,
    PolicyDecision,
    PolicyRegistry,
    RouteZonePolicy,
)
from app.services.order_service import ORDER_STATE_GRAPH, parse_order_status
from app.services.outbox_service import emit_outbox_event, outbox_key

POLICY_CODE = "zippy-agent-policy-framework"
DEFAULT_POLICY_VERSION = "1.0"

AGENT_ALLOWED_ACTIONS = {
    "SUP": {"policy.check", "case.hold", "case.approve", "case.reject", "fraud.hold", "settlement.hold", "settlement.hold.clear"},
    "OMS": {"order.transition", "state.transition", "order.submit", "order.cancel", "document.validate", "workflow.trigger"},
    "IMS": {"vehicle.match", "vehicle.rank", "capacity.recommend"},
    "TMS": {"state.transition", "route.plan", "route.reroute", "eta.update", "shipment.milestone"},
    "FIN": {"state.transition", "settlement.release", "settlement.check", "payment.record", "invoice.generate", "journal.create", "gst.invoice.create"},
    "DISPUTE": {"dispute.score", "refund.recommend", "exception.raise"},
    "COMMS": {"notification.draft", "notification.trigger"},
    "ADMIN_OPS": {"state.transition", "driver.verify", "audit.query", "privacy.mask", "compliance.check"},
}


@dataclass(frozen=True)
class PolicyOutcome:
    result: str
    reason_code: str
    requires_human_review: bool = False


def active_policy_version(db: Session) -> str:
    policy = (
        db.query(PolicyRegistry)
        .filter(PolicyRegistry.policy_code == POLICY_CODE, PolicyRegistry.status == "active")
        .order_by(PolicyRegistry.effective_at.desc())
        .first()
    )
    return policy.policy_version if policy else DEFAULT_POLICY_VERSION


def decision_category(entity_type: str, requested_action: str) -> str:
    probe = f"{entity_type}.{requested_action}".lower()
    if any(term in probe for term in ("finance", "settlement", "payment", "invoice", "journal", "gst", "margin")):
        return "financial"
    if any(term in probe for term in ("compliance", "document", "eway", "e-way", "permit")):
        return "compliance"
    if any(term in probe for term in ("notification", "message", "comms")):
        return "communication"
    return "operational"


def validate_idempotency_trace(trace_id: str | None, idempotency_key: str | None) -> PolicyOutcome | None:
    if not trace_id:
        return PolicyOutcome("rejected", "TRACE_ID_REQUIRED")
    if not idempotency_key:
        return PolicyOutcome("rejected", "IDEMPOTENCY_KEY_REQUIRED")
    return None


def validate_agent_role(agent_code: str, requested_action: str) -> PolicyOutcome | None:
    allowed = AGENT_ALLOWED_ACTIONS.get(agent_code)
    if not allowed:
        return PolicyOutcome("rejected", "UNKNOWN_AGENT_CODE")
    if requested_action not in allowed:
        return PolicyOutcome("rejected", "FORBIDDEN_AGENT_ACTION")
    return None


def validate_state_transition(payload: dict) -> PolicyOutcome | None:
    if "from_state" not in payload and "to_state" not in payload:
        return None
    try:
        from_state = parse_order_status(str(payload.get("from_state", "")))
        to_state = parse_order_status(str(payload.get("to_state", "")))
    except Exception:
        return PolicyOutcome("rejected", "INVALID_STATE")
    if to_state not in ORDER_STATE_GRAPH.get(from_state, set()):
        return PolicyOutcome("rejected", "INVALID_STATE_TRANSITION")
    return None


def validate_confidence_threshold(db: Session, category: str, confidence_score: float | None) -> PolicyOutcome | None:
    if confidence_score is None:
        return PolicyOutcome("hold", "CONFIDENCE_SCORE_REQUIRED", True)
    threshold = db.query(ConfidenceThreshold).filter(ConfidenceThreshold.decision_category == category).first()
    minimum = float(threshold.minimum_confidence) if threshold else 0.75
    if confidence_score < minimum:
        return PolicyOutcome("hold", "LOW_CONFIDENCE_REVIEW_REQUIRED", True)
    return None


def validate_route_margin_floor(db: Session, payload: dict) -> PolicyOutcome | None:
    route_zone = payload.get("route_zone")
    if not route_zone or "proposed_margin_pct" not in payload:
        return None
    row = db.query(RouteZonePolicy).filter(RouteZonePolicy.route_zone == route_zone).first()
    if not row:
        return PolicyOutcome("rejected", "UNKNOWN_ROUTE_ZONE")
    proposed = Decimal(str(payload["proposed_margin_pct"]))
    supply_pct = Decimal(str(payload.get("vehicle_supply_pct", "100")))
    minimum = Decimal(row.min_gross_margin_pct)
    if supply_pct < Decimal(row.vehicle_supply_threshold_pct):
        minimum -= Decimal(row.crisis_margin_buffer_pct)
    if proposed < minimum:
        return PolicyOutcome("rejected", "ROUTE_MARGIN_FLOOR_VIOLATION")
    return None


def validate_required_documents(db: Session, payload: dict) -> PolicyOutcome | None:
    shipment_type = payload.get("shipment_type")
    route_type = payload.get("route_type")
    if not shipment_type or not route_type:
        return None
    provided = set(payload.get("documents") or [])
    rules = (
        db.query(ComplianceDocumentRule)
        .filter(
            ComplianceDocumentRule.shipment_type == shipment_type,
            ComplianceDocumentRule.route_type == route_type,
            ComplianceDocumentRule.mandatory == True,
        )
        .all()
    )
    missing = [rule.document_name for rule in rules if rule.document_name not in provided]
    if missing:
        return PolicyOutcome("rejected", "REQUIRED_DOCUMENT_MISSING")
    return None


def validate_action_policy(db: Session, *, agent_code: str, entity_type: str, requested_action: str, confidence_score: float | None, payload: dict, trace_id: str | None, idempotency_key: str | None) -> PolicyOutcome:
    for check in (
        validate_idempotency_trace(trace_id, idempotency_key),
        validate_agent_role(agent_code, requested_action),
        validate_state_transition(payload) if requested_action in {"order.transition", "state.transition"} else None,
        validate_route_margin_floor(db, payload),
        validate_required_documents(db, payload),
    ):
        if check:
            return check
    confidence = validate_confidence_threshold(db, decision_category(entity_type, requested_action), confidence_score)
    if confidence:
        return confidence
    return PolicyOutcome("approved", "POLICY_APPROVED")


def record_policy_decision(
    db: Session,
    *,
    agent_code: str,
    entity_type: str,
    entity_id: str,
    requested_action: str,
    decision_reason: str | None,
    trace_id: str | None,
    idempotency_key: str | None,
    confidence_score: float | None,
    evidence_refs: list,
    payload: dict,
    outcome: PolicyOutcome,
) -> PolicyDecision:
    existing = db.query(PolicyDecision).filter(PolicyDecision.idempotency_key == idempotency_key).first() if idempotency_key else None
    if existing:
        return existing
    decision = PolicyDecision(
        agent_code=agent_code,
        entity_type=entity_type,
        entity_id=str(entity_id),
        requested_action=requested_action,
        decision_reason=decision_reason,
        trace_id=trace_id,
        idempotency_key=idempotency_key,
        confidence_score=confidence_score,
        evidence_refs=evidence_refs or [],
        payload=payload or {},
        policy_version=active_policy_version(db),
        result=outcome.result,
        reason_code=outcome.reason_code,
        requires_human_review=outcome.requires_human_review,
    )
    db.add(decision)
    db.flush()
    if decision.result in {"hold", "rejected"}:
        try:
            aggregate_id = UUID(str(entity_id))
        except ValueError:
            aggregate_id = decision.decision_id
        emit_outbox_event(
            db,
            event_type="policy.check_hold" if decision.result == "hold" else "policy.check_rejected",
            aggregate_type=entity_type,
            aggregate_id=aggregate_id,
            recipient_role="supervisor",
            channel="system",
            payload={
                "decision_id": str(decision.decision_id),
                "agent_code": agent_code,
                "requested_action": requested_action,
                "reason_code": decision.reason_code,
                "policy_version": decision.policy_version,
            },
            idempotency_key=outbox_key("policy.check", decision.result, decision.idempotency_key or decision.decision_id),
        )
    return decision
