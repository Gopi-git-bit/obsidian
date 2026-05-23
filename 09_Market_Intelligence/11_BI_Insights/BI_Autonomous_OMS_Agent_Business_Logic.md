# Autonomous OMS, IMS & Agent Business Logic

> **Operational rulebook for customer prioritization, vehicle assignment, fallback handling, and agent orchestration in Zippy Logitech**
> **Source Basis:** Extracted and normalized from user-provided OMS/IMS business-logic draft on April 13, 2026

---

## Executive Summary

| Decision Area | Adopted Logic | Zippy Impact |
|---------------|---------------|--------------|
| **Customer Priority** | High-value customers first, then second-grade, then least-value | Protects best customers during vehicle scarcity |
| **Vehicle Selection** | Match by body type, dimensions, model, then tonnage | Reduces damage risk and wrong-fit assignments |
| **Express Fulfillment** | Prefer owner-drivers, newer vehicles, higher score thresholds | Supports premium SLA and lower failure rate |
| **Standard Fulfillment** | 5 km → 10 km → ETA → transport company → WhatsApp RAG | Maximizes fill rate without over-promising |
| **Fallback UX** | Offer similar vehicle + price delta + ETA choice | Preserves conversion when exact inventory is unavailable |
| **Payment Guardrails** | High-risk customers prepaid; arrears appended for trusted customers | Balances growth with credit discipline |
| **Agent Model** | OMS validates, IMS matches, TMS executes, Payment settles, Communication notifies | Clean orchestration boundaries for AI agents |

---

## 1. Why This Note Exists

This file fills the gap between generic OMS lifecycle theory and Zippy's real marketplace operating rules.

It focuses on what was missing or only partially covered in existing notes:
- Customer-tier-based order priority
- Owner-driver vs salaried-driver vs transport-company assignment logic
- Material-to-body enforcement rules
- Express vs standard dispatch cascades
- ETA/radius/WhatsApp fallback rules
- Payment trust logic, arrears handling, and ToPay consent guardrails
- Agent-to-agent event handoff for autonomous execution

Cross-reference this note with:
- `BI_Order_Management_System_Lifecycle.md`
- `BI_Agent_System_Architecture.md` (5-agent system, communication, SLAs, policies)
- `BI_Pricing_Mechanism_Cost_Structure.md`
- `BI_Vehicle_Models_Database.md`
- `BI_Tech_Stack_ML_Systems.md`
- `BI_Payment_Compliance_Guide.md`
- `BI_EWay_Bill_Automation_Guide.md`

---

## 2. Customer Segmentation and OMS Priority

### Customer Tiers

| Tier | Identification Signals | OMS Priority | Payment Rule | Typical Profile |
|------|------------------------|--------------|--------------|-----------------|
| **High-Value** | `order_volume >= 5/month`, strong payment discipline, higher shipment value, recurring long-haul or multi-vehicle demand | **Priority 1** | Can continue ordering even with limited arrears, but arrears must be surfaced in current invoice | Warehouses, disciplined MSMEs, enterprise buyers |
| **Second-Grade** | Moderate order frequency, meaningful volume, mostly reliable but sometimes delayed settlement | **Priority 2** | Standard validation flow | MSMEs, traders, mixed short/long-haul buyers |
| **Least-Value** | Low frequency, high bargaining behavior, weak payment discipline, remote/inter-city low-volume orders | **Priority 3** | **100% prepayment** before assignment | Small traders, shops, occasional individual shippers |

### Scoring Dimensions

Customer scoring should prioritize these three dimensions:
1. **ROI contribution**
2. **Order volume / recurrence**
3. **Payment discipline**

### OMS Queue Rule

When multiple orders arrive together, sort by:

```text
customer_priority DESC -> created_at ASC
```

### Zippy Mapping

This logic fits Zippy's business model because the platform promise is not only cheap freight, but also **reliable matching within <=4 hours** for the customers who create the most repeat value.

---

## 3. Supply-Side Segmentation

