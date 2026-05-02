---
type: memo
domain: frontend
scope: architecture
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[Business Models Hub]]"
tags:
  - frontend
  - architecture
  - mobile
  - admin
  - source-of-truth
---

# Frontend Architecture for Current Project

## Purpose

This note transforms the older `frontend deeopment planning .txt` into the current frontend architecture reference for the Zippy project.

It keeps the durable product and UX structure, and removes or relaxes the parts that are too stack-specific or operationally inconsistent with the refined source-of-truth notes.

## Current Frontend Mission

The frontend system should support a corridor-first logistics platform connecting:

- consignors or customers
- drivers and owner-drivers
- transport companies
- admin and ops users

The frontend is not just UI. It is the operational surface for:

- booking
- matching visibility
- trip execution
- delivery proof
- SLA-aware status communication
- payment and invoice visibility
- control-tower monitoring

## Frontend Surfaces

The current project needs four frontend surfaces:

1. Driver mobile app
2. Customer mobile app
3. Transport-company mobile or responsive app
4. Admin and ops web app

Transport-company workflows should be designed explicitly, but implemented in phases so the core corridor workflow is not delayed.

## Current Frontend Principle

The frontend should reflect operational truth from the backend.

That means:

- the frontend does not own state-machine truth
- the frontend does not invent pricing or assignment logic
- the frontend should present deterministic backend outcomes clearly

Use [[Frontend UI Blueprint for Current Project]] as the screen/state/action blueprint for this principle.

## Recommended Frontend Shape

```text
shared design and logic
-> driver mobile app
-> customer mobile app
-> admin and ops web app
```

## Current App Set

## 1. Driver Mobile App

Purpose:

- accept and execute assigned transport work
- access trip details and required operational actions
- support document scanning and POD flow
- receive alerts and operational messages

Core driver capabilities:

- authentication and profile
- availability and online status
- assigned order and trip view
- route and ETA view
- shipment status updates
- invoice or challan scan at loading if required
- receipt or POD scan at delivery
- alerts for prolonged halt, route deviation, and other issues
- communication visibility for authorized contacts

Important current-context rule:

The driver app is an execution surface, not an assignment authority.

The driver may:

- accept
- reject or ignore
- update execution progress
- upload required documents

The driver app should not:

- bypass OMS assignment logic
- rewrite payment terms
- override route or SLA policy logic

## 2. Customer Mobile App

Purpose:

- allow customers to place and track shipment orders
- display pricing, service level, and shipment progress
- handle payment and document flows

Core customer capabilities:

- signup or login
- booking form
- origin and destination entry
- vehicle preference selection
- service-level selection
- payment mode selection
- optional document upload
- order confirmation
- driver and shipment tracking visibility after assignment
- invoice and payment visibility
- alerts for ETA, delay, and delivery completion

Important current-context rule:

The customer app should help booking and tracking, but must rely on backend truth for:

- available service levels
- actual quote
- final assignment
- promised delivery window

## 3. Admin and Ops Web App

Purpose:

- act as the control tower and operational cockpit
- monitor order, matching, trip, payment, and alert states

Core admin and ops capabilities:

- order funnel visibility
- pending and exception queues
- vehicle and provider availability overview
- real-time trip and alert monitoring
- SLA risk and breach review
- finance and settlement oversight
- driver and provider performance visibility
- incident and override review

The admin app is not just a reporting panel. It is the human supervision layer for:

- exceptions
- escalations
- unresolved disputes
- blocked workflows

## 4. Transport Company App

Purpose:

- let transport companies provide capacity or place orders without mixing role context
- manage company fleet, drivers, active work, and finance status

Core transport-company capabilities:

- provider-side opportunity review
- customer-side order placement
- fleet and driver availability
- vehicle/driver assignment
- active trip visibility
- service fee, invoice, and settlement visibility
- company verification and documents

Important current-context rule:

Transport-company UI must keep separate:

- company as customer
- company as provider

