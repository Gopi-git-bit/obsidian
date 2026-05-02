"""
Order SQLAlchemy Model — freight transport order lifecycle
"""

import enum
import uuid
from sqlalchemy import (
    Column,
    String,
    Numeric,
    Boolean,
    Integer,
    DateTime,
    Text,
    Enum,
    ForeignKey,
    Index,
    CheckConstraint,
    Uuid,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    PENDING_MATCH = "pending_match"
    MATCHED = "matched"
    BIDDING = "bidding"
    BID_ACCEPTED = "bid_accepted"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


TERMINAL_ORDER_STATUSES = {
    OrderStatus.DELIVERED,
    OrderStatus.CANCELLED,
}


class CargoType(str, enum.Enum):
    GENERAL = "general"
    FRAGILE = "fragile"
    PERISHABLE = "perishable"
    HAZARDOUS = "hazardous"
    OVERSIZED = "oversized"


class Order(Base):
    """Freight transport order"""

    __tablename__ = "orders"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

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

    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.CREATED,
        nullable=False,
        index=True,
    )

    notes = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    bids = relationship("Bid", back_populates="order", cascade="all, delete-orphan")
    matches = relationship(
        "Match", back_populates="order", cascade="all, delete-orphan"
    )
    state_events = relationship(
        "OrderStateEvent",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderStateEvent.created_at",
    )

    __table_args__ = (
        Index("idx_order_status", "status"),
        Index("idx_order_origin_dest", "origin_city", "destination_city"),
        Index("idx_order_created", "created_at"),
        CheckConstraint("weight_kg > 0", name="positive_weight"),
    )

    def __repr__(self):
        return f"<Order {self.id} {self.origin_city}->{self.destination_city} [{self.status}]>"


class OrderStateEvent(Base):
    """Audit event for order lifecycle transitions."""

    __tablename__ = "order_state_events"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    from_status = Column(Enum(OrderStatus), nullable=False)
    to_status = Column(Enum(OrderStatus), nullable=False)
    event = Column(String(80), nullable=False)
    actor_role = Column(String(40), nullable=False)
    actor_id = Column(String(80))
    idempotency_key = Column(String(120), nullable=False, unique=True, index=True)
    reason = Column(Text)
    evidence_ref = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="state_events")

    __table_args__ = (
        Index("idx_order_state_event_order_created", "order_id", "created_at"),
        Index("idx_order_state_event_to_status", "to_status"),
    )

    def __repr__(self):
        return f"<OrderStateEvent {self.order_id} {self.from_status}->{self.to_status}>"


class BidStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COUNTERED = "countered"
    EXPIRED = "expired"


class Bid(Base):
    """Bid placed by a vehicle/driver on an order"""

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

    def __repr__(self):
        return f"<Bid {self.id} ₹{self.bid_amount} [{self.status}]>"


class MatchStatus(str, enum.Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Match(Base):
    """Vehicle-load match assignment"""

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

    def __repr__(self):
        return f"<Match {self.id} score={self.match_score} [{self.status}]>"
