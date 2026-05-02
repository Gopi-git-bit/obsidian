---
type: memo
domain: execution
scope: mvp
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Operations Strategy Hub]]"
  - "[[Technology Stack Hub]]"
tags:
  - mvp
  - build-order
  - execution
---

# MVP Build Order

## Purpose

This note defines the build order for the first Zippy MVP that is most likely to turn the current architecture into working product proof.

## MVP Definition

The MVP is not:

- a full multi-city platform
- a complete AI-agent system
- a finished analytics suite
- a generic logistics super-app

The MVP is:

```text
one corridor-first shipment workflow
from booking to settlement
with driver execution, customer visibility, and ops oversight
```

## Corridor Bias

The MVP should be built around the strongest current wedge:

- Western Tamil Nadu plus Chennai / Bengaluru-adjacent corridor logic

Suggested first validation candidates:

- Tiruppur -> Chennai
- Chennai -> Coimbatore
- Bengaluru -> Hosur

## Build Order

## Step 1: Backend Truth

Build first:

- refined order model
- refined match model
- trip and trip-leg models
- SLA commitment models
- finance event models
- driver alert models

Reason:

- without these, the workflow stays conceptual

## Step 2: Core Services

Build second:

- `order_service`
- `matching_service`
- `trip_service`
- `sla_service`
- `payment_service`
- `alert_service`

Reason:

- service-layer workflows are the backbone of reliable backend behavior

## Step 3: Critical APIs

Build third:

- create order
- estimate quote
- initiate payment intent
- list or accept matches
- create or fetch active trip
- update shipment milestone
- upload POD or receipt metadata
- fetch customer tracking view
- fetch ops exception view

Reason:

- these endpoints define the actual MVP user experience

## Step 4: Driver Frontend Critical Path

Build fourth:

- login
- home summary
- order offer list
- accept or reject
- active trip screen
- milestone updates
- document upload
- alert display

Reason:

- the driver app is the execution engine of the MVP

## Step 5: Customer Frontend Critical Path

Build fifth:

- login
- booking form
- quote display
- payment mode flow
- order confirmation
- shipment tracking
- delivery status and document visibility

Reason:

- this gives the platform its shipper-facing value

## Step 6: Ops Web Critical Path

Build sixth:

- pending order queue
- unmatched or failed queue
- active trip monitor
- alert and incident queue
- payment and settlement blocker queue

Reason:

- the MVP needs a supervision layer to survive real operations

## Step 7: Event Logging And Analytics Feed

Build seventh:

- order state events
- shipment events
- finance events
- lane delay event generation

Reason:

- this creates the first real data flywheel

## Step 8: First Reliability And Pricing Loop

Build eighth:

- lane pricing signal ingestion
- first quote audit trail
- first SLA commitment evaluation
- first lane reliability metrics

Reason:

- this is where the MVP starts becoming differentiated, not just functional

## What To Delay

Delay until after MVP proof:

- broad transport-company multi-mode polish
- advanced dispute automation
- elaborate agent runtime complexity
- nationwide lane library
- warehouse or SKU inventory expansion
- extensive BI or dashboard breadth beyond core ops

## Required MVP Outcomes

The MVP should prove:

1. customer can place an order and see a quote
2. driver can receive, accept, and execute a trip
3. backend can track milestones and state correctly
4. payment and settlement states are visible and traceable
5. ops can monitor exceptions
6. the system produces usable operational data

## MVP Exit Criteria

The MVP is ready for field validation when:

- one real corridor workflow runs end-to-end
- state transitions are enforced
- driver and customer apps cover the happy path
- ops view covers the main exception path
- core finance events are recorded
- first lane data starts collecting

## Bottom Line

The right build order is:

```text
schema and services
-> critical APIs
-> driver app
-> customer app
-> ops cockpit
-> event and analytics feed
-> first reliability and pricing loop
```

That is the shortest path from refined architecture to real product proof.
