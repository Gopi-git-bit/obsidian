---
type: memo
domain: frontend
scope: ui_blueprint
status: active
last_updated: 2026-05-31
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
tags:
  - frontend
  - ui-blueprint
  - state-driven-ui
  - mobile
  - web
  - source-of-truth
source_files:
  - "C:\Users\user\Downloads\frontend ui.txt"
  - "C:\Users\user\Downloads\new -chatgpt  (1).txt"
---

# Frontend UI Blueprint for Current Project

## Purpose

This note reframes the UI blueprint from `frontend ui.txt` for the current Zippy project.

The useful idea from the source is:

```text
frontend screens should be driven by backend workflow state
```

This means the UI does not decide business truth.

It displays the current state and sends allowed action requests to the backend.

## Authority Status

This note is the canonical frontend contract for state-driven UI behavior in the current project.

Role-specific frontend notes are supporting notes.

Raw screen PRDs and chat extracts remain reference inputs unless their rules are restated here or in another canonical current-project note.
## Non-Negotiable UI Rules

1. Frontend never changes order, trip, payment, settlement, or audit state locally.
2. UI buttons are requests, not decisions.
3. Backend transition or service response is the source of truth.
4. If the backend rejects a requested action, the UI must show the rejection and refresh state.
5. Mobile local state is only for UX continuity and evidence capture, not business authority.
6. Every high-risk action should show clear confirmation, owner, and consequence.

Core rule:

```text
frontend requests
backend decides
frontend renders
```

## Responsibility Boundaries

| Layer | Responsibility |
|---|---|
| Screen | layout, workflow presentation, user intent capture |
| Component | reusable UI rendering |
| Hook | data fetching, mutation calls, realtime subscriptions |
| SDK/API client | typed backend contract |
| Backend service | workflow decision and state transition |
| Policy layer | lifecycle, role, payment, SLA, and safety rules |
| Event log | audit trail and state history |

No component should bypass the hook/API layer to invent state.

## State-Driven Screen Model

The UI should map workflow state to the correct screen or screen section.

Recommended operational state families:

```text
DRAFT
PAYMENT_PENDING
PAYMENT_GATE_SATISFIED
CONFIRMED
VEHICLE_SEARCH
DRIVER_ASSIGNED
ARRIVED_PICKUP
LOADING
ENROUTE
ARRIVED_DELIVERY
POD_UPLOADED
DELIVERY_COMPLETED
INVOICE_PENDING
INVOICE_SENT
SETTLEMENT_PREPROCESSING
SETTLEMENT_ON_HOLD
SETTLEMENT_READY
PAYOUT_INITIATED
PAYOUT_SUCCESSFUL
SETTLEMENT_RECONCILED
CLOSED
FAILED
CANCELLED
```

The exact backend enum can evolve, but the frontend must not create private business states that contradict backend truth.

## Customer App UI Blueprint

Customer goals:

- place order
- pay or confirm payment responsibility
- track vehicle
- access documents
- raise issue
- view history and invoices

## Customer Screen Map

| State / Condition | Screen | UI Shows | Allowed Customer Actions |
|---|---|---|---|
| always | Customer Home | active orders, past orders, create order CTA, blockers | create order, open order |
| registration | Registration / Verification | organized-company vs individual/unorganized segment, required OTP/KYC status | submit profile, verify OTP |
| `DRAFT` | Create Order | pickup/drop, cargo, vehicle, schedule, payer, GST/billing inputs, missing fields | submit order request |
| quote ready | Quote / Proforma | quote, payment mode, payer, proforma status, GST classification, invoice ownership | accept quote, edit, cancel |
| `PAYMENT_PENDING` | Payment | amount, payment mode, payer responsibility, retry info, ToPay consent or credit gate | pay now, request ToPay consent, cancel if policy allows |
| ToPay denied or on hold | ToPay Resolution | consignee denial, consignor pay/cancel/hold choices, resume state | pay full amount, cancel, hold, resume |
| `PAYMENT_GATE_SATISFIED` | Confirmation Pending | payment/authorization/ToPay/credit gate satisfied, backend confirmation pending | wait, refresh, contact support |
| `CONFIRMED` | Order Confirmed | summary, searching/processing status | cancel if policy allows |
| `VEHICLE_SEARCH` | Searching / Matching | vehicle search status, next update time | view status, contact support if delayed |
| `DRIVER_ASSIGNED` to `ENROUTE` | Live Tracking | map/status, timeline, ETA, driver/provider info if authorized | view only, report issue |
| `ARRIVED_DELIVERY` to `DELIVERY_COMPLETED` | Delivery / POD | delivery status, POD preview, final invoice pending state, rating/feedback | rate, report issue |
| `INVOICE_PENDING` / `INVOICE_SENT` | Invoice / Payment Closure | final invoice status, GST review, invoice sent, payment obligation, receipt | pay balance, download, email |
| `SETTLEMENT_READY` / `CLOSED` | Invoice / Receipt | invoice PDF, receipt, POD, payment closed, download/email | download, email, reorder |
| `FAILED` / `CANCELLED` | Failed / Cancelled | reason, refund/payment status, support CTA | reorder, contact support |

