---
type: algorithm
domain: allocation
decision_value: high
inputs:
  - order_requirements
  - available_vehicles
  - route_details
  - partner_capacity
outputs:
  - selected_vehicle
  - assignment_rationale
  - assignment_confidence
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - algorithm
  - allocation
  - vehicle
---

# Vehicle Assignment Logic

## Purpose

Select the best-fit vehicle for an order by balancing cargo fit, pickup feasibility, utilization impact, and service risk.

## Inputs

| Input | Description |
|-------|-------------|
| order_requirements | Cargo type, weight, timing, special handling |
| available_vehicles | Own and partner vehicles with current status |
| route_details | Distance, terrain, restrictions, ETA sensitivity |
| partner_capacity | External fallback capacity by corridor |

## Logic

```text
1. PRE-FILTER vehicles by cargo compatibility, delivery type, dimensions, age, and legal fit
2. REMOVE vehicles that cannot meet timing, route, or handling constraints
3. SCORE candidates by proximity, utilization impact, reliability, ETA confidence, and return potential
4. PREFER own fleet when fit is strong and service risk is low
5. USE partner capacity when own fleet is unavailable or corridor fit is better
6. KEEP top alternates and compute assignment confidence
7. TRIGGER fallback cascade if confidence is below threshold or no feasible vehicle exists
8. RETURN highest-scoring feasible vehicle with rationale
```

## Scoring Factors

| Factor | Weight | Purpose |
|--------|--------|---------|
| Capacity fit | 30% | Avoid over/under-sizing |
| Pickup proximity | 25% | Reduce response delay |
| Utilization impact | 20% | Improve fleet economics |
| Reliability | 15% | Reduce service failure risk |
| Route fit | 10% | Match vehicle to corridor needs |

## Confidence and Fallback Rules

- Auto-assign only when assignment confidence is strong and no hard-rule violations remain.
- Keep at least two alternates for dispatcher review on high-value or urgent orders.
- If no candidate clears threshold, expand radius, query partner capacity, or re-open the order to manual dispatch.
- Treat reservation success as temporary inventory control, not assignment finality.

## Related Notes

- [[Driver Assignment Logic]]
- [[Fleet Allocation Algorithm]]
- [[Load Matching Algorithm]]
- [[IMS Matching Engine]]
- [[Return Load Optimization]]
- [[Fleet Utilization]]
- [[Transport Company Network Model]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
