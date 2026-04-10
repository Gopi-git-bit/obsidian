"""
Pydantic schemas for Order, Bid, and Match API endpoints
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# ─── Order Schemas ───


class OrderCreate(BaseModel):
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
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    offered_price: Optional[float] = Field(None, gt=0)
    negotiated_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: UUID
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

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    orders: list[OrderResponse]


# ─── Bid Schemas ───


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

    class Config:
        from_attributes = True


class BidListResponse(BaseModel):
    total: int
    bids: list[BidResponse]


# ─── Match Schemas ───


class MatchResponse(BaseModel):
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

    class Config:
        from_attributes = True


class MatchListResponse(BaseModel):
    total: int
    matches: list[MatchResponse]


class MatchAction(BaseModel):
    notes: Optional[str] = None
