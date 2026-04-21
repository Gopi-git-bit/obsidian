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

## Related Notes

- [[Transport Company Network Model]]
- [[Load Matching Algorithm]]
- [[Fleet Allocation Algorithm]]
- [[Scenario - No Own Fleet Available]]
