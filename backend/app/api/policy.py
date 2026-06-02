"""Deterministic policy check endpoint."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import require_roles
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole
from app.models.policy_model import PolicyDecision
from app.services.policy_service import record_policy_decision, validate_action_policy

router = APIRouter()

POLICY_CHECK_ROLES = {
    UserRole.SUPERVISOR.value,
    UserRole.SUPER_ADMIN.value,
    UserRole.FINANCE_ADMIN.value,
    UserRole.OPS_ADMIN.value,
}


class PolicyCheckRequest(BaseModel):
    agent_code: str = Field(..., min_length=2, max_length=40)
    entity_type: str = Field(..., min_length=1, max_length=60)
    entity_id: str = Field(..., min_length=1, max_length=120)
    requested_action: str = Field(..., min_length=1, max_length=120)
    decision_reason: str | None = None
    trace_id: str | None = Field(None, max_length=120)
    idempotency_key: str | None = Field(None, max_length=180)
    confidence_score: float | None = Field(None, ge=0, le=1)
    evidence_refs: list[str] = Field(default_factory=list)
    payload: dict = Field(default_factory=dict)


def _value(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    return value


def _can_run_check(user: UserAccount, payload: PolicyCheckRequest) -> bool:
    if user.role in {UserRole.SUPERVISOR, UserRole.SUPER_ADMIN}:
        return True
    probe = f"{payload.entity_type}.{payload.requested_action}".lower()
    if user.role == UserRole.FINANCE_ADMIN:
        return any(term in probe for term in ("finance", "settlement", "payment", "invoice", "journal", "gst", "margin"))
    if user.role == UserRole.OPS_ADMIN:
        return any(term in probe for term in ("order", "shipment", "route", "vehicle", "document", "workflow"))
    return False


@router.post("/policy/check", dependencies=[Depends(require_roles(POLICY_CHECK_ROLES))])
async def check_policy(
    payload: PolicyCheckRequest,
    db: Session = Depends(get_db),
    user: UserAccount = Depends(require_roles(POLICY_CHECK_ROLES)),
):
    if not _can_run_check(user, payload):
        raise HTTPException(status_code=403, detail="Insufficient role for policy domain")

    existing = db.query(PolicyDecision).filter(PolicyDecision.idempotency_key == payload.idempotency_key).first() if payload.idempotency_key else None
    if existing:
        return {
            "approved": existing.result == "approved",
            "result": existing.result,
            "reason_code": existing.reason_code,
            "policy_version": existing.policy_version,
            "requires_human_review": existing.requires_human_review,
            "decision_id": str(existing.decision_id),
        }

    outcome = validate_action_policy(
        db,
        agent_code=payload.agent_code,
        entity_type=payload.entity_type,
        requested_action=payload.requested_action,
        confidence_score=payload.confidence_score,
        payload=payload.payload,
        trace_id=payload.trace_id,
        idempotency_key=payload.idempotency_key,
    )
    decision = record_policy_decision(
        db,
        agent_code=payload.agent_code,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        requested_action=payload.requested_action,
        decision_reason=payload.decision_reason,
        trace_id=payload.trace_id,
        idempotency_key=payload.idempotency_key,
        confidence_score=payload.confidence_score,
        evidence_refs=payload.evidence_refs,
        payload=payload.payload,
        outcome=outcome,
    )
    db.commit()
    return {
        "approved": decision.result == "approved",
        "result": decision.result,
        "reason_code": decision.reason_code,
        "policy_version": decision.policy_version,
        "requires_human_review": decision.requires_human_review,
        "decision_id": str(decision.decision_id),
    }
