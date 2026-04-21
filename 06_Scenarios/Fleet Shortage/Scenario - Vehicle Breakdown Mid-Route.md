---
type: scenario
domain: fleet
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
  - Fleet & Transport Hub
  - Operations Strategy Hub
source_notes:
  - claude
tags:
  - scenario
  - fleet
  - breakdown
---

# Scenario - Vehicle Breakdown Mid-Route

## Situation

Vehicle assigned to an order breaks down during transit. Cargo is on board and delivery is at risk.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Breakdown type | Mechanical | Can be repaired? |
| Location | Current | Remote or accessible? |
| Cargo status | Safe | Driver and goods safe |
| ETA impact | Significant | Delivery at risk |

## Decision Questions

1. **Can vehicle be repaired?** Quick fix possible?
2. **Transfer cargo?** Need another vehicle?
3. **Customer notification?** Proactive communication?
4. **Timeline recovery?** Can we still meet delivery?

## Recommended Response

```
1. RECEIVE breakdown notification from driver
2. ASSESS situation - repairable or need transfer
3. IF quick fix: Dispatch repair support, give time
4. IF transfer needed:
   a. SEND replacement vehicle to location
   b. COORDINATE cargo transfer
   c. UPDATE driver with new ETA
5. NOTIFY customer of situation and revised timeline
6. TRACK new vehicle to destination
7. INVESTIGATE breakdown cause post-delivery
```

## Risks

- Delivery delay → SLA breach
- Cargo damage → Claims
- Customer dissatisfaction → Churn

## Related SOPs

- [[SOP - Handle Vehicle Breakdown]]
- [[SOP - Handle Partner Transporter]]
- [[SOP - Customer Communication]]

## Related Concepts

- [[Fleet Maintenance Scheduling]]
- [[Vehicle Availability]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Route Risk Scoring]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
