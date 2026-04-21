---
type: algorithm
domain: allocation
decision_value: high
inputs:
  - vehicle_assigned
  - available_drivers
  - order_requirements
  - route_details
outputs:
  - driver_assignment
  - assignment_score
  - response_window
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
tags:
  - algorithm
  - allocation
  - driver
---

# Driver Assignment Logic

## Purpose

Assign the best available driver to an assigned vehicle based on performance, experience, and match factors.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| vehicle_assigned | Object | Vehicle details |
| available_drivers | Array | Drivers with current status |
| order_requirements | Object | Route and cargo details |
| route_details | Object | Distance, terrain, duration |

## Logic

```
1. FILTER drivers by:
   - License type matches vehicle
   - Location within pickup range
   - Availability at required time
   - Route familiarity

2. SCORE drivers by:
   - Performance rating (40%)
   - Experience with route type (25%)
   - On-time record (20%)
   - Customer ratings (15%)

3. RANK candidates by score

4. ASSIGN highest-ranked available driver
```

## Operational Response Rules

- Treat assignment acceptance as a backend-confirmed action, not a UI assumption.
- Use bounded response windows before timing out and re-offering work.
- Support snooze or deferral semantics only when they are explicit and time-limited.

## Scoring Components

| Factor | Weight | Data Source |
|--------|--------|-------------|
| Performance Rating | 40% | Historical delivery data |
| Route Experience | 25% | Past deliveries on similar routes |
| On-time Record | 20% | Delivery SLA adherence |
| Customer Rating | 15% | Shipper feedback |

## Assignment Rules

| Rule | Description |
|------|-------------|
| License match | Driver must have valid license for vehicle type |
| Shift limits | No assignment exceeding 10 hours driving |
| Break compliance | Schedule break points for long routes |
| History check | No recent safety incidents |
| Response window | Driver must respond within the configured timeout |

## Related Notes

- [[Vehicle Assignment Logic]]
- [[Fleet Allocation Algorithm]]
- [[Driver App Frontend Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
