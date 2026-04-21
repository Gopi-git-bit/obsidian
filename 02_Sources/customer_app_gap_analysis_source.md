---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline customer app architecture brief
notes: Customer app gap analysis and architectural refinements for state safety, idempotency, ToPay consent, offline resilience, and auditability
---

# Customer App Gap Analysis Source

## Overview

This source refines the Zippy customer app architecture around:

- strict frontend alignment with the locked state machine
- idempotent mutation handling
- explicit ToPay consent flow control
- offline-first draft persistence and retry-safe sync
- audit-ready UI event logging
- agent-boundary enforcement between UI and backend orchestration

## Core Takeaways

### 1. The Frontend Is Not a Decision Engine

- The customer app must not price, assign, or mutate workflow state directly.
- All state changes should flow through transition APIs.
- UI logic may suggest or validate locally, but backend remains authoritative.

### 2. Booking and Payment Need Replay Safety

- Idempotency keys must travel with every mutation.
- Payment retries need a defined cascade and duplicate-click protection.
- Consent and payment timeouts must have explicit operational outcomes.

### 3. ToPay Flow Is a Separate Control Problem

- Consignee consent has its own lifecycle, timeout, and cancellation behavior.
- Frontend should observe consent status, not infer final order state locally.

### 4. Offline Capability Is Business-Critical

- Tier-2 and Tier-3 connectivity requires local draft persistence and later sync.
- Reconnect behavior should be intentional, auditable, and retry-safe.

### 5. UI Events Matter Operationally

- Customer-side actions such as retries, damage reports, and draft recovery should emit audit events.
- Observability should include not just backend transitions but also important UX behavior.

## Derived Notes

- [[Customer App Frontend Architecture]]
- [[Order Lifecycle]]
- [[Logistics SLA]]
- [[Technology Stack Hub]]
- [[MSME Owner Persona]]

## Related Notes

- [[pricing_engine_architecture_source]]
- [[fallback_resilience_architecture_source]]
- [[claude_source_reference]]

