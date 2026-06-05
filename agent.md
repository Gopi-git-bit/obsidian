# AGENTS.md — Zippy Logistics Coding Agent Directive

> **Purpose**: This file is the single source of truth for any AI coding agent working on the Zippy Logistics codebase. Read it fully before writing a single line of code. It provides project context, architectural understanding, planning methodology, execution rules, and hard boundaries that must never be crossed.

---

## Table of Contents

1. [Project Identity](#1-project-identity)
2. [Architecture Overview](#2-architecture-overview)
3. [Tech Stack Reference](#3-tech-stack-reference)
4. [Agent System](#4-agent-system)
5. [State Machine Reference](#5-state-machine-reference)
6. [Database Schema Reference](#6-database-schema-reference)
7. [API Surface Reference](#7-api-surface-reference)
8. [Policy Framework and Guardrails](#8-policy-framework-and-guardrails)
9. [Pricing Engine Reference](#9-pricing-engine-reference)
10. [Anti-Hallucination Rules for Coding Agents](#10-anti-hallucination-rules-for-coding-agents)
11. [Coding Standards and Patterns](#11-coding-standards-and-patterns)
12. [Critical Flows That Must Not Break](#12-critical-flows-that-must-not-break)
13. [Planning Methodology](#13-planning-methodology)
14. [Execution Workflow](#14-execution-workflow)
15. [Testing Requirements](#15-testing-requirements)
16. [Environment Rules](#16-environment-rules)
17. [Docker Runtime Rules](#17-docker-runtime-rules)
18. [Git Rules](#18-git-rules)
19. [What NOT to Build](#19-what-not-to-build)
20. [Required Response Format](#20-required-response-format)
21. [Repository Structure](#21-repository-structure)

---

## 1. Project Identity

**Name**: Zippy Logistics MVP
**Type**: Logistics SaaS platform for India (FTL truck booking, fleet management, settlement, compliance)
**Market**: India, starting with Tamil Nadu–Karnataka corridors
**Status**: Controlled internal pilot. NOT production-ready. NOT publicly launched.
**Operating Model**: Broker/agent model — Zippy earns commission + platform fee, does NOT recognize gross freight as revenue (Ind AS 115 compliance)

**Core Principle**:
> **Agents propose. Backend enforces. Audit records. Outbox announces.**

This principle is non-negotiable. No AI agent, frontend code, or test shortcut may bypass deterministic backend enforcement.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     6 Frontend Web Harnesses                    │
│  admin-web | customer-web | driver-web | transport-company-web │
│           supervisor-console | finance-console                  │
│         (Vanilla JS + auto-generated OpenAPI client)           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP (JWT Bearer)
┌────────────────────────────▼────────────────────────────────────┐
│                    FastAPI Backend (Python 3.11)                 │
│  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────────────┐  │
│  │   API    │ │ Services │ │  Agent    │ │   Middleware     │  │
│  │  Routes  │ │ (Logic)  │ │ Clients  │ │ (Auth, Privacy,  │  │
│  │          │ │          │ │ (HTTP)   │ │  Accounting)     │  │
│  └────┬─────┘ └────┬─────┘ └─────┬────┘ └──────────────────┘  │
│       │            │              │                              │
│  ┌────▼────────────▼──────────────▼──────────────────────────┐ │
│  │              SQLAlchemy ORM + Alembic Migrations           │ │
│  └────────────────────────┬──────────────────────────────────┘ │
└───────────────────────────┼────────────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────────────┐
│                    PostgreSQL 15 (Alpine)                       │
│  Orders | Vehicles | Bids | Matches | Trips | Settlements     │
│  Policy | Supervisor | Outbox | Audit | Auth                   │
└────────────────────────────────────────────────────────────────┘
```

**Key Architectural Decisions**:
- **FastAPI** over Django/Flask — native async, auto OpenAPI, Pydantic validation
- **PostgreSQL** over MongoDB — ACID compliance for financial transactions, strong JSON support
- **LightGBM** for pricing ML — fast, handles mixed data types, good for demand prediction
- **OR-Tools** for routing — industry-standard constraint programming
- **Agent model** (not carrier model) — Zippy is a platform, not a trucking company
- **Dual-layer enforcement** — contextual soft guardrails + deterministic hard boundaries

---

## 3. Tech Stack Reference

### Backend
| Component | Technology | Version |
|---|---|---|
| Runtime | Python | 3.11 |
| Framework | FastAPI | 0.109.0 |
| Server | Uvicorn | 0.27.0 |
| ORM | SQLAlchemy | 2.0.25 |
| Database | PostgreSQL | 15 (Alpine) |
| Migrations | Alembic | 1.13.1 |
| Validation | Pydantic | 2.5.3 |
| Auth | python-jose (JWT HS256) | 3.3.0 |
| Password | passlib (pbkdf2_sha256) | 1.7.4 |
| ML Pricing | LightGBM | 4.5.0 |
| ML Utils | scikit-learn | 1.5.1 |
| Route Optimization | OR-Tools | 9.10.4067 |
| Geo | geopy | 2.4.1 |
| HTTP Client | httpx | 0.26.0 |
| Testing | pytest | 7.4.4 |

### Frontend (All 6 Harnesses)
| Component | Technology |
|---|---|
| Type | Vanilla JS single-page apps (no framework) |
| Testing | Node.js built-in test runner |
| E2E | Playwright 1.56–1.60 |
| API Client | Auto-generated from OpenAPI spec |

### Infrastructure
| Component | Technology |
|---|---|
| Containerization | Docker |
| Orchestration | Docker Compose 3.8 |
| Database | PostgreSQL 15 Alpine |
| Cache | Redis 7 Alpine (optional, commented out) |

---

## 4. Agent System

### 4.1 Agent Types and Boundaries

The platform operates 8 specialized agents. Each agent has a strict action whitelist — no agent may perform actions outside its domain.

| Code | Name | Domain | Allowed Actions |
|---|---|---|---|
| **OMS** | Order Management | Order lifecycle, validation, cancellation | `order.transition`, `state.transition`, `order.submit`, `order.cancel`, `document.validate`, `workflow.trigger` |
| **TMS** | Transport Management | Route planning, ETA, milestones | `state.transition`, `route.plan`, `route.reroute`, `eta.update`, `shipment.milestone` |
| **IMS** | Inventory / Matching | Vehicle matching, ranking, capacity | `vehicle.match`, `vehicle.rank`, `capacity.recommend` |
| **FIN** | Finance | Settlements, payments, GST, journaling | `state.transition`, `settlement.release`, `settlement.check`, `payment.record`, `invoice.generate`, `journal.create`, `gst.invoice.create` |
| **SUP** | Supervisor | Exception handling, fraud holds, approvals | `policy.check`, `case.hold`, `case.approve`, `case.reject`, `fraud.hold`, `settlement.hold`, `settlement.hold.clear` |
| **DISPUTE** | Dispute Resolution | SLA scoring, refund recommendations | `dispute.score`, `refund.recommend`, `exception.raise` |
| **COMMS** | Communications | Notifications, alerts | `notification.draft`, `notification.trigger` |
| **ADMIN_OPS** | Admin Operations | Verification, audit, compliance, privacy | `state.transition`, `driver.verify`, `audit.query`, `privacy.mask`, `compliance.check` |

### 4.2 Agent Client Architecture

Agent clients live in `backend/app/agent_clients/` and communicate via HTTP to the backend API:

```
base.py          → TransitionClient (HTTP POST wrapper for /api/v1/orders/{id}/transition)
oms_client.py    → OrderManagementAgentClient
tms_client.py    → TransportManagementAgentClient
supervisor_client.py → SupervisorAgentClient
rma_client.py    → ResourceManagementAgentClient
```

**Pattern**: Agents call backend endpoints the same way external clients do. They never bypass the API layer or access the database directly. This ensures RBAC, policy preflight, and audit logging always apply.

### 4.3 Agent Telemetry Rules

**TMS Telemetry Detection** (`TransportManagementAgentClient.report_incident_from_telemetry`):
- Speed anomaly: vehicle speed > 95 km/h
- Prolonged stop: idle > 45 minutes
- Route deviation: > 10 km from planned route

**SUP Fraud Detection** (`SupervisorAgentClient.evaluate_policy_request`):
- Fraud score >= 0.75 → automatic hold
- Payment amount >= 500,000 INR → automatic hold for review

### 4.4 Actor Roles vs Agent Codes

The system uses two role systems. Understand the distinction:

| Actor Roles (auth/transition) | Agent Codes (policy) |
|---|---|
| `OMS`, `TMS`, `FIN`, `RAG`, `SUP`, `CUSTOMER`, `DRIVER`, `ADMIN` | `OMS`, `TMS`, `IMS`, `FIN`, `SUP`, `DISPUTE`, `COMMS`, `ADMIN_OPS` |

- **Actor roles** are used in RBAC checks, JWT tokens, and state transition permissions
- **Agent codes** are used in policy preflight checks and action validation
- They overlap but are NOT identical (e.g., `IMS` is an agent code but not an actor role; `CUSTOMER` and `DRIVER` are actor roles but not agent codes)

---

## 5. State Machine Reference

### 5.1 ORDER_STATE_GRAPH

This is the canonical order lifecycle. **Do NOT modify without explicit approval.**

```
CREATED ──→ {PAYMENT_PENDING, CONFIRMED, CANCELLED, SUSPENDED, INCIDENT}
PAYMENT_PENDING ──→ {CONFIRMED, CANCELLED, SUSPENDED, INCIDENT}
CONFIRMED ──→ {RINGING, CANCELLED, SUSPENDED, INCIDENT}
RINGING ──→ {ASSIGNED, CONFIRMED, CANCELLED, SUSPENDED, INCIDENT}
ASSIGNED ──→ {EN_ROUTE_TO_PICKUP, CANCELLED, SUSPENDED, INCIDENT}
EN_ROUTE_TO_PICKUP ──→ {AT_PICKUP_WAITING, CANCELLED, SUSPENDED, INCIDENT}
AT_PICKUP_WAITING ──→ {LOADING, CANCELLED, SUSPENDED, INCIDENT}
LOADING ──→ {DEPARTED_FOR_DELIVERY, CANCELLED, SUSPENDED, INCIDENT}
DEPARTED_FOR_DELIVERY ──→ {AT_DELIVERY_WAITING, CANCELLED, SUSPENDED, INCIDENT}
AT_DELIVERY_WAITING ──→ {DELIVERED_PENDING_SETTLEMENT, CANCELLED, SUSPENDED, INCIDENT}
DELIVERED_PENDING_SETTLEMENT ──→ {COMPLETED, SUSPENDED, INCIDENT}
COMPLETED ──→ {}  (terminal)
CANCELLED ──→ {}  (terminal)
SUSPENDED ──→ {}  (terminal)
INCIDENT ──→ {RINGING, ASSIGNED, CANCELLED, SUSPENDED}
```

**Terminal states**: COMPLETED, CANCELLED, SUSPENDED (no transitions out)

### 5.2 Role-State Transition Permissions

| Role | Allowed Target States |
|---|---|
| OMS | PAYMENT_PENDING, CONFIRMED, RINGING, CANCELLED, INCIDENT |
| TMS | RINGING, ASSIGNED, EN_ROUTE_TO_PICKUP, AT_PICKUP_WAITING, LOADING, DEPARTED_FOR_DELIVERY, AT_DELIVERY_WAITING, INCIDENT |
| FIN | PAYMENT_PENDING, CONFIRMED, COMPLETED, INCIDENT |
| SUP | RINGING, ASSIGNED, CANCELLED, SUSPENDED, INCIDENT |
| CUSTOMER | PAYMENT_PENDING, CANCELLED |
| DRIVER | ASSIGNED, EN_ROUTE_TO_PICKUP, AT_PICKUP_WAITING, LOADING, DEPARTED_FOR_DELIVERY, AT_DELIVERY_WAITING, DELIVERED_PENDING_SETTLEMENT, INCIDENT |
| ADMIN | ALL states |

### 5.3 State Machine Enforcement Rules

1. Every transition is validated against `ORDER_STATE_GRAPH` — invalid transitions are rejected with 422
2. Every transition is validated against `ROLE_STATE_PERMISSIONS` — wrong role is rejected with 403
3. Every transition requires `trace_id` and `idempotency_key`
4. Every transition is logged to `state_audit_logs` (append-only)
5. Failed transitions that cannot be processed go to `agent_dlq_messages` (dead-letter queue)

### 5.4 Golden Path (MVP Operating Spine)

```
Customer creates order (CREATED)
  → validated and priced (PAYMENT_PENDING / CONFIRMED)
  → vehicle/driver assigned (RINGING → ASSIGNED)
  → driver accepts and proceeds (EN_ROUTE_TO_PICKUP → AT_PICKUP_WAITING)
  → loading evidence uploaded (LOADING)
  → transit begins (DEPARTED_FOR_DELIVERY)
  → delivery reached (AT_DELIVERY_WAITING)
  → POD uploaded + OTP collected (DELIVERED_PENDING_SETTLEMENT)
  → POD verified + OTP verified by authorized role
  → supervisor clears exceptions if any
  → finance releases settlement (COMPLETED)
  → journal + GST invoice records created
  → audit + outbox records emitted
```

**This is the core of the MVP. Everything else is secondary. Do not break this flow.**

---

## 6. Database Schema Reference

### 6.1 Core Tables

**`user_accounts`** — Authentication and RBAC
- `id` (UUID PK), `username` (String 120, UNIQUE), `password_hash` (pbkdf2_sha256)
- `role` (Enum: customer, driver, transport_company, supervisor, support_admin, ops_admin, finance_admin, super_admin)
- `is_active` (Boolean, default True), `created_at`, `updated_at`

**`orders`** — The central entity
- `id` (UUID PK), `customer_id` (String 80, Indexed), `vehicle_id` (UUID FK)
- Shipper: `shipper_name`, `shipper_phone`, `shipper_email`
- Origin: `origin_city`, `origin_state`, `origin_pincode`, `origin_lat`, `origin_lng`
- Destination: `destination_city`, `destination_state`, `destination_pincode`, `destination_lat`, `destination_lng`
- Cargo: `cargo_type` (general/fragile/perishable/hazardous/oversized), `cargo_description`, `material_type`, `body_type_required`
- Payment: `payment_mode` (advance/full/topay), `topay_consent_status` (not_required/pending/accepted/rejected/timeout)
- Metrics: `weight_kg` (>0 constraint), `volume_cbm`, `num_packages`, `estimated_distance_km`, `estimated_duration_hours`
- Flags: `is_interstate`, `is_festival_period`, `is_remote_location`, `is_hill_area`
- Pricing: `offered_price`, `negotiated_price` (Numeric 12,2)
- **`current_state`** (Enum OrderStatus) — THE canonical lifecycle field
- `payload_metadata` (JSON), `notes` (Text), timestamps

**`state_audit_logs`** — Append-only transition log
- `log_id`, `order_id`, `from_state`, `to_state`, `event_name`, `actor_role`, `actor_id`
- `idempotency_key`, `trace_id`, `payload_hash`, `request_payload`, `cached_response`, `timestamp`

**`vehicle_reservations`** — Double-booking protection
- `reservation_id`, `vehicle_id`, `order_id`, `expires_at`, `is_active`
- Partial unique index on `(vehicle_id WHERE is_active=True)`

**`agent_dlq_messages`** — Dead-letter queue for failed transitions
- `message_id`, `order_id`, `event_name`, `actor_role`, `idempotency_key`, `trace_id`
- `error_code`, `error_detail`, `payload`, `retry_count`, `topic`

**`bids`** — Driver/transport company bidding
- `id`, `order_id`, `vehicle_id`, `driver_name`, `driver_phone`, `bid_amount`, `counter_amount`
- `estimated_eta_hours`, `estimated_arrival_hours`, `vehicle_available_at`, `notes`
- `status` (PENDING/ACCEPTED/REJECTED/COUNTERED/EXPIRED)

**`matches`** — Vehicle-order matching
- `id`, `order_id`, `vehicle_id`, `transport_company_id`, `bid_id`
- `match_score`, `utilization_percent`, `efficiency_score`
- `agreed_price`, `platform_fee`, `gst_amount`, `total_amount`
- `status` (PROPOSED/ACCEPTED/REJECTED/IN_PROGRESS/COMPLETED/CANCELLED), timestamps

**`vehicle_models`** — Pre-populated with 26 Indian commercial vehicles
- `id`, `manufacturer`, `model_name`, `transport_company_id`, `variant`
- `category` (LCV/ICV/HCV/Tipper/Tractor), `body_type` (open/closed/tipper/tanker/trailer)
- `gvw_kg`, `payload_kg`, `tonnage_class`, dimensions (mm), engine specs, `price_ex_showroom`, `is_active`

### 6.2 Flow Tables (Order → Settlement Pipeline)

**`quote_records`**: `quote_id`, `order_id`, `currency` (INR), `base_amount`, `platform_fee`, `gst_amount`, `total_amount`, `status`

**`trips`**: `trip_id`, `order_id` (unique), `vehicle_id`, `driver_id`, `transport_company_id`, `status`, `otp_verified`

**`payment_records`**: `payment_id`, `order_id`, `trip_id`, `payment_type`, `status`, `amount`, `currency`, `provider_ref`, `idempotency_key`

**`trip_documents`**: `document_id`, `order_id`, `trip_id`, `document_type`, `document_url`, `verification_status`, `payload`

**`trip_milestones`**: `milestone_id`, `order_id`, `trip_id`, `milestone_type`, `status`, `payload`, `idempotency_key`

**`settlement_records`**: `settlement_id`, `order_id`, `trip_id`, `status`, `amount`, `currency`, `idempotency_key`, `released_at`

**`journal_entries`**: `journal_entry_id`, `order_id`, `settlement_id`, `debit_ledger`, `credit_ledger`, `amount`, `currency`, `idempotency_key`

**`gst_invoice_records`**: `invoice_id`, `order_id`, `settlement_id`, `invoice_number` (unique), `taxable_amount`, `gst_amount`, `total_amount`, `status`

### 6.3 Policy Tables

**`policy_registry`**: `policy_id`, `policy_code` (unique), `policy_version`, `status`, `description`, `effective_at`

**`policy_decisions`**: `decision_id`, `agent_code`, `entity_type`, `entity_id`, `requested_action`, `decision_reason`, `trace_id`, `idempotency_key` (unique), `confidence_score`, `evidence_refs`, `payload`, `policy_version`, `result`, `reason_code`, `requires_human_review`

**`route_zone_policy`**: `id`, `route_zone` (unique), `min_gross_margin_pct`, `max_allowable_delay_mins`, `compliance_required`, `vehicle_supply_threshold_pct`, `crisis_margin_buffer_pct`, `policy_version`

**`compliance_document_rules`**: `id`, `shipment_type`, `route_type`, `document_name`, `mandatory`, `validation_endpoint`, `policy_version`

**`confidence_thresholds`**: `id`, `decision_category` (unique), `minimum_confidence`, `below_threshold_action`, `policy_version`

### 6.4 Supervisor Tables

**`exception_cases`**: `case_id`, `order_id`, `trip_id`, `settlement_id`, `case_type`, `status`, `severity`, `title`, `description`, `payload`, `created_by`

**`fraud_holds`**: `hold_id`, `case_id`, `order_id`, `reason`, `is_active`, `placed_by`, `released_by`, timestamps

**`settlement_holds`**: `hold_id`, `case_id`, `settlement_id`, `order_id`, `trip_id`, `reason`, `is_active`, `placed_by`, `released_by`, timestamps

**`supervisor_decisions`**: `decision_id`, `case_id`, `decision`, `notes`, `decided_by`, `payload`

### 6.5 Outbox Table

**`event_outbox`**: `id`, `event_id` (unique), `event_type`, `aggregate_type`, `aggregate_id`, `recipient_role`, `recipient_id`, `channel`, `payload`, `status`, `attempts`, `last_error`, `idempotency_key` (unique), `created_at`, `available_at`, `dispatched_at`

---

## 7. API Surface Reference

All endpoints are prefixed with `/api/v1`. Authentication is JWT Bearer token.

### 7.1 Auth
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/login` | Public | JWT login |
| POST | `/auth/dev-login` | Dev only | Dev JWT with role selection |

### 7.2 Orders
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/orders` | CUSTOMER_ORDER_ROLES | Create order |
| POST | `/orders/intake` | CUSTOMER_ORDER_ROLES | DPDP-consented intake |
| GET | `/orders` | ORDER_READ_ROLES | List with filters |
| GET | `/orders/stats/summary` | SUPPORT_READ_ROLES | Stats |
| GET | `/orders/{id}` | ORDER_READ_ROLES | Get order |
| PATCH | `/orders/{id}` | CUSTOMER_ORDER_ROLES | Update commercial fields |
| POST | `/orders/{id}/transition` | OPS_ADMIN_ROLES | State transition (policy preflight) |
| GET | `/orders/{id}/events` | SUPPORT_READ_ROLES | State audit log |
| POST | `/orders/{id}/cancel` | OPS_ADMIN_ROLES | Cancel order |

### 7.3 Vehicles
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/vehicles` | TRANSPORT_COMPANY_ROLES | Create vehicle |
| GET | `/vehicles` | SUPPORT_READ + TRANSPORT_COMPANY | List with filters |
| GET | `/vehicles/{id}` | Same | Get vehicle |
| PATCH | `/vehicles/{id}` | TRANSPORT_COMPANY_ROLES | Update vehicle |
| GET | `/vehicles/recommend` | Same | Vehicle recommendation |
| GET | `/manufacturers` | Same | List manufacturers |
| GET | `/categories` | Same | List categories |

### 7.4 Pricing
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/pricing/estimate` | CUSTOMER + SUPPORT + TRANSPORT | Simple estimate |
| GET | `/pricing/rates` | Same | Current rates |
| POST | `/pricing/ml-estimate` | Same | ML-enhanced full breakdown |
| POST | `/pricing/surge-predict` | Same | Surge prediction |
| GET | `/pricing/rate-card` | Same | Full rate card |
| POST | `/pricing/compare` | Same | Zippy vs broker comparison |

### 7.5 Matching and Bidding
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/orders/{id}/match` | TRANSPORT_COMPANY | Find matching vehicles |
| POST | `/matches/{id}/accept` | TRANSPORT_COMPANY | Accept match |
| POST | `/matches/{id}/reject` | TRANSPORT_COMPANY | Reject match |
| POST | `/orders/{id}/bids` | DRIVER + TRANSPORT | Place bid |
| GET | `/orders/{id}/bids` | ALL READ ROLES | List bids |
| POST | `/bids/{id}/accept` | CUSTOMER | Accept bid |
| POST | `/bids/{id}/reject` | CUSTOMER + DRIVER + TRANSPORT | Reject bid |
| POST | `/bids/{id}/counter` | Same | Counter-offer |

### 7.6 Policy
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/policy/check` | SUPERVISOR + FINANCE + OPS + SUPER_ADMIN | Deterministic policy check |

### 7.7 Route Optimization
| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/optimize/route` | DRIVER + SUPPORT + TRANSPORT | OR-Tools VRPTW solver |
| GET | `/optimize/distance` | Same | Haversine + road distance |
| GET | `/optimize/gst-zone` | Same | GST zone classification |
| POST | `/optimize/multi-stop` | Same | Multi-stop route |

### 7.8 Order Flow (Quote → Settlement)
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/orders/{id}/flow-summary` | SUPPORT_READ | Full flow summary |
| GET | `/orders/{id}/customer-flow-summary` | CUSTOMER | Customer-visible flow |
| POST | `/orders/{id}/quote` | OPS_ADMIN | Create quote |
| POST | `/orders/{id}/payments/advance` | FINANCE_ADMIN | Record advance payment |
| POST | `/trips/{id}/assign-driver` | OPS_ADMIN | Assign driver |
| POST | `/driver/trips/{id}/acknowledge` | DRIVER | Acknowledge trip |
| POST | `/trips/{id}/loading-photo` | DRIVER | Upload loading photo |
| POST | `/trips/{id}/milestones` | DRIVER | Update milestone |
| POST | `/trips/{id}/pod` | DRIVER | Upload POD (→ DELIVERED_PENDING_SETTLEMENT) |
| POST | `/trips/{id}/pod/verify` | VERIFICATION_ROLES | Verify POD |
| POST | `/trips/{id}/otp/verify` | VERIFICATION_ROLES | Verify OTP |
| POST | `/trips/{id}/settlements/release` | FINANCE_ADMIN | Release settlement |

### 7.9 Finance and Revenue
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/finance/settlements` | FINANCE_ADMIN | Settlement queue |
| GET | `/finance/settlements/{trip_id}` | FINANCE_ADMIN | Settlement detail |
| POST | `/revenue/recognize` | FINANCE_ADMIN | ASC 606 revenue recognition |

### 7.10 Supervisor
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/supervisor/cases` | SUPPORT + SUPERVISOR | List cases |
| GET | `/supervisor/cases/{id}` | Same | Case detail |
| POST | `/supervisor/cases/{id}/hold` | SUPERVISOR | Hold case |
| POST | `/supervisor/cases/{id}/approve` | SUPERVISOR | Approve (releases holds) |
| POST | `/supervisor/cases/{id}/reject` | SUPERVISOR | Reject case |
| POST | `/supervisor/orders/{id}/fraud-hold` | SUPERVISOR | Place fraud hold |
| POST | `/supervisor/settlements/{id}/hold` | SUPERVISOR | Place settlement hold |
| POST | `/supervisor/trips/{id}/settlement-hold` | SUPERVISOR | Place trip settlement hold |
| POST | `/supervisor/settlements/{id}/release-hold` | SUPERVISOR | Release settlement hold |

### 7.11 Outbox
| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/outbox/events` | SUPERVISOR + FINANCE + SUPER_ADMIN | List events |
| POST | `/outbox/events/{id}/mark-dispatched` | SUPER_ADMIN | Mark dispatched |
| POST | `/outbox/events/{id}/mark-failed` | SUPER_ADMIN | Mark failed |

### 7.12 Health
| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |

### 7.13 RBAC Role Sets (Reference)

```
ADMIN_ROLES          = {supervisor, support_admin, ops_admin, finance_admin, super_admin}
SUPERVISOR_ROLES     = {supervisor, super_admin}
OPS_ADMIN_ROLES      = {ops_admin, super_admin}
FINANCE_ADMIN_ROLES  = {finance_admin, super_admin}
CUSTOMER_ORDER_ROLES = customer + all admin roles
DRIVER_TRIP_ROLES    = driver + all admin roles
TRANSPORT_COMPANY_ROLES = transport_company + all admin roles
```

**Resource Ownership**:
- Customers → own orders only (`customer_id` filter)
- Drivers → own trips only (`driver_id` filter)
- Transport companies → own vehicles/trips only (`transport_company_id` filter)

---

## 8. Policy Framework and Guardrails

### 8.1 Policy Kernel (`policy_service.py`)

The policy kernel enforces a sequential validation chain for every high-risk action:

```
1. validate_idempotency_trace()  → requires trace_id + idempotency_key
2. validate_agent_role()          → checks agent code has requested action
3. validate_state_transition()    → verifies transition in ORDER_STATE_GRAPH
4. validate_route_margin_floor()  → RouteZonePolicy margin check with crisis buffer
5. validate_required_documents()  → ComplianceDocumentRule check
6. validate_confidence_threshold() → ConfidenceThreshold check, holds if below
```

Any failure in this chain results in a `PolicyDecision` record with the reason code and may trigger a hold.

### 8.2 Confidence Thresholds

| Decision Category | Minimum Confidence | Below-Threshold Action |
|---|---|---|
| Financial | 0.85 | Hold for human review |
| Compliance | 0.95 | Block + hold for supervisor |
| Operational | 0.75 | Warn + allow with flag |
| Communication | 0.70 | Allow with disclaimer |

### 8.3 Route Zone Policy

Each route zone has a defined margin floor:
- `min_gross_margin_pct` — minimum acceptable gross margin
- `max_allowable_delay_mins` — maximum delay tolerance
- `compliance_required` — whether compliance documents are mandatory
- `vehicle_supply_threshold_pct` — supply threshold below which crisis rules apply
- `crisis_margin_buffer_pct` — margin relaxation during supply crisis

**Margin Protection Logic**:
- If `proposed_margin_pct < min_gross_margin_pct` → `ROUTE_MARGIN_FLOOR_VIOLATION` rejection
- If `vehicle_supply_pct < vehicle_supply_threshold_pct` → margin floor relaxed by `crisis_margin_buffer_pct`

### 8.4 Accounting Controls (`accounting_controls.py`)

**Segregation of Duties**: Invoice generation and approval must be performed by different users. The `SegregationOfDutiesValidator` enforces this.

**Agent Model Revenue Guard**: Under the agent (broker) model, Zippy revenue cannot exceed `commission + platform_fee`. The `validate_no_gross_revenue_under_agent_model` function prevents gross freight from being recognized as Zippy revenue (Ind AS 115 compliance).

### 8.5 Privacy Controls (`privacy.py`)

**DPDP Privacy Masking Middleware**: Automatically masks phone numbers in JSON responses:
- Masks: `phone`, `mobile`, `contact_number`, `shipper_phone`, `driver_phone`, `consignee_phone`
- Preserves last 4 digits (e.g., `******7890`)
- Bypass: `x-zippy-pii-access: full` header required

### 8.6 Business Rules (in `order_service.py`)

- ToPay orders require `topay_consent_status = accepted` before CONFIRMED
- Pharma material requires closed body vehicle before CONFIRMED
- `driver_response ACCEPT` must target ASSIGNED state
- `driver_response REJECT/TIMEOUT` cannot assign order
- `shipment_doc_scanned` requires `doc_type`, `doc_url`, `scan_exif` + target LOADING
- `pod_scanned` requires `pod_url`, `consignee_otp`, `pod_exif` + target DELIVERED_PENDING_SETTLEMENT

### 8.7 Settlement Release Guard

Settlement release (`POST /trips/{id}/settlements/release`) requires ALL of:
1. Order exists
2. Trip exists
3. POD is verified
4. OTP is verified
5. No active fraud hold exists
6. No active settlement hold exists
7. Actor role is `finance_admin` or `super_admin`
8. Policy preflight approves (FIN agent code + `settlement.release` action)

On success:
- Creates `SettlementRecord` + `JournalEntry` + `GSTInvoiceRecord`
- Emits outbox events: `settlement.released`, `finance.journal_created`, `finance.gst_invoice_created`
- Transitions order to COMPLETED

On block:
- Emits outbox event: `settlement.release_blocked`
- Does NOT create any financial records

---

## 9. Pricing Engine Reference

### 9.1 Pricing Pipeline (`DynamicPricingEngine.calculate_price`)

The pricing pipeline applies adjustments in this exact order. Do not reorder or skip steps:

1. **Base cost** = `distance_km * RATE_PER_KM`
   - LCV: ₹12/km | ICV: ₹15/km | HCV: ₹18/km | Tipper: ₹20/km | Tractor: ₹16/km | Trailer: ₹22/km
2. **City tier multiplier** — Metro: 0.95 | Tier-2: 1.0 | Other: 1.15
3. **Fuel index** — diesel >₹95: 1.05+ | diesel <₹85: 0.98
4. **Route difficulty surcharge** — 0–20: 0% | 20–40: 5% | 40–60: 10% | 60–80: 15% | 80–100: 25%
5. **Urbanization density** — Metro: 1.08 | Tier-2: 1.00 | Smaller: 1.07
6. **Scenario surcharges** — festival: 30% | remote: 35% | hill: 45% | congestion: 15%
7. **Surge multiplier** — LightGBM model (1.0–3.0) or rule-based fallback
8. **Service type** — standard: 1.0 | express: 1.5 | priority: 1.8
9. **Deadhead/lane viability** — highly_balanced: 0% | moderately_balanced: 6% | unbalanced: 12% | seasonal: 10% | remote_low_demand: 18%
10. **Platform fee** — >200km: 4% | ≤200km: 5%
11. **Customer adjustment** — high_value: -10% | low_value: +5%
12. **GST** — Transport: 12% + Services: 18%

### 9.2 ML Pricing (`SurgePredictor`)

- Model: LightGBM with 17 features
- Feature engineering via `FeatureEngineer` class
- Falls back to rule-based if model unavailable
- Surge range: 1.0–3.0
- Training script: `backend/ml/train_pricing_model.py`

### 9.3 Rate Comparison

The `/pricing/compare` endpoint provides Zippy vs traditional broker comparison:
- Zippy platform fee: 3–5%
- Traditional broker fee: 8–12%

---

## 10. Anti-Hallucination Rules for Coding Agents

These rules prevent coding agents from generating incorrect code, inventing APIs, or making unsafe assumptions.

### 10.1 Never Invent

- **Do not invent API endpoints** that do not exist in the codebase. Check `backend/app/api/` files before assuming an endpoint exists.
- **Do not invent database fields** that are not in the SQLAlchemy models. Check `backend/app/models/` before assuming a field exists.
- **Do not invent state transitions** that are not in `ORDER_STATE_GRAPH`. Check `backend/app/services/order_service.py`.
- **Do not invent agent actions** that are not in `AGENT_ALLOWED_ACTIONS`. Check `backend/app/services/policy_service.py`.
- **Do not invent role permissions** that are not in `ROLE_STATE_PERMISSIONS`.
- **Do not invent RBAC role sets** that are not defined in `backend/app/auth.py`.
- **Do not invent environment variables** that are not in `.env.example`.

### 10.2 Always Verify Before Claiming

Before stating "this endpoint does X" or "this model has field Y", verify against the actual codebase. If you cannot verify, say "not verified" instead of assuming.

### 10.3 Use Precise Labels

| Label | Meaning |
|---|---|
| Implemented | Confirmed in code, tests pass |
| Partial | Code exists but incomplete or untested |
| Simulated | Stub/mock, not real integration |
| Documented only | Spec/design exists, no code |
| Not found | No code or spec found |
| Not verified | Code exists but not tested in this session |

### 10.4 Forbidden Phrases

Never use these in your responses:
- "probably works"
- "should be fine"
- "production ready"
- "fully complete"
- "I assume"
- "typically this would"
- "in most systems"

### 10.5 When Uncertain, Read the Code

If you are unsure about any behavior, read the relevant source file before making changes. The source code is the ultimate authority, not documentation or assumptions.

### 10.6 Do Not Speculatively Add Features

Do not add features, endpoints, models, or integrations that were not explicitly requested. If you see a gap, report it but do not fill it without approval.

---

## 11. Coding Standards and Patterns

### 11.1 Framework Rules

- Follow the existing FastAPI + SQLAlchemy + Alembic stack. Do not migrate or add alternative frameworks.
- Do not convert the backend to another language or stack.
- Do not add a second backend architecture.

### 11.2 Migration Rules

Every persistent schema change must include:
1. Alembic migration file in `backend/alembic/versions/`
2. SQLAlchemy model update in `backend/app/models/`
3. Migration parity test where relevant
4. PostgreSQL compatibility check

**PostgreSQL Enum Rules**:
- Do not blindly recreate existing enum types
- Use idempotent enum creation patterns
- Use `create_type=False` where the enum already exists
- Never drop live enum/data casually
- Keep revision IDs within safe length (the project widened `alembic_version.version_num` for long IDs)

### 11.3 Idempotency Pattern

For all state-changing actions:
- Require or preserve `idempotency_key`
- Duplicate requests must NOT double-create settlements, journal records, GST records, outbox events, or policy decisions
- Same key with different payload should be handled safely per existing project pattern

### 11.4 Traceability Pattern

High-risk requests must include:
- `trace_id`
- `idempotency_key`
- `decision_reason`
- `confidence_score`
- `evidence_refs` where applicable

### 11.5 Error Response Pattern

- Return consistent JSON errors
- Include request ID / correlation ID where existing middleware supports it
- Do not expose stack traces in pilot/production mode
- Use appropriate HTTP status codes (422 for validation, 403 for RBAC, 404 for not found)

### 11.6 Event Outbox Pattern

All significant state changes should emit outbox events via `emit_outbox_event()`:
- Events are idempotent (duplicate `idempotency_key` does not create duplicates)
- Events include `event_type`, `aggregate_type`, `aggregate_id`, `recipient_role`, `channel`, `payload`
- Outbox events are processed separately from the main transaction

### 11.7 Naming Conventions

- API routes: `snake_case` for paths, `camelCase` for JSON fields in schemas
- Database: `snake_case` for tables and columns
- Python: `snake_case` for functions and variables, `PascalCase` for classes
- Enums: `UPPER_SNAKE_CASE` for values

---

## 12. Critical Flows That Must Not Break

### 12.1 Order Lifecycle

**Files**: `backend/app/api/orders.py`, `backend/app/api/flow.py`, `backend/app/schemas/order.py`, `backend/app/services/order_service.py`

Do not break:
- Order creation
- Order transition endpoint
- State-machine validation
- Policy preflight on order transition
- Invalid transition rejection
- Trace/idempotency metadata handling
- Admin/customer/driver harness flows

### 12.2 Settlement Release

**Files**: `backend/app/api/flow.py`, `backend/app/api/finance.py`, `backend/tests/test_settlement_release.py`

Do not break:
- POD + OTP verification requirement
- Fraud hold blocking
- Settlement hold blocking
- Finance admin role requirement
- Policy preflight requirement
- Idempotent record creation
- Outbox event emission on both success and block

### 12.3 Supervisor Holds

**Files**: `backend/app/api/supervisor.py`, `backend/app/models/supervisor_model.py`, `backend/tests/test_supervisor.py`

Do not break:
- Exception case listing/detail
- Fraud hold creation
- Settlement hold creation and release
- Supervisor decision audit
- Wrong-role blocking
- Driver POD/OTP verification blocking

### 12.4 Policy Kernel

**Files**: `backend/app/api/policy.py`, `backend/app/models/policy_model.py`, `backend/app/services/policy_service.py`, `backend/tests/test_policy_kernel.py`

Do not break:
- `POST /api/v1/policy/check`
- All policy tables and their constraints
- Sequential validation chain
- Hold/reject decision creation
- Policy outbox events
- Duplicate idempotency handling

### 12.5 Event Outbox

**Files**: `backend/app/api/outbox.py`, `backend/app/models/outbox_model.py`, `backend/app/services/outbox_service.py`

Do not break:
- Event creation with idempotency
- Event read/mark endpoints
- Policy hold/reject outbox events
- Settlement release/block events

### 12.6 Auth and Environment Safety

**Files**: `backend/app/config.py`, `backend/app/api/auth.py`, `backend/tests/test_api.py`

Do not break:
- Dev-login blocked outside development mode
- JWT validation on all protected routes
- RBAC role set enforcement
- Resource ownership filtering

---

## 13. Planning Methodology

Before writing any code, follow this planning process:

### Step 1: Understand the Request

- What is the exact requirement? Re-read the task.
- Which agent domain does it fall under? (OMS, TMS, FIN, SUP, etc.)
- Does it affect any critical flow listed in Section 12?
- Does it require a database migration?
- Does it require new policy rules?

### Step 2: Locate Relevant Code

- Find the relevant API route in `backend/app/api/`
- Find the relevant service in `backend/app/services/`
- Find the relevant model in `backend/app/models/`
- Find the relevant schema in `backend/app/schemas/`
- Find existing tests in `backend/tests/`

### Step 3: Assess Impact

- Will this change affect the order state machine?
- Will this change affect pricing calculations?
- Will this change affect settlement release?
- Will this change affect policy validation?
- Will this change require frontend updates across multiple harnesses?
- Will this break existing tests?

### Step 4: Plan the Smallest Change

- Make the minimum change that satisfies the requirement
- Do not refactor unrelated code
- Do not add features not requested
- Do not change patterns that are working

### Step 5: Plan Tests

- What tests need to be added?
- What existing tests might break?
- How will you verify the change works?

---

## 14. Execution Workflow

For any coding task, follow this exact sequence:

```
1. Read current status (git status, recent commits)
2. Inspect relevant files (models, services, routes, schemas, tests)
3. Make the smallest change that satisfies the task
4. Add or update tests for the change
5. Run targeted tests for the changed area
6. Run full backend test suite
7. Run affected frontend smoke/E2E tests
8. Run all smoke/E2E if the change is cross-cutting
9. Verify Docker only if runtime/deployment changed
10. Report exact results (see Section 20)
11. Commit only when requested or when task explicitly includes commit
```

---

## 15. Testing Requirements

### 15.1 Verified Baseline

The current passing baseline is:
- Backend tests: 90 passed
- Admin smoke: 3 passed
- Customer smoke: 3 passed
- Driver smoke: 3 passed
- Transport company smoke: 3 passed
- Supervisor smoke: 3 passed
- Finance smoke: 5 passed
- Admin E2E: 1 passed
- Customer E2E: 1 passed
- Driver E2E: 1 passed
- Transport company E2E: 1 passed
- Supervisor E2E: 1 passed
- Finance E2E: 1 passed

**If your change reduces this baseline, stop and report the regression.**

### 15.2 Test Commands

**Backend** (from `backend/` or project root):
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Frontend Smoke** (in each frontend folder):
```powershell
npm.cmd test
```

**Frontend E2E** (in each frontend folder):
```powershell
npm.cmd run test:e2e
```

Use `npm.cmd` (not `npm`) on Windows PowerShell.

### 15.3 Test Categories

| Test File | What It Tests |
|---|---|
| `test_orders.py` | Order CRUD, state transitions, validation |
| `test_api.py` | Auth, RBAC, dev-login blocking |
| `test_policy_kernel.py` | Policy validation chain, confidence thresholds |
| `test_rbac.py` | Role-based access control |
| `test_supervisor.py` | Supervisor holds, fraud holds, decisions |
| `test_migration_parity.py` | Migration model consistency |
| `test_alignment_endpoints.py` | Endpoint alignment |
| `test_settlement_release.py` | Settlement release guards |
| `test_order_to_settlement_flow.py` | End-to-end order → settlement |

### 15.4 E2E Test Environment

E2E tests spawn a backend with:
- `APP_ENV=development`
- `CORS_ORIGINS=*` or test-compatible equivalent

This prevents pilot runtime settings from breaking local E2E tests.

---

## 16. Environment Rules

| Environment | Dev-Login | Data | CORS | Secrets | External Ops |
|---|---|---|---|---|---|
| `development` | Allowed | Local test data | Open | `.env` file | Simulated |
| `pilot` | Blocked | Controlled users only | Restricted | Strong JWT secret | Manual |
| `production` | Blocked | Full auth/provisioning | TLS + strict | Secrets manager | Real integrations |

**Key Environment Variables** (from `.env.example`):
```
DATABASE_URL=postgresql://logimatch:CHANGE_ME@localhost:5432/logimatch
POSTGRES_DB=zippy
APP_ENV=development|pilot|production
BACKEND_PORT=8000
JWT_SECRET=change_me
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

**Do not** hardcode secrets. **Do not** commit `.env` files with credentials.

---

## 17. Docker Runtime Rules

**Startup sequence**:
```
alembic upgrade head → uvicorn app.main:app
```
If migration fails, container should exit. Do not serve app with stale schema.

**Health checks**:
```
GET /health  → returns 200 if app is running
GET /ready   → returns 200 if app + DB are connected
```

**Port collision warning**: Docker backend and Playwright E2E both default to port 8000. Stop Docker before E2E, or configure different ports.

**Docker commands**:
```powershell
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml up -d --build
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml ps
docker compose --env-file backend/.env.example -f docker-compose.runtime.yml down
```
Use `down -v` only when intentionally deleting local Postgres volume.

---

## 18. Git Rules

### Before Changing Code
```powershell
git status --short
git log --oneline --decorate -10
```

### Commit Messages
Be specific:
```
mvp: harden pilot runtime environment
mvp: wire policy preflight into settlement release
mvp: add confidence threshold validation to policy kernel
chore: ignore playwright test artifacts
```

Do not mix unrelated tasks in one commit.

### Do Not Commit
- Real secrets
- `.env` with credentials
- Playwright `test-results/` or `playwright-report/`
- Local DB files
- Generated temporary artifacts

---

## 19. What NOT to Build

Do not implement these unless explicitly requested:

| Category | Items |
|---|---|
| Payment | Real Razorpay/payment gateway |
| Communications | Real WhatsApp/SMS/email provider |
| Compliance | Real GST/NIC/e-way filing |
| Verification | Real ULIP/VAHAN integration |
| Documents | Real OCR vendor integration |
| AI | Full RAG/contextual policy injection, full autonomous agent execution |
| Infrastructure | Kubernetes, complex observability stack |
| Frontend | Full production mobile apps, large UI redesign, new frameworks |
| Business | Multi-tenant billing, public launch setup |

These are post-pilot or controlled integration tasks. Building them prematurely introduces risk.

---

## 20. Required Response Format

After every task, return this 12-point checklist:

```
1. What was already working
2. What was added
3. Files changed
4. Backend endpoints added/changed
5. Database/migration changes
6. Frontend changes
7. Tests added/updated
8. Commands run
9. Test results
10. Docker/runtime verification result (or "not relevant")
11. Remaining gaps
12. Recommended next task
```

**Rules**:
- Be factual
- Do not claim completion unless tests pass
- If a command was not run, say so
- If Docker was not available, say so
- If only compose config was verified but runtime was not started, say so

---

## 21. Repository Structure

```
obsidian/
├── backend/
│   ├── app/
│   │   ├── api/               # Route handlers
│   │   │   ├── auth.py        # JWT login, dev-login
│   │   │   ├── orders.py      # Order CRUD + transitions
│   │   │   ├── vehicles.py    # Vehicle CRUD + recommend
│   │   │   ├── pricing.py     # Pricing estimates + rates
│   │   │   ├── ml_pricing.py  # ML pricing + surge
│   │   │   ├── matches.py     # Vehicle matching
│   │   │   ├── bids.py        # Bidding system
│   │   │   ├── policy.py      # Policy check endpoint
│   │   │   ├── routing.py     # Route optimization
│   │   │   ├── shipments.py   # Shipment tracking
│   │   │   ├── flow.py        # Order-to-settlement flow
│   │   │   ├── finance.py     # Settlement queue
│   │   │   ├── revenue.py     # Revenue recognition
│   │   │   ├── outbox.py      # Event outbox
│   │   │   ├── supervisor.py  # Supervisor operations
│   │   │   └── health.py      # Health/readiness
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── auth_model.py
│   │   │   ├── order_model.py
│   │   │   ├── vehicle_model.py
│   │   │   ├── flow_model.py
│   │   │   ├── policy_model.py
│   │   │   ├── supervisor_model.py
│   │   │   └── outbox_model.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── order.py
│   │   │   ├── vehicle.py
│   │   │   ├── logistics.py
│   │   │   └── revenue.py
│   │   ├── services/          # Business logic
│   │   │   ├── order_service.py    # State machine + transitions
│   │   │   ├── pricing_service.py  # Dynamic pricing engine
│   │   │   ├── policy_service.py   # Policy kernel
│   │   │   ├── revenue_service.py  # Revenue recognition
│   │   │   ├── outbox_service.py   # Event outbox
│   │   │   └── route_optimizer.py  # OR-Tools routing
│   │   ├── agent_clients/     # Agent HTTP clients
│   │   │   ├── base.py
│   │   │   ├── oms_client.py
│   │   │   ├── tms_client.py
│   │   │   ├── supervisor_client.py
│   │   │   └── rma_client.py
│   │   ├── middleware/        # Cross-cutting concerns
│   │   │   ├── accounting_controls.py
│   │   │   └── privacy.py
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Environment config
│   │   ├── auth.py            # JWT + RBAC dependencies
│   │   ├── observability.py   # Request ID, logging, Sentry
│   │   └── database/          # SQLAlchemy engine, session, Base
│   ├── alembic/
│   │   └── versions/          # 10 migrations (001–010)
│   ├── ml/
│   │   └── train_pricing_model.py
│   ├── scripts/               # Backtest scripts
│   ├── tests/                 # Test suite (90+ tests)
│   ├── Dockerfile
│   └── requirements.txt
├── admin-web/                 # Admin dashboard harness
├── customer-web/              # Customer booking + tracking
├── driver-web/                # Driver trip management + POD
├── transport-company-web/     # Transport company fleet + orders
├── supervisor-console/        # Supervisor exception handling
├── finance-console/           # Finance settlement queue
├── docker-compose.yml
├── .env.example
├── AGENTS.md                  # ← This file
├── PROJECT.md
├── DECISIONS.md
├── KNOWLEDGE.md
├── ROADMAP.md
└── .obsidian/                 # Obsidian vault (knowledge base)
```

**Do not move folders unless explicitly requested. Do not rename APIs unless tests and frontend clients are updated.**

---

## Quick Reference Card

When in doubt, follow these rules in order of priority:

1. **Safety first** — Never weaken settlement release, policy enforcement, or RBAC
2. **Read the code** — The source code is the ultimate authority
3. **Smallest change** — Make the minimum change that satisfies the requirement
4. **Test everything** — If it is not tested, it is broken
5. **Idempotency** — Every state-changing action must be idempotent
6. **Audit trail** — Every significant action must be auditable
7. **Policy preflight** — High-risk actions must go through the policy kernel
8. **Outbox pattern** — Announce state changes, do not rely on synchronous side effects
9. **Do not invent** — If you cannot verify it exists, do not assume it does
10. **Report honestly** — Use precise labels, never claim what you did not verify

---

*This AGENTS.md is the directive for all coding agents working on the Zippy Logistics platform. Read it, follow it, and when uncertain, re-read it.*
