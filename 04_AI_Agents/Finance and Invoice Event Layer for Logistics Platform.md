---
title: Finance and Invoice Event Layer for Logistics Platform
type: agent-architecture
category: logistics-finance
status: draft
region: India
created: 2026-04-30
tags:
  - logistics
  - finance
  - invoice-events
  - payment-events
  - settlement-events
  - oms
  - tms
  - gst
  - tally
  - zippy-logistics
related:
  - Order Management Agent
  - Payment Settlement Agent
  - Payment Invoice and Accounting Agent Architecture for Logistics Platform
  - Transportation Agent
  - Resource Management Agent
  - Platform Administration Agent
  - Communication Agent
  - Demurrage Solution Translated for Current Logistics Project
source_files:
  - C:\Users\user\Downloads\chatgpt final verdict 1.txt
  - C:\Users\user\Downloads\chatgpt final verdict 2.txt
---

# Finance and Invoice Event Layer for Logistics Platform

## Purpose

This note refines the previous finance-event and invoice-event drafts after reviewing the actual application and agent PRD.

The earlier ChatGPT output had useful event details, but it missed one important architecture truth:

```text
Finance is not the order brain.
Finance is the money-control layer attached to the order brain.
```

For this logistics platform, the correct design is:

```text
OMS owns lifecycle truth.
TMS proves transport execution.
IMS/WMS proves inventory, warehouse, loading, unloading, and storage activity.
DWIS proves waiting-time and demurrage events.
Payment Agent moves money.
Invoice Agent creates compliant documents.
Settlement Agent controls provider payout readiness.
Accounting Agent records ledger truth.
Tally Agent syncs finalized accounting records.
Admin Agent governs risk, override, audit, and retention.
Communication Agent sends invoices, receipts, alerts, and payment messages.
```

Core rule:

```text
Every operational event should produce the right financial event.
Every financial event should produce a controlled accounting record.
No financial agent should casually change OMS state.
```

---

# 1. What ChatGPT Missed Without The Full PRD

The previous finance drafts were useful, but they treated invoice and settlement as if they could close the whole order by themselves.

That is risky.

## Required Corrections

| Previous Assumption | Correct PRD-Aligned Design |
| --- | --- |
| Finance events can directly close order | OMS owns order state and closure |
| TMS can trigger payout because POD exists | TMS provides evidence; Settlement Agent evaluates payout; OMS applies hold/release gates |
| Invoice sent updates GST and accounting immediately | Final tax invoice/accounting posting should be controlled, not every communication event |
| Settlement completed is one event | Split into disbursement success, reconciliation, and settlement closed |
| Customer and provider finance flows are similar | Customer payment and provider payout are separate financial lifecycles |
| Transport company is only provider | Transport company can be customer-role or provider-role depending on active role |
| Logs can be purged after closure | Logs purge only after archive and retention policy check |

## Better Mental Model

```text
Order lifecycle = OMS state machine
Money lifecycle = finance event spine
Evidence lifecycle = TMS + IMS/WMS + DWIS
Governance lifecycle = Admin + audit + retention
Communication lifecycle = Communication Agent
```

Tiny distinction, giant system spine.

---

# 2. Agent Boundary Overview Before Finance Execution

## 2.1 OMS Agent

OMS is the source of truth for order state.

It owns:

- order creation
- quote acceptance
- confirmation
- payment gate
- allocation gate
- document gate
- POD gate
- settlement gate
- order closure
- order holds
- lifecycle audit events

OMS states from the current PRD:

```text
CREATED
-> CONFIRMED
-> PICKED_UP
-> IN_TRANSIT
-> OUT_FOR_DELIVERY
-> DELIVERED
-> COMPLETED
```

Also supported:

```text
CANCELLED
EXCEPTION
VALIDATION_HOLD
PAYMENT_HOLD
ALLOCATION_HOLD
DOCUMENT_HOLD
SETTLEMENT_HOLD
```

