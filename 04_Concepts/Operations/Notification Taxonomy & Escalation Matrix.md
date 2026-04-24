---
type: concept
domain: operations
decision_value: high
status: verified
related_hubs:
  - Operations Strategy Hub
  - AI Agents Hub
  - Customer Problems Hub
tags:
  - concept
  - notifications
  - escalation
  - communication
  - operations
---

# Notification Taxonomy & Escalation Matrix

## Purpose

Define how operational events become customer, driver, consignee, partner, finance, and supervisor notifications without creating noise, missed actions, or unsafe escalation gaps.

## Why It Matters

- A strong state machine still fails operationally if the right people are not informed at the right time.
- Notification policy should be deterministic enough to support audit, retries, and customer trust.
- Logistics operations need more than message delivery; they need delivery priority, acknowledgement rules, and fallback channels.

## Core Principles

1. Notifications are triggered by canonical events, not UI guesses.
2. Severity determines channel choice and escalation speed.
3. Critical actions should have acknowledgement or follow-up rules.
4. Notification retries must be deduplicated and observable.
5. Channel preference should influence delivery, but not suppress safety-critical communication.

## Audience Model

| Audience | Typical Need |
|----------|--------------|
| Customer or consignor | Booking, assignment, delay, delivery, payment, dispute visibility |
| Consignee | Arrival window, ToPay, delivery confirmation, OTP or POD-linked actions |
| Driver | Assignment, route, exception, evidence, and payment-status prompts |
| Transport company or partner | Assignment, SLA risk, vehicle issue, settlement or performance updates |
| Operations or supervisor | SLA breach, fraud risk, routing failure, unresolved escalation |
| Finance | Payment failure, settlement hold, reconciliation mismatch |

## Severity Classes

| Severity | Meaning | Typical Channels |
|----------|---------|------------------|
| Informational | User should know, but no action required now | In-app, push, email digest |
| Action required | User or operator must respond | Push, in-app, WhatsApp, SMS fallback |
| SLA risk | Delay or quality risk affecting service commitment | Push, WhatsApp, supervisor or ops alert |
| Financial critical | Payment, settlement, or duplicate-charge risk | In-app, email, finance alert, supervisor path |
| Safety or fraud critical | Immediate operational threat | SMS, phone workflow, supervisor alert, ops escalation |

## Canonical Event-to-Notification Pattern

| Event Type | Primary Audience | Primary Channel | Fallback | Escalation Owner |
|------------|------------------|-----------------|----------|------------------|
| `order_confirmed` | Customer | Push and in-app | Email | OMS |
| `assignment_accepted` | Customer | Push and in-app | WhatsApp | OMS |
| `driver_arriving_pickup` | Customer | Push | SMS for critical scheduling | TMS |
| `eta_delayed_significant` | Customer and ops | Push and WhatsApp | SMS | TMS |
| `gps_silence_detected` | Ops and supervisor | Internal alert | SMS or call tree | TMS |
| `route_deviation_confirmed` | Ops, supervisor, sometimes customer | Internal alert first | Customer push if material | TMS |
| `payment_failed` | Customer and finance | In-app and email | SMS for blocked flow | OMS and FIN |
| `topay_consent_pending` | Consignee | WhatsApp or SMS | Call-center path if unresolved | OMS |
| `pod_uploaded` | Customer and finance | Push and email | In-app only if low urgency | TMS and FIN |
| `settlement_on_hold` | Provider and finance | In-app and email | Ops alert | FIN |

## Delivery Rules

| Rule | Meaning |
|------|---------|
| Push first for app-active users | Fastest low-friction path for routine operational updates |
| WhatsApp or SMS for action-required flows | Better for time-sensitive responses |
| Email for durable records | Best for invoices, POD copies, policy-heavy messages |
| In-app for timeline continuity | Keeps order history visible and replayable |
| Internal alerting separate from customer messaging | Ops and supervisor alerts should not depend on consumer channels |

## Retry and Deduplication

- Every notification attempt should carry an idempotency key or deterministic message key.
- Repeated ETA micro-changes should be batched or thresholded rather than sent individually.
- A failed push should not produce duplicate SMS and WhatsApp sends without policy control.
- Retry policy should be channel-specific and severity-aware.

## Acknowledgement Rules

| Event Class | Ack Required |
|-------------|--------------|
| Informational | No |
| Action required | Yes when the flow depends on user response |
| SLA risk | Internal acknowledgement by ops or supervisor |
| Financial critical | Finance or operator acknowledgement |
| Safety or fraud critical | Immediate internal acknowledgement and escalation |

## Audit Requirements

- Log `queued`, `sent`, `delivered`, `read`, `failed`, `suppressed`, and `escalated` states where channel support exists.
- Preserve actor, event source, recipient type, channel, template key, and message key.
- Mask or minimize PII in analytics surfaces while retaining enough audit value for dispute review.

## Still Important to Improve

- Explicit quiet-hours and region-aware messaging rules
- Channel preference and consent model per audience
- Template library with placeholders, localization, and compliance wording
- Escalation timers for unacknowledged customer and consignee actions
- Notification suppression rules during incident storms

## Related Notes

- [[Communication Agent]]
- [[Order Lifecycle]]
- [[Customer App Frontend Architecture]]
- [[Driver App Frontend Architecture]]
- [[Operational Observability Architecture]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[AI Agents Hub]]
- [[Customer Problems Hub]]
