---
type: algorithm
domain: routing
decision_value: high
inputs:
  - order_request
  - idempotency_key
  - trace_id
  - vehicle_candidates
  - route_matrix
  - eta_context
  - rds_score
  - pickup_delivery_pairs
outputs:
  - candidate_routes
  - eta_windows
  - eta_confidence
  - loop_group_metadata
  - routing_trace
status: verified
related_hubs:
  - Algorithms Hub
  - Operations Strategy Hub
  - Technology Stack Hub
tags:
  - algorithm
  - routing
  - vrp
  - orchestration
  - idempotency
---

# Unified Routing & Optimization Algorithm

## Purpose

Coordinate routing, ETA prediction, backhaul discovery, and return-trip marketing while preserving strict separation between optimization output and order-state mutation.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| order_request | Object | Shipment, timing, and corridor requirements |
| idempotency_key | String | Replay-safe identifier for routing and matching work |
| trace_id | String | End-to-end observability token |
| vehicle_candidates | Array | IMS-filtered feasible vehicles |
| route_matrix | Object | Valhalla or fallback travel matrix |
| eta_context | Object | GPS, traffic, weather, and freshness inputs for ETA scoring |
| rds_score | Float | Route difficulty signal used only as bounded penalty |
| pickup_delivery_pairs | Array | Backhaul or paired movement constraints |

## Hard Guardrails

- Routing must not write directly to order state.
- Every output must include `trace_id`, `idempotency_key`, and `agent_code`.
- Return-trip suggestions remain metadata-only until explicit acceptance.
- SLA breaches may open disputes but must not auto-refund or auto-adjust fares.
- ML penalties may influence cost and ETA but may not override hard feasibility constraints.
- TMS should not reassign drivers or mutate pricing from routing workflows.

## Logic

```text
1. RUN deterministic gatekeeper on hard constraints
2. IF gatekeeper fails, send event to DLQ and raise supervisor alert
3. ASK IMS to pre-filter vehicles by capacity, compatibility, and corridor fit
4. CALL Valhalla for truck-aware matrix and ETA baseline
5. APPLY bounded RDS penalty to duration and route cost
6. CALCULATE confidence-scored ETA windows using [[ETA Prediction Logic]]
7. RUN OR-Tools VRP/PDP using adjusted matrix, capacities, and pickup-delivery pairs
8. GENERATE candidate routes and perform PCR check for return-trip opportunity
9. TAG loop metadata when return-leg linkage is commercially viable
10. RETURN suggestions to OMS for explicit transition handling
11. HAND OFF accepted routes to TMS for ETA monitoring and FIN for per-order settlement logic
```

## Recommended Stack Roles

| Component | Responsibility | Guardrail |
|-----------|----------------|-----------|
| OMS | Requests transitions after routing returns candidates | Owns state graph and `/transition` semantics |
| IMS | Filters capacity and binds loop metadata | No state mutation |
| TMS | Monitors ETA and SLA adherence | Breach creates dispute, not fare mutation |
| ETA layer | Produces confidence-scored arrival windows | Must degrade safely when live data is stale |
| FIN | Applies discounts and surcharges per order | Never merges looped orders into one settlement |
| Supervisor | Reviews failures and unsafe suggestions | Human or policy veto path |

## Key Decision Rules

- Clamp RDS penalties so they remain bounded and explainable.
- Keep fallback routing hierarchies explicit and ordered.
- Prefer Valhalla, then OSRM, then heuristic estimate, then cache for degraded routing.
- Require explicit acceptance before converting return-trip suggestions into operational commitments.
- Preserve per-order taxation, settlement, and reversibility even when loops are commercially linked.

## Operational Metrics

| Metric | Target Use |
|--------|------------|
| Routing latency p95 | Detect route-engine degradation |
| Empty-leg reduction | Measure backhaul program impact |
| ETA error p90 | Track route quality and SLA fit |
| ETA confidence calibration | Validate uncertainty quality |
| PCR compliance | Gate return-trip marketing quality |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Valhalla unavailable | Fall back to static matrix or heuristic estimate |
| Optimization timeout | Return best feasible route seen so far with degraded-confidence flag |
| Replay request | Use idempotency key to reject duplicate mutation attempts |
| Weak backhaul economics | Keep suggestion internal and do not market |
| GPS stream noisy or stale | Freeze confidence downward and escalate telemetry quality concern |

## Related Notes

- [[Route Optimization Logic]]
- [[Return Load Optimization]]
- [[ETA Prediction Logic]]
- [[TMS Execution Architecture]]
- [[Logistics SLA]]
- [[Order Lifecycle]]
- [[Hybrid Logistics Data Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Operations Strategy Hub]]
- [[Technology Stack Hub]]
