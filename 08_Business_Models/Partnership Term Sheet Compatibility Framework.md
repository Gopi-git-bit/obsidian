---
type: business-model
domain: partnerships
decision_value: high
status: draft
last_updated: 2026-05-21
related_hubs:
  - Business Models Hub
  - Compliance & Regulation Hub
  - Operations Strategy Hub
tags:
  - partnerships
  - contracts
  - sla
  - settlement
  - compliance
  - partner-governance
---

# Partnership Term Sheet Compatibility Framework

## Purpose

Convert the uploaded partnership term sheet draft into a Zippy-compatible contract and operating framework.

This note should guide business, product, finance, legal, and engineering review before any partner-facing term sheet is used.

## Compatibility Verdict

The source draft is directionally strong because it treats partnerships as operational integrations, not only commercial relationships.

It is compatible with the current Zippy knowledge base if these constraints are preserved:

- OMS remains the order lifecycle source of truth.
- Partners cannot bypass the state machine.
- All partner state-changing calls require idempotency.
- Partner economics must match the active revenue model.
- Driver, vehicle, GST, payment, insurance, and data-protection obligations must be validated before go-live.
- AI may score or recommend, but human/admin approval is required for refunds, overrides, closures, and monetary decisions.

## Business Practice Alignment

| Area | Current Zippy practice | Term sheet compatibility action |
|---|---|---|
| Driver partner economics | Driver commission default is 10% | Use 10% as default unless a signed corridor-specific rule overrides it |
| Transport company economics | Transport company default is flat service fee, currently Rs 700/order in the business-model hub | Do not replace with generic percentage revenue share unless approved as a strategic collaboration |
| Enterprise SCaaS | Supported as a future expansion layer | Keep as pilot or anchor-client contract, not default MSME workflow |
| Payment custody | Treated as regulated design decision | Use licensed payment partner/escrow flow or legal sign-off before Zippy holds/splits funds |
| Insurance | Insurance add-ons are valuable but regulated | Treat Zippy as technology/distribution layer unless IRDAI registration or partner model is approved |
| Loop logic | Loop economics improve backhaul but GST remains per-order | Apply loop discounts once per loop, but invoice and refund per order |
| Disputes | POD and settlement holds already exist in finance logic | Add SLA breach detection and evidence lock without allowing AI auto-refunds |
| Compliance | Compliance gates already govern dispatch and settlement | Add partner clauses that make compliance gates contractually binding |

## Approved Partner Types

### Anchor Tenant or Enterprise SCaaS

Use for high-volume manufacturers, FMCG, automotive, warehouse networks, or large recurring shippers.

Required terms:

- committed corridor and volume
- API or portal integration scope
- order creation, tracking, POD, invoice, and SLA workflow
- SLA credits capped by monthly fees
- data-sharing limits
- wind-down period for in-flight shipments
- audit rights limited to partnership transactions

Do not promise unlimited custom control over Zippy routing, pricing, or state machine behavior.

### Small Fleet Operator Partner

Use for independent vehicle owners, driver-cum-owners, and local small fleets.

Required terms:

- valid vehicle registration, fitness, insurance, permit, and PUC where applicable
- valid driver licence and vehicle-class eligibility
- app-based state transitions only
- POD, GPS, and shipment-document evidence requirements
- transparent commission, advance, final payout, and hold rules
- suspension path for fake POD, expired documents, repeated no-show, or safety breach

Default economics should start from current Zippy practice: 10% driver commission unless a new approved rule exists.

### Transport Company or Co-opetition Alliance

Use for asset-heavy carriers, regional transporters, specialized fleets, or partner marketplaces.

Required terms:

- partner provides physical execution and local operational capability
- Zippy controls customer interface, order visibility, audit, and settlement rules where contracted
- shared capacity scope must be explicit by corridor, vehicle type, service tier, and data field
- partner cannot access customer base outside assigned orders
- non-circumvention and data protection clauses are mandatory
- partner health score should govern scale, restriction, or exit

For normal transport-company orders, preserve the flat service fee model unless the partnership is formally upgraded to strategic revenue share.

### EV or Green Fleet Partnership

Use for EV fleets, charging networks, sustainability pilots, and enterprise green-lane demand.

Required terms:

- corridor-level EV suitability
- charging availability and fallback process
- battery/charging telemetry fields
- carbon calculation methodology documented before customer-facing claims
- incentive structure tied to actual utilization and service reliability

Avoid marketing precise carbon reductions unless the methodology is documented and audit-ready.

### Payment Gateway or Escrow Partner

Use only with a regulated and approved payment partner.

Required terms:

- partner licence or regulatory status
- settlement account structure
- webhook signing, idempotency, reconciliation, and failure handling
- refund and chargeback responsibility
- daily reconciliation
- fallback settlement path
- incident and breach notification

