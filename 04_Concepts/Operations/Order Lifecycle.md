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
Inquiry → Booking → Confirmation → Pickup → In Transit → Delivered → POD → Invoice → Payment
```

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

## Key Variables

- Order priority level
- Vehicle type required
- Route distance
- Urgency level
- Customer payment terms

## Decision Impact

- Affects [[Fleet Utilization]]
- Drives [[Load Matching Algorithm]]
- Triggers [[Communication Agent]]

## Risks

- Delayed pickup
- Transit exceptions
- POD disputes
- Payment delays
- Duplicate routing or assignment attempts without idempotency controls
- Unsafe fallback execution that bypasses explicit transition controls
- Weak-connectivity drop-off during booking or payment

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
