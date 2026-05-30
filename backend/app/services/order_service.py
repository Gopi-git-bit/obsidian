"""Order workflow service with canonical state-machine enforcement."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.order_model import (
    ActorRole,
    AgentDLQMessage,
    ConsentStatus,
    Order,
    OrderStatus,
    PaymentMode,
    StateAuditLog,
    TERMINAL_ORDER_STATUSES,
    VehicleReservation,
)

ERROR_INVALID_INPUT = "INVALID_INPUT"
ERROR_POLICY_VIOLATION = "POLICY_VIOLATION"
ERROR_CONFLICT = "CONFLICT"
ERROR_DLQ_PUSHED = "DLQ_PUSHED"

IDEMPOTENCY_WINDOW = timedelta(hours=24)


ORDER_STATE_GRAPH: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.CREATED: {
        OrderStatus.PAYMENT_PENDING,
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.PAYMENT_PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.RINGING,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.RINGING: {
        OrderStatus.ASSIGNED,
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.ASSIGNED: {
        OrderStatus.EN_ROUTE_TO_PICKUP,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.EN_ROUTE_TO_PICKUP: {
        OrderStatus.AT_PICKUP_WAITING,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.AT_PICKUP_WAITING: {
        OrderStatus.LOADING,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.LOADING: {
        OrderStatus.DEPARTED_FOR_DELIVERY,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.DEPARTED_FOR_DELIVERY: {
        OrderStatus.AT_DELIVERY_WAITING,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.AT_DELIVERY_WAITING: {
        OrderStatus.DELIVERED_PENDING_SETTLEMENT,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.DELIVERED_PENDING_SETTLEMENT: {
        OrderStatus.COMPLETED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
    OrderStatus.SUSPENDED: set(),
    OrderStatus.INCIDENT: {
        OrderStatus.RINGING,
        OrderStatus.ASSIGNED,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
    },
}


ROLE_STATE_PERMISSIONS: dict[ActorRole, set[OrderStatus]] = {
    ActorRole.OMS: {
        OrderStatus.PAYMENT_PENDING,
        OrderStatus.CONFIRMED,
        OrderStatus.RINGING,
        OrderStatus.CANCELLED,
        OrderStatus.INCIDENT,
    },
    ActorRole.TMS: {
        OrderStatus.RINGING,
        OrderStatus.ASSIGNED,
        OrderStatus.EN_ROUTE_TO_PICKUP,
        OrderStatus.AT_PICKUP_WAITING,
        OrderStatus.LOADING,
        OrderStatus.DEPARTED_FOR_DELIVERY,
        OrderStatus.AT_DELIVERY_WAITING,
        OrderStatus.INCIDENT,
    },
    ActorRole.FIN: {
        OrderStatus.PAYMENT_PENDING,
        OrderStatus.CONFIRMED,
        OrderStatus.COMPLETED,
        OrderStatus.INCIDENT,
    },
    ActorRole.RAG: set(),
    ActorRole.SUP: {
        OrderStatus.RINGING,
        OrderStatus.ASSIGNED,
        OrderStatus.CANCELLED,
        OrderStatus.SUSPENDED,
        OrderStatus.INCIDENT,
    },
    ActorRole.CUSTOMER: {
        OrderStatus.PAYMENT_PENDING,
        OrderStatus.CANCELLED,
    },
    ActorRole.DRIVER: {
        OrderStatus.ASSIGNED,
        OrderStatus.EN_ROUTE_TO_PICKUP,
        OrderStatus.AT_PICKUP_WAITING,
        OrderStatus.LOADING,
        OrderStatus.DEPARTED_FOR_DELIVERY,
        OrderStatus.AT_DELIVERY_WAITING,
        OrderStatus.DELIVERED_PENDING_SETTLEMENT,
        OrderStatus.INCIDENT,
    },
    ActorRole.ADMIN: set(OrderStatus),
}


def parse_order_status(value: str | OrderStatus) -> OrderStatus:
    if isinstance(value, OrderStatus):
        return value
    normalized = value.strip().upper()
    if normalized == "ALLOCATED":
        normalized = OrderStatus.ASSIGNED.value
    try:
        return OrderStatus(normalized)
    except ValueError as exc:
        valid = [status.value for status in OrderStatus]
        raise HTTPException(
            status_code=400,
            detail={"error_code": ERROR_INVALID_INPUT, "message": f"Invalid state. Must be one of: {valid}"},
        ) from exc


def parse_actor_role(value: str | ActorRole) -> ActorRole:
    if isinstance(value, ActorRole):
        return value
    normalized = value.strip().upper()
    try:
        return ActorRole(normalized)
    except ValueError as exc:
        valid = [role.value for role in ActorRole]
        raise HTTPException(
            status_code=403,
            detail={"error_code": ERROR_INVALID_INPUT, "message": f"Unknown actor_role. Must be one of: {valid}"},
        ) from exc


def get_order_or_404(db: Session, order_id: UUID) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=404,
            detail={"error_code": ERROR_INVALID_INPUT, "message": "Order not found"},
        )
    return order


def _jsonable(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _payload_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(_jsonable(payload), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _error(status_code: int, code: str, message: str, trace_id: str | None = None):
    detail: dict[str, Any] = {"error_code": code, "message": message}
    if trace_id:
        detail["trace_id"] = trace_id
    raise HTTPException(status_code=status_code, detail=detail)


def _push_dlq(
    db: Session,
    *,
    order_id: UUID | None,
    event: str,
    actor_role: str,
    idempotency_key: str | None,
    trace_id: str | None,
    error_code: str,
    error_detail: str,
    payload: dict[str, Any],
) -> None:
    try:
        db.rollback()
        db.add(
            AgentDLQMessage(
                order_id=order_id,
                event_name=event or "unknown",
                actor_role=actor_role or "unknown",
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                error_code=error_code,
                error_detail=error_detail,
                payload=_jsonable(payload),
            )
        )
        db.commit()
    except Exception:
        db.rollback()


def _fail_with_dlq(
    db: Session,
    *,
    status_code: int,
    error_code: str,
    message: str,
    order_id: UUID | None,
    event: str,
    actor_role: str,
    idempotency_key: UUID | str | None,
    trace_id: str | None,
    payload: dict[str, Any],
):
    _push_dlq(
        db,
        order_id=order_id,
        event=event,
        actor_role=actor_role,
        idempotency_key=str(idempotency_key) if idempotency_key else None,
        trace_id=trace_id,
        error_code=error_code,
        error_detail=message,
        payload=payload,
    )
    _error(status_code, error_code, f"{message}; routed to agent.dlq", trace_id)


def _ensure_role_can_transition(
    role: ActorRole,
    target_state: OrderStatus,
    *,
    db: Session,
    order_id: UUID,
    event: str,
    idempotency_key: UUID,
    trace_id: str,
    payload: dict[str, Any],
) -> None:
    allowed = ROLE_STATE_PERMISSIONS[role]
    if target_state not in allowed:
        _fail_with_dlq(
            db,
            status_code=403,
            error_code=ERROR_POLICY_VIOLATION,
            message=f"Role {role.value} cannot transition to {target_state.value}",
            order_id=order_id,
            event=event,
            actor_role=role.value,
            idempotency_key=idempotency_key,
            trace_id=trace_id,
            payload=payload,
        )


def _validate_business_rules(
    order: Order,
    target_state: OrderStatus,
    payload: dict[str, Any],
    *,
    db: Session,
    event: str,
    actor_role: ActorRole,
    idempotency_key: UUID,
    trace_id: str,
) -> None:
    if target_state == OrderStatus.CONFIRMED:
        payment_mode = payload.get("payment_mode", order.payment_mode.value)
        consent = payload.get("topay_consent_status", order.topay_consent_status.value)
        material = payload.get("material_type", order.material_type)
        body = payload.get("body_type_required", order.body_type_required)

        if payment_mode == PaymentMode.TOPAY.value and consent != ConsentStatus.ACCEPTED.value:
            _fail_with_dlq(
                db,
                status_code=409,
                error_code=ERROR_POLICY_VIOLATION,
                message="ToPay orders cannot be CONFIRMED until consent is accepted",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )
        if material.strip().lower() == "pharma" and body.strip().lower() != "closed":
            _fail_with_dlq(
                db,
                status_code=409,
                error_code=ERROR_POLICY_VIOLATION,
                message="Pharma orders require closed body vehicle before CONFIRMED",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )

    if event == "driver_response":
        action = payload.get("action")
        if action == "ACCEPT" and target_state != OrderStatus.ASSIGNED:
            _fail_with_dlq(
                db,
                status_code=400,
                error_code=ERROR_INVALID_INPUT,
                message="driver_response ACCEPT must target ASSIGNED",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )
        if action in {"REJECT", "TIMEOUT"} and target_state == OrderStatus.ASSIGNED:
            _fail_with_dlq(
                db,
                status_code=409,
                error_code=ERROR_POLICY_VIOLATION,
                message="driver_response REJECT/TIMEOUT cannot assign order",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )

    if event == "shipment_doc_scanned":
        required = {"doc_type", "doc_url", "scan_exif"}
        if target_state != OrderStatus.LOADING or not required.issubset(payload):
            _fail_with_dlq(
                db,
                status_code=400,
                error_code=ERROR_INVALID_INPUT,
                message="shipment_doc_scanned requires doc_type, doc_url, scan_exif and target LOADING",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )

    if event == "pod_scanned":
        required = {"pod_url", "consignee_otp", "pod_exif"}
        if (
            target_state != OrderStatus.DELIVERED_PENDING_SETTLEMENT
            or not required.issubset(payload)
        ):
            _fail_with_dlq(
                db,
                status_code=400,
                error_code=ERROR_INVALID_INPUT,
                message="pod_scanned requires pod_url, consignee_otp, pod_exif and target DELIVERED_PENDING_SETTLEMENT",
                order_id=order.id,
                event=event,
                actor_role=actor_role.value,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload=payload,
            )


def _release_expired_reservations(db: Session) -> None:
    now = datetime.now(timezone.utc)
    (
        db.query(VehicleReservation)
        .filter(
            VehicleReservation.is_active.is_(True),
            VehicleReservation.expires_at <= now,
        )
        .update({VehicleReservation.is_active: False}, synchronize_session=False)
    )


def _reserve_vehicle_if_needed(
    db: Session,
    *,
    order: Order,
    target_state: OrderStatus,
    payload: dict[str, Any],
) -> None:
    vehicle_id = payload.get("vehicle_id")
    expires_at = payload.get("expires_at")
    if not vehicle_id or target_state not in {OrderStatus.RINGING, OrderStatus.ASSIGNED}:
        return
    if isinstance(vehicle_id, str):
        vehicle_id = UUID(vehicle_id)

    _release_expired_reservations(db)

    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    if expires_at is None:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)

    existing = (
        db.query(VehicleReservation)
        .filter(
            VehicleReservation.vehicle_id == vehicle_id,
            VehicleReservation.is_active.is_(True),
            VehicleReservation.order_id != order.id,
        )
        .first()
    )
    if existing:
        raise IntegrityError("vehicle already actively reserved", None, None)

    own_existing = (
        db.query(VehicleReservation)
        .filter(
            VehicleReservation.vehicle_id == vehicle_id,
            VehicleReservation.order_id == order.id,
            VehicleReservation.is_active.is_(True),
        )
        .first()
    )
    if own_existing:
        own_existing.expires_at = expires_at
    else:
        db.add(
            VehicleReservation(
                vehicle_id=vehicle_id,
                order_id=order.id,
                expires_at=expires_at,
                is_active=True,
            )
        )
    order.vehicle_id = vehicle_id


def transition_order(
    db: Session,
    *,
    order_id: UUID,
    event: str,
    payload: dict[str, Any],
    actor_role: str,
    idempotency_key: UUID,
    trace_id: str,
    to_state: str | OrderStatus | None = None,
    new_status: str | None = None,
    actor_id: str | None = None,
    reason: str | None = None,
    evidence_ref: str | None = None,
) -> Order | dict[str, Any]:
    """Apply a lifecycle transition through the only state mutation gateway."""

    target_state = parse_order_status(to_state or new_status or "")
    role = parse_actor_role(actor_role)
    request_payload = {
        "order_id": str(order_id),
        "event": event,
        "payload": _jsonable(payload),
        "actor_role": role.value,
        "to_state": target_state.value,
        "actor_id": actor_id,
        "reason": reason,
        "evidence_ref": evidence_ref,
    }
    payload_hash = _payload_hash(request_payload)
    since = datetime.now(timezone.utc) - IDEMPOTENCY_WINDOW

    existing_log = (
        db.query(StateAuditLog)
        .filter(
            StateAuditLog.idempotency_key == idempotency_key,
            StateAuditLog.timestamp >= since,
        )
        .order_by(StateAuditLog.timestamp.desc())
        .first()
    )
    if existing_log:
        if existing_log.payload_hash != payload_hash:
            _error(
                409,
                ERROR_CONFLICT,
                "Idempotency key replay uses different payload",
                trace_id,
            )
        return get_order_or_404(db, order_id)

    order = get_order_or_404(db, order_id)
    current_state = parse_order_status(order.current_state)

    if current_state in TERMINAL_ORDER_STATUSES:
        _fail_with_dlq(
            db,
            status_code=409,
            error_code=ERROR_POLICY_VIOLATION,
            message=f"Cannot transition terminal order in {current_state.value}",
            order_id=order_id,
            event=event,
            actor_role=role.value,
            idempotency_key=idempotency_key,
            trace_id=trace_id,
            payload=payload,
        )

    allowed_next = ORDER_STATE_GRAPH.get(current_state, set())
    if target_state not in allowed_next:
        _fail_with_dlq(
            db,
            status_code=400,
            error_code=ERROR_INVALID_INPUT,
            message=f"Illegal transition {current_state.value} -> {target_state.value}",
            order_id=order_id,
            event=event,
            actor_role=role.value,
            idempotency_key=idempotency_key,
            trace_id=trace_id,
            payload=payload,
        )

    _ensure_role_can_transition(
        role,
        target_state,
        db=db,
        order_id=order_id,
        event=event,
        idempotency_key=idempotency_key,
        trace_id=trace_id,
        payload=payload,
    )
    _validate_business_rules(
        order,
        target_state,
        payload,
        db=db,
        event=event,
        actor_role=role,
        idempotency_key=idempotency_key,
        trace_id=trace_id,
    )

    if target_state == OrderStatus.CONFIRMED:
        if "payment_mode" in payload:
            order.payment_mode = PaymentMode(payload["payment_mode"])
        if "topay_consent_status" in payload:
            order.topay_consent_status = ConsentStatus(payload["topay_consent_status"])
        if "material_type" in payload:
            order.material_type = payload["material_type"]
        if "body_type_required" in payload:
            order.body_type_required = payload["body_type_required"]

    try:
        _reserve_vehicle_if_needed(
            db, order=order, target_state=target_state, payload=payload
        )
        order.current_state = target_state
        metadata = dict(order.payload_metadata or {})
        metadata[event] = payload
        order.payload_metadata = metadata
        cached_response = {
            "id": str(order.id),
            "current_state": target_state.value,
            "status": target_state.value,
            "trace_id": trace_id,
        }
        db.add(
            StateAuditLog(
                order_id=order.id,
                from_state=current_state,
                to_state=target_state,
                event_name=event,
                actor_role=role,
                actor_id=actor_id,
                idempotency_key=idempotency_key,
                trace_id=trace_id,
                payload_hash=payload_hash,
                request_payload=request_payload,
                cached_response=cached_response,
            )
        )
        db.commit()
    except IntegrityError as exc:
        _fail_with_dlq(
            db,
            status_code=409,
            error_code=ERROR_CONFLICT,
            message="Database constraint failure or active vehicle reservation conflict",
            order_id=order_id,
            event=event,
            actor_role=role.value,
            idempotency_key=idempotency_key,
            trace_id=trace_id,
            payload=payload,
        )
        raise exc
    except HTTPException:
        raise
    except Exception as exc:
        _fail_with_dlq(
            db,
            status_code=503,
            error_code=ERROR_DLQ_PUSHED,
            message=f"Unexpected transition failure: {exc}",
            order_id=order_id,
            event=event,
            actor_role=role.value,
            idempotency_key=idempotency_key,
            trace_id=trace_id,
            payload=payload,
        )

    db.refresh(order)
    return order
