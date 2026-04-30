---
type: algorithm
domain: matching
decision_value: high
status: draft
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
  - Technology Stack Hub
tags:
  - ims
  - return-load
  - hub-and-spoke
  - backhaul
  - matching
---

# Hub-Aware Return Trip Matching

## Purpose

Enhance IMS return-trip matching with hub-and-spoke awareness while preserving the existing safety model: IMS suggests, OMS commits, FIN applies money, and order state is not mutated by matching.

Derived from [[IMS Hub-Aware Return Trip Matching Source]].

## Design Goals

| Goal | Implementation Rule |
|------|---------------------|
| hub-aligned matching | prefer return orders in the same hub, adjacent spoke, or aligned corridor |
| empty-leg reduction | score saved deadhead km from hub/spoke return flow |
| hub capacity awareness | penalize overloaded hubs with excessive pending returns |
| backward compatibility | fall back to radius-based search when no hub context exists |
| state-machine safety | only attach `loop_group_id` and hub metadata; no order-state mutation |
| collaboration awareness | search partner fleets only when an active collaboration agreement permits it |

## Algorithm Flow

```text
1. load completed order, vehicle, and driver
2. reject if order is not delivery-completed or vehicle/driver inactive
3. identify outbound hub from completed drop location and vehicle type
4. fetch compatible return candidates by time, vehicle fit, state, and loop availability
5. if hub exists, keep same-hub, adjacent-spoke, or fallback-radius candidates
6. if hub does not exist, use original radius-based behavior
7. score candidates with base return-load and hub-aware factors
8. reject if best score is below threshold
9. create loop group ID and hub metadata
10. write metadata/audit only; do not mutate order state
11. return advisory result to OMS and FIN
```

## Candidate Filters

Hard filters:

- completed order state must be delivery-completed
- vehicle and driver must be active
- candidate order state must be draft or payment-pending
- candidate must be unlooped
- candidate must match vehicle body and capacity requirements
- candidate pickup time must fall within the wait window
- partner return candidates require valid `collaboration_pool_id` and agreement scope

Hub filters:

```text
if outbound_hub exists:
  allow candidate when:
    candidate_hub == outbound_hub
    OR candidate_hub shares spoke zone with outbound_hub
    OR pickup is within fallback radius
else:
  allow candidate when pickup is within fallback radius
```

## Scoring Model

```text
score =
  distance_bonus
+ wait_window_bonus
+ vehicle_model_bonus
+ return_zone_bonus
+ same_hub_bonus
+ corridor_alignment_bonus
+ empty_leg_savings_bonus
+ underutilized_hub_bonus
- overloaded_hub_penalty
```

Recommended scoring shape:

| Component | Points |
|-----------|--------|
| distance bonus | up to 12 |
| wait window bonus | up to 54 |
| vehicle model match | 20 |
| return zone match | 15 |
| same hub | 25 |
| corridor hint | 15 |
| empty-leg savings | up to 20 |
| underutilized hub | 10 |
| overloaded hub penalty | -15 |

Threshold:

```text
if best_score < 40:
  return no match
```

## Corridor And Discount Rules

Corridor ID should be deterministic:

```text
{HUB_CODE}-{VEHICLE_TYPE}
```

or, where inter-hub context exists:

```text
{ORIGIN_HUB}-{DESTINATION_HUB}-{VEHICLE_TYPE}
```

The loop discount remains advisory:

```text
discount = min(floor(score * 0.5), 30)
discount += corridor_bonus
discount = min(discount, 40)
```

FIN should apply any real discount or commission adjustment only after the loop is accepted and settlement rules pass.

## Database Pattern

| Table | Constraint |
|-------|------------|
| hub_configs | read-mostly reference table; service radius between 50 and 300 km; vehicle type scoped |
| loop_hub_metadata | append-only; keyed by `loop_group_id`; stores hub IDs, corridor ID, and saved km |
| orders | index unlooped draft/payment-pending candidate orders for hub-aware search |

## Safety And Audit

- duplicate request returns existing loop result
- no write to `orders.state`
- loop metadata append-only
- audit event for every suggestion
- no financial side effects inside IMS
- no PII in hub metadata logs
- hub service outage falls back to radius mode
- partner-fleet search must obey [[Collaborative Logistics Network Framework]]

## Rollout

```text
Phase 1: shadow mode for 7 days
  compare hub-aware scoring with original return-load matching

Phase 2: canary for 5% of hub-corridor orders
  monitor empty-leg reduction, acceptance rate, and hub load balance

Phase 3: full enablement
  enable all hub-corridor orders while non-hub orders keep radius fallback
```

## Related Notes

- [[IMS Hub-Aware Return Trip Matching Source]]
- [[IMS Matching Engine]]
- [[Return Load Optimization]]
- [[Hub-and-Spoke Network Design Algorithm]]
- [[Return Load Economics]]
- [[Resource Management Agent]]
- [[Collaborative Logistics Network Framework]]
