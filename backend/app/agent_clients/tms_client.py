"""Transport Management Agent client example."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from app.agent_clients.base import TransitionClient, TransitionResult


class TransportManagementAgentClient:
    """Monitors telemetry and routes anomalies through the transition API."""

    def __init__(self, transition_client: TransitionClient) -> None:
        self.transition_client = transition_client

    def report_incident_from_telemetry(
        self,
        *,
        order_id: UUID,
        telemetry_ping: dict[str, Any],
        eta_minutes: int,
        trace_id: str,
    ) -> TransitionResult | None:
        speed_kmph = float(telemetry_ping.get("speed_kmph", 0))
        idle_minutes = int(telemetry_ping.get("idle_minutes", 0))
        route_deviation_km = float(telemetry_ping.get("route_deviation_km", 0))

        if speed_kmph > 95:
            incident_type = "speed_anomaly"
            severity = "high"
        elif idle_minutes > 45:
            incident_type = "prolonged_stop"
            severity = "medium"
        elif route_deviation_km > 10:
            incident_type = "route_deviation"
            severity = "high"
        else:
            return None

        payload = {
            "incident_type": incident_type,
            "severity": severity,
            "description": f"Telemetry anomaly detected; ETA={eta_minutes} minutes",
            "telemetry": telemetry_ping,
        }
        return self.transition_client.transition(
            order_id=order_id,
            to_state="INCIDENT",
            event="incident_detected",
            payload=payload,
            actor_role="TMS",
            actor_id="tms-agent",
            idempotency_key=uuid4(),
            trace_id=trace_id,
        )