Important:

```text
tracking is mostly read-only for customers
```

Customer actions should never directly move trip execution states.

## Driver App UI Blueprint

Driver goals:

- receive work
- accept or reject
- navigate and execute
- capture evidence
- upload POD
- view earnings or settlement status

## Driver Screen Map

| State / Condition | Screen | UI Shows | Allowed Driver Actions |
|---|---|---|---|
| always | Driver Home | online/offline, active job, earnings summary, sync status | toggle availability, open job |
| `DRIVER_ASSIGNED` | Incoming Order | pickup/drop, distance, load, timeline, earning preview | accept, reject |
| express offer | Incoming Order | express badge, SLA countdown, earning/commission context | accept express, reject |
| ToPay pending/denied before departure | Trip Gate | consent status, dispatch blocker, support state | wait, return/escalate if allowed |
| accepted / going pickup | Pickup | address, route, authorized contact, instructions | arrived pickup |
| `ARRIVED_PICKUP` | Pickup Arrival | pickup details, document checklist | start loading |
| `LOADING` | Loading | timer, notes, document scan if needed | depart origin |
| `ENROUTE` | Navigation | map/navigation, ETA, alerts, support | issue alert, view route |
| `ARRIVED_DELIVERY` | Delivery | delivery details, camera/POD action | upload POD |
| `POD_UPLOADED` / `DELIVERY_COMPLETED` | Job Complete | summary, payout preview/status | close view |

Important:

```text
driver actions create event/transition requests; backend validates legality
```

## Transport Company UI Blueprint

Transport-company goals:

- manage company capacity
- receive work as provider
- place work as customer
- assign verified vehicles/drivers
- track company finance without mixing roles

## Transport Company Screen Map

| Context | Screen | UI Shows | Allowed Actions |
|---|---|---|---|
| always | Dashboard | role context, active work, available fleet, blockers | switch context, open queues |
| provider opportunity | Received Work | lane, cargo, SLA, earning, service fee, payout blockers, requirements | accept/reject, assign vehicle |
| placed order | Placed Order Tracking | customer-side order status, payer, invoice/payment, ToPay or credit state | track, pay/follow up, report issue |
| fleet | Fleet | vehicles, drivers, verification, availability | mark availability, upload documents |
| finance | Finance | provider earnings, customer payments, service fees, invoices, holds, settlements | view, download, follow up |

Important:

```text
provider-side earnings and customer-side payments must stay visually and financially separate
```

Transport-company finance states:

```text
Placed Order:
proforma_generated
payment_link_created
advance_paid
partially_paid
fully_paid
topay_consent_pending
topay_consent_accepted
topay_consent_denied
topay_collection_pending
topay_collection_received
on_hold_topay_consent
on_hold_payment_resolution
resumed_topay_consent_requested
credit_due
final_tax_invoice_generated
invoice_paid
```

```text
Received Work:
pod_under_review
settlement_preprocessing
settlement_on_hold
settlement_ready_for_disbursement
payout_initiated
payout_successful
payout_failed
settlement_reconciled
settlement_closed
```

## Ops UI Blueprint

Ops goals:

- monitor orders
- own exceptions
- keep workflow moving
- intervene only through approved controls

## Ops Screen Map

| State / Condition | Screen | UI Shows | Allowed Ops Actions |
|---|---|---|---|
| always | Ops Dashboard | orders by state, alerts, KPI tiles, aging queues | open queue, assign owner |
| all states | Order Detail | full timeline, customer, driver/provider, audit trail | add note, request action |
| failed/stuck | Exception Handling | failure reason, recommended actions, owner | retry assignment, escalate |
| active trips | Trip Monitor | ETA risk, alerts, route status, driver status | contact, incident, escalation |
| finance blockers | Finance Queue | payment, invoice, settlement blockers | request follow-up, escalate |

Ops should see more than customers/drivers, but still should not bypass backend policy.

## Admin UI Blueprint

Admin goals:

- supervision
- compliance
- audit
- controlled override
- cross-app harness monitoring

## Admin Screen Map

