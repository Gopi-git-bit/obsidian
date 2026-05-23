---
type: concept
domain: compliance
decision_value: high
status: draft
last_updated: 2026-05-21
related_hubs:
  - Compliance & Regulation Hub
  - Operations Strategy Hub
tags:
  - compliance
  - logistics
  - gst
  - e-invoicing
  - e-way-bill
  - audit
  - product-controls
---

# Compliance Compatibility Plan for Current Logistics Environment

## Purpose

Keep the improved compliance document compatible with the current Zippy Logistics product environment without disturbing the existing OMS, TMS, IMS, finance, driver, customer, transport-company, and admin flows.

Compliance should work as a validation, evidence, invoice, audit, and escalation layer around the logistics platform. It should not become the order brain.

## Governing Principle

The logistics system should remain event-driven:

- OMS owns order lifecycle truth.
- TMS owns transport execution evidence.
- IMS/WMS owns inventory, loading, unloading, and warehouse evidence where applicable.
- Finance and Invoice agents own GST, invoice, settlement, reconciliation, and accounting records.
- Supervisor/Admin owns overrides, exception review, DLQ handling, and audit governance.

Compliance may block, hold, validate, annotate, or escalate. It should not silently rewrite core business records.

## Compatibility Map by Product Role

| Product area | Compliance responsibility | User-visible surface |
|---|---|---|
| Customer App | GST/PAN validation, invoice access, payment status, shipment documents, POD delivery | Registration, Book Shipment, Payments, Track Orders |
| Driver App | Document scan, POD capture, vehicle/permit alerts, trip compliance warnings | Current Order, Active Navigation, Document Scanner |
| Transport Company App | Fleet permit status, partner-company records, service fee evidence, dual-role separation | Dashboard, Orders, Fleet, Network, Financials |
| Admin/Ops | Exception review, manual approvals, audit trails, regulatory risk monitoring | Control tower, exception queue, compliance dashboard |
| Finance Agent | GST classification, e-invoice registration, invoice PDF, GSTR-1 export, reconciliation | Finance workflows and customer invoice delivery |
| Supervisor Agent | Signal detection, DLQ triage, compliance risk scoring, escalation thresholds | Admin alerts and policy decision queues |

## Event Compatibility Spine

Compliance integrations should listen to current platform events instead of directly changing workflow state.

Recommended event triggers:

- `ORDER_CREATED`
- `ORDER_CONFIRMED`
- `VEHICLE_ASSIGNED`
- `DOCUMENT_UPLOADED`
- `LOADING_COMPLETE`
- `DISPATCH_READY`
- `PICKUP_COMPLETE`
- `POD_UPLOADED`
- `ORDER_DELIVERED`
- `SETTLEMENT_PREPROCESS`
- `PAYMENT_CAPTURED`
- `INVOICE_REGISTERED`
- `COMPLIANCE_EXCEPTION_RAISED`

Important rule:

`SETTLEMENT_PREPROCESS` is the correct trigger for GST invoice generation. Invoice registration should not close the order by itself.

## Data Integrity Rules

The compliance layer must never silently alter:

- order IDs
- tracking numbers
- GSTIN/PAN values
- invoice numbers
- e-Way Bill numbers
- IRN/acknowledgement references
- vehicle registration numbers
- driver licence numbers
- SKU/product descriptions
- dates and timestamps
- shipment value
- payment amount
- commission, platform fee, surcharge, or tax values

Corrections should use an admin-approved amendment flow with reason, actor, timestamp, old value, new value, and audit log entry.

## Compliance Gate Matrix

| Workflow stage | Compliance checks | Block type | Owner |
|---|---|---|---|
| Customer registration | GST/PAN, phone/email verification, privacy notice | Hard block | Auth/Admin |
| Shipment booking | customer eligibility, blocked payment status, document requirement, hazardous flag | Hard or conditional | OMS |
| Vehicle assignment | RC, insurance, fitness, permit, PUC, vehicle class match | Hard block for expired/missing critical docs | TMS/IMS |
| Driver assignment | licence validity, vehicle-class eligibility, active status | Hard block | TMS |
| Dispatch readiness | e-Way Bill, shipment document, vehicle details, route/state permit checks | Hard block where legally required | OMS/TMS |
| Loading complete | document scan, product/package quality evidence | Conditional hold | Driver App/Ops |
| Settlement preprocess | GST classification, invoice sequence, tax calculation, broker/principal mode | Hard block for invalid invoice basis | Finance Agent |
| Invoice registration | IRP/GSP response, QR/IRN, PDF storage | Retry/DLQ before final issue | Invoice Agent |
| Delivery complete | POD, OTP/receiver acknowledgement, damage/shortage flag | Settlement hold if incomplete | OMS/Settlement |
| Reconciliation | IRP status, local invoice status, GSTR-1 export | Finance exception | Finance/Admin |

