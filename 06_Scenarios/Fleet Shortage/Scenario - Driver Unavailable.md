---
type: scenario
domain: fleet
urgency: high
decision_value: high
actors:
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - scenario
  - fleet
  - driver-issue
---

# Scenario - Driver Unavailable

## Situation

Assigned driver is unavailable for pickup due to illness, personal emergency, or no-show. Vehicle is ready but driver cannot operate.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Unavailability reason | Various | Need to document |
| Time to pickup | Urgent | Customer waiting |
| Vehicle status | Ready | Can be reassigned |
| Replacement | Needed | New driver required |

## Decision Questions

1. **Can driver be reached?** Emergency contact?
2. **Backup driver available?** Within time window?
3. **Vehicle reassignment?** Different driver-vehicle pair?
4. **Customer notification?** Inform of delay?

## Recommended Response

```
1. CONTACT driver for status confirmation
2. IF unavailable:
   a. CHECK for backup driver in area
   b. IDENTIFY alternative vehicle-driver pair
   c. COORDINATE quick handover
3. COMMUNICATE delay to customer with new ETA
4. DOCUMENT incident for records
5. FOLLOW UP with unavailable driver post-incident
```

## Risks

- Pickup delay → Order at risk
- Customer dissatisfaction → Trust impact
- Driver performance → Review needed

## Related SOPs

- [[SOP - Assign Vehicle to Order]]
- [[SOP - Handle Partner Transporter]]
- [[SOP - Customer Communication]]

## Related Concepts

- [[Driver Assignment Logic]]
- [[Driver Performance Metrics]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Driver Assignment Logic]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
