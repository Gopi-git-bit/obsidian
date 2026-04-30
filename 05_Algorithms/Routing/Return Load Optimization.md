---
type: algorithm
domain: routing
decision_value: high
inputs:
  - outbound_route
  - nearby_return_orders
  - corridor_history
  - vehicle_capability
  - wait_time_tolerance
outputs:
  - backhaul_plan
  - deadhead_risk
  - return_confidence
  - pcr_result
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - algorithm
  - routing
  - backhaul
  - utilization
---

# Return Load Optimization

## Purpose

Reduce empty return miles by pairing completed outbound trips with feasible backhaul demand, reposition opportunities, or open-route continuations.

For hub-and-spoke networks, use [[Hub-Aware Return Trip Matching]] to add hub corridor, spoke adjacency, hub capacity, and empty-leg savings metadata to the return-load decision.

## Strategic Relevance

India-scale freight efficiency depends heavily on reducing empty running. Return-trip probability should feed allocation, pricing, corridor planning, and the 2050 roadmap goal of lowering unnecessary vehicular freight activity.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| outbound_route | Object | Completed or near-complete primary movement |
| nearby_return_orders | Array | Candidate loads near destination or along return corridor |
| corridor_history | Object | Historic reload density, wait time, and success rate by lane |
| vehicle_capability | Object | Body type, tonnage, certifications, restrictions |
| wait_time_tolerance | Number | Maximum reload wait before margin deteriorates |

## Logic

```text
1. IDENTIFY feasible backhaul candidates near delivery point and return corridor
2. FILTER by vehicle compatibility, timing window, and service commitments
3. SCORE each candidate by reload proximity, margin recovery, wait time, and reliability
4. ESTIMATE return_confidence using corridor history and current nearby demand
5. IF multiple vehicles and loads interact, use stable matching or open-route VRP logic
6. CHOOSE best loaded return when confidence beats empty reposition baseline
7. OTHERWISE reposition to the next best demand pocket or accept priced deadhead
```

## Commercial Gate

Use a profitability gate before surfacing return-trip campaigns:

```text
PCR = backhaul_revenue / (detour_cost + return_cost)
Only promote return-trip options when PCR clears the configured threshold.
```

## Scoring Factors

| Factor | Weight | Purpose |
|--------|--------|---------|
| Reload proximity | 0.30 | Reduce unproductive empty distance |
| Margin recovery | 0.25 | Improve trip-level economics |
| Wait time fit | 0.20 | Avoid excessive dwell after delivery |
| Compatibility | 0.15 | Ensure vehicle-body and cargo fit |
| Partner reliability | 0.10 | Reduce return-leg execution risk |

## Hub-Aware Extension

When a completed delivery is inside an active hub/spoke service radius, return-load scoring should add:

| Factor | Purpose |
|--------|---------|
| same hub | prefer returns that keep vehicle flow inside the same hub network |
| adjacent spoke | support hub-to-spoke-to-hub cycles without excessive deadhead |
| corridor alignment | favor known profitable corridors and vehicle-type patterns |
| hub capacity | avoid overloading hubs with too many pending returns |
| empty-leg saved km | quantify operational savings for OMS/FIN and network analytics |

If hub context is unavailable, matching should fall back to the original radius-based search.

## Decision Rules

- Prefer loaded returns on long-haul lanes where empty running is materially expensive.
- Use open-route logic when returning to depot is not economically justified.
- Cap dwell time when reload confidence is weak or customer SLA risk rises.
- Feed high deadhead risk into [[Dynamic Pricing Logic]] and [[Fleet Allocation Algorithm]].
- Do not convert suggestions into committed return orders without explicit acceptance and loop binding.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No nearby reload | Reposition to strongest demand node or accept priced deadhead |
| Return load conflicts with next committed job | Preserve committed service unless backhaul value clearly outweighs it |
| Low confidence on corridor | Use manual review and keep alternates |
| PCR below threshold | Suppress outbound marketing and keep insight internal |

## Related Notes

- [[Return Load Economics]]
- [[Route Optimization Logic]]
- [[Hub-Aware Return Trip Matching]]
- [[Hub-and-Spoke Network Design Algorithm]]
- [[Unified Routing & Optimization Algorithm]]
- [[Load Matching Algorithm]]
- [[Fleet Utilization]]
- [[Scenario - Excess Capacity from Partner]]
- [[India Freight 2050 Strategic Roadmap]]
- [[Autonomous Logistics Execution Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