## OMS Rule

```text
Finance agents may request a hold or release.
Only OMS/admin-controlled flow should apply lifecycle state changes.
```

---

## 2.2 TMS Agent

TMS owns live transport execution evidence.

It provides:

- route plan
- ETA
- GPS trail
- pickup arrival
- loading completion
- transit progress
- delivery arrival
- POD trigger
- SLA breach signals
- route deviation signals

TMS must not own:

- order state mutation
- pricing mutation
- settlement approval
- invoice approval
- carrier reassignment without OMS/supervisor flow

## TMS Rule

```text
TMS proves what happened.
OMS decides what that means for lifecycle state.
Finance decides what that means for money.
```

---

## 2.3 IMS/WMS Agent

IMS/WMS matters when the order includes:

- warehouse storage
- cross-dock
- inventory handling
- loading/unloading
- consolidation
- partial dispatch
- stock damage
- returns

It sends financial inputs such as:

- storage charge
- handling charge
- loading charge
- unloading charge
- warehouse demurrage
- damage/shortage report
- partial dispatch evidence

---

## 2.4 DWIS Agent

DWIS is the Dynamic Wait Intelligence System.

It sends:

- pickup wait
- delivery wait
- free time
- billable wait
- responsible party
- evidence packet
- demurrage amount
- carrier/driver waiting share

DWIS should not simply punish customers.

It should prove:

```text
where time was lost
who caused it
how much it cost
whether it is billable
how future dispatch should be buffered or priced
```

---

## 2.5 Payment Settlement Agent

Payment Settlement Agent handles:

- payment collection
- partial payment tracking
- ToPay collection status
- overdue reminders
- invoice-payment matching
- provider settlement calculation
- settlement holds
- reconciliation
- refunds
- credit notes
- TDS/GST support where applicable

It can request:

```text
PAYMENT_HOLD
SETTLEMENT_HOLD
manual_review_required
settlement_ready_for_disbursement
```

It should not directly force:

```text
order_completed
order_closed
logs_purged
```

---

## 2.6 Invoice Agent

Invoice Agent creates and manages:

- proforma invoice
- payment receipt
- final tax invoice
- debit note
- credit note
- settlement slip
- invoice PDF
- e-invoice fields if applicable
- GST split fields

Important:

```text
Proforma invoice can happen before payment.
Final tax invoice should happen after delivery/POD or taxable supply confirmation.
```

---

## 2.7 Accounting Agent and Tally Agent

Accounting Agent posts only clean financial records.

Tally should receive finalized accounting entries, not every operational event.

Tally push should be used for:

- receipts
- final tax invoices
- credit notes
- debit notes
- payout vouchers
- reconciliation entries

Not for:

- route updates
- GPS pings
- quote drafts
- invoice sent notifications
- every settlement status tick

---

## 2.8 Admin Agent

Admin Agent owns governance.

It handles:

- manual override
- settlement dual authorization
- high-value payout review
- compliance hold
- data retention
- archive approval
- dispute closure
- audit log integrity

---

## 2.9 Communication Agent

Communication Agent sends:

- invoice ready message
- payment link
- receipt
- provider payout update
- ToPay reminders
- overdue notices
- dispute alerts
- POD and invoice copies

It should not calculate finance.

It should only deliver approved finance messages.

---

# 3. Correct Finance + Invoice Lifecycle

## Full Lifecycle

```text
order_created
-> quote_generated
-> quote_accepted
-> proforma_invoice_generated
-> payment_link_created
-> payment_gate_satisfied
-> carrier_assigned
-> shipment_picked_up
-> shipment_in_transit
-> delivery_completed
-> pod_verified
-> demurrage_finalized_if_any
-> final_tax_invoice_generated
-> invoice_sent
-> invoice_paid_or_payment_obligation_resolved
-> settlement_preprocessing_started
-> settlement_ready_for_disbursement
-> settlement_disbursement_started
-> settlement_disbursement_success
-> settlement_reconciled
-> settlement_closed
-> order_closed
-> data_archived
-> logs_purged_after_retention
```

