---
type: concept
domain: operations
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - concept
  - operations
  - delivery
  - last-mile
---

# Delivery Attempt Management

## Definition

Delivery attempt management is the control process for deciding when a shipment is ready for doorstep attempt, how the recipient is contacted, what the driver should do at arrival, and how the system records success or failure.

## Attempt Readiness Checklist

| Check | Why it matters |
|-------|----------------|
| Address quality | Prevents wasted travel caused by bad geocodes, missing landmarks, or ambiguous pins |
| Consignee contact quality | Enables pre-call, WhatsApp, SMS, and issue clarification |
| Delivery window confidence | Aligns route plan with recipient availability |
| Payment readiness | Avoids COD/ToPay disputes at the doorstep |
| Cargo handling instructions | Protects fragile, perishable, high-value, or special cargo |
| Driver capacity | Ensures route length, payload, and time windows are realistic |
| POD requirements | Clarifies OTP, signature, photo, invoice, or recipient ID before attempt |

## Doorstep Protocol

```text
Pre-alert -> navigate -> arrival confirmation -> contact recipient -> wait window -> handover -> evidence capture -> status update
```

- Send a pre-alert before arrival with ETA, driver contact, payment requirement, and delivery instructions.
- Use a short call/WhatsApp/SMS escalation sequence if the consignee is not immediately available.
- Apply a standard wait window before marking the attempt failed.
- Capture precise failure reason if delivery cannot complete.
- Avoid marking delivered unless OTP/signature/POD and location evidence satisfy the order requirement.

## Attempt Outcomes

| Outcome | System action |
|---------|---------------|
| Delivered | Capture POD, update order, trigger invoice/payment closure where applicable |
| Partial issue | Capture notes/photos, escalate to support or operations |
| Consignee unavailable | Schedule retry based on route feasibility and customer promise |
| Address issue | Send to address correction flow before retry |
| Payment issue | Move to payment hold or ToPay clarification |
| Refused delivery | Capture reason, photos if needed, and create exception/RTO decision |
| Access restriction | Reschedule, request alternate contact, or route to support |

## Key Metrics

- first-attempt success rate
- attempts per successful delivery
- average wait time per stop
- failed attempt reason mix
- address-correction rate
- pre-alert delivery/read rate
- consignee response rate
- delivery-window adherence
- POD capture completeness

## Decision Impact

- Improves [[Last-Mile Delivery Execution]] by reducing unnecessary retries.
- Feeds [[Failed Delivery Handling]] with structured failure reasons.
- Supports [[Notification Taxonomy & Escalation Matrix]] with precise pre-alert and retry events.
- Protects [[Proof of Delivery]] quality before financial closure.

## Related Notes

- [[Last-Mile Delivery Execution]]
- [[Failed Delivery Handling]]
- [[Proof of Delivery]]
- [[Order Lifecycle]]
- [[Notification Taxonomy & Escalation Matrix]]
- [[Customer App Frontend Architecture]]
