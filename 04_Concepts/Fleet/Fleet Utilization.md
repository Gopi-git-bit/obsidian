---
type: concept
domain: fleet
decision_value: high
status: evergreen
related_hubs:
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - concept
  - fleet
---

# Fleet Utilization

## Definition

The percentage of time vehicles are actively engaged in revenue-generating operations versus idle or empty movement.

## Formula

```
Fleet Utilization % = (Revenue-Generating Hours / Total Available Hours) × 100
```

## Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Time Utilization | Hours moving vs available | >70% |
| Load Factor | Capacity used vs available | >85% |
| Empty Running | Deadhead percentage | <30% |
| Turnaround Time | Time between trips | Minimize |

## Why It Matters

- Directly impacts profitability
- Determines effective fleet capacity
- Affects pricing competitiveness
- Drives return load optimization

## Key Variables

- [[Return Load Economics]]
- Route density
- [[LCV vs MCV vs HCV]] mix
- Seasonality
- Geographic coverage

## Decision Impact

- [[Vehicle Assignment Logic]]
- [[Dynamic Pricing Logic]]
- Partner fleet need assessment

## Ways to Improve

1. **Backhaul optimization** - [[Return Load Optimization]]
2. **Route clustering** - Group nearby deliveries
3. **Flexible vehicle mix** - Match vehicle to load
4. **Real-time matching** - Quick turnaround
5. **Forecast capacity, execute demand** - Plan aggregate vehicle availability by lane or region, but commit exact vehicles only when live demand appears
6. **Idle-age escalation** - Alert operations when an available vehicle remains unmatched beyond the target threshold

## Demand-Driven Utilization Principle

Do not improve utilization by locking vehicles into weak assumptions too early.

Use [[Demand-Driven Logistics Blueprint]] logic:

- keep capacity visible and flexible
- monitor demand by lane and pincode cluster
- move vehicles toward probable demand where confidence is high
- finalize assignment only after request, timing, cargo fit, and owner response are confirmed

This reduces empty movement while protecting responsiveness on uncertain lanes.

## Related Notes

- [[Transport Company Network Model]]
- [[Load Matching Algorithm]]
- [[Fleet Allocation Algorithm]]
- [[Demand-Driven Logistics Blueprint]]
- [[Collaborative Planning and Forecasting for Logistics]]
- [[Scenario - No Own Fleet Available]]
