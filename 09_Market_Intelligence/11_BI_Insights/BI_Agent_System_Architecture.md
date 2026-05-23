# 5-Agent Autonomous System Architecture

> **System architecture, agent roles, communication model, SLAs, policies, and admin playbook for Zippy Logitech's autonomous logistics platform**
> **Source:** Extracted from user-provided Autonomous Agentic AI PRD (5-Agent Architecture)
> **Cross-reference:** `BI_Autonomous_OMS_Agent_Business_Logic.md` (business rules), `BI_Tech_Stack_ML_Systems.md` (ML stack)

---

## Executive Summary

Zippy Logitech operates a **5-agent autonomous system** for real-time supply chain orchestration. Each agent owns a specific domain, communicates via structured events through an event bus, and the Supervisor enforces policies to prevent unsafe actions.

| Layer | Component | Technology |
|-------|-----------|------------|
| **Client** | Customer App, Driver App, Transport Co Portal, Admin Console | React Native / Expo |
| **API** | Orders, Driver Ops, Vehicle Inventory, Payment, OCR, Routing | **FastAPI** (existing implementation — see `backend/`) |
| **Event Bus** | AgentCommunicator, Dead Letter Queue, Retry Orchestrator | Redis Streams / Kafka + Celery |
| **Agents** | Supervisor, Operations, Transport, Finance, RAG | Deterministic rules + LLM reasoning |
| **External** | Razorpay, WhatsApp Business API, Mapbox/Google Maps, OCR models, LLMs | API integrations |

---

## 1. The 5 Agents — Core Responsibilities

### 1.1 Supervisor Agent (Cogito Brain)

**Role:** Central brain — strategic decisions, conflict resolution, policy enforcement.

| Responsibility | Detail |
|----------------|--------|
| Arbitration | Resolves disputes between agents |
| Policy enforcement | Safety, payment, driver penalties |
| Hallucination detection | Flags conflicting or fabricated responses |
| Fallback triggering | Switches to deterministic rules when LLM uncertain |
| Performance monitoring | Tracks agent metrics, kills/restarts tasks |
| SLA enforcement | Timeout and SLA constant enforcement |
| Agent versioning | Manages agent deployments |

**Typical Decisions:**
- Driver no-show → Reassign
- Payment mismatch → Hold settlement
- Consignee OTP failed → Mark as risk case
- IMS exhausted drivers → Escalate to Admin

---

### 1.2 Operations Agent (OMS Owner)

**Role:** Owns the entire order lifecycle from draft → confirm → assignment → delivery → communication.

| Responsibility | Detail |
|----------------|--------|
| Order parsing | Validate consignor/consignee info |
| ToPay consent | Trigger consent workflows before assignment |
| Pricing quotes | Generate quotes with RDS scoring |
| Booking confirmation | Confirm and dispatch orders |
| Driver orchestration | Trigger driver search via IMS interface |
| State machine | Dispatch and order tracking states |
| Notifications | Trigger customer and driver notifications |

**Events Owned:**

```
order_draft_created
consignor_details_submitted
consignee_details_submitted
customer_payment_initiated
topay_consent_requested
order_confirmed
driver_assigned
vehicle_arriving
loading_started
loading_delayed
shipment_enroute
shipment_delivered
pod_uploaded
feedback_received
```

---

### 1.3 Transport Agent (TMS Owner)

**Role:** Vehicle assignment, routing, ETA predictions, RDS computation, en-route incidents.

| Responsibility | Detail |
|----------------|--------|
| Multi-step driver search | 5km → 10km → Transport Company fallback |
| RDS computation | Route Difficulty Score calculation |
| Routing + ETA | Dynamic routing and ETA updates |
| Deviation detection | Monitors breakdowns and reroutes |
| Dynamic reassignment | Reassigns vehicles as needed |
| Driver monitoring | Offline detection, phone-off escalation |

**Events Owned:**

```
vehicle_search_started
vehicle_search_failed
driver_accept_timeout
driver_started_trip
driver_arrived_pickup
driver_arrived_delivery
route_updated
incident_detected
breakdown_recovery_started
```

---

### 1.4 Finance Agent (Payment + Settlements)

**Role:** Advance payment, ToPay logic, invoice generation, settlement, refunds, fraud checks.

