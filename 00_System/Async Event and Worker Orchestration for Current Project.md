---
type: memo
domain: backend
scope: async_orchestration
status: active
last_updated: 2026-05-31
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Backend Structure for Current Project]]"
  - "[[API and Event Contract for Current Project]]"
tags:
  - async
  - celery
  - events
  - workers
  - source-of-truth
  - current-project
source_files:
  - "C:\\Users\\user\\Downloads\\CELERY -EVENT.txt"
---

# Async Event and Worker Orchestration for Current Project

## Purpose

This note extracts the durable event-driven worker ideas from `CELERY -EVENT.txt` and aligns them to the current Zippy build.

The source contains Django-specific implementation examples.

The durable current-project idea is:

```text
workers orchestrate
but the transition gateway remains the only lifecycle authority
```

## Authority Status

This note is the canonical async orchestration note for the active current project.

It defines how background workers, event dispatch, retries, and failure handling should behave.

Stack-specific examples from older drafts are supporting context only unless they fit the current FastAPI-aligned backend reality.

## Current Runtime Interpretation

For the current project, Celery is the preferred first async worker runtime.

Use it for:

- notifications
- timeout and expiry handling
- workflow follow-up tasks
- route, score, and refresh jobs
- replay-safe orchestration after accepted transitions

If Kafka or another event bus is introduced, treat it as an event transport or analytics feed, not as a replacement for backend workflow truth.

The improved backend design adds a reliability spine that should be adopted in the current FastAPI interpretation:

```text
accepted database write
-> transactional outbox row
-> publisher emits to Redis Streams/Kafka or worker queue
-> consumer handles idempotently
-> consumer requests legal follow-up transition if needed
```

## Core Principle

Workers must never mutate lifecycle state directly.

Workers may:

- request legal transitions
- emit durable events
- trigger notifications
- schedule retries
- enrich analytics feeds

Workers must not:

- bypass policy rules
- set lifecycle state outside the transition gateway
- create duplicate finance or settlement outcomes
- invent success after partial failure

## Orchestration Rule

The safe async pattern is:

```text
accepted transition or approved workflow action
-> emit durable event
-> dispatch worker
-> worker performs side work
-> worker requests next legal transition if needed
-> backend validates that request through the same gateway
```

## Canonical Worker Discipline

### 1. One Transition Gateway

All worker-driven lifecycle requests must pass through the same transition service or endpoint used by APIs and operators.

Required inputs:

- `new_state`
- `event`
- `actor_role`
- `actor_id` where relevant
- `idempotency_key`
- optional `reason`
- optional `evidence_ref`

### 2. Durable Event First

Important workflow actions should write durable event records before or alongside downstream orchestration.

Use event rows for:

- replay and audit
- retry safety
- analytics feed
- ops troubleshooting

For actions that mutate business state, write the domain row and outbox message in the same database transaction. A publisher should send only committed outbox rows and mark delivery status separately.

### 3. Safe Retry

Every async step should be safe to replay.

Minimum rules:

- duplicate idempotency key must not duplicate lifecycle change
- duplicate payout, invoice, alert, or notification must be blocked where harmful
- exhausted retries must land in a visible failure bucket

Outbox and worker idempotency:

- outbox message id must be stable
- consumer idempotency key must include event type and entity id
- duplicate publish must not duplicate payment, invoice, settlement, notification, assignment, or state transition
- negative idempotency can preserve repeatable validation failures for command retries

### 4. Ordered Ownership

Recommended ownership shape:

- OMS-owned workers for order gating and workflow kickoff
- IMS-owned workers for match discovery and assignment preparation
- TMS-owned workers for telemetry interpretation, alerts, and trip-side automation
- FIN-owned workers for finance follow-ups, invoice generation, and settlement preparation

Workers coordinate domains.

They do not replace domain services.

## Recommended First-Pass Worker Set

For current project scope, prioritize:

1. notification dispatch workers
2. timeout and expiry workers
3. event fan-out workers
4. route or score refresh workers
5. bounded workflow follow-up workers

Do not make AI-agent orchestration the first async dependency.

## Failure Handling Rules

Every important worker path should define:

- retry policy
- terminal failure visibility
- owner of investigation
- replay method

Minimum failure classes:

- transient infrastructure failure
- downstream dependency failure
- invalid state or policy rejection
- duplicate or replay conflict

## Observability Requirements

Track at minimum:

- queue latency
- task execution latency
- retry count
- dead-letter count or equivalent
- workflow follow-up failure count
- policy rejection count for worker-requested transitions

Worker logs should include:

- `trace_id`
- `idempotency_key`
- `event`
- `worker_name`
- `order_id`, `trip_id`, or `finance entity id` where relevant

Trace context should move across:

- HTTP request
- outbox row
- event bus message
- Celery task
- agent action request
- supervisor policy check
- audit/event record

Use `trace_id`, `request_id`, `idempotency_key`, and source app/agent fields consistently so Admin Harness Monitor can correlate frontend, backend, worker, and agent behavior.

## Agent-Orchestration Boundary

Workers may call agent APIs for recommendation or classification, but agents do not become worker authority.

Safe pattern:

```text
worker loads backend context
-> calls agent recommendation endpoint
-> records recommendation event
-> calls supervisor policy check when high-risk
-> requests legal backend command if approved
```

Unsafe pattern:

```text
worker or agent writes order/payment/settlement state directly
```

Long-running orchestrators such as Temporal can be introduced later for complex assignment, payment, settlement, or dispute workflows, but they must follow the same gateway, outbox, idempotency, and audit rules.

## Relationship To Event Contract

This note does not replace [[API and Event Contract for Current Project]].

Use that note for:

- canonical event envelope
- lifecycle transition contract
- resource families

Use this note for:

- worker behavior
- async orchestration boundaries
- retry and failure discipline

## Relationship To Backend Structure

Implement async logic under the backend event and worker layers described in [[Backend Structure for Current Project]].

Current recommended shape:

```text
services/
events/
workers/
```

Service layer owns workflow meaning.

Worker layer owns deferred execution and retries.

## First-Pass Bottom Line

The current project should use event-driven workers to improve reliability and autonomy, but:

```text
workers are helpers
not workflow truth
```

That is the rule that keeps Celery useful without turning it into a hidden source of business authority.
