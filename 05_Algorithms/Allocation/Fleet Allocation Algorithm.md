---
type: algorithm
domain: allocation
decision_value: high
inputs:
  - order_requirements
  - available_vehicles
  - vehicle_types
  - location_constraints
outputs:
  - vehicle_assignment
  - allocation_score
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
tags:
  - algorithm
  - allocation
---

# Fleet Allocation Algorithm

## Purpose

Optimally allocate available fleet resources to maximize utilization while meeting delivery requirements.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| order_requirements | Array | All pending orders |
| available_vehicles | Array | Current fleet status |
| vehicle_types | Enum | LCV/MCV/HCV/Container |
| location_constraints | Object | Depot locations, coverage areas |

## Logic

```
1. PRIORITIZE orders by:
   - Urgency (deadline)
   - Margin potential
   - Customer value

2. MATCH vehicles to orders:
   - Capacity fit (avoid underutilization)
   - Location proximity
   - Vehicle availability timeline

3. CALCULATE allocation score:
   - Utilization efficiency
   - Deadhead minimization
   - Customer priority alignment

4. OPTIMIZE globally:
   - Batch compatible orders
   - Minimize repositioning
   - Balance workload across vehicles
```

## Optimization Rules

| Priority | Weight | Description |
|----------|--------|-------------|
| Utilization | 0.30 | Maximize capacity usage |
| Deadhead | 0.25 | Minimize empty return |
| Proximity | 0.20 | Closest vehicle first |
| Priority | 0.15 | Urgency-based |
| Margin | 0.10 | Revenue optimization |

## Utilization Targets

| Vehicle Type | Target Load | Min Acceptable |
|-------------|-------------|----------------|
| LCV | 85% | 60% |
| MCV | 80% | 55% |
| HCV | 75% | 50% |

## Related Notes

- [[Fleet Utilization]]
- [[Load Matching Algorithm]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
