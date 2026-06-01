"""Shipment tracking projection endpoints for Z.ai frontend status screens."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import CUSTOMER_ORDER_ROLES, DRIVER_TRIP_ROLES, SUPPORT_READ_ROLES, require_roles
from app.database import get_db
from app.models.order_model import Order
from app.schemas.logistics import ShipmentStatusListResponse, ShipmentStatusResponse

router = APIRouter(
    dependencies=[Depends(require_roles(CUSTOMER_ORDER_ROLES | DRIVER_TRIP_ROLES | SUPPORT_READ_ROLES))]
)


def _delay_risk(order: Order) -> str:
    if order.status in {"CANCELLED"}:
        return "high"
    if (
        order.delivery_deadline
        and order.status not in {"COMPLETED", "CANCELLED"}
        and order.delivery_deadline < datetime.now(timezone.utc)
    ):
        return "medium"
    return "none"


def _shipment_projection(order: Order) -> ShipmentStatusResponse:
    latest_milestone = order.status
    if order.state_events:
        latest_milestone = order.state_events[-1].event_name

    return ShipmentStatusResponse(
        order_id=order.id,
        shipment_status=order.status,
        origin_city=order.origin_city,
        destination_city=order.destination_city,
        latest_milestone=latest_milestone,
        delay_risk=_delay_risk(order),
        current_eta=order.delivery_deadline,
        customer_phone=order.shipper_phone,
        updated_at=order.updated_at or order.created_at,
    )


@router.get("/shipments/status", response_model=ShipmentStatusListResponse)
async def get_shipments_status(
    order_id: Optional[UUID] = Query(None, description="Filter status by order id"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Return role-safe shipment status projections for frontend tracking views."""
    query = db.query(Order)
    if order_id:
        query = query.filter(Order.id == order_id)

    total = query.count()
    orders = query.order_by(Order.updated_at.desc()).offset(offset).limit(limit).all()

    return ShipmentStatusListResponse(
        total=total,
        shipments=[_shipment_projection(order) for order in orders],
    )
