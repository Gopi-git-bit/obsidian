---
type: concept
domain: compliance
decision_value: high
status: verified
related_hubs:
  - Compliance & Regulation Hub
  - Operations Strategy Hub
tags:
  - concept
  - compliance
  - legal
  - contracts
  - hazardous-goods
---

# Legal Compliance Framework

## Purpose

Capture the general legal and compliance guardrails that a logistics operator should embed into company setup, contracting, shipment documentation, and hazardous-goods handling.

## Important Boundary

- This note is operational guidance, not formal legal advice.
- Law, permits, tax, and contract language should be validated with current counsel and up-to-date statutory requirements before production use.

## Core Areas

| Area | Why It Matters |
|------|----------------|
| Company setup | Establishes legal entity, tax identity, and licensing baseline |
| Customer contracts | Defines SLA, liability, escalation, and payment obligations |
| Shipment documents | Supports movement, tax, and dispute evidence |
| Vehicle and carrier compliance | Protects operational legality and insurability |
| Hazardous-goods controls | Prevents unsafe or unlawful bookings |

## Contracting Principles

- Keep pricing, surcharge triggers, liability caps, and escalation paths explicit.
- Clarify loading, unloading, insurance, shortage, and delivery-window responsibilities.
- Define what happens if demand cannot be met, including fallback and compensation logic.
- Prefer simple, transparent terms for MSMEs over dense legal complexity.
- Keep customer-facing T&C and privacy wording aligned with real booking, payment, cancellation, POD, and data-sharing behavior.

## Documentation Principles

- Preserve commercial invoice, packing details, carriage proof, POD, and payment evidence.
- Keep tax and shipment records structured enough for audit and dispute handling.
- Use digital signatures and digital KYC where legally appropriate and operationally useful.

## Hazardous-Goods Principles

- Screen shipments using structured material identifiers, such as HSN and UN references where relevant.
- Flag or reject restricted cargo unless documentation and authorization are sufficient.
- Require safety documents and permits before dispatch for regulated cargo classes.
- Apply special packaging, handling, insurance, and approval workflows where risk is elevated.

## Operational Implications for Zippy

| Function | Compliance Expectation |
|---------|------------------------|
| OMS | Collect enough cargo and contract metadata to screen risky or restricted orders |
| IMS | Avoid assigning non-compliant vehicle or driver combinations |
| TMS | Preserve movement and POD evidence for audit and dispute use |
| FIN | Maintain invoice, tax, and settlement evidence cleanly |
| Supervisor | Review escalated compliance and policy exceptions |

## Related Notes

- [[Compliance & Regulation Hub]]
- [[GST for Logistics]]
- [[E-way Bill System]]
- [[Proof of Delivery]]
- [[Customer Terms & Privacy Policy Framework]]
- [[Authoritative Database Schema]]

## Related Hubs

- [[Compliance & Regulation Hub]]
- [[Operations Strategy Hub]]
