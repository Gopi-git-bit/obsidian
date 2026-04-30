---
type: concept
domain: operations
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - AI Agents Hub
tags:
  - concept
  - operations
---

# Order Lifecycle

## Definition

The complete journey of a shipment from initial inquiry to final delivery and payment settlement.

## Stages

```
Inquiry -> Booking -> Confirmation -> Pickup -> In Transit -> Delivered -> POD -> Invoice -> Payment
                                      \-> Reverse / Return / Reattempt -> Evidence -> Settlement
```

## OMS Control Principle

The OMS should be treated as the lifecycle command center: every operational system can execute a part of the job, but the OMS owns the canonical order record, allowed state transitions, exception holds, and customer-visible order truth.

| Layer | OMS responsibility | Execution partner |
|-------|--------------------|-------------------|
| Demand capture | Create inquiry, draft, quote, booking, and order ID | Customer app, web, WhatsApp, API |
| Validation | Check serviceability, address quality, cargo rules, payment readiness, and duplicate risk | Pricing engine, maps, payment gateway |
| Allocation | Trigger load matching, capacity checks, fallback queues, and assignment approval | [[Load Matching Algorithm]], fleet/partner systems |
| Execution | Control pickup, dispatch, transit, delivery, and exception state changes | TMS, driver app, tracking layer |
| Evidence | Attach document scans, POD, GPS traces, timestamps, and consent records | Driver app, document store |
| Settlement | Trigger invoice, payment reconciliation, and provider settlement workflows | Payment gateway, [[Payment Settlement Agent]] |
| Reverse logistics | Control return request, evidence capture, reverse pickup/drop-off, refund/claim hold, and settlement closure | [[Reverse Logistics and Return Policy Framework]], 3PL partners, warehouse desks |

## Lifecycle Gates

Use gates to prevent an order from moving forward before the required business truth exists.

| Gate | Required before transition | Failure handling |
|------|----------------------------|------------------|
| Booking gate | Customer, route, cargo, schedule, vehicle need, and contact details are complete | Save as draft or send to customer support |
| Validation gate | Address serviceability, restricted cargo, duplicate order, and feasibility checks pass | Reject, request correction, or create manual review |
| Payment/consent gate | Payment mode, advance condition, ToPay consent, and outstanding dues policy are resolved | Hold order and notify customer/admin |
| Allocation gate | Vehicle/provider capacity is feasible and assignment is idempotent | Retry matching, partner fallback, or escalation |
| Pickup gate | Driver arrival, goods inspection, document capture, and loading confirmation are recorded | Hold advance release or create damage/document exception |
| Transit gate | GPS stream, ETA confidence, route adherence, and delay alerts remain observable | Trigger deviation, delay, or safety workflow |
| Delivery gate | Recipient validation, OTP/signature, unloading status, and POD quality are captured | Block completion until evidence is corrected or reviewed |
| Settlement gate | Invoice, payment ledger, provider settlement, and audit trail are consistent | Reconcile before marking financial completion |
| Return gate | Return reason, evidence, cost owner, reverse destination, and 3PL responsibility are explicit | Hold refund/settlement, create reverse order, or escalate to operations |

## Strategy Layer: CODP for Logistics OMS

Customer Order Decoupling Point logic helps the OMS decide how much work should be pre-planned versus triggered only after a specific customer order exists.

| Scenario | OMS strategy | Practical rule |
|----------|--------------|----------------|
| Standard, repeatable lane with predictable demand | Make-to-stock equivalent | Pre-build lane rates, vehicle pools, SLA promises, and dispatch cut-offs |
| High-variety shipment with common components | Assemble-to-order equivalent | Pre-plan reusable route, vehicle, partner, and document templates, then finalize per order |
| Customized cargo, special handling, risky location, or perishable goods | Make-to-order equivalent | Do not confirm until requirements, capacity, risk, and customer consent are explicit |
| Highly complex enterprise movement | Engineer-to-order equivalent | Route to operations planning before quote, assignment, or SLA commitment |

| Strategy | Logistics Reading | Tradeoff |
|----------|-------------------|----------|
| MTS | Forecast-driven standard products or repeat lanes with pre-positioned capacity | Short delivery time and high utilization, but inventory/capacity risk if forecast is wrong |
| MTO | Customer-order-driven movement with individualized requirements, lower stock cost, and variable lot size | Reduced stock risk, but longer lead time and heavier validation |
| ATO | Standard components assembled into a customized service | Good fit for reusable lane, vehicle, document, pricing, and partner templates |
| ETO | Individual design or enterprise movement planned from scratch | Highest fit quality, but slowest and most operations-heavy |

## Enhanced OMS Loop

```
Capture -> Validate -> Price -> Confirm -> Allocate -> Dispatch -> Track -> Deliver -> Evidence -> Bill -> Settle -> Learn
```

- Capture should support drafts, retries, and duplicate prevention across app, API, phone, and WhatsApp channels.
- Validate should combine customer eligibility, lane feasibility, cargo compatibility, address quality, and payment policy.
- Price should show the customer-facing estimate while preserving internal cost, commission, and provider payout logic separately.
- Confirm should lock the customer-visible promise only after payment/consent and feasibility gates pass.
- Allocate should use deterministic idempotency so retries do not create duplicate vehicle or provider assignments.
- Dispatch should respect cut-off windows, route plans, vehicle readiness, and document prerequisites.
- Track should store events from GPS, driver app updates, customer communication, and exception detectors.
- Deliver should capture OTP/signature, recipient identity, unloading completion, and POD evidence.
- Bill and settle should separate invoices, payment attempts, ledger entries, and provider settlement.
- Learn should feed future pricing, ETA, carrier scoring, customer risk, return-policy tuning, and SOP improvements.
### 1. Inquiry
- Customer requests quote
- [[Dynamic Pricing Logic]] generates estimate
- Lead created in system