| Segment | Definition | Strength | Risk | Best Use |
|---------|------------|----------|------|----------|
| **Driver-cum-owner** | Vehicle owner drives own truck | High accountability, better uptime, stronger care for asset | Limited fleet size | Express, critical orders, premium customers |
| **Owner + salaried driver** | Owner controls fleet but driver is employee | Higher inventory depth than owner-driver | Driver absenteeism, turnover, variable service quality | Standard orders, overflow, regional lanes |
| **Transport service provider** | Fleet operator or transport company | Large capacity pool, emergency backup | Higher dependence on third-party process discipline | Emergency sourcing, scarcity, bulk recovery |

### Marketplace Preference Order

1. Owner-driver
2. Owner + salaried driver
3. Transport service provider

This ordering is especially important for express and high-value orders.

---

## 4. Vehicle Selection Policy

### 4.1 Material -> Body Type Enforcement

| Material / Cargo Type | Required Body Type | Rule |
|-----------------------|--------------------|------|
| Electronics, electricals, textiles, toys, packaged food, grain flour, furniture, pharma, medicines, cartons | **Closed body** | Mandatory |
| Plastics, rubber, metals, machinery, auto tools, agri produce, cement, hollow blocks, sand, raw wood, commodity cargo | **Open body** | Default |
| Perishables / cold-chain goods | **Refrigerated** | Mandatory |

### Guardrail

If material type requires closed or refrigerated carriage and the candidate vehicle does not satisfy that body rule, OMS/IMS must reject the match before pricing or assignment.

### Body Type Mapping (Vehicle DB → OMS)

The vehicle models database uses these body types: `open`, `closed`, `tipper`, `tanker`, `trailer`.

The OMS material rules use: `open`, `closed`, `refrigerated`.

| DB Body Type | OMS Body Type | Rule |
|-------------|---------------|------|
| `open` | `open` | Direct match |
| `closed` | `closed` | Direct match |
| `tipper` | `open` | Tippers are open-body for cargo matching |
| `tanker` | `closed` | Tankers are enclosed; match to closed-body materials |
| `trailer` | `open` | Trailers match open-body unless specifically enclosed |

> See: `BI_Vehicle_Models_Database.md` §1 (schema), §3 (vehicle inventory)

### 4.2 Matching Hierarchy

Vehicle matching should follow this decision order:

1. **Body type compatibility**
2. **Specific model request** if customer named a model
3. **Interior cargo dimensions** for light but bulky / high-value goods
4. **Payload / tonnage class**
5. **Age and score constraints**
6. **Distance suitability and ETA**

### 4.3 Refined IMS Vehicle Matching Algorithm (4-Phase)

The IMS uses a **4-phase matching algorithm** that combines rule-based pre-filtering, ML-enhanced scoring, stable matching for return trips, and cascade fallbacks.

#### Phase 1: Pre-Filter (Rule-Based Elimination)

Filters out vehicles that cannot physically or contractually serve the order:

| Filter | Rule | Enforcement |
|--------|------|-------------|
| **Delivery type** | Express/Standard must match vehicle capability | Hard reject |
| **Material body type** | Material requires closed/open/refrigerated body | Hard reject |
| **Tonnage** | Order tonnage > vehicle capacity | Hard reject |
| **Dimensions** | Cargo must fit vehicle interior dimensions | Hard reject |
| **Vehicle age** | Must be below MAX_AGE_THRESHOLD (10 years default) | Hard reject |

> If no candidates survive Phase 1 → immediately trigger fallback cascade (Phase 4).

#### Phase 2: ML-Enhanced Scoring

Each surviving candidate is scored on a **weighted multi-factor model**:

| Factor | Weight | Source | Description |
|--------|--------|--------|-------------|
| **ETA prediction** | **40%** | LightGBM model | Minimize p50/p90 ETA errors; uses distance, RDS, traffic, weather, speed_factor |
| **Reliability score** | **25%** | Driver-rated events | Historical on-time performance, driver rating, owner score |
| **Eco impact** | **15%** | Fuel efficiency × RDS | Higher mileage + low RDS = better eco_score |
| **Return trip probability** | **10%** | NN similarity on historical pairs | Predict if a loaded return is likely from destination area |
| **3D bin packing efficiency** | **10%** | Cargo volume vs vehicle volume | Higher packing utilization = better score |