## Critical Correction

```text
settlement_preprocessing can start after POD verification.
settlement disbursement should wait for payment, dispute, risk, and admin gates.
```

This avoids a bad payout before ToPay collection, damage claims, or demurrage disputes are resolved.

---

# 4. Payment Mode Rules From The App PRD

## Supported Payment Modes

| Payment Mode | Meaning | Finance Rule |
| --- | --- | --- |
| Full Payment | Customer pays 100 percent | Order can proceed once payment is captured and OMS gate clears |
| Part Payment | Customer pays minimum 50 percent | Balance remains receivable; settlement can be held until final payment rule clears |
| ToPay | Consignee pays at delivery | Invoice/payment collection must be tied to consignee; provider payout waits unless admin-approved |
| Credit | Approved customer pays later | Must require credit policy, exposure limit, due date, and admin/fintech approval |
| Escrow/Hold | Customer pays platform, provider paid after POD | Best trust model for early startup |

## Important PRD Rule

The customer app PRD says:

```text
Orders are not confirmed until payment is successfully processed.
```

So the safe design is:

```text
quote_accepted
-> proforma_invoice_generated
-> payment_intent_created
-> required_payment_captured
-> OMS confirms order
```

## Advance Payment Timing Nuance

The PRD also says advance payment may be processed after loading is complete.

That means the platform needs two gates:

| Gate | Use |
| --- | --- |
| Booking payment gate | Confirms customer intent, token, authorization, escrow, or minimum precondition |
| Loading payment gate | Captures advance/balance after loading evidence if business policy requires |

Recommended implementation:

```text
Before assignment: collect booking advance or payment authorization.
After loading: capture required advance if the selected product allows post-loading capture.
Before settlement: confirm invoice/payment obligation is resolved.
```

This keeps operations flexible without letting fake bookings consume vehicles.

---

# 5. Event Groups

## 5.1 Customer Payment Events

| Event | Meaning |
| --- | --- |
| payment_intent_created | payment process started |
| payment_link_created | payment link generated |
| advance_payment_received | customer paid required advance |
| partial_payment_received | installment received |
| full_payment_received | full amount captured |
| topay_collection_pending | consignee payment not yet received |
| topay_collection_received | consignee paid |
| payment_failed | gateway/payment failed |
| payment_mismatch_detected | paid amount and invoice/order amount disagree |
| refund_initiated | refund started |
| refund_completed | refund completed |

Razorpay Payment Links support partial payment behavior where multiple payments can remain tied to the same order/payment link until the due amount becomes zero.

---

## 5.2 Invoice Events

| Event | Meaning |
| --- | --- |
| proforma_invoice_generated | quote-stage invoice, not final tax record |
| payment_receipt_generated | receipt for advance/partial/full payment |
| final_tax_invoice_generated | final GST invoice after POD/taxable supply confirmation |
| invoice_sent | invoice delivered through app/email/approved channels |
| invoice_paid | invoice payment obligation cleared |
| debit_note_generated | demurrage/extra charge adjustment |
| credit_note_generated | refund/adjustment after invoice |
| invoice_synced_to_tally | invoice posted to accounting system |

## Invoice Timing Rule

```text
Do not create final tax invoice too early.
Use proforma before execution.
Use final invoice after POD or taxable supply confirmation.
```

For GST e-invoicing, applicable B2B/export invoices must be authenticated through the IRP to get IRN and QR code.

---

## 5.3 Settlement Events

| Event | Meaning |
| --- | --- |
| settlement_preprocessing_started | payout calculation and validation begins |
| settlement_on_hold | settlement blocked due to risk/dispute/payment issue |
| settlement_ready_for_disbursement | payout approved but not yet transferred |
| settlement_disbursement_started | payout transfer initiated |
| settlement_disbursement_success | payout transfer confirmed successful |
| settlement_disbursement_failed | payout failed |
| settlement_reconciled | payout matched with gateway/bank/Tally |
| settlement_closed | settlement locked and audit-ready |

