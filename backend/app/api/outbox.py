"""Minimal event outbox visibility and status controls."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import require_roles
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole
from app.models.outbox_model import EventOutbox

router = APIRouter()

OUTBOX_READ_ROLES = {UserRole.SUPER_ADMIN.value, UserRole.SUPERVISOR.value, UserRole.FINANCE_ADMIN.value}
OUTBOX_MARK_ROLES = {UserRole.SUPER_ADMIN.value}
SUPERVISOR_EVENT_TYPES = {
    "settlement.release_blocked",
    "settlement.hold_created",
    "settlement.hold_cleared",
    "fraud.hold_created",
    "fraud.hold_resolved",
}
FINANCE_EVENT_PREFIXES = ("settlement.", "finance.")


class MarkFailedRequest(BaseModel):
    error: str = Field(..., min_length=1)


def _value(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _row(event: EventOutbox) -> dict:
    return {
        "id": str(event.id),
        "event_id": str(event.event_id),
        "event_type": event.event_type,
        "aggregate_type": event.aggregate_type,
        "aggregate_id": str(event.aggregate_id),
        "recipient_role": event.recipient_role,
        "recipient_id": event.recipient_id,
        "channel": event.channel,
        "payload": event.payload,
        "status": event.status,
        "attempts": event.attempts,
        "last_error": event.last_error,
        "idempotency_key": event.idempotency_key,
        "created_at": _value(event.created_at),
        "available_at": _value(event.available_at),
        "dispatched_at": _value(event.dispatched_at),
    }


def _can_read(event: EventOutbox, user: UserAccount) -> bool:
    if user.role == UserRole.SUPER_ADMIN:
        return True
    if user.role == UserRole.FINANCE_ADMIN:
        return event.event_type.startswith(FINANCE_EVENT_PREFIXES)
    if user.role == UserRole.SUPERVISOR:
        return event.event_type in SUPERVISOR_EVENT_TYPES
    return False


def _readable_query(db: Session, user: UserAccount):
    query = db.query(EventOutbox)
    if user.role == UserRole.SUPER_ADMIN:
        return query
    if user.role == UserRole.FINANCE_ADMIN:
        return query.filter(EventOutbox.event_type.like("settlement.%") | EventOutbox.event_type.like("finance.%"))
    if user.role == UserRole.SUPERVISOR:
        return query.filter(EventOutbox.event_type.in_(SUPERVISOR_EVENT_TYPES))
    raise HTTPException(status_code=403, detail="Insufficient role")


def _event_or_404(db: Session, event_id: UUID, user: UserAccount) -> EventOutbox:
    event = db.query(EventOutbox).filter(EventOutbox.event_id == event_id).first()
    if not event or not _can_read(event, user):
        raise HTTPException(status_code=404, detail="Outbox event not found")
    return event


@router.get("/outbox/events", dependencies=[Depends(require_roles(OUTBOX_READ_ROLES))])
async def list_outbox_events(
    status: str | None = Query(None),
    event_type: str | None = Query(None),
    aggregate_id: UUID | None = Query(None),
    db: Session = Depends(get_db),
    user: UserAccount = Depends(require_roles(OUTBOX_READ_ROLES)),
):
    query = _readable_query(db, user)
    if status:
        query = query.filter(EventOutbox.status == status)
    if event_type:
        query = query.filter(EventOutbox.event_type == event_type)
    if aggregate_id:
        query = query.filter(EventOutbox.aggregate_id == aggregate_id)
    events = query.order_by(EventOutbox.created_at.desc()).all()
    return {"total": len(events), "events": [_row(event) for event in events]}


@router.get("/outbox/events/{event_id}", dependencies=[Depends(require_roles(OUTBOX_READ_ROLES))])
async def get_outbox_event(event_id: UUID, db: Session = Depends(get_db), user: UserAccount = Depends(require_roles(OUTBOX_READ_ROLES))):
    return _row(_event_or_404(db, event_id, user))


@router.post("/outbox/events/{event_id}/mark-dispatched", dependencies=[Depends(require_roles(OUTBOX_MARK_ROLES))])
async def mark_outbox_dispatched(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(EventOutbox).filter(EventOutbox.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Outbox event not found")
    event.status = "dispatched"
    event.dispatched_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(event)
    return _row(event)


@router.post("/outbox/events/{event_id}/mark-failed", dependencies=[Depends(require_roles(OUTBOX_MARK_ROLES))])
async def mark_outbox_failed(event_id: UUID, payload: MarkFailedRequest, db: Session = Depends(get_db)):
    event = db.query(EventOutbox).filter(EventOutbox.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Outbox event not found")
    event.status = "failed"
    event.attempts += 1
    event.last_error = payload.error
    db.commit()
    db.refresh(event)
    return _row(event)
