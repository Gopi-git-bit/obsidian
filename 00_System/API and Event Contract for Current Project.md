---
type: memo
domain: architecture
scope: api_and_event_contract
status: active
last_updated: 2026-05-31
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
POST   /auth/register/customer
POST   /auth/otp/send
POST   /auth/otp/verify
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

`POST /auth/register/customer` minimum request:

```json
{
  "customer_segment": "organized_company | individual_unorganized",
  "company_name": "string or null",
  "gst_number": "string or null",
  "business_pan": "string or null",
  "person_or_trade_name": "string or null",
  "aadhaar_or_kyc_ref": "string or null",
  "email": "string or null",
  "phone": "string",
  "address": {},
  "authorized_person_name": "string or null",
  "authorized_person_mobile": "string or null"
}
```

Registration rules:

- `organized_company` requires company identity, company email OTP, phone number, address, and authorized-person details.
- `individual_unorganized` hides GST/company/PAN requirements and requires person or trade name, phone OTP, address, and Aadhaar/KYC reference.
- OTP verification state must be stored as backend truth and exposed to the app as `pending | verified | failed | expired`.

### Customer Order Flow

```text
POST   /orders
GET    /orders/{order_id}
GET    /orders
POST   /orders/{order_id}/quote
POST   /orders/{order_id}/otp-checkpoint
POST   /orders/{order_id}/topay/consent-request
POST   /orders/{order_id}/topay/consent-response
POST   /orders/{order_id}/hold
POST   /orders/{order_id}/resume
POST   /orders/{order_id}/payment-intent
POST   /orders/{order_id}/transition
```

`POST /orders` minimum request:

```json
{
  "origin_city": "Tiruppur",
  "destination_city": "Chennai",
  "customer_segment": "organized_company | individual_unorganized",
  "pickup_window_start": "ISO",
  "pickup_window_end": "ISO",
  "material_type": "textile_cartons",
  "vehicle_type_preference": "17ft_closed_body",
  "service_level": "standard",
  "payment_mode": "advance | full | topay",
  "consignor": {},
  "consignee": {
    "name": "string",
    "phone": "string",
    "address": {},
    "company_name": "string or null",
    "gst_number": "string or null"
  },
  "documents": []
}
```

Order booking identity rules:

- Organized-company bookings require company or billing profile, authorized person, consignor address, phone, and email OTP checkpoint before submission can move forward.
- Individual/unorganized bookings require phone OTP checkpoint before submission can move forward; GST number, company name, and company PAN must not be required.
- ToPay bookings require consignee payer details before quote confirmation.

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

`POST /orders/{order_id}/topay/consent-request` minimum request:

```json
{
  "consignee_name": "string",
  "consignee_phone": "string",
  "message_channel": "whatsapp | sms",
  "idempotency_key": "string"
}
```

`POST /orders/{order_id}/topay/consent-response` minimum request:

```json
{
  "response": "yes | no",
  "actor_role": "consignee",
  "payment_intent_id": "UUID or null",
  "idempotency_key": "string"
}
```

ToPay behavior:

- `yes` opens or confirms the consignee payment path and may progress only when payment or policy gate clears.
- `no` redirects the obligation to the consignor, who may pay full amount, cancel, or place the order on hold for negotiation.
- Hold/resume are explicit commands; resume resends consignee consent and creates a new consent attempt without erasing the earlier denial event.

`POST /orders/{order_id}/hold` minimum request:

```json
{
  "hold_type": "topay_consent | payment_resolution | document | compliance | dispute",
  "reason": "string",
  "actor_role": "customer | admin | ops",
  "actor_id": "UUID",
  "idempotency_key": "string"
}
```

`POST /orders/{order_id}/resume` minimum request:

```json
{
  "resume_action": "resend_topay_consent | retry_payment | continue_order",
  "actor_role": "customer | admin | ops",
  "actor_id": "UUID",
  "idempotency_key": "string"
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
POST   /orders/{order_id}/consignee-otp/send
POST   /orders/{order_id}/consignee-otp/verify
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

Consignee POD OTP rule:

- After POD scanning/upload, consignee phone OTP must be verified before delivery completion and revenue/settlement gates can treat the delivery as fully evidenced.
- The frontend must render OTP pending, verified, failed, or expired from backend response data.

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

Minimum customer payment response shape:

```json
{
  "order_id": "UUID",
  "payment_mode": "advance | full | topay | credit",
  "payer": "consignor | consignee | approved_credit_account",
  "payment_status": "payment_not_started | payment_link_created | booking_payment_pending | advance_paid | partially_paid | fully_paid | topay_consent_pending | topay_consent_accepted | topay_consent_denied | topay_collection_pending | topay_collection_received | on_hold_topay_consent | on_hold_payment_resolution | resumed_topay_consent_requested | credit_approved_due_later | payment_failed | payment_mismatch_under_review | refund_initiated | refund_completed",
  "amount_due_now": 0,
  "amount_paid": 0,
  "remaining_balance": 0,
  "next_action": "none | pay_now | wait_for_consignee | resend_consent | choose_pay_cancel_or_hold | retry_payment | contact_support"
}
```

Minimum customer invoice response shape:

```json
{
  "order_id": "UUID",
  "invoice_status": "proforma_generated | receipt_generated | final_invoice_pending_pod | final_invoice_pending_gst_review | final_tax_invoice_generated | invoice_sent | invoice_paid | debit_note_generated | credit_note_generated",
  "download_url": "string or null"
}
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
TOPAY_CONSENT_PENDING
TOPAY_CONSENT_DENIED
ON_HOLD
RESUMED
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

Hold-state rule:

- `ON_HOLD` is a controlled pause state used for ToPay denial, payment resolution, document/compliance blockers, or dispute review.
- `RESUMED` records the restart event after a hold and must immediately route to the next legal policy gate, such as ToPay consent pending, payment pending, matching, or cancellation.
- The event trail must preserve every hold reason, resume reason, and ToPay consent attempt.

## Canonical Event Families

### Order State Events

- `order_created`
- `customer_registered`
- `otp_sent`
- `otp_verified`
- `order_booking_otp_verified`
- `quote_generated`
- `topay_consent_requested`
- `topay_consent_accepted`
- `topay_consent_denied`
- `order_hold_applied`
- `order_resumed`
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
- `consignee_otp_sent`
- `consignee_otp_verified`

### Finance Events

- `payment_initiated`
- `payment_confirmed`
- `payment_failed`
- `payment_mismatch_under_review`
- `advance_payment_received`
- `topay_collection_pending`
- `topay_collection_received`
- `refund_initiated`
- `refund_completed`
- `invoice_generated`
- `invoice_sent`
- `invoice_paid`
- `debit_note_generated`
- `credit_note_generated`
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
