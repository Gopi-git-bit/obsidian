---
type: algorithm_operating_spec
domain: backhaul
scope: return_trip_v1
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Algorithms Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[AI Agents Hub]]"
tags:
  - return-trip
  - backhaul
  - ims
  - oms
  - finance
  - deterministic
  - zippy-logistics
source_files:
  - "C:\\Users\\user\\Downloads\\new -chatgpt .txt"
---

# Return Trip Streamlined Operations v1

## Purpose

This note extracts the useful return-trip operating logic from `new -chatgpt .txt` and aligns it with the current Zippy architecture.

The source contains many implementation claims. The durable operational idea is:

```text
return-trip matching should start as deterministic, metadata-only, auditable, and safe
```

This note should guide the first production version of return-trip operations.

## Core Principle

Return-trip logic must not violate the order state machine.

Rules:

- IMS may suggest a return-trip candidate.
- OMS validates and offers it.
- Actor accepts or rejects explicitly.
- Loop identity is metadata, not a lifecycle state.
- Finance uses loop metadata only as calculation context.
- Settlements remain per order.
- Disputes and refunds remain scoped to the affected order or leg.

Short version:

```text
suggest
-> validate
-> offer
-> accept
-> bind metadata
-> execute normal workflow
-> settle loop-aware, not merged
```

## v1 Return-Trip Flow

```text
outbound delivery completed
-> IMS searches nearby compatible open orders
-> IMS returns suggestion only
-> OMS validates eligibility
-> OMS creates return-trip offer
-> eligible actor accepts or rejects
-> OMS binds loop_group_id metadata
-> return order continues through normal lifecycle
-> FIN calculates settlement with loop context
-> analytics measures avoided empty km and conversion
```

## IMS Return-Trip Suggestion

IMS v1 should be a deterministic decision function.

It should:

- read completed outbound order
- read vehicle and driver
- search nearby open orders
- filter by vehicle compatibility
- filter by pickup window
- score candidates by distance, wait time, vehicle fit, and corridor fit
- return an explainable suggestion

It should not:

- mutate order state
- assign the return order
- confirm payment
- create settlement records
- override OMS policy

Recommended v1 inputs:

| Input | Use |
|---|---|
| completed order ID | identify outbound delivery |
| vehicle ID | ensure continuity |
| driver ID | ensure continuity |
| max search radius | limit pickup distance |
| max wait minutes | limit driver waiting |

Recommended default configuration:

| Setting | v1 Default |
|---|---:|
| max search radius | 30 km |
| max wait window | 180 minutes |
| minimum score threshold | 40 |
| offer TTL | 15-30 minutes |

These should become configurable policy values, not scattered constants.

## IMS Candidate Rules

Reject candidate if:

- candidate is the same as the completed order
- candidate already has a loop group
- pickup is outside search radius
- pickup time is outside waiting window
- vehicle type/body/capacity is incompatible
- driver or vehicle is inactive
- candidate order state is not eligible

Preferred candidate features:

- closer pickup to completed drop
- shorter wait time
- exact vehicle model match
- return direction supports prior origin/corridor
- expected route economics improve loaded km ratio

## OMS Return-Trip Offer

OMS treats IMS output as a proposal, not a decision.

OMS should create a return-trip offer record only after re-validating eligibility.

Offer fields:

| Field | Purpose |
|---|---|
| offer ID | unique proposal |
| outbound order ID | completed leg |
| return order ID | candidate leg |
| loop group ID | shared loop metadata |
| discount percentage | commercial adjustment |
| status | pending, accepted, rejected, expired |
| expires at | offer TTL |
| accepted by | actor metadata |
| idempotency key | safe retries |

OMS must not change order state when creating the offer.

## OMS Eligibility Checks

Before showing an offer:

| Check | Rule |
|---|---|
| outbound order | must be delivered/completed enough for return search |
| return order | must be unassigned and eligible for matching |
| payment risk | no blocking payment or ToPay issue on outbound |
| vehicle continuity | same vehicle must be feasible |
| driver continuity | same driver must be feasible |
| time window | pickup within allowed window |
| customer or provider eligibility | actor must be allowed to accept |
| duplicate offer | no active offer for same pair |

If any check fails, OMS should drop the offer without disturbing the workflow.

## Acceptance Routing

Who sees the offer depends on provider context.

| Actor Context | UI Surface | Meaning |
|---|---|---|
| owner-driver | driver app | driver accepts or rejects return work |
| transport company | TC app / ops panel | authorized dispatcher accepts |
| customer-controlled return order | customer app or ops-assisted flow | customer accepts before driver sees active return leg |

Acceptance should call one backend endpoint or service action with:

- offer ID
- actor type
- actor ID
- idempotency key

## Acceptance Effects

On acceptance:

- offer becomes accepted
- outbound and return orders receive the same `loop_group_id`
- return order is marked as return leg metadata where applicable
- event is emitted
- normal lifecycle continues

