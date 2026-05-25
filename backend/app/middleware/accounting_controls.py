"""GAAP/COSO accounting control validators."""

from __future__ import annotations

from fastapi import HTTPException, status


INVOICE_GENERATION = "invoice_generation"
INVOICE_APPROVAL = "invoice_approval"


class SegregationOfDutiesValidator:
    """Enforces maker-checker separation for accounting actions."""

    @staticmethod
    def validate_invoice_generation_approval(
        *,
        user_id: str,
        invoice_generation_user_id: str,
        invoice_approval_user_id: str,
    ) -> None:
        normalized_requester = user_id.strip()
        generator = invoice_generation_user_id.strip()
        approver = invoice_approval_user_id.strip()

        if not normalized_requester:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="user_id is required for audit attribution",
            )

        if generator == approver:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Segregation of duties violation: invoice_generation and "
                    "invoice_approval cannot be performed by the same user"
                ),
            )

        if normalized_requester == generator and normalized_requester == approver:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Segregation of duties violation: requester attempted both invoice controls",
            )


def validate_no_gross_revenue_under_agent_model(
    *,
    principal_agent_status: str,
    revenue_amount: float,
    commission_amount: float,
    platform_fee_amount: float,
) -> None:
    if principal_agent_status.upper() != "AGENT":
        return

    allowed_revenue = commission_amount + platform_fee_amount
    if revenue_amount > allowed_revenue:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Gross freight cannot be recognized as Zippy revenue under agent model",
        )
