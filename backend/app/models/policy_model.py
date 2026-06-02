"""Deterministic policy kernel models."""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, Numeric, String, Text, Uuid
from sqlalchemy.sql import func

from app.database import Base


class PolicyRegistry(Base):
    __tablename__ = "policy_registry"

    policy_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_code = Column(String(80), unique=True, nullable=False)
    policy_version = Column(String(40), nullable=False)
    status = Column(String(30), default="active", nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    effective_at = Column(DateTime(timezone=True), server_default=func.now())


class PolicyDecision(Base):
    __tablename__ = "policy_decisions"

    decision_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_code = Column(String(40), nullable=False, index=True)
    entity_type = Column(String(60), nullable=False)
    entity_id = Column(String(120), nullable=False)
    requested_action = Column(String(120), nullable=False)
    decision_reason = Column(Text)
    trace_id = Column(String(120), index=True)
    idempotency_key = Column(String(180), unique=True)
    confidence_score = Column(Numeric(5, 4))
    evidence_refs = Column(JSON, default=list, nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    policy_version = Column(String(40), nullable=False)
    result = Column(String(30), nullable=False, index=True)
    reason_code = Column(String(80), nullable=False)
    requires_human_review = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RouteZonePolicy(Base):
    __tablename__ = "route_zone_policy"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_zone = Column(String(80), unique=True, nullable=False)
    min_gross_margin_pct = Column(Numeric(6, 2), nullable=False)
    max_allowable_delay_mins = Column(Integer, nullable=False)
    compliance_required = Column(Boolean, default=False, nullable=False)
    vehicle_supply_threshold_pct = Column(Numeric(6, 2), nullable=False)
    crisis_margin_buffer_pct = Column(Numeric(6, 2), default=0, nullable=False)
    policy_version = Column(String(40), nullable=False)


class ComplianceDocumentRule(Base):
    __tablename__ = "compliance_document_rules"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_type = Column(String(60), nullable=False)
    route_type = Column(String(60), nullable=False)
    document_name = Column(String(120), nullable=False)
    mandatory = Column(Boolean, default=True, nullable=False)
    validation_endpoint = Column(String(160))
    policy_version = Column(String(40), nullable=False)


class ConfidenceThreshold(Base):
    __tablename__ = "confidence_thresholds"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_category = Column(String(60), unique=True, nullable=False)
    minimum_confidence = Column(Numeric(5, 4), nullable=False)
    below_threshold_action = Column(String(80), nullable=False)
    policy_version = Column(String(40), nullable=False)
