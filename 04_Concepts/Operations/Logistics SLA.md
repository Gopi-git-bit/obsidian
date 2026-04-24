---
type: concept
domain: operations
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - Customer Problems Hub
tags:
  - concept
  - operations
  - sla
---

# Logistics SLA

## Definition

The service-level commitment that defines expected performance for booking, pickup, transit, delivery, communication, and issue resolution in logistics operations.

## Typical SLA Dimensions

| Dimension | Example Measure |
|-----------|-----------------|
| Booking response | Quote or confirmation within target time |
| Pickup timeliness | Vehicle arrives within pickup window |
| Transit updates | Status updates shared at defined intervals |
| Delivery timeliness | Delivery completed within promised ETA window |
| POD turnaround | Proof of delivery submitted within target period |
| Complaint resolution | Customer issue resolved within agreed time |

## Why It Matters

- Sets clear customer expectations
- Anchors operational escalation thresholds
- Supports performance reviews and dispute handling
- Connects service quality to retention and margin

## Common SLA Risks

- Delay from driver or partner failure
- Poor customer communication during disruption
- Missing POD or incomplete documentation
- Unrealistic commitments during booking

## Decision Impact

- Drives [[SOP - Customer Communication]]
- Shapes [[SOP - Handle Delayed Shipment]]
- Determines escalation timing in exception handling
- Defines when TMS alerts become disputes instead of silent ETA drift

## Routing-Specific SLA Notes

- ETA monitoring should compare planned versus actual route progression.
- Routing latency and ETA accuracy are operational SLAs, not just engineering metrics.
- SLA breaches should create explicit dispute or escalation records.
- Pricing, refunds, and settlement changes should remain outside automatic routing workflows.
- ETA confidence calibration matters because false certainty is an SLA risk, not just a modeling issue.
- Low-confidence ETA should trigger conservative promises and earlier human review.
- GPS silence, route deviation, and delayed movement after assignment are transportation SLAs, not just telemetry curiosities.
- Grace periods should be explicit before emitting breach events.

## Dwell-Time SLA Notes

- Arrival, gate-in, service-start, and gate-out events should be treated as operational evidence, not optional metadata.
- Repeated pickup or delivery dwell beyond policy thresholds is both an SLA and profitability problem.
- Demurrage or detention charges should only be raised from traceable timeline evidence and explicit free-time rules.
- High-dwell sites should influence ETA promises, dispatch sequencing, and partner review.

## Fallback-Specific SLA Notes

- Degraded mode is acceptable only if it remains observable and reversible.
- High fallback frequency is itself an SLA warning signal.
- Recovery quality should be measured, not assumed from mere completion.

## Customer-App SLA Notes

- Booking and payment retries should not create duplicate operational side effects.
- Consent status, payment progress, and assignment updates should stay visible under weak network conditions.
- Critical user actions should remain auditable even when the app falls back to deferred sync.

## Related Notes

- [[Proof of Delivery]]
- [[Unified Routing & Optimization Algorithm]]
- [[ETA Prediction Logic]]
- [[TMS Execution Architecture]]
- [[Fallback & Resilience Architecture]]
- [[Customer App Frontend Architecture]]
- [[Detention & Demurrage Framework]]
- [[Scenario - Route Blocked Due to Protests]]
- [[Scenario - Vehicle Breakdown Mid-Route]]
- [[Customer Service Agent]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Customer Problems Hub]]
