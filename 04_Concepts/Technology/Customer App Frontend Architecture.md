---
type: concept
domain: technology
decision_value: high
status: evergreen
related_hubs:
  - Technology Stack Hub
  - Operations Strategy Hub
  - Customer Problems Hub
tags:
  - concept
  - frontend
  - mobile
  - customer
  - architecture
---

# Customer App Frontend Architecture

## Definition

The application architecture pattern for the customer-facing mobile app, focused on state-safe order handling, offline resilience, auditability, and real-time order visibility.

## Why It Matters

- The customer app is the commercial front door for booking and payment.
- Weak frontend boundaries can break state integrity even if backend rules are correct.
- Connectivity constraints in Indian operating conditions make offline behavior a product requirement, not a nice-to-have.

## Core Principles

1. The frontend never mutates order state directly.
2. All mutations must be idempotent and retry-safe.
3. Local validation may guide the user but backend remains authoritative.
4. Offline drafts should survive app restarts and reconnect cleanly.
5. Important UI actions should be logged for compliance and operations review.

## Key Architecture Pattern

| Layer | Responsibility |
|-------|----------------|
| React components | Present booking, tracking, payment, and issue-reporting flows |
| Custom hooks | Encapsulate queries, transitions, retries, polling, and websocket handling |
| API SDK | Frozen contract for read and transition APIs |
| Local persistence | Draft storage, retry queue, and reconnect sync |
| Realtime layer | WebSocket first, polling fallback |

## Non-Negotiable Guardrails

- Use transition APIs for lifecycle changes.
- Attach idempotency keys to all write operations.
- Keep payment fallback order explicit and visible.
- Treat ToPay consent as a separate status flow with timeout handling.
- Keep pricing, driver assignment, and approval logic out of the UI layer.

## Operational Features

| Feature | Why It Exists |
|---------|---------------|
| Offline draft persistence | Protect bookings during weak connectivity |
| WebSocket plus polling fallback | Maintain visibility when realtime channels fail |
| Audit event logging | Support compliance, dispute review, and debugging |
| Feature flags | Gradual rollout of risky flows such as consent changes |
| Error boundaries | Keep failures recoverable without silent data loss |

## Decision Impact

- Strengthens [[Order Lifecycle]]
- Supports [[Fallback & Resilience Architecture]]
- Improves customer trust for [[MSME Owner Persona]]
- Reduces booking abandonment under unstable network conditions

## Risks

- Duplicate submissions if idempotency is weak
- Consent race conditions in ToPay flows
- Draft corruption if offline sync is not transactional
- UX confusion if backend-authoritative state is not reflected clearly

## Related Notes

- [[Order Lifecycle]]
- [[Logistics SLA]]
- [[Fallback & Resilience Architecture]]
- [[MSME Owner Persona]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
- [[Customer Problems Hub]]