| Responsibility | Detail |
|----------------|--------|
| Payment idempotency | Uses `attempt_id` for all payment operations |
| Razorpay webhook | Handles gateway events |
| Advance release | Releases 40% after doc_scan validation |
| Final settlement | After OTP verification |
| Refunds | Per refund policy rules |
| ToPay consent | Enforcement before assignment |
| Fraud heuristics | Fake POD, GPS mismatch detection |

**Events Owned:**

```
payment_intent_created
advance_released
payment_failed
payment_captured
refund_initiated
settlement_scheduled
settlement_released
```

---

### 1.5 RAG / Knowledge Agent

**Role:** Contextual intelligence provider for all other agents.

| Responsibility | Detail |
|----------------|--------|
| Rule retrieval | Pricing rules, RDS definitions, policy documents |
| Document validation | OCR + EXIF verification on uploaded docs |
| Vehicle type suggestion | Recommend correct vehicle based on cargo |
| Return-trip optimization | Suggest loop/discount opportunities |
| Factual reasoning | Provide answers with source citations |

---

## 2. Agent-to-Agent Communication Model

All communication flows through **AgentCommunicator** using **Redis Streams** or **Kafka**.

### Message Format

```json
{
  "message_id": "uuid",
  "from_agent": "operations_agent",
  "to_agent": "transport_agent",
  "intent": "find_driver",
  "payload": { },
  "timestamp": "ISO-8601",
  "idempotency_key": "uuid",
  "priority": "low|normal|high",
  "trace_id": "uuid"
}
```

### Intent Values

`find_driver`, `confirm_reservation`, `release_reservation`, `compute_rds`, `request_payment`, `policy_check`, etc.

### Priority Levels

| Priority | When Used | Subscriber |
|----------|-----------|------------|
| **low** | Background tasks | Standard workers |
| **normal** | Standard operations | Standard workers |
| **high** | Fraud, safety incidents, critical events | **Supervisor** subscribes directly |

---

## 3. Retry Semantics & Idempotency

### HTTP Retry (Agent-to-Agent REST)

| Response | Action |
|----------|--------|
| **5xx / 429** | Retry up to 3 times with exponential backoff (1s, 2s, 4s) |
| **4xx (except 409)** | Do not retry; fix payload |
| **409 Conflict** | Optimistic lock collision — abort and fetch next candidate, or retry with jitter (up to 3s) |

### Message Bus Retry

- Consumer retries N times (recommended: 5) with exponential backoff (100ms × 2^attempt)
- After N retries → send to DLQ topic `agent.dlq` with `error_context` and `last_error`
- Supervisor watches DLQ depth; triggers manual review when threshold exceeded

### Payment Flows

- Use idempotent `attempt_id` for all payment operations
- No client-side duplicate attempts — rely on gateway idempotency + server reconciliation
- Reconciliation job runs nightly for failed/ambiguous attempts

### Idempotency Rules

| Rule | Detail |
|------|--------|
| **Key required** | All state-changing endpoints and bus messages must include `idempotency_key` |
| **Dedup window** | 24 hours (default) |
| **Same key + same payload** | Return previous response |
| **Same key + different payload** | Return `409 IDENTITY_MISMATCH` |
| **Reservation TTL** | 300 seconds (5 min) for vehicle reservations |
| **Reservation table** | `vehicle_reservations{vehicle_id, reservation_id, expires_at}` with unique constraint |

---

## 4. Error Codes (Canonical List)

| Code | HTTP | Meaning | Retry? |
|------|------|---------|--------|
| `INVALID_INPUT` | 400 | Validation failed | No |
| `UNAUTHORIZED` | 401 | Service JWT invalid | No |
| `FORBIDDEN` | 403 | Action disallowed by policy | No |
| `NOT_FOUND` | 404 | Resource missing | No |
| `CONFLICT` | 409 | Optimistic lock/reservation conflict | Next candidate |
| `RATE_LIMIT` | 429 | Client rate limit | Yes (backoff) |
| `TEMPORARY_ERROR` | 500 | Transient error | Yes |
| `PERMANENT_ERROR` | 500 | Permanent error | No |
| `DLQ_PUSHED` | 503 | Message moved to DLQ | Manual review |
| `POLICY_VIOLATION` | 422 | Failed Supervisor check | Fix policy context |

---

