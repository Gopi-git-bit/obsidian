"""Schemas for ASC 606 revenue recognition controls."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


PrincipalAgentStatus = Literal["AGENT", "PRINCIPAL"]
RevenuePresentation = Literal["NET_COMMISSION", "GROSS_FREIGHT"]


class PerformanceObligationEvidence(BaseModel):
    vehicle_assigned: bool
    trip_completed: bool
    pod_uploaded: bool
    pod_verified: bool
    otp_verified: bool
    cancellation_hold: bool = False
    fraud_hold: bool = False
    dispute_hold: bool = False
    claim_hold: bool = False
    completed_at: Optional[datetime] = None

    def is_complete(self) -> bool:
        return all(
            [
                self.vehicle_assigned,
                self.trip_completed,
                self.pod_uploaded,
                self.pod_verified,
                self.otp_verified,
            ]
        ) and not any(
            [
                self.cancellation_hold,
                self.fraud_hold,
                self.dispute_hold,
                self.claim_hold,
            ]
        )


class RevenueRecognitionRequest(BaseModel):
    order_id: UUID
    user_id: str = Field(..., min_length=1, max_length=120)
    invoice_generation_user_id: str = Field(..., min_length=1, max_length=120)
    invoice_approval_user_id: str = Field(..., min_length=1, max_length=120)
    principal_agent_status: PrincipalAgentStatus = "AGENT"
    revenue_presentation: RevenuePresentation = "NET_COMMISSION"
    gross_freight_amount: float = Field(..., ge=0)
    driver_payable_amount: float = Field(..., ge=0)
    commission_amount: float = Field(..., ge=0)
    platform_fee_amount: float = Field(default=0, ge=0)
    gst_amount: float = Field(default=0, ge=0)
    revenue_amount: Optional[float] = Field(default=None, ge=0)
    accounting_policy_version: str = Field(..., min_length=1, max_length=80)
    idempotency_key: str = Field(..., min_length=1, max_length=120)
    performance_obligation: PerformanceObligationEvidence

    @model_validator(mode="after")
    def validate_revenue_presentation(self):
        if self.principal_agent_status == "AGENT" and self.revenue_presentation != "NET_COMMISSION":
            raise ValueError("AGENT transactions must use NET_COMMISSION presentation")
        if self.principal_agent_status == "PRINCIPAL" and self.revenue_presentation != "GROSS_FREIGHT":
            raise ValueError("PRINCIPAL transactions must use GROSS_FREIGHT presentation")
        return self


class JournalLine(BaseModel):
    debit_ledger: Optional[str] = None
    credit_ledger: Optional[str] = None
    amount: float


class RevenueRecognitionResponse(BaseModel):
    order_id: UUID
    recognition_status: str
    recognized_at: datetime
    principal_agent_status: PrincipalAgentStatus
    revenue_presentation: RevenuePresentation
    revenue_amount: float
    gst_amount: float
    accounting_policy_version: str
    idempotency_key: str
    journal_lines: list[JournalLine]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
