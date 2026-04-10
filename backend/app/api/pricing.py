"""
Pricing API endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()


class PriceEstimateRequest(BaseModel):
    weight_kg: float
    distance_km: float
    vehicle_category: Optional[str] = None
    is_interstate: bool = False
    is_festival_period: bool = False
    is_remote_location: bool = False
    is_hill_area: bool = False
    is_congested_route: bool = False


class PriceEstimateResponse(BaseModel):
    base_cost: float
    distance_rate: float
    surcharges: dict
    platform_fee: float
    gst_amount: float
    total_amount: float
    currency: str = "INR"


@router.post("/pricing/estimate", response_model=PriceEstimateResponse)
async def estimate_price(request: PriceEstimateRequest, db: Session = Depends(get_db)):
    """
    Calculate price estimate for freight transport.

    Formula:
    - Base Cost = Distance × Rate per km
    - Surcharges = Festival (+20-60%) + Remote (+25-50%) + Hill (+35-60%) + Congestion (+10-25%)
    - Platform Fee = 3-5% of base + surcharges
    - GST = 12% on transport, 18% on platform fee
    """
    # Base rate per km (₹15-25 for FTL, varies by vehicle type)
    base_rate_per_km = 18.0  # Default FTL rate

    if request.vehicle_category:
        rate_map = {
            "LCV": 12.0,
            "ICV": 15.0,
            "HCV": 18.0,
            "Tipper": 20.0,
        }
        base_rate_per_km = rate_map.get(request.vehicle_category, 18.0)

    # Calculate base cost
    base_cost = request.distance_km * base_rate_per_km

    # Calculate surcharges
    surcharges = {}
    total_surcharge_percent = 0

    if request.is_festival_period:
        surcharges["festival"] = 30  # Average festival surcharge
        total_surcharge_percent += 30

    if request.is_remote_location:
        surcharges["remote"] = 35  # Average remote surcharge
        total_surcharge_percent += 35

    if request.is_hill_area:
        surcharges["hill"] = 45  # Average hill surcharge
        total_surcharge_percent += 45

    if request.is_congested_route:
        surcharges["congestion"] = 15  # Average congestion surcharge
        total_surcharge_percent += 15

    surcharge_amount = base_cost * (total_surcharge_percent / 100)

    # Platform fee (3-5% based on distance)
    platform_fee_percent = 4.0 if request.distance_km > 200 else 5.0
    platform_fee = (base_cost + surcharge_amount) * (platform_fee_percent / 100)

    # GST calculation
    # Transport: 12%, Services (platform fee): 18%
    transport_gst = base_cost * 0.12
    service_gst = platform_fee * 0.18
    gst_amount = transport_gst + service_gst

    # Total
    total_amount = base_cost + surcharge_amount + platform_fee + gst_amount

    return PriceEstimateResponse(
        base_cost=round(base_cost, 2),
        distance_rate=base_rate_per_km,
        surcharges=surcharges,
        platform_fee=round(platform_fee, 2),
        gst_amount=round(gst_amount, 2),
        total_amount=round(total_amount, 2),
    )


@router.get("/pricing/rates")
async def get_current_rates(db: Session = Depends(get_db)):
    """Get current base rates for pricing"""
    return {
        "rates_per_km": {
            "LCV": 12.0,
            "ICV": 15.0,
            "HCV": 18.0,
            "Tipper": 20.0,
            "Tractor": 16.0,
        },
        "surcharges": {
            "festival": {"min": 20, "max": 60, "typical": 30},
            "remote": {"min": 25, "max": 50, "typical": 35},
            "hill": {"min": 35, "max": 60, "typical": 45},
            "congestion": {"min": 10, "max": 25, "typical": 15},
        },
        "platform_fee_percent": {
            "short_haul": 5.0,  # < 200km
            "long_haul": 4.0,  # > 200km
        },
        "gst_rates": {
            "transport": 12,
            "services": 18,
        },
    }
