---
type: memo
domain: backend
scope: architecture
status: active
last_updated: 2026-05-31
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[AI Agents Hub]]"
  - "[[Operations Strategy Hub]]"
tags:
  - backend
  - architecture
  - fastapi
  - operational-core
---

# Backend Structure for Current Project

## Purpose

This note extracts the backend structure that still fits the current Zippy project from the older `backend.txt` PRD.

It intentionally ignores unstable choices such as:

- specific LLM assignments
- old Django-only service shapes when they conflict with the current FastAPI repo
- agent orchestration details that no longer match the current codebase

It aligns instead to:

- the current FastAPI backend on disk
- the refined operational core schema
- the current corridor-first logistics platform scope

## Current Backend Reality

The current backend is best understood as:

```text
FastAPI application
-> route modules for core operational flows
-> SQLAlchemy models and schemas
-> service layer for pricing and routing logic
-> PostgreSQL-oriented operational and analytics data model
```

Current implemented API areas visible in the repo:

- health
- vehicles
- pricing
- orders
- matches
- bids
- ML pricing
- routing

This means the old backend PRD should be treated as a source of design ideas, not as the current implementation truth.

The improved backend design should be absorbed as a reliability and integration layer, not as a framework switch. Where that source says "Django", the current project translates the idea into FastAPI route handlers, middleware, service modules, workers, and policy modules.

## Backend Mission In Current Project

The backend should support a vehicle-owner to consignor logistics platform focused on:

- order intake and validation
- pricing and quoting
- vehicle and provider matching
- trip execution and status tracking
- SLA-aware delivery commitments
- payment and invoice traceability
- operational alerts and control-tower workflows
- downstream analytics for lane reliability and return-trip intelligence

Use [[Current Project Navigation Hub]] as the top-level navigation note that connects this backend note to frontend, compliance, and source-of-truth notes.

## Recommended Backend Layers

## 1. API Layer

Purpose:

- expose stable endpoints for apps, admin tools, and internal workflows
- validate requests and responses
- keep business logic out of route handlers

Recommended route groups:

- `/health`
- `/auth` and `/users`
- `/vehicles`
- `/orders`
- `/matches`
- `/bids`
- `/pricing`
- `/routing`
- `/trips`
- `/payments`
- `/notifications`
- `/admin`
- `/agents`
- `/rag`
- `/supervisor`
- `/ops/harness`

Current repo already partially covers this through:

- `backend/app/api/orders.py`
- `backend/app/api/matches.py`
- `backend/app/api/bids.py`
- `backend/app/api/pricing.py`
- `backend/app/api/ml_pricing.py`
- `backend/app/api/routing.py`
- `backend/app/api/vehicles.py`

## 2. Application Service Layer

Purpose:

- hold business workflows
- coordinate transactional operations
- call pricing, routing, and matching logic
- emit operational events

Recommended service families:

- `order_service`
- `matching_service`
- `pricing_service`
- `routing_service`
- `trip_service`
- `payment_service`
- `notification_service`
- `sla_service`
- `alert_service`
- `agent_gateway_service`
- `audit_service`
- `idempotency_service`
- `supervisor_policy_service`

Important current-context refinement:

The old PRD used agent service classes as the main backend unit.

For the current project, the stronger shape is:

```text
application services first
agent wrappers second
```

That keeps the business logic usable even if the agent layer changes later.

## API Middleware And Request Discipline

All state-changing backend calls from frontend apps, agents, workers, webhooks, and admin tools should pass through the same request discipline:

- forwarded header and client context parsing
- request body size limits, with separate file-upload policy
- authentication through JWT for user apps and scoped service credentials for internal agents/workers
- optional HMAC signature and nonce replay protection for high-risk mobile, webhook, and service calls
- schema validation before service execution
- idempotency key validation for every mutation
- trace context propagation through `trace_id`, `request_id`, and W3C `traceparent` where available
- RBAC and policy guard checks before any lifecycle, finance, settlement, or admin action

Idempotency behavior:

- new key: create an `IN_PROGRESS` record and continue
- completed key: return the saved response
- in-progress key: return `409` or `202` with current processing status
- invalid repeated request: return the same cached validation error where feasible

This discipline must be shared by frontend commands and agent commands so agents cannot bypass the frontend/API contract.

## 3. Domain and Policy Layer

Purpose:

- encode deterministic rules
- protect core logistics decisions from free-form orchestration logic

Examples:

- order lifecycle transitions
- provider eligibility rules
- lane pricing rules
- SLA buffer rules
- backhaul and deadhead pricing adjustments
- payment hold policies
- cancellation rules

This layer should own the rules described in the vault, not the HTTP handlers.

## State Transition Gateway

The `new -chatgpt  (1).txt` source adds one strong implementation rule:

```text
there should be one legal path for order lifecycle transitions
```

Current FastAPI interpretation:

- expose a dedicated transition endpoint or service method
- reject direct state mutation from generic update endpoints
- require actor role, event name, idempotency key, and reason/context
- validate transition graph
- validate role permission
- write state event/audit record
- return authoritative updated state

Recommended external shape:

