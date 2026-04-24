---
type: concept
domain: operations
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - Business Models Hub
  - Customer Problems Hub
tags:
  - concept
  - operations
  - detention
  - demurrage
  - dock-scheduling
  - wait-time
---

# Detention & Demurrage Framework

## Purpose

Define how loading and unloading delay should be measured, priced, and operationalized in a state-safe and audit-ready logistics system.

## Why It Matters

- Idle vehicles destroy trip productivity, fleet utilization, and driver earnings.
- Delay cost is often hidden until it becomes a dispute.
- Consignor and consignee dwell time should be converted into measurable operational signals instead of handled through ad hoc negotiation.

## Core Model

| Concept | Meaning |
|--------|---------|
| Free time | Allowed loading or unloading time before penalty logic begins |
| Detention | Vehicle or driver wait time beyond free time at pickup or delivery |
| Demurrage | Commercial charge calculated from excess wait according to policy |
| Gate events | Arrival, gate-in, loading start, loading end, gate-out, or equivalent milestone evidence |

## Required Event Evidence

- Arrival timestamp near consignor or consignee geofence
- Gate-in and gate-out when the site supports it
- Driver-side confirmation for manual sites
- Optional dock or queue assignment metadata
- Source attribution for whether delay was pickup-side or delivery-side

## Minimum Timeline Logic

1. Capture vehicle arrival at the site.
2. Capture service-start event when loading or unloading actually begins.
3. Capture service-end or gate-out event.
4. Compute total dwell time and billable excess beyond free time.

## Operational Rules

| Rule | Reading |
|------|---------|
| Evidence before billing | No detention billing without timeline evidence |
| Free-time policy is explicit | Site, customer, or corridor-specific allowances must be versioned |
| Pickup and delivery are separate | Consignor-side and consignee-side delays should not be blended into one opaque charge |
| ETA and dispatch should learn | Repeated dwell patterns should improve route planning and commitment quality |
| Disputes are traceable | Delay charges must be explainable from raw event history |

## Product and Pricing Implications

- Dispatch should surface expected dwell risk before vehicle assignment where historical data exists.
- Pricing can include explicit free-time assumptions instead of hiding delay inside base freight.
- Premium fast-turnaround services become possible only when slot access and dwell control are measurable.
- Partner scorecards should include site efficiency and detention frequency.

## Technology Reading

| Capability | Why It Helps |
|-----------|--------------|
| Dock scheduling | Reduces unmanaged queues and creates structured slot ownership |
| Gate-event capture | Makes detention evidence auditable |
| Wait-time prediction | Improves ETA quality and dispatch sequencing |
| Automated notifications | Keeps drivers, warehouses, and customers aligned on slot and queue changes |
| Timeline-linked invoicing | Converts excess wait into transparent commercial logic |

## Zippy-Fit Direction

- Start with arrival, gate-in, and gate-out telemetry before building premium slot products.
- Use dwell data first for visibility and partner benchmarking, then for demurrage automation.
- Keep detention and demurrage policy deterministic and configurable rather than agent-invented.

## Related Notes

- [[Indian Road Logistics Pain Point Map]]
- [[Logistics SLA]]
- [[TMS Execution Architecture]]
- [[ETA Prediction Logic]]
- [[Notification Taxonomy & Escalation Matrix]]
- [[Revenue Model Decision Framework]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Business Models Hub]]
- [[Customer Problems Hub]]