## 5. System-Wide Constraints & SLAs

### 5.1 Timeouts & SLAs

| Metric | Target |
|--------|--------|
| Driver acceptance window | **10 minutes** (600s offer TTL) |
| Driver movement start | **15 minutes** |
| Loading grace period | **15 minutes** (warning at 1 hour) |
| Consignee OTP verification | **≤ 2 seconds** |
| Express assignment | **≤ 2 minutes** |
| Standard assignment | **≤ 5 minutes** |
| Vehicle match accuracy | **≥ 95%** |
| High-value order drop rate | **≤ 0.5%** |

### 5.2 Pricing Constraints

| Constraint | Value |
|------------|-------|
| Express shipping multiplier | **+30% to +70%** |
| Remote/hill surcharge | **+35% to +50%** |
| Loop-discount | **15–20%** (only if both legs committed) |

### 5.3 Evidence & Fraud Rules

| Rule | Detail |
|------|--------|
| POD requirements | Photo + EXIF + GPS match + OTP (all four) |
| Shipment doc | OCR validation required |
| Driver misconduct | Immediate event to Risk team |

### 5.4 Safety

| Rule | Detail |
|------|--------|
| Hazardous goods | Must block assignments |
| Driver phone-off | Auto-escalate |

---

## 6. High-Level Flows

### 6.1 Customer Booking → Assignment → Delivery

```
Step 1: Customer submits order (Operations Agent)
   ↓
Step 2: Validate + price quote with RDS (Operations ↔ Transport ↔ RAG)
   ↓
Step 3: ToPay consent if required (Finance Agent)
   ↓
Step 4: Driver search (Transport + IMS)
   ↓
Step 5: Driver accepts (10m SLA) (Transport Agent)
   ↓
Step 6: Shipment doc scan → 40% advance release (Driver App → Finance)
   ↓
Step 7: Enroute + telemetry (Transport Agent)
   ↓
Step 8: POD scan + OTP (Driver App → OMS + Finance)
   ↓
Step 9: Settlement + rating (Finance Agent + Operations)
```

### 6.2 Breakdown / Incident Flow

```
Step 1: vehicle_breakdown_reported
   ↓
Step 2: Supervisor evaluates severity
   ↓
Step 3: Transport Agent attempts recovery (30 min SLA)
   ↓
Step 4: If fail → Reassign vehicle OR escalate to Admin
   ↓
Step 5: Customer notified throughout
```

### 6.3 Loop / Return-Trip Optimization Flow

```
Step 1: Outbound delivery completes
   ↓
Step 2: RAG Agent queries trade clusters
   ↓
Step 3: IMS finds nearest matching return route
   ↓
Step 4: Operations Agent suggests discounted return-trip
   ↓
Step 5: Driver accepts → loop_group created
   ↓
Step 6: Combined settlement for both legs (15-20% discount)
```

---

## 7. Supervisor Policy Engine

### Policy Evaluation Order

```text
If any matched policy has action == "reject" → decision = "reject"
Else if any matched policy has action == "hold" → decision = "hold"
Else if any matched policy has action == "approve" → decision = "approve"
Else → decision = "hold" (safe default)
```

### Key Policies

| Policy ID | Action | Priority | Trigger |
|-----------|--------|----------|---------|
| `P_ADVANCE_RELEASE_BASIC` | approve | high | doc_valid=true, consignor_verified=true, fraud_score<0.02 |
| `P_ADVANCE_RELEASE_HIGH_RISK` | hold | critical | doc_valid=false OR fraud_score>=0.02 OR scan_exif_mismatch |
| `P_SETTLEMENT_RELEASE_BASIC` | approve | high | pod_verified=true, otp_verified=true, fraud_score<0.015, driver_score>50 |
| `P_SETTLEMENT_SUSPECT` | hold | critical | fraud_score>=0.015 OR driver_score<50 OR otp_replay_detected |
| `P_DRIVER_BLACKLIST_HARD` | reject | critical | driver_id in blacklist |
| `P_HAZARDOUS_GOODS_BLOCK` | hold | high | material_is_hazardous=true OR declared_hazardous=false |
| `P_RDS_SURCHARGE_APPROVAL` | approve | medium | RDS category in R0-R2 |
| `P_DLQ_SPIKE` | hold | high | dlq_depth>=50 OR dlq_rate>=10/min |

