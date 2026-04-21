---
type: scenario
domain: fleet
urgency: high
decision_value: high
actors:
  - dispatcher
  - customer
  - partner_transporter
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
  - shortage
---

# Scenario - No Own Fleet Available

## Situation

Customer has confirmed booking but no own fleet vehicle is available at required time/location.

## Variables

| Variable | Notes |
|----------|-------|
| Order priority | Determines search urgency |
| Time constraint | Hours until pickup window |
| Vehicle requirement | Type, capacity, special needs |
| Customer relationship | Repeat vs new customer |
| Profit margin | Can we absorb partner cost? |

## Decision Questions

1. **Partner fleet first?** Can partner fulfill on time?
2. **Price to customer?** Pass partner cost + margin?
3. **Delay shipment?** Negotiate timing with customer?
4. **Reject order?** Last resort if unworkable?

## Recommended Response

### Tier 1: Partner Network (Preferred)

```
1. SEARCH partner_transporters BY:
   - Location proximity
   - Vehicle availability
   - Historical reliability score
   - Price competitiveness

2. SELECT best_match using [[Load Matching Algorithm]]

3. CONFIRM with [[Carrier Scoring Algorithm]]

4. ESCALATE to dispatcher if no match
```

### Tier 2: Market Search

```
1. POST to load boards
2. CONTACT known transporters
3. NEGOTIATE terms
4. ACCEPT best available option
```

### Tier 3: Customer Communication

```
1. INFORM customer of situation
2. PROPOSE alternatives:
   - Slightly delayed pickup
   - Different vehicle type
   - Higher price for priority
3. GET explicit confirmation
```

## Risks

| Risk | Mitigation |
|------|------------|
| Partner delays | Real-time tracking, backup plan |
| Quality issues | Verify partner credentials |
| Margin erosion | Minimum margin floor |
| Customer churn | Proactive communication |

## Related SOPs

- [[SOP - Handle Partner Transporter]]
- [[SOP - Customer Communication]]
- [[SOP - Escalate Delayed Shipment]]

## Related Concepts

- [[Transport Company Network Model]]
- [[Fleet Utilization]]
- [[Return Load Economics]]