## Settlement Timing Rule

```text
POD verified can start preprocessing.
Invoice paid or payment obligation resolved can unlock disbursement.
Reconciliation should happen before settlement is closed.
```

Razorpay Route is relevant because it supports linked accounts, splitting payments, settlement management, reversals, refunds, and API-driven reconciliation for one-to-many payout models.

---

# 6. Provider Payout Logic

## Provider Types

| Provider Type | Platform Earning Model | Basic Rule |
| --- | --- | --- |
| Driver | commission percentage | Zippy deducts 10 percent from total fare |
| Transport Company | flat service fee | Zippy deducts INR 700 service fee |

## Improved Payout Formula

```text
Provider Final Payout =
Total Fare
+ Provider Demurrage Share
- Zippy Commission or TC Service Fee
- Penalties
- Refund Adjustments
- Claims Adjustments
- TDS if applicable
```

## Zippy Revenue Formula

```text
Zippy Revenue =
Driver Commission
+ TC Service Fee
+ Premium SLA Fee
+ Route Optimization Fee
+ Demurrage Platform Share
- Discounts
- Refunds
```

## Customer Commission Rule

The customer app PRD says customers do not pay commission to Zippy.

So commission should be shown as:

```text
deducted from provider payout
```

not:

```text
extra customer commission line
```

This protects customer trust and keeps pricing explanation clean.

---

# 7. Transport Company Dual-Role Finance Rule

Transport companies can act as:

- customer role: placing orders when they need vehicles
- provider role: accepting orders when they have excess capacity

Every finance event should include role context.

## Required Payload Fields

```json
{
  "actor_id": "UUID",
  "actor_type": "customer | driver | transport_company | admin | consignee",
  "actor_role_context": "customer_role | provider_role | admin_role | payer_role",
  "order_side": "placed_order | received_order",
  "provider_type": "driver | transport_company | partner_carrier"
}
```

## Why This Matters

The same transport company may appear in two different ledgers:

| Role | Ledger Treatment |
| --- | --- |
| TC as customer | Customer receivable / payment collection |
| TC as provider | Provider settlement payable |

Do not mix the two.

That little mistake can turn accounting into soup with wheels.

---

# 8. Clean Event Contracts

## 8.1 invoice_sent

Lead agent: Communication Agent

Supporting agents: Invoice Agent, Accounting Agent

```json
{
  "event": "invoice_sent",
  "version": "1.0",
  "trace_id": "UUID",
  "order_id": "UUID",
  "invoice_id": "UUID",
  "customer_id": "UUID",
  "provider_id": "UUID",
  "source": "communication_agent",
  "payload": {
    "invoice_url": "https://cdn.zippy.ai/invoices/INV-000123.pdf",
    "sent_to_email": true,
    "sent_to_app": true,
    "sent_to_tc": true,
    "sent_to_consignee": false,
    "email_delivery_status": "delivered",
    "push_notification_status": "sent",
    "channels": ["email", "app"],
    "generated_at": "iso_timestamp",
    "sent_at": "iso_timestamp"
  },
  "metadata": {
    "delivery_method": "multi_channel",
    "retry_count": 0,
    "notification_template_version": "2026_v1",
    "idempotency_key": "invoice_sent:INV-000123"
  },
  "timestamp": "iso_timestamp"
}
```

## Important Correction

```text
invoice_sent proves document delivery.
It should not by itself mean payment received, GST filed, or settlement ready.
```

---

## 8.2 invoice_paid

Lead agent: Payment Settlement Agent

Supporting agents: Invoice Agent, Accounting Agent, Admin Agent

