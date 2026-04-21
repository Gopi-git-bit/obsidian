---
type: scenario
domain: operations
urgency: medium
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
  - multi-stop
---

# Scenario - Multiple Pickup Points

## Situation

Customer needs goods collected from multiple pickup locations before delivering to a single destination or multiple destinations.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Number of stops | 2-10+ | Depends on order |
| Stop sequence | Must optimize | Minimize route |
| Time at each stop | Variable | 15-60 min |
| Load consolidation | Required | Maximize vehicle |

## Decision Questions

1. **Route optimization?** Best sequence for stops
2. **Time window?** Customer availability at each stop
3. **Vehicle capacity?** Enough for all pickups
4. **Loading sequence?** First pickup = last delivery?

## Recommended Response

```
1. COLLECT all pickup addresses and times
2. RUN [[Multi-stop Route Planning]] algorithm
3. CONFIRM vehicle capacity meets combined load
4. COMMUNICATE route to driver with timing
5. TRACK each pickup completion
```

## Related SOPs

- [[SOP - Assign Vehicle to Order]]
- [[SOP - Handle Partner Transporter]]

## Related Concepts

- [[Line Haul vs Last Mile]]
- [[Load Planning]]

## Related Algorithms

- [[Route Optimization Logic]]
- [[Load Matching Algorithm]]

## Related Hubs

- [[Algorithms Hub]]
- [[Operations Strategy Hub]]
