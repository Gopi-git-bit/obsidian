# Zippy Logistics - Autonomous Agentic AI Application

**Aligned with AI Agent PRD + Customer/Driver Business Logic**
**Version:** 1.1
**Effective:** December 8, 2025

> [!WARNING] Governance
> Agents **NEVER** mutate DB state directly.
> Agents **NEVER** move money without approval.
> All lifecycle actions flow through [[07_State_Machine]] via the `transition()` method.
> Agent outputs must include an idempotency key, actor identity, trace context, and decision reason.
> Agent integrations must use the backend agent APIs in [[API and Event Contract for Current Project]]; direct DB writes are forbidden.

## Purpose

This document is the main operating specification for the Zippy Logistics autonomous agent system. It merges the AI-agent PRD, OMS business logic, customer segmentation rules, driver/resource segmentation, vehicle selection rules, and express/standard delivery workflows into one AI-readable execution model.

The system is designed around a 7-agent architecture:

- Customer Service Agent
- Order Management Agent
- Resource Management Agent
- Transportation Agent
- Payment & Settlement Agent
- Platform Administration Agent
- Communication Agent

The Order Management Agent is the orchestration brain. It validates demand, prioritizes customers, delegates vehicle selection, coordinates payment and pricing checks, emits canonical lifecycle events, and escalates failures without bypassing governance.

## Current Backend/API Alignment

This note preserves the older operational agent roles, but implementation must align to the current backend structure:

```text
FastAPI services and policy modules own workflow truth
agents recommend, score, summarize, classify, or request actions
supervisor policy gate approves, holds, rejects, or escalates high-risk outputs
frontend apps render only backend-persisted status
```

Agent API boundary:

```text
GET    /agents/{agent_code}/context/{entity_type}/{entity_id}
POST   /agents/{agent_code}/recommendations
POST   /agents/{agent_code}/actions
POST   /supervisor/policy/check
POST   /rag/query
POST   /rag/ocr/validate
```

Required agent payload fields:

- `agent_code`
- `entity_type`
- `entity_id`
- `requested_action` or recommendation type
- `decision_reason`
- `trace_id`
- `idempotency_key`
- `evidence_refs`
- confidence score where applicable

Frontend harness rule:

```text
agent output becomes visible to Customer, Driver, Transport Company, or Admin UI only after backend persistence and policy validation.
```

## Agent Inventory

| Agent | Code | Role | Primary Responsibilities | Forbidden Actions |
|---|---:|---|---|---|
| Customer Service Agent | `CSA` | Unified customer interface and support | Intake orders, resolve queries, coordinate support, surface order status | Confirm assignments, approve refunds, change order state directly |
| Order Management Agent | `OMA` | Order lifecycle orchestration | Validate orders, assign customer tier, coordinate matching, emit lifecycle events | Book vehicles without RMA confirmation, settle payments directly |
| Resource Management Agent | `RMA` | Vehicle, driver, and transport company allocation | Search inventory, score candidates, manage resource availability, coordinate transport company pool | Accept trips without OMS state approval, change pricing |
| Transportation Agent | `TMS` | Route optimization and execution monitoring | ETA, routing, driver movement, SLA monitoring, disruption response | Reassign drivers independently, change price or payment rules |
| Payment & Settlement Agent | `PSA` | Payment, invoice, commission, and settlement control | Razorpay/payment coordination, GST invoice handoff, settlement, reconciliation | Move money without approval, approve disputes alone |
| Platform Administration Agent | `PAA` | Governance, compliance, and oversight | User verification, policy enforcement, fraud/document checks, agent monitoring | Override financial controls without audit, bypass state machine |
| Communication Agent | `COMMS` | Multi-channel notification delivery | Push, SMS, email, WhatsApp, in-app templates, retry and delivery tracking | Change order truth, create unapproved promises |

## Core OMS Responsibilities

| Function | Autonomous Logic |
|---|---|
| Order ingestion | Ingest via customer app, validate payment mode, material type, vehicle specs, pickup/drop details, and required documents |
| Customer prioritization | Apply customer scoring and assign priority queue |
| Vehicle matching | Ask RMA/IMS to select using delivery type, material-to-body mapping, dimensions, capacity, age, location, ETA, and resource score |
| Driver assignment | Trigger assignment cascade according to express or standard workflow |
| Pricing | Use dynamic surcharge/discount logic through `pricing_engine.py` and payment rules |
| State orchestration | Emit canonical events such as `order_submitted`, `customer_tier_assigned`, `vehicle_candidates_found`, `driver_assigned`, and `order_confirmation_sent` |
| Fallback handling | Move through ETA, radius expansion, transport company pool, WhatsApp RAG, and customer notification |
| Auditability | Log `actor_id`, `trace_id`, `request_id`, `idempotency_key`, and `decision_reason` for every agent action |

