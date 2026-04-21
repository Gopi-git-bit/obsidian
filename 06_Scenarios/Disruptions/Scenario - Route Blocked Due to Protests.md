---
type: scenario
domain: operations
urgency: high
decision_value: high
actors:
  - dispatcher
  - driver
  - customer
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
source_notes:
  - claude
tags:
  - scenario
  - disruptions
  - route-issue
---

# Scenario - Route Blocked Due to Protests

## Situation

Driver encounters road blockage due to protests, bandhs, or local disturbances while in transit. Cannot continue on planned route.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Blockage type | Protest/Bandh | Duration unknown |
| Location | Current position | Detour options |
| Cargo urgency | Time-sensitive | Delay impact |
| Safety | Priority | Driver and cargo |

## Decision Questions

1. **Detour available?** Alternative routes?
2. **Wait it out?** Estimated clearance time?
3. **Return to origin?** Unload and reschedule?
4. **Customer communication?** Proactive updates?

## Recommended Response

```
1. COMMUNICATE with driver for situation assessment
2. CHECK alternative routes via [[Route Optimization Logic]]
3. CALCULATE delay impact and new ETA
4. NOTIFY customer immediately with updated timeline
5. IF safe: Route through detour
6. IF unsafe: Wait for clearance or arrange alternate pickup
7. DOCUMENT incident for records
```

## Risks

- Extended delays → SLA breach
- Safety concerns → Driver welfare
- Cargo at risk → Security measures

## Related SOPs

- [[SOP - Handle Delayed Shipment]]
- [[SOP - Handle Vehicle Breakdown]]

## Related Concepts

- [[Route Deviation Risk]]
- [[Logistics SLA]]

## Related Algorithms

- [[Route Risk Scoring]]
- [[ETA Prediction Logic]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Fleet & Transport Hub]]
