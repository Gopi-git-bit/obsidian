---
type: algorithm
domain: allocation
decision_value: high
inputs:
  - cost_efficiency
  - route_familiarity
  - operational_reliability
  - capacity_utilization
  - driver_expertise
outputs:
  - normalized_vehicle_score
  - ranking_explanation
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Technology Stack Hub
tags:
  - algorithm
  - allocation
  - optimization
  - scoring
---

# Multi-Objective Vehicle Scoring

## Purpose

Rank vehicles for an order using normalized utility scoring so cost does not dominate reliability, familiarity, and utilization signals.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| cost_efficiency | Float | Estimated trip cost where lower is better |
| route_familiarity | Float | Driver or vehicle familiarity with the corridor |
| operational_reliability | Float | Maintenance and execution reliability |
| capacity_utilization | Float | Expected load fit on the candidate vehicle |
| driver_expertise | Float | Suitability for cargo type and handling needs |

## Logic

```text
1. NORMALIZE each objective to a common 0-1 scale
2. INVERT cost so lower cost produces a higher utility score
3. APPLY explicit weights to cost, familiarity, reliability, utilization, and expertise
4. SUM weighted utilities into a composite score
5. RANK candidates and preserve factor-level explanation for manual review
```

## Default Weights

| Objective | Weight |
|-----------|--------|
| Cost efficiency | 0.30 |
| Route familiarity | 0.15 |
| Operational reliability | 0.20 |
| Capacity utilization | 0.10 |
| Driver expertise | 0.15 |

## Decision Rules

- Use normalized scoring only after hard-rule feasibility checks pass.
- Prefer explainable factors over opaque black-box scoring for dispatch workflows.
- Re-tune weights by lane, service tier, or cargo category when commercial behavior differs materially.
- Keep room for Pareto-style expansion when multiple candidates are similarly strong.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| One metric dwarfs others | Re-check normalization bounds |
| Reliability data missing | Penalize confidence or require manual review |
| Multiple near-equal scores | Prefer lower service risk or higher backhaul fit |

## Related Notes

- [[Vehicle Assignment Logic]]
- [[Load Matching Algorithm]]
- [[Return Load Optimization]]
- [[Hybrid Logistics Data Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Technology Stack Hub]]

