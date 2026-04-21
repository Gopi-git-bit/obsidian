---
type: scenario
domain: operations
urgency: medium
decision_value: medium
actors:
  - customer
  - dispatcher
region: India
status: draft
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
tags:
  - scenario
  - customer-requests
  - cancellation
---

# Scenario - Customer Cancels Order

## Situation

Customer requests cancellation of an order that has been confirmed and possibly assigned to a vehicle/driver.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Cancellation reason | Various | Customer choice/Issue |
| Order status | Assigned/Pending | Stage matters |
| Vehicle status | Assigned/En route | Resource impact |
| Time window | Within limits? | Cancellation policy |

## Recommended Response

```
1. RECEIVE cancellation request
2. VERIFY cancellation policy applies
3. CHECK vehicle/driver assignment stage
4. IF vehicle not dispatched: Cancel and release
5. IF vehicle dispatched: Calculate cancellation fee
6. COMMUNICATE fee if applicable
7. RELEASE vehicle for other orders
8. UPDATE customer with confirmation
9. SEND refund if advance payment received
```

## Related SOPs

- [[SOP - Customer Communication]]
- [[SOP - Handle Partner Transporter]]

## Related Concepts

- [[Order Lifecycle]]
- [[Cancellation Policy]]

## Related Hubs

- [[Operations Strategy Hub]]
