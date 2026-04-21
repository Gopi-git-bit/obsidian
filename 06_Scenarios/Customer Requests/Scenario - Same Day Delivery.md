---
type: scenario
domain: operations
urgency: critical
decision_value: high
actors:
  - customer
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
tags:
  - scenario
  - customer-requests
  - urgent
---

# Scenario - Same Day Delivery

## Situation

Customer requires shipment to be picked up and delivered within the same business day - no advance scheduling.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Urgency | Critical | Same-day only |
| Distance | Any | Within feasible range |
| Vehicle type | Any | Based on cargo |
| Price sensitivity | Lower | Urgency premium expected |

## Decision Questions

1. **Available capacity?** Immediate vehicle availability
2. **Route feasibility?** Can reach destination same day
3. **Pricing?** Apply [[Urgency Surcharge Logic]]
4. **Priority?** Bump other orders if needed

## Recommended Response

```
1. CHECK immediate vehicle availability
2. IF available: Quote with urgency premium
3. IF not available: Search partner network
4. COORDINATE immediate pickup scheduling
5. MONITOR transit in real-time
6. PREPARE for fastest delivery route
```

## Risks

- No vehicles available → Escalate to customer
- Route delays → Proactive communication
- Driver unavailable → Partner fallback

## Related SOPs

- [[SOP - Handle Urgent Request]]
- [[SOP - Assign Vehicle to Order]]

## Related Concepts

- [[Urgency Surcharge Logic]]
- [[Fleet Utilization]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Route Optimization Logic]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Fleet & Transport Hub]]
