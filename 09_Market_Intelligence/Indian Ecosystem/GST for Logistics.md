---
type: concept
domain: compliance
decision_value: high
status: evergreen
related_hubs:
  - Indian Logistics Ecosystem Hub
  - Compliance & Regulation Hub
tags:
  - concept
  - india-logistics
  - compliance
  - tax
  - gst
  - gta
---

# GST for Logistics

## Overview

GST for Indian logistics should be modeled as a decision system, not a single rate card.

For Zippy, the safest architecture is a hybrid model:

- marketplace/intermediary for most partner-led freight
- principal/GTA for selected enterprise or controlled-service flows

Core rule:

```text
Do not decide GST from B2B or B2C labels alone.
Decide GST from who supplies the freight service, who pays freight, what goods are moving, what tax mode applies, and whether the case qualifies for exemption or review.
```

---

## Canonical Business Models

### Marketplace / Intermediary

In this model:

- the transport partner or GTA is the freight supplier
- the freight invoice belongs to the partner
- Zippy issues a separate platform/service invoice where applicable

Use this as the common default for fragmented partner-led freight.

### Principal / GTA

In this model:

- Zippy is the supplier of the freight service
- Zippy issues the consignment note / LR and freight invoice
- Zippy owns the freight-side GST treatment

Use this only for selected enterprise or controlled-service flows where Zippy intentionally takes supplier responsibility.

### Hybrid

In practice, Zippy should support both:

- marketplace mode for most scalable day-to-day partner freight
- principal/GTA mode for enterprise, SLA-heavy, or tightly controlled operations

The vault should treat hybrid as the canonical architecture and marketplace as the common operational default.

---

## GST Decision Inputs

The tax engine should classify each order from structured inputs:

1. `business_model`: `marketplace | principal_gta | hybrid`
2. `freight_supplier_type`: `partner_gta | non_gta_transporter | zippy_principal`
3. customer legal type
4. customer GST registration status
5. GSTIN, when available
6. freight payer / person liable to pay freight
7. goods category
8. whether a consignment note / LR is issued
9. partner or Zippy tax mode
10. effective tax rule version for the transaction date

Core rule:

```text
The app should not ask the user to pick a GST slab.
It should ask who the parties are, what service is being supplied, and what documents govern the movement.
Then the system decides the tax path.
```

---

## Invoice Ownership Matters

The most important distinction is invoice ownership.

### Freight Invoice

This invoice belongs to the actual supplier of transport service:

- partner GTA in marketplace mode
- Zippy in principal/GTA mode

This invoice determines freight-side GST treatment.

### Zippy Platform / Service Invoice

This invoice belongs to Zippy when it charges:

- platform fee
- service fee
- booking fee
- convenience fee
- subscription or support fee

This invoice must be modeled separately from the freight invoice unless Zippy is intentionally acting as principal/GTA.

Core rule:

```text
Do not merge partner freight GST and Zippy platform GST into one assumed freight bill.
```

---

## Practical Tax Modes

Represent tax treatment as controlled modes, not informal labels:

- `rcm`
- `fcm_5`
- `fcm_standard`
- `exempt`
- `review_required`

Supporting flags:

- `invoice_split_required`
- `rcm_flag`
- `exemption_reason`
- `review_required`

### Interpretation Guide

| Tax Mode | Typical Meaning |
| --- | --- |
| `rcm` | freight GST payable by recipient under applicable reverse-charge logic |
| `fcm_5` | forward-charge freight invoice at a concessional rate where supported by the applicable rule set |
| `fcm_standard` | forward-charge freight invoice at the standard effective rate for the rule/date context |
| `exempt` | nil tax due to supplier classification, recipient eligibility, goods exemption, or other rule-based exemption |
| `review_required` | risky or ambiguous case that should not auto-finalize |

Do not hard-code one national forever-rate table into this note. Use an effective-dated rule registry instead.

---

## Hybrid GST Decision Flow

```text
Step 1: Identify business model.
If marketplace, separate freight invoice and Zippy invoice.
If principal/GTA, Zippy owns freight-side invoice logic.

Step 2: Identify freight supplier type.
Is the supplier a GTA, a non-GTA transporter, or Zippy acting as principal?

Step 3: Identify recipient and freight payer.
Tax treatment depends on the person liable to pay freight, not only the booking account.

Step 4: Identify goods category and exemption path.
Some goods or recipient combinations may qualify for nil treatment.

Step 5: Apply supplier tax mode and effective-dated rule version.
Do not assume yesterday's rate or last year's option still applies.

Step 6: If classification is incomplete or risky, move to GST review queue.
```

