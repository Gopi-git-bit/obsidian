---
type: scenario
domain: operations
urgency: high
decision_value: high
actors:
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - scenario
  - disruptions
  - fuel
---

# Scenario - Fuel Shortage Crisis

## Situation

Region experiences fuel shortage due to strikes, price hikes, or supply disruption. Vehicles cannot refuel normally.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Fuel availability | Limited | May need long waits |
| Price impact | Increased | Higher costs |
| Vehicle stranded | Possible | Current fuel level |
| Operations impact | High | All routes affected |

## Decision Questions

1. **Current fuel levels?** Vehicles can complete trips?
2. **Alternative fuel sources?** Other stations?
3. **Route planning?** Fuel-efficient routes only
4. **Cost absorption?** Price increase handling?

## Recommended Response

```
1. ASSESS fuel situation in affected regions
2. COMMUNICATE with all drivers for fuel status
3. PRIORITIZE vehicles with critical deliveries
4. COORDINATE with fuel stations if possible
5. PLAN routes to minimize fuel consumption
6. ADJUST pricing to reflect fuel cost increase
7. MONITOR situation for resolution
```

## Risks

- Deliveries delayed → SLA breach
- Higher costs → Margin compression
- Driver welfare → Need at pumps

## Related SOPs

- [[SOP - Handle Delayed Shipment]]
- [[SOP - Driver Onboarding]]

## Related Concepts

- [[Fuel Tax Implications]]
- [[Route Optimization Logic]]

## Related Algorithms

- [[Route Optimization Logic]]
- [[Dynamic Pricing Logic]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