### Policy Enforcement Semantics

| Action | Effect |
|--------|--------|
| **approve** | Proceed with the action |
| **hold** | Pause; push `settlement_hold` event; notify Ops + Admin; require human review |
| **reject** | Block entirely; log attempt; remove from candidate lists |

---

## 8. Admin Playbook

### 8.1 When Supervisor Decision = Hold

**Step 1 — Gather Context (2 min)**
- Open order timeline (order_id)
- Collect: trace_id, request_id, idempotency_key
- Review events: shipment_doc_scanned, pod_scanned, consignee_otp_verified
- Check fraud indicators: fraud_score, scan_exif_mismatch, ocr_confidence, otp_replay_detected
- Driver info: driver_id, reliability_score, past_strikes
- Payment info: attempt_id, gateway_status, escrow_status

**Step 2 — Quick Triage (5-10 min)**

| Condition | Action |
|-----------|--------|
| fraud_score >= 0.05 | Escalate to Fraud Team (P0 ticket) |
| doc_valid=false + scan_exif_mismatch | Ask driver for additional photos; get consignor phone confirmation |
| otp_replay_detected=true | Call consignee to verify identity; do NOT release funds |

**Step 3 — Evidence Collection Checklist**
- Download pod_photo (store in audit bucket) + EXIF metadata
- Export driver_gps_trace (last 2 hours)
- Export OCR result + original scan
- Export payment gateway webhook payloads + settlement ledger entries
- Save all to `audit/<order_id>/<timestamp>/` with trace_id in filenames

**Step 4 — Actions by Risk Level**

| Case | Condition | Action |
|------|-----------|--------|
| **A (low-risk)** | doc_valid=true, fraud_score<0.015 | Approve release; record admin_override_reason + admin_id |
| **B (medium-risk)** | fraud_score 0.015-0.05 | Hold 24-72 hours; require extra proof (photo + video + consignor email) |
| **C (high-risk)** | fraud_score>=0.05 or criminal indicators | Freeze indefinitely; notify Legal; mark driver suspended; escalate to police if needed |

**Step 5 — Audit Closure**

```json
{
  "event": "admin_override",
  "order_id": "ord_xxx",
  "admin_id": "admin_42",
  "action": "approve|hold|reject",
  "reason": "Free text + template code",
  "evidence_urls": ["s3://..."],
  "trace_id": "trace-xxx",
  "timestamp": "ISO"
}
```

### 8.2 DLQ Spike Runbook

**Trigger:** DLQ depth >= 50 or rate >= 10/min

**Immediate (first 5 min):**
1. Pause non-critical retry workers
2. Inspect top 10 DLQ messages (via `/v1/supervisor/dlq/inspect`)
3. If malformed payload → hotfix API gateway to reject invalid messages
4. Notify SRE + Ops

**Remediation (15-60 min):**
- Fix root cause (schema validation, auth, transient infra)
- Reprocess DLQ items selectively (manual replays)
- If fraud-sensitive events → escalate to Fraud team before reprocessing

**Post-mortem:** RCA + action items + schema updates + producer input validation

### 8.3 Driver Blacklisting Workflow

**Trigger:** 3x no-show within 30 days, confirmed misconduct, or proof from customer

1. Add to staging blacklist (soft block) → agent stops assigning
2. Notify driver with reason + appeal process
3. If permanent → set `driver.status=BLACKLISTED`, revoke tokens, remove vehicles from inventory

### 8.4 Admin Override Rules

- Two-person approval required if payout > ₹100,000 or fraud_score > 0.03
- All overrides create immutable audit entries (admin_id, admin_role, justification, attachments)
- Rollback requires idempotent `rollback_settlement` referencing attempt_id

---

## 9. OpenAPI Contract Summary

### Combined Endpoints (Single Gateway Spec)