```text
weighted_score = (0.4 × (1/predicted_eta)) +
                 (0.25 × reliability_score) +
                 (0.15 × eco_score) +
                 (0.1 × return_trip_probability) +
                 (0.1 × 3d_bin_packing_efficiency)
```

Top 5 candidates ranked by weighted_score proceed to Phase 3.

#### Phase 3: Stable Matching for Return Trips (Gale-Shapley Inspired)

For orders with return trip potential, the algorithm pairs outbound deliveries with nearby return orders to reduce empty-leg miles:

- Uses **Gale-Shapley stable matching** logic
- Prioritizes pairs with high `return_trip_probability`
- Creates `loop_group` with combined settlement (15-20% discount)
- Reduces deadhead miles by 20-30%

#### Phase 4: Cascade Fallbacks (Probability-Based)

If no matched vehicle achieves confidence >= 0.7, or matching fails:

| Step | Fallback | Action |
|------|----------|--------|
| 1 | **Radius expansion** | Expand search from 5km → 10km → broader area |
| 2 | **TC database** | Query Transport Company fleet inventory |
| 3 | **WhatsApp RAG** | Scan transport company WhatsApp posts for availability |
| 4 | **Customer notification** | Offer similar vehicle + price delta + ETA choice |

```text
Trigger: matched['score'] < MIN_CONFIDENCE (0.7)
Action: fallback_cascade(order_details, matched)
Event: vehicle_matched → fallback_used
```

### 4.4 Dimension-First Logic

For electronics, packaged furniture, automotive components, cartons, or other low-weight / high-volume cargo, prefer:

```text
usable cargo dimensions > payload surplus
```

This avoids under-utilizing large-volume shipments in vehicles chosen only by tonnage.

### 4.5 Tonnage Matching Rule

| Case | Matching Rule |
|------|---------------|
| Exact tonnage available | Use exact or nearest standard model |
| Exact not available | Use **next higher class only** |
| Default oversize tolerance | Prefer <= 500 kg uplift |
| Small-vehicle market gap | If the market jumps to the next standard bracket (example: 1.5T -> 2T), allow it with customer approval |
| Undersized candidate | Never assign |

### 4.5 Similar-Match Customer Notice

If exact inventory is not available and the substitute increases price by >20%, customer must see:
- exact requested model not available
- nearest substitute model
- new amount vs expected amount
- ETA for the exact model if the customer prefers to wait

---

## 5. Vehicle Age and Quality Policy

| Use Case | Vehicle Age Rule | Additional Rule |
|----------|------------------|-----------------|
| **Express** | **<= 3 years** | Valid fitness + high driver / owner score |
| **Standard local (15-50 km)** | Older vehicles allowed | Fitness must be valid |
| **Standard regional / long (>300 km)** | Prefer **<= 7 years** | Avoid poor-condition units |
| **Long-distance premium** | Prefer newer fleet | Reliability first |

### Quality Score Thresholds

| Mode | Minimum Suggested Score |
|------|--------------------------|
| **Express owner-driver** | >= 85 |
| **Express owner + salaried** | owner >= 80, driver >= 80 |
| **Transport company fallback** | fleet >= 75 |

---

## 6. Express vs Standard Fulfillment Logic

### 6.1 Express Delivery Cascade

Express orders should use this allocation order:

1. **Driver-cum-owner** with new vehicle and strong score
2. **Owner + salaried driver** with high combined score
3. **ETA pool** for premium vehicles already inbound or soon available
4. **Transport service provider** if ETA misses promise window

### Express Pricing Rule

Source logic suggests:
- customer-facing premium of **+30% to +70%** over standard
- higher internal commission target (example: 15%)

### Zippy Mapping

Zippy's strategic target remains **3-5% platform fee** versus broker 8-12%.

Therefore, the better operating interpretation is:
- keep the core marketplace fee broker-lite
- apply **express premium as service surcharge**
- optionally charge higher managed-service fee only for enterprise premium handling workflows

