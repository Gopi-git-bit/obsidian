---
type: memo
domain: product
scope: frontend_backend_flow_map
status: active
last_updated: 2026-05-31
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
- Registration Segment Selection
- Registration OTP Verification
- Booking Form
- Booking OTP Checkpoint
- Quote View
- ToPay Consent View when applicable
- Hold / Resume Payment Resolution when applicable
- Payment Intent View
- Order Confirmation

### API Path

```text
POST /auth/register/customer
-> POST /auth/otp/send
-> POST /auth/otp/verify
-> POST /orders
-> POST /orders/{order_id}/otp-checkpoint
-> POST /orders/{order_id}/quote
-> POST /orders/{order_id}/topay/consent-request
-> POST /orders/{order_id}/topay/consent-response
-> POST /orders/{order_id}/hold or POST /orders/{order_id}/resume
-> POST /orders/{order_id}/payment-intent
-> GET /orders/{order_id}
```

### Backend Records Touched

- `customer_accounts`
- `customer_verification_events`
- `orders`
- `price_quotes`
- `topay_consent_events`
- `payment_intents`
- `order_state_events`
- `notifications`

### UI States

#### Registration

- segment selection required
- organized-company email OTP pending / verified / failed / expired
- individual-unorganized phone OTP pending / verified / failed / expired
- profile blocked for missing GST/PAN, phone, email, Aadhaar/KYC reference, or authorized-person data based on segment

#### Booking Form

- loading route and service metadata
- validation errors
- submit success with `order_id`
- organized-company booking OTP pending
- individual/unorganized booking OTP pending
- consignee details required for ToPay

#### Quote View

- quote loading
- quote available
- quote unavailable or blocked

#### ToPay Consent View

- consent request not sent
- consent request sent by WhatsApp/SMS
- consignee accepted
- consignee denied
- consent expired
- redirected to consignor for full payment, cancellation, or hold

#### Payment Intent View

- payment intent loading
- payment initiated
- payment pending
- payment confirmed
- payment failed
- payment mismatch under review
- on hold for ToPay or payment resolution
- resumed and waiting for consignee response

### Critical Events

- `customer_registered`
- `otp_sent`
- `otp_verified`
- `order_created`
- `order_booking_otp_verified`
- `quote_generated`
- `topay_consent_requested`
- `topay_consent_accepted`
- `topay_consent_denied`
- `order_hold_applied`
- `order_resumed`
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
- Consignee OTP Verification
- Upload Success
- Upload Retry

### API Path

```text
POST /documents/pod
-> POST /orders/{order_id}/consignee-otp/send
-> POST /orders/{order_id}/consignee-otp/verify
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
- consignee OTP pending
- consignee OTP verified
- consignee OTP failed or expired
- upload failed
- duplicate submission safe retry

### Critical Events

- `pod_uploaded`
- `consignee_otp_sent`
- `consignee_otp_verified`

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
- payment link created
- booking payment pending
- payment initiated
- payment confirmed
- advance paid
- partially paid
- fully paid
- ToPay consent pending
- ToPay consent accepted
- ToPay consent denied
- ToPay collection pending
- ToPay collection received
- order on hold for ToPay or payment resolution
- resume requested and waiting for consignee response
- invoice generated
- invoice pending
- final invoice pending POD
- final invoice pending GST review
- invoice sent
- invoice paid after amount matching
- debit note or credit note generated
- refund initiated or completed
- payment mismatch under review
- settlement visibility pending

## Flow 8: Cross-App Frontend Harness Backtest

### Screens

- Admin Harness Monitor
- Customer Registration / ToPay Resolution
- Driver Offer / Active Trip
- Transport Company Dashboard / Role Context

### API Path

```text
GET /ops/harness/events
-> GET /ops/harness/state-health
-> GET /ops/harness/sla-health
-> GET /ops/harness/verification-health
-> GET /ops/harness/finance-gates
-> GET /ops/harness/offline-sync
```

### Backend Records Touched

- `order_state_events`
- `shipment_events`
- `finance_events`
- `customer_verification_events`
- `topay_consent_events`
- `notifications`
- `driver_alerts`
- `incident_logs`
- `admin_activities`

### UI States

- all frontend apps aligned
- missing canonical event
- illegal or stale state
- SLA timer mismatch
- OTP or verification checkpoint failed
- ToPay consent unresolved
- payment or settlement gate blocked
- offline action awaiting sync
- role-context conflict

### Critical Events

- `topay_consent_denied`
- `order_hold_applied`
- `order_resumed`
- `consignee_otp_verified`
- `driver_no_show_detected`
- `doc_validation_failed`
- `payment_mismatch_under_review`
- `dual_role_toggled`
- `inventory_updated`
- `admin_action_logged`

## MVP Screen-To-Endpoint Summary

| Screen | Main Endpoint |
| --- | --- |
| Customer Registration | `POST /auth/register/customer` |
| OTP Send / Verify | `POST /auth/otp/send`, `POST /auth/otp/verify` |
| Booking Form | `POST /orders` |
| Booking OTP Checkpoint | `POST /orders/{order_id}/otp-checkpoint` |
| Quote View | `POST /orders/{order_id}/quote` |
| ToPay Consent | `POST /orders/{order_id}/topay/consent-request`, `POST /orders/{order_id}/topay/consent-response` |
| Hold / Resume | `POST /orders/{order_id}/hold`, `POST /orders/{order_id}/resume` |
| Payment View | `POST /orders/{order_id}/payment-intent` |
| Customer Tracking | `GET /customer/orders/{order_id}/tracking` |
| Driver Offer List | `GET /drivers/{driver_id}/offers` |
| Driver Accept | `POST /driver-offers/{offer_id}/accept` |
| Active Trip | `GET /trips/{trip_id}` |
| Milestone Submit | `POST /trips/{trip_id}/milestones` |
| POD Upload | `POST /documents/pod` |
| Consignee POD OTP | `POST /orders/{order_id}/consignee-otp/send`, `POST /orders/{order_id}/consignee-otp/verify` |
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
