---
type: concept
domain: operations
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - Scenario Playbooks Hub
tags:
  - concept
  - operations
  - delivery
  - exception
---

# Failed Delivery Handling

## Definition

Failed delivery handling is the exception workflow that decides whether a missed last-mile attempt should become a retry, address correction, payment hold, customer escalation, return-to-origin, or dispute case.

## Failure Categories

| Category | Examples | Default response |
|----------|----------|------------------|
| Address failure | Bad pin, incomplete address, wrong landmark, inaccessible location | Correct address before retry |
| Consignee unavailable | No answer, closed premises, absent recipient | Retry within allowed window |
| Payment failure | COD/ToPay refusal, insufficient amount, payment confusion | Payment clarification hold |
| Refusal | Damaged item claim, unwanted shipment, wrong shipment | Capture evidence and escalate |
| Access issue | Security gate, restricted timing, no unloading space | Reschedule with access instructions |
| Driver/route issue | Delay, vehicle breakdown, overloaded route | Reassign or resequence route |
| Evidence issue | Missing OTP, weak POD, GPS mismatch | Document hold before completion |

## Recovery Decision Tree

```text
Failed attempt
-> classify reason
-> check retry eligibility
-> correct missing data or consent
-> choose retry / reschedule / escalation / RTO
-> notify customer and consignee
-> sync evidence and cost impact
```

## Retry Rules

- Retry only after the reason for failure is specific enough to fix or intentionally accept.
- Do not retry an address failure without corrected geocode, landmark, or recipient confirmation.
- Do not retry payment failure without payment-mode clarification or approved exception.
- Prioritize same-day retry only when route capacity, customer promise, and driver hours allow it.
- Escalate high-value, fragile, perishable, or customer-critical shipments sooner than standard parcels.
- Move to RTO only after retry policy, customer communication, and exception approval are complete.

## Cost And Risk Controls

- Track cost per failed attempt, not only cost per dispatched order.
- Separate controllable failures from customer-caused failures.
- Feed address failures into serviceability and geocoding improvements.
- Feed consignee-unavailable patterns into delivery-window recommendation logic.
- Feed payment failures into customer risk, ToPay policy, and pre-alert messaging.
- Preserve evidence for disputes before returning, redelivering, or settling payment.

## Key Metrics

- failed delivery rate
- failure reason distribution
- retry success rate
- average attempts per delivered shipment
- RTO rate
- address-error rate
- cost per failed attempt
- support tickets per failed delivery
- time from failed attempt to next decision

## Related Notes

- [[Delivery Attempt Management]]
- [[Last-Mile Delivery Execution]]
- [[Fallback & Resilience Architecture]]
- [[Proof of Delivery]]
- [[Order Lifecycle]]
- [[Scenario Management Framework]]