```json
{
  "event": "invoice_paid",
  "version": "1.0",
  "trace_id": "UUID",
  "order_id": "UUID",
  "invoice_id": "UUID",
  "customer_id": "UUID",
  "provider_id": "UUID",
  "source": "payment_gateway",
  "payload": {
    "payment_intent_id": "string",
    "transaction_id": "string",
    "amount_paid": 0,
    "invoice_amount": 0,
    "currency": "INR",
    "payment_method": "upi",
    "paid_by": "customer",
    "paid_at": "iso_timestamp",
    "is_full_payment": true,
    "is_overdue_payment": false,
    "gateway_response_ref": "stored_securely"
  },
  "metadata": {
    "invoice_status_before_payment": "sent",
    "verification_status": "auto",
    "amount_match_status": "matched",
    "gst_compliance_check": true,
    "idempotency_key": "invoice_paid:INV-000123:TXN-001"
  },
  "timestamp": "iso_timestamp"
}
```

## Unlock Rule

```text
invoice_paid can unlock settlement_ready_for_disbursement only if:
POD verified
+ no active dispute
+ no payment mismatch
+ no demurrage dispute
+ no claim hold
+ no admin hold
```

---

## 8.3 settlement_preprocessing_started

Lead agent: Payment Settlement Agent

Supporting agents: OMS, TMS, DWIS, Accounting Agent

```json
{
  "event": "settlement_preprocessing_started",
  "version": "1.0",
  "trace_id": "UUID",
  "order_id": "UUID",
  "settlement_id": "UUID",
  "provider_id": "UUID",
  "provider_type": "driver",
  "customer_id": "UUID",
  "amounts": {
    "total_fare": 0,
    "tax_amount": 0,
    "net_fare_after_tax": 0,
    "zippy_commission": 0,
    "tc_service_fee": 0,
    "provider_demurrage_share": 0,
    "claims_adjustment": 0,
    "provider_payout_before_adjustment": 0
  },
  "payload": {
    "settlement_stage": "preprocessing",
    "payment_type": "full | part | to_pay | credit",
    "is_to_pay_pending": false,
    "delivery_status_confirmed": true,
    "pod_status": "verified",
    "demurrage_status": "none | finalized | disputed"
  },
  "metadata": {
    "payout_model": "provider_type_based",
    "commission_policy_version": "2026_v1",
    "settlement_risk_check": "pending",
    "refund_required": false,
    "idempotency_key": "settlement_preprocess:ORDER-001"
  },
  "timestamp": "iso_timestamp"
}
```

## Key Rule

```text
This event calculates and validates.
It does not transfer money.
```

---

## 8.4 settlement_disbursement_success

Lead agent: Payment Settlement Agent

Supporting agents: Accounting Agent, Communication Agent, Admin Agent

```json
{
  "event": "settlement_disbursement_success",
  "version": "1.0",
  "trace_id": "UUID",
  "settlement_id": "UUID",
  "order_id": "UUID",
  "provider_id": "UUID",
  "provider_type": "driver",
  "source": "payout_gateway",
  "payload": {
    "payout_amount": 0,
    "payout_reference": "string",
    "payout_time": "iso_timestamp",
    "bank_rrn": "string",
    "gateway_response_ref": "stored_securely",
    "provider_bank_details": {
      "account_number": "masked",
      "ifsc": "masked",
      "name_match_status": "matched"
    }
  },
  "metadata": {
    "settlement_stage": "disbursement_success",
    "gateway": "razorpayx | bank",
    "transaction_status": "success",
    "audit_complete": false,
    "reconciliation_required": true,
    "idempotency_key": "payout_success:SETTLEMENT-001:RRN-001"
  },
  "timestamp": "iso_timestamp"
}
```

## Important Correction

```text
settlement_disbursement_success means money reached provider.
It does not automatically mean settlement_closed.
```

Settlement should close only after reconciliation and audit checks.

---

# 9. Database Tables

## invoices

