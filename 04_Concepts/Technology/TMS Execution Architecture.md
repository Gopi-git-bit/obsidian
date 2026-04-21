---
type: concept
domain: technology
decision_value: high
status: verified
related_hubs:
  - Technology Stack Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - concept
  - tms
  - routing
  - telemetry
  - sla
  - event-driven
---

# TMS Execution Architecture

## Purpose

Define how the transportation-management layer executes routing, ETA, telemetry ingestion, deviation detection, and SLA monitoring without violating state-machine or agent-boundary rules.

## Component Boundaries

| Layer | Responsibility | Hard Constraint |
|------|----------------|-----------------|
| TMS | Route planning, ETA, GPS ingestion, SLA monitoring, deviation detection | Must not change order state, pricing, or assignment ownership |
| OMS | State transitions, notifications, lifecycle orchestration | Must not own live telemetry mutation |
| IMS | Vehicle and driver matching, reservation, loop discovery | Must not track live movement |
| Supervisor | Escalation, policy review, emergency override | Must not bypass state machine casually |

## Routing Hierarchy

| Priority | Engine | Use |
|---------|--------|-----|
| 1 | Valhalla | Default truck-aware routing and ETA baseline |
| 2 | OSRM | Static fallback matrix if Valhalla fails |
| 3 | Straight-line plus historical factor | Emergency heuristic estimate |
| 4 | Cached route | Fastest degraded response when upstream routing is unavailable |

## ETA Rules

- Compute deterministic base ETA from segment distance and historical speed.
- Apply bounded multipliers for traffic, weather, and load context.
- Clamp realtime ETA so it stays within approved lower and upper bounds of the base estimate.
- Treat ML as advisory refinement only where policy allows.

## GPS Ingestion Rules

- Accept pings only in movement-relevant lifecycle states.
- Reject low-quality telemetry, such as poor accuracy or impossible speed.
- Deduplicate by idempotency key or near-identical driver-timestamp pairs.
- Feed accepted telemetry into ETA refresh, silence detection, and deviation checks.

## SLA Monitoring Pattern

| Signal | Typical Threshold Use |
|--------|------------------------|
| Driver acceptance latency | Reassignment or wake-up workflow |
| Movement after acceptance | Ops intervention before full breach |
| ETA error p90 | Customer-update quality control |
| GPS silence | Fraud or signal-loss investigation |
| Route deviation | TMS alert and customer-update trigger |

## Event Pattern

- Use one canonical event envelope with `trace_id`, `order_id`, `event_type`, `payload`, `source`, `timestamp`, and `idempotency_key`.
- Send GPS, breach, assignment, and POD milestones through the same event discipline.
- Keep retries and DLQ handling explicit rather than hiding failures in local code paths.

## Observability Pattern

- Separate generic uptime metrics from transport-execution metrics.
- Keep GPS freshness, route deviation rate, ETA error, and SLA-breach rate visible on dedicated transport dashboards.
- Treat illegal transition success, audit failure, or hidden DLQ growth as control failures rather than normal noise.

## Related Notes

- [[Transportation Agent]]
- [[Unified Routing & Optimization Algorithm]]
- [[ETA Prediction Logic]]
- [[Logistics SLA]]
- [[Fallback & Resilience Architecture]]
- [[Operational Observability Architecture]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
- [[Fleet & Transport Hub]]