## Current Logistics Compliance Additions

For the Indian logistics environment, keep these checks available as structured product controls:

- vehicle registration validity
- vehicle fitness certificate validity
- vehicle insurance validity
- permit validity for route and cargo use case
- PUC validity where used in the operating workflow
- driver licence validity and class match
- e-Way Bill requirement and expiry
- cross-state movement checks
- hazardous-goods classification and SDS evidence
- vehicle load limit and overloading risk
- POD completeness and dispute hold
- payment custody and settlement model review

## Compliance Risk Score

Add a simple risk status to orders, vehicles, drivers, and partner companies.

| Score | Meaning | Product action |
|---|---|---|
| Green | all required checks pass | allow normal workflow |
| Amber | document expiring soon, manual review pending, or API fallback used | allow with warning or ops review |
| Red | expired/missing critical document, GST mismatch, missing e-Way Bill, failed invoice registration, active dispute | block or hold until resolved |

## API Failure and Manual Fallback

Government, GST, payment, and verification APIs may be unavailable or rate-limited. The platform should support a controlled fallback path:

- TTL-based cache for prior verification results.
- Retry queue for transient API errors.
- DLQ for validation failures or repeated external failures.
- Manual upload and admin approval for edge cases.
- Clear statuses: `AUTO_VERIFIED`, `MANUAL_PENDING`, `FAILED`, `EXPIRED`, `OVERRIDDEN`.

Do not block all logistics movement only because a non-critical API is temporarily unavailable. Do block legally unsafe movement, missing statutory documents, expired critical documents, and invalid tax invoice issuance.

## Audit and Evidence Requirements

Every compliance decision should create an immutable audit record:

- event name
- actor or system component
- timestamp
- related order, vehicle, driver, invoice, or partner ID
- input hash or evidence reference
- decision result
- external API reference if used
- failure reason if any
- override reason and approver if any

The audit log should be append-only and suitable for finance, tax, legal, and customer dispute review.

## 90-Day Compatibility Rollout

### Days 1-15: Alignment

1. Finalize the compliance event list.
2. Map every compliance rule to Customer, Driver, Transport Company, Admin, Finance, or Supervisor surfaces.
3. Mark each rule as hard block, conditional hold, warning, or audit-only.
4. Freeze GST invoice numbering, tax classification, and settlement trigger assumptions.

### Days 16-35: Data Model

1. Add or confirm tables for invoices, compliance audit logs, vehicle compliance, driver compliance, partner compliance, and DLQ records.
2. Add RLS policies for finance-only writes and customer-scoped reads.
3. Add compliance status fields without replacing the existing OMS state machine.
4. Confirm retention and evidence storage rules.

### Days 36-60: Core Workflows

1. Implement GST and e-invoice workflow from `SETTLEMENT_PREPROCESS`.
2. Add vehicle and driver document checks before assignment and dispatch.
3. Add compliance score to orders, vehicles, drivers, and partner companies.
4. Add admin exception dashboard and manual approval flow.

### Days 61-75: Integrations

1. Test IRP/GSP sandbox registration.
2. Connect vehicle and driver verification sources where available.
3. Configure PDF invoice generation, QR/IRN injection, and secure storage.
4. Configure customer, driver, transport-company, and admin notifications.
5. Add daily reconciliation cron.

### Days 76-90: Verification

1. Test normal order completion to invoice generation.
2. Test failed IRP registration and DLQ route.
3. Test expired vehicle permit and dispatch block.
4. Test blocked customer payment status.
5. Test cross-state route check.
6. Test API downtime fallback.
7. Test audit export and reconciliation reports.

## Related Notes

- [[Compliance & Regulation Hub]]
- [[Operational Compliance Framework for Indian Logistics Startup 2025-2026]]
- [[Legal Compliance Framework]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]]
- [[API and Event Contract for Current Project]]
- [[Frontend-to-Backend Flow Map for Current Project]]
- [[Authoritative Database Schema]]