## Customer Prioritization

OMS must prioritize simultaneous orders by customer tier and creation time:

`customer_tier DESC, created_at ASC`

| Tier | Identification Logic | OMS Priority Rule |
|---|---|---|
| High-Value | `order_volume >= 5/mo` + `payment_score >= 90` + `avg_shipment_value > ₹10k` | Priority 1: assign within **2 min**, override standard vehicle rules if needed |
| Second-Grade | `order_volume >= 2/mo` + `payment_score >= 70` + mixed distances | Priority 2: standard assignment within **5 min** |
| Least-Value | `orders < 1/mo` + `payment_score < 60` + frequent price negotiation | Priority 3: assign only after P1/P2; require **100% prepayment** |

Customer scoring should consider ROI, order volume, and payment discipline.

High-value customers are typically warehouses or MSMEs that place sequential orders, prefer reliable service over low price, place long-distance or multiple-vehicle shipments, and settle payments on time.

Second-grade customers are warehouses, MSMEs, and traders with less frequent but meaningful order volume, a mix of short and long distance orders, and generally reliable but sometimes delayed payment behavior.

Least-value customers include occasional warehouses, MSMEs, traders, small shops, and individual persons who place low-frequency orders, bargain heavily, pay late, and often request remote or difficult routes.

## Driver and Provider Segmentation

| Segment | Description | OMS/RMA Use |
|---|---|---|
| Driver cum owner | Owner drives one or two vehicles and carries direct maintenance responsibility | First preference for express when vehicle age and score qualify |
| Vehicle owner + salaried driver | Owner has multiple vehicles, often 3-5 or 5-10, operated by salaried drivers | Second preference when both owner and driver scores qualify |
| Transport service provider | Larger transport service provider with broader vehicle portfolio and domain experience | Emergency and low-inventory fallback, especially for high-value customers |

## Vehicle Selection and Matching

### Body Type Mapping

| Material Type | Required Body |
|---|---|
| Electronics, Pharma, Textiles, Furniture, Processed Food | Closed Body mandatory |
| Agri, Cement, Metals, Machinery, Raw Wood | Open Body |
| Perishables | Refrigerated, closed, and temperature-controlled |

OMS must block booking when a hard material/body rule is violated. Example: pharma cargo with a non-closed body vehicle must be rejected before assignment.

### Dimension and Capacity Matching

| Input Type | Matching Rule |
|---|---|
| By model, such as Eicher 20ft | Exact match; if unavailable, suggest the next-closest model |
| By dimensions, L x W x H | Match interior cargo space from `vehicle_model_db` within **±5% tolerance** |
| By tonnage, such as 1.5T | Select same or next higher class, max **+500kg**; never undersize |

When no exact match exists, OMS should show a clear alternative with the price delta, such as: "Your Eicher 20ft is not available. We found Ashok Leyland 22ft (₹10,500 vs ₹9,200). Proceed?"

### Vehicle Age Policy

| Delivery Type | Vehicle Age Rule |
|---|---|
| Express | **<=3 years old** + valid fitness + score >= 85 |
| Standard local, 15-50 km or <=50 km | Any age if fitness is valid |
| Standard long, >300 km | **<=7 years old** |

New vehicles within 3 years old should be reserved for express, long-distance, and high-accountability shipments when demand and inventory allow. Old vehicles should be preferred for local delivery in the 15-50 km band. IMS should also consider ETA, reserved vehicles, vehicles in transition, offline vehicles, and time-of-day availability patterns.

## Express vs Standard Delivery

### Express Delivery Assignment Cascade

Express delivery is for urgent or emergency customer needs. It requires well-conditioned vehicles and accountable drivers.

1. Driver + Vehicle Owner, where the owner drives the vehicle:
   - Vehicle age **<=3 years**
   - Reliability score >= 85
2. Vehicle Owner + Salaried Driver:
   - Owner score >= 80
   - Driver score >= 80
3. Transport Company:
   - Fleet score >= 75
   - Real-time availability

Pricing rule: standard service usually charges **10% commission**. Express delivery is a premium service that normally costs **30-50% higher than standard price** and may use **15% commission**. The polished OMS source also allows a **30-70% surge** band for express pricing; implementation should keep both values visible to product/finance and resolve the active pricing band in the pricing specification before code rollout.

### Standard Delivery Assignment

1. Search **5km radius** and assign the best available resource.
2. If none, expand to **10km radius**.
3. If none, approach transport company service providers.
4. If none, check ETA of incoming/arriving vehicles.
5. If none, broadcast via WhatsApp RAG Agent to registered transport companies.

