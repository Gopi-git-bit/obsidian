"""Order-to-settlement flow endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import (
    CUSTOMER_ORDER_ROLES,
    DRIVER_TRIP_ROLES,
    FINANCE_ADMIN_ROLES,
    OPS_ADMIN_ROLES,
    SUPPORT_READ_ROLES,
    TRANSPORT_COMPANY_ROLES,
    VERIFICATION_ROLES,
    require_roles,
)
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole
from app.models.flow_model import (
    GSTInvoiceRecord,
    JournalEntry,
    PaymentRecord,
    QuoteRecord,
    SettlementRecord,
    Trip,
    TripDocument,
    TripMilestone,
)
from app.models.order_model import Match, Order, OrderStatus
from app.models.vehicle_model import VehicleModel
from app.models.supervisor_model import FraudHold
from app.services.order_service import transition_order

router = APIRouter()

FLOW_STEPS = (
    "quote",
    "match",
    "trip",
    "advance_payment",
    "loading_photo",
    "trip_milestone",
    "pod_uploaded",
    "pod_verified",
    "otp_verified",
    "settlement",
    "journal_entry",
    "gst_invoice",
)


class IdempotentPayload(BaseModel):
    idempotency_key: str = Field(..., min_length=1, max_length=120)


class AdvancePaymentRequest(IdempotentPayload):
    amount: float = Field(..., gt=0)
    currency: str = "INR"
    provider_ref: str | None = None


class LoadingPhotoRequest(IdempotentPayload):
    photo_url: str = Field(..., min_length=1)
    uploaded_by: str = Field(..., min_length=1)


class MilestoneRequest(IdempotentPayload):
    milestone_type: str = Field(..., min_length=1, max_length=60)
    status: str = "recorded"
    payload: dict = Field(default_factory=dict)


class PODUploadRequest(IdempotentPayload):
    pod_url: str = Field(..., min_length=1)
    consignee_otp: str = Field(..., min_length=4)
    pod_exif: dict = Field(default_factory=dict)
    uploaded_by: str = Field(..., min_length=1)


class PODVerifyRequest(IdempotentPayload):
    verified_by: str = Field(..., min_length=1)


class OTPVerifyRequest(IdempotentPayload):
    otp: str = Field(..., min_length=4)
    verified_by: str = Field(..., min_length=1)


class SettlementReleaseRequest(IdempotentPayload):
    amount: float = Field(..., gt=0)
    commission_amount: float = Field(..., ge=0)
    gst_amount: float = Field(..., ge=0)
    driver_payable_amount: float = Field(..., ge=0)
    currency: str = "INR"


class DriverAssignRequest(BaseModel):
    driver_id: str = Field(..., min_length=1, max_length=80)


class TripAcknowledgeRequest(IdempotentPayload):
    acknowledged_by: str | None = Field(None, max_length=80)


def _order_or_404(db: Session, order_id: UUID) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def _trip_or_404(db: Session, trip_id: UUID) -> Trip:
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


def _assert_customer_owns_order(order: Order, user: UserAccount) -> None:
    if user.role == UserRole.CUSTOMER and order.customer_id != str(user.id):
        raise HTTPException(status_code=404, detail="Order not found")


def _assert_driver_owns_trip(trip: Trip, user: UserAccount) -> None:
    if user.role == UserRole.DRIVER and trip.driver_id != str(user.id):
        raise HTTPException(status_code=404, detail="Trip not found")


def _assert_company_owns_trip(trip: Trip, user: UserAccount) -> None:
    if user.role == UserRole.TRANSPORT_COMPANY and trip.transport_company_id != str(user.id):
        raise HTTPException(status_code=404, detail="Trip not found")


def _value(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "__float__"):
        try:
            return float(value)
        except (TypeError, ValueError):
            return value
    return value


def _row_dict(row, fields: tuple[str, ...]) -> dict:
    return {field: _value(getattr(row, field)) for field in fields}


def _driver_trip_summary(db: Session, trip: Trip) -> dict:
    order = _order_or_404(db, trip.order_id)
    match = (
        db.query(Match)
        .filter(Match.order_id == trip.order_id, Match.vehicle_id == trip.vehicle_id)
        .order_by(Match.accepted_at.desc().nullslast(), Match.matched_at.desc())
        .first()
    )
    documents = (
        db.query(TripDocument)
        .filter(TripDocument.trip_id == trip.trip_id)
        .order_by(TripDocument.uploaded_at.desc())
        .all()
    )
    milestones = (
        db.query(TripMilestone)
        .filter(TripMilestone.trip_id == trip.trip_id)
        .order_by(TripMilestone.recorded_at.desc())
        .all()
    )
    loading_photos = [doc for doc in documents if doc.document_type == "loading_photo"]
    pods = [doc for doc in documents if doc.document_type == "pod"]
    return {
        "trip": _row_dict(
            trip,
            ("trip_id", "order_id", "vehicle_id", "driver_id", "status", "otp_verified", "created_at", "updated_at"),
        ),
        "order": _row_dict(
            order,
            ("id", "origin_city", "origin_state", "destination_city", "destination_state", "current_state", "weight_kg", "num_packages"),
        ),
        "match": _row_dict(match, ("id", "match_score", "status", "matched_at", "accepted_at")) if match else None,
        "milestones": [
            _row_dict(m, ("milestone_id", "milestone_type", "status", "payload", "recorded_at"))
            for m in milestones
        ],
        "loading_proofs": [
            _row_dict(d, ("document_id", "document_url", "verification_status", "payload", "uploaded_at", "verified_at"))
            for d in loading_photos
        ],
        "pod_status": {
            "uploaded": bool(pods),
            "verified": any(doc.verification_status == "verified" for doc in pods),
            "latest_status": pods[0].verification_status if pods else "missing",
        },
        "otp_status": {"verified": trip.otp_verified == "true"},
    }


def _transport_trip_summary(db: Session, trip: Trip) -> dict:
    order = _order_or_404(db, trip.order_id)
    settlements = (
        db.query(SettlementRecord)
        .filter(SettlementRecord.trip_id == trip.trip_id)
        .order_by(SettlementRecord.released_at.desc())
        .all()
    )
    return {
        "trip": _row_dict(trip, ("trip_id", "order_id", "vehicle_id", "transport_company_id", "status", "created_at", "updated_at")),
        "order": _row_dict(order, ("id", "origin_city", "destination_city", "current_state", "weight_kg")),
        "settlement_visibility": [
            _row_dict(s, ("settlement_id", "status", "amount", "currency", "released_at"))
            for s in settlements
        ],
    }


def create_trip_for_order(db: Session, *, order_id: UUID, vehicle_id: UUID) -> Trip:
    existing = db.query(Trip).filter(Trip.order_id == order_id).first()
    if existing:
        return existing
    vehicle = db.query(VehicleModel).filter_by(id=vehicle_id).first()
    trip = Trip(
        order_id=order_id,
        vehicle_id=vehicle_id,
        transport_company_id=getattr(vehicle, "transport_company_id", None),
        status="created",
    )
    db.add(trip)
    db.flush()
    return trip


def _record_milestone(
    db: Session,
    *,
    trip: Trip,
    milestone_type: str,
    idempotency_key: str,
    status: str = "recorded",
    payload: dict | None = None,
) -> TripMilestone:
    existing = db.query(TripMilestone).filter(TripMilestone.idempotency_key == idempotency_key).first()
    if existing:
        return existing
    milestone = TripMilestone(
        order_id=trip.order_id,
        trip_id=trip.trip_id,
        milestone_type=milestone_type,
        status=status,
        payload=payload or {},
        idempotency_key=idempotency_key,
    )
    db.add(milestone)
    trip.status = milestone_type.lower()
    db.flush()
    return milestone


@router.get(
    "/orders/{order_id}/flow-summary",
    dependencies=[Depends(require_roles(SUPPORT_READ_ROLES))],
)
async def get_order_flow_summary(order_id: UUID, db: Session = Depends(get_db)):
    order = _order_or_404(db, order_id)
    quotes = db.query(QuoteRecord).filter(QuoteRecord.order_id == order.id).order_by(QuoteRecord.created_at.desc()).all()
    matches = db.query(Match).filter(Match.order_id == order.id).order_by(Match.matched_at.desc()).all()
    trip = db.query(Trip).filter(Trip.order_id == order.id).first()
    payments = db.query(PaymentRecord).filter(PaymentRecord.order_id == order.id).order_by(PaymentRecord.recorded_at.desc()).all()
    documents = db.query(TripDocument).filter(TripDocument.order_id == order.id).order_by(TripDocument.uploaded_at.desc()).all()
    milestones = db.query(TripMilestone).filter(TripMilestone.order_id == order.id).order_by(TripMilestone.recorded_at.desc()).all()
    settlements = db.query(SettlementRecord).filter(SettlementRecord.order_id == order.id).order_by(SettlementRecord.released_at.desc()).all()
    journal_entries = db.query(JournalEntry).filter(JournalEntry.order_id == order.id).order_by(JournalEntry.created_at.desc()).all()
    gst_invoices = db.query(GSTInvoiceRecord).filter(GSTInvoiceRecord.order_id == order.id).order_by(GSTInvoiceRecord.created_at.desc()).all()

    loading_photos = [doc for doc in documents if doc.document_type == "loading_photo"]
    pods = [doc for doc in documents if doc.document_type == "pod"]
    verified_pods = [doc for doc in pods if doc.verification_status == "verified"]
    advance_payments = [payment for payment in payments if payment.payment_type == "advance"]

    present = {
        "quote": bool(quotes),
        "match": bool(matches),
        "trip": trip is not None,
        "advance_payment": bool(advance_payments),
        "loading_photo": bool(loading_photos),
        "trip_milestone": bool(milestones),
        "pod_uploaded": bool(pods),
        "pod_verified": bool(verified_pods),
        "otp_verified": bool(trip and trip.otp_verified == "true"),
        "settlement": bool(settlements),
        "journal_entry": bool(journal_entries),
        "gst_invoice": bool(gst_invoices),
    }

    return {
        "order_id": str(order.id),
        "current_state": order.current_state.value,
        "steps": [
            {"step": step, "status": "present" if present[step] else "missing"}
            for step in FLOW_STEPS
        ],
        "missing_steps": [step for step in FLOW_STEPS if not present[step]],
        "quote_records": [
            _row_dict(q, ("quote_id", "order_id", "currency", "base_amount", "platform_fee", "gst_amount", "total_amount", "status", "created_at"))
            for q in quotes
        ],
        "matches": [
            _row_dict(m, ("id", "order_id", "vehicle_id", "match_score", "utilization_percent", "efficiency_score", "agreed_price", "platform_fee", "gst_amount", "total_amount", "status", "matched_at", "accepted_at"))
            for m in matches
        ],
        "trip": _row_dict(trip, ("trip_id", "order_id", "vehicle_id", "status", "otp_verified", "created_at", "updated_at")) if trip else None,
        "payment_records": [
            _row_dict(p, ("payment_id", "order_id", "trip_id", "payment_type", "status", "amount", "currency", "provider_ref", "recorded_at"))
            for p in payments
        ],
        "loading_photos": [
            _row_dict(d, ("document_id", "order_id", "trip_id", "document_type", "document_url", "verification_status", "payload", "uploaded_at", "verified_at"))
            for d in loading_photos
        ],
        "milestones": [
            _row_dict(m, ("milestone_id", "order_id", "trip_id", "milestone_type", "status", "payload", "recorded_at"))
            for m in milestones
        ],
        "pod_records": [
            _row_dict(d, ("document_id", "order_id", "trip_id", "document_type", "document_url", "verification_status", "payload", "uploaded_at", "verified_at"))
            for d in pods
        ],
        "settlement_records": [
            _row_dict(s, ("settlement_id", "order_id", "trip_id", "status", "amount", "currency", "released_at"))
            for s in settlements
        ],
        "journal_entries": [
            _row_dict(j, ("journal_entry_id", "order_id", "settlement_id", "debit_ledger", "credit_ledger", "amount", "currency", "created_at"))
            for j in journal_entries
        ],
        "gst_invoice_records": [
            _row_dict(i, ("invoice_id", "order_id", "settlement_id", "invoice_number", "taxable_amount", "gst_amount", "total_amount", "status", "created_at"))
            for i in gst_invoices
        ],
    }


@router.get(
    "/orders/{order_id}/customer-flow-summary",
    dependencies=[Depends(require_roles(CUSTOMER_ORDER_ROLES))],
)
async def get_customer_order_flow_summary(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(CUSTOMER_ORDER_ROLES)),
):
    order = _order_or_404(db, order_id)
    _assert_customer_owns_order(order, current_user)

    quotes = (
        db.query(QuoteRecord)
        .filter(QuoteRecord.order_id == order.id)
        .order_by(QuoteRecord.created_at.desc())
        .all()
    )
    matches = (
        db.query(Match)
        .filter(Match.order_id == order.id)
        .order_by(Match.matched_at.desc())
        .all()
    )
    trip = db.query(Trip).filter(Trip.order_id == order.id).first()
    documents = (
        db.query(TripDocument)
        .filter(TripDocument.order_id == order.id)
        .order_by(TripDocument.uploaded_at.desc())
        .all()
    )
    milestones = (
        db.query(TripMilestone)
        .filter(TripMilestone.order_id == order.id)
        .order_by(TripMilestone.recorded_at.desc())
        .all()
    )
    settlements = (
        db.query(SettlementRecord)
        .filter(SettlementRecord.order_id == order.id)
        .order_by(SettlementRecord.released_at.desc())
        .all()
    )
    invoices = (
        db.query(GSTInvoiceRecord)
        .filter(GSTInvoiceRecord.order_id == order.id)
        .order_by(GSTInvoiceRecord.created_at.desc())
        .all()
    )

    pods = [doc for doc in documents if doc.document_type == "pod"]
    verified_pods = [doc for doc in pods if doc.verification_status == "verified"]

    return {
        "order_id": str(order.id),
        "current_state": order.current_state.value,
        "quote_records": [
            _row_dict(q, ("quote_id", "currency", "total_amount", "status", "created_at"))
            for q in quotes
        ],
        "match_status": [
            _row_dict(m, ("id", "match_score", "status", "matched_at", "accepted_at"))
            for m in matches
        ],
        "trip_status": _row_dict(trip, ("trip_id", "status", "created_at", "updated_at")) if trip else None,
        "milestone_status": [
            _row_dict(m, ("milestone_id", "milestone_type", "status", "recorded_at"))
            for m in milestones
        ],
        "pod_status": {
            "uploaded": bool(pods),
            "verified": bool(verified_pods),
            "latest_status": pods[0].verification_status if pods else "missing",
        },
        "otp_status": {"verified": bool(trip and trip.otp_verified == "true")},
        "settlement_visibility": [
            _row_dict(s, ("settlement_id", "status", "amount", "currency", "released_at"))
            for s in settlements
        ],
        "invoice_visibility": [
            _row_dict(i, ("invoice_id", "invoice_number", "status", "total_amount", "created_at"))
            for i in invoices
        ],
    }


@router.get(
    "/driver/trips",
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def list_driver_trips(
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    query = db.query(Trip)
    if current_user.role == UserRole.DRIVER:
        query = query.filter(Trip.driver_id == str(current_user.id))
    trips = query.order_by(Trip.updated_at.desc()).all()
    return {
        "total": len(trips),
        "trips": [_driver_trip_summary(db, trip) for trip in trips],
    }


@router.get(
    "/driver/trips/{trip_id}",
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def get_driver_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_driver_owns_trip(trip, current_user)
    return _driver_trip_summary(db, trip)


@router.get(
    "/transport-company/trips",
    dependencies=[Depends(require_roles(TRANSPORT_COMPANY_ROLES))],
)
async def list_transport_company_trips(
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(TRANSPORT_COMPANY_ROLES)),
):
    query = db.query(Trip)
    if current_user.role == UserRole.TRANSPORT_COMPANY:
        query = query.filter(Trip.transport_company_id == str(current_user.id))
    trips = query.order_by(Trip.updated_at.desc()).all()
    return {"total": len(trips), "trips": [_transport_trip_summary(db, trip) for trip in trips]}


@router.get(
    "/transport-company/trips/{trip_id}",
    dependencies=[Depends(require_roles(TRANSPORT_COMPANY_ROLES))],
)
async def get_transport_company_trip(
    trip_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(TRANSPORT_COMPANY_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_company_owns_trip(trip, current_user)
    return _transport_trip_summary(db, trip)


@router.post(
    "/trips/{trip_id}/assign-driver",
    dependencies=[Depends(require_roles(OPS_ADMIN_ROLES))],
)
async def assign_trip_driver(
    trip_id: UUID,
    payload: DriverAssignRequest,
    db: Session = Depends(get_db),
):
    trip = _trip_or_404(db, trip_id)
    trip.driver_id = payload.driver_id
    trip.status = "assigned"
    db.commit()
    db.refresh(trip)
    return _driver_trip_summary(db, trip)


@router.post(
    "/driver/trips/{trip_id}/acknowledge",
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def acknowledge_driver_trip(
    trip_id: UUID,
    payload: TripAcknowledgeRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_driver_owns_trip(trip, current_user)
    trip.status = "acknowledged"
    _record_milestone(
        db,
        trip=trip,
        milestone_type="driver_acknowledged",
        idempotency_key=payload.idempotency_key,
        payload={"acknowledged_by": payload.acknowledged_by or str(current_user.id)},
    )
    db.commit()
    return _driver_trip_summary(db, trip)


@router.post(
    "/orders/{order_id}/quote",
    status_code=201,
    dependencies=[Depends(require_roles(OPS_ADMIN_ROLES))],
)
async def create_quote(order_id: UUID, db: Session = Depends(get_db)):
    order = _order_or_404(db, order_id)
    distance = float(order.estimated_distance_km or 0)
    weight = float(order.weight_kg or 0)
    base_amount = max(distance * 18, weight * 2)
    platform_fee = base_amount * 0.04
    gst_amount = base_amount * 0.12 + platform_fee * 0.18
    quote = QuoteRecord(
        order_id=order.id,
        base_amount=round(base_amount, 2),
        platform_fee=round(platform_fee, 2),
        gst_amount=round(gst_amount, 2),
        total_amount=round(base_amount + platform_fee + gst_amount, 2),
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return {
        "quote_id": str(quote.quote_id),
        "order_id": str(order.id),
        "status": quote.status,
        "currency": quote.currency,
        "base_amount": float(quote.base_amount),
        "platform_fee": float(quote.platform_fee),
        "gst_amount": float(quote.gst_amount),
        "total_amount": float(quote.total_amount),
    }


@router.get(
    "/orders/{order_id}/trip",
    dependencies=[Depends(require_roles(SUPPORT_READ_ROLES | DRIVER_TRIP_ROLES))],
)
async def get_order_trip(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(SUPPORT_READ_ROLES | DRIVER_TRIP_ROLES)),
):
    trip = db.query(Trip).filter(Trip.order_id == order_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    _assert_driver_owns_trip(trip, current_user)
    return {"trip_id": str(trip.trip_id), "order_id": str(trip.order_id), "vehicle_id": str(trip.vehicle_id), "status": trip.status}


@router.post(
    "/orders/{order_id}/payments/advance",
    status_code=201,
    dependencies=[Depends(require_roles(FINANCE_ADMIN_ROLES))],
)
async def record_advance_payment(order_id: UUID, payload: AdvancePaymentRequest, db: Session = Depends(get_db)):
    order = _order_or_404(db, order_id)
    existing = db.query(PaymentRecord).filter(PaymentRecord.idempotency_key == payload.idempotency_key).first()
    if existing:
        return {"payment_id": str(existing.payment_id), "status": existing.status, "payment_type": existing.payment_type}
    trip = db.query(Trip).filter(Trip.order_id == order.id).first()
    payment = PaymentRecord(
        order_id=order.id,
        trip_id=trip.trip_id if trip else None,
        payment_type="advance",
        amount=payload.amount,
        currency=payload.currency,
        provider_ref=payload.provider_ref,
        idempotency_key=payload.idempotency_key,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {"payment_id": str(payment.payment_id), "order_id": str(order.id), "status": payment.status, "payment_type": payment.payment_type}


@router.post(
    "/trips/{trip_id}/loading-photo",
    status_code=201,
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def upload_loading_photo(
    trip_id: UUID,
    payload: LoadingPhotoRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_driver_owns_trip(trip, current_user)
    document = TripDocument(
        order_id=trip.order_id,
        trip_id=trip.trip_id,
        document_type="loading_photo",
        document_url=payload.photo_url,
        verification_status="uploaded",
        payload={"uploaded_by": payload.uploaded_by},
    )
    db.add(document)
    milestone = _record_milestone(
        db,
        trip=trip,
        milestone_type="loading_photo_uploaded",
        idempotency_key=payload.idempotency_key,
        payload={"document_url": payload.photo_url},
    )
    db.commit()
    db.refresh(document)
    return {"document_id": str(document.document_id), "milestone_id": str(milestone.milestone_id), "status": document.verification_status}


@router.post(
    "/trips/{trip_id}/milestones",
    status_code=201,
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def update_trip_milestone(
    trip_id: UUID,
    payload: MilestoneRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_driver_owns_trip(trip, current_user)
    milestone = _record_milestone(
        db,
        trip=trip,
        milestone_type=payload.milestone_type,
        status=payload.status,
        payload=payload.payload,
        idempotency_key=payload.idempotency_key,
    )
    db.commit()
    db.refresh(milestone)
    return {"milestone_id": str(milestone.milestone_id), "milestone_type": milestone.milestone_type, "status": milestone.status}


@router.post(
    "/trips/{trip_id}/pod",
    status_code=201,
    dependencies=[Depends(require_roles(DRIVER_TRIP_ROLES))],
)
async def upload_pod(
    trip_id: UUID,
    payload: PODUploadRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(DRIVER_TRIP_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    _assert_driver_owns_trip(trip, current_user)
    document = TripDocument(
        order_id=trip.order_id,
        trip_id=trip.trip_id,
        document_type="pod",
        document_url=payload.pod_url,
        verification_status="uploaded",
        payload={"uploaded_by": payload.uploaded_by, "pod_exif": payload.pod_exif},
    )
    db.add(document)
    order = transition_order(
        db,
        order_id=trip.order_id,
        to_state=OrderStatus.DELIVERED_PENDING_SETTLEMENT.value,
        event="pod_scanned",
        payload={"pod_url": payload.pod_url, "consignee_otp": payload.consignee_otp, "pod_exif": payload.pod_exif},
        actor_role="DRIVER",
        idempotency_key=uuid4(),
        trace_id=f"pod-upload:{trip.trip_id}",
        reason="POD uploaded from trip flow",
    )
    _record_milestone(
        db,
        trip=trip,
        milestone_type="pod_uploaded",
        idempotency_key=payload.idempotency_key,
        payload={"document_url": payload.pod_url},
    )
    db.commit()
    db.refresh(document)
    return {"document_id": str(document.document_id), "order_state": order.current_state.value, "status": document.verification_status}


@router.post(
    "/trips/{trip_id}/pod/verify",
    dependencies=[Depends(require_roles(VERIFICATION_ROLES))],
)
async def verify_pod(
    trip_id: UUID,
    payload: PODVerifyRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(VERIFICATION_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    document = (
        db.query(TripDocument)
        .filter(TripDocument.trip_id == trip.trip_id, TripDocument.document_type == "pod")
        .order_by(TripDocument.uploaded_at.desc())
        .first()
    )
    if not document:
        raise HTTPException(status_code=409, detail="POD must be uploaded before verification")
    document.verification_status = "verified"
    document.verified_at = datetime.now(timezone.utc)
    _record_milestone(db, trip=trip, milestone_type="pod_verified", idempotency_key=payload.idempotency_key, payload={"verified_by": payload.verified_by})
    db.commit()
    return {"document_id": str(document.document_id), "verification_status": document.verification_status}


@router.post(
    "/trips/{trip_id}/otp/verify",
    dependencies=[Depends(require_roles(VERIFICATION_ROLES))],
)
async def verify_otp(
    trip_id: UUID,
    payload: OTPVerifyRequest,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(VERIFICATION_ROLES)),
):
    trip = _trip_or_404(db, trip_id)
    trip.otp_verified = "true"
    _record_milestone(db, trip=trip, milestone_type="otp_verified", idempotency_key=payload.idempotency_key, payload={"verified_by": payload.verified_by})
    db.commit()
    return {"trip_id": str(trip.trip_id), "otp_verified": True}


@router.post(
    "/trips/{trip_id}/settlements/release",
    status_code=201,
    dependencies=[Depends(require_roles(FINANCE_ADMIN_ROLES))],
)
async def release_settlement(trip_id: UUID, payload: SettlementReleaseRequest, db: Session = Depends(get_db)):
    trip = _trip_or_404(db, trip_id)
    active_hold = db.query(FraudHold).filter(FraudHold.order_id == trip.order_id, FraudHold.is_active == True).first()
    if active_hold:
        raise HTTPException(status_code=409, detail="Active fraud hold requires supervisor clearance")
    pod = (
        db.query(TripDocument)
        .filter(
            TripDocument.trip_id == trip.trip_id,
            TripDocument.document_type == "pod",
            TripDocument.verification_status == "verified",
        )
        .first()
    )
    if not pod or trip.otp_verified != "true":
        raise HTTPException(status_code=409, detail="POD and OTP must be verified before settlement release")

    existing = db.query(SettlementRecord).filter(SettlementRecord.idempotency_key == payload.idempotency_key).first()
    if existing:
        return {"settlement_id": str(existing.settlement_id), "status": existing.status}

    settlement = SettlementRecord(
        order_id=trip.order_id,
        trip_id=trip.trip_id,
        amount=payload.amount,
        currency=payload.currency,
        idempotency_key=payload.idempotency_key,
    )
    db.add(settlement)
    db.flush()

    journal = JournalEntry(
        order_id=trip.order_id,
        settlement_id=settlement.settlement_id,
        debit_ledger="Customer Advance / Freight Collection Liability",
        credit_ledger="Driver / Vehicle Owner Payable",
        amount=payload.driver_payable_amount,
        currency=payload.currency,
        idempotency_key=f"journal:{payload.idempotency_key}",
    )
    invoice = GSTInvoiceRecord(
        order_id=trip.order_id,
        settlement_id=settlement.settlement_id,
        invoice_number=f"GST-{str(settlement.settlement_id)[:8].upper()}",
        taxable_amount=payload.commission_amount,
        gst_amount=payload.gst_amount,
        total_amount=payload.commission_amount + payload.gst_amount,
    )
    db.add_all([journal, invoice])
    transition_order(
        db,
        order_id=trip.order_id,
        to_state=OrderStatus.COMPLETED.value,
        event="payment_captured",
        payload={"payment_id": str(settlement.settlement_id), "amount": payload.amount, "currency": payload.currency},
        actor_role="FIN",
        idempotency_key=uuid4(),
        trace_id=f"settlement-release:{settlement.settlement_id}",
        reason="Settlement released after POD and OTP verification",
    )
    db.commit()
    return {
        "settlement_id": str(settlement.settlement_id),
        "status": settlement.status,
        "journal_entry_id": str(journal.journal_entry_id),
        "gst_invoice_id": str(invoice.invoice_id),
        "invoice_number": invoice.invoice_number,
    }