### 6.2 Standard Delivery Cascade

Standard orders should use this order:

1. Search **5 km radius**
2. Expand to **10 km radius**
3. Check **ETA of inbound / transitioning vehicles**
4. Search **transport service providers**
5. Query **WhatsApp RAG pool** for third-party fleet availability

### Driver Broadcast Rule

For standard assignment, the system may notify supply in a **1 vehicle : 3 driver** broadcast ratio to improve response probability without over-reserving.

---

## 7. ETA, Reservation, and Scarcity Logic

IMS should track at least these resource states:
- online vehicles
- reserved vehicles
- in-transition / ETA vehicles
- offline vehicles
- transport-company fallback pool

### Scarcity Scenarios

| Scenario | Adopted Rule |
|----------|--------------|
| Express requested but exact premium vehicle unavailable | Use owner-driver → owner+salaried → ETA → transport company |
| Standard order but only newer vehicles are free | Allow new vehicle use if premium fleet is not under scarcity pressure |
| High-value customer needs multiple vehicles but recent bookings consumed inventory | Use ETA + WhatsApp RAG + transport-company sourcing to protect SLA |
| Customer refuses to wait | Offer similar vehicle with transparent delta |

### Demand-Aware Fleet Release Rule

OMS should evaluate:

```text
available_new_vehicles / current_express_demand
```

If premium fleet depth is adequate, newer vehicles may be released to standard orders. Otherwise they stay protected for express and high-value bookings.

---

## 8. Fallback and Exception Protocols

### Assignment Exhaustion Flow

| Step | Condition | Action |
|------|-----------|--------|
| 1 | No exact vehicle | Suggest nearest similar model |
| 2 | No nearby vehicle | Expand radius and inspect ETA |
| 3 | No ETA within SLA | Query transport companies |
| 4 | High-value order still unmatched | Query WhatsApp RAG with priority bias |
| 5 | All paths fail | Notify customer with wait/cancel choice |

### Canonical Event

```text
assignment_exhausted -> notify_customer -> log_to_ops
```

### Operational UX Recovery Patterns

| Event | Recovery Action |
|-------|-----------------|
| Payment gateway failure | Preserve draft, retry alternate method, allow proof upload |
| No vehicle found | Offer notify-me, similar vehicle, or reschedule |
| Driver unreachable | Auto-reassign and send revised ETA |
| Document scan failure | Ask for rescanning, gallery upload, and GPS proximity validation |
| OTP rejected | Resend OTP, call consignee, prevent false completion |
| ToPay consent overdue | Allow resend, payer switch, or cancellation |
| Route disruption | Re-route, update ETA, notify both sides |
| Refund delay | Show bank-dependent timeline and escalation path |
| Draft abandoned | Recover draft and prompt resume |

---

## 9. Payment, Trust, and GST Logic

### Payment Trust Rules

| Scenario | Rule |
|----------|------|
| High-value customer has one pending invoice | Allow new order, surface arrears in current invoice |
| Least-value customer | Require full prepayment |
| ToPay order | Do not assign until consignee consent is accepted |
| Express cancellation | Optional premium cancellation fee policy |

### Arrears Handling Message Pattern

Invoice layer should show:
- current shipment charge
- applicable GST
- previous unpaid amount
- prior transaction date / order id / reference id

### Ledger Structure

The financial model should maintain at least four ledgers:
1. **Commission income**
2. **Output GST liability**
3. **Input GST / ITC**
4. **Driver settlement liability**

### GST Principle

```text
Net GST Payable = Output GST on Commission - Input Tax Credit
```

### Compliance Reminder

If the platform operates as a marketplace intermediary, the compliance boundary must stay explicit:
- platform facilitates match and payment
- customer remains responsible for cargo legality and shipment declarations
- incidents such as revenue-department inspection must be logged, but liability follows the contractual shipment party unless platform misconduct is involved

See:
- `BI_Payment_Compliance_Guide.md`
- `BI_EWay_Bill_Automation_Guide.md`

