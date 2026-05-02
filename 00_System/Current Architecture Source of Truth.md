---
type: memo
domain: architecture
scope: source_of_truth
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Operations Strategy Hub]]"
  - "[[Technology Stack Hub]]"
  - "[[Business Models Hub]]"
tags:
  - architecture
  - source-of-truth
  - backend
  - database
  - product
---

# Current Architecture Source of Truth

## Purpose

This note is the current architecture source of truth for the Zippy project.

It ties together:

- current product shape
- current backend structure
- current database structure
- current operational logic

It should be used instead of older PRD, backend, and database drafts when those conflict with present project direction.

## Project Definition

Zippy is currently best defined as:

```text
a corridor-first logistics platform that connects consignors, drivers, owner-drivers, and transport companies for shipment execution, return-load optimization, and reliability-aware operations
```

The project is not currently centered on:

- warehouse inventory management
- broad generic marketplace logic without corridor intelligence
- stack-specific or model-specific architecture commitments

## Current Product Scope

The platform currently needs four main operational surfaces:

- customer or consignor flows
- driver or owner-driver flows
- transport-company flows
- admin and ops control-tower flows

Core product capabilities:

- order booking and validation
- price quotation
- provider and vehicle matching
- trip execution and tracking
- SLA-aware promise handling
- proof of delivery and delivery closure
- payment and invoice traceability
- alerts, incidents, and operational oversight
- analytics for reliability, pricing, and return-trip intelligence

## Current System Shape

The best current high-level architecture is:

```text
apps and operational users
-> backend coordination core
-> operational database and event records
-> pricing, matching, routing, SLA, and finance workflows
-> analytics and control-tower intelligence
```

## Backend Source Of Truth

The backend should be treated as:

```text
FastAPI application
-> route modules
-> service layer
-> deterministic policy layer
-> persistence layer
-> event/workflow layer
-> analytics feed layer
```

Current backend note:

- [[Backend Structure for Current Project]]

Current backend implementation reality in the repo:

- FastAPI
- SQLAlchemy models
- API modules for health, vehicles, pricing, orders, matches, bids, ML pricing, routing
- pricing and routing services already present

Recommended backend module shape:

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
```

## Database Source Of Truth

The database should be treated as:

```text
transactional operational core
-> event traces
-> analytics feed
-> reporting and scorecards
```

Current database note:

- [[Zippy Logistics Operational Core Schema]]

Current database principle:

- operational schema first
- analytics schema second
- no free-form duplication from old drafts

## Accepted Operational Domains

The current accepted database domains are:

| Domain | Main Tables |
|---|---|
| Identity | `app_users`, `customer_accounts`, `driver_profiles`, `transport_companies` |
| Fleet | `vehicle_models`, `vehicles`, `vehicle_availability_snapshots` |
| Network | `directed_lanes`, `lane_rate_bands`, `partner_relationships` |
| Pricing intelligence | `city_market_profiles`, `lane_pricing_signals`, `price_quotes` |
| OMS | `orders`, `order_stops`, `order_documents`, `order_state_events` |
| Matching | `order_bids`, `order_matches` |
| TMS | `trips`, `trip_legs`, `shipment_events` |
| SLA and service policy | `service_levels`, `sla_policies`, `order_sla_commitments` |
| Finance | `payment_records`, `payment_intents`, `invoice_records`, `finance_events` |
| Trust and ops | `notifications`, `push_tokens`, `driver_ratings`, `transport_company_ratings`, `admin_activities`, `incident_logs`, `driver_alerts` |

## User Roles

Current operational roles:

- `customer`
- `driver`
- `transport_company`
- `admin`
- `ops`

Important role interpretation:

- transport companies may act in dual-role workflows
- owner-driver behavior belongs under driver plus vehicle ownership context
- warehouse-only roles are out of current scope

## Current Operational Logic

The current system should be driven by these operational ideas:

- directed lanes, not symmetric city pairs
- return-load and triangle-route logic where useful
- deterministic pricing inputs with auditable quotes
- SLA policies stored as data, not only in documents
- event-backed order and trip lifecycle tracking
- finance traceability across payment, invoice, and settlement
- control-tower awareness through alerts and incidents

## SLA Source Of Truth

SLA logic belongs in both operations and data model.

Current relevant notes:

- [[On-Time Delivery Control Tower Strategy for Multimodal Freight]]
- [[Zippy Logistics Operational Core Schema]]

Current SLA principles:

- each lane can have a different promise shape
- service levels should be explicit
- promised windows should be stored per order
- buffer, backup, and breach logic should be data-backed

## Pricing Source Of Truth

Pricing must remain:

- deterministic
- explainable
- lane-aware
- backhaul-aware
- auditable

Current pricing logic should draw from:

- lane and city context
- density and congestion signals
- demand-supply context
- return-load or deadhead risk
- service-level commitments

## Event Source Of Truth

Important operational events:

- order created
- quote generated
- payment initiated
- payment confirmed
- provider matched
- driver assigned
- trip started
- pickup completed
- in-transit milestone reached
- SLA risk raised
- POD uploaded
- delivery completed
- settlement completed

The database should record these through state events, shipment events, finance events, and alert or incident records.

## Analytics Source Of Truth

Operational data should feed analytics, not replace it.

Current analytics direction:

- lane delay events
- shipment delay facts
- lane reliability scorecards
- pricing calibration
- triangle and backhaul performance measurement

That means:

```text
operational database != analytics database
```

They should connect, but not collapse into one blurred schema.

## Testing Source Of Truth

Testing must focus on business workflows, not just code presence.

Current required test areas:

- migration tests
- constraint tests
- trigger tests
- order lifecycle tests
- pricing rule tests
- matching rule tests
- SLA promise vs outcome tests
- finance event tests
- idempotency and concurrency tests

## What Is Explicitly Out Of Scope For Current Truth

These should not be treated as current architecture commitments:

- old Django-first backend assumptions
- specific LLM or model assignments
- warehouse inventory schema expansion
- vendor-specific infra choices as permanent truth
- old duplicated database drafts

## Primary Reference Notes

Use these as the linked source set:

- [[Master PRD Distillation for Current Project]]
- [[Backend Structure for Current Project]]
- [[Zippy Logistics Operational Core Schema]]
- [[On-Time Delivery Control Tower Strategy for Multimodal Freight]]
- [[Founder SWOT + Moat + Investor Score Memo]]

## Practical Rule

When a future note conflicts with an older draft:

1. prefer current operational scope over historical ambition
2. prefer current backend reality over old framework assumptions
3. prefer refined schema notes over raw draft tables
4. prefer deterministic business rules over tool-specific or model-specific detail

## Bottom Line

The current architecture source of truth is:

```text
multi-role logistics platform
-> FastAPI coordination backend
-> operational core schema
-> deterministic pricing, matching, SLA, and finance workflows
-> event-backed logistics execution
-> analytics for lane reliability and return-trip intelligence
```

That is the architecture to build against now.
