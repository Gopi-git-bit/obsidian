"""Durable event outbox for future notification dispatch."""

from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text, Uuid
from sqlalchemy.sql import func

from app.database import Base


class EventOutbox(Base):
    __tablename__ = "event_outbox"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(Uuid(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    event_type = Column(String(80), nullable=False, index=True)
    aggregate_type = Column(String(60), nullable=False)
    aggregate_id = Column(Uuid(as_uuid=True), nullable=False)
    recipient_role = Column(String(60), nullable=False, index=True)
    recipient_id = Column(String(120))
    channel = Column(String(30), default="in_app", nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    status = Column(String(30), default="pending", nullable=False, index=True)
    attempts = Column(Integer, default=0, nullable=False)
    last_error = Column(Text)
    idempotency_key = Column(String(180), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    available_at = Column(DateTime(timezone=True))
    dispatched_at = Column(DateTime(timezone=True))