| Tag | Endpoint | Method | Purpose |
|-----|----------|--------|---------|
| **orders** | `/v1/orders/submit` | POST | Submit order for orchestration |
| **orders** | `/v1/orders/{id}/status` | GET | Canonical order status + timeline |
| **orders** | `/v1/orders/{id}/driver_response` | POST | Receive driver ACCEPT/CANCEL/LATER (idempotent) |
| **transport** | `/v1/transport/assign` | POST | Attempt vehicle assignment (creates reservations) |
| **transport** | `/v1/transport/reservations/{id}/confirm` | POST | Confirm reservation (idempotent) |
| **transport** | `/v1/transport/rds/compute` | POST | Compute Route Difficulty Score |
| **finance** | `/v1/finance/payments/intents` | POST | Create payment intent / escrow |
| **finance** | `/v1/finance/payments/webhook` | POST | Razorpay webhook handler |
| **finance** | `/v1/finance/settlements/schedule` | POST | Schedule settlement (calls Supervisor) |
| **rag** | `/v1/rag/query` | POST | Query knowledge base with provenance |
| **rag** | `/v1/rag/ocr/validate` | POST | Validate OCR/EXIF on uploaded document |
| **supervisor** | `/v1/supervisor/policy/check` | POST | Run policy checks |
| **supervisor** | `/v1/supervisor/dlq/inspect` | GET | Inspect DLQ items |

### Key Event Schemas

| Event | Required Fields |
|-------|-----------------|
| `order_assigned` | event, timestamp, order_id, candidate_driver_id, candidate_vehicle_id, payload |
| `driver_response` | event, timestamp, order_id, driver_id, action (ACCEPT/CANCEL/LATER), idempotency_key |
| `shipment_doc_scanned` | event, timestamp, order_id, driver_id, doc_type, doc_url, scan_exif |
| `pod_scanned` | event, timestamp, order_id, driver_id, pod_url, consignee_otp |
| `agent_message` | message_id, from_agent, to_agent, intent, payload, timestamp, idempotency_key, trace_id |

### Field Validation Rules

| Field | Rule |
|-------|------|
| phone | E.164 format (e.g. +9198XXXX) |
| pincode | 6-digit string (India) |
| coordinates | lat ∈ [-90,90], lng ∈ [-180,180] |
| currency | ISO 4217 (INR default) |
| amount | Integer (paise) or 2 decimal; non-negative |
| OTP | 4-6 digits; single-use; TTL 5 min |
| document URLs | Signed URLs; validate expiration on upload |

---

## 10. LLM Prompt Templates

### Guidelines for All Agent Prompts
- Bind agent role and allowed tools (RAG, SQL, OR-Tools, Payment SDK) at system level
- Require JSON-only responses (no prose)
- Use `temperature=0.0` for deterministic outputs
- Include `confidence` field (0.0-1.0); if < threshold, escalate to Supervisor
- Sanitize incoming context strings before sending to LLM prompts (prompt injection protection)

### Confidence Thresholds

| Agent | Approve Threshold | Escalate Threshold |
|-------|-------------------|-------------------|
| Supervisor | >= 0.85 | < 0.70 → hold |
| Operations | >= 0.75 | < 0.75 → correction only |
| Transport | >= 0.75 | < 0.75 → Supervisor policy_check |
| Finance | >= 0.80 | < 0.80 → do not auto-release funds |
| RAG | citation score > 0.6 | < 0.6 → return empty answer, require human lookup |

---

## 11. Example Happy-Path Message Flow

```
1. Operations → Transport: /v1/transport/assign
   idempotency_key: "assign-req-123"
   → Transport returns candidates + reservation_id (TTL 300s)

2. Transport → Agent Bus: order_assigned event
   same idempotency_key

3. Driver taps ACCEPT → Mobile → Operations: driver_response
   idempotency_key: "drvresp-0001"

4. Operations → Transport: /v1/reservations/{id}/confirm
   same idempotency key
   → If 409 (reservation consumed) → try next candidate

5. Driver scans doc → Finance: shipment_doc_scanned
   OCR + EXIF validation → advance_released (40%)

6. Driver arrives → POD + OTP → Finance: pod_scanned
   Supervisor policy_check → settlement

7. Finance → /v1/finance/settlements/schedule
   Supervisor: approve (if all checks pass)
```

---

## 12. Developer Checklist

- [ ] JSON Schema validation at API gateway for all event endpoints
- [ ] Idempotency key store (Redis or Postgres) with 24h TTL
- [ ] `vehicle_reservations` table with unique constraint + TTL eviction
- [ ] DLQ wiring + Supervisor alerts
- [ ] Nightly reconciliation jobs for payments
- [ ] Policy YAML versioning + audit trail
- [ ] Prompt injection protection on all LLM inputs
- [ ] HTTP retry logic (3 attempts, exponential backoff: 1s, 2s, 4s)
- [ ] Message bus retry logic (5 attempts, exponential backoff: 100ms × 2^attempt)

