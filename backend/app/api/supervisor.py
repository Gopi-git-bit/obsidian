"""Supervisor exception and hold endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import SUPPORT_READ_ROLES, SUPERVISOR_ROLES, require_roles
from app.database import get_db
from app.models.auth_model import UserAccount
from app.models.flow_model import SettlementRecord, Trip
from app.models.order_model import Order
from app.models.supervisor_model import ExceptionCase, FraudHold, SettlementHold, SupervisorDecision
from app.services.outbox_service import emit_outbox_event, outbox_key

router = APIRouter()


class SupervisorAction(BaseModel):
    reason: str = Field(default="Supervisor review")
    notes: str | None = None
    payload: dict = Field(default_factory=dict)


def _value(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _row(row, fields):
    return {field: _value(getattr(row, field)) for field in fields}


def _case_or_404(db: Session, case_id: UUID) -> ExceptionCase:
    case = db.query(ExceptionCase).filter(ExceptionCase.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


def _case_detail(db: Session, case: ExceptionCase) -> dict:
    decisions = (
        db.query(SupervisorDecision)
        .filter(SupervisorDecision.case_id == case.case_id)
        .order_by(SupervisorDecision.created_at)
        .all()
    )
    fraud_holds = db.query(FraudHold).filter(FraudHold.case_id == case.case_id).all()
    settlement_holds = db.query(SettlementHold).filter(SettlementHold.case_id == case.case_id).all()
    return {
        "case": _row(case, ("case_id", "order_id", "trip_id", "settlement_id", "case_type", "status", "severity", "title", "description", "payload", "created_by", "created_at", "updated_at")),
        "fraud_holds": [_row(h, ("hold_id", "order_id", "reason", "is_active", "placed_by", "released_by", "placed_at", "released_at")) for h in fraud_holds],
        "settlement_holds": [_row(h, ("hold_id", "settlement_id", "order_id", "trip_id", "reason", "is_active", "placed_by", "released_by", "placed_at", "released_at")) for h in settlement_holds],
        "audit_trail": [_row(d, ("decision_id", "decision", "notes", "decided_by", "payload", "created_at")) for d in decisions],
    }


def _record_decision(db: Session, case: ExceptionCase, user: UserAccount, decision: str, payload: SupervisorAction) -> SupervisorDecision:
    row = SupervisorDecision(
        case_id=case.case_id,
        decision=decision,
        notes=payload.notes or payload.reason,
        decided_by=str(user.id),
        payload=payload.payload,
    )
    db.add(row)
    case.status = decision
    return row


@router.get("/supervisor/cases", dependencies=[Depends(require_roles(SUPPORT_READ_ROLES | SUPERVISOR_ROLES))])
async def list_cases(status: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(ExceptionCase)
    if status:
        query = query.filter(ExceptionCase.status == status)
    cases = query.order_by(ExceptionCase.updated_at.desc()).all()
    return {"total": len(cases), "cases": [_case_detail(db, case) for case in cases]}


@router.get("/supervisor/cases/{case_id}", dependencies=[Depends(require_roles(SUPPORT_READ_ROLES | SUPERVISOR_ROLES))])
async def get_case(case_id: UUID, db: Session = Depends(get_db)):
    return _case_detail(db, _case_or_404(db, case_id))


@router.post("/supervisor/cases/{case_id}/hold", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def hold_case(case_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    case = _case_or_404(db, case_id)
    _record_decision(db, case, user, "held", payload)
    if case.order_id:
        hold = FraudHold(case_id=case.case_id, order_id=case.order_id, reason=payload.reason, placed_by=str(user.id))
        db.add(hold)
        db.flush()
        emit_outbox_event(
            db,
            event_type="fraud.hold_created",
            aggregate_type="order",
            aggregate_id=case.order_id,
            recipient_role="supervisor",
            payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(case.order_id), "reason": payload.reason},
            idempotency_key=outbox_key("fraud.hold_created", hold.hold_id),
        )
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/cases/{case_id}/approve", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def approve_case(case_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    case = _case_or_404(db, case_id)
    _record_decision(db, case, user, "approved", payload)
    now = datetime.now(timezone.utc)
    for hold in db.query(FraudHold).filter(FraudHold.case_id == case.case_id, FraudHold.is_active == True).all():
        hold.is_active = False
        hold.released_by = str(user.id)
        hold.released_at = now
        emit_outbox_event(
            db,
            event_type="fraud.hold_resolved",
            aggregate_type="order",
            aggregate_id=hold.order_id,
            recipient_role="supervisor",
            payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(hold.order_id), "decision": "approved", "reason": payload.reason},
            idempotency_key=outbox_key("fraud.hold_resolved", hold.hold_id, "approved"),
        )
    for hold in db.query(SettlementHold).filter(SettlementHold.case_id == case.case_id, SettlementHold.is_active == True).all():
        hold.is_active = False
        hold.released_by = str(user.id)
        hold.released_at = now
        emit_outbox_event(
            db,
            event_type="settlement.hold_cleared",
            aggregate_type="trip" if hold.trip_id else "settlement",
            aggregate_id=hold.trip_id or hold.settlement_id,
            recipient_role="finance_admin",
            payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(hold.order_id) if hold.order_id else None, "trip_id": str(hold.trip_id) if hold.trip_id else None, "settlement_id": str(hold.settlement_id) if hold.settlement_id else None, "reason": payload.reason},
            idempotency_key=outbox_key("settlement.hold_cleared", hold.hold_id),
        )
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/cases/{case_id}/reject", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def reject_case(case_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    case = _case_or_404(db, case_id)
    _record_decision(db, case, user, "rejected", payload)
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/orders/{order_id}/fraud-hold", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def place_order_fraud_hold(order_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    case = ExceptionCase(order_id=order.id, case_type="fraud_hold", status="held", severity="high", title=f"Fraud hold for order {order.id}", description=payload.reason, payload=payload.payload, created_by=str(user.id))
    db.add(case)
    db.flush()
    hold = FraudHold(case_id=case.case_id, order_id=order.id, reason=payload.reason, placed_by=str(user.id))
    db.add(hold)
    db.flush()
    emit_outbox_event(
        db,
        event_type="fraud.hold_created",
        aggregate_type="order",
        aggregate_id=order.id,
        recipient_role="supervisor",
        payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(order.id), "reason": payload.reason},
        idempotency_key=outbox_key("fraud.hold_created", hold.hold_id),
    )
    _record_decision(db, case, user, "held", payload)
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/settlements/{settlement_id}/hold", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def place_settlement_hold(settlement_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    settlement = db.query(SettlementRecord).filter(SettlementRecord.settlement_id == settlement_id).first()
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
    case = ExceptionCase(order_id=settlement.order_id, trip_id=settlement.trip_id, settlement_id=settlement.settlement_id, case_type="settlement_hold", status="held", severity="medium", title=f"Settlement hold {settlement.settlement_id}", description=payload.reason, payload=payload.payload, created_by=str(user.id))
    db.add(case)
    db.flush()
    hold = SettlementHold(
        case_id=case.case_id,
        settlement_id=settlement.settlement_id,
        order_id=settlement.order_id,
        trip_id=settlement.trip_id,
        reason=payload.reason,
        placed_by=str(user.id),
    )
    db.add(hold)
    db.flush()
    emit_outbox_event(
        db,
        event_type="settlement.hold_created",
        aggregate_type="settlement",
        aggregate_id=settlement.settlement_id,
        recipient_role="finance_admin",
        payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(settlement.order_id), "trip_id": str(settlement.trip_id), "settlement_id": str(settlement.settlement_id), "reason": payload.reason},
        idempotency_key=outbox_key("settlement.hold_created", hold.hold_id),
    )
    _record_decision(db, case, user, "held", payload)
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/trips/{trip_id}/settlement-hold", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def place_trip_settlement_hold(trip_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    case = ExceptionCase(order_id=trip.order_id, trip_id=trip.trip_id, case_type="settlement_hold", status="held", severity="medium", title=f"Settlement hold for trip {trip.trip_id}", description=payload.reason, payload=payload.payload, created_by=str(user.id))
    db.add(case)
    db.flush()
    hold = SettlementHold(case_id=case.case_id, order_id=trip.order_id, trip_id=trip.trip_id, reason=payload.reason, placed_by=str(user.id))
    db.add(hold)
    db.flush()
    emit_outbox_event(
        db,
        event_type="settlement.hold_created",
        aggregate_type="trip",
        aggregate_id=trip.trip_id,
        recipient_role="finance_admin",
        payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(trip.order_id), "trip_id": str(trip.trip_id), "reason": payload.reason},
        idempotency_key=outbox_key("settlement.hold_created", hold.hold_id),
    )
    _record_decision(db, case, user, "held", payload)
    db.commit()
    return _case_detail(db, case)


@router.post("/supervisor/settlements/{settlement_id}/release-hold", dependencies=[Depends(require_roles(SUPERVISOR_ROLES))])
async def release_settlement_hold(settlement_id: UUID, payload: SupervisorAction, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(SUPERVISOR_ROLES))):
    holds = (
        db.query(SettlementHold)
        .filter(
            SettlementHold.is_active == True,
            or_(SettlementHold.settlement_id == settlement_id, SettlementHold.trip_id == settlement_id),
        )
        .all()
    )
    if not holds:
        raise HTTPException(status_code=404, detail="Active settlement hold not found")
    now = datetime.now(timezone.utc)
    case = _case_or_404(db, holds[0].case_id)
    for hold in holds:
        hold.is_active = False
        hold.released_by = str(user.id)
        hold.released_at = now
        emit_outbox_event(
            db,
            event_type="settlement.hold_cleared",
            aggregate_type="trip" if hold.trip_id else "settlement",
            aggregate_id=hold.trip_id or hold.settlement_id,
            recipient_role="finance_admin",
            payload={"case_id": str(case.case_id), "hold_id": str(hold.hold_id), "order_id": str(hold.order_id) if hold.order_id else None, "trip_id": str(hold.trip_id) if hold.trip_id else None, "settlement_id": str(hold.settlement_id) if hold.settlement_id else None, "reason": payload.reason},
            idempotency_key=outbox_key("settlement.hold_cleared", hold.hold_id),
        )
    _record_decision(db, case, user, "approved", payload)
    db.commit()
    return _case_detail(db, case)
