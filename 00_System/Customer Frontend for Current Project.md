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
- payment mode and payer responsibility
- GST/PAN profile, freight payer, and billing contact where required
- special handling

Payment-mode section:

- Full Payment: customer pays the full required amount before OMS confirms the order.
- Part Payment: customer pays the required advance or authorization before confirmation; balance remains visible as receivable until cleared by policy.
- ToPay: consignor selects consignee as payer; the app must collect consignee name, phone, address, consent status, and payment reminder channel before confirmation.
- Credit: visible only for approved customers with a credit limit, due date, and backend policy approval.
- Escrow/Hold: visible only when the approved custody model supports it; do not describe it as Zippy freely holding funds unless compliance approval exists.

Payment-gate copy:

```text
Your shipment is confirmed only after the required payment condition is satisfied.
For ToPay or Credit orders, confirmation depends on approved payer consent, credit policy, and backend finance checks.
```

GST and billing inputs:

- The app should ask for company GST/PAN, billing address, freight payer, and consignee payer details where applicable.
- The app should not ask the customer to choose a GST slab.
- GST handling is auto-classified from supplier type, customer profile, freight payer, goods category, document basis, and effective rule version.
- If supplier ownership, freight payer, or tax mode is unclear, show `GST review pending` and block final invoice readiness.

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
- proforma invoice amount
- GST classification status
- billing model: partner freight invoice, Zippy platform/service invoice, or Zippy freight invoice
- estimated pickup and delivery window
- payment mode
- payer: consignor, consignee, approved credit account, or regulated payment partner
- required booking payment or authorization
- remaining balance rule
- ToPay consent state if applicable
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

Invoice rule:

```text
Quote review may show a proforma invoice or payment link.
It must not describe the proforma as the final GST invoice.
Final tax invoice appears only after delivery/POD or other taxable-supply confirmation and GST ownership checks.
```

Confirmation flow:

```text
quote accepted
-> proforma invoice generated
-> payment intent or approved ToPay/Credit obligation created
-> required payment gate satisfied
-> OMS confirms order
-> assignment and dispatch workflow starts
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
- payer responsibility
- required booking payment status
- advance paid / pending
- balance due and due trigger
- ToPay consent and collection status if applicable
- credit due date and exposure status if applicable
- proforma invoice status
- final tax invoice status
- freight invoice owner
- Zippy platform/service invoice if invoice split applies
- receipts
- POD-linked invoice
- outstanding payment blocker
- transaction history
- debit notes, credit notes, demurrage charges, or refund status where applicable

Rules:

- customers do not see provider settlement internals
- customers should see only their payment obligation and invoice status
- payment completion must come from backend finance events
- `invoice_sent` means the document was delivered; it does not mean payment is complete.
- `invoice_paid` means the payment obligation is cleared only when amount matching and backend finance checks pass.
- ToPay orders remain `collection pending` until the consignee payment is received or admin-approved policy resolves the obligation.
- POD can make final invoice generation eligible, but settlement and order closure still depend on payment, dispute, GST, and custody gates.

Customer payment states:

```text
payment_not_started
payment_link_created
booking_payment_pending
advance_paid
partially_paid
fully_paid
topay_consent_pending
topay_collection_pending
topay_collection_received
credit_approved_due_later
payment_failed
payment_mismatch_under_review
refund_initiated
refund_completed
```

Invoice states:

```text
proforma_generated
receipt_generated
final_invoice_pending_pod
final_invoice_pending_gst_review
final_tax_invoice_generated
invoice_sent
invoice_paid
debit_note_generated
credit_note_generated
```

Payment-mode flows:

```text
Full Payment:
quote accepted
-> proforma generated
-> full payment captured
-> order confirmed
-> shipment executed
-> POD verified
-> final tax invoice generated and sent
```

```text
Part Payment:
quote accepted
-> proforma generated
-> required advance captured or authorized
-> order confirmed
-> loading/payment policy checked
-> balance collected before delivery, POD release, or due date as policy defines
-> final tax invoice generated after POD/tax confirmation
```

```text
ToPay:
quote accepted
-> consignee payer details captured
-> ToPay consent requested
-> order confirmed only after policy-approved consent/payment gate clears
-> delivery/POD triggers final invoice and consignee payment request
-> provider payout remains blocked until ToPay collection or admin-approved obligation resolution
```

GST display copy:

```text
GST is calculated by the finance system based on supplier role, freight payer, customer tax profile, goods category, and current rule version.
If freight is supplied by a partner, the freight invoice and Zippy service invoice may be separate.
```

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
- ToPay consent required
- ToPay collection pending
- payment mismatch under review
- vehicle/provider assigned
- truck reached pickup
- loading completed
- in transit
- delay risk
- delivery imminent
- delivered
- POD uploaded
- final invoice pending GST review
- invoice raised
- debit note or credit note issued
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

## Related Project Notes

- [[Current Project Navigation Hub]]
- [[Frontend Architecture for Current Project]]
- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Operational Compliance Framework for Indian Logistics Startup 2025-2026]]
