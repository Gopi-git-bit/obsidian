---
type: memo
domain: frontend
scope: driver_mobile
status: active
last_updated: 2026-05-31
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[Business Models Hub]]"
tags:
  - frontend
  - driver
  - mobile
  - source-of-truth
source_files:
  - "C:\\Users\\user\\Downloads\\frontend driver.txt"
---

# Driver Frontend for Current Project

## Purpose

This note transforms the older `driver.txt` into the current driver mobile frontend reference for Zippy.

It keeps the durable execution and UX requirements, while aligning them to the current source-of-truth notes for:

- backend-driven workflow truth
- role-aware frontend behavior
- deterministic OMS, TMS, SLA, and payment flows

## Driver App Mission

The driver app is the execution surface for:

- owner-drivers
- drivers attached to transport companies

Its purpose is not to manage the whole marketplace.

Its purpose is to help a driver:

- receive work
- accept or reject it
- execute the trip correctly
- stay aligned with route, SLA, and documentation requirements
- complete delivery and proof-of-delivery workflows

## Current Driver App Principle

The driver app is an execution tool, not a workflow authority.

That means:

- OMS assigns and governs the order lifecycle
- TMS governs route, ETA, and active trip execution logic
- payment and settlement truth comes from backend finance workflows
- the driver app shows and updates only what the driver is allowed to act on

## Main Navigation

## Verification Harness Alignment

The Driver App must stay synchronized with OMS, TMS, IMS, Payment, Verification, Risk, Communication, and DriverOps agents. Every driver-facing action must map to a backend event, state gate, SLA timer, or escalation path.

Harness-critical overlays:

- Express delivery must show a distinct badge, stricter SLA countdown, explicit acceptance confirmation, vehicle-age/driver-score eligibility where exposed, and elevated commission context returned by backend pricing.
- ToPay consent must be visible before departure. Driver should see `pending`, `accepted`, `denied`, or `expired/timeout`; rejected or expired consent must trigger wait-for-consignor, return-to-consignor, or support escalation options returned by OMS.
- Driver no-movement after acceptance must show the movement timeout and escalation status; the app cannot silently keep the order assigned when TMS/OMS has raised reassignment risk.
- Loading/unloading waiting time must show a timer and backend-calculated late-fee eligibility; the app records evidence but does not calculate final charges locally.
- VTU/telematics and phone GPS mismatch must surface as an integrity warning when backend detects it. VTU should be treated as authoritative when backend policy says so.
- Transit damage reporting must capture timestamped, geotagged photos, a short description, and sync/evidence status. Settlement remains blocked until verification/risk review clears.
- Owner-driver, fleet owner, and salaried driver permissions must be role-aware. Every action must log `actor_id` and `actor_role`.
- Offline mode must preserve trip context, document scans, POD capture, timestamps, GPS metadata, and sync status without pretending backend transitions succeeded.
- Fatigue/night-driving alerts should appear when configured by TMS policy and must include rest guidance or escalation state from backend.

Recommended primary navigation:

- Home
- Orders
- Trip
- Notifications
- Profile

Important refinement from the old draft:

- `Inventory` does not need to remain a top-level driver navigation item in the same sense as an admin or ops view
- for the driver, vehicle availability is better represented through:
  - current vehicle status
  - online or offline state
  - assigned or available state

## App Structure

```text
Driver App
├── Auth
│   ├── Login
│   └── Registration / Verification
├── Main
│   ├── Home
│   ├── Orders
│   ├── Active Trip
│   ├── Notifications
│   └── Profile
├── Modals
│   ├── Accept / Reject Order
│   ├── Document Viewer
│   ├── Upload Confirmation
│   └── Alert Details
└── Full-Screen Trip Mode
    ├── Route
    ├── Status Actions
    ├── Contact Access
    └── POD / Document Actions
```

## Core Screens

## 1. Home Screen

Purpose:

- give the driver fast operational awareness

Key components:

- current vehicle and driver status
- online or offline toggle
- current assignment summary if any
- quick stats
  - earnings today
  - trips completed
  - current payment status
- action shortcuts
  - view new orders
  - open active trip
  - view pending documents