---

## GST Review Queue Triggers

The system should not auto-dispatch or auto-finalize tax invoices for risky cases.

Send cases to review when any of these are true:

- supplier type is unclear
- business model is unclear
- customer legal type and GST status conflict
- freight payer is missing
- consignment note / LR ownership is unclear
- goods category suggests exemption but evidence is missing
- unregistered recipient appears to be an excluded or risky entity type
- freight invoice and e-way bill details do not align
- tax mode cannot be supported by the current effective-dated rule set
- customer requests invoice treatment that conflicts with captured facts

Core rule:

```text
No tax certainty, no dispatch finalization.
```

---

## E-way Bill And Dispatch Guardrails

The compliance layer should block dispatch or final invoice generation unless required fields are complete:

- supplier role confirmed
- freight payer confirmed
- invoice basis confirmed
- consignment note / LR ownership confirmed
- e-way bill requirement evaluated
- transporter ID / GSTIN captured where required
- vehicle and shipment document status complete

For order flows above the applicable threshold, e-way bill checks must be part of dispatch readiness, not an afterthought.

---

## Input Tax Credit (ITC) Guidance

ITC should be treated as rule-governed and eligibility-based.

Safe posture for this vault:

- do not state broad ITC availability without rule context
- do not assume every operating expense gives usable ITC
- do not assume freight-side ITC treatment is the same across all GTA modes

Operational implication:

```text
ITC eligibility must come from the applicable tax mode and rule version, not from a generic transport-company checklist.
```

---

## Operational Data Model

Minimum shared GST classification tables:

### `customer_tax_profile`

- `customer_id`
- `legal_type`
- `gst_status`
- `gstin`
- `freight_payer_type`
- `rcm_eligible`
- `exemption_eligible`

### `partner_tax_profile`

- `partner_id`
- `gstin`
- `is_gta`
- `issues_consignment_note`
- `tax_mode`
- `fcm_rate`
- `itc_enabled`
- `e_invoice_applicable`

### `gst_rate_master`

- `rule_id`
- `service_code`
- `service_name`
- `rate`
- `mechanism`
- `itc_allowed`
- `effective_from`
- `effective_to`
- `source_reference`
- `notification_reference`

### `order_tax_decision`

- `order_id`
- `business_model`
- `freight_supplier_id`
- `freight_supplier_type`
- `customer_id`
- `tax_mode_selected`
- `gst_rate`
- `rcm_flag`
- `exemption_reason`
- `review_required`
- `rule_id`

### `invoice_split`

- `order_id`
- `freight_invoice_id`
- `zippy_platform_invoice_id`
- `invoice_split_required`
- `partner_payout`
- `zippy_fee`
- `gst_on_zippy_fee`
- `tcs_amount`

---

## Product And Messaging Guidance

Customer-facing UI should lead with billing type and handling logic, not raw slab choice.

Preferred explanation style:

- freight billed by transport partner or by Zippy, depending on operating model
- GST may be under reverse charge, forward charge, exemption, or review depending on transaction facts
- Zippy platform fee, when charged, is handled separately from freight unless Zippy is the principal supplier

Avoid simplistic language such as:

- "B2B always 5%"
- "B2C always 12%"
- "GST extra"

Prefer:

```text
GST handling is auto-classified from supplier type, customer profile, freight payer, goods category, and current rule version.
```

---

## Risks And Common Mistakes

- treating marketplace freight as if Zippy always supplied it
- using one GST boolean for all orders
- assuming freight GST and Zippy service GST are the same thing
- finalizing invoices without supplier-role clarity
- hard-coding rates without effective dates
- letting dispatch proceed while tax basis is unresolved

---

## Related Notes

- [[E-way Bill System]]
- [[Legal Compliance Framework]]
- [[Operational Compliance Framework for Indian Logistics Startup 2025-2026]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]]

## Related Hubs

- [[Indian Logistics Ecosystem Hub]]
- [[Compliance & Regulation Hub]]
