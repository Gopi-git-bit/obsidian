"""Durable records for the order-to-settlement integration flow."""

from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Index, Numeric, String, Text, Uuid, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class QuoteRecord(Base):
    __tablename__ = "quote_records"

    quote_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    currency = Column(String(3), default="INR", nullable=False)
    base_amount = Column(Numeric(12, 2), nullable=False)
    platform_fee = Column(Numeric(12, 2), nullable=False)
    gst_amount = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(30), default="generated", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    vehicle_id = Column(Uuid(as_uuid=True), ForeignKey("vehicle_models.id"), nullable=False)
    driver_id = Column(String(80), index=True)
    transport_company_id = Column(String(80), index=True)
    status = Column(String(40), default="created", nullable=False)
    otp_verified = Column(String(10), default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    documents = relationship("TripDocument", back_populates="trip", cascade="all, delete-orphan")
    milestones = relationship("TripMilestone", back_populates="trip", cascade="all, delete-orphan")


class PaymentRecord(Base):
    __tablename__ = "payment_records"

    payment_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id = Column(Uuid(as_uuid=True), ForeignKey("trips.trip_id", ondelete="SET NULL"))
    payment_type = Column(String(30), nullable=False)
    status = Column(String(30), default="recorded", nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    provider_ref = Column(String(120))
    idempotency_key = Column(String(120), nullable=False, unique=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class TripDocument(Base):
    __tablename__ = "trip_documents"

    document_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id = Column(Uuid(as_uuid=True), ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False, index=True)
    document_type = Column(String(40), nullable=False)
    document_url = Column(Text, nullable=False)
    verification_status = Column(String(30), default="uploaded", nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True))

    trip = relationship("Trip", back_populates="documents")


class TripMilestone(Base):
    __tablename__ = "trip_milestones"

    milestone_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id = Column(Uuid(as_uuid=True), ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False, index=True)
    milestone_type = Column(String(60), nullable=False)
    status = Column(String(30), default="recorded", nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    idempotency_key = Column(String(120), nullable=False, unique=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip", back_populates="milestones")


class SettlementRecord(Base):
    __tablename__ = "settlement_records"

    settlement_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    trip_id = Column(Uuid(as_uuid=True), ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), default="released", nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    idempotency_key = Column(String(120), nullable=False, unique=True)
    released_at = Column(DateTime(timezone=True), server_default=func.now())


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    journal_entry_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    settlement_id = Column(Uuid(as_uuid=True), ForeignKey("settlement_records.settlement_id", ondelete="CASCADE"), nullable=False)
    debit_ledger = Column(String(120), nullable=False)
    credit_ledger = Column(String(120), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    idempotency_key = Column(String(120), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GSTInvoiceRecord(Base):
    __tablename__ = "gst_invoice_records"

    invoice_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    settlement_id = Column(Uuid(as_uuid=True), ForeignKey("settlement_records.settlement_id", ondelete="CASCADE"), nullable=False)
    invoice_number = Column(String(80), nullable=False, unique=True)
    taxable_amount = Column(Numeric(12, 2), nullable=False)
    gst_amount = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(30), default="created", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


Index("idx_trip_documents_type_status", TripDocument.document_type, TripDocument.verification_status)
