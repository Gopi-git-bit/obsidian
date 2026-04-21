---
type: concept
domain: technology
decision_value: high
status: evergreen
related_hubs:
  - Technology Stack Hub
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - concept
  - frontend
  - mobile
  - driver
  - architecture
---

# Driver App Frontend Architecture

## Definition

The application architecture pattern for the driver-facing mobile app, focused on state-safe assignment handling, field-grade offline resilience, fraud-resistant proof capture, and auditable operational actions.

## Why It Matters

- Drivers operate under variable network quality, time pressure, and high fraud sensitivity.
- Small UI mistakes in assignment or POD flows can create costly downstream operational errors.
- The driver app is a critical execution surface for TMS and settlement workflows.

## Core Principles

1. The app never changes assignment or order state directly.
2. All driver mutations must be idempotent and replay-safe.
3. Offline capture must preserve intent until backend acknowledgement succeeds.
4. POD and document flows must prioritize evidence integrity over speed.
5. Driver permissions should reflect ownership and authorization scope.

## Key Architecture Pattern

| Layer | Responsibility |
|-------|----------------|
| React Native components | Present assignments, navigation, scans, POD, and earnings flows |
| Custom hooks | Encapsulate assignment queries, response actions, realtime updates, and queue sync |
| API SDK | Frozen contract for assignment, order-read, transition, and evidence APIs |
| Local persistence | Offline action queue, reconnect sync, and temporary evidence state |
| Realtime layer | WebSocket first, polling fallback, queued retry for weak network |

## Non-Negotiable Guardrails

- Use assignment-response and transition APIs rather than direct state mutation.
- Attach idempotency keys to every operational write.
- Treat "Later" as explicit snooze logic with TTL and re-offer rules.
- Gate advance release and POD progress on verifiable evidence checks.
- Keep assignment authority, payment release, and fraud decisions on the backend.

## Operational Features

| Feature | Why It Exists |
|---------|---------------|
| Offline assignment queue | Preserve driver intent during network drop |
| Realtime plus polling fallback | Maintain awareness of assignment status changes |
| POD evidence capture | Protect settlement and dispute workflows |
| Driver audit logging | Support compliance, fraud review, and appeals |
| Feature flags | Stage risky controls such as fraud checks and offline sync changes |

## Decision Impact

- Strengthens [[Driver Assignment Logic]]
- Supports [[Proof of Delivery]]
- Improves execution quality for [[Transportation Agent]]
- Reduces failed field actions under weak connectivity

## Risks

- Duplicate assignment responses if replay safety is weak
- False POD confidence if metadata validation is absent
- Authorization leakage across multiple vehicles or driver roles
- Field frustration if offline sync behavior is unclear

## Related Notes

- [[Proof of Delivery]]
- [[Driver Assignment Logic]]
- [[Transportation Agent]]
- [[Fallback & Resilience Architecture]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]

