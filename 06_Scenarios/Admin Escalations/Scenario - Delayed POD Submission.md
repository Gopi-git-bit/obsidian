---
type: scenario
domain: operations
urgency: medium
decision_value: medium
actors:
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
source_notes:
  - claude
tags:
  - scenario
  - admin-escalations
  - documentation
---

# Scenario - Delayed POD Submission

## Situation

Driver has completed delivery but Proof of Delivery (POD) is not submitted within expected timeframe. Customer is waiting and invoice cannot be generated.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Delivery status | Completed | Goods delivered |
| POD status | Missing | Not received |
| Delay duration | Variable | Time since delivery |
| Impact | Billing blocked | Payment pending |

## Recommended Response

```
1. CONTACT driver immediately for POD
2. REQUEST photo of signed POD
3. IF unavailable: Send proof of delivery alternatives
4. VERIFY delivery completion independently
5. PROCESS manual POD if needed
6. UPDATE invoice status accordingly
7. FOLLOW UP with driver on process compliance
```

## Risks

- Payment delay → Cash flow impact
- Customer dispute → Without POD evidence
- Process violation → Driver review needed

## Related SOPs

- [[SOP - Verify Shipment Documents]]
- [[SOP - Handle POD Disputes]]

## Related Concepts

- [[Proof of Delivery]]
- [[E-way Bill System]]

## Related Hubs

- [[Operations Strategy Hub]]
