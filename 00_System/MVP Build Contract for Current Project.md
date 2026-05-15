---
type: memo
domain: execution
scope: mvp_contract
status: active
last_updated: 2026-05-15
related_hubs:
  - "[[Operations Strategy Hub]]"
  - "[[Technology Stack Hub]]"
  - "[[Current Project Navigation Hub]]"
tags:
  - mvp
  - build-contract
  - source-of-truth
  - execution
---

# MVP Build Contract for Current Project

## Purpose

This note is the implementation contract for the first real Zippy build.

It is written for builder tools and engineers who need one decision-complete statement of:

- what the first product must do
- what must be built first
- what is explicitly out of scope
- what counts as MVP success

Use this note with:

- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Frontend Architecture for Current Project]]
- [[API and Event Contract for Current Project]]

## MVP Definition

The MVP is:

```text
one corridor-first shipment workflow
from booking to settlement visibility
with customer booking, driver execution, and ops supervision
```

The MVP is not:

- a nationwide logistics platform
- a complete autonomous agent platform
- a finished transport-company dual-role product
- a full warehouse or inventory system
- a full accounting suite

## First Validation Corridor

Build against one corridor-first wedge.

Current recommended candidate set:

- Tiruppur -> Chennai
- Chennai -> Coimbatore
- Bengaluru -> Hosur

Default implementation assumption:

```text
Tiruppur -> Chennai is the first live validation corridor
```

## Required User Surfaces

The first shippable MVP must include:

1. Customer booking and tracking surface
2. Driver execution surface
3. Admin and ops control-tower surface

Transport-company-specific UI may be deferred after MVP proof, but the backend should preserve the role model.

## Required End-To-End Workflow

The MVP must support this exact operational path:

```text
customer creates order
-> system generates quote
-> customer chooses payment mode and payment intent is created
-> order becomes confirmed when required payment gate clears
-> provider and vehicle are matched
-> driver receives assignment
-> active trip begins
-> pickup milestone is recorded
-> in-transit milestones are recorded
-> delivery milestone is recorded
-> POD is uploaded
-> invoice and payment status are visible
-> settlement visibility is updated
```

## Must-Build Backend Domains

These are mandatory for MVP:

- identity and role model
- operational vehicles
- orders and order state events
- matching and assignment
- trips and shipment events
- SLA commitment storage
- payment intents and payment records
- invoice records and finance events
- driver alerts and incident logs

## Must-Build Frontend Capabilities

### Customer

- login
- booking form
- quote view
- payment mode selection
- order confirmation
- shipment tracking
- POD and invoice visibility

### Driver

- login
- assignment list
- accept or reject flow
- active trip view
- milestone updates
- POD upload
- alert view

### Admin and Ops

- pending orders queue
- unmatched or failed queue
- active trip monitor
- alert and incident queue
- payment and settlement blocker view

## Explicitly Out Of Scope For MVP

- dynamic multi-city rollout tooling
- complete transport-company self-service portal
- advanced dispute automation
- full GST return filing automation
- elaborate agent orchestration runtime
- large BI dashboard suite
- broad warehouse execution and SKU inventory modules

## Required Non-Functional Rules

- backend is the source of workflow truth
- all lifecycle transitions must be validated through service and policy layers
- state changes must write event records
- finance status must come from backend state, not frontend assumptions
- frontend must render loading, error, empty, and blocked states for every critical path
- critical endpoints must be idempotent where retries are expected

## MVP Exit Criteria

The MVP is ready for field validation only when all of these are true:

1. A real customer can create an order and receive a quote.
2. A payment intent can be created and recorded.
3. A driver can accept assigned work and execute milestones.
4. Ops can monitor live orders, trips, and exceptions.
5. POD can be uploaded and tied to the shipment.
6. Invoice and payment status are visible to the right user roles.
7. Order, shipment, and finance event records are persisted.
8. One corridor can run end to end without manual spreadsheet-only coordination.

## Build Sequence

1. Backend domain alignment
2. Service and policy layers
3. Critical APIs
4. Driver frontend critical path
5. Customer frontend critical path
6. Ops web critical path
7. Event logging and analytics feed

## Bottom Line

Build this first:

```text
order
-> quote
-> payment intent
-> assignment
-> trip
-> POD
-> invoice/payment visibility
-> ops exception handling
```

If a feature does not strengthen that path, it is not MVP-critical.
