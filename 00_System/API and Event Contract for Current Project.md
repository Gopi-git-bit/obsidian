---
type: memo
domain: architecture
scope: api_and_event_contract
status: active
last_updated: 2026-05-15
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Current Project Navigation Hub]]"
  - "[[Backend Structure for Current Project]]"
tags:
  - api
  - events
  - contract
  - backend
  - source-of-truth
---

# API and Event Contract for Current Project

## Purpose

This note defines the minimum canonical API and event contract for the first real Zippy build.

It is intentionally narrower than the total vision.

Use this as the builder-facing contract for:

- frontend integration
- backend route planning
- state transitions
- event persistence
- role-aware behavior

## Contract Principles

1. Backend owns lifecycle truth.
2. Frontend never mutates lifecycle state directly.
3. Important actions create durable events.
4. Transition commands must be explicit and idempotent.
5. Response payloads should be role-safe and stage-aware.

## Canonical Resource Families

- `auth`
- `users`
- `vehicles`
- `orders`
- `quotes`
- `payments`
- `matches`
- `trips`
- `documents`
- `alerts`
- `ops`

## API Surface

### Auth And Identity

```text
POST   /auth/login
POST   /auth/logout
GET    /auth/me
```

Minimum `/auth/me` response:

```json
{
  "user_id": "UUID",
  "role": "customer | driver | transport_company | admin | ops",
  "profile_status": "active",
  "display_name": "string"
}
```

### Customer Order Flow

```text
POST   /orders
GET    /orders/{order_id}
GET    /orders
POST   /orders/{order_id}/quote
POST   /orders/{order_id}/payment-intent
POST   /orders/{order_id}/transition
```

`POST /orders` minimum request:

```json
{
  "origin_city": "Tiruppur",
  "destination_city": "Chennai",
  "pickup_window_start": "ISO",
  "pickup_window_end": "ISO",
  "material_type": "textile_cartons",
  "vehicle_type_preference": "17ft_closed_body",
  "service_level": "standard",
  "payment_mode": "advance | full | topay",
  "documents": []
}
```

`POST /orders/{order_id}/quote` minimum response:

```json
{
  "order_id": "UUID",
  "quote_id": "UUID",
  "currency": "INR",
  "base_amount": 0,
  "service_level": "standard",
  "price_breakdown": {},
  "quote_status": "generated"
}
```

`POST /orders/{order_id}/payment-intent` minimum response:

```json
{
  "order_id": "UUID",
  "payment_intent_id": "UUID",
  "amount_due_now": 0,
  "payment_mode": "advance | full | topay",
  "payment_status": "initiated"
}
```

### Matching And Assignment

```text
GET    /orders/{order_id}/matches
POST   /orders/{order_id}/matches/{match_id}/confirm
GET    /drivers/{driver_id}/offers
POST   /driver-offers/{offer_id}/accept
POST   /driver-offers/{offer_id}/reject
```

Driver offer minimum response:

```json
{
  "offer_id": "UUID",
  "order_id": "UUID",
  "trip_preview": {
    "origin_city": "string",
    "destination_city": "string",
    "material_type": "string"
  },
  "expires_at": "ISO"
}
```

### Trip Execution

```text
GET    /trips/{trip_id}
POST   /trips/{trip_id}/milestones
POST   /trips/{trip_id}/documents
GET    /trips/{trip_id}/tracking
```

`POST /trips/{trip_id}/milestones` minimum request:

```json
{
  "event": "pickup_arrived | loaded | in_transit | delivered",
  "timestamp": "ISO",
  "location": {
    "lat": 0,
    "lng": 0
  },
  "idempotency_key": "string"
}
```

### POD And Documents

```text
POST   /documents/pod
GET    /orders/{order_id}/documents
```

`POST /documents/pod` minimum request:

```json
{
  "order_id": "UUID",
  "trip_id": "UUID",
  "document_type": "pod",
  "file_ref": "string",
  "uploaded_by_role": "driver",
  "idempotency_key": "string"
}
```

### Customer Tracking

```text
GET    /customer/orders/{order_id}/tracking
```

Minimum tracking response:

```json
{
  "order_id": "UUID",
  "order_status": "string",
  "promised_window": {},
  "current_eta": "ISO",
  "latest_milestone": "string",
  "delay_risk": "none | low | medium | high"
}
```

### Ops And Exceptions

```text
GET    /ops/orders/pending
GET    /ops/orders/exceptions
GET    /ops/trips/active
GET    /ops/alerts
POST   /ops/incidents
```

### Finance Visibility

```text
GET    /orders/{order_id}/payments
GET    /orders/{order_id}/invoices
GET    /ops/finance/blockers
```

## Canonical Transition Gateway

Only one route may change order lifecycle state:

```text
POST /orders/{order_id}/transition
```

Minimum request:

```json
{
  "new_state": "string",
  "event": "string",
  "actor_role": "customer | driver | transport_company | admin | ops",
  "actor_id": "UUID",
  "idempotency_key": "string",
  "reason": "optional string",
  "evidence_ref": "optional string"
}
```

Required behavior:

- validate current state
- validate legal transition
- validate role permission
- write order state event
- return authoritative updated state

## Canonical Order States

Use this minimum state set for MVP:

```text
DRAFT
PAYMENT_PENDING
CONFIRMED
MATCHING
ASSIGNED
IN_TRANSIT
DELIVERED
POD_UPLOADED
SETTLEMENT_PENDING
CLOSED
CANCELLED
EXCEPTION
```

## Canonical Event Families

### Order State Events

- `order_created`
- `quote_generated`
- `payment_intent_created`
- `payment_confirmed`
- `order_confirmed`
- `match_confirmed`
- `driver_assigned`
- `order_cancelled`
- `order_exception_raised`

### Shipment Events

- `trip_started`
- `pickup_arrived`
- `loaded`
- `in_transit`
- `sla_risk_raised`
- `delivered`
- `pod_uploaded`

### Finance Events

- `payment_initiated`
- `payment_confirmed`
- `invoice_generated`
- `settlement_visibility_updated`

### Alert And Incident Events

- `driver_alert_created`
- `incident_logged`

## Canonical Event Envelope

```json
{
  "event_id": "UUID",
  "event_type": "string",
  "entity_type": "order | trip | payment | invoice | alert | incident",
  "entity_id": "UUID",
  "actor_role": "string",
  "actor_id": "UUID",
  "timestamp": "ISO",
  "idempotency_key": "string",
  "payload": {}
}
```

## Required Integration Rules

- frontend reads authoritative status from resource responses
- workers may emit events but must not bypass transition rules
- realtime streams may mirror events but not act as command channels
- every accepted transition must create at least one durable event row

## Bottom Line

Build against this path:

```text
orders
-> quotes
-> payment intents
-> matches
-> trips
-> POD documents
-> finance visibility
-> ops exceptions
```

If a planned endpoint does not strengthen that contract, it is not MVP-critical.
