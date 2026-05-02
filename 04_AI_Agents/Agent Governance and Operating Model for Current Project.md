---
type: ai_agent
domain: governance
decision_value: High
status: active
related_hubs:
  - "[[AI Agents Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[Technology Stack Hub]]"
tags:
  - ai-agent
  - governance
  - operating-model
  - autonomy
  - policy
created: 2026-05-01
updated: 2026-05-01
---

# Agent Governance and Operating Model for Current Project

## Purpose

This note transforms the older `agent prd.txt` into a current-context governance note for the Zippy project.

It keeps the durable strategic value of the earlier draft:

- bounded autonomy
- role clarity
- escalation discipline
- event-based coordination

It removes or updates what no longer fits:

- frozen old agent inventory
- stack-specific orchestration assumptions
- old naming that does not match the current backend and database direction

## Core Principle

Agents are not the source of truth.

The source of truth is:

- the operational database
- deterministic business rules
- service-layer workflows
- auditable events

Agents help the platform:

- evaluate
- score
- recommend
- monitor
- explain
- escalate

Agents should not become a hidden replacement for backend logic.

## Current Agent Philosophy

The current project should use:

```text
backend services first
agent intelligence second
```

That means:

- core workflows must still function if agent logic is reduced or swapped
- agents should sit on top of stable services and policy modules
- pricing, matching, SLA, and finance rules remain deterministic

## Non-Negotiable Rules

## 1. Agents Must Not Bypass Operational Truth

Agents must not:

- write arbitrary state directly
- skip lifecycle transitions
- invent pricing formulas
- invent payment outcomes
- close disputes unilaterally
- override stored SLA policies without an approved control path

## 2. Agents May Operate Only Within Clear Boundaries

Agents may:

- analyze
- rank
- recommend
- summarize
- trigger approved workflows
- emit auditable events
- raise risk or escalation flags

## 3. Every Important Agent Action Must Be Traceable

Agent-originated actions should carry:

- `trace_id`
- `idempotency_key`
- `agent_code`
- `timestamp`
- `input reference`
- `output summary`

## Current Agent Set

The current project does not need the older frozen 6-agent or 7-agent inventory copied literally.

The agent set that best fits current scope is:

| Agent | Code | Main Role |
|---|---|---|
| Supervisor / Policy Agent | `SUP` | conflict resolution, policy escalation, workflow freeze |
| Order Coordination Agent | `OMS` | order evaluation, lifecycle guidance, workflow routing |
| Resource and Matching Agent | `IMS` | provider and vehicle matching, capacity compatibility, return-load suggestions |
| Transportation Agent | `TMS` | route, ETA, SLA risk, telemetry interpretation, control-tower support |
| Finance and Settlement Agent | `FIN` | settlement preparation, invoice and payment workflow support, finance exceptions |
| Dispute and Exception Agent | `DISPUTE` | dispute scoring, refund recommendations, evidence summarization |
| Communication Agent | `COMMS` | notifications, message drafting, status communication support |
| Administration / Oversight Agent | `ADMIN_OPS` | controlled overrides, audit support, policy review assistance |

## Why This Agent Set Fits Better

It aligns with:

- current backend structure note
- current operational schema
- existing AI-agent notes in `04_AI_Agents`
- current product scope across customer, driver, transport company, and ops workflows

## Agent Responsibilities

## 1. Supervisor / Policy Agent (`SUP`)

Responsibilities:

- detect policy conflicts
- detect illegal workflow recommendations
- arbitrate between agent outputs when they disagree
- escalate high-risk or ambiguous cases
- recommend workflow freeze when fraud, payment, or SLA risk is high

Allowed outputs:

- `policy_violation_detected`
- `agent_conflict_detected`
- `override_required`
- `workflow_freeze_recommended`
- `manual_review_required`

Forbidden:

- changing order or trip state directly
- issuing refunds
- changing quoted prices

## 2. Order Coordination Agent (`OMS`)

Responsibilities:

- validate order completeness
- guide order progression through lifecycle
- coordinate pricing, payment, matching, and SLA workflows
- create structured return-trip or follow-on opportunity suggestions when relevant

Allowed outputs:

- `order_validated`
- `quote_requested`
- `payment_required`
- `matching_requested`
- `order_cancellation_recommended`
- `return_trip_offer_recommended`

Forbidden:

- assigning vehicles directly
- changing finance records directly
- bypassing lifecycle and payment controls

## 3. Resource and Matching Agent (`IMS`)

Responsibilities:

- rank candidate vehicles and providers
- verify compatibility across vehicle, cargo, and lane constraints
- suggest return-load or triangle opportunities where policy allows
- surface inventory exhaustion and alternatives

Allowed outputs:

- `vehicle_match_recommended`
- `provider_match_recommended`
- `vehicle_search_failed`
- `capacity_mismatch_detected`
- `triangle_candidate_suggested`

Forbidden:

- accepting matches unilaterally
- applying discounts directly
- editing order commercial terms