---

## 13. Celery Integration Plan (Route Optimization)

### RoutePlan Data Model

| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Primary key |
| `order` | FK → Order | Associated order |
| `vehicle` | FK → Vehicle | Assigned vehicle |
| `optimizer_type` | Enum | `return_trip`, `backhaul`, `hybrid` |
| `routes` | Array[Array[int]] | Node sequences (e.g., [[0,3,1], [0,2,4]]) |
| `total_cost` | float | Predicted route cost (km or weighted units) |
| `empty_leg_km` | float | Estimated empty-leg distance |
| `confidence_score` | float | Fallback trigger if < 0.7 |
| `created_at` | timestamp | Creation time |

### Celery Task: optimize_loaded_return

**Trigger:** On `order_confirmed` / `vehicle_matched`

**Flow:**
1. Fetch order + vehicle details
2. Build distance matrix (PostGIS)
3. Query nearby return opportunities (within 75km radius)
4. Build node list: depot=0, deliveries=1..N, backhauls=N+1..
5. Choose optimizer: BackhaulOptimizer (if confirmed backhauls) or ReturnTripOptimizer (if speculative)
6. Set return_weights: 8x boost on backhaul edges
7. Run ACO optimization (30 ants, 100 iterations)
8. Save RoutePlan to DB
9. If confidence < 0.7 → trigger fallback cascade
10. Push routes to driver app via WebSocket

**Confidence Logic:**
| Condition | Confidence |
|-----------|-----------|
| Confirmed backhauls exist | 0.9 |
| No backhauls, speculative only | 0.65 |
| Route cost > 2x baseline | 0.4 |

### API Endpoint

`POST /api/agents/transportation/optimize-route/`
- Request: `{ order_id, vehicle_id }`
- Response: `{ status: "optimization_started", task_id }`

### Empty-Leg Estimation

```text
For each route in routes:
  for each edge in route:
    total_empty_km += distance[edge.from][edge.to]
  if last_node is not backhaul:
    total_empty_km += distance[last_node][depot]  # empty return
```

---

## 14. Simulation Framework

### Decision Simulator

Runs AI agents against **historical order data** to validate decisions before production deployment.

**Architecture:**

| Component | Purpose |
|-----------|---------|
| `data_loader.py` | Load 3 months of historical orders, drivers, weather/traffic |
| `decision_simulator.py` | Feed historical orders through isolated OMS/IMS/TMS agents |
| `metrics_collector.py` | Compare AI decisions vs actual outcomes |
| `report_generator.py` | Generate simulation report with accuracy, fallback rates, ETA errors |

### Simulation Pipeline (5 Steps)

1. **Feed order to OMS** → approve/reject decision
2. **Feed to IMS** → vehicle/driver match decision
3. **Feed to TMS** → route plan, ETA prediction
4. **Compare with reality** → vehicle match accuracy, ETA error, route efficiency, problem prediction
5. **Record metrics** → per-order comparison stored

### Simulation Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| OMS approval accuracy | ≥ 92% | Approval matches actual delivery |
| Vehicle match accuracy | ≥ 85% | Simulated vehicle matches actual |
| ETA accuracy (p50) | ≤ 45 min | Median ETA prediction error |
| Route efficiency | ≥ 90% | Simulated distance vs actual |
| Problem prediction recall | ≥ 70% | Predicted problems match actual |

### Simulation → Retraining Feedback Loop

| Condition | Action |
|-----------|--------|
| `fallback_success_rate < 0.90` | Trigger model retraining |
| `eta_error_p90 > 1800 seconds` | Trigger model retraining |
| `first_candidate_success_rate < 0.85` | Trigger model retraining |
| `oms_approval_accuracy < 0.92` | Trigger model retraining |

**Retraining:** Celery task → model retraining → canary deployment

---

## 15. AI Agent Monitoring & Observability

### Decision Auditing

Every agent decision is logged to:

