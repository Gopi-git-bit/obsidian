---
type: memo
domain: backend
scope: gap_analysis
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
tags:
  - backend
  - gap-analysis
  - implementation
  - mvp
---

# Backend Gap Analysis Against Current Target

## Purpose

This note compares the actual backend codebase in `backend/app` against the current backend and database target defined in:

- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Zippy Logistics Operational Core Schema]]
- [[MVP Build Order]]

## Executive Summary

The current backend is a meaningful prototype, not a production-aligned implementation of the refined project.

It already has:

- FastAPI app structure
- SQLAlchemy integration
- core API modules for orders, pricing, matching, bidding, routing, and vehicles
- working price and route logic modules
- basic tests

It does **not** yet implement the current architecture’s full operational core.

The biggest mismatch is:

```text
current code models a simplified load-order prototype
while the current project target models a multi-role logistics workflow platform
```

## Gap Severity Summary

| Gap Area | Severity | Summary |
|---|---:|---|
| Domain model coverage | High | Current ORM covers only `orders`, `bids`, `matches`, and reference `vehicle_models` |
| Service-layer structure | High | Business workflows mostly live inside route handlers or are missing |
| Lifecycle and policy enforcement | High | Refined state machine, SLA commitments, and policy modules are not implemented |
| Finance workflow | High | No payment, invoice, settlement, or finance event models or APIs |
| Trip execution model | High | No `trips`, `trip_legs`, or execution event models in backend code |
| Identity and roles | High | No `app_users`, `customer_accounts`, `driver_profiles`, `transport_companies`, or auth layer implementation |
| Alert and incident support | High | No `driver_alerts`, `incident_logs`, or ops-facing runtime handling |
| Pricing intelligence persistence | Medium | Pricing endpoints exist, but pricing context tables and quote audit persistence do not |
| Analytics feed integration | Medium | Routing and pricing services exist, but event-to-analytics feed is not implemented |
| Test depth | High | Tests cover basic endpoints, not refined workflows, SLA, finance, or idempotency |

## What Exists Today

## 1. FastAPI Entry Point

Current file:

- [backend/app/main.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/main.py)

Strengths:

- clean FastAPI app bootstrap
- router registration already present
- local schema creation for development and tests

Gaps:

- no modular `core/`, `policies/`, `events/`, `workers/`, or `repositories/` layers yet
- direct metadata creation is fine for local work but not a substitute for mature migration flow

## 2. Current ORM Coverage

Current files:

- [backend/app/models/order_model.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/models/order_model.py)
- [backend/app/models/vehicle_model.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/models/vehicle_model.py)

Strengths:

- orders, bids, and matches already exist
- vehicle model reference table is detailed
- some useful constraints and indexes are already present

Gaps:

- `VehicleModel` is a reference catalog, not the operational `vehicles` table the current target needs
- no user, driver, customer, transport company, trip, SLA, payment, alert, or finance models
- order lifecycle is too small relative to the refined target
- no explicit state-event log table in the code

## 3. Current API Coverage

Current files:

- [backend/app/api/orders.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/orders.py)
- [backend/app/api/matches.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/matches.py)
- [backend/app/api/bids.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/bids.py)
- [backend/app/api/pricing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/pricing.py)
- [backend/app/api/ml_pricing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/ml_pricing.py)
- [backend/app/api/routing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/routing.py)
- [backend/app/api/vehicles.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/vehicles.py)

Strengths:

- useful initial endpoint surface
- pricing and routing API shape is already meaningful
- order, bidding, and matching happy paths are started

Gaps:

- route handlers contain too much business workflow logic
- no endpoints yet for:
  - users and auth
  - trips
  - SLA commitments
  - payments
  - invoices
  - notifications
  - driver alerts
  - incidents
  - admin or ops views

## 4. Current Services

Current files:

- [backend/app/services/pricing_service.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/services/pricing_service.py)
- [backend/app/services/route_optimizer.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/services/route_optimizer.py)

Strengths:

- service layer exists in principle
- pricing and routing logic are separated from API handlers
- these are reusable building blocks for the refined backend

Gaps:

- missing core business workflow services:
  - `order_service`
  - `matching_service`
  - `trip_service`
  - `payment_service`
  - `sla_service`
  - `alert_service`
- no explicit policy layer separate from services

## 5. Current Test Coverage

Current files:

- [backend/tests/test_api.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/tests/test_api.py)
- [backend/tests/test_orders.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/tests/test_orders.py)

Strengths:

- basic endpoint smoke coverage exists
- order creation, listing, update, cancel, and some match stats are covered

Gaps:

- no refined lifecycle transition tests
- no idempotency tests
- no pricing-rule validation against persisted quote data
- no trip, alert, SLA, finance, or permission tests

## Detailed Gap Analysis

## A. Domain Model Gap

Target backend requires these operational domains:

- identity
- fleet
- network
- pricing intelligence
- OMS
- matching
- TMS
- SLA and service policy
- finance
- trust and ops

Current code implements only fragments of:

- OMS
- matching
- pricing
- routing
- vehicle reference catalog

Conclusion:

The current backend is missing most of the accepted operational domains.

## B. State and Lifecycle Gap

Target project expects:

- explicit order lifecycle policy
- state events
- SLA commitments
- structured trip milestones
- alert and incident escalation