## 4. Transportation Agent (`TMS`)

Responsibilities:

- support route planning
- interpret ETA and routing signals
- monitor SLA exposure
- interpret telemetry and raise deviation or halt alerts
- support control-tower operations

Allowed outputs:

- `trip_route_recommended`
- `eta_updated`
- `sla_risk_detected`
- `incident_detected`
- `driver_alert_detected`
- `backup_route_recommended`

Forbidden:

- reassigning vehicles outside approved workflows
- editing finance or pricing records
- resolving disputes

## 5. Finance and Settlement Agent (`FIN`)

Responsibilities:

- support settlement preparation
- validate finance workflow completeness
- classify invoice and payment exceptions
- recommend settlement holds when data is incomplete or risk is high

Allowed outputs:

- `payment_verification_required`
- `settlement_precheck_completed`
- `settlement_on_hold`
- `refund_execution_ready`
- `invoice_issue_detected`

Forbidden:

- approving disputes finally
- inventing refund percentages
- changing order lifecycle state directly

## 6. Dispute and Exception Agent (`DISPUTE`)

Responsibilities:

- assess dispute strength
- recommend refund or adjustment ranges
- summarize evidence
- explain why a case should be escalated, rejected, or partially compensated

Allowed outputs:

- `dispute_strength_score`
- `recommended_action`
- `recommended_refund_pct`
- `evidence_summary`
- `manual_review_required`

Forbidden:

- executing refunds
- closing disputes
- writing settlement records

## 7. Communication Agent (`COMMS`)

Responsibilities:

- prepare customer, driver, partner, and ops communications
- draft update notifications
- normalize status messages across channels
- support escalation messaging during SLA risk and incidents

Allowed outputs:

- `notification_draft_ready`
- `status_message_ready`
- `alert_message_ready`
- `customer_update_ready`

Forbidden:

- changing operational state
- suppressing incidents
- deciding commercial outcomes

## 8. Administration / Oversight Agent (`ADMIN_OPS`)

Responsibilities:

- assist admins and ops with review queues
- summarize anomalies, overrides, and repeated issues
- support governance and platform review workflows

Allowed outputs:

- `admin_review_summary`
- `override_context_ready`
- `incident_cluster_detected`
- `policy_gap_detected`

Forbidden:

- auto-approving unsafe overrides
- acting as a hidden superuser over the state machine

## Coordination Model

The current project should not assume direct agent-to-agent freeform behavior as the main architecture.

Preferred coordination model:

```text
API request or worker event
-> service-layer workflow
-> policy checks
-> agent evaluation where needed
-> event/log emission
-> persisted result
```

This means the main orchestrator remains backend workflow logic, with agents providing bounded intelligence.

## Event Expectations

Agents should work against the same operational event reality as the rest of the system.

Important event families:

- order events
- matching events
- trip and telemetry events
- payment and invoice events
- SLA risk and breach events
- alert and incident events

## Role Of Agents In Return-Trip And Triangle Logic

This is important in the current project.

Agents may:

- suggest return-load opportunities
- compare direct vs triangle options
- score candidate loops
- explain why a triangle is better or worse

Agents must not:

- make loop metadata override the core order state machine
- blend multiple orders into ambiguous settlement behavior
- treat refund logic as loop-level instead of order-level

## SLA And Promise Rules

Agents may:

- interpret lane risk
- compare planned vs promised windows
- raise risk before breach
- recommend backup actions

Agents must not:

- rewrite SLA policy records arbitrarily
- shrink delivery windows to make metrics look better
- claim a promise level not supported by service level and lane policy

## Finance Rules

Agents may:

- detect payment anomalies
- classify settlement blockers
- recommend holds
- prepare finance context for human or workflow action

Agents must not:

- invent tax logic
- change recorded payment status without verified system event
- override refunds or commissions outside approved paths

## Testing Requirements For Agent Behavior

Agent behavior should be tested as workflow behavior, not just prompt behavior.

Required test categories:

- illegal action prevention tests
- lifecycle boundary tests
- duplicate event replay tests
- pricing non-override tests
- dispute recommendation vs execution separation tests
- SLA escalation correctness tests
- alert classification tests

## What Survives Tool Or Model Changes

This note is designed so the governance model survives changes in:

- model provider
- orchestration framework
- workflow engine
- event transport
- backend deployment details

Because the durable truths are:

- clear domains
- bounded autonomy
- deterministic business rules
- auditability
- escalation discipline

## Relationship To Other Current Notes

Use this note with:

- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Zippy Logistics Operational Core Schema]]
- [[Corridor Matching Agent with PydanticAI]]
- [[Transportation Agent]]
- [[Payment Settlement Agent]]
- [[Platform Administration Agent]]

## Bottom Line

The current project should use agents as:

```text
bounded operational intelligence
on top of
stable backend workflows and auditable data
```

That is the version of the old agent PRD that still fits the project now.
