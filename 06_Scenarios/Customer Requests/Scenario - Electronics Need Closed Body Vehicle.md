---
type: scenario
domain: transport
urgency: medium
decision_value: high
actors:
  - customer
  - dispatcher
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Fleet & Transport Hub
tags:
  - scenario
  - customer-requests
  - cargo-type
---

# Scenario - Electronics Need Closed Body Vehicle

## Situation

Customer needs to transport electronic goods (laptops, phones, TVs) that require closed body vehicles for protection from dust, moisture, and theft.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Cargo type | Electronics | Closed body mandatory |
| Value | High | Security concerns |
| Handling | Careful | Fragile components |
| Route | Any | Standard routes |

## Recommended Response

```
1. REQUIRE closed body vehicle only
2. VERIFY vehicle has no rear opening issues
3. CHECK for GPS tracking capability
4. CONFIRM cargo insurance coverage
5. DOCUMENT vehicle condition at pickup
```

## Related SOPs

- [[SOP - Assign Secure Vehicle]]
- [[SOP - Verify Shipment Documents]]

## Related Concepts

- [[Closed Body Vehicle]]
- [[Electronics Logistics Requirements]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
