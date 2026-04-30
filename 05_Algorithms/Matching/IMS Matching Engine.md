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

This engine is also a strategic control point: it is where real-time demand visibility, structured supply data, and operational learning turn into faster and more reliable matching.

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

## Strategic Abstractions

### 1. IMS As The Seizing Layer

Within the project's competitive-advantage model, IMS is the system layer that converts sensed market demand into executable capacity options.

- sensing happens upstream through requests, availability signals, lane history, and partner behavior
- IMS seizes those signals by turning them into ranked, reservation-safe candidates
- OMS and downstream workflows decide commitment, communication, and settlement

### 2. Data Advantage Through Matching

The engine should not only consume data. It should improve future matching quality by producing reusable operational truth such as:

- candidate quality
- reservation conflicts
- search exhaustion frequency
- lane-level success patterns
- return-loop performance
- acceptance responsiveness by supply source
- future supply realization accuracy

These outputs create the learning loop that makes the matching system harder to imitate over time.

### 3. Matching Quality Over Match Volume

A weak marketplace can generate many candidate lists.

A strong IMS should optimize for:

- feasible matches
- fast matches
- economically sound matches
- replay-safe and auditable matches
- matches that improve future lane intelligence

### 4. Multi-Echelon Fleet View

IMS should treat vehicles as network inventory, not a flat list of available units.

- idle vehicles are current supply
- returning or enroute vehicles are future supply
- corridor clusters and nearby cities form lateral supply options
- low-demand destinations create downstream scarcity risk if no return path exists

This turns IMS from a local matcher into a network-aware supply intelligence layer.

### 5. Hub-Aware Return Trips

When hub-and-spoke topology exists, IMS should use [[Hub-Aware Return Trip Matching]] to enrich return-load suggestions with hub context.

- Prefer same-hub, adjacent-spoke, and corridor-aligned return orders.
- Preserve radius-based fallback for non-hub orders.
- Keep `loop_group_id`, corridor ID, outbound hub, return hub, and empty-leg saved km as advisory metadata.
- Do not mutate order state or apply financial discounts inside IMS.

### 6. Collaborative Pool Matching

When an order carries a `collaboration_pool_id`, IMS may search approved partner capacity under the agreement scope.

- Partner fleet access must be authorized by agreement ID and partner token.
- Sensitive customer/order data should follow the data-sharing level in [[Collaborative Logistics Network Framework]].
- IMS should emit partner candidate metadata, but OMS still commits assignment.
- Partner matching should be auditable by partner ID, agreement ID, and pool ID.

## Logic

```text
1. APPLY hard filters for active status, compliance validity, body fit, weight, and volume
2. IF no feasible vehicles remain, emit matching_exhausted or enter fallback ladder
3. CHECK deterministic cache and recent lane intelligence where available
4. CALCULATE future demand alignment for the destination and penalize dead-zone drops where return probability is weak
5. SCORE feasible vehicles on proximity, driver quality, loop success, condition, future demand alignment, and bounded RDS penalty
6. USE ML scoring only as advisory refinement when deterministic confidence is insufficient
7. ATTEMPT atomic reservations on top-ranked candidates with short TTL
8. ENRICH results with return-trip or loop metadata when economically useful
9. EMIT vehicle_candidates_found or matching_exhausted for OMS consumption
```

## Deterministic Fallback Ladder

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Search primary radius | Prefer nearest feasible inventory |
| 2 | Expand radius | Broaden internal fleet search |
| 3 | Query partner or TC pool | Fill capacity gap externally |
| 4 | Trigger RAG or broadcast fallback | Surface scarce demand to wider pool |
| 5 | Emit exhaustion event | Let OMS notify and escalate |

## Network-Aware Supply Model

Useful IMS supply should include more than currently idle vehicles:

```text
future_supply = idle + enroute_arrivals + returning_vehicles + predicted_reactivation
```

Where the platform has enough signal quality, IMS should keep this view by city or corridor cluster so matching and fallback can use nearby future capacity instead of treating every city as isolated.

## Rebalancing Trigger

IMS should not directly dispatch vehicles between cities, but it should emit rebalancing signals when local imbalance is persistent.

Example triggers:

- demand materially exceeds feasible supply in a target city or corridor
- nearby cities show surplus idle or returning capacity
- repeated exhaustion events indicate structural shortage, not one-off noise

Those signals can feed planning, partner outreach, or a downstream rebalancing service.

## Reservation Rules

- Reservation TTL should be short, explicit, and observable.
- Expired reservations must release automatically with no implied commitment.
- Reservations should block concurrent duplicate use of the same vehicle.
- OMS remains responsible for final assignment after reservation success.

## Technical Implications For Defensibility

- Persist matching events so lane intelligence and return-loop models can improve over time.
- Track supply responsiveness by vehicle, owner, and partner pool rather than only trip completion.
- Keep deterministic features queryable for audit, debugging, and model refinement.
- Add new external or predictive signals only when they measurably improve candidate quality or exhaustion rate.
- Protect ranking quality and reservation correctness because these are part of the platform moat, not just implementation detail.
- Model corridor clusters and future supply explicitly before adding more advanced ML or optimization layers.
- Keep any ML, OR, or RL layer advisory-first with clear fallback and constraint enforcement.

## Loop and Return Logic

- Prefer candidates with strong loop-success history when all else is comparable.
- Emit `loop_group_id` or return-potential metadata as advisory context only.
- Keep discounting and settlement decisions downstream in OMS and FIN.
- Penalize assignments into low-demand destinations when loop recovery is consistently weak.
- Use [[Hub-Aware Return Trip Matching]] when a completed delivery falls inside an active hub/spoke service radius.
- Hub-aware matching may score hub capacity, but it must not force a return through an overloaded hub.

## Driver And Corridor Intelligence

Where the data exists, IMS scoring can benefit from:

- route familiarity
- state permit compatibility
- regional or language fit when it affects execution reliability

These should remain bounded scoring features or eligibility checks, not opaque overrides.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Reservation conflict | Try next ranked candidate and record conflict metric |
| Match confidence low | Expand search or fall back to deterministic escalation |
| Compliance record stale | Treat as ineligible until refreshed |
| Exhaustion after all steps | Emit explicit no-match event with attempted fallbacks |

## Strategic Metrics

| Metric | Why It Matters |
|--------|----------------|
| matching lead-time | shows how quickly demand becomes candidate capacity |
| exhaustion rate | reveals supply gaps or poor visibility by lane |
| reservation conflict rate | exposes concurrency pressure and stale availability |
| candidate-to-assignment conversion | shows whether ranking quality is actually useful downstream |
| idle vehicle age before match | reflects how well IMS converts visible supply into revenue |
| loop-success contribution | shows whether matching is reducing empty-run leakage |
| future supply accuracy | shows whether predicted arrivals and returns are operationally useful |
| rebalance signal hit rate | shows whether scarcity signals correctly predict downstream shortages |

## Related Notes

- [[Load Matching Algorithm]]
- [[Vehicle Assignment Logic]]
- [[Return Load Optimization]]
- [[Hub-Aware Return Trip Matching]]
- [[Hub-and-Spoke Network Design Algorithm]]
- [[Collaborative Logistics Network Framework]]
- [[Resource Management Agent]]
- [[Fallback & Resilience Architecture]]
- [[Lane Intelligence Model]]
- [[Competitive Advantage Framework]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