---

## 10. Autonomous Agent Handoff Model

| Step | Trigger | Responsible Agent / System | Output Event |
|------|---------|----------------------------|--------------|
| 1 | Order created | Customer Service / OMS | `order_submitted` |
| 2 | Customer score evaluated | OMS | `customer_tier_assigned` |
| 3 | Vehicle search requested | IMS / Resource layer | `vehicle_candidates_found` |
| 4 | Driver / provider reserved | OMS + IMS | `driver_assigned` |
| 5 | Price finalized | Payment / Pricing engine | `final_price_calculated` |
| 6 | Order confirmed | Communication layer | `order_confirmation_sent` |
| 7 | Fallback exhausted | OMS + Communication | `assignment_exhausted` |

### Functional Boundary Model

| Layer | Responsibility |
|-------|----------------|
| **OMS** | validation, priority, state transitions, assignment orchestration |
| **IMS / Resource Management** | vehicle availability, ETA, owner/driver scoring, reservations |
| **TMS / Transportation** | route plan, execution tracking, reroute, ETA updates |
| **Pricing / Payment** | quote, surcharge logic, settlement, invoice, GST |
| **Communication** | SMS, email, WhatsApp, in-app notification |

---

## 11. Zippy Implementation Mapping

### Current Backend Alignment

| Existing Zippy Capability | Needed Extension from This Note |
|---------------------------|---------------------------------|
| Orders API | Add customer score, customer tier, service type, consent state |
| Matching API | Add body-type rules, model/dimension matching, age filters, ETA fallback |
| Pricing API | Add service-type premium, payment-risk logic, customer-tier adjustment |
| Bids / matches | Add owner score, driver score, source type, reservation TTL |
| ML services | Add demand-supply, vehicle age, congestion, RDS, customer type features |

### Recommended New Data Fields

- `customer_score`
- `customer_tier`
- `service_type` (`standard`, `express`)
- `body_type_required`
- `preferred_vehicle_model`
- `cargo_length_mm`, `cargo_width_mm`, `cargo_height_mm`
- `owner_score`, `driver_score`, `fleet_score`
- `vehicle_age_years`
- `eta_minutes`
- `source_pool` (`5km`, `10km`, `eta`, `transport_company`, `whatsapp_rag`)
- `topay_consent_status`
- `arrears_amount`

### SLA Targets Carried Forward

| Metric | Suggested Target |
|--------|------------------|
| Express assignment | <= 2 minutes |
| Standard assignment | <= 5 minutes |
| Vehicle match accuracy | >= 95% |
| High-value order drop rate | <= 0.5% |

---

## 12. Key Takeaways for Zippy Logitech

1. Zippy should treat **customer priority** and **vehicle quality gating** as first-class OMS rules, not post-processing logic.
2. Vehicle matching must support **body type + dimensions + model + tonnage**, not payload alone.
3. **ETA-aware fallback** is mandatory because exact inventory will often be unavailable in fragmented Indian road freight markets.
4. Express delivery should be implemented as a **premium service tier**, but without breaking Zippy's long-term 3-5% broker-lite positioning.
5. Payment trust logic must balance **conversion** with **credit discipline**, especially for repeat MSME customers.
6. The AI-agent model is viable only if canonical events, reservation TTLs, and cross-agent ownership boundaries are explicit.

---

## 13. Order State Machine (Canonical Transitions)

### Allowed State Transitions

| Current State | Allowed Next States | Event Emitted |
|--------------|---------------------|---------------|
| `draft` | confirmed, cancelled | `order_confirmed` or `order_cancelled` |
| `confirmed` | driver_assigned, cancelled | `driver_assigned` or `order_cancelled` |
| `driver_assigned` | enroute, cancelled | `shipment_enroute` or `order_cancelled` |
| `enroute` | driver_arrived_delivery | `driver_arrived_delivery` |
| `driver_arrived_delivery` | unloading_started | `unloading_started` |
| `unloading_started` | shipment_delivered | `shipment_delivered` |
| `shipment_delivered` | pod_uploaded | `pod_uploaded` |
| `pod_uploaded` | settlement_preprocessing | `delivery_completed` |
| `settlement_preprocessing` | completed | `settlement_released` |
| `completed` | (terminal) | — |
| `cancelled` | (terminal) | — |

