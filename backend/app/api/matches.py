"""
Match API endpoints — vehicle-load matching engine
"""

from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func

from app.database import get_db
from app.models.order_model import Order, OrderStatus, Match, MatchStatus
from app.models.vehicle_model import VehicleModel
from app.models.order_model import Bid
from app.schemas.order import MatchResponse, MatchListResponse, MatchAction
from app.services.order_service import transition_order

router = APIRouter()


def calculate_match_score(order, vehicle) -> dict:
    weight_kg = float(order.weight_kg)
    payload_kg = float(vehicle.payload_kg or 1)
    gvw_kg = float(vehicle.gvw_kg or payload_kg * 1.5)

    utilization = min(weight_kg / payload_kg * 100, 100) if payload_kg > 0 else 0

    mileage = float(vehicle.mileage_kmpl or 8)
    mileage_score = min(mileage / 12.0 * 100, 100)

    if vehicle.price_ex_showroom:
        price_per_ton = float(vehicle.price_ex_showroom) / (payload_kg / 1000)
        price_score = max(100 - (price_per_ton - 50000) / 5000, 20)
    else:
        price_score = 50.0

    interstate_bonus = 10 if getattr(order, "is_interstate", False) else 0

    score = (
        utilization * 0.45
        + mileage_score * 0.25
        + price_score * 0.20
        + interstate_bonus * 0.10
    )

    return {
        "match_score": round(min(score, 100), 2),
        "utilization_percent": round(utilization, 2),
        "efficiency_score": round(mileage_score, 2),
    }


@router.get("/orders/{order_id}/match")
async def find_matches(
    order_id: UUID,
    limit: int = Query(5, ge=1, le=20, description="Max matches to return"),
    min_score: float = Query(30.0, ge=0, le=100, description="Minimum match score"),
    db: Session = Depends(get_db),
):
    """Find best vehicles for an order using weighted scoring algorithm"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    preferred_category = getattr(order, "vehicle_category_preference", None)

    query = db.query(VehicleModel)

    weight_kg = float(order.weight_kg)
    if preferred_category:
        query = query.filter(VehicleModel.category == preferred_category)

    vehicles = query.all()

    if not vehicles:
        raise HTTPException(
            status_code=404,
            detail="No vehicles available for matching",
        )

    matches = []
    for vehicle in vehicles:
        if vehicle.payload_kg and weight_kg > float(vehicle.payload_kg):
            continue

        scores = calculate_match_score(order, vehicle)

        if scores["match_score"] < min_score:
            continue

        match = Match(
            order_id=order.id,
            vehicle_id=vehicle.id,
            match_score=scores["match_score"],
            utilization_percent=scores["utilization_percent"],
            efficiency_score=scores["efficiency_score"],
            status=MatchStatus.PROPOSED,
        )
        db.add(match)
        matches.append((match, vehicle, scores))

    db.commit()

    for match, vehicle, scores in matches:
        db.refresh(match)

    if not matches:
        raise HTTPException(
            status_code=404,
            detail=f"No matching vehicles found with score >= {min_score}",
        )

    matches.sort(key=lambda x: x[2]["match_score"], reverse=True)
    matches = matches[:limit]

    if order.status == OrderStatus.CREATED:
        transition_order(
            db,
            order_id=order.id,
            new_status=OrderStatus.PENDING_MATCH.value,
            event="match_candidates_generated",
            actor_role="OMS",
            idempotency_key=f"match-candidates-generated:{order.id}",
            reason="Matching engine generated vehicle candidates",
        )
    else:
        db.commit()

    return {
        "order_id": str(order_id),
        "total_matches": len(matches),
        "matches": [
            {
                "match_id": str(m.id),
                "vehicle_id": str(v.id),
                "vehicle_name": f"{v.manufacturer} {v.model_name}",
                "vehicle_category": v.category,
                "payload_kg": float(v.payload_kg or 0),
                "match_score": s["match_score"],
                "utilization_percent": s["utilization_percent"],
                "efficiency_score": s["efficiency_score"],
                "status": m.status.value,
            }
            for m, v, s in matches
        ],
    }


@router.post("/matches/{match_id}/accept", response_model=MatchResponse)
async def accept_match(
    match_id: UUID,
    action: MatchAction = MatchAction(),
    db: Session = Depends(get_db),
):
    """Accept a proposed match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != MatchStatus.PROPOSED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot accept match in {match.status.value} status",
        )

    match.status = MatchStatus.ACCEPTED
    match.accepted_at = datetime.utcnow()

    order = db.query(Order).filter(Order.id == match.order_id).first()
    vehicle = db.query(VehicleModel).filter(VehicleModel.id == match.vehicle_id).first()

    if order and vehicle:
        from app.api.pricing import PriceEstimateRequest

        distance = float(order.estimated_distance_km or 500)
        base_rate = float(vehicle.mileage_kmpl or 8) * 2.0
        if base_rate < 12:
            base_rate = 18.0

        base_cost = distance * base_rate
        surcharges = {}
        total_pct = 0
        if order.is_festival_period:
            surcharges["festival"] = 30
            total_pct += 30
        if order.is_remote_location:
            surcharges["remote"] = 35
            total_pct += 35
        if order.is_hill_area:
            surcharges["hill"] = 45
            total_pct += 45

        surcharge_amount = base_cost * (total_pct / 100)
        platform_fee = (base_cost + surcharge_amount) * 0.04
        gst = base_cost * 0.12 + platform_fee * 0.18

        match.agreed_price = round(base_cost + surcharge_amount, 2)
        match.platform_fee = round(platform_fee, 2)
        match.gst_amount = round(gst, 2)
        match.total_amount = round(base_cost + surcharge_amount + platform_fee + gst, 2)

    if order:
        transition_order(
            db,
            order_id=order.id,
            new_status=OrderStatus.MATCHED.value,
            event="match_accepted",
            actor_role="IMS",
            idempotency_key=f"match-accepted:{match.id}",
            reason=action.notes,
        )

    db.commit()
    db.refresh(match)
    return match


