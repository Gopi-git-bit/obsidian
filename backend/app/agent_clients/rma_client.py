"""Resource Management Agent client example."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from app.agent_clients.base import TransitionClient, TransitionResult


class ResourceManagementAgentClient:
    """Selects a candidate vehicle and requests canonical ASSIGNED state."""

    def __init__(self, transition_client: TransitionClient) -> None:
        self.transition_client = transition_client

    def reserve_and_assign_vehicle(
        self,
        *,
        order_id: UUID,
        candidate_vehicle_id: UUID,
        proximity_matrix: dict[str, Any],
        trace_id: str,
        lock_ttl_seconds: int = 300,
    ) -> TransitionResult:
        if lock_ttl_seconds <= 0:
            raise ValueError("lock_ttl_seconds must be positive")

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=lock_ttl_seconds)
        payload = {
            "vehicle_id": str(candidate_vehicle_id),
            "reservation_id": str(uuid4()),
            "expires_at": expires_at.isoformat(),
            "proximity_matrix": proximity_matrix,
            "optimistic_lock": {
                "strategy": "active_vehicle_unique_reservation",
                "ttl_seconds": lock_ttl_seconds,
            },
        }
        return self.transition_client.transition(
            order_id=order_id,
            to_state="ASSIGNED",
            event="vehicle_reserved",
            payload=payload,
            actor_role="TMS",
            actor_id="rma-agent",
            idempotency_key=uuid4(),
            trace_id=trace_id,
        )

