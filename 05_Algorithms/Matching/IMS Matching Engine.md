---
type: algorithm
domain: matching
decision_value: high
inputs:
  - order_request
  - inventory_snapshot
  - idempotency_key
  - route_context
  - compliance_status
outputs:
  - candidate_vehicles
  - reservation_results
  - fallback_path
  - matching_events
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - algorithm
  - matching
  - ims
  - reservation
---

# IMS Matching Engine

## Purpose

Generate vehicle candidates for OMS by applying compliance-safe hard filters, deterministic scoring, loop-aware ranking, and atomic reservation without mutating order state.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| order_request | Object | Pickup, load, body, urgency, and serviceability needs |
| inventory_snapshot | Array | Available vehicles and current capacity context |
| idempotency_key | String | Replay-safe identifier for the matching request |
| route_context | Object | Corridor, ETA, RDS category, and geography signals |
| compliance_status | Object | Fitness, insurance, and KYC eligibility data |

## Hard Guardrails

- IMS must not write to `orders.state`.
- IMS emits candidate or exhaustion events rather than committing assignments.
- Compliance failures are hard stops, not soft penalties.
- Reservations are temporary locks, not assignments.
- Duplicate requests must remain replay-safe under the same idempotency key.

## Logic

```text
1. APPLY hard filters for active status, compliance validity, body fit, weight, and volume
2. IF no feasible vehicles remain, emit matching_exhausted or enter fallback ladder
3. CHECK deterministic cache and recent lane intelligence where available
4. SCORE feasible vehicles on proximity, driver quality, loop success, condition, and bounded RDS penalty
5. USE ML scoring only as advisory refinement when deterministic confidence is insufficient
6. ATTEMPT atomic reservations on top-ranked candidates with short TTL
7. ENRICH results with return-trip or loop metadata when economically useful
8. EMIT vehicle_candidates_found or matching_exhausted for OMS consumption
```

## Deterministic Fallback Ladder

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Search primary radius | Prefer nearest feasible inventory |
| 2 | Expand radius | Broaden internal fleet search |
| 3 | Query partner or TC pool | Fill capacity gap externally |
| 4 | Trigger RAG or broadcast fallback | Surface scarce demand to wider pool |
| 5 | Emit exhaustion event | Let OMS notify and escalate |

## Reservation Rules

- Reservation TTL should be short, explicit, and observable.
- Expired reservations must release automatically with no implied commitment.
- Reservations should block concurrent duplicate use of the same vehicle.
- OMS remains responsible for final assignment after reservation success.

## Loop and Return Logic

- Prefer candidates with strong loop-success history when all else is comparable.
- Emit `loop_group_id` or return-potential metadata as advisory context only.
- Keep discounting and settlement decisions downstream in OMS and FIN.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Reservation conflict | Try next ranked candidate and record conflict metric |
| Match confidence low | Expand search or fall back to deterministic escalation |
| Compliance record stale | Treat as ineligible until refreshed |
| Exhaustion after all steps | Emit explicit no-match event with attempted fallbacks |

## Related Notes

- [[Load Matching Algorithm]]
- [[Vehicle Assignment Logic]]
- [[Return Load Optimization]]
- [[Resource Management Agent]]
- [[Fallback & Resilience Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]

