---
type: memo
domain: product
scope: frontend_backend_flow_map
status: active
last_updated: 2026-05-15
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Frontend Architecture for Current Project]]"
  - "[[API and Event Contract for Current Project]]"
tags:
  - frontend
  - backend
  - flow-map
  - integration
  - source-of-truth
---

# Frontend-to-Backend Flow Map for Current Project

## Purpose

This note maps each MVP-critical user flow to backend resources, required states, and UI behavior.

It exists so builder tools do not need to infer:

- which screen calls which endpoint
- which action creates which event
- which statuses must be rendered
- which failures must block progress

## Mapping Principles

1. Frontend screens render backend truth.
2. Every mutation calls a specific API.
3. Every accepted mutation creates or updates a backend event trail.
4. Every critical screen must define loading, empty, success, and blocked states.

## Flow 1: Customer Booking

### Screens

- Login
- Booking Form
- Quote View
- Payment Intent View
- Order Confirmation

### API Path

```text
POST /orders
-> POST /orders/{order_id}/quote
-> POST /orders/{order_id}/payment-intent
-> GET /orders/{order_id}
```

### Backend Records Touched

- `orders`
- `price_quotes`
- `payment_intents`
- `order_state_events`

### UI States

#### Booking Form

- loading route and service metadata
- validation errors
- submit success with `order_id`

#### Quote View

- quote loading
- quote available
- quote unavailable or blocked

#### Payment Intent View

- payment intent loading
- payment initiated
- payment pending
- payment confirmed
- payment failed

### Critical Events

- `order_created`
- `quote_generated`
- `payment_intent_created`

## Flow 2: Customer Tracking

### Screens

- Order Detail
- Tracking View
- Delivery Status
- POD and Invoice Visibility

### API Path

```text
GET /orders/{order_id}
-> GET /customer/orders/{order_id}/tracking
-> GET /orders/{order_id}/documents
-> GET /orders/{order_id}/payments
-> GET /orders/{order_id}/invoices
```

### Backend Records Touched

- `orders`
- `trips`
- `shipment_events`
- `order_documents`
- `payment_records`
- `invoice_records`

### UI States

- order confirmed but not assigned
- assigned and awaiting pickup
- in transit
- delivered
- POD available
- invoice visible
- delay risk visible

## Flow 3: Driver Offer Acceptance

### Screens

- Driver Login
- Offer List
- Offer Detail

### API Path

```text
GET /drivers/{driver_id}/offers
-> POST /driver-offers/{offer_id}/accept
or
-> POST /driver-offers/{offer_id}/reject
```

### Backend Records Touched

- `order_matches`
- `orders`
- `order_state_events`

### UI States

- no offers
- offer available
- offer accepted
- offer expired
- accept failed due to race or reassignment

### Critical Events

- `match_confirmed`
- `driver_assigned`

## Flow 4: Driver Trip Execution

### Screens

- Active Trip
- Milestone Update
- Route and ETA View
- Alert View

### API Path

```text
GET /trips/{trip_id}
-> POST /trips/{trip_id}/milestones
-> GET /trips/{trip_id}/tracking
```

### Backend Records Touched

- `trips`
- `trip_legs`
- `shipment_events`
- `driver_alerts`

### UI States

- trip assigned but not started
- pickup arrived
- loaded
- in transit
- delivered
- alert raised
- milestone submission retry state

### Critical Events

- `trip_started`
- `pickup_arrived`
- `loaded`
- `in_transit`
- `delivered`

## Flow 5: POD Upload

### Screens

- POD Upload
- Upload Success
- Upload Retry

### API Path

```text
POST /documents/pod
-> GET /orders/{order_id}/documents
```

### Backend Records Touched

- `order_documents`
- `shipment_events`
- `order_state_events`

### UI States

- file selected
- upload in progress
- upload success
- upload failed
- duplicate submission safe retry

### Critical Events

- `pod_uploaded`

## Flow 6: Ops Order Supervision

### Screens

- Pending Orders Queue
- Unmatched Orders Queue
- Active Trips Monitor
- Alerts and Incidents Queue
- Finance Blockers View

### API Path

```text
GET /ops/orders/pending
GET /ops/orders/exceptions
GET /ops/trips/active
GET /ops/alerts
POST /ops/incidents
GET /ops/finance/blockers
```

### Backend Records Touched

- `orders`
- `order_matches`
- `trips`
- `driver_alerts`
- `incident_logs`
- `finance_events`

### UI States

- queue empty
- queue populated
- SLA risk visible
- incident logged
- blocker resolved after refresh

## Flow 7: Payment And Invoice Visibility

### Screens

- Customer Payment Status
- Customer Invoice View
- Ops Finance Blocker View

### API Path

```text
GET /orders/{order_id}/payments
GET /orders/{order_id}/invoices
GET /ops/finance/blockers
```

### Backend Records Touched

- `payment_intents`
- `payment_records`
- `invoice_records`
- `finance_events`

### UI States

- no payment started
- payment initiated
- payment confirmed
- invoice generated
- invoice pending
- settlement visibility pending

## MVP Screen-To-Endpoint Summary

| Screen | Main Endpoint |
| --- | --- |
| Booking Form | `POST /orders` |
| Quote View | `POST /orders/{order_id}/quote` |
| Payment View | `POST /orders/{order_id}/payment-intent` |
| Customer Tracking | `GET /customer/orders/{order_id}/tracking` |
| Driver Offer List | `GET /drivers/{driver_id}/offers` |
| Driver Accept | `POST /driver-offers/{offer_id}/accept` |
| Active Trip | `GET /trips/{trip_id}` |
| Milestone Submit | `POST /trips/{trip_id}/milestones` |
| POD Upload | `POST /documents/pod` |
| Ops Queue | `GET /ops/orders/pending` |

## Required UI Behavior Rules

Every MVP-critical screen must implement:

- loading state
- empty state
- success state
- API error state
- blocked or not-allowed state where relevant

Additional rules:

- optimistic lifecycle mutation is not allowed for critical workflow states
- frontend should refresh from backend after mutation success
- repeated submit actions must use idempotency-safe calls where applicable

## Bottom Line

Builders should map the first fullstack release like this:

```text
customer booking screens
-> order, quote, payment APIs
-> driver offer and trip screens
-> trip and document APIs
-> ops queue screens
-> alert and finance blocker APIs
```

If a screen cannot be tied to one authoritative backend contract, it is not ready to build.
