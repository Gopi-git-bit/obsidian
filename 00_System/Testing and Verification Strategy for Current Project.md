---
type: memo
domain: verification
scope: testing_strategy
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Backend Structure for Current Project]]"
  - "[[API and Event Contract for Current Project]]"
tags:
  - testing
  - verification
  - source-of-truth
  - current-project
source_files:
  - "C:\\Users\\user\\Downloads\\Testing phase.txt"
---

# Testing and Verification Strategy for Current Project

## Purpose

This note extracts the durable testing ideas from `Testing phase.txt` and aligns them to the current Zippy build.

The source contains stack-locked Django, Kafka, and infrastructure details.

The durable value is the testing discipline:

```text
verify workflow truth first
-> verify API contract
-> verify events and workers
-> verify observability and failure handling
```

## Authority Status

This note is the canonical testing and verification note for the active current project.

It defines what must be tested before the current project can be called workflow-safe.

Framework-specific examples from older drafts are supporting context only unless they fit the current FastAPI-aligned backend reality.

## Core Principle

Testing must focus on business workflow integrity, not only code presence or endpoint existence.

The highest-value failures to catch are:

- illegal lifecycle transitions
- broken idempotency
- worker bypass of policy
- missing audit/event rows
- finance or settlement drift
- observability blind spots during failure

## Verification Layers

## 1. Policy and Domain Tests

Verify deterministic rules directly.

Minimum coverage:

- valid transition succeeds
- illegal state skip is blocked
- role cannot transition outside its authority
- terminal state cannot move again
- pricing rule remains deterministic
- matching rule respects compatibility and policy gates
- settlement or finance policy does not bypass workflow ownership

## 2. API Contract Tests

Verify the builder-facing contract.

Minimum coverage:

- required fields rejected when missing
- transition endpoint requires `idempotency_key`
- generic update endpoints cannot mutate lifecycle state
- role-safe payload shape is preserved
- invalid event or role requests fail clearly
- duplicate idempotency replay is safe

## 3. Event and Worker Tests

Verify async helpers do not become hidden workflow authority.

Minimum coverage:

- worker-requested transition follows the same transition gateway
- event emission occurs after accepted workflow actions
- retry does not duplicate lifecycle, finance, or notification outcomes
- failed worker can be retried safely
- dead-letter or failure capture path exists for exhausted retries

## 4. End-to-End Workflow Tests

Verify the MVP corridor path as one operational flow.

Minimum workflow:

```text
order
-> quote
-> payment intent
-> confirmation
-> matching
-> assignment
-> trip milestones
-> POD
-> payment and settlement visibility
```

Minimum assertions:

- event rows are persisted across the flow
- role-safe screens and APIs see the same authoritative state
- blocked or failed branches produce explainable status
- exception paths remain auditable

## 5. Observability and Failure Tests

Verify operators can see workflow problems.

Minimum coverage:

- illegal transition counter or equivalent metric increments
- failed worker path is visible
- retry count is visible
- stuck workflow is visible in ops view or logs
- audit trail is queryable for accepted transitions

## Recommended Test Ladder

Apply tests in this order:

```text
unit and policy tests
-> API contract tests
-> event and worker tests
-> end-to-end corridor workflow tests
-> failure and observability drills
```

## Current Required Test Areas

- migration tests
- constraint tests
- trigger tests where used
- order lifecycle tests
- pricing rule tests
- matching rule tests
- SLA promise vs outcome tests
- finance event tests
- idempotency and concurrency tests
- worker retry and replay tests

## Explicit Non-Goals For First Pass

Do not block first-pass verification on:

- nationwide scale simulation
- advanced AI-agent quality benchmarks
- full BI/dashboard correctness suites
- warehouse-only workflows outside current MVP scope

## Practical Rule

If a workflow step can change money, customer promise, provider assignment, or lifecycle state, it must have:

- a deterministic rule path
- an auditable event trail
- an idempotency test
- a failure-path test

That is the minimum bar for calling the current project safe to build forward.
