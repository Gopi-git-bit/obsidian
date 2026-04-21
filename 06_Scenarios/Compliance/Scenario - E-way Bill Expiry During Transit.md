---
type: scenario
domain: compliance
urgency: critical
decision_value: high
actors:
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Compliance & Regulation Hub
tags:
  - scenario
  - compliance
  - e-way-bill
---

# Scenario - E-way Bill Expiry During Transit

## Situation

Vehicle is in transit but the E-way bill is about to expire before reaching the destination. Legal implications if not addressed.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| E-way bill expiry | Soon | Within hours |
| Distance remaining | Significant | May not reach in time |
| Location | En route | Remote or near state border |
| Legal risk | High | Penalties for expiry |

## Recommended Response

```
1. ALERT received for expiring E-way bill
2. CALCULATE if delivery possible before expiry
3. IF possible: Expedite delivery, priority routing
4. IF not possible:
   a. STOP at nearest safe location
   b. UPDATE Part B with extended validity
   c. COORDINATE with consignor for extension
5. COMMUNICATE situation to customer
6. ENSURE driver does NOT continue without valid E-way bill
7. DOCUMENT for compliance records
```

## Risks

- Legal penalty → Fines and confiscation
- Vehicle detention → Extended delays
- Customer impact → Delivery blocked

## Related SOPs

- [[SOP - E-way Bill Generation]]
- [[SOP - Verify Shipment Documents]]

## Related Concepts

- [[E-way Bill]]
- [[State-wise Entry Tax]]

## Related Hubs

- [[Compliance & Regulation Hub]]
