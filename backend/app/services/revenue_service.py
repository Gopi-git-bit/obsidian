"""ASC 606 revenue recognition service."""

from __future__ import annotations

from fastapi import HTTPException, status

from app.middleware.accounting_controls import (
    SegregationOfDutiesValidator,
    validate_no_gross_revenue_under_agent_model,
)
from app.schemas.revenue import JournalLine, RevenueRecognitionRequest, utc_now


def recognize_revenue(payload: RevenueRecognitionRequest) -> dict:
    """Validate ASC 606 gates and return a controlled journal proposal."""
    SegregationOfDutiesValidator.validate_invoice_generation_approval(
        user_id=payload.user_id,
        invoice_generation_user_id=payload.invoice_generation_user_id,
        invoice_approval_user_id=payload.invoice_approval_user_id,
    )

    if not payload.performance_obligation.is_complete():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Revenue recognition blocked: performance obligation is incomplete "
                "or a cancellation/fraud/dispute/claim hold is active"
            ),
        )

    revenue_amount = payload.revenue_amount
    if revenue_amount is None:
        if payload.principal_agent_status == "AGENT":
            revenue_amount = payload.commission_amount + payload.platform_fee_amount
        else:
            revenue_amount = payload.gross_freight_amount

    validate_no_gross_revenue_under_agent_model(
        principal_agent_status=payload.principal_agent_status,
        revenue_amount=revenue_amount,
        commission_amount=payload.commission_amount,
        platform_fee_amount=payload.platform_fee_amount,
    )

    if payload.principal_agent_status == "AGENT":
        debit_amount = revenue_amount + payload.gst_amount
        journal_lines = [
            JournalLine(
                debit_ledger="Customer Advance / Freight Collection Liability",
                amount=debit_amount,
            ),
            JournalLine(credit_ledger="Commission / Platform Service Income", amount=revenue_amount),
        ]
        if payload.gst_amount:
            journal_lines.append(
                JournalLine(credit_ledger="Output GST - Commission / Platform Fee", amount=payload.gst_amount)
            )
    else:
        journal_lines = [
            JournalLine(debit_ledger="Customer Receivable / Customer Advance", amount=revenue_amount),
            JournalLine(credit_ledger="Freight Revenue", amount=revenue_amount),
        ]
        if payload.gst_amount:
            journal_lines.append(JournalLine(credit_ledger="Output GST - Freight", amount=payload.gst_amount))

    return {
        "order_id": payload.order_id,
        "recognition_status": "recognized",
        "recognized_at": utc_now(),
        "principal_agent_status": payload.principal_agent_status,
        "revenue_presentation": payload.revenue_presentation,
        "revenue_amount": revenue_amount,
        "gst_amount": payload.gst_amount,
        "accounting_policy_version": payload.accounting_policy_version,
        "idempotency_key": payload.idempotency_key,
        "journal_lines": journal_lines,
    }
