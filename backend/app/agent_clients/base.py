"""Shared HTTP client for agent-to-core state transition requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

import httpx


@dataclass(frozen=True)
class TransitionResult:
    order_id: UUID
    current_state: str
    trace_id: str
    raw: dict[str, Any]


class TransitionClient:
    """Small HTTP wrapper used by isolated worker agents."""

    def __init__(
        self,
        base_url: str,
        *,
        timeout_seconds: float = 10.0,
        api_prefix: str = "/api/v1",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.api_prefix = api_prefix.rstrip("/")

    def transition(
        self,
        *,
        order_id: UUID,
        to_state: str,
        event: str,
        payload: dict[str, Any],
        actor_role: str,
        trace_id: str,
        idempotency_key: UUID | None = None,
        actor_id: str | None = None,
    ) -> TransitionResult:
        """Call the backend state-machine gateway and return the canonical state."""

        request_body: dict[str, Any] = {
            "to_state": to_state,
            "event": event,
            "payload": payload,
            "actor_role": actor_role,
            "actor_id": actor_id,
            "idempotency_key": str(idempotency_key or uuid4()),
            "trace_id": trace_id,
        }
        url = f"{self.base_url}{self.api_prefix}/orders/{order_id}/transition"
        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(url, json=request_body)
            response.raise_for_status()
        data = response.json()
        return TransitionResult(
            order_id=UUID(data["id"]),
            current_state=data["current_state"],
            trace_id=trace_id,
            raw=data,
        )

