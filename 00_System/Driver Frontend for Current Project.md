---
type: memo
domain: frontend
scope: driver_mobile
status: active
last_updated: 2026-05-01
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
- payment terms visibility
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
- prolonged halt alert
- route deviation alert
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

- advance payment status
- pending payment status
- settlement completion status
- deductions or commission visibility where relevant

The driver app should not:

- infer finance completion from local actions
- allow manual override of payment state

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
