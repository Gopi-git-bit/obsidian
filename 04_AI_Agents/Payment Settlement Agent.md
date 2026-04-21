---
type: ai_agent
domain: financial_operations
decision_value: Critical
status: active
related_hubs:
  - "[[Business Models Hub]]"
  - "[[AI Agents Hub]]"
tags:
  - ai-agent
  - payment
  - settlement
  - invoicing
actors:
  - Payment Settlement Agent
region:
  - India
created: 2025-01-15
updated: 2025-01-15
---

# Payment Settlement Agent

## Overview

The Payment Settlement Agent manages all financial transactions including invoicing, payment collection, reconciliation, and dispute resolution for the logistics platform.

## Core Responsibilities

### Invoice Generation
- Create invoices upon delivery confirmation (POD)
- Calculate charges based on [[Distance Based Pricing]] logic
- Apply surcharges, fuel adjustments, and tolls

### Payment Collection
- Track payment status against due dates
- Send automated payment reminders
- Process partial payments and payment plans
- Release driver-side advances only after required field evidence clears validation gates

### Reconciliation
- Match payments received to outstanding invoices
- Handle TDS (Tax Deducted at Source) calculations
- Reconcile with transporter settlements

### Dispute Resolution
- Investigate billing discrepancies
- Process credit notes and refunds
- Escalate complex disputes per [[SOP - Handle POD Disputes]]

## Decision Points

| Scenario | Decision Logic |
|----------|----------------|
| Payment overdue | Apply late payment penalties per contract terms |
| POD disputed | Trigger [[SOP - Handle POD Disputes]] workflow |
| Amount mismatch | Hold settlement, request POD verification |
| Customer dispute | Engage [[Communication Agent]] for resolution |
| Field evidence incomplete | Hold advance or final release until verification succeeds |

## GST & Compliance

### Tax Handling (India)
- GSTIN validation for all parties
- Proper HSN/SAC code assignment
- E-invoice generation compliance
- Refer: [[GST for Logistics]]

### TDS Management
- Calculate TDS on transporter payments (if applicable)
- Generate TDS certificates
- File quarterly TDS returns

## Integration Points

- **Input**: Delivery confirmations, POD data, rate cards, verified shipment-document evidence
- **Output**: Invoices, payment records, settlement batches
- **Dependencies**: [[Payment Risk Logic]], [[Business Models Hub]]

## Settlement Cycles

| Customer Type | Default Cycle |
|---------------|---------------|
| Premium | 15 days |
| Standard | 30 days |
| Credit | 45 days |
| Spot | Immediate |

## Related Algorithms

- [[Distance Based Pricing]]
- [[Payment Risk Logic]]
- [[Proof of Delivery]]

## Related SOPs

- [[SOP - Handle POD Disputes]]
- [[SOP - Escalate Delayed Shipment]]

## Related Scenarios

- [[Scenario - Payment Dispute]]
- [[Scenario - Delayed POD Submission]]

---

*Linked to: [[Business Models Hub]], [[AI Agents Hub]], [[Communication Agent]]*
