"""
Order API endpoints — freight transport order lifecycle management
"""

from typing import Optional
from uuid import NAMESPACE_URL, UUID, uuid5

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import (
    CUSTOMER_ORDER_ROLES,
    OPS_ADMIN_ROLES,
    SUPPORT_READ_ROLES,
    require_roles,
)
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole
from app.models.order_model import Order, OrderStatus, CargoType
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    OrderTransitionRequest,
    OrderStateEventListResponse,
    StateAuditLogResponse,
)
from app.schemas.logistics import OrderIntakeRequest, OrderIntakeResponse
from app.services.order_service import get_order_or_404, transition_order

router = APIRouter()
transition_alias_router = APIRouter()


VALID_STATUSES = [s.value for s in OrderStatus]
VALID_CARGO_TYPES = [c.value for c in CargoType]


ORDER_READ_ROLES = CUSTOMER_ORDER_ROLES | SUPPORT_READ_ROLES


def _is_customer(user: UserAccount) -> bool:
    return user.role == UserRole.CUSTOMER


def _assert_customer_owns_order(order: Order, user: UserAccount) -> None:
    if _is_customer(user) and order.customer_id != str(user.id):
        raise HTTPException(status_code=404, detail="Order not found")


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(CUSTOMER_ORDER_ROLES)),
):
    """Create a new freight transport order"""
    if order_data.cargo_type and order_data.cargo_type not in VALID_CARGO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cargo_type. Must be one of: {VALID_CARGO_TYPES}",
        )

    payload = order_data.model_dump()
    if _is_customer(current_user):
        payload["customer_id"] = str(current_user.id)

    order = Order(
        current_state=OrderStatus.CREATED,
        **payload,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post(
    "/orders/intake",
    response_model=OrderIntakeResponse,
    status_code=201,
)
async def intake_order(
    order_data: OrderIntakeRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(CUSTOMER_ORDER_ROLES)),
):
    """Create a DPDP-consented order from the Z.ai frontend intake flow."""
    if order_data.cargo_type and order_data.cargo_type not in VALID_CARGO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cargo_type. Must be one of: {VALID_CARGO_TYPES}",
        )

    query = db.query(Order).filter(
        Order.notes.ilike(f"%intake_idempotency_key={order_data.idempotency_key}%")
    )
    if _is_customer(current_user):
        query = query.filter(Order.customer_id == str(current_user.id))

    existing = (
        query
        .first()
    )
    if existing:
        return OrderIntakeResponse(
            order_id=existing.id,
            status=existing.status,
            shipper_name=existing.shipper_name,
            shipper_phone=existing.shipper_phone,
            origin_city=existing.origin_city,
            destination_city=existing.destination_city,
            consent_id=order_data.consent_id,
            privacy_notice_version=order_data.privacy_notice_version,
            idempotency_key=order_data.idempotency_key,
            created_at=existing.created_at,
        )

    notes_parts = [
        order_data.notes or "",
        f"consent_id={order_data.consent_id}",
        f"privacy_notice_version={order_data.privacy_notice_version}",
        f"intake_idempotency_key={order_data.idempotency_key}",
    ]
    order_payload = order_data.model_dump(
        exclude={"consent_id", "privacy_notice_version", "idempotency_key"}
    )
    if _is_customer(current_user):
        order_payload["customer_id"] = str(current_user.id)
    order_payload["notes"] = " | ".join(part for part in notes_parts if part)

    order = Order(current_state=OrderStatus.CREATED, **order_payload)
    db.add(order)
    db.commit()
    db.refresh(order)

    return OrderIntakeResponse(
        order_id=order.id,
        status=order.status,
        shipper_name=order.shipper_name,
        shipper_phone=order.shipper_phone,
        origin_city=order.origin_city,
        destination_city=order.destination_city,
        consent_id=order_data.consent_id,
        privacy_notice_version=order_data.privacy_notice_version,
        idempotency_key=order_data.idempotency_key,
        created_at=order.created_at,
    )