> ⚠️ Any deviation from these transitions raises `InvalidStateTransition` and is logged as `invalid_state_transition_attempted`.

### Enforcement Rules

- No code may update `order.status` directly — all transitions go through `transition_order_state()`
- Each transition is atomic (DB row lock via `select_for_update`)
- Each transition emits an event to `order_event_logs`
- Supervisor can force-override via `force_transition()` with mandatory audit trail

---

## 14. Cancel & Reschedule Policies

### 14.1 Cancellation Rules

| Order Status | Customer | Driver | Admin/Supervisor |
|-------------|----------|--------|-------------------|
| `draft` | ✅ Allowed | — | ✅ |
| `confirmed` | ✅ Allowed | ✅ | ✅ |
| `driver_assigned` | ✅ Allowed | ✅ (via rejection) | ✅ |
| `enroute` | ❌ Blocked | ❌ Blocked | ✅ Override |
| `delivered`+ | ❌ Blocked | ❌ Blocked | ✅ Override |

**Events:** `order_cancelled`, `driver_rejection_cascade`

### 14.2 Reschedule Rules

Rescheduling allowed only **before enroute**:

| Order Status | Can Reschedule? | Effect |
|-------------|----------------|--------|
| `confirmed` | ✅ Yes | Update pickup time |
| `driver_assigned` | ✅ Yes | Update pickup time + emit `driver_reassignment_required` |
| `enroute`+ | ❌ No | Blocked by state machine |

**Events:** `order_rescheduled`, `driver_reassignment_required`

---

## 15. Driver Assignment Lifecycle

### Accept / Reject / Timeout Cascade

| Action | Trigger | Outcome |
|--------|---------|---------|
| **Accept** | Driver taps accept within 10 min | Status → `accepted`, order → `driver_assigned` |
| **Reject** | Driver taps reject | Status → `rejected`, emit `driver_rejection_cascade` → next driver |
| **Later** | Driver taps "later" | 900s exclusion pool, same as reject for assignment |
| **Timeout** | No response after 10 min | Status → `timed_out`, emit `driver_timeout_cascade` → next driver or escalate |

### Assignment Cascade (5km → 10km → TC → WhatsApp RAG)

| Step | Action | Event |
|------|--------|-------|
| 1 | Assign to nearest driver in 5km | `assignment_created` |
| 2 | If rejected/timed out → next driver in 5km | `driver_rejection_cascade` |
| 3 | If all 5km exhausted → expand to 10km | `assignment_expanded` |
| 4 | If 10km exhausted → query Transport Companies | `tc_fallback_triggered` |
| 5 | If TC exhausted → WhatsApp RAG broadcast | `whatsapp_rag_broadcast` |
| 6 | If all fail → notify customer | `assignment_exhausted` |

### Auto-Timeout Configuration

- **Driver acceptance window:** 10 minutes (600s)
- **Driver movement start:** 15 minutes
- **Timeout handler:** Runs via Celery beat every 60 seconds

---

## 16. Delivery Flow (Driver Arrival → POD → Settlement)

### 16.1 State Flow at Delivery

```
enroute → driver_arrived_delivery → unloading_started → shipment_delivered → pod_uploaded → settlement_preprocessing
```

### 16.2 Delivery Completion Rules

| Rule | Detail |
|------|--------|
| **OTP required** | Shipment delivered only if `consignee_otp_verified = true` |
| **POD required** | Settlement blocked without POD |
| **GPS + EXIF** | POD must include photo, EXIF metadata, GPS coordinates |
| **OTP one-time-use** | Single-use token with 5-minute TTL |

### 16.3 Settlement Gating

Settlement is a **multi-gated** operation:

```
POD uploaded → Supervisor policy_check → approve/hold/reject
  ↓ approve
settlement_preprocessing → Finance calculates payout
  ↓
settlement_released → driver receives payment
```

