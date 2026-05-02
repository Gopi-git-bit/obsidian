---
type: memo
domain: frontend
scope: customer_mobile
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[Business Models Hub]]"
tags:
  - frontend
  - customer
  - mobile
  - booking
  - tracking
  - source-of-truth
source_files:
  - "C:\\Users\\user\\Downloads\\frontend customer.txt"
---

# Customer Frontend for Current Project

## Purpose

This note reshapes the older customer mobile PRD for the current Zippy project state.

The customer app is not a generic shipment booking app anymore. It is the customer-facing surface for a corridor-first logistics operating system.

It must support:

- structured shipment intake
- quote and service-level clarity
- payment-mode visibility
- real-time shipment tracking
- POD, invoice, and payment closure
- customer relationship and retention workflows
- route-performance proof for repeat customers

## Current Customer App Mission

The customer app helps MSMEs, warehouses, factories, and logistics managers:

- place shipment requests accurately
- understand price, promise, and payment responsibility
- track live execution without repeated calls
- receive proactive delay and POD updates
- manage invoices, payments, and shipment history
- see measurable value from Zippy over time

## Current Product Principle

The customer frontend should reduce uncertainty.

It should answer:

```text
what did I book?
what will it cost?
what was promised?
who is executing it?
where is the shipment?
what changed?
where is POD?
what is pending for payment or invoice?
```

## Recommended Navigation

Primary navigation:

- Home
- Book
- Track
- Payments
- Profile

Future/managed-account addition:

- Performance

This can appear later for repeat customers with monthly route reports.

## Current App Structure

```text
Customer App
├── Auth
│   ├── Login
│   └── Registration / Verification
├── Main
│   ├── Home
│   ├── Book Shipment
│   ├── Track Orders
│   ├── Payments
│   └── Profile
├── Modals
│   ├── Quote Details
│   ├── Order Details
│   ├── Document Viewer
│   ├── Issue / Complaint
│   └── Communication Thread
└── Full-Screen Tracking
    ├── Map / Status
    ├── Timeline
    ├── ETA / Delay
    ├── POD / Documents
    └── Contact / Support
```

## Core Screens

## 1. Home Screen

Purpose:

- show the customer what needs attention now

Components:

- company/account header
- active shipment summary
- quick action to book shipment
- payment or invoice blocker status
- recent orders
- next required action
- notification badge

For repeat customers, add:

- route performance snapshot
- pending POD or invoice count
- monthly shipment count
- service health indicator

## 2. Book Shipment Screen

Purpose:

- capture complete and usable shipment demand

Booking steps:

```text
shipment details
-> vehicle requirement
-> pickup and delivery
-> consignee and documents
-> service level and payment mode
-> quote review
-> confirmation
```

Required fields:

- product or cargo type
- weight / volume
- vehicle type and count
- pickup address and time window
- delivery address and deadline
- consignee name and contact
- document requirements
- payment mode
- special handling

Important refinement:

The app should not allow vague booking when core information is missing.

Use smart missing-field prompts:

```text
to quote accurately, please add pickup window, cargo weight, and delivery deadline
```

AI use:

- infer cargo category from description
- detect missing fields
- suggest vehicle class
- warn when shipment details and vehicle choice conflict

## 3. Quote Review Screen

Purpose:

- make price and promise understandable before confirmation

Show:

- base freight
- service-level option
- estimated pickup and delivery window
- payment mode
- detention/waiting policy
- document requirements
- cancellation window
- quote validity
- route or backhaul explanation where relevant

Do not show:

- internal provider payout logic
- confidential carrier margin
- unstable AI-only estimates as final price

Rule:

```text
quote truth comes from backend pricing and policy services
```

## 4. Tracking Screen

Purpose:

- give customer shipment confidence without phone chasing

Show:

- current order status
- driver/provider details when assigned and authorized
- vehicle details
- pickup and delivery timeline
- ETA and promised delivery window
- delay reason and next update time
- map or simplified route view
- POD and document status
- issue/report action

Important UX:

- show honest delay state, not vague optimism
- every delay alert should include next update timing
- avoid overexposing driver/customer contacts before workflow stage allows it

## 5. Payments And Invoices

Purpose:

- make commercial closure clear

Show:

- payment mode
- advance paid / pending
- ToPay responsibility if applicable
- invoice status
- receipts
- POD-linked invoice
- outstanding payment blocker
- transaction history

Rules:

- customers do not see provider settlement internals
- customers should see only their payment obligation and invoice status
- payment completion must come from backend finance events

## 6. Profile And CRM

Purpose:

- keep customer identity, contacts, addresses, and relationship data clean

Sections:

- company profile
- GST/PAN and verification status
- address book
- operational contacts
- billing contacts
- notification preferences
- support and complaints
- saved routes
- satisfaction and feedback history where appropriate

For managed customers:

- assigned relationship owner
- monthly performance reports
- route review schedule

## Customer Notifications

Required notifications:

- order created
- quote ready
- payment required
- vehicle/provider assigned
- truck reached pickup
- loading completed
- in transit
- delay risk
- delivery imminent
- delivered
- POD uploaded
- invoice raised
- payment reminder
- issue resolved

## CRM And Retention Hooks

The customer app should support:

- after-delivery satisfaction survey
- issue category selection
- complaint status tracking
- repeat route shortcuts
- route performance reports
- at-risk customer follow-up tasks for internal users

This connects to:

- [[CRM and Customer Retention Playbook for Zippy Logistics]]
- [[AI Logistics Value Chain Implementation Guide]]

## MVP Scope

Build first:

- login / registration
- company profile
- booking form
- quote review
- order confirmation
- active shipment tracking
- document/POD visibility
- payment and invoice status
- issue reporting

Delay:

- advanced route analytics for all customers
- full managed-service dashboard
- complex address collaboration
- deep customer success automation

## Success Metrics

- booking completion rate
- missing-field reduction
- quote acceptance rate
- tracking view usage
- customer status inquiry reduction
- POD view/download rate
- invoice dispute rate
- repeat shipment rate
- CSAT / NPS / CES

## Bottom Line

The current customer frontend should be treated as:

```text
a shipment booking, tracking, payment, and relationship surface
that turns Zippy's operational truth into customer confidence
```