Useful additions:

- support or emergency access
- weather or route conditions only if operationally relevant

## 2. Orders Screen

Purpose:

- show available assignments and order history relevant to the driver

Recommended sections:

- New Offers
- Assigned
- Completed
- Rejected / Missed

For each offer, show:

- pickup and destination summary
- cargo summary
- vehicle-fit relevance
- service level
- payment-mode visibility: Full Payment, Part Payment, ToPay, Credit, or approved custody/hold model
- expected earning preview
- deduction preview: driver commission, penalties, claims, or waiting-time share where applicable
- payout readiness blockers, if already known
- promised timeline

Driver actions:

- accept
- reject
- ignore

Important current-context rule:

Accepting an order should be treated as:

```text
driver acceptance signal
-> OMS assignment flow
-> trip creation and TMS execution
```

not as direct self-assignment.

## 3. Active Trip Screen

Purpose:

- become the full-screen operational cockpit during trip execution

Key sections:

- route and next step
- ETA and promised window
- trip progress
- pickup and delivery milestones
- authorized contact access
- alerts and escalation status
- required document actions

Status actions should be structured, not free-form:

- arrived at pickup
- loading started
- loading completed
- departed origin
- arrived delivery
- POD uploaded
- trip completed

These actions should map to backend-approved state or event transitions.

## 4. Notifications Screen

Purpose:

- show all operationally relevant alerts and messages

Categories:

- order offers
- trip updates
- payment updates
- document requirements
- system alerts
- incident or route alerts

Important driver-specific notifications:

- new order offer
- assignment confirmed
- express delivery SLA commitment
- ToPay consent denied, expired, or resolved before departure
- prolonged halt alert
- route deviation alert
- VTU/phone GPS mismatch alert
- no-movement timeout after acceptance
- fatigue or mandatory rest alert where configured
- transit damage evidence review update
- ETA risk or delay update
- pending document upload reminder

## 5. Profile Screen

Purpose:

- manage driver identity and execution readiness

Key sections:

- personal profile
- driver verification status
- linked vehicle info
- company affiliation if applicable
- rating summary
- language and app preferences
- logout and support

Useful operational elements:

- document verification indicators
- active role context
- contact and emergency preferences

## Driver Workflow

## 1. Assignment Flow

```text
driver receives order offer
-> reviews summary
-> accepts or rejects
-> OMS confirms assignment
-> TMS opens trip execution context
```

## 2. Pickup Flow

```text
navigate to pickup
-> confirm arrival
-> loading begins
-> scan invoice or challan if required
-> confirm loading completion
```

## 3. In-Transit Flow

```text
follow route
-> receive ETA and alert updates
-> handle route deviations or halts
-> notify if issue or incident occurs
```

## 4. Delivery Flow

```text
arrive at destination
-> unload
-> scan receipt or POD
-> confirm delivery completion
```

## 5. Completion Flow

```text
trip closes
-> vehicle becomes available through backend workflow
-> payment and settlement status update appears in driver app
```

## Contact Visibility Rules

The old draft exposed contact-sharing broadly.

Current-context interpretation:

- contact visibility must be role-based and workflow-based
- the driver should see only the contact data needed for active execution
- visibility should depend on assignment and trip stage

This includes possible access to:

- consignor contact
- consignee contact
- transport-company coordinator contact

when operationally necessary and backend-authorized.

## Payment Visibility Rules

The driver app should show:

- customer payment gate status only where it affects dispatch or payout readiness
- ToPay consent status before departure where it affects movement authorization
- expected earning
- commission deducted from driver payout
- demurrage or waiting compensation if collected and approved
- payout readiness state
- settlement hold reason when visible to the driver
- payout initiated, payout successful, payout failed, and settlement slip states
- ToPay collection pending when consignee payment blocks payout
- dispute, claim, POD, GST, or bank-verification blocker summaries

The driver app should not:

- infer finance completion from local actions
- allow manual override of payment state
- describe POD upload as automatic payout release
- expose customer invoice internals beyond what affects driver execution or payout

Driver payout states:

