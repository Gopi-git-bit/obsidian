---
type: memo
domain: architecture
scope: autonomous_agent_integration
status: active
last_updated: 2026-06-01
related_hubs:
  - "[[02_Agentic_AI_Application]]"
  - "[[07_State_Machine]]"
  - "[[API and Event Contract for Current Project]]"
tags:
  - ai-agents
  - state-machine
  - idempotency
  - audit
  - api
  - orchestration
---

# Autonomous Agent Integration Blueprint

## Purpose

This note closes the architecture gaps between the external agent mapping/API PRD and the current vault notes. It should be used as the senior implementation contract for seamless autonomous integration.

The correct interpretation is:

- 5 core AI decision agents: Supervisor, Operations, Transport, Finance, RAG/Knowledge.
- Additional operational agents/services: IMS/RMA, Communication/Notification, Admin/Ops, OCR, pricing, telemetry, and worker runners.
- Only backend services mutate state. Agents recommend, request, validate, score, arbitrate, or trigger approved commands.

This prevents the system from being limited to "5 agents" while still preserving the 5-agent AI governance model.

## Non-Negotiable Integration Rules

1. Every lifecycle change goes through the locked transition gateway in [[07_State_Machine]].
2. Every state-changing API request and bus event must include `request_id`, `trace_id`, `idempotency_key`, `actor_id`, `actor_role`, `source_agent`, and `schema_version`.
3. Agents must never write directly to order, payment, settlement, vehicle, or ledger tables.
4. Supervisor policy checks are mandatory for settlement release, refund, manual override, fraud hold release, blacklisted driver handling, and high-risk document/POD outcomes.
5. Duplicate commands must return the original result when the payload hash matches, and must fail with conflict when the same key is reused with a different payload.
6. All autonomous decisions must be explainable with evidence references, model version, policy IDs, and deterministic fallback reason.
7. Human overrides are allowed only through audited admin commands, never by editing state directly.

## Canonical Agent Topology

| Layer | Component | Responsibility | Can Mutate State |
|---|---|---|---|
| Governance | Supervisor Agent | Policy checks, conflict arbitration, DLQ supervision, high-risk action approval | No, returns decision only |
| Lifecycle | Operations Agent | Order orchestration, lifecycle command preparation, customer-facing workflow | No, requests transitions |
| Mobility | Transport Agent | Assignment, ETA, telemetry, geofence, incident detection | No, requests transitions |
| Resource | IMS/RMA Service | Vehicle and driver inventory, candidate scoring, reservation locks | Yes, only reservation records through owned API |
| Finance | Finance Agent | Payment intent, webhook reconciliation, settlement preparation, payout request | No direct ledger mutation without Finance API command |
| Knowledge | RAG/OCR Agent | Rules retrieval, document intelligence, validation evidence | No |
| Messaging | Communication Agent | Push, SMS, WhatsApp, email, retry and delivery receipt tracking | Yes, only notification records |
| Admin | Platform Admin/Ops | Manual review, override workflow, compliance evidence | Yes, only through audited override APIs |

## Event Envelope

All event topics must use the same envelope.

```json
{
  "event_id": "uuid",
  "event_type": "order_confirmed",
  "schema_version": "2026-06-01",
  "occurred_at": "ISO-8601",
  "producer": "ops-agent",
  "source_agent": "OPS",
  "target_agent": "TMS",
  "entity_type": "order",
  "entity_id": "order_uuid",
  "request_id": "uuid",
  "trace_id": "uuid",
  "parent_trace_id": "uuid-or-null",
  "idempotency_key": "string",
  "payload_hash": "sha256",
  "actor_id": "system-or-user-id",
  "actor_role": "customer | driver | transport_company | admin | system | agent",
  "causation_event_id": "uuid-or-null",
  "correlation_id": "order-or-payment-correlation-id",
  "payload": {},
  "evidence_refs": [],
  "decision_reason": "short deterministic explanation"
}
```

Required storage:

- Raw event in append-only event log.
- Current read model updated by consumers.
- Audit row with payload hash and previous event hash for protected lifecycle events.
- OpenTelemetry span linked by `trace_id`.

## State Machine Contract

The order state machine remains the backbone:

```text
DRAFT
PAYMENT_PENDING
CONFIRMED
VEHICLE_SEARCH
DRIVER_ASSIGNED
ARRIVED_PICKUP
LOADING
ENROUTE
ARRIVED_DELIVERY
POD_UPLOADED
DELIVERY_COMPLETED
SETTLEMENT_PREPROCESS
SETTLEMENT_READY
SETTLEMENT_RELEASED
CLOSED
```

Operational holds are overlays, not lifecycle states. Examples:

- `topay_consent_pending`
- `document_verification_hold`
- `payment_mismatch_hold`
- `fraud_review_hold`
- `dlq_manual_review`
- `driver_no_show_recovery`

Each overlay must include:

- `hold_type`
- `hold_reason`
- `opened_by`
- `opened_at`
- `supervisor_policy_ids`
- `release_condition`
- `released_by`
- `released_at`
- `release_evidence_refs`

## Idempotency Model

Use three layers of idempotency.

| Layer | Key | Store | Window | Behavior |
|---|---|---|---|---|
| API command | `idempotency_key + route + actor_id` | Redis plus Postgres fallback | 24 hours minimum | Same payload returns same response; different payload returns conflict |
| Event consumer | `event_id` and `payload_hash` | Consumer inbox table | Permanent for lifecycle/finance, 30 days for notifications | Already processed event is acknowledged without reprocessing |
| External provider | Provider attempt ID plus internal command ID | Payment/document/provider ledger | Permanent | Webhook replay reconciles to existing attempt |