| Backend | Purpose |
|---------|---------|
| **PostgreSQL** | Structured querying, audit trail |
| **TimescaleDB** | Time-series analysis (decision logs partitioned by date) |
| **PostHog** | Behavioral analytics (fallback rates, confidence trends) |
| **Sentry** | Error tracking, anomaly alerts |

### Logged Decision Fields

| Field | Description |
|-------|-------------|
| `agent_name` | oms, ims, tms, payment, verification |
| `decision_id` | Unique decision identifier |
| `order_id` | Associated order |
| `input_features` | What the agent received |
| `output_decision` | What the agent decided |
| `confidence_score` | 0.0-1.0 |
| `model_version` | Which model version was used |
| `processing_time_ms` | Execution time |
| `rule_applied` | Which business rules were triggered |
| `fallback_triggered` | Whether fallback was used |

### Anomaly Detection Rules

| Anomaly Type | Condition | Severity | Action |
|-------------|-----------|----------|--------|
| **Low confidence** | `confidence < 0.3` | High | Alert + review |
| **Slow processing** | `processing_time_ms > 5000` | Medium | Check server load |
| **High fallback rate** | `fallback_rate > 10%` in 1 hour | Medium | Model drift check |
| **Confidence distribution change** | KS test p-value < 0.01 | Low | Monitor for drift |
| **Multiple anomalies** | > 5 in 10 minutes | Critical | Auto-switch to rule-based |

### Alerting Channels

| Channel | Use Case |
|---------|----------|
| **Slack** | Warnings, low-confidence decisions |
| **PagerDuty** | Critical anomalies, system failures |
| **Email** | Daily health reports, weekly summaries |
| **Dashboard** | Real-time gauges, confidence trends |

### Key Metrics to Track

| Metric | Prometheus Query |
|--------|-----------------|
| Fallback rate per agent | `rate(fallback_triggered_total{agent="oms"}[5m]) / rate(decision_total{agent="oms"}[5m])` |
| Model confidence p10 | `histogram_quantile(0.10, rate(decision_confidence_bucket[5m]))` |
| Processing time p99 | `histogram_quantile(0.99, rate(processing_time_seconds_bucket[5m]))` |

---

## 16. Chaos Engineering & Fallback Testing

### Chaos Simulator

Tests multi-agent cascading failures:

| Scenario | Injected Failure | Expected Outcome |
|----------|-----------------|-----------------|
| **Map API + Payment down** | MapmyIndia timeout + Razorpay gateway failure | TMS fallback → payment offline mode |
| **OMS ↔ IMS partition** | IMS unreachable | OMS uses rule-based fallback or manual review |
| **Regional DB outage** | Mumbai DB down | Failover to Hyderabad replica |
| **Multi-agent failure** | TMS + Payment failing together | Graceful degradation cascade |

### Fallback Testing Strategy

| Test Type | Purpose | Run Frequency |
|-----------|---------|---------------|
| **Unit tests** | Individual fallback strategies | Every commit |
| **Integration tests** | End-to-end fallback cascades | Nightly |
| **Chaos tests** | Multi-failure scenarios | Weekly |
| **Simulation** | Historical replay | Nightly |

---

## 17. Circuit Breakers (External API Resilience)

### Configuration

| Service | Timeout | Error Threshold | Reset Timeout | Fallback |
|---------|---------|----------------|---------------|----------|
| **MapmyIndia** | 3s | 50% failures | 30s | Cached route from Redis, then OSRM |
| **Razorpay** | 5s | 40% failures | 60s | Switch to GPay/Paytm |
| **Twilio** | 2s | 60% failures | 15s | SendGrid email fallback |

### States

| State | Meaning | Behavior |
|-------|---------|----------|
| **Closed** | Normal | All requests pass through |
| **Open** | Too many failures | All requests fail, use fallback |
| **Half-Open** | Testing recovery | Allow 1 request to test |

### Metrics

- `circuit_breaker_open_total{service}` — counter
- `circuit_breaker_fallback_total{service}` — counter

---

## 18. SLOs & SLIs

| SLO | Target | Metric | Alert |
|-----|--------|--------|-------|
| **Assignment Latency** | p99 < 30s | `decision_eval_duration_seconds` | Alert if p99 > 30s for 5m |
| **ETA Accuracy** | p90 < 15min | `eta_error_seconds` | Alert if p90 > 15min |
| **API Uptime** | 99.9% | `/health` | Alert if < 99.9% over 30d |
| **Payment Success** | > 99.5% | `payment_success_rate` | Alert if < 99% |
| **Driver No-Show** | < 2% | `driver_no_show_total` | Alert if > 3%/hour |
| **Decision Engine** | p95 < 500ms | `decision_time_seconds` | Alert if p95 > 500ms |