Acceptance must not:

- auto-confirm payment
- auto-close outbound settlement
- auto-assign beyond approved workflow
- merge settlements into one order
- bypass document or SLA checks

## Rejection And Expiry

On rejection:

- offer becomes rejected
- no loop metadata is written
- vehicle can continue normal availability flow
- rejection reason should be captured when possible

On expiry:

- offer becomes expired
- no side effects
- expiry contributes to analytics

## Data Model Requirements

Minimum table:

```text
return_trip_offers
```

Minimum order metadata:

```text
orders.loop_group_id
orders.is_return_leg
```

Constraints:

- prevent duplicate pending offers for same outbound/return order pair
- index status
- index expiry
- index loop group
- index outbound and return order references

Do not add DB triggers that mutate order states or settlement states.

## Finance Rules

Finance should be loop-aware, not merged.

Principles:

- each order keeps its own invoice and settlement record
- loop group is calculation context
- return-leg discount applies only where policy allows
- provider payout can be grouped operationally, but ledger entries remain traceable per order
- if return leg fails, discount reversal or refund is scoped by policy
- ToPay or payment blocker on one leg should not silently corrupt the other leg

Finance flow:

```text
both legs delivered
-> settlement preprocessing per order
-> loop context applied
-> holds checked
-> disbursement approved
-> reconciliation
-> settlement close
```

## Dispute And Refund Rules

Looped orders create extra risk because one commercial loop contains two operational legs.

Rules:

- disputes are scoped to the affected order/leg
- settlement hold can be loop-aware but should remain specific
- AI may score dispute severity but cannot issue refund
- refund suggestions require evidence and admin/finance approval
- no refund state should be stored in the order lifecycle state

Common scenarios:

| Scenario | Handling |
|---|---|
| return leg cancelled before pickup | return leg cancelled; outbound settlement normal unless discount policy says otherwise |
| return leg delayed | partial dispute/refund logic on return leg |
| outbound dispute after loop accepted | hold affected settlement; keep return leg separate unless linked risk exists |
| discount applied but return fails | evaluate discount reversal |
| ToPay return unpaid | settlement hold on affected leg/provider payout |

## SLA To Dispute Trigger

The source proposes automated SLA breach detection. Keep the safe part:

- SLA breach can create dispute/review record
- SLA breach can place settlement on hold if policy allows
- SLA breach should not automatically refund money
- SLA breach should not mutate order state directly

Useful auto-generated KPIs:

- SLA breach count
- breach by lane
- breach by driver/provider
- dispute conversion rate
- refund suggestion acceptance
- settlement hold days

## Return-Trip KPIs

Track:

| KPI | Meaning |
|---|---|
| return-trip offer count | how many opportunities generated |
| acceptance/conversion rate | accepted offers divided by generated offers |
| expiry rate | timing or UX issue |
| rejection reason mix | why actors decline |
| empty km avoided | core efficiency value |
| loaded km ratio improvement | utilization improvement |
| average wait before return pickup | driver time cost |
| loop gross margin | commercial quality |
| discount reversal rate | policy or execution issue |
| settlement efficiency per loop | finance discipline |

Interpretation:

| Conversion | Meaning |
|---:|---|
| below 10% | poor timing, poor pricing, weak candidate quality |
| 15-25% | healthy early corridor signal |
| above 30% | strong corridor fit |

## Dashboard Views

Ops dashboard:

- pending return offers
- expiring offers
- accepted loops
- rejected loops
- average wait time
- active return legs

Finance dashboard:

- loop settlement holds
- discount applied
- discount reversed
- payout readiness
- dispute/refund impact

Executive dashboard:

- empty km avoided
- savings estimate
- conversion rate
- top corridors
- return-trip margin

## v1 Before v2

Launch v1 deterministic before advanced optimization.

Do not jump immediately to VRP/ACO/ML unless real data proves the deterministic approach is limiting operations.

Use v1 because it is:

- fast
- explainable
- auditable
- easy to debug
- stable under low data
- safer for driver and customer trust

Use v2 later when:

- volume is high enough for batch optimization
- v1 causes obvious suboptimal assignments
- drivers reject v1 offers because better options exist
- corridor-level data exists
- ops can explain and monitor the optimizer

## Future Optimization Path

Recommended order:

```text
v1 deterministic scoring
-> geohash/spatial index performance improvement
-> A/B test optimized candidate filtering
-> batch assignment for high-volume lanes
-> OR-Tools / VRP for fleet-wide optimization
-> ML acceptance and ETA models
```

Do not skip the measurement layer.

## Bottom Line

Return-trip operations should become a safe loop:

```text
IMS suggests
OMS governs
actor accepts
metadata links
normal workflow executes
FIN settles with context
analytics learns
```

That is the streamlined return-trip operating model for v1.