Database constraints required:

- Unique reservation key: `order_id + vehicle_id + reservation_status in active_statuses`.
- Unique payment attempt: `provider + provider_attempt_id`.
- Unique transition command: `order_id + idempotency_key`.
- Unique settlement release: `settlement_id + release_attempt_id`.

## API Structure

Use one public API gateway and internal service APIs.

```text
/v1/orders
/v1/orders/{order_id}/quote
/v1/orders/{order_id}/payment-intent
/v1/orders/{order_id}/transition
/v1/orders/{order_id}/hold
/v1/orders/{order_id}/resume
/v1/transport/assign
/v1/transport/reservations/{reservation_id}/confirm
/v1/finance/payment-intents
/v1/finance/webhooks/razorpay
/v1/finance/settlements/{settlement_id}/release
/v1/rag/query
/v1/rag/ocr/validate
/v1/supervisor/policy/check
/v1/supervisor/dlq/inspect
/v1/notifications/send
```

Required headers:

```text
Authorization
X-Request-Id
X-Trace-Id
Idempotency-Key
X-Schema-Version
```

Required state-changing response fields:

```json
{
  "request_id": "uuid",
  "trace_id": "uuid",
  "idempotency_key": "string",
  "status": "accepted | completed | held | rejected | conflict",
  "entity_id": "uuid",
  "current_state": "string",
  "decision_reason": "string",
  "audit_event_id": "uuid"
}
```

## Agent Interconnection Rules

Agents should communicate by events first and synchronous API only for policy gates, reservations, and payment/provider calls.

| From | To | Method | Contract |
|---|---|---|---|
| OPS | RAG | Sync or async | Validate address, cargo rules, pricing evidence, and policy citations |
| OPS | FIN | Sync command | Create payment intent or ToPay consent payment path |
| FIN | OPS | Event | Emit payment captured, failed, mismatch, refund status |
| OPS | IMS/RMA | Sync command | Request vehicle search and reservation |
| IMS/RMA | TMS | Event | Emit reserved vehicle and assignment candidate |
| TMS | OPS | Event | Emit driver assigned, geofence arrivals, loading, enroute, delivery events |
| TMS | SUP | Event or sync | Escalate no-show, GPS loss, route deviation, breakdown |
| FIN | SUP | Sync | Request approval before settlement, refund, rollback, or high-risk release |
| RAG/OCR | SUP | Event | Escalate document mismatch, low confidence, missing evidence |
| Any agent | COMMS | Event | Request notification through template and channel policy |
| Any failed consumer | SUP | Event | Push DLQ summary with trace and replay eligibility |

## Autonomous Recovery Playbooks

The application should recover without human action when the next action is deterministic and low risk.

| Failure | Autonomous Response | Human Review Trigger |
|---|---|---|
| Driver reject or timeout | Offer next candidate, then expand radius, then transport company pool | Candidate exhaustion |
| Reservation conflict | Retry next candidate with new reservation command | Repeated conflicts above threshold |
| GPS signal lost | Notify driver, fallback to last known ETA, monitor heartbeat | No signal beyond configured threshold |
| Payment webhook replay | Deduplicate by provider attempt ID and reconcile status | Payment status mismatch |
| POD OCR low confidence | Request clearer upload and hold settlement | Fraud indicators or repeated mismatch |
| Notification failure | Retry alternate channel based on preference | Critical notification undelivered after retries |
| DLQ spike | Pause non-critical replay, alert Supervisor, group errors by schema/error code | Finance, fraud, or malformed lifecycle event in DLQ |

## Audit Logging

Audit logs must answer: who acted, what changed, why it changed, which policy allowed it, and how to replay or dispute it.

Required audit fields:

- `audit_event_id`
- `entity_type`
- `entity_id`
- `event_type`
- `from_state`
- `to_state`
- `actor_id`
- `actor_role`
- `source_agent`
- `request_id`
- `trace_id`
- `idempotency_key`
- `payload_hash`
- `prev_hash`
- `chain_hash`
- `policy_ids`
- `model_name`
- `model_version`
- `prompt_version`
- `confidence`
- `evidence_refs`
- `decision_reason`
- `created_at`

Finance, settlement, refund, cancellation fee, POD, and admin override events must be immutable and retained permanently.

## Implementation Checklist

- Create shared JSON Schema files for the event envelope and command metadata.
- Enforce `Idempotency-Key`, `X-Request-Id`, and `X-Trace-Id` at the API gateway.
- Add a command inbox/outbox table for each state-changing service.
- Add consumer inbox tables for each async worker.
- Make order transition service the only writer for `orders.state`.
- Use the transactional outbox pattern when a DB change must emit an event.
- Store policy files and prompt templates with versions.
- Add contract tests for duplicate commands, duplicate events, payload hash mismatch, reservation conflict, webhook replay, DLQ replay, and illegal state transitions.
- Add dashboards for state transition latency, assignment SLA, payment reconciliation, DLQ depth, policy holds, notification delivery, and agent confidence distribution.

## Gap Decisions

1. Do not collapse all operational roles into the 5 AI agents. Keep 5 AI decision agents and separate deterministic services for inventory, notifications, OCR, telemetry, and workers.
2. Do not allow LLM output to be an executable command by itself. It must be schema-valid, policy-checked, and persisted by backend APIs.
3. Do not treat holds as state-machine jumps. Holds are overlays with explicit release evidence.
4. Do not rely only on Redis for idempotency. Redis can be the fast path, but Postgres must hold protected lifecycle and finance idempotency records.
5. Do not make audit logging optional. Audit is part of the product architecture, not only an ops feature.