Current code has:

- a small `OrderStatus` enum
- direct status mutation in route handlers

Example:

- [backend/app/api/orders.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/orders.py)
- [backend/app/api/matches.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/matches.py)
- [backend/app/api/bids.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/bids.py)

Conclusion:

Lifecycle logic is underpowered and too handler-local for the current architecture.

## C. Identity and Permissions Gap

Target architecture requires:

- `app_users`
- `customer_accounts`
- `driver_profiles`
- `transport_companies`
- role-aware behavior across customer, driver, transport company, admin, and ops

Current code has:

- no identity model implementation in backend
- no role-aware API boundaries

Conclusion:

Role and permission enforcement is still largely absent.

## D. Vehicle and Provider Gap

Target architecture expects:

- operational `vehicles`
- availability snapshots
- provider identity
- company-owned and owner-driver distinction

Current code has:

- only `VehicleModel`, which behaves like a spec catalog

Conclusion:

The backend can recommend vehicle types, but not yet manage live operational fleet assets properly.

## E. Trip Execution Gap

Target architecture expects:

- `trips`
- `trip_legs`
- `shipment_events`
- active execution lifecycle
- document and POD actions tied to trip progression

Current code has:

- no trip model
- no trip API
- no shipment event persistence layer

Conclusion:

The core movement of freight is not yet represented as a first-class backend domain.

## F. Finance Gap

Target architecture expects:

- `payment_records`
- `payment_intents`
- `invoice_records`
- `finance_events`

Current code has:

- price calculation only
- no payment persistence
- no invoice or settlement lifecycle

Conclusion:

The backend currently prices work, but does not yet run the finance lifecycle the product needs.

## G. SLA Gap

Target architecture expects:

- `service_levels`
- `sla_policies`
- `order_sla_commitments`

Current code has:

- route and ETA estimation
- no stored service-level or commitment model

Conclusion:

The backend can estimate travel, but cannot yet enforce or audit customer promises in the way the current operating model requires.

## H. Alert and Ops Gap

Target architecture expects:

- `driver_alerts`
- `incident_logs`
- ops and admin exception views

Current code has:

- no alert or incident runtime support

Conclusion:

Control-tower operations are still missing from implementation.

## I. Event and Analytics Feed Gap

Target architecture expects:

- event-backed operational traces
- analytics feed into lane and reliability tables

Current code has:

- no explicit event module
- no persistent state-event model in code
- no operational-to-analytics feed path

Conclusion:

The system cannot yet generate the data flywheel the strategy depends on.

## Reuse Opportunities

Not everything should be rewritten.

The best reusable pieces are:

### 1. API Skeleton

- the FastAPI structure in [backend/app/main.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/main.py)
- the existing router grouping approach

### 2. Pricing Logic

- [backend/app/services/pricing_service.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/services/pricing_service.py)
- [backend/app/api/pricing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/pricing.py)
- [backend/app/api/ml_pricing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/ml_pricing.py)

These should be refactored to read from persisted pricing context later, not discarded.

### 3. Routing Logic

- [backend/app/services/route_optimizer.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/services/route_optimizer.py)
- [backend/app/api/routing.py](C:/Users/user/Downloads/MiniMax%20Agent_%20Minimize%20Effort,%20Maximize%20Intelligence_files/backend/app/api/routing.py)

These are strong candidates to sit behind future `trip_service` and `sla_service`.

### 4. Basic Order / Match / Bid Patterns

- existing schemas and endpoints are useful scaffolding for the new order and matching layers

They should be evolved, not thrown away wholesale.

## Recommended Implementation Sequence

## Phase 1: Persistence Alignment

Add missing backend models for:

- users and profiles
- vehicles and availability
- orders and order state events
- trips and trip legs
- service levels and SLA commitments
- payments, invoices, finance events
- alerts and incidents

## Phase 2: Service Layer Buildout

Implement:

- `order_service`
- `matching_service`
- `trip_service`
- `payment_service`
- `sla_service`
- `alert_service`

## Phase 3: Move Logic Out Of Handlers

Refactor route handlers so they:

- validate
- call services
- return results

and no longer perform workflow logic inline.

## Phase 4: Event and Policy Layer

Implement:

- lifecycle policy checks
- event emission and persistence
- idempotency handling
- workflow-safe transitions

## Phase 5: Critical MVP Endpoints

Build or upgrade:

- order creation and quote path
- payment intent path
- match confirmation path
- active trip path
- shipment milestone path
- POD path
- ops exception path

## Phase 6: Test Expansion

Add:

- transition tests
- pricing rule tests
- SLA commitment tests
- payment and finance event tests
- alert tests
- role and authorization tests

## Shortest Path To Product Proof

The shortest useful path from the current codebase is:

```text
keep FastAPI skeleton
-> align models to operational schema
-> add service layer
-> implement order -> payment -> match -> trip -> POD -> settlement
-> expose driver/customer/ops critical path
```

That path will close the most important backend gaps without wasting the existing prototype work.

## Bottom Line

The current backend is a solid prototype foundation, but it is still far from the refined target architecture.

The biggest backend closure step is not “more features.”

It is:

```text
align the codebase to the accepted operational domains and workflow structure
```

Once that is done, the rest of the product can be built on much firmer ground.