```text
earning_estimated
payment_gate_pending
trip_in_progress
pod_uploaded
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

Driver-visible harness statuses:

```text
express_sla_active
topay_consent_pending
topay_consent_denied
movement_timeout_warning
loading_wait_timer_active
damage_report_submitted
telemetry_mismatch_under_review
offline_sync_pending
fatigue_alert_active
```

Settlement hold copy:

```text
Payout is on hold until required payment, POD, dispute, bank, GST, or compliance checks are cleared.
```

Completion-to-payout flow:

```text
delivery completed
-> POD uploaded
-> POD verified by backend workflow
-> final invoice and payment obligation checked
-> settlement preprocessing starts
-> commission, penalties, demurrage share, and claim adjustments calculated
-> payout readiness computed
-> disbursement starts only after payment, dispute, bank, custody, and compliance gates clear
-> payout success and reconciliation update driver app
```

ToPay rule:

```text
For ToPay orders, driver completion and POD upload do not mean payout is ready.
Payout remains blocked until consignee collection is received or an admin-approved finance policy resolves the obligation.
```

## Document Handling

The driver app should support:

- invoice or challan scan at loading when required
- POD or receipt scan at delivery
- upload progress and verification state
- document retry or re-upload where needed

Document UX should emphasize:

- clarity
- low-friction capture
- offline tolerance if possible
- clear success or failure states

## Alerts And Safety

The current database and control-tower model now includes `driver_alerts`.

The driver frontend should surface alerts such as:

- long halt
- route deviation
- breakdown
- accident
- GPS loss
- temperature deviation when applicable

Driver-side response patterns:

- acknowledge
- view details
- call support
- follow guided next step

## Offline And Weak Network Behavior

Driver workflows often happen in weak-connectivity environments.

Important behaviors:

- preserve local trip context
- queue non-destructive updates where safe
- clearly show sync status
- avoid pretending a backend-confirmed transition happened when it has not synced

Offline conflict rule:

```text
local evidence can queue, but assignment, payment, POD verification, settlement, and cancellation truth must refresh from backend after reconnect.
```

## Driver Harness Backtest Cases

| Test ID | Scenario | Required Driver UI Evidence |
|---|---|---|
| T-DRV-01 | Express offer accepted | express badge, SLA countdown, backend earning preview |
| T-DRV-02 | ToPay denied before departure | consent status, wait/return/escalate options |
| T-DRV-03 | Driver accepts but does not move | movement timer, alert, reassignment state |
| T-DRV-04 | Loading delay crosses grace period | wait timer, evidence event, fee review status |
| T-DRV-05 | VTU and phone GPS mismatch | telemetry warning, backend review status |
| T-DRV-06 | Offline POD captured and synced | local evidence, sync pending, backend accepted/rejected result |
| T-DRV-07 | Transit damage reported | geotagged evidence, incident status, settlement hold |
| T-DRV-08 | Salaried driver tries owner-only action | action hidden or blocked with role-safe reason |

## Driver UX Priorities

The driver app should optimize for:

- speed
- clarity
- large touch targets
- low reading burden while on the move
- minimal distraction during active trip

The trip screen especially should feel like:

```text
operational cockpit
not generic app dashboard
```

## What Was Kept From The Old Driver Draft

- home, orders, notifications, profile structure
- execution-first order flow
- document scanning requirements
- route and map support
- alerting for prolonged stops
- payment status visibility
- profile and verification context

## What Was Refined

- inventory moved away from being treated as a driver-control domain
- assignment authority clarified as backend-owned
- contact-sharing constrained by authorization and workflow stage
- trip execution reorganized as a structured active-trip surface
- payment treated as visibility, not driver-controlled workflow truth

## Related Current Notes

Use this note with:

- [[Current Project Navigation Hub]]
- [[Frontend Architecture for Current Project]]
- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Zippy Logistics Operational Core Schema]]
- [[On-Time Delivery Control Tower Strategy for Multimodal Freight]]

## Bottom Line

The current driver frontend should be treated as:

```text
a mobile execution cockpit for assigned transport work
with route, status, document, alert, and payment visibility
backed by OMS, TMS, SLA, and finance truth from the backend
```

That is the driver frontend to build against now.
