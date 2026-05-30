"""Supervisor Agent policy evaluation client example."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from app.agent_clients.base import TransitionClient, TransitionResult


class SupervisorAgentClient:
    """Evaluates policy and emits allow/hold requests without DB mutation."""

    def __init__(self, transition_client: TransitionClient) -> None:
        self.transition_client = transition_client

    def evaluate_policy_request(
        self,
        *,
        order_id: UUID,
        requested_state: str,
        policy_context: dict[str, Any],
        trace_id: str,
    ) -> TransitionResult:
        fraud_score = float(policy_context.get("fraud_score", 0))
        payment_amount = float(policy_context.get("payment_amount", 0))
        policies_hit: list[str] = []

        if fraud_score >= 0.75:
            policies_hit.append("fraud_score_high")
        if payment_amount >= 500000:
            policies_hit.append("large_disbursement_review")

        decision = "hold" if policies_hit else "allow"
        payload = {
            "decision": decision,
            "decision_reason": "Policy hold required" if policies_hit else "Policy clear",
            "policies_hit": policies_hit,
        }
        target_state = "SUSPENDED" if decision == "hold" else requested_state
        return self.transition_client.transition(
            order_id=order_id,
            to_state=target_state,
            event="supervisor_policy_result",
            payload=payload,
            actor_role="SUP",
            actor_id="sup-agent",
            idempotency_key=uuid4(),
            trace_id=trace_id,
        )