### 2. Booking
- Customer confirms quote
- [[SOP - New Shipment Booking]] triggered
- Order created with unique ID
- Customer app should persist drafts and retries safely before confirmation succeeds
- Order projection should be backed by append-only event history for replay and audit

### 3. Confirmation
- Order validated
- [[Load Matching Algorithm]] finds capacity
- Routing candidates prepared before assignment is finalized
- OMS remains responsible for explicit transition requests
- Low-confidence decisions may enter deterministic fallback paths before confirmation proceeds
- ToPay consent must resolve explicitly before confirmation can safely finalize where that mode applies
- State projection and event log should remain consistent enough to support replay, debugging, and agent traceability

### 4. Pickup
- Driver reaches pickup location
- [[Proof of Delivery]] initiated
- Goods inspected and loaded
- Driver-side evidence and document capture may gate advance-release eligibility

### 5. In Transit
- Real-time tracking active
- [[ETA Prediction Logic]] updates
- Alerts for exceptions
- TMS compares actual movement against planned route and SLA
- GPS telemetry should remain queryable for route deviation, ETA recalculation, and dispute support

### 6. Delivered
- Goods reached destination
- POD captured
- [[SOP - Handle Delivery Confirmation]]

### 7. POD
- Proof of delivery signed
- Images captured
- Document attached to order
- POD quality should be backed by location, timestamp, and recipient validation where required

### 8. Invoice
- Invoice generated
- Sent to customer
- Payment terms applied
- Customer-facing consent and payment status should remain observable in the app without local state inference

### 9. Payment
- Payment received
- [[Payment Settlement Agent]] reconciles
- Order marked complete
- Gateway failures may temporarily move payment handling into controlled offline follow-up
- Ledger and settlement records should stay separate from UI-visible payment attempts

### 10. Reverse / Return / Reattempt
- Return or reverse movement may be triggered by cancellation, failed delivery, consignee rejection, damaged cargo, wrong vehicle fit, excess material, or reusable packaging recovery.
- [[Reverse Logistics and Return Policy Framework]] should create a reverse order ID instead of hiding the work inside support notes.
- Refund, claim, or provider settlement should remain on hold until evidence, cost owner, and reverse receipt are resolved.

## Key Variables

- Order priority level
- Vehicle type required
- Route distance
- Urgency level
- Customer payment terms
- Customer eligibility and outstanding dues status
- Address quality and serviceability confidence
- Cargo risk, document requirements, and special handling needs
- Capacity availability across own fleet, driver network, and partners
- Payment mode: full, part payment, ToPay, or controlled offline follow-up
- Return reason, reverse destination, return evidence, cost owner, and reverse pickup/drop-off mode
- ETA confidence, route risk, and exception severity
- POD evidence quality and dispute probability

## Control KPIs

| KPI | Why it matters |
|-----|----------------|
| Order validation time | Shows whether booking can move quickly without support intervention |
| Validation accuracy | Prevents bad addresses, restricted cargo, duplicate orders, and wrong commitments |
| Allocation time | Measures how fast confirmed demand becomes executable capacity |
| On-time dispatch rate | Shows whether pickup and vehicle readiness are controlled |
| On-time delivery rate | Measures customer promise reliability |
| Exception recovery rate | Shows whether fallback workflows actually restore the lifecycle |
| POD acceptance rate | Reduces disputes and delayed billing |
| Billing accuracy | Protects customer trust and settlement integrity |
| Failed delivery rate | Reveals consignee, address, timing, and communication issues |

## Decision Impact

- Affects [[Fleet Utilization]]
- Drives [[Load Matching Algorithm]]
- Triggers [[Communication Agent]]
- Defines when [[Fallback & Resilience Architecture]] should take over from automated execution
- Provides event inputs to [[Transport Control Tower KPI Framework]]

## Risks

- Delayed pickup
- Transit exceptions
- POD disputes
- Payment delays
- Duplicate routing or assignment attempts without idempotency controls
- Unsafe fallback execution that bypasses explicit transition controls
- Weak-connectivity drop-off during booking or payment
- Premature confirmation before serviceability, capacity, payment, or ToPay consent is resolved
- Missing document/POD evidence that blocks billing or creates disputes
- Treating UI-visible payment status as the ledger source of truth
- Manual exception handling that does not emit auditable lifecycle events

## Related Notes

- [[Order Status Tracking]]
- [[Order Priority Scoring]]
- [[SOP - New Shipment Booking]]
- [[SOP - Handle Delayed Shipment]]
- [[Unified Routing & Optimization Algorithm]]
- [[Fallback & Resilience Architecture]]
- [[Customer App Frontend Architecture]]
- [[Driver App Frontend Architecture]]
- [[Authoritative Database Schema]]
- [[Order Processing and Transportation Management Knowledge Map]]

- [[OMS Lifecycle Enhancement Source]]