| Screen | UI Shows | Allowed Actions |
|---|---|---|
| Admin Dashboard | severe alerts, policy queues, audit indicators | open review |
| Harness Monitor | event registry health, state transition health, SLA timer health, verification health, finance gate health, offline sync health | inspect, assign owner, request retry, escalate |
| Audit Viewer | immutable logs, actor, order, timestamp, action trail | filter, export if authorized |
| Manual Override | rare override workflows | force close, refund trigger, hold release where policy allows |
| User / Role Management | roles, permissions, verification | suspend, reactivate, change role with audit |

Admin override rule:

```text
all admin override actions must be logged, justified, and visible in audit trail
```

Harness rule:

```text
Admin Web proves that Customer, Driver, and Transport Company app actions map to canonical backend events, state transitions, SLA timers, verification checkpoints, and finance gates.
```

Admin Web must render ToPay denial/hold/resume, OTP checkpoints, driver telemetry conflicts, transport-company dual-role conflicts, and finance blockers from backend truth rather than local assumptions.

## Web First, Mobile Derived

The source proposes a useful build order:

```text
web reference UI first
mobile execution UI second
```

Current interpretation:

- admin/ops web should be the authoritative control-tower surface
- customer and driver mobile should use the same API contracts and workflow states
- transport-company app can be mobile or responsive web depending on rollout priorities

Recommended shared packages:

```text
shared/
  api-client/
  hooks/
  contracts/
  status-mapping/
  validation/
  formatters/
  ui-tokens/
```

## Recommended Web Structure

```text
web/
  src/
    app/
    api/
    hooks/
    screens/
      customer/
      ops/
      admin/
      transport-company/
    components/
      OrderStatusTimeline
      OrderActions
      AlertBanner
      MapView
      DocumentPreview
      FinanceStatus
    contracts/
```

## Recommended Mobile Structure

```text
mobile/
  apps/
    customer/
    driver/
    transport-company/
  shared/
    api/
    hooks/
    realtime/
    components/
    contracts/
    offline/
```

## State-Safe Action Buttons

Action buttons should be displayed only when:

- current backend state allows the action
- current user role allows the action
- required data is present
- network/offline rules allow the request

Even then, the button only requests the action.

Example pattern:

```text
if backend says action is allowed:
  render button
on press:
  call transition/request endpoint
  show pending
  refresh authoritative state
else:
  hide or disable action with reason
```

Preferred API shape:

```text
GET order detail -> includes current state and allowed_actions
POST action request -> backend validates and emits event
```

## Finance State Rendering Contract

Payment, invoice, settlement, and payout states must render from finance events, not inferred lifecycle shortcuts.

Required frontend distinctions:

- `payment_gate_satisfied` is not the same as `fully_paid`.
- `proforma_generated` is not the same as `final_tax_invoice_generated`.
- `invoice_sent` is not the same as `invoice_paid`.
- `pod_verified` is not the same as `settlement_ready_for_disbursement`.
- `settlement_ready_for_disbursement` is not the same as `payout_successful`.
- `payout_successful` is not the same as `settlement_reconciled` or `settlement_closed`.

Common payment-mode state text:

```text
Full Payment:
pay full required amount -> payment gate satisfied -> order confirmed

Part Payment:
pay required advance/authorization -> balance remains due by policy -> final payment clears before release point

ToPay:
consignee consent pending -> collection pending -> collection received or obligation resolved

Credit:
credit approved -> due later -> overdue or paid
```

GST and invoice UI rules:

```text
Do not ask users to choose GST rate.
Show GST classification, review state, and invoice owner returned by backend.
If marketplace mode applies, show partner freight invoice and Zippy service invoice separately.
If principal/GTA mode applies, show Zippy freight invoice.
```

## Frontend API Contract

The source `new -chatgpt  (1).txt` adds a useful frontend contract rule:

```text
there should be one frontend write path for lifecycle transitions
```

