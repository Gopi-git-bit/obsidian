"""Helpers for idempotent event outbox writes."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.outbox_model import EventOutbox


def outbox_key(*parts: object) -> str:
    return ":".join(str(part) for part in parts if part is not None)[:180]


def emit_outbox_event(
    db: Session,
    *,
    event_type: str,
    aggregate_type: str,
    aggregate_id: UUID,
    recipient_role: str,
    payload: dict,
    channel: str = "in_app",
    recipient_id: str | None = None,
    idempotency_key: str | None = None,
    available_at: datetime | None = None,
) -> EventOutbox:
    if idempotency_key:
        existing = db.query(EventOutbox).filter(EventOutbox.idempotency_key == idempotency_key).first()
        if existing:
            return existing
    event = EventOutbox(
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        recipient_role=recipient_role,
        recipient_id=recipient_id,
        channel=channel,
        payload=payload,
        status="pending",
        idempotency_key=idempotency_key,
        available_at=available_at or datetime.now(timezone.utc),
    )
    db.add(event)
    db.flush()
    return event
