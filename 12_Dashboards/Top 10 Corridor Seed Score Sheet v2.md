---
type: dashboard-seed
domain: market-intelligence
scope: strategic
status: active
last_updated: 2026-05-11
related_hubs:
  - Market Intelligence Hub
tags:
  - dashboard
  - corridor-scoring
  - seed-data
  - strategic
  - v2
  - zippy-logistics
---

# Top 10 Corridor Seed Score Sheet v2

## Purpose

This note is the `v2` re-score pass for the top 10 corridors.

It upgrades the first-pass seed sheet by adding the strongest currently available validation inputs from the workspace:

- directed lane strength and backhaul signals
- triangle-route evidence
- sample corridor reliability data where available
- lane scorecard hints
- port and policy corridor signals
- empty-return and compatibility risk notes

## Important Honesty Rule

This is **not** a full live field-validation pass yet.

What it adds is:

- stronger proxy operational signals
- clearer confidence grading
- score adjustments grounded in existing vault evidence

What is still missing for a true field-validated v2:

- shipper interviews
- transporter interviews
- 10-14 day live rate capture
- reverse-lane posting counts
- real wait-time evidence

## Validation Inputs Used

| Validation Input | Source Type | Strength |
| --- | --- | --- |
| directed lane strength and backhaul | lane notes and master tables | strong |
| triangle-route viability | triangle route notes and masters | strong |
| corridor reliability snapshots | sample corridor and lane scorecards | medium |
| port and policy corridor priority | TN corridor and market-scan notes | medium |
| empty-return and compatibility risks | empty-return red-zone notes | medium |
| live field interviews | not yet available in vault | missing |

## v2 Rescored Corridors

| Lane ID | Total v1 | Total v2 | Delta | Confidence v2 | Hard Gate | Recommendation v2 | Why It Moved |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| tiruppur:chennai:garments | 74 | 76 | +2 | medium | no | validate manually | strong outbound lane plus strong triangle evidence, but reverse-rate validation still missing |
| chennai:tiruppur:textiles | 60 | 56 | -4 | low | no | build later | weak-return evidence is clearer than before; lane still useful mainly as triangle support leg |
| coimbatore:chennai:engineering | 73 | 75 | +2 | medium | no | validate manually | strong Chennai-bound industrial relevance and better support from broader corridor notes |
| chennai:coimbatore:mixed | 69 | 74 | +5 | medium | no | validate manually | strong directed-lane evidence plus corridor sample reliability support |
| erode:chennai:textiles | 70 | 73 | +3 | medium | no | validate manually | medium-strong lane and validated triangle pattern improve confidence |
| karur:chennai:home_textiles | 67 | 68 | +1 | medium | no | validate manually | export and home-textile relevance is real, but field density still thinner than Tiruppur or Coimbatore |
| namakkal:chennai:poultry_industrial | 64 | 61 | -3 | medium | no | build later | supply is strong, but vehicle hygiene and return-fit complexity weaken immediate lane attractiveness |
| hosur:chennai:auto_components | 77 | 80 | +3 | medium | no | launch now | high-priority policy corridor, strong industrial demand, and good service-premium potential |
| hosur:coimbatore:industrial | 72 | 75 | +3 | medium | no | validate manually | western industrial corridor logic strengthened, but still needs live benchmark capture |
| coimbatore:tuticorin_via_madurai:export | 66 | 68 | +2 | low | yes | validate manually | policy and export logic are strong, but port workflow and documentation complexity remain gating factors |

## v2 Detailed Scoring Table

| Lane ID | Demand | Supply | Backhaul | Pricing | Payment | Complexity | Proof | Competition | Total v2 | Confidence | Recommendation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| tiruppur:chennai:garments | 18 | 10 | 12 | 7 | 6 | 6 | 9 | 8 | 76 | medium | validate manually |
| chennai:tiruppur:textiles | 10 | 11 | 4 | 6 | 6 | 7 | 6 | 6 | 56 | low | build later |
| coimbatore:chennai:engineering | 17 | 11 | 10 | 7 | 7 | 7 | 8 | 8 | 75 | medium | validate manually |
| chennai:coimbatore:mixed | 15 | 11 | 10 | 7 | 7 | 7 | 7 | 10 | 74 | medium | validate manually |
| erode:chennai:textiles | 16 | 9 | 11 | 7 | 6 | 6 | 8 | 10 | 73 | medium | validate manually |
| karur:chennai:home_textiles | 14 | 8 | 10 | 7 | 6 | 6 | 8 | 9 | 68 | medium | validate manually |
| namakkal:chennai:poultry_industrial | 13 | 13 | 6 | 6 | 6 | 4 | 5 | 8 | 61 | medium | build later |
| hosur:chennai:auto_components | 17 | 11 | 10 | 8 | 7 | 8 | 8 | 11 | 80 | medium | launch now |
| hosur:coimbatore:industrial | 15 | 10 | 11 | 7 | 7 | 7 | 7 | 11 | 75 | medium | validate manually |
| coimbatore:tuticorin_via_madurai:export | 15 | 8 | 9 | 7 | 6 | 5 | 8 | 10 | 68 | low | validate manually |

## What Changed Strategically

### Stronger Than v1

- `hosur:chennai:auto_components`
- `chennai:coimbatore:mixed`
- `erode:chennai:textiles`

Why:

- better support from policy-corridor signals, directed-lane notes, and reliability proxies

### Weaker Than v1

- `chennai:tiruppur:textiles`
- `namakkal:chennai:poultry_industrial`

Why:

- the return-fit problem and vehicle-compatibility risk are clearer than they first appeared

## New v2 Strategic Read

### Launch-Now Lane

- `hosur:chennai:auto_components`

Why it qualifies:

- strong industrial demand
- strong corridor priority
- ability to support premium reliability promise
- competitive position is attractive enough for focused attack

### Best Validate-Manually Lanes

- `tiruppur:chennai:garments`
- `coimbatore:chennai:engineering`
- `chennai:coimbatore:mixed`
- `erode:chennai:textiles`
- `hosur:coimbatore:industrial`

Why:

- these lanes are strategically attractive, but still need real rate and field-confirmation data before broad rollout

### Build-Later Lanes

- `chennai:tiruppur:textiles`
- `namakkal:chennai:poultry_industrial`

Why:

- useful within broader loops, but not strong enough yet as independent launch priorities

### Gated Port-Linked Lane

- `coimbatore:tuticorin_via_madurai:export`

Why:

- strategically promising
- still blocked by port workflow, document, and partner-complexity risk

## True Field Inputs Still Needed

Before a `v3` pass:

- 3-5 shipper interviews per top corridor
- 3-5 transporter interviews per top corridor
- 10-14 day live rate capture
- reverse-load posting evidence
- live delay and wait-time evidence
- proof-asset availability confirmation

## v2 Conclusion

This pass is materially better than `v1`.

It is strong enough for:

- dashboard prototyping
- corridor sequencing discussion
- GTM focus narrowing
- pricing confidence prioritization

It is not yet strong enough to replace actual field validation.