| Field |
| --- |
| invoice_id |
| order_id |
| shipment_id |
| customer_id |
| payer_type |
| invoice_type |
| invoice_number |
| taxable_value |
| cgst |
| sgst |
| igst |
| total_amount |
| amount_paid |
| amount_due |
| irn |
| qr_code_url |
| invoice_url |
| invoice_status |
| sent_at |
| paid_at |
| synced_to_tally |
| tally_voucher_id |

## payments

| Field |
| --- |
| payment_id |
| order_id |
| invoice_id |
| customer_id |
| paid_by |
| payer_role_context |
| payment_gateway |
| gateway_payment_id |
| amount |
| payment_method |
| payment_status |
| payment_type |
| received_at |
| reconciled_at |

## settlements

| Field |
| --- |
| settlement_id |
| order_id |
| provider_id |
| provider_type |
| provider_role_context |
| total_fare |
| commission_amount |
| tc_service_fee |
| demurrage_share |
| claims_adjustment |
| penalties |
| provider_payout |
| payout_method |
| payout_reference |
| settlement_status |
| risk_status |
| approved_at |
| payout_started_at |
| payout_completed_at |
| reconciled_at |
| closed_at |

## ledger_entries

| Field |
| --- |
| entry_id |
| order_id |
| source_event |
| source_id |
| debit_ledger |
| credit_ledger |
| amount |
| gst_amount |
| posting_status |
| tally_voucher_id |
| created_at |

## financial_holds

| Field |
| --- |
| hold_id |
| order_id |
| hold_type |
| hold_reason |
| requested_by_agent |
| applied_by |
| status |
| evidence_ref |
| created_at |
| released_at |

## documents

| Field |
| --- |
| document_id |
| order_id |
| document_type |
| file_url |
| delivery_status |
| archived |
| retention_until |
| created_at |

---

# 10. Accounting Entries

## Advance Payment Received

```text
Dr Bank / Payment Gateway Receivable
    Cr Customer Advance Liability
```

## Final Tax Invoice Generated

```text
Dr Customer Receivable / Customer Advance
    Cr Platform Commission Income / Freight Revenue
    Cr Output GST
```

## Provider Settlement Liability Created

```text
Dr Carrier Cost / Pass-through
    Cr Provider Settlement Liability
```

## Provider Paid

```text
Dr Provider Settlement Liability
    Cr Bank / RazorpayX
```

## Refund Before Final Invoice

```text
Dr Customer Advance Liability
    Cr Bank / Payment Gateway
```

## Refund After Final Invoice

```text
Dr Sales Return / Credit Note
Dr Output GST Reversal if applicable
    Cr Customer Receivable / Bank
```

## Demurrage Charged

```text
Dr Customer Receivable
    Cr Demurrage Recovery / Income
    Cr Output GST if applicable
```

## Demurrage Share Payable To Carrier

```text
Dr Demurrage Pass-through Expense
    Cr Provider Settlement Liability
```

---

# 11. Tally Integration Rule

Tally should receive finalized accounting records, not noisy operational events.

TallyPrime supports XML over HTTP integration and can act as an HTTP server when configured on a port such as 9000 with a company loaded.

## Push To Tally Only When

| Event | Push To Tally? | Voucher / Record |
| --- | --- | --- |
| quote_generated | No | none |
| proforma_invoice_generated | Optional | proforma/non-posting record |
| payment_link_created | No | none |
| payment_received | Yes | receipt voucher |
| final_tax_invoice_generated | Yes | sales invoice |
| debit_note_generated | Yes | debit note |
| credit_note_generated | Yes | credit note |
| settlement_disbursement_success | Yes | payment voucher |
| settlement_reconciled | Yes | reconciliation marker |
| data_archived | No | document archive only |

## Approval Rule

```text
Do not auto-post high-value, disputed, mismatched, or manually overridden entries to Tally without approval.
```

---

# 12. Risk And Hold Rules

## Settlement Must Pause If