especially for orders, ledgers, invoices, and settlement.

## Shared Frontend Concepts

These should be shared across surfaces where appropriate:

- auth and session handling
- design tokens
- map and location display logic
- document upload components
- notification presentation
- currency and time formatting
- validation rules
- common API client logic

## Frontend Folder Direction

The older file's folder concept is still useful in principle.

Current recommended shape:

```text
frontend/
  shared/
    components/
    hooks/
    utils/
    assets/
    theme/
  mobile/
    driver-app/
    customer-app/
  web-admin/
```

This is a product-structure recommendation, not a locked framework mandate.

## Maps And Realtime Requirements

The exact libraries may change, but the frontend still needs:

- map rendering
- location selection
- route display
- ETA visibility
- real-time or near-real-time status refresh

Durable frontend requirements:

- customer can track assigned shipment
- driver can view route and trip progress
- ops can monitor active movement and exceptions

## Frontend Workflow Interpretation

## Driver / Provider Execution Flow

```text
receive assignment
-> accept or reject
-> view trip
-> proceed to pickup
-> confirm loading milestones
-> scan required document if needed
-> move in transit
-> receive alerts and ETA signals
-> confirm delivery
-> upload POD or receipt
```

## Customer Booking Flow

```text
login or signup
-> create booking
-> choose route and vehicle preference
-> choose payment mode
-> upload optional documents
-> confirm booking
-> receive quote and status updates
-> track assigned shipment
-> receive delivery and payment closure updates
```

## Admin And Ops Flow

```text
monitor new orders
-> review matching and assignment health
-> monitor active trips and alerts
-> inspect SLA risk and incidents
-> review payment and settlement blockers
-> act on escalations and overrides
```

## Contact Visibility Clarification

The older file contains some contradictory contact-sharing statements.

Current-context clarification:

- contact visibility should be role-based and minimal
- only operationally necessary contact details should be exposed
- customer, driver, consignee, and provider visibility should be governed by backend authorization and workflow stage

This means contact access is not a static frontend rule. It is a controlled product rule.

## Payment UX Clarification

The older note mixes several payment cases.

Current frontend truth should be:

- show payment mode clearly
- show quote and invoice status clearly
- show advance, pending, and settlement-related statuses clearly
- do not let frontend infer payment completion from local assumptions

All finance truth should come from backend state and finance events.

## SLA And Delivery UX

The frontend should present:

- promised pickup and delivery windows
- current shipment status
- ETA updates
- risk or delay notifications
- proof-of-delivery completion state

Important principle:

The frontend should communicate promise windows honestly, not just fastest-path estimates.

## Testing Guidance For Frontend

Frontend testing should cover:

- booking forms
- role-aware navigation
- status rendering by lifecycle state
- document upload flows
- map and tracking screens
- payment state rendering
- alert and notification rendering
- offline or degraded connectivity behavior on mobile

## What Was Kept From The Old Frontend Doc

- multi-surface frontend structure
- shared design layer concept
- driver/customer/admin separation
- driver execution flow
- customer booking and tracking flow
- transport company dual-role idea
- map, document, alert, and status visibility as core requirements

## What Was Intentionally Not Locked

- exact UI framework choice
- exact map provider choice
- exact state management library
- exact testing library set
- exact realtime transport library

Those can evolve.

## Primary Current References

Use this note with:

- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Zippy Logistics Operational Core Schema]]
- [[On-Time Delivery Control Tower Strategy for Multimodal Freight]]
- [[Driver Frontend for Current Project]]
- [[Customer Frontend for Current Project]]
- [[Transport Company Frontend for Current Project]]
- [[Admin and Ops Frontend for Current Project]]
- [[Frontend UI Blueprint for Current Project]]

## Bottom Line

The current frontend architecture should be treated as:

```text
three operational surfaces
-> shared design and logic
-> backend-driven workflow truth
-> role-aware booking, execution, tracking, payment, and control-tower UX
```

That is the frontend shape to build against now.
