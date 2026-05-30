"""Order Management Agent client example."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from app.agent_clients.base import TransitionClient, TransitionResult


class OrderManagementAgentClient:
    """Consumes order submission context and asks core to confirm the order."""

    def __init__(self, transition_client: TransitionClient) -> None:
        self.transition_client = transition_client

    def confirm_submitted_order(
        self,
        *,
        order_id: UUID,
        order_context: dict[str, Any],
        trace_id: str,
    ) -> TransitionResult:
        required = {"payment_mode", "material_type", "body_type_required"}
        missing = required.difference(order_context)
        if missing:
            raise ValueError(f"Missing OMS order context fields: {sorted(missing)}")

        payload = {
            "payment_mode": order_context["payment_mode"],
            "topay_consent_status": order_context.get(
                "topay_consent_status", "not_required"
            ),
            "material_type": order_context["material_type"],
            "body_type_required": order_context["body_type_required"],
        }
        return self.transition_client.transition(
            order_id=order_id,
            to_state="CONFIRMED",
            event="order_submitted",
            payload=payload,
            actor_role="OMS",
            actor_id="oms-agent",
            idempotency_key=uuid4(),
            trace_id=trace_id,
        )