```text
POD mismatch
POD not verified
invoice unpaid
ToPay not collected
payment amount mismatch
duplicate payment detected
demurrage dispute active
damage claim active
GPS route mismatch
new provider bank account
provider name/bank mismatch
large payout threshold crossed
admin compliance hold active
customer outstanding policy violated
```

## Hold Ownership

| Hold Type | Requested By | Applied By |
| --- | --- | --- |
| PAYMENT_HOLD | Payment Settlement Agent | OMS/Admin |
| DOCUMENT_HOLD | TMS/IMS/Invoice Agent | OMS/Admin |
| SETTLEMENT_HOLD | Payment Settlement Agent | OMS/Admin |
| COMPLIANCE_HOLD | Admin Agent | Admin Agent |
| DISPUTE_HOLD | Customer Service/Payment Agent | OMS/Admin |

## Release Rule

```text
A hold should be released only when the original blocking reason has evidence of resolution.
```

---

# 13. Agent Responsibility Map

| Event | Lead Agent | Supporting Agents |
| --- | --- | --- |
| proforma_invoice_generated | Invoice Agent | OMS |
| payment_link_created | Payment Agent | OMS, Communication |
| payment_received | Payment Agent | Accounting Agent |
| pod_verified | OMS | TMS, Admin |
| demurrage_finalized | DWIS Agent | TMS, Invoice, Admin |
| final_tax_invoice_generated | Invoice Agent | OMS, TMS, Accounting |
| invoice_sent | Communication Agent | Invoice Agent |
| invoice_paid | Payment Settlement Agent | Invoice, Accounting |
| settlement_preprocessing_started | Payment Settlement Agent | OMS, TMS, DWIS |
| settlement_ready_for_disbursement | Payment Settlement Agent | Admin, Accounting |
| settlement_disbursement_started | Payment Settlement Agent | Admin |
| settlement_disbursement_success | Payment Settlement Agent | Accounting, Communication |
| settlement_reconciled | Accounting Agent | Payment Settlement, Tally |
| settlement_closed | Accounting Agent | Admin, OMS |
| order_closed | OMS/Admin Agent | All relevant agents |
| data_archived | Admin/Data Agent | Accounting, Documents |
| logs_purged | Admin/System Agent | Audit Agent |

---

# 14. n8n Workflow Names

```text
WF_PAY_01_payment_link_created
WF_PAY_02_payment_received
WF_PAY_03_refund_completed
WF_INV_01_proforma_invoice_generated
WF_INV_02_final_tax_invoice_generated
WF_INV_03_debit_or_credit_note_generated
WF_DOC_38_invoice_sent
WF_FIN_39_invoice_paid
WF_FIN_31_settlement_preprocessing_started
WF_FIN_32_settlement_ready_for_disbursement
WF_FIN_33_settlement_disbursement_started
WF_FIN_34_settlement_disbursement_success
WF_FIN_35_settlement_reconciled
WF_FIN_42_settlement_closed
WF_OMS_41_order_closed
WF_ARCHIVE_44_data_archived
WF_SYS_45_logs_purged_after_retention
```

## Workflow Discipline

```text
Each workflow must be idempotent.
Each workflow must write an event log.
Each workflow must support retry and dead-letter handling.
Each workflow must avoid duplicate payout, duplicate invoice, or duplicate notification.
```

---

# 15. Frontend Impact By App

## Customer App

Show:

- quote/proforma
- payment link
- payment status
- invoice PDF
- receipt
- ToPay status if consignee is payer
- outstanding payment block if policy applies
- POD and invoice after delivery

Do not show:

- internal settlement risk score
- provider payout breakdown unless required by policy
- admin audit internals

---

## Driver App

Show:

- expected earning
- commission deducted
- pending payout
- settlement processing
- payout initiated
- payout successful
- demurrage/waiting compensation if collected
- settlement slip

Do not show:

- customer invoice internals beyond what affects payout
- GST/Tally posting internals

---

## Transport Company App

Because TC can be both customer and provider, separate tabs are required:

