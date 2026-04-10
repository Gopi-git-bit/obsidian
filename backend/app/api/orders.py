"""
Order API endpoints — freight transport order lifecycle management
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.models.order_model import Order, OrderStatus, CargoType
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
)

router = APIRouter()


VALID_STATUSES = [s.value for s in OrderStatus]
VALID_CARGO_TYPES = [c.value for c in CargoType]


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new freight transport order"""
    if order_data.cargo_type and order_data.cargo_type not in VALID_CARGO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cargo_type. Must be one of: {VALID_CARGO_TYPES}",
        )

    order = Order(
        status=OrderStatus.CREATED,
        **order_data.model_dump(),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=OrderListResponse)
async def list_orders(
    status: Optional[str] = Query(None, description="Filter by order status"),
    origin_city: Optional[str] = Query(None, description="Filter by origin city"),
    destination_city: Optional[str] = Query(
        None, description="Filter by destination city"
    ),
    cargo_type: Optional[str] = Query(None, description="Filter by cargo type"),
    min_weight: Optional[float] = Query(None, ge=0, description="Min weight in kg"),
    max_weight: Optional[float] = Query(None, ge=0, description="Max weight in kg"),
    limit: int = Query(50, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List orders with optional filters"""
    query = db.query(Order)

    if status:
        if status not in VALID_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {VALID_STATUSES}",
            )
        query = query.filter(Order.status == status)
    if origin_city:
        query = query.filter(Order.origin_city.ilike(f"%{origin_city}%"))
    if destination_city:
        query = query.filter(Order.destination_city.ilike(f"%{destination_city}%"))
    if cargo_type:
        query = query.filter(Order.cargo_type == cargo_type)
    if min_weight is not None:
        query = query.filter(Order.weight_kg >= min_weight)
    if max_weight is not None:
        query = query.filter(Order.weight_kg <= max_weight)

    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset(offset).limit(limit).all()

    return OrderListResponse(
        total=total,
        limit=limit,
        offset=offset,
        orders=[OrderResponse.from_orm(o) for o in orders],
    )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
):
    """Update an order's status or price"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order_data.model_dump(exclude_unset=True)

    if "status" in update_data:
        new_status = update_data["status"]
        if new_status not in VALID_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {VALID_STATUSES}",
            )
        order.status = OrderStatus(new_status)

    if "offered_price" in update_data and update_data["offered_price"] is not None:
        order.offered_price = update_data["offered_price"]
    if (
        "negotiated_price" in update_data
        and update_data["negotiated_price"] is not None
    ):
        order.negotiated_price = update_data["negotiated_price"]
    if "notes" in update_data and update_data["notes"] is not None:
        order.notes = update_data["notes"]

    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: UUID, db: Session = Depends(get_db)):
    """Cancel an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel order in {order.status.value} status",
        )

    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders/stats/summary")
async def get_order_stats(db: Session = Depends(get_db)):
    """Get order summary statistics"""
    from sqlalchemy import func as sql_func

    total_orders = db.query(sql_func.count(Order.id)).scalar() or 0

    status_counts = (
        db.query(Order.status, sql_func.count(Order.id)).group_by(Order.status).all()
    )
    status_map = {str(s.value): c for s, c in status_counts}

    avg_weight = db.query(sql_func.avg(Order.weight_kg)).scalar() or 0
    total_weight = db.query(sql_func.sum(Order.weight_kg)).scalar() or 0

    top_routes = (
        db.query(
            Order.origin_city,
            Order.destination_city,
            sql_func.count(Order.id).label("count"),
        )
        .group_by(Order.origin_city, Order.destination_city)
        .order_by(sql_func.count(Order.id).desc())
        .limit(5)
        .all()
    )

    return {
        "total_orders": total_orders,
        "by_status": status_map,
        "avg_weight_kg": round(float(avg_weight), 2),
        "total_weight_kg": round(float(total_weight), 2),
        "top_routes": [
            {"origin": r[0], "destination": r[1], "count": r[2]} for r in top_routes
        ],
    }
