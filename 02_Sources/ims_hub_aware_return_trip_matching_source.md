---
type: source
domain: matching
status: extracted
origin: user_provided
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
  - Technology Stack Hub
---

# IMS Hub-Aware Return Trip Matching Source

## Source Scope

This source note extracts the user-provided IMS Agent update for hub-aware return-trip matching.

The update extends return-load matching with hub-and-spoke network context while preserving existing IMS safety rules: idempotency, no order-state mutation, audit logging, metadata-only loop binding, and downstream FIN ownership of discounts and settlement.

## Core Thesis

Hub-aware return matching improves empty-leg reduction when network topology provides a useful signal, while non-hub orders should continue to use the existing radius-based fallback.

```text
completed delivery
-> identify outbound hub
-> fetch compatible return candidates
-> score by distance, wait time, vehicle fit, hub alignment, corridor, savings, and hub capacity
-> tag loop metadata only
-> OMS/FIN decide acceptance, notification, discount, and settlement
```

## Data Contracts

| Object | Purpose |
|--------|---------|
| HubConfig | hub ID, location, vehicle-specific service radius, spoke zones, and pending-return capacity guardrail |
| HubAwareReturnTripRequest | completed order, vehicle, driver, optional search radius/wait, optional OMS hub hint |
| HubAwareReturnTripResult | matched return order, confidence, reason, pricing adjustment suggestion, loop group ID, hub metadata |
| hub_metadata | outbound hub, return hub, corridor ID, and empty-leg saved km |

## Candidate Logic

| Case | Candidate Filter |
|------|------------------|
| hub exists | same hub, adjacent spoke, or within fallback radius |
| no hub exists | original radius-based search |
| already looped order | excluded |
| incompatible vehicle | excluded |
| outside wait window | excluded |

## Scoring Logic

| Score Component | Meaning |
|-----------------|---------|
| reload distance | shorter deadhead from completed drop to return pickup scores higher |
| wait time | shorter acceptable wait after delivery scores higher |
| vehicle model/body fit | exact fit gets bonus |
| return-to-origin zone | drop zone matching original pickup zone gets bonus |
| same hub | strongest hub alignment bonus |
| corridor hint | corridor match gets additional bonus |
| empty-leg saved km | larger savings improves score with cap |
| hub capacity | underutilized hub gets bonus; overloaded pending returns get penalty |

Threshold:

```text
if hub_aware_score < 40:
  no match
```

## Safety Guarantees

- Duplicate loop requests should return the prior result.
- IMS must not mutate order state.
- `loop_group_id` and hub metadata are advisory binding metadata.
- Discount is suggested but applied later by FIN only after acceptance.
- Hub config outage must degrade to radius mode.
- Audit logs must include hub context without PII.
- Loop hub metadata should be append-only.

## Rollout Strategy

| Phase | Goal | Guardrail |
|-------|------|-----------|
| Shadow mode | compare hub-aware scoring against original algorithm | require explainable deltas |
| Canary | enable small share of hub-corridor orders | rollback if acceptance drops materially |
| Full enablement | all hub-corridor orders eligible | weekly corridor performance reviews |

## Derived Notes

- [[Hub-Aware Return Trip Matching]]
- [[IMS Matching Engine]]
- [[Return Load Optimization]]
- [[Hub-and-Spoke Network Design Algorithm]]
- [[Resource Management Agent]]
