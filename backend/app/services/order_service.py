"""Order workflow service with policy-checked lifecycle transitions."""

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.order_model import (
    Order,
    OrderStateEvent,
    OrderStatus,
    TERMINAL_ORDER_STATUSES,
)


ORDER_STATUS_GRAPH: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.CREATED: {
        OrderStatus.PENDING_MATCH,
        OrderStatus.BIDDING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PENDING_MATCH: {
        OrderStatus.MATCHED,
        OrderStatus.BIDDING,
        OrderStatus.CANCELLED,
    },
    OrderStatus.BIDDING: {OrderStatus.BID_ACCEPTED, OrderStatus.CANCELLED},
    OrderStatus.MATCHED: {OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED},
    OrderStatus.BID_ACCEPTED: {OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED},
    OrderStatus.IN_TRANSIT: {OrderStatus.DELIVERED, OrderStatus.CANCELLED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


ROLE_STATUS_PERMISSIONS: dict[str, set[OrderStatus]] = {
    "OMS": {
        OrderStatus.PENDING_MATCH,
        OrderStatus.BIDDING,
        OrderStatus.BID_ACCEPTED,
        OrderStatus.CANCELLED,
    },
    "IMS": {
        OrderStatus.MATCHED,
        OrderStatus.BID_ACCEPTED,
    },
    "TMS": {
        OrderStatus.IN_TRANSIT,
        OrderStatus.DELIVERED,
    },
    "FIN": set(),
    "FINANCE": set(),
    "ADMIN": set(OrderStatus),
}


def parse_order_status(value: str) -> OrderStatus:
    try:
        return OrderStatus(value)
    except ValueError as exc:
        valid = [status.value for status in OrderStatus]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {valid}",
        ) from exc


def get_order_or_404(db: Session, order_id: UUID) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def _normalize_role(actor_role: str) -> str:
    return actor_role.strip().upper()


def _ensure_role_can_transition(actor_role: str, new_status: OrderStatus) -> None:
    role = _normalize_role(actor_role)
    allowed = ROLE_STATUS_PERMISSIONS.get(role)
    if allowed is None:
        raise HTTPException(status_code=403, detail=f"Unknown actor_role: {actor_role}")
    if new_status not in allowed:
        raise HTTPException(
            status_code=403,
            detail=f"Role {role} cannot transition to {new_status.value}",
        )


def transition_order(
    db: Session,
    *,
    order_id: UUID,
    new_status: str,
    event: str,
    actor_role: str,
    idempotency_key: str,
    actor_id: str | None = None,
    reason: str | None = None,
    evidence_ref: str | None = None,
) -> Order:
    """Apply a lifecycle transition and write an auditable state event."""

    existing_event = (
        db.query(OrderStateEvent)
        .filter(OrderStateEvent.idempotency_key == idempotency_key)
        .first()
    )
    if existing_event:
        if existing_event.order_id != order_id:
            raise HTTPException(
                status_code=409,
                detail="Idempotency key already used for another order",
            )
        target_status = parse_order_status(new_status)
        if (
            existing_event.to_status != target_status
            or existing_event.event != event
            or existing_event.actor_role != _normalize_role(actor_role)
        ):
            raise HTTPException(
                status_code=409,
                detail="Idempotency key replay does not match original transition",
            )
        return get_order_or_404(db, order_id)

    order = get_order_or_404(db, order_id)
    target_status = parse_order_status(new_status)
    current_status = OrderStatus(order.status.value)

    if current_status in TERMINAL_ORDER_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition terminal order in {current_status.value} status",
        )

    allowed_next = ORDER_STATUS_GRAPH.get(current_status, set())
    if target_status not in allowed_next:
        raise HTTPException(
            status_code=400,
            detail=f"Illegal transition {current_status.value} -> {target_status.value}",
        )

    _ensure_role_can_transition(actor_role, target_status)

    state_event = OrderStateEvent(
        order_id=order.id,
        from_status=current_status,
        to_status=target_status,
        event=event,
        actor_role=_normalize_role(actor_role),
        actor_id=actor_id,
        idempotency_key=idempotency_key,
        reason=reason,
        evidence_ref=evidence_ref,
    )
    order.status = target_status
    db.add(state_event)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Duplicate idempotency key or transition conflict",
        ) from exc

    db.refresh(order)
    return order