Recommended frontend-visible endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /orders/{order_id}` | read authoritative order state |
| `GET /orders/{order_id}/timeline` | read event/timeline history |
| `POST /orders/{order_id}/transition` | request lifecycle transition |
| `POST /orders/{order_id}/documents` | upload documents/evidence |
| `GET /orders/{order_id}/allowed-actions` | optional explicit action map |

Transition request should include:

- new state or action name
- event
- actor role
- idempotency key
- optional evidence reference

Frontend must not retry transition mutations automatically.

If a transition fails:

- show backend reason
- refresh authoritative state
- let the user or operator decide next action

## Shared Frontend Hooks Contract

Web and mobile should share the same conceptual hooks:

- read-only order query
- transition mutation
- order realtime subscription
- driver location subscription
- document upload mutation

Rules:

- read hooks may poll or subscribe
- transition hook is the only lifecycle write path
- transition mutations must have retry disabled by default
- realtime updates may refresh cache but must not infer next state
- optimistic UI may show loading, but not optimistic lifecycle state

## Offline Driver Strategy

Driver offline support is required, but must be evidence-only.

Allowed offline:

- view cached active job
- use device navigation
- capture location points
- capture POD photo
- store notes and timestamps
- show local progress helper

Not allowed offline:

- final state transitions
- payment actions
- settlement confirmation
- admin overrides

Local-only states:

```text
LOCAL_ACTIVE_JOB
LOCAL_ENROUTE
LOCAL_AT_PICKUP
LOCAL_AT_DELIVERY
LOCAL_POD_CAPTURED
LOCAL_SYNC_PENDING
```

These are UX helper states only.

Backend state remains authoritative.

## Offline Persistence

Persist locally:

- order ID
- cached trip summary
- local evidence events
- timestamps
- GPS metadata
- POD file path
- sync status
- idempotency keys

Use:

- device storage for metadata
- file system for photos
- SQLite if the workflow becomes more complex

## Offline Sync Order

Strict sync sequence:

1. Upload POD files.
2. Upload location batches.
3. Upload event metadata.
4. Request backend transition.
5. Refresh order/trip state.

If a step fails, stop and retry later.

Do not continue to later sync steps blindly.

## Conflict Handling

| Scenario | UI Behavior |
|---|---|
| backend already advanced | drop or mark local event as already satisfied |
| backend cancelled order | stop sync and show backend state |
| duplicate POD | rely on backend idempotency |
| GPS overlap | backend deduplicates |
| transition rejected | show reason and refresh |

Frontend does not resolve business conflicts.

It shows the backend result.

## SMS Fallback Rule

SMS can be useful for low-connectivity driver communication, but it must be notification-only.

SMS may notify:

- new job assigned
- important address or instruction change
- customer cancellation
- escalation/support message

SMS must not:

- mutate state
- include transition commands
- include secrets or tokenized links
- include payment links
- expose full sensitive address details unless policy approves it

SMS behavior:

```text
SMS wakes the driver
driver opens app
app syncs and fetches authoritative state
backend decides allowed next action
```

## Driver Location Stream Contract

Driver location is passive telemetry.

Frontend may:

- render driver marker
- show last updated time
- show stale location indicator
- freeze marker when realtime disconnects

Frontend must not:

- infer ETA from location unless backend provides ETA
- advance trip state from GPS position
- mark pickup or delivery complete from location alone
- fake movement if stream stops

Location payload should include:

- driver ID
- order/trip ID where applicable
- latitude
- longitude
- accuracy
- recorded timestamp
- source

If location is stale, show it clearly.

Do not hide uncertainty.

## Realtime And Sync UX Indicators

Every app should clearly show:

- offline
- syncing
- sync failed
- all data synced
- backend rejected action
- stale data warning

Drivers especially must never be shown fake certainty.

## UI Test Checklist

Test:

- customer organized-company registration requires email OTP and company identity fields
- customer individual/unorganized registration hides GST/company/PAN and requires phone OTP plus KYC reference
- ToPay accept, deny, hold, resume, and collection states render consistently across Customer, Driver, Transport Company, and Admin surfaces
- driver express delivery, movement timeout, VTU/GPS mismatch, transit damage, and offline sync states render with backend status
- transport-company GST/landline verification, TCRS, role toggle, dual-role conflict, and payment-path states render with backend status
- Admin Harness Monitor shows event, state, SLA, verification, finance, offline sync, and notification health
- every state renders the correct screen
- action buttons appear only for allowed role and state
- rejected backend transitions are handled
- stale state refresh works
- driver offline POD capture works
- sync failure and retry states work
- customer tracking is read-only
- finance status is backend-driven
- admin overrides require confirmation and audit reason
- transport-company role context stays separated
- transition hook does not retry automatically
- realtime update only mirrors backend event
- driver location stream cannot mutate order state
- stale location warning appears
- backend rejection refreshes state

## What To Ignore From The Source

The source claims the full stack is already complete and enterprise-ready.

Current project reality:

- frontend implementation is not yet present in the workspace
- backend exists as prototype code and needs alignment
- these UI blueprints are implementation guidance, not proof of implementation

Use this note as a build specification, not as a completed-status claim.

## Bottom Line

The current frontend UI should be:

```text
state-driven
role-aware
backend-sovereign
offline-safe
audit-friendly
and designed around the order-to-POD-to-settlement workflow
```

That is the UI blueprint to build against now.