### 16.4 Invoice & Payout (GST Compliance)

| Document | Content |
|----------|---------|
| **Customer Tax Invoice** | Order ID, base fare, waiting penalty, GST (12% transport + 18% services), total |
| **Driver Payout Statement** | Gross fare, commission deducted, waiting penalty share, net payout |
| **Settlement PDF** | GST-ready, auditor-friendly, immutable documents |

---

## 17. GPS Tracking & Fraud Detection

### 17.1 GPS Ingestion Rules

| Rule | Detail |
|------|--------|
| **Allowed states** | Only `enroute`, `driver_arrived_delivery`, `unloading_started` |
| **Rejected states** | Before loading or after POD |
| **Payload** | `lat`, `lng`, `speed_kmph`, `heading`, `accuracy_m`, `timestamp` |
| **Storage** | Event-sourced (no hot tables), append-only |
| **Rate limiting** | 60 pings/min per driver (prevents GPS spam) |

### 17.2 GPS Signal Loss Detection

| Rule | Detail |
|------|--------|
| **Threshold** | No GPS ping received for 5+ minutes |
| **Event** | `gps_signal_lost` |
| **Action** | Supervisor alert, ops notification |
| **Escalation** | If signal lost > 30 min → contact driver → reassign if needed |

### 17.3 Route Deviation Detection

| Rule | Detail |
|------|--------|
| **Method** | Compare GPS trajectory against planned route polyline |
| **Threshold** | Distance from planned route > threshold |
| **Event** | `route_deviation_detected` |
| **Action** | TMS attempts reroute, notifies customer |

---

## 18. Production Hardening

### 18.1 Rate Limiting

| Endpoint | Rate | Purpose |
|----------|------|---------|
| GPS ingestion | 60/min per driver | Prevent GPS spam |
| OTP send | 5/min per phone | Prevent OTP abuse |
| Webhooks (Razorpay) | 30/min | Prevent webhook floods |
| General API | 100/min per user | Standard protection |

### 18.2 Authentication

| Method | Use Case |
|--------|----------|
| **JWT** | Customer app, Driver app (30 min access, 7 day refresh) |
| **Service tokens** | Agents, n8n, internal services |
| **Role-based** | IsDriver, IsCustomer, IsAdmin permissions |

### 18.3 Key Metrics to Track

| Metric | Threshold | Alert Action |
|--------|-----------|-------------|
| GPS silence | > 5 min | `gps_signal_lost` event |
| Assignment SLA | > 10 min | `assignment_exhausted` |
| Payment failure spike | > 10% in 1 hour | Supervisor alert |
| Settlement stuck | > 24 hours | Finance team notification |
| Fallback rate | > 10% | Degraded mode |
| Confidence < 0.3 | Any occurrence | `low_confidence` alert |

### 18.4 Graceful Degradation Levels

| Level | Condition | AI Enabled | Fallback Threshold | Features Disabled |
|-------|-----------|-----------|-------------------|-------------------|
| **Normal** | All systems healthy | ✅ Yes | < 5% | None |
| **Degraded** | Some agents struggling | ✅ Yes (higher confidence required) | < 10% | None |
| **Limited** | Multiple failures | ❌ No (rule-based only) | < 30% | predictive_routing, ml_pricing |
| **Emergency** | System-wide failure | ❌ No | Manual review | All AI features |

---

## 19. Deterministic Rules & Decision Engine

### 19.1 Rule Priority Order (Non-Negotiable)

The decision engine follows a strict priority chain. **No probabilistic model can override a deterministic rule.**

```
1. DETERMINISTIC GUARDRAILS (safety/compliance)
   ↓ ALL PASS
2. RULE ENGINE (fast, deterministic, high confidence)
   ↓ score < 0.85
3. CACHED CASES DB (historical matches)
   ↓ success_rate < 0.80
4. ML MODEL (LightGBM / GLM)
   ↓ confidence < 0.70
5. FALLBACK (rule-based or human review)
```

### 19.2 Deterministic Guardrails (Absolute Blockers)