For multiple bookings, OMS should message drivers in a 1:3 ratio: **1 vehicle and 3 drivers**. During low inventory, OMS must escalate to transport company service providers before declaring failure. The business policy is to avoid customer disappointment by continuing background search and offering practical alternatives.

Remote areas, worst-road-condition lanes, and hill station shipments may cost up to **50% higher** than normal transportation cost. Pricing should consider loading capacity, annual depreciation, fitness expenses, insurance, driver salary, fuel price, vehicle price, road tax, toll plaza charges, and state entry charges.

## Fallback and Escalation Protocol

| Step | Condition | Action |
|---:|---|---|
| 1 | No exact vehicle match | Suggest similar vehicle and show price delta |
| 2 | No vehicle in 10km | Check ETA of incoming vehicles |
| 3 | Still no match | Activate WhatsApp RAG Agent and scan transport company posts |
| 4 | High-value customer | RAG prioritizes high-score transport company vehicles |
| 5 | All options fail | Notify customer with wait/cancel/reschedule options and log to ops |

Required event:

`assignment_exhaustion -> notify_customer + log_to_ops`

## Payment, Invoice, and Trust Logic

| Scenario | OMS / Payment Agent Action |
|---|---|
| High-value customer with 1 pending payment | Allow new order and append pending amount to new invoice |
| Least-value customer | Block unless **100% prepayment** is completed |
| Express order cancellation | Apply **₹500 cancellation fee** as non-refundable |
| Abandoned cart | Trigger email and voice-assist prompt within **10 min** |
| Payment gateway failure | Preserve draft for **24h** and offer retry or payment proof upload |
| ToPay consent not given | After **24h**, allow consignor to pay, resend once, or cancel; auto-cancel in **2 hours** if no action |

Payment and invoice responsibility is split:

| Layer | System | Responsibility |
|---|---|---|
| Operational layer | OMS/Razorpay | Real-time payment processing, fraud/risk scoring, payment links, refunds, payment-order linking |
| Accounting layer | QuickBooks/Xero | GST-compliant invoices, receipts, ledgers, reconciliation, credit notes |

Commission and accounting rules:

- Drivers: platform commission is **10%** on standard orders.
- Transport companies: service fee is **₹700** where the transport-company model applies.
- Express: commission may be **15%**.
- Return leg orders marked `is_return_leg=True` get **20%** discount and remain linked to the outbound order through `loop_group_id`.
- Driver settlement liability records the remaining **90%** of the customer payment owed to the driver.
- Advance payment for logistics/goods uses proforma invoice plus payment receipt; GST is charged and paid only when the final tax invoice is issued at delivery.
- The platform charges GST on platform commission, not on shipment cost, when both driver and customer are unregistered.
- Net GST payable is calculated as output GST on commission minus input tax credit.

## Material and Compliance Guardrails

| Risk | Enforcement |
|---|---|
| Hazardous material declared | Require government documents and block if invalid |
| Wrong vehicle body | Reject during pre-assignment validation |
| RTO/checkpost stop | Platform has no platform liability; customer and driver must resolve shipment-document or material issue |
| Suspicious shipment documents | Notify customer/authorized person and escalate to operations/admin |
| Shipment doc scan failed | Driver must retry with full document in frame, no glare/shadow, and GPS within **500m** of consignor |
| Advance release after document scan | Advance payment release depends on valid scan; source scenario references **40%** release after valid scan |

## Agent Handoff Protocol

| Step | Trigger | Responsible Agent | Output Event |
|---:|---|---|---|
| 1 | Order created | Customer Service Agent | `order_submitted` |
| 2 | Validate customer tier | Order Management Agent | `customer_tier_assigned` |
| 3 | Match vehicle | Resource Management Agent | `vehicle_candidates_found` |
| 4 | Confirm assignment | Order Management Agent | `driver_assigned` |
| 5 | Calculate price | Payment & Settlement Agent | `final_price_calculated` |
| 6 | Notify customer | Communication Agent | `order_confirmation_sent` |
| 7 | Execute route | Transportation Agent | `shipment_execution_started` |
| 8 | Monitor exceptions | Transportation Agent + Platform Administration Agent | `exception_detected` or `sla_breach_detected` |

Event flow:

`Customer App -> OMA validate -> RMA assign -> OMA confirm state -> PSA price/payment -> COMMS notify`

Guardrails:

- OMA never assigns without RMA confirmation.
- RMA never books without optimistic lock.
- TMS never reassigns without OMS/RMA authorization.
- PSA never releases payment without required approval and state-machine eligibility.
- All agents log `actor_id`, `trace_id`, and `decision_reason`.
- LLM-backed decision calls should use deterministic settings, including `temperature=0`.

## Failure and Retry Scenarios

