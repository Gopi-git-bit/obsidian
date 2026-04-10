"""
ML-Enhanced Pricing API endpoints

Extends the base pricing engine with LightGBM surge prediction and
detailed cost breakdowns per BI_Pricing_Mechanism_Cost_Structure.md
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.pricing_service import pricing_engine, DynamicPricingEngine

router = APIRouter()


class MLPricingRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Cargo weight in kg")
    distance_km: float = Field(..., gt=0, description="Distance in km")
    vehicle_category: str = Field(
        default="HCV", description="LCV, ICV, HCV, Tipper, Tractor, Trailer"
    )
    origin_city: str = Field(default="", description="Origin city for tier detection")
    destination_city: str = Field(default="", description="Destination city for RDS")
    is_interstate: bool = Field(default=False)
    is_festival: bool = Field(default=False)
    is_remote: bool = Field(default=False)
    is_hill: bool = Field(default=False)
    is_congested: bool = Field(default=False)
    service_type: str = Field(
        default="standard", description="standard, express, priority"
    )
    customer_type: str = Field(
        default="medium", description="high_value, medium, low_value"
    )
    demand: int = Field(default=10, description="Current demand (number of orders)")
    supply: int = Field(default=5, description="Available vehicles in area")
    diesel_price: float = Field(
        default=89.62, description="Current diesel price INR/litre"
    )


class MLPricingResponse(BaseModel):
    base_cost: float
    base_rate_per_km: float
    city_tier: int
    tier_multiplier: float
    fuel_index: float
    tier_adjusted_cost: float
    surcharges: dict
    total_surcharge_pct: float
    surcharge_amount: float
    surge_multiplier: float
    surge_model: str
    surge_confidence: float
    surge_amount: float
    service_type: str
    service_multiplier: float
    service_amount: float
    subtotal: float
    customer_type: str
    customer_adjustment: float
    platform_fee_pct: float
    platform_fee: float
    gst_breakdown: dict
    gst_amount: float
    savings_vs_broker_pct: float
    final_price: float
    currency: str = "INR"
    breakdown_per_km: float


class SurgePredictRequest(BaseModel):
    demand: int = Field(default=10)
    supply: int = Field(default=5)
    city: str = Field(default="")
    is_remote: bool = Field(default=False)
    is_hill: bool = Field(default=False)
    is_festival: bool = Field(default=False)
    distance_km: float = Field(default=500)
    origin_city: str = Field(default="")
    destination_city: str = Field(default="")
    congestion_level: float = Field(default=0.3, ge=0, le=1)
    vehicle_category: str = Field(default="HCV")
    vehicle_age: int = Field(default=3)
    diesel_price: float = Field(default=89.62)
    customer_type: str = Field(default="medium")


@router.post("/pricing/ml-estimate", response_model=MLPricingResponse)
async def ml_price_estimate(request: MLPricingRequest, db: Session = Depends(get_db)):
    """
    ML-enhanced dynamic pricing estimate.

    Uses LightGBM surge prediction (when model is trained) or rule-based fallback.
    Produces detailed cost breakdown with Indian logistics specifics:
    - City tier pricing (Metro discount, Rural surcharge)
    - Festival/remote/hill/congestion surcharges
    - Demand-supply dynamic surge
    - Service type multiplier (standard/express/priority)
    - Customer tier adjustments
    - Platform fee (3-5%) vs broker (8-12%)
    - GST (12% transport + 18% services)
    """
    params = request.model_dump()
    result = pricing_engine.calculate_price(params)
    return result


@router.post("/pricing/surge-predict")
async def predict_surge(request: SurgePredictRequest):
    """
    Predict demand-supply surge multiplier.

    Returns surge multiplier (1.0-3.0) with confidence score.
    Uses LightGBM model when trained, rule-based fallback otherwise.
    """
    input_data = request.model_dump()
    result = pricing_engine.surge_predictor.predict(input_data)
    return result


@router.get("/pricing/rate-card")
async def get_detailed_rate_card():
    """
    Get current dynamic rate card with all multipliers and surcharges.

    Includes base rates, city tier multipliers, surcharge ranges,
    service multipliers, platform fee structure, and GST rates.
    """
    return pricing_engine.get_rate_card()


@router.post("/pricing/compare")
async def compare_pricing(request: MLPricingRequest):
    """
    Compare Zippy pricing vs traditional broker pricing.

    Shows side-by-side cost breakdown demonstrating 18-25% savings.
    """
    params = request.model_dump()
    zippy_result = pricing_engine.calculate_price(params)

    broker_price = zippy_result["subtotal"] * 1.10
    broker_gst = broker_price * 0.18
    broker_total = broker_price + broker_gst

    zippy_total = zippy_result["final_price"]
    savings_amount = broker_total - zippy_total
    savings_pct = (savings_amount / broker_total) * 100 if broker_total > 0 else 0

    return {
        "zippy": {
            "subtotal": zippy_result["subtotal"],
            "platform_fee": zippy_result["platform_fee"],
            "platform_fee_pct": zippy_result["platform_fee_pct"],
            "gst": zippy_result["gst_amount"],
            "total": zippy_total,
        },
        "broker": {
            "subtotal": broker_price,
            "commission_pct": 10.0,
            "commission_amount": round(broker_price * 0.10, 2),
            "gst": round(broker_gst, 2),
            "total": round(broker_total, 2),
        },
        "savings": {
            "amount": round(savings_amount, 2),
            "percentage": round(savings_pct, 1),
            "per_km": round(savings_amount / max(params["distance_km"], 1), 2),
        },
        "breakdown": {
            "platform_fee_savings_pct": round(
                10.0 - zippy_result["platform_fee_pct"], 1
            ),
            "gst_savings": round((broker_gst - zippy_result["gst_amount"]), 2),
        },
    }
