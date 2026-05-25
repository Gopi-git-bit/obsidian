"""Schemas for Z.ai logistics intake and shipment tracking endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class OrderIntakeRequest(BaseModel):
    shipper_name: str = Field(..., min_length=1, max_length=150)
    shipper_phone: str = Field(..., min_length=10, max_length=15)
    shipper_email: Optional[str] = None

    origin_city: str = Field(..., min_length=1, max_length=100)
    origin_state: str = Field(..., min_length=1, max_length=50)
    origin_pincode: Optional[str] = None
    origin_lat: Optional[float] = Field(None, ge=-90, le=90)
    origin_lng: Optional[float] = Field(None, ge=-180, le=180)

    destination_city: str = Field(..., min_length=1, max_length=100)
    destination_state: str = Field(..., min_length=1, max_length=50)
    destination_pincode: Optional[str] = None
    destination_lat: Optional[float] = Field(None, ge=-90, le=90)
    destination_lng: Optional[float] = Field(None, ge=-180, le=180)

    cargo_type: str = Field(default="general")
    cargo_description: Optional[str] = None
    weight_kg: float = Field(..., gt=0)
    volume_cbm: Optional[float] = Field(None, gt=0)
    num_packages: int = Field(default=1, ge=1)
    vehicle_category_preference: Optional[str] = None
    is_interstate: bool = False
    estimated_distance_km: Optional[float] = Field(None, gt=0)
    estimated_duration_hours: Optional[float] = Field(None, gt=0)
    offered_price: Optional[float] = Field(None, gt=0)
    pickup_datetime: Optional[datetime] = None
    delivery_deadline: Optional[datetime] = None
    consent_id: str = Field(..., min_length=1, max_length=120)
    privacy_notice_version: str = Field(..., min_length=1, max_length=60)
    idempotency_key: str = Field(..., min_length=1, max_length=120)
    notes: Optional[str] = None

    @field_validator("shipper_phone")
    @classmethod
    def validate_phone_digits(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 10:
            raise ValueError("shipper_phone must contain at least 10 digits")
        return value


class OrderIntakeResponse(BaseModel):
    order_id: UUID
    status: str
    shipper_name: str
    shipper_phone: str
    origin_city: str
    destination_city: str
    consent_id: str
    privacy_notice_version: str
    idempotency_key: str
    created_at: datetime


class ShipmentStatusResponse(BaseModel):
    order_id: UUID
    shipment_status: str
    origin_city: str
    destination_city: str
    latest_milestone: str
    delay_risk: str
    current_eta: Optional[datetime]
    customer_phone: Optional[str]
    updated_at: datetime


class ShipmentStatusListResponse(BaseModel):
    total: int
    shipments: list[ShipmentStatusResponse]
