"""Finance settlement queue endpoints."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import FINANCE_ADMIN_ROLES, require_roles
from app.database import get_db
from app.models.flow_model import GSTInvoiceRecord, JournalEntry, SettlementRecord, Trip, TripDocument, TripMilestone
from app.models.order_model import Order
from app.models.outbox_model import EventOutbox
from app.models.supervisor_model import FraudHold, SettlementHold

router = APIRouter()


def _value(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _row(row, fields):
    return {field: _value(getattr(row, field)) for field in fields}


def _trip_or_404(db: Session, trip_id: UUID) -> Trip:
    trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


def _detail(db: Session, trip: Trip) -> dict:
    order = db.query(Order).filter(Order.id == trip.order_id).first()
    pod = (
        db.query(TripDocument)
        .filter(TripDocument.trip_id == trip.trip_id, TripDocument.document_type == "pod")
        .order_by(TripDocument.uploaded_at.desc())
        .first()
    )
    settlement = (
        db.query(SettlementRecord)
        .filter(SettlementRecord.trip_id == trip.trip_id)
        .order_by(SettlementRecord.released_at.desc())
        .first()
    )
    journal = (
        db.query(JournalEntry)
        .filter(JournalEntry.settlement_id == settlement.settlement_id)
        .order_by(JournalEntry.created_at.desc())
        .first()
        if settlement
        else None
    )
    gst_invoice = (
        db.query(GSTInvoiceRecord)
        .filter(GSTInvoiceRecord.settlement_id == settlement.settlement_id)
        .order_by(GSTInvoiceRecord.created_at.desc())
        .first()
        if settlement
        else None
    )
    fraud_holds = db.query(FraudHold).filter(FraudHold.order_id == trip.order_id).order_by(FraudHold.placed_at.desc()).all()
    settlement_hold_filters = [SettlementHold.order_id == trip.order_id, SettlementHold.trip_id == trip.trip_id]
    if settlement:
        settlement_hold_filters.append(SettlementHold.settlement_id == settlement.settlement_id)
    settlement_holds = db.query(SettlementHold).filter(or_(*settlement_hold_filters)).order_by(SettlementHold.placed_at.desc()).all()
    milestones = (
        db.query(TripMilestone)
        .filter(TripMilestone.trip_id == trip.trip_id)
        .order_by(TripMilestone.recorded_at.desc())
        .all()
    )
    outbox_ids = [trip.trip_id, trip.order_id]
    if settlement:
        outbox_ids.append(settlement.settlement_id)
    outbox_events = (
        db.query(EventOutbox)
        .filter(EventOutbox.aggregate_id.in_(outbox_ids))
        .order_by(EventOutbox.created_at.desc())
        .all()
    )

    pod_verified = bool(pod and pod.verification_status == "verified")
    otp_verified = trip.otp_verified == "true"
    active_fraud_hold = next((hold for hold in fraud_holds if hold.is_active), None)
    active_settlement_hold = next((hold for hold in settlement_holds if hold.is_active), None)
    release_status = settlement.status if settlement else "pending"
    blocker_code = None
    blocker_reason = None
    if settlement:
        release_eligible = False
    elif active_fraud_hold:
        release_eligible = False
        blocker_code = "FRAUD_HOLD_ACTIVE"
        blocker_reason = active_fraud_hold.reason
    elif active_settlement_hold:
        release_eligible = False
        blocker_code = "SETTLEMENT_HOLD_ACTIVE"
        blocker_reason = active_settlement_hold.reason
    elif not pod_verified:
        release_eligible = False
        blocker_code = "POD_NOT_VERIFIED"
        blocker_reason = "POD must be verified before settlement release"
    elif not otp_verified:
        release_eligible = False
        blocker_code = "OTP_NOT_VERIFIED"
        blocker_reason = "OTP must be verified before settlement release"
    else:
        release_eligible = True

    return {
        "trip_id": str(trip.trip_id),
        "order_id": str(trip.order_id),
        "customer_id": getattr(order, "customer_id", None) if order else None,
        "driver_id": trip.driver_id,
        "provider_id": trip.transport_company_id,
        "amount": float(settlement.amount) if settlement else float(getattr(order, "offered_price", 0) or 0),
        "currency": settlement.currency if settlement else "INR",
        "pod_status": pod.verification_status if pod else "missing",
        "pod_verified": pod_verified,
        "otp_verified": otp_verified,
        "fraud_hold_active": active_fraud_hold is not None,
        "settlement_hold_active": active_settlement_hold is not None,
        "release_status": release_status,
        "release_eligible": release_eligible,
        "blocker_code": blocker_code,
        "blocker_reason": blocker_reason,
        "settlement": _row(settlement, ("settlement_id", "order_id", "trip_id", "status", "amount", "currency", "released_at")) if settlement else None,
        "journal_created": journal is not None,
        "gst_invoice_created": gst_invoice is not None,
        "journal_id": str(journal.journal_entry_id) if journal else None,
        "gst_invoice_id": str(gst_invoice.invoice_id) if gst_invoice else None,
        "fraud_holds": [_row(hold, ("hold_id", "order_id", "reason", "is_active", "placed_by", "released_by", "placed_at", "released_at")) for hold in fraud_holds],
        "settlement_holds": [_row(hold, ("hold_id", "settlement_id", "order_id", "trip_id", "reason", "is_active", "placed_by", "released_by", "placed_at", "released_at")) for hold in settlement_holds],
        "audit_trail": [_row(milestone, ("milestone_id", "milestone_type", "status", "payload", "idempotency_key", "recorded_at")) for milestone in milestones],
        "outbox_events": [_row(event, ("event_id", "event_type", "aggregate_type", "aggregate_id", "recipient_role", "channel", "payload", "status", "attempts", "last_error", "created_at", "available_at", "dispatched_at")) for event in outbox_events],
    }


@router.get("/finance/settlements", dependencies=[Depends(require_roles(FINANCE_ADMIN_ROLES))])
async def list_finance_settlements(db: Session = Depends(get_db)):
    trips = db.query(Trip).order_by(Trip.updated_at.desc()).all()
    items = [_detail(db, trip) for trip in trips]
    return {"total": len(items), "settlements": items}


@router.get("/finance/settlements/{trip_id}", dependencies=[Depends(require_roles(FINANCE_ADMIN_ROLES))])
async def get_finance_settlement(trip_id: UUID, db: Session = Depends(get_db)):
    return _detail(db, _trip_or_404(db, trip_id))