@router.get(
    "/orders",
    response_model=OrderListResponse,
)
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
    current_user: UserAccount = Depends(require_roles(ORDER_READ_ROLES)),
):
    """List orders with optional filters"""
    query = db.query(Order)
    if _is_customer(current_user):
        query = query.filter(Order.customer_id == str(current_user.id))

    if status:
        normalized_status = status.strip().upper()
        if normalized_status not in VALID_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {VALID_STATUSES}",
            )
        query = query.filter(Order.current_state == OrderStatus(normalized_status))
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
        orders=[OrderResponse.model_validate(o) for o in orders],
    )


@router.get(
    "/orders/stats/summary",
    dependencies=[Depends(require_roles(SUPPORT_READ_ROLES))],
)
async def get_order_stats(db: Session = Depends(get_db)):
    """Get order summary statistics"""
    from sqlalchemy import func as sql_func

    total_orders = db.query(sql_func.count(Order.id)).scalar() or 0

    status_counts = (
        db.query(Order.current_state, sql_func.count(Order.id))
        .group_by(Order.current_state)
        .all()
    )
    status_map = {getattr(s, "value", str(s)): c for s, c in status_counts}

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


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
)
async def get_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(ORDER_READ_ROLES)),
):
    """Get a specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    _assert_customer_owns_order(order, current_user)
    return order


@router.patch(
    "/orders/{order_id}",
    response_model=OrderResponse,
)
async def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(CUSTOMER_ORDER_ROLES)),
):
    """Update editable order commercial fields.

    Lifecycle status changes must go through /orders/{order_id}/transition.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    _assert_customer_owns_order(order, current_user)

    update_data = order_data.model_dump(exclude_unset=True)

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


@router.post(
    "/orders/{order_id}/transition",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles(OPS_ADMIN_ROLES))],
)
@transition_alias_router.post(
    "/orders/{order_id}/transition",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles(OPS_ADMIN_ROLES))],
)
async def transition_order_status(
    order_id: UUID,
    transition_data: OrderTransitionRequest,
    db: Session = Depends(get_db),
):
    """Request an order lifecycle transition through the policy gateway."""
    return transition_order(
        db,
        order_id=order_id,
        event=transition_data.event,
        payload=transition_data.payload,
        actor_role=transition_data.actor_role,
        actor_id=transition_data.actor_id,
        idempotency_key=transition_data.idempotency_key,
        trace_id=transition_data.trace_id,
        to_state=transition_data.to_state,
        reason=transition_data.reason,
        evidence_ref=transition_data.evidence_ref,
    )


@router.get(
    "/orders/{order_id}/events",
    response_model=OrderStateEventListResponse,
    dependencies=[Depends(require_roles(SUPPORT_READ_ROLES))],
)
async def list_order_state_events(order_id: UUID, db: Session = Depends(get_db)):
    """List lifecycle state events for an order."""
    order = get_order_or_404(db, order_id)
    events = order.state_events
    return OrderStateEventListResponse(
        total=len(events),
        events=[StateAuditLogResponse.model_validate(event) for event in events],
    )


@router.post(
    "/orders/{order_id}/cancel",
    response_model=OrderResponse,
    dependencies=[Depends(require_roles(OPS_ADMIN_ROLES))],
)
async def cancel_order(order_id: UUID, db: Session = Depends(get_db)):
    """Cancel an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return transition_order(
        db,
        order_id=order_id,
        to_state=OrderStatus.CANCELLED.value,
        event="order_cancelled",
        payload={"reason": "Cancel endpoint requested"},
        actor_role="OMS",
        actor_id=None,
        idempotency_key=uuid5(NAMESPACE_URL, f"cancel:{order_id}"),
        trace_id=f"cancel-{order_id}",
        reason="Cancel endpoint requested",
    )
