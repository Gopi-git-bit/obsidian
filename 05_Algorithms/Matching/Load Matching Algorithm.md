---
type: algorithm
domain: matching
decision_value: high
inputs:
  - order_requirements
  - vehicle_type
  - route
  - urgency
  - cargo_type
  - customer_priority
  - historical_data
outputs:
  - assignment_decision
  - match_score
  - fallback_path
  - reservation_hint
status: verified
related_hubs:
  - Algorithms Hub
  - Operations Strategy Hub
tags:
  - algorithm
  - matching
---

# Load Matching Algorithm

## Purpose

Match available vehicle capacity with incoming shipment requirements to optimize feasibility, service quality, and trip economics.

The algorithm should follow the [[Demand-Driven Logistics Blueprint]] principle: forecast capacity at the lane or region level, but execute assignment against live customer demand and confirmed vehicle availability.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| order_requirements | Object | Weight, volume, vehicle type, special needs |
| vehicle_type | Enum | LCV, MCV, HCV, container |
| route | Object | Origin, destination, distance |
| urgency | Enum | Normal, express, urgent |
| cargo_type | String | Category of goods |
| customer_priority | Integer | 1-5 priority score |
| historical_data | Object | ETA, reliability, lane demand, and return-trip patterns |

## Logic

```text
1. PRE-FILTER candidates by vehicle type, body compatibility, capacity, dimensions, and timing feasibility
2. IF no candidate passes, trigger fallback search or radius expansion
3. CALCULATE route_match_score (origin proximity + destination fit)
4. CALCULATE capacity_utilization (load vs vehicle capacity)
5. CALCULATE timing_score (urgency vs vehicle availability)
6. CALCULATE reliability_score (vehicle/driver history)
7. CALCULATE return_trip_probability from lane history and nearby demand
8. CALCULATE packing_efficiency for space fit on the selected vehicle
9. WEIGHTED_SCORE = route + capacity + timing + reliability + return potential + packing
10. STABLE-MATCH top candidates where return-trip optimization matters
11. ATTEMPT candidate reservation or reservation hinting where concurrency risk exists
12. TRACK matching lead-time from validation to match proposal
13. SELECT top candidate above threshold and keep alternates
14. IF request remains unmatched beyond SLA, trigger radius expansion, partner fallback, or dispatcher escalation
```

### Default Weights

- route_match: 0.25
- capacity_utilization: 0.20
- timing_score: 0.20
- reliability_score: 0.15

### Advanced Scoring Extension

When lane history and telemetry are available, add:

- return_trip_probability: 0.10
- packing_efficiency: 0.10

In mature deployments, timing can be upgraded from a rules-based score to predictive ETA confidence.

## Rules

### Hard Rules (Must Pass)

- Vehicle type must match requirement
- Vehicle must be available at pickup time
- Capacity must accommodate cargo
- Dimensions and body type must fit cargo requirements
- Route must be feasible
- Compliance status must be valid for dispatch

### Soft Rules (Preference)

- Higher utilization preferred (>70%)
- Partner reliability score > 3.5
- Route deadhead minimization
- Higher return-trip probability preferred on long-haul lanes
- Prefer flexible capacity pools over early hard pre-allocation on volatile lanes
- Favor candidates that can respond within the target acceptance window

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No vehicle match | Escalate to [[Scenario - No Own Fleet Available]] |
| Multiple equal matches | Prefer existing customer |
| Urgent with no capacity | Trigger [[SOP - Handle Urgent Request]] |
| Special cargo (hazmat) | Verify certifications first |
| Weak match confidence | Keep alternates and route to manual dispatch review |
| Request aging beyond SLA | Trigger [[Strategic Lead-Time Management]] escalation rule |

## Related Notes

- [[Vehicle Assignment Logic]]
- [[IMS Matching Engine]]
- [[Carrier Selection Algorithm]]
- [[Fleet Allocation Algorithm]]
- [[Return Load Optimization]]
- [[Scenario - No Own Fleet Available]]
- [[Demand-Driven Logistics Blueprint]]
- [[Strategic Lead-Time Management]]