| View | Shows |
| --- | --- |
| Placed Orders | invoices payable, payments made, ToPay status |
| Received Orders | payout, INR 700 service fee deduction, settlement slip |
| Fleet/Provider Finance | earned revenue, pending settlements |
| Customer Finance | outstanding payables, invoices received |

---

## Admin Panel

Show:

- payment mismatch queue
- POD dispute queue
- ToPay pending queue
- settlement holds
- payout approval queue
- duplicate payment alerts
- Tally sync failures
- archived records
- retention status

---

# 16. Build Order

## Phase 1: Payment And Invoice Spine

Build:

```text
order_created
quote_generated
proforma_invoice_generated
payment_link_created
payment_received
payment_failed
```

Core tables:

- orders
- payments
- invoices
- event_log

---

## Phase 2: Delivery To Final Invoice

Build:

```text
pod_verified
final_tax_invoice_generated
invoice_sent
invoice_paid
```

Add:

- POD evidence link
- invoice PDF
- receipt
- GST split
- invoice status

---

## Phase 3: Provider Settlement

Build:

```text
settlement_preprocessing_started
settlement_on_hold
settlement_ready_for_disbursement
settlement_disbursement_started
settlement_disbursement_success
```

Add:

- settlement table
- provider payout calculation
- driver commission rule
- TC INR 700 service fee rule
- payout reference
- provider notifications

---

## Phase 4: Accounting And Tally

Build:

```text
ledger_entry_created
invoice_synced_to_tally
payment_synced_to_tally
settlement_synced_to_tally
settlement_reconciled
```

Add:

- ledger_entries
- reconciliation
- tally_voucher_id
- mismatch handling

---

## Phase 5: Closure And Governance

Build:

```text
settlement_closed
order_closed
data_archived
logs_purged_after_retention
```

Add:

- retention policy
- admin override log
- immutable close state
- audit export

---

# 17. Final Recommended Design

## Name

```text
Finance + Invoice Event Layer
```

## One-Line Strategy

```text
Order -> Payment -> Invoice -> Settlement -> Accounting -> Closure -> Archive
```

## Final Architecture

```text
OMS = lifecycle owner
TMS = transport proof
IMS/WMS = warehouse and inventory proof
DWIS = waiting-time proof
Payment Settlement Agent = money movement and settlement control
Invoice Agent = document and GST record
Accounting Agent = ledger truth
Tally Agent = local accounting sync
Admin Agent = governance and retention
Communication Agent = message delivery
```

## Final Takeaway

This layer is not just finance backend.

It is the trust engine of the logistics platform.

Customers trust it because invoices and receipts are clear.
Drivers trust it because payouts are predictable.
Transport companies trust it because customer-role and provider-role ledgers do not get mixed.
Admins trust it because every rupee has an event trail.
Accounting trusts it because every posting comes from verified events.

That is how the platform avoids becoming a WhatsApp broker with a payment link.

It becomes a serious logistics operating system with financial memory.

---

# Source Links

- [Razorpay Payment Links - Partial Payments](https://razorpay.com/docs/payments/payment-links/partial-payments/)
- [Razorpay Route Docs](https://razorpay.com/docs/payments/route/)
- [Razorpay Route - Transfer Funds To Linked Accounts](https://razorpay.com/docs/payments/route/transfer-funds-to-linked-accounts/)
- [GST IRP - E-Invoice Mandate](https://einvoice6.gst.gov.in/content/einvoice-mandate/)
- [TallyHelp - Integration With TallyPrime](https://help.tallysolutions.com/integration-with-tallyprime/)
- [TallyHelp - XML Interface](https://help.tallysolutions.com/xml-interface/)
- [[Order Management Agent]]
- [[Payment Settlement Agent]]
- [[Transportation Agent]]
- [[Resource Management Agent]]
- [[Platform Administration Agent]]
- [[Communication Agent]]
- [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]]
- [[Demurrage Solution Translated for Current Logistics Project]]
