"""Supervisor exception and hold records."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, JSON, String, Text, Uuid
from sqlalchemy.sql import func

from app.database import Base


class ExceptionCase(Base):
    __tablename__ = "exception_cases"

    case_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=True, index=True)
    trip_id = Column(Uuid(as_uuid=True), ForeignKey("trips.trip_id", ondelete="SET NULL"), nullable=True, index=True)
    settlement_id = Column(Uuid(as_uuid=True), ForeignKey("settlement_records.settlement_id", ondelete="SET NULL"), nullable=True, index=True)
    case_type = Column(String(60), nullable=False, index=True)
    status = Column(String(30), default="open", nullable=False, index=True)
    severity = Column(String(20), default="medium", nullable=False)
    title = Column(String(160), nullable=False)
    description = Column(Text)
    payload = Column(JSON, default=dict, nullable=False)
    created_by = Column(String(80))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FraudHold(Base):
    __tablename__ = "fraud_holds"

    hold_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(Uuid(as_uuid=True), ForeignKey("exception_cases.case_id", ondelete="CASCADE"), nullable=True, index=True)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    placed_by = Column(String(80), nullable=False)
    released_by = Column(String(80))
    placed_at = Column(DateTime(timezone=True), server_default=func.now())
    released_at = Column(DateTime(timezone=True))


class SettlementHold(Base):
    __tablename__ = "settlement_holds"

    hold_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(Uuid(as_uuid=True), ForeignKey("exception_cases.case_id", ondelete="CASCADE"), nullable=True, index=True)
    settlement_id = Column(Uuid(as_uuid=True), ForeignKey("settlement_records.settlement_id", ondelete="CASCADE"), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    placed_by = Column(String(80), nullable=False)
    released_by = Column(String(80))
    placed_at = Column(DateTime(timezone=True), server_default=func.now())
    released_at = Column(DateTime(timezone=True))


class SupervisorDecision(Base):
    __tablename__ = "supervisor_decisions"

    decision_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(Uuid(as_uuid=True), ForeignKey("exception_cases.case_id", ondelete="CASCADE"), nullable=False, index=True)
    decision = Column(String(30), nullable=False, index=True)
    notes = Column(Text)
    decided_by = Column(String(80), nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