Do not describe Zippy as freely holding, splitting, or releasing customer funds unless legal and compliance review approves that operating model.

### Insurance or Risk Partner

Use for cargo insurance, claims workflow, risk analytics, or loss-prevention add-ons.

Required terms:

- partner must hold required insurance authorization
- Zippy role must be clearly defined as technology provider, referral partner, corporate agent, broker, or another approved model
- customer consent and product disclosure must be clear
- claim evidence bundle must include POD, GPS, incident photos, order metadata, and audit trail
- claim payout must not bypass settlement controls

## Non-Negotiable Universal Clauses

Every partnership term sheet should include:

- state machine integrity clause
- idempotency clause for all state-changing APIs
- audit and compliance clause
- data protection and confidentiality clause
- non-circumvention clause for customer and partner data
- GST, invoice, settlement, and refund responsibility clause
- SLA and evidence clause
- liability cap and indemnity clause
- dispute escalation path
- termination, wind-down, data portability, and final settlement clause

## SLA and Dispute Compatibility

The uploaded draft includes a useful SLA and dispute system. Use it as a companion workflow to [[Payment Settlement Agent]] and [[SOP - Handle POD Disputes]].

Recommended flow:

1. OMS or TMS emits an SLA breach event.
2. System creates an `order_dispute`.
3. Evidence is locked: GPS trace, POD, timestamps, telemetry, and chat logs.
4. DISPUTE_AI scores the case and recommends liability/refund range.
5. Settlement moves to hold if payout is not completed.
6. L2 Ops accepts or rejects non-monetary liability.
7. L3 Finance approves refund or credit note within policy cap.
8. Finance creates refund, GST reversal, and ledger adjustment.
9. Supervisor/Admin handles override cases.
10. Audit log records the complete decision trail.

Hard rule:

DISPUTE_AI can recommend; it must not issue refunds, close disputes, override admins, or mutate settlement.

## Contract-To-System Mapping

| Contract clause | System control |
|---|---|
| state machine integrity | OMS transition API, rejected illegal transitions, audit log |
| idempotency | mandatory request key, duplicate execution block |
| partner scope | agreement ID, corridor, vehicle type, service tier |
| data-sharing limit | RBAC, RLS, partner-scoped API responses |
| SLA | TMS/OMS event measurement and breach log |
| settlement | Finance Agent payout gate and reconciliation |
| dispute | order dispute case, evidence lock, admin queue |
| loop economics | loop group ID, per-order invoice and refund isolation |
| exit | freeze new assignments, drain in-flight orders, final reconciliation, revoke access |

## Red Flags Before Signing

Do not sign without review if a term sheet includes:

- partner ability to directly change order status
- uncapped SLA credits or indirect damages
- partner access to all customer data
- cross-use of driver/customer PII beyond the order purpose
- auto-refund or auto-settlement without finance approval
- Zippy holding customer funds without approved payment structure
- insurance sale language without approved IRDAI pathway
- carbon or ESG claims without methodology
- loop discount applied in a way that corrupts per-order GST records
- no wind-down path for live orders

## Implementation Checklist

- [ ] Select partnership type and default economic model.
- [ ] Confirm whether partner is capacity, demand, technology, payment, insurance, or strategic alliance.
- [ ] Map partner authority to allowed OMS/TMS/FIN actions.
- [ ] Validate data-sharing fields and retention rules.
- [ ] Confirm payment custody and settlement path.
- [ ] Confirm GST, invoice, refund, and credit-note handling.
- [ ] Configure agreement ID, partner ID, corridor, vehicle type, and service-tier scope.
- [ ] Test idempotency, retry, DLQ, and audit logging.
- [ ] Create partner scorecard and review cadence.
- [ ] Confirm exit, wind-down, final settlement, and API revocation process.

## Validation Notes

- Payment aggregation and escrow terms require current RBI/payment-partner review before launch.
- Insurance distribution, corporate-agent, broker, or referral language requires IRDAI-model review before launch.
- DPDP clauses should follow the live privacy readiness plan and avoid over-collecting driver/customer data.
- Jurisdiction, arbitration, liability caps, indemnity, and insurance clauses require counsel review.

## Related Notes

- [[Business Models Hub]]
- [[Partnership and Contract Strategy for a Multimodal Logistics Startup]]
- [[Partnership-Led Market Entry Framework]]
- [[Collaborative Logistics Network Framework]]
- [[Collaboration Risk Opportunity Balance Framework]]
- [[PartnershipAgreement.yaml]]
- [[Transport Company Network Model]]
- [[Strategic Profit Sharing Framework]]
- [[Payment Settlement Agent]]
- [[Operational Compliance Framework for Indian Logistics Startup 2025-2026]]
- [[Compliance Compatibility Plan for Current Logistics Environment]]
- [[SOP - Handle POD Disputes]]
