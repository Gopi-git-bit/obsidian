"""Order SQLAlchemy models for the canonical state-machine gateway."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class OrderStatus(str, enum.Enum):
    CREATED = "CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    RINGING = "RINGING"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE_TO_PICKUP = "EN_ROUTE_TO_PICKUP"
    AT_PICKUP_WAITING = "AT_PICKUP_WAITING"
    LOADING = "LOADING"
    DEPARTED_FOR_DELIVERY = "DEPARTED_FOR_DELIVERY"
    AT_DELIVERY_WAITING = "AT_DELIVERY_WAITING"
    DELIVERED_PENDING_SETTLEMENT = "DELIVERED_PENDING_SETTLEMENT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    SUSPENDED = "SUSPENDED"
    INCIDENT = "INCIDENT"


TERMINAL_ORDER_STATUSES = {
    OrderStatus.COMPLETED,
    OrderStatus.CANCELLED,
    OrderStatus.SUSPENDED,
}


class ActorRole(str, enum.Enum):
    OMS = "OMS"
    TMS = "TMS"
    FIN = "FIN"
    RAG = "RAG"
    SUP = "SUP"
    CUSTOMER = "CUSTOMER"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"


class PaymentMode(str, enum.Enum):
    ADVANCE = "advance"
    FULL = "full"
    TOPAY = "topay"


class ConsentStatus(str, enum.Enum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


class CargoType(str, enum.Enum):
    GENERAL = "general"
    FRAGILE = "fragile"
    PERISHABLE = "perishable"
    HAZARDOUS = "hazardous"
    OVERSIZED = "oversized"


class Order(Base):
    """Freight transport order.

    `current_state` is the canonical lifecycle field. `status` is retained as a
    read/write compatibility property for older API response code.
    """

    __tablename__ = "orders"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(80), index=True)
    vehicle_id = Column(Uuid(as_uuid=True), ForeignKey("vehicle_models.id"), index=True)

    shipper_name = Column(String(150), nullable=False)
    shipper_phone = Column(String(15), nullable=False)
    shipper_email = Column(String(255))

    origin_city = Column(String(100), nullable=False, index=True)
    origin_state = Column(String(50), nullable=False)
    origin_pincode = Column(String(10))
    origin_lat = Column(Numeric(9, 6))
    origin_lng = Column(Numeric(9, 6))

    destination_city = Column(String(100), nullable=False, index=True)
    destination_state = Column(String(50), nullable=False)
    destination_pincode = Column(String(10))
    destination_lat = Column(Numeric(9, 6))
    destination_lng = Column(Numeric(9, 6))

    cargo_type = Column(Enum(CargoType), default=CargoType.GENERAL, nullable=False)
    cargo_description = Column(Text)
    material_type = Column(String(60), default="general_goods", nullable=False)
    body_type_required = Column(String(30), default="open", nullable=False)

    payment_mode = Column(Enum(PaymentMode), default=PaymentMode.ADVANCE, nullable=False)
    topay_consent_status = Column(
        Enum(ConsentStatus), default=ConsentStatus.NOT_REQUIRED, nullable=False
    )

    weight_kg = Column(Numeric(10, 2), nullable=False)
    volume_cbm = Column(Numeric(10, 2))
    num_packages = Column(Integer, default=1)

    vehicle_category_preference = Column(String(30))
    is_interstate = Column(Boolean, default=False)
    is_festival_period = Column(Boolean, default=False)
    is_remote_location = Column(Boolean, default=False)
    is_hill_area = Column(Boolean, default=False)

    estimated_distance_km = Column(Numeric(10, 2))
    estimated_duration_hours = Column(Numeric(6, 2))

    offered_price = Column(Numeric(12, 2))
    negotiated_price = Column(Numeric(12, 2))

    pickup_datetime = Column(DateTime(timezone=True))
    delivery_deadline = Column(DateTime(timezone=True))

    current_state = Column(
        Enum(OrderStatus),
        default=OrderStatus.CREATED,
        nullable=False,
        index=True,
    )
    payload_metadata = Column(JSON, default=dict, nullable=False)

    notes = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    bids = relationship("Bid", back_populates="order", cascade="all, delete-orphan")
    matches = relationship(
        "Match", back_populates="order", cascade="all, delete-orphan"
    )
    state_audit_logs = relationship(
        "StateAuditLog",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="StateAuditLog.timestamp",
    )
    reservations = relationship(
        "VehicleReservation",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_order_current_state", "current_state"),
        Index("idx_order_origin_dest", "origin_city", "destination_city"),
        Index("idx_order_created", "created_at"),
        CheckConstraint("weight_kg > 0", name="positive_weight"),
    )

    @property
    def status(self) -> str:
        return self.current_state.value if self.current_state else OrderStatus.CREATED.value

    @status.setter
    def status(self, value: str | OrderStatus) -> None:
        if isinstance(value, OrderStatus):
            self.current_state = value
            return
        normalized = value.strip().upper()
        legacy_map = {
            "PENDING_MATCH": OrderStatus.CONFIRMED,
            "BIDDING": OrderStatus.RINGING,
            "MATCHED": OrderStatus.ASSIGNED,
            "BID_ACCEPTED": OrderStatus.ASSIGNED,
            "IN_TRANSIT": OrderStatus.DEPARTED_FOR_DELIVERY,
            "DELIVERED": OrderStatus.COMPLETED,
        }
        self.current_state = legacy_map.get(normalized, OrderStatus(normalized))

    @property
    def state_events(self):
        return self.state_audit_logs

    def __repr__(self):
        return (
            f"<Order {self.id} {self.origin_city}->{self.destination_city} "
            f"[{self.current_state}]>"
        )


class StateAuditLog(Base):
    """Append-only historical log for every state mutation."""

    __tablename__ = "state_audit_logs"

    log_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    from_state = Column(Enum(OrderStatus), nullable=False)
    to_state = Column(Enum(OrderStatus), nullable=False)
    event_name = Column(String(80), nullable=False)
    actor_role = Column(Enum(ActorRole), nullable=False)
    actor_id = Column(String(80))
    idempotency_key = Column(Uuid(as_uuid=True), nullable=False, index=True)
    trace_id = Column(String(120), nullable=False, index=True)
    payload_hash = Column(String(64), nullable=False)
    request_payload = Column(JSON, default=dict, nullable=False)
    cached_response = Column(JSON, default=dict, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    order = relationship("Order", back_populates="state_audit_logs")

    __table_args__ = (
        Index("idx_state_audit_order_timestamp", "order_id", "timestamp"),
        Index("idx_state_audit_idempotency_timestamp", "idempotency_key", "timestamp"),
    )


class VehicleReservation(Base):
    """Vehicle reservation with active unique protection against double booking."""

    __tablename__ = "vehicle_reservations"

    reservation_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(Uuid(as_uuid=True), nullable=False, index=True)
    order_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="reservations")

    __table_args__ = (
        Index(
            "uq_vehicle_reservations_active_vehicle",
            "vehicle_id",
            unique=True,
            postgresql_where=(is_active.is_(True)),
            sqlite_where=(is_active.is_(True)),
        ),
    )


class AgentDLQMessage(Base):
    """Table-backed `agent.dlq` layout for unprocessable transition attempts."""

    __tablename__ = "agent_dlq_messages"

    message_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid(as_uuid=True), index=True)
    event_name = Column(String(80), nullable=False)
    actor_role = Column(String(40), nullable=False)
    idempotency_key = Column(String(120), index=True)
    trace_id = Column(String(120), index=True)
    error_code = Column(String(40), nullable=False)
    error_detail = Column(Text, nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    retry_count = Column(Integer, default=0, nullable=False)
    topic = Column(String(80), default="agent.dlq", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_agent_dlq_created", "created_at"),
        Index("idx_agent_dlq_trace", "trace_id"),
    )


class BidStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COUNTERED = "countered"
    EXPIRED = "expired"


class Bid(Base):
    """Bid placed by a vehicle/driver on an order."""

    __tablename__ = "bids"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vehicle_id = Column(
        Uuid(as_uuid=True), ForeignKey("vehicle_models.id"), nullable=False, index=True
    )

    driver_name = Column(String(150), nullable=False)
    driver_phone = Column(String(15), nullable=False)

    bid_amount = Column(Numeric(12, 2), nullable=False)
    counter_amount = Column(Numeric(12, 2))

    estimated_eta_hours = Column(Numeric(6, 2))
    estimated_arrival_hours = Column(Numeric(6, 2))

    vehicle_available_at = Column(DateTime(timezone=True))
    notes = Column(Text)

    status = Column(
        Enum(BidStatus), default=BidStatus.PENDING, nullable=False, index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    order = relationship("Order", back_populates="bids")

    __table_args__ = (
        Index("idx_bid_order_status", "order_id", "status"),
        CheckConstraint("bid_amount > 0", name="positive_bid"),
    )


class MatchStatus(str, enum.Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Match(Base):
    """Vehicle-load match assignment."""

    __tablename__ = "matches"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vehicle_id = Column(
        Uuid(as_uuid=True), ForeignKey("vehicle_models.id"), nullable=False, index=True
    )
    bid_id = Column(
        Uuid(as_uuid=True), ForeignKey("bids.id"), nullable=True, index=True
    )

    match_score = Column(Numeric(5, 2))
    utilization_percent = Column(Numeric(5, 2))
    efficiency_score = Column(Numeric(5, 2))

    agreed_price = Column(Numeric(12, 2))
    platform_fee = Column(Numeric(10, 2))
    gst_amount = Column(Numeric(10, 2))
    total_amount = Column(Numeric(12, 2))

    status = Column(
        Enum(MatchStatus), default=MatchStatus.PROPOSED, nullable=False, index=True
    )

    matched_at = Column(DateTime(timezone=True), server_default=func.now())
    accepted_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="matches")

    __table_args__ = (
        Index("idx_match_status", "status"),
        Index("idx_match_order_vehicle", "order_id", "vehicle_id"),
    )