| Category | Rule | Action on Failure |
|----------|------|-------------------|
| **Safety** | Vehicle has valid insurance and fitness certificate | REJECT |
| **Safety** | Driver has valid, non-expired license | REJECT |
| **Safety** | Cargo not on banned/dangerous goods list | REJECT |
| **Safety** | Cargo dimensions comply with govt regulations (no overloading) | REJECT |
| **Business** | Customer/Driver not blocked | REJECT |
| **Business** | ToPay order has consignee consent (OTP verified) | HOLD |
| **Business** | Vehicle body type matches material requirements | REJECT |
| **Pre-Condition** | Customer advance payment authorized | HOLD |

### 19.3 Decision Engine Flow

```
ORDER REQUEST
   ↓
DETERMINISTIC CHECKS (vehicle_insurance, driver_license, banned_cargo, blocked_user)
   ↓ PASS
RULE ENGINE (distance < 8km + reliability > 0.85 = accept)
   ↓ score < 0.85
CACHED CASES DB (origin_grid + dest_grid + vehicle_category + service_tier)
   ↓ success_rate < 0.80
ML MODEL (17 features → LightGBM confidence)
   ↓ confidence < 0.70
RULE FALLBACK (nearest available driver)
   ↓ no driver
HUMAN REVIEW QUEUE
```

### 19.4 Decision Output Schema

Every decision returns a structured JSON:

```json
{
  "decision": "accept|reject|hold|review",
  "confidence": 0.82,
  "driver_id": "D0042",
  "reason_codes": ["rule_confident", "vehicle_age_ok", "permit_ok"],
  "explanation": {
    "ruleHits": [{"rule_id": "R-NEAR-01", "score": 0.88}],
    "cacheCase": {"case_id": "c-001", "success_rate": 0.93},
    "modelOutputs": {"model_version": "v1.4", "score": 0.85, "confidence": 0.82},
    "deterministicChecks": {"vehicle_age_ok": true, "permit_ok": true}
  },
  "timestamps": {"evaluated_at": "2025-12-12T12:00:00Z"}
}
```

### 19.5 Cache Strategy (Multi-Layer)

| Layer | Store | Purpose | TTL |
|-------|-------|---------|-----|
| **L1: Redis** | Real-time state | Driver online/offline, vehicle telemetry, route cache | Volatile (5 min TTL) |
| **L2: PostgreSQL** | Persistent data | Orders, users, payments, scoring | 90 days hot, archive cold |
| **L3: TimescaleDB** | Time-series | Decision logs, telemetry, metrics | 2 years |
| **L4: S3 + Parquet** | Cold archive | Historical decisions, simulation results | 7 years |

### 19.6 Cached Cases DB Schema

Stores successful past decisions for fast lookup:

| Field | Purpose |
|-------|---------|
| `origin_grid` | Pickup location bucket (lat/lon bucketed) |
| `dest_grid` | Delivery location bucket |
| `vehicle_category` | LCV / MCV / HCV |
| `service_tier` | Standard / Express |
| `total_attempts` | Number of past orders |
| `successful_deliveries` | Number of successful completions |
| `success_rate` | Computed: successful / total |
| `best_driver_id` | Best-performing driver for this route |
| `best_vehicle_id` | Best-performing vehicle for this route |

**Accept threshold:** `success_rate >= 0.80`

---

## Cross-References

- `BI_Order_Management_System_Lifecycle.md`: generic OMS lifecycle, CODP, SOPs
- `BI_Pricing_Mechanism_Cost_Structure.md`: freight cost engine and surcharge structure
- `BI_Vehicle_Models_Database.md`: payload, dimensions, categories, body types
- `BI_Tech_Stack_ML_Systems.md`: LightGBM, OR-Tools, DRL4Route, feature-store architecture
- `BI_Payment_Compliance_Guide.md`: Razorpay, GST, invoicing, KYC
- `BI_EWay_Bill_Automation_Guide.md`: document automation and compliance boundary
- `BI_Third_Party_Logistics_3PL.md`: transport-company fallback and ecosystem role