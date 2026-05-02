"""
Bid API endpoints — driver bidding system for orders
"""

from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func

from app.database import get_db
from app.models.order_model import Order, OrderStatus, Bid, BidStatus
from app.models.vehicle_model import VehicleModel
from app.schemas.order import (
    BidCreate,
    BidCounter,
    BidResponse,
    BidListResponse,
)
from app.services.order_service import transition_order

router = APIRouter()


@router.post("/orders/{order_id}/bids", response_model=BidResponse, status_code=201)
async def create_bid(
    order_id: UUID,
    bid_data: BidCreate,
    db: Session = Depends(get_db),
):
    """Place a bid on an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in (
        OrderStatus.CREATED,
        OrderStatus.PENDING_MATCH,
        OrderStatus.BIDDING,
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot bid on order in {order.status.value} status",
        )

    vehicle = (
        db.query(VehicleModel).filter(VehicleModel.id == bid_data.vehicle_id).first()
    )
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    weight_kg = float(order.weight_kg)
    payload_kg = float(vehicle.payload_kg or 1)
    if weight_kg > payload_kg:
        raise HTTPException(
            status_code=400,
            detail=f"Vehicle payload ({payload_kg}kg) insufficient for order weight ({weight_kg}kg)",
        )

    bid = Bid(
        order_id=order.id,
        **bid_data.model_dump(),
        status=BidStatus.PENDING,
    )
    db.add(bid)

    if order.status != OrderStatus.BIDDING:
        transition_order(
            db,
            order_id=order.id,
            new_status=OrderStatus.BIDDING.value,
            event="bid_window_opened",
            actor_role="OMS",
            idempotency_key=f"bid-window-opened:{order.id}",
            reason="First eligible bid received",
        )

    db.commit()
    db.refresh(bid)
    return bid


@router.get("/orders/{order_id}/bids", response_model=BidListResponse)
async def list_bids(
    order_id: UUID,
    status: Optional[str] = Query(None, description="Filter by bid status"),
    db: Session = Depends(get_db),
):
    """List all bids for an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    query = db.query(Bid).filter(Bid.order_id == order_id)

    if status:
        valid = [s.value for s in BidStatus]
        if status not in valid:
            raise HTTPException(
                status_code=400, detail=f"Invalid status. Must be one of: {valid}"
            )
        query = query.filter(Bid.status == status)

    bids = query.order_by(Bid.bid_amount.asc()).all()

    return BidListResponse(
        total=len(bids),
        bids=[BidResponse.model_validate(b) for b in bids],
    )


@router.post("/bids/{bid_id}/accept", response_model=BidResponse)
async def accept_bid(bid_id: UUID, db: Session = Depends(get_db)):
    """Accept a bid"""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if bid.status != BidStatus.PENDING:
        raise HTTPException(
            status_code=400, detail=f"Cannot accept bid in {bid.status.value} status"
        )

    bid.status = BidStatus.ACCEPTED

    order = db.query(Order).filter(Order.id == bid.order_id).first()
    if order:
        if bid.bid_amount:
            order.negotiated_price = bid.bid_amount
        transition_order(
            db,
            order_id=order.id,
            new_status=OrderStatus.BID_ACCEPTED.value,
            event="bid_accepted",
            actor_role="OMS",
            idempotency_key=f"bid-accepted:{bid.id}",
            reason="Customer accepted provider bid",
        )

    competing = (
        db.query(Bid)
        .filter(
            Bid.order_id == bid.order_id,
            Bid.id != bid.id,
            Bid.status == BidStatus.PENDING,
        )
        .all()
    )
    for c in competing:
        c.status = BidStatus.REJECTED

    db.commit()
    db.refresh(bid)
    return bid


@router.post("/bids/{bid_id}/reject", response_model=BidResponse)
async def reject_bid(bid_id: UUID, db: Session = Depends(get_db)):
    """Reject a bid"""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if bid.status not in (BidStatus.PENDING, BidStatus.COUNTERED):
        raise HTTPException(
            status_code=400, detail=f"Cannot reject bid in {bid.status.value} status"
        )

    bid.status = BidStatus.REJECTED
    db.commit()
    db.refresh(bid)
    return bid


@router.post("/bids/{bid_id}/counter", response_model=BidResponse)
async def counter_bid(
    bid_id: UUID,
    counter_data: BidCounter,
    db: Session = Depends(get_db),
):
    """Counter-offer on a bid"""
    bid = db.query(Bid).filter(Bid.id == bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if bid.status != BidStatus.PENDING:
        raise HTTPException(
            status_code=400, detail=f"Cannot counter bid in {bid.status.value} status"
        )

    bid.counter_amount = counter_data.counter_amount
    bid.status = BidStatus.COUNTERED

    db.commit()
    db.refresh(bid)
    return bid