@router.post("/matches/{match_id}/reject", response_model=MatchResponse)
async def reject_match(
    match_id: UUID,
    action: MatchAction = MatchAction(),
    db: Session = Depends(get_db),
):
    """Reject a proposed match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != MatchStatus.PROPOSED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reject match in {match.status.value} status",
        )

    match.status = MatchStatus.REJECTED
    db.commit()
    db.refresh(match)
    return match


@router.get("/matches", response_model=MatchListResponse)
async def list_matches(
    status: Optional[str] = Query(None, description="Filter by match status"),
    order_id: Optional[UUID] = Query(None, description="Filter by order ID"),
    limit: int = Query(50, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List all matches with optional filters"""
    query = db.query(Match)

    if status:
        valid = [s.value for s in MatchStatus]
        if status not in valid:
            raise HTTPException(
                status_code=400, detail=f"Invalid status. Must be one of: {valid}"
            )
        query = query.filter(Match.status == status)
    if order_id:
        query = query.filter(Match.order_id == order_id)

    total = query.count()
    matches = query.order_by(Match.matched_at.desc()).offset(offset).limit(limit).all()

    return MatchListResponse(
        total=total,
        matches=[MatchResponse.model_validate(m) for m in matches],
    )


@router.get("/matches/stats")
async def get_match_stats(db: Session = Depends(get_db)):
    """Get match statistics"""
    total_matches = db.query(sql_func.count(Match.id)).scalar() or 0

    status_counts = (
        db.query(Match.status, sql_func.count(Match.id)).group_by(Match.status).all()
    )
    status_map = {str(s.value): c for s, c in status_counts}

    avg_score = db.query(sql_func.avg(Match.match_score)).scalar() or 0

    avg_util = db.query(sql_func.avg(Match.utilization_percent)).scalar() or 0

    return {
        "total_matches": total_matches,
        "by_status": status_map,
        "avg_match_score": round(float(avg_score), 2),
        "avg_utilization_percent": round(float(avg_util), 2),
    }
