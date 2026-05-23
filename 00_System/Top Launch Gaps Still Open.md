---
type: memo
domain: execution
scope: launch_gaps
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[MVP Build Contract for Current Project]]"
  - "[[MVP Build Order]]"
tags:
  - launch
  - gaps
  - execution
  - current-project
---

# Top Launch Gaps Still Open

## Purpose

This note turns the current project canon into one practical launch-priority checklist.

It does not redefine product strategy.

It shows the highest-value missing pieces that still block:

- safe pilot launch
- workflow-complete MVP execution
- confident application build sequencing

Use this note with:

- [[MVP Build Contract for Current Project]]
- [[MVP Build Order]]
- [[Backend Gap Analysis Against Current Target]]
- [[Testing and Verification Strategy for Current Project]]
- [[Async Event and Worker Orchestration for Current Project]]

## Bottom Line

The current project is strong enough to build and pilot.

It is not yet launch-ready for live business operations without founder-heavy manual support.

The main issue is not idea quality.

The main issue is that the documented workflow is ahead of the implemented workflow.

## Launch Gap Ranking

Rank gaps by how directly they block one real shipment from moving safely:

1. canonical order-to-settlement workflow completion
2. role and identity implementation
3. trip execution and POD flow
4. finance visibility and settlement traceability
5. workflow-safe frontend surfaces
6. async orchestration with guardrails
7. workflow-first test coverage
8. observability and ops control
9. production hardening and compliance basics
10. pilot operations playbook and manual fallback

## 1. Canonical Order-To-Settlement Workflow Completion

Current gap:

- the vault canon expects booking -> payment gate -> matching -> assignment -> trip -> POD -> invoice visibility -> settlement visibility
- the implemented backend still behaves more like a shorter load-order prototype

Why it matters:

- this is the core business promise
- every other launch step depends on a legal and complete workflow corridor

Build now:

- complete the single transition-gateway lifecycle
- add missing states for payment gate, trip progress, POD, invoice visibility, and settlement visibility
- persist order state events as first-class records

Done when:

- one shipment can move end to end with no manual hidden state edits

## 2. Role And Identity Implementation

Current gap:

- the canon defines customer, driver, ops, finance, and transport-company roles
- current implementation does not yet fully enforce that operational identity model

Why it matters:

- launch without role boundaries creates unsafe workflow access
- every surface depends on correct role-scoped actions

Build now:

- implement authentication and role-aware authorization
- model core user profiles needed for customer, driver, ops, and finance
- enforce transition permissions by role

Done when:

- each role can see and do only its MVP-safe actions

## 3. Trip Execution And POD Flow

Current gap:

- trip execution, delivery milestones, and POD handling are described in the canon
- they are not yet complete as a working backend-plus-frontend path

Why it matters:

- real logistics trust is won or lost during execution and proof of delivery

Build now:

- add trip and milestone records
- support driver-side pickup, in-transit, and delivery updates
- support POD upload, attachment, and visibility

Done when:

- ops and customer can see a clean delivery trail and final POD for a shipment

## 4. Finance Visibility And Settlement Traceability

Current gap:

- finance is central in the canon but still thin in the implementation
- payment intent, invoice visibility, and settlement state are not yet robust enough

Why it matters:

- you cannot run a logistics business safely if delivery is visible but money movement is ambiguous

Build now:

- add payment intent and payment status records
- add invoice and finance event records
- add settlement visibility states and blocker reasons

Done when:

- every shipment shows what was charged, what is pending, and what blocks settlement

## 5. Workflow-Safe Frontend Surfaces

Current gap:

- frontend notes are detailed, but live production-grade user surfaces are not yet complete

Why it matters:

- an MVP is only real when customer, driver, and ops can execute the workflow themselves

Build now:

- customer booking and tracking surface
- driver execution and POD surface
- ops control-tower surface

Done when:

- the three core roles can complete the MVP corridor without dev-tool intervention

## 6. Async Orchestration With Guardrails

Current gap:

- Celery direction is now clear, but the worker layer still needs real implementation discipline

Why it matters:

- launch pain often appears in reminders, retries, expiries, and follow-up jobs
- unsafe workers can silently corrupt workflow truth

Build now:

- add worker queues for notification, timeout, refresh, and finance follow-up jobs
- keep workers behind the transition gateway
- add retry, dead-letter, and idempotency rules

Done when:

- background jobs help operations without secretly mutating lifecycle truth

## 7. Workflow-First Test Coverage

Current gap:

- testing direction is now strong in the vault
- implemented coverage still needs to prove real business safety

Why it matters:

- launch should be blocked by workflow failures in test, not discovered in customer shipments

Build now:

- transition policy tests
- API contract tests
- worker-requested-transition tests
- end-to-end corridor tests
- finance and idempotency failure-path tests

Done when:

- the MVP corridor survives both happy path and controlled failure-path verification

## 8. Observability And Ops Control

Current gap:

- the canon expects event visibility, blocker queues, and operational supervision
- implementation support is still incomplete

Why it matters:

- live operations fail slowly when no one can see stuck jobs, delayed trips, or settlement blockers

Build now:

- shipment event timeline
- worker/job status visibility
- ops exception queue
- alerting for stuck transitions and missing POD

Done when:

- ops can detect and recover from workflow exceptions early

## 9. Production Hardening And Compliance Basics

Current gap:

- architecture and compliance intent exist, but launch basics still need concrete execution

Why it matters:

- pilot users will trust the system only if reliability and policy basics are visible

Build now:

- migration discipline
- environment separation
- audit logging
- document retention rules
- basic role, data, and action traceability

Done when:

- pilot operations can be explained, audited, and recovered safely

## 10. Pilot Operations Playbook And Manual Fallback

Current gap:

- the product vision is strong, but live launch still needs a human operations script

Why it matters:

- first launch should be resilient even when software is incomplete

Build now:

- founder-led pilot SOP for booking, assignment, issue handling, POD chasing, and settlement follow-up
- manual fallback rules for every critical workflow stage
- launch-day support checklist

Done when:

- the team can run the first corridor safely even if some automation still needs manual support

## Recommended Build Order

Follow this order:

1. complete canonical workflow and transition model
2. implement role and identity enforcement
3. build trip execution and POD path
4. build finance visibility and settlement traceability
5. ship customer, driver, and ops MVP surfaces
6. add Celery workers for reminders, expiry, and follow-up
7. deepen workflow-first testing
8. add ops observability and exception handling
9. harden production and compliance basics
10. run founder-assisted pilot before broader launch

## Launch Readiness Rule

Do not call the project launch-ready until these are all true:

- one shipment can move from booking to POD with legal state transitions
- payment, invoice, and settlement visibility are traceable
- customer, driver, and ops can complete the corridor in their own surfaces
- workers assist workflow without becoming hidden business authority
- failure-path testing proves the corridor is resilient
- ops can detect and recover from stuck or broken workflow states

## Practical Interpretation

This means the next best move is not broad feature expansion.

It is disciplined closure of the MVP corridor until one real operating loop is trustworthy.