```text
POST /orders/{order_id}/transition
```

Recommended internal shape:

```text
order_service.transition_order(...)
```

Required payload fields:

- `new_state`
- `event`
- `actor_role`
- `actor_id`
- `idempotency_key`
- optional `reason`
- optional `evidence_ref`

The route handler should call the service/policy layer instead of implementing transition logic directly.

## Transition Ownership Rules

Suggested role ownership:

| Role | Allowed Lifecycle Area |
|---|---|
| OMS | order intake, quote, payment gate, confirmation, cancellation policy |
| IMS | matching and assignment requests |
| TMS | trip execution milestones and POD request |
| FIN | payment, invoice, settlement, closure-related finance steps |
| ADMIN | approved overrides, holds, exceptional closure |

Workers, AI agents, and frontend clients should request transitions through this same path.

They should not set order state directly.

## Realtime And Telemetry Rule

Realtime streams should never be command channels.

Use realtime for:

- order state changed event broadcast
- shipment event broadcast
- alert broadcast
- driver location broadcast

Do not use realtime for:

- transition commands
- payment confirmation
- settlement release
- admin override

Driver location is telemetry.

It can support ETA, map display, alerts, and audit.

It must not directly mutate order state.

## 4. Persistence Layer

Purpose:

- map the refined operational schema into code
- keep repositories or query helpers clean
- support both transactional workflows and analytics feeds

The persistent model should align to:

- `app_users`, `customer_accounts`, `driver_profiles`, `transport_companies`
- `vehicles`, `vehicle_availability_snapshots`
- `directed_lanes`, `lane_rate_bands`, `city_market_profiles`, `lane_pricing_signals`
- `orders`, `order_stops`, `order_documents`, `order_state_events`
- `order_bids`, `order_matches`
- `trips`, `trip_legs`, `shipment_events`
- `service_levels`, `sla_policies`, `order_sla_commitments`
- `payment_records`, `payment_intents`, `invoice_records`, `finance_events`
- `driver_alerts`, `incident_logs`, `notifications`

## 5. Event and Workflow Layer

Purpose:

- handle important operational transitions asynchronously where useful
- provide replay-safe traces
- support notifications, alerts, and analytics ingestion

Current-context guidance:

- keep event emission durable and simple
- use database state and event logs as the core truth
- treat background workers as helpers, not as the only source of business truth
- use a transactional outbox for accepted state changes and important side effects
- publish from outbox to Redis Streams, Kafka, or another event transport only after the database transaction commits
- propagate `trace_id`, `idempotency_key`, actor, and source service through every event

Current async orchestration note:

- [[Async Event and Worker Orchestration for Current Project]]

Important events:

- order created
- order validated
- quote generated
- payment initiated
- payment confirmed
- provider matched
- trip started
- shipment delayed
- SLA risk raised
- POD uploaded
- delivery completed
- settlement completed

Transactional outbox rule:

```text
domain write + event/outbox insert happen in one transaction
outbox publisher sends events asynchronously
consumers are idempotent and may request legal follow-up transitions
```

Do not let message-bus delivery become the only proof that a business action happened. The database row and event/audit row remain the source of truth.

## 5.1 Agent API Layer

Agents should interact with the backend through explicit APIs or internal service adapters, not direct table writes.

Recommended agent-facing API groups:

```text
POST /agents/{agent_code}/actions
GET  /agents/{agent_code}/context/{entity_type}/{entity_id}
POST /agents/{agent_code}/recommendations
POST /supervisor/policy/check
POST /rag/query
POST /rag/ocr/validate
```

Agent action requests must include:

- `agent_code`
- `actor_role`
- `actor_id` or service identity
- `entity_type`
- `entity_id`
- `requested_action`
- `decision_reason`
- `confidence` where applicable
- `trace_id`
- `idempotency_key`
- `evidence_refs`

Allowed agent outputs:

- recommendation
- risk flag
- policy check request
- notification draft
- transition request through the legal transition gateway
- settlement or payment hold recommendation

Forbidden agent outputs:

- direct state mutation
- direct money movement
- direct settlement release
- direct final invoice/payment status mutation
- unapproved admin override

Supervisor gate:

```text
high-risk agent output
-> /supervisor/policy/check
-> approve | hold | reject | manual_review_required
-> backend service applies only approved action paths
```

## Required Backend Safety Tests

Future implementation should include tests that try to break the workflow.

Minimum test set:

- valid transition succeeds
- illegal state skip is blocked
- role cannot transition outside its authority
- duplicate idempotency key is safe
- terminal state cannot move again
- generic update endpoint cannot edit lifecycle state
- direct model/state update cannot bypass guard where feasible
- worker-requested transition follows the same gateway
- frontend/realtime cannot create state changes
- audit/event row is written for every accepted transition
- idempotency replay returns the same response or safe in-progress status
- outbox publisher does not duplicate downstream side effects
- agent action API cannot mutate state outside the transition gateway
- supervisor policy hold blocks high-risk finance or lifecycle action
- frontend harness statuses match backend response payloads

These tests matter more than happy-path endpoint tests.

