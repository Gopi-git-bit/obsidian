---
type: memo
domain: execution
scope: sprint_plan
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Top Launch Gaps Still Open]]"
  - "[[MVP Build Order]]"
tags:
  - sprint
  - phase-1
  - execution
  - current-project
---

# Phase 1 Build Sprint Plan

## Purpose

This note turns the launch-gap order into the first practical build sprint for the active project.

Phase 1 is not a full MVP delivery sprint.

Phase 1 is the sprint that makes the MVP corridor buildable, testable, and safe to extend.

Use this note with:

- [[Top Launch Gaps Still Open]]
- [[MVP Build Contract for Current Project]]
- [[MVP Build Order]]
- [[Backend Structure for Current Project]]
- [[Testing and Verification Strategy for Current Project]]

## Phase 1 Outcome

At the end of Phase 1, the project should have one trustworthy backend workflow spine:

```text
order
-> quote
-> payment intent
-> confirmation gate
-> matching
-> assignment
-> trip start
-> pickup
-> in-transit
-> delivery
-> POD recorded
-> settlement visibility updated
```

The goal is not full polish.

The goal is to make this corridor real, enforceable, and test-covered.

## Phase 1 Scope

This sprint directly addresses the first four launch gaps:

1. canonical order-to-settlement workflow completion
2. role and identity implementation
3. trip execution and POD flow
4. finance visibility and settlement traceability

It begins the next three:

5. workflow-safe frontend surfaces
6. async orchestration with guardrails
7. workflow-first test coverage

## Sprint Priorities

### Priority 1: Lock Workflow Authority

Build:

- one transition gateway for lifecycle changes
- legal state map for the MVP corridor
- event persistence for accepted transitions
- idempotency key handling for transition-triggering APIs

Why first:

- all other work becomes fragile if workflow truth is not centralized

Done when:

- no endpoint, worker, or manual shortcut can mutate shipment lifecycle outside the gateway

### Priority 2: Add Core Identity And Role Enforcement

Build:

- authentication entry path
- role model for customer, driver, ops, and finance
- authorization checks on state-changing actions
- role-scoped read visibility for key records

Why now:

- booking, execution, and finance visibility all depend on actor boundaries

Done when:

- each core action is traceable to a permitted role

### Priority 3: Build Trip Execution Backbone

Build:

- trip record
- trip milestone/event record
- assignment record if still incomplete
- driver-executable updates for start, pickup, in-transit, delivery

Why now:

- this creates the operational heart of the shipment loop

Done when:

- the system can represent one real trip from assignment through delivery

### Priority 4: Add POD And Finance Visibility Backbone

Build:

- POD metadata record and attachment reference
- payment intent and payment status records
- invoice visibility record
- settlement visibility state and blocker reason

Why now:

- the MVP promise ends in closure visibility, not only in physical movement

Done when:

- ops and customer can tell whether the order is delivered, documented, invoiced, and settlement-ready

### Priority 5: Ship Minimal MVP API Corridor

Build these APIs first:

- create order
- get quote or estimate
- initiate payment intent
- confirm order after payment gate
- match and assign provider or driver
- fetch active trip
- post milestone update
- record POD metadata
- fetch tracking view
- fetch ops exception or status view

Why now:

- this is the smallest backend interface that makes real product surfaces possible

Done when:

- one shipment can be operated through APIs without hidden admin edits

### Priority 6: Start Minimal Frontend Surfaces

Build only the minimum thin surfaces needed to exercise the corridor:

- customer: booking, quote, order status
- driver: assignment, active trip, milestone update, POD upload
- ops: active shipment list, stuck order list, settlement blocker visibility

Why only thin surfaces:

- we need workflow proof, not polish-heavy product expansion

Done when:

- each core role can complete its happy-path task without developer tooling

### Priority 7: Add Safe Worker Assistance

Build:

- Celery queue wiring
- notification jobs
- expiry or reminder jobs
- retry-safe follow-up workers for finance and POD chasing

Guardrail:

- workers may request legal actions, but may not own lifecycle truth

Done when:

- background jobs assist operations without bypassing policy or duplicating outcomes

### Priority 8: Prove Workflow Safety In Tests

Build tests for:

- lifecycle transition legality
- role-gated action safety
- idempotency replay
- worker-requested transition discipline
- end-to-end MVP corridor
- finance visibility and settlement blocker behavior

Done when:

- the corridor passes both happy-path and key failure-path checks

## Suggested Sprint Sequence

Work in this sequence:

### Track A: Backend Truth

1. transition gateway
2. state model and event log
3. role permissions
4. trip and milestone models
5. POD and finance visibility models

### Track B: Backend Interfaces

6. critical APIs for order, payment, matching, trip, POD, and tracking
7. ops status and exception visibility APIs

### Track C: Worker Support

8. Celery wiring
9. notification and timeout jobs
10. retry and failure capture path

### Track D: Thin Frontends

11. customer happy-path view
12. driver execution view
13. ops supervision view

### Track E: Verification

14. policy tests
15. API contract tests
16. event and worker tests
17. end-to-end corridor tests

## Explicitly Out Of Scope For Phase 1

Do not let these distract the sprint:

- broad multi-city expansion
- warehouse or inventory workflows
- advanced BI polish
- deep transport-company multi-role complexity
- advanced autonomous agent behavior
- nationwide optimization logic

## Phase 1 Exit Criteria

Phase 1 is successful only when all of these are true:

- one corridor shipment can move from order to POD with legal transitions
- payment intent and settlement visibility are present
- driver milestones are recorded through the intended path
- POD is attached to the shipment record
- customer, driver, and ops each have a minimal usable interface
- background jobs assist but do not bypass workflow authority
- automated tests prove the corridor is safe enough for founder-assisted pilot use

## Team Rule

If a task does not strengthen the order-to-settlement corridor, defer it unless it removes a direct blocker for that corridor.

## Practical Next Step

Start Phase 1 by implementing the transition gateway, the event log, and the missing MVP corridor states before building more UI breadth.
