---
type: memo
domain: frontend
scope: ui_blueprint
status: active
last_updated: 2026-05-01
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
  - "C:\\Users\\user\\Downloads\\frontend ui.txt"
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
CONFIRMED
VEHICLE_SEARCH
DRIVER_ASSIGNED
ARRIVED_PICKUP
LOADING
ENROUTE
ARRIVED_DELIVERY
POD_UPLOADED
DELIVERY_COMPLETED
SETTLEMENT_READY
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
| `DRAFT` | Create Order | pickup/drop, cargo, vehicle, schedule, missing fields | submit order request |
| `PAYMENT_PENDING` | Payment | amount, payment mode, retry info | pay now, cancel if policy allows |
| `CONFIRMED` | Order Confirmed | summary, searching/processing status | cancel if policy allows |
| `VEHICLE_SEARCH` | Searching / Matching | vehicle search status, next update time | view status, contact support if delayed |
| `DRIVER_ASSIGNED` to `ENROUTE` | Live Tracking | map/status, timeline, ETA, driver/provider info if authorized | view only, report issue |
| `ARRIVED_DELIVERY` to `DELIVERY_COMPLETED` | Delivery / POD | delivery status, POD preview, rating/feedback | rate, report issue |
| `SETTLEMENT_READY` / `CLOSED` | Invoice / Receipt | invoice PDF, receipt, POD, download/email | download, email, reorder |
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
| provider opportunity | Received Work | lane, cargo, SLA, earning/service fee, requirements | accept/reject, assign vehicle |
| placed order | Placed Order Tracking | customer-side order status, invoice/payment | track, report issue |
| fleet | Fleet | vehicles, drivers, verification, availability | mark availability, upload documents |
| finance | Finance | provider earnings, customer payments, service fees, settlements | view, download, follow up |

Important:

```text
provider-side earnings and customer-side payments must stay visually and financially separate
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

## Admin Screen Map

| Screen | UI Shows | Allowed Actions |
|---|---|---|
| Admin Dashboard | severe alerts, policy queues, audit indicators | open review |
| Audit Viewer | immutable logs, actor, order, timestamp, action trail | filter, export if authorized |
| Manual Override | rare override workflows | force close, refund trigger, hold release where policy allows |
| User / Role Management | roles, permissions, verification | suspend, reactivate, change role with audit |

Admin override rule:

```text
all admin override actions must be logged, justified, and visible in audit trail
```

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
