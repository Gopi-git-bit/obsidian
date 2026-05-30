"""Pydantic schemas for order lifecycle, bid, and match APIs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


CANONICAL_ORDER_STATES = {
    "CREATED",
    "PAYMENT_PENDING",
    "CONFIRMED",
    "RINGING",
    "ASSIGNED",
    "EN_ROUTE_TO_PICKUP",
    "AT_PICKUP_WAITING",
    "LOADING",
    "DEPARTED_FOR_DELIVERY",
    "AT_DELIVERY_WAITING",
    "DELIVERED_PENDING_SETTLEMENT",
    "COMPLETED",
    "CANCELLED",
    "SUSPENDED",
    "INCIDENT",
}

ACTOR_ROLES = {"OMS", "TMS", "FIN", "RAG", "SUP", "CUSTOMER", "DRIVER", "ADMIN"}


class OrderCreate(BaseModel):
    customer_id: Optional[str] = Field(None, max_length=80)
    vehicle_id: Optional[UUID] = None

    shipper_name: str = Field(..., min_length=1, max_length=150)
    shipper_phone: str = Field(..., min_length=10, max_length=15)
    shipper_email: Optional[str] = None

    origin_city: str = Field(..., min_length=1, max_length=100)
    origin_state: str = Field(..., min_length=1, max_length=50)
    origin_pincode: Optional[str] = None
    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None

    destination_city: str = Field(..., min_length=1, max_length=100)
    destination_state: str = Field(..., min_length=1, max_length=50)
    destination_pincode: Optional[str] = None
    destination_lat: Optional[float] = None
    destination_lng: Optional[float] = None

    cargo_type: str = Field(default="general")
    cargo_description: Optional[str] = None
    material_type: str = Field(default="general_goods", max_length=60)
    body_type_required: str = Field(default="open", max_length=30)
    payment_mode: Literal["advance", "full", "topay"] = "advance"
    topay_consent_status: Literal[
        "not_required", "pending", "accepted", "rejected", "timeout"
    ] = "not_required"

    weight_kg: float = Field(..., gt=0)
    volume_cbm: Optional[float] = Field(None, gt=0)
    num_packages: int = Field(default=1, ge=1)

    vehicle_category_preference: Optional[str] = None
    is_interstate: bool = False
    is_festival_period: bool = False
    is_remote_location: bool = False
    is_hill_area: bool = False

    estimated_distance_km: Optional[float] = Field(None, gt=0)
    estimated_duration_hours: Optional[float] = Field(None, gt=0)

    offered_price: Optional[float] = Field(None, gt=0)
    pickup_datetime: Optional[datetime] = None
    delivery_deadline: Optional[datetime] = None
    payload_metadata: dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offered_price: Optional[float] = Field(None, gt=0)
    negotiated_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class OrderSubmittedPayload(BaseModel):
    payment_mode: Literal["advance", "full", "topay"] = "advance"
    topay_consent_status: Literal[
        "not_required", "pending", "accepted", "rejected", "timeout"
    ] = "not_required"
    material_type: str = "general_goods"
    body_type_required: str = "open"


class PaymentCapturedPayload(BaseModel):
    payment_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = "INR"


class VehicleReservedPayload(BaseModel):
    vehicle_id: UUID
    reservation_id: Optional[UUID] = None
    expires_at: datetime


class DriverResponsePayload(BaseModel):
    driver_id: str = Field(..., min_length=1)
    vehicle_id: UUID
    action: Literal["ACCEPT", "REJECT", "TIMEOUT"]
    response_id: Optional[str] = None


class ShipmentDocScannedPayload(BaseModel):
    driver_id: str = Field(..., min_length=1)
    vehicle_id: UUID
    doc_type: str = Field(..., min_length=1)
    doc_url: str = Field(..., min_length=1)
    scan_exif: dict[str, Any]


class PodScannedPayload(BaseModel):
    driver_id: str = Field(..., min_length=1)
    pod_url: str = Field(..., min_length=1)
    consignee_otp: str = Field(..., min_length=4)
    verification_status: Literal["PENDING", "VERIFIED", "ACCEPTED"] = "PENDING"
    pod_exif: dict[str, Any]


class IncidentDetectedPayload(BaseModel):
    incident_type: str = Field(..., min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    description: str = Field(..., min_length=1)


class SupervisorPolicyResultPayload(BaseModel):
    decision: Literal["allow", "hold"]
    decision_reason: str = Field(..., min_length=1)
    policies_hit: list[str] = Field(default_factory=list)


EVENT_PAYLOAD_SCHEMAS = {
    "order_submitted": OrderSubmittedPayload,
    "payment_captured": PaymentCapturedPayload,
    "vehicle_reserved": VehicleReservedPayload,
    "driver_response": DriverResponsePayload,
    "shipment_doc_scanned": ShipmentDocScannedPayload,
    "pod_scanned": PodScannedPayload,
    "incident_detected": IncidentDetectedPayload,
    "supervisor_policy_result": SupervisorPolicyResultPayload,
}


class OrderTransitionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to_state: str = Field(
        ...,
        validation_alias=AliasChoices("to_state", "new_state", "new_status"),
    )
    event: str = Field(..., min_length=1, max_length=80)
    payload: dict[str, Any]
    actor_role: str = Field(..., min_length=1, max_length=40)
    actor_id: Optional[str] = Field(None, max_length=80)
    idempotency_key: UUID
    trace_id: str = Field(..., min_length=1, max_length=120)
    reason: Optional[str] = None
    evidence_ref: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def validate_transition_contract(self):
        self.actor_role = self.actor_role.strip().upper()
        if self.actor_role not in ACTOR_ROLES:
            raise ValueError(f"actor_role must be one of {sorted(ACTOR_ROLES)}")

        self.to_state = self.to_state.strip().upper()
        if self.to_state == "ALLOCATED":
            self.to_state = "ASSIGNED"
        if self.to_state not in CANONICAL_ORDER_STATES:
            raise ValueError(
                f"to_state must be one of {sorted(CANONICAL_ORDER_STATES)}"
            )

        schema = EVENT_PAYLOAD_SCHEMAS.get(self.event)
        if schema is not None:
            self.payload = schema.model_validate(self.payload).model_dump(mode="json")
        return self


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: Optional[str]
    vehicle_id: Optional[UUID]

    shipper_name: str
    shipper_phone: str
    shipper_email: Optional[str]

    origin_city: str
    origin_state: str
    origin_pincode: Optional[str]
    origin_lat: Optional[float]
    origin_lng: Optional[float]

    destination_city: str
    destination_state: str
    destination_pincode: Optional[str]
    destination_lat: Optional[float]
    destination_lng: Optional[float]

    cargo_type: str
    cargo_description: Optional[str]
    material_type: str
    body_type_required: str
    payment_mode: str
    topay_consent_status: str

    weight_kg: float
    volume_cbm: Optional[float]
    num_packages: int

    vehicle_category_preference: Optional[str]
    is_interstate: bool
    is_festival_period: bool
    is_remote_location: bool
    is_hill_area: bool

    estimated_distance_km: Optional[float]
    estimated_duration_hours: Optional[float]

    offered_price: Optional[float]
    negotiated_price: Optional[float]

    pickup_datetime: Optional[datetime]
    delivery_deadline: Optional[datetime]

    current_state: str
    status: str
    payload_metadata: dict[str, Any]

    created_at: datetime
    updated_at: datetime


class StateAuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    log_id: UUID
    order_id: UUID
    from_state: str
    to_state: str
    event_name: str
    actor_role: str
    actor_id: Optional[str]
    idempotency_key: UUID
    trace_id: str
    payload_hash: str
    timestamp: datetime


class OrderStateEventResponse(StateAuditLogResponse):
    @property
    def id(self) -> UUID:
        return self.log_id

    @property
    def from_status(self) -> str:
        return self.from_state

    @property
    def to_status(self) -> str:
        return self.to_state

    @property
    def event(self) -> str:
        return self.event_name

    @property
    def created_at(self) -> datetime:
        return self.timestamp


class OrderStateEventListResponse(BaseModel):
    total: int
    events: list[StateAuditLogResponse]


class OrderListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    orders: list[OrderResponse]


class BidCreate(BaseModel):
    vehicle_id: UUID
    driver_name: str = Field(..., min_length=1, max_length=150)
    driver_phone: str = Field(..., min_length=10, max_length=15)
    bid_amount: float = Field(..., gt=0)
    estimated_eta_hours: Optional[float] = Field(None, gt=0)
    estimated_arrival_hours: Optional[float] = Field(None, gt=0)
    vehicle_available_at: Optional[datetime] = None
    notes: Optional[str] = None


class BidCounter(BaseModel):
    counter_amount: float = Field(..., gt=0)
    notes: Optional[str] = None


class BidResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    vehicle_id: UUID
    driver_name: str
    driver_phone: str
    bid_amount: float
    counter_amount: Optional[float]
    estimated_eta_hours: Optional[float]
    estimated_arrival_hours: Optional[float]
    vehicle_available_at: Optional[datetime]
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class BidListResponse(BaseModel):
    total: int
    bids: list[BidResponse]


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    vehicle_id: UUID
    bid_id: Optional[UUID]
    match_score: Optional[float]
    utilization_percent: Optional[float]
    efficiency_score: Optional[float]
    agreed_price: Optional[float]
    platform_fee: Optional[float]
    gst_amount: Optional[float]
    total_amount: Optional[float]
    status: str
    matched_at: Optional[datetime]
    accepted_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime


class MatchListResponse(BaseModel):
    total: int
    matches: list[MatchResponse]


class MatchAction(BaseModel):
    notes: Optional[str] = None