Current testing note:

- [[Testing and Verification Strategy for Current Project]]

## 6. Analytics Feed Layer

Purpose:

- convert operational traces into corridor and reliability intelligence

Outputs:

- lane delay events
- shipment delay facts
- lane performance aggregates
- pricing calibration inputs
- triangle and backhaul performance signals

## Backend Structure That Best Fits Current Project

Recommended module layout:

```text
backend/app/
  api/
  core/
  database/
  models/
  schemas/
  services/
  policies/
  events/
  repositories/
  workers/
  agents/
  middleware/
  observability/
```

Suggested responsibilities:

- `api/`: request handling and response models
- `core/`: settings, logging, security, shared utilities
- `database/`: engine, sessions, migrations glue
- `models/`: SQLAlchemy ORM models
- `schemas/`: Pydantic request and response contracts
- `services/`: business workflows
- `policies/`: deterministic decision rules
- `events/`: event emitters and consumers
- `repositories/`: query and persistence helpers where needed
- `workers/`: async jobs such as expiries, notifications, score refresh triggers
- `agents/`: agent adapters, context builders, recommendation persistence, and supervisor policy clients
- `middleware/`: auth, idempotency, request context, signature/nonce, trace context
- `observability/`: structured logging, metrics, tracing, Sentry/OTel setup

## How To Translate The Old Agent PRD

The old PRD contained useful role separation, but it should be translated into the current backend like this:

| Old PRD Idea | Current Backend Translation |
|---|---|
| Customer Service Agent | `order_service` + `notification_service` |
| Order Management Agent | `order_service` + `matching_service` + lifecycle policies |
| Resource Management Agent | `vehicle availability` + `matching` + `provider eligibility` services |
| Transportation Agent | `trip_service` + `routing_service` + `driver_alerts` |
| Payment Settlement Agent | `payment_service` + `finance_events` + invoice workflows |
| Admin / Supervisor Agent | `admin tools` + `incident_logs` + override policies |

Backend-to-agent translation must follow [[Agent Governance and Operating Model for Current Project]]:

```text
backend services decide and persist
agents recommend, score, summarize, or request approved actions
supervisor blocks unsafe actions
frontend renders backend truth
```

This preserves the intent without forcing the repo into an outdated agent runtime design.

## Required Core Backend Workflows

## 1. Order Intake Workflow

```text
create order
-> validate inputs
-> assign lane context
-> generate quote
-> create SLA commitment
-> move to payment pending or confirmed path
```

## 2. Matching Workflow

```text
load order context
-> fetch eligible vehicles/providers
-> apply deterministic filters
-> score and rank options
-> create bids or proposed matches
-> confirm assignment
```

## 3. Trip Execution Workflow

```text
create trip
-> create trip legs
-> ingest shipment events
-> update SLA risk state
-> raise driver alerts or incident logs when thresholds are breached
-> close trip on POD and delivery completion
```

## 4. Payment and Settlement Workflow

```text
create payment intent
-> confirm payment
-> record payment record
-> issue invoice
-> append finance events
-> close settlement
```

## 5. Pricing Workflow

```text
load lane pricing signals
-> apply deterministic cost floor
-> apply density, congestion, and backhaul logic
-> write quote breakdown
-> return explainable result
```

## 6. SLA Control Workflow

```text
derive service level
-> attach SLA policy
-> store order promise windows
-> monitor execution against commitment
-> raise risk or breach records
```

## Backend Enhancements That Match Current Context

These are the most useful enhancements to carry forward from the old PRD:

- clearer service boundaries
- explicit workflow coordination between orders, matching, transport, and finance
- durable event logs instead of hidden side effects
- strong admin and ops visibility
- role-aware workflow handling for transport companies acting as providers or customers
- mutation-wide idempotency with saved responses
- transactional outbox for event emission
- scoped internal agent APIs
- supervisor policy gate for high-risk actions
- trace context across APIs, workers, agents, and events
- structured audit records for state, finance, agent, and admin decisions
- frontend harness endpoints for event/state/SLA/verification/finance health

## Things To Avoid Carrying Forward Blindly

- Django-specific application structure as the canonical shape
- endpoint names from outside drafts when they conflict with [[API and Event Contract for Current Project]]
- agent-to-agent message buses as the only orchestration model
- model- or provider-specific assumptions
- backend complexity ahead of actual operational proof

## Recommended Near-Term Backend Priorities

1. Align ORM models to the refined operational core schema.
2. Introduce a real service layer around orders, matching, trips, payments, and SLA commitments.
3. Add trip, SLA, finance, and alert endpoints before adding more orchestration complexity.
4. Keep deterministic rules in policy modules so pricing, matching, and SLA logic remain stable.
5. Emit operational events that can feed analytics and reliability scoring.

## Bottom Line

The current project does not need the old backend PRD copied forward literally.

It does need the durable structure hidden inside that PRD:

- clear service boundaries
- deterministic workflow ownership
- event-backed logistics operations
- role-aware provider and customer handling
- pricing, SLA, and settlement as first-class backend concerns

That is the backend shape that best matches the current Zippy project.