| Scenario | Trigger | Recovery Behavior |
|---|---|---|
| Payment gateway failure | Razorpay/payment gateway timeout, failure, or 3+ retries | Save order draft, offer retry with common Indian payment methods, allow payment proof upload, keep draft valid for **24h** |
| No vehicle found for standard order | IMS exhausts 5km, 10km, and transport company pool | Offer notify-when-available, similar vehicle with price delta, or reschedule |
| Express vehicle unavailable | No premium vehicle available within 15 mins | Offer wait **20 mins**, switch to standard, or escalate to priority queue for Tier-1/high-value customer |
| Driver unreachable | `driver_no_show_detected` after **15 min** | Auto-assign replacement through OMS/RMA and send revised ETA |
| Shipment doc scan failed | OCR/EXIF/GPS validation fails | Ask driver to rescan or upload from gallery; enforce **500m** GPS check |
| Consignee OTP rejected | OTP expired, wrong, or reused | Resend OTP, call consignee, or report issue; delivery cannot complete until verified |
| ToPay consent overdue | Consignee ignores or declines WhatsApp ToPay request for **24h** | Consignor can pay now, resend once, or cancel; auto-cancel in **2 hours** |
| Route disruption | Weather, accident, or delay >45 min | Reroute, notify consignee, update ETA, and guide driver |
| Refund processing delay | Refund stuck >24h | Show bank timeline: UPI instant, card **2-5 business days** |
| Draft recovery after crash/offline | App relaunch finds unsaved draft | Offer resume or discard |

## SLA Targets

| Metric | Target |
|---|---:|
| Express assignment time | <=2 min |
| Standard assignment time | <=5 min |
| Vehicle match accuracy | >=95% |
| High-value order drop rate | <=0.5% |

Locked transportation SLA breach rules from the state-machine implementation:

| Breach Type | Threshold | Grace Period |
|---|---:|---:|
| PICKUP_DELAY | 30 min | 15 min |
| DELIVERY_DELAY | 60 min | 30 min |
| POD_DELAY | 120 min | None |
| ROUTE_DEVIATION | 15% extra km | None |

## Memory, Orchestration, and Safety

| Area | Rule |
|---|---|
| Orchestration | LangGraph/agent reasoning may propose actions; workflow tools handle validation, retry, and DLQ; backend state machine and transition gateway remain the source of truth |
| Idempotency | Every output requires `idempotency_key`, `request_id`, or `assignment_request_id` |
| DLQ | Permanent failures go to Dead Letter Queue |
| Shadow mode | New models run in parallel before activation |
| Human-in-the-loop | Refunds above cap, SEV-1 incidents, suspicious compliance issues, and policy overrides require admin review |
| Memory | Use agent-segregated namespaces such as `oms_rules` and `dispute_history` |
| Retention | **90 Days Hot**, **1 Year Cold Archive** |

## Implementation Readiness Checklist

- [ ] OMA validates payment mode, material type, vehicle specs, customer tier, and required document flags before confirmation.
- [ ] RMA/IMS enforces material-to-body, dimensions, capacity, vehicle age, fitness, and score policies.
- [ ] Express and standard assignment cascades are implemented as deterministic workflows.
- [ ] Customer tier sorting uses `customer_tier DESC, created_at ASC`.
- [ ] Pricing engine supports standard **10% commission**, express **15% commission**, **30-50% higher** premium pricing, possible **30-70% surge** analysis band, remote surcharge up to **50%**, and transport company **₹700** fee.
- [ ] Payment and invoice integrations separate Razorpay/OMS operations from QuickBooks/Xero accounting.
- [ ] Failure prompts preserve user draft data and provide at least one forward path.
- [ ] All agent actions flow through [[07_State_Machine]] and produce auditable events.
- [ ] Related schema and event models remain aligned with [[08_Database_Schema]].
- [ ] Revenue and commission behavior remains aligned with [[01_Business_Model]].
- [ ] Return-trip scoring and discount behavior remains aligned with [[03_ReturnTrip_Algorithm]].

## Related Notes

- [[07_State_Machine]] - State graph and transition enforcement
- [[08_Database_Schema]] - Order, OrderEvent, and related data models
- [[01_Business_Model]] - Revenue and commission logic
- [[03_ReturnTrip_Algorithm]] - IMS return-trip scoring and loop logic
- [[Payment Settlement Agent]] - Payment and settlement behavior
- [[Finance and Invoice Event Layer for Logistics Platform]] - Finance event architecture
- [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]] - Invoice/accounting architecture
- [[Resource Management Agent]] - Resource allocation behavior
- [[Transportation Agent]] - Route and shipment execution behavior
- [[Communication Agent]] - Notification and customer messaging behavior

---

*Status: Governance Locked*
*Source: Cleaned integration from `D:\Agent Algo.txt`*