---

## 19. Incident Runbooks

### Runbook 1: Payment Gateway Down (P1)

**Trigger:** Razorpay circuit breaker opens

**Actions:**
1. Activate GPay/Paytm fallback automatically
2. SMS customers with pending payments
3. Notify team via Slack

**Resolution:** Monitor Razorpay status → wait 5 min after recovery → gradual traffic ramp (10%→50%→100%) → reconcile failed transactions

### Runbook 2: No-Match Surge (P2)

**Trigger:** `ims_no_match_rate > 0.15`

**Actions:**
1. Check inventory by region
2. Dynamic pricing surge (+50% for 30 min)
3. Notify transport companies with incentive
4. Rebalance idle vehicles from nearby regions

### Runbook 3: DB Replication Lag > 5s (P2)

**Trigger:** `pg_replication_lag_seconds > 5`

**Actions:**
1. Pause non-critical writes
2. Scale up replica
3. Investigate cause

---

## 20. GLM-4.6 Autonomy Targets

### Metrics

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| AI Confidence | ~75% | > 92% | +22% |
| Self-Healing | ~60% | > 95% | +58% |
| Human Interventions | ~15/1000 | < 2/1000 | -87% |
| Decision Latency | 1.2s | < 0.5s | 2.4x faster |

### Implementation Phases

| Phase | Focus |
|-------|-------|
| **1 (Mo 1-3)** | Confidence calibration, ensemble verification |
| **2 (Mo 4-6)** | Root cause analysis, solution generation |
| **3 (Mo 7-9)** | Advanced exception handling, continuous learning |
| **4 (Mo 10-12)** | Full autonomy, predictive optimization |

### Data Requirements

| Category | Key Fields |
|----------|------------|
| Historical orders | Outcomes, timelines, routes, costs |
| Real-time telemetry | Vehicle location, speed, status |
| External data | Traffic, weather, fuel prices, demand |
| Performance metrics | On-time rate, ETA accuracy, satisfaction |
| Exception data | Types, resolutions, prevention measures |

---

## Cross-References

- `BI_Autonomous_OMS_Agent_Business_Logic.md`: customer tiers, vehicle assignment cascades, fallback logic, material-to-body mapping
- `BI_Order_Management_System_Lifecycle.md`: CODP, SOPs, order processing
- `BI_Pricing_Mechanism_Cost_Structure.md`: dynamic pricing, cost benchmarks, RDS surcharges
- `BI_Tech_Stack_ML_Systems.md`: LightGBM, OR-Tools, DRL4Route, feature store
- `BI_Vehicle_Models_Database.md`: vehicle specs, body types, dimensions
- `BI_Payment_Compliance_Guide.md`: Razorpay, GST (12% transport + 18% services), E-Way Bill
- `BI_EWay_Bill_Automation_Guide.md`: document automation
- `BI_Third_Party_Logistics_3PL.md`: transport-company fallback role

---

## Validation Checklist (Metrics vs Source Doc)

| Metric | Source | This Doc | Status |
|--------|--------|----------|--------|
| Driver acceptance window | PRD §4.1 | 10 min (600s) | ✅ |
| Reservation TTL | PRD §11 | 300s (5 min) | ✅ |
| Express multiplier | PRD §4.2 | +30% to +70% | ✅ |
| Loop discount | PRD §4.2 | 15-20% | ✅ |
| OTP verification time | PRD §4.1 | ≤ 2 seconds | ✅ |
| Idempotency window | PRD §11 | 24 hours | ✅ |
| DLQ threshold | PRD §2/B | depth >= 50 or rate >= 10/min | ✅ |
| Fraud score (settlement) | PRD YAML | < 0.015 | ✅ |
| Fraud score (advance) | PRD YAML | < 0.02 | ✅ |
| Driver blacklist trigger | PRD §C | 3x no-show / 30 days | ✅ |
| Admin override threshold | PRD §D | payout > ₹100K or fraud > 0.03 | ✅ |