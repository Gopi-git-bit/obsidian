---
type: hub
domain: technology
scope: technical
status: active
last_updated: 2026-04-16
related_hubs:
  - AI Agents Hub
  - Operations Strategy Hub
---

# Technology Stack Hub

Central hub for technology architecture, integrations, and digital infrastructure.

## Core Systems

### Order Management
- [[Order Management System]]
- [[OMS Integration APIs]]
- [[Order Lifecycle Automation]]

### Transportation Management
- [[Transportation Management System (TMS)]]
- [[Route Optimization Engine]]
- [[Fleet Tracking System]]
- [[ETA Prediction Logic]]
- [[TMS Execution Architecture]]
- Valhalla for truck-aware runtime routing
- OR-Tools for VRP, PDP, and backhaul sequencing

### Warehouse Management
- [[Warehouse Management System]]
- [[Inventory Tracking]]
- [[Pick-pack-ship Logic]]

## Integration Architecture

- [[API Integration Standards]]
- [[Hybrid Logistics Data Architecture]]
- [[Authoritative Database Schema]]
- [[Supabase Integration]]
- [[Third-party API Connectors]]
- [[Data Synchronization Patterns]]
- [[Operational Observability Architecture]]

## AI & Automation

- [[AI Agent Infrastructure]]
- [[Machine Learning Models]]
- [[Hyperparameter Tuning System]]
- [[Natural Language Processing]]
- [[Predictive Analytics]]
- Celery-driven replay, retraining, and recovery jobs
- LightGBM for ETA residual prediction and tabular routing forecasts
- Optuna and Ray Tune for controlled model search and tuning workflows

## Frontend & Mobile

- [[Web Application Architecture]]
- [[Mobile App for Drivers]]
- [[Customer Portal]]
- [[Customer App Frontend Architecture]]
- [[Driver App Frontend Architecture]]

## Data & Analytics

- [[Data Pipeline Architecture]]
- [[Analytics Dashboard]]
- [[Real-time Reporting]]
- GraphQL gateway for unified pricing and routing responses
- Specialized storage split for transactional and graph-native workloads
- Prometheus and Grafana for fallback, anomaly, and SLA monitoring

## Key Technologies

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js | Customer/admin UI |
| Backend | Node.js/Python | Business logic |
| Database | Supabase/PostgreSQL | Data storage |
| AI | Claude API | Agent intelligence |
| Maps | Mapbox/Google Maps | Route visualization |
| ML | LightGBM + joblib | ETA prediction and fast online inference |

## Data Model Pattern

| Concern | Recommended Pattern | Constraint |
|---------|---------------------|------------|
| Lifecycle truth | Event log plus projection | Do not treat projection as sole history |
| Spatial operations | PostGIS geometry with GIST indexes | Required for corridor and radius queries |
| Telemetry scale | Partition or manage high-volume pings carefully | Avoid unbounded hot-table growth |
| AI control | Decision audit and feature flags | Autonomy must remain reviewable |
| Finance | Separate payments, settlements, invoices, ledger | Preserve deterministic audit trails |

## Frontend Reliability Pattern

| Concern | Recommended Pattern | Constraint |
|---------|---------------------|------------|
| Order writes | Transition API with idempotency key | No direct state mutation |
| Realtime updates | WebSocket with polling fallback | UI must tolerate channel failure |
| Weak connectivity | Local draft queue and reconnect sync | Sync must remain replay-safe |
| Sensitive flows | Feature flags and progressive rollout | Avoid full-population risk on first release |
| Compliance | UI audit logging | Strip PII before analytics forwarding |

## Driver-Field Reliability Pattern

| Concern | Recommended Pattern | Constraint |
|---------|---------------------|------------|
| Assignment response | Dedicated response API with idempotency key | Driver app must not mutate assignment state directly |
| POD and document capture | EXIF, GPS, timestamp, and OTP validation | Evidence quality beats speed |
| Offline field actions | Persist response intent and sync later | Do not fabricate acknowledgement locally |
| Multi-vehicle access | Role-aware authorization | Distinguish owner control from salaried-driver scope |

## Emerging Stack Pattern

| Layer | Candidate Tech | Role in Pricing |
|-------|----------------|-----------------|
| Transactional data | SQLite or PostgreSQL | Quotes, fees, configs, audit trails |
| Relationship intelligence | Neo4j | Backhaul, familiarity, route topology |
| API orchestration | GraphQL | Unified quote and route response |
| Precision math | Decimal arithmetic | Financial correctness under load |

## Routing Architecture Pattern

| Component | Suggested Role | Constraint |
|-----------|----------------|------------|
| Valhalla | Truck routing and live-cost matrix | Suggestion engine only |
| OSRM or static routing | Fallback matrix layer | Use only when primary path degrades |
| OR-Tools | Sequence and pairing optimization | Must respect pre-filtered feasibility |
| PostGIS | Corridor and trading-pair search | Supports return-trip discovery |
| ETA ensemble | Historical baseline plus live and ML correction | Must expose confidence and freshness |
| Event workflow | Marketing and follow-up automation | No direct state mutation |
| Telemetry ingestion | GPS validation, dedupe, and breach detection | Only movement-safe states should update live tracking |

## Resilience Tooling Pattern

| Component | Suggested Role | Constraint |
|-----------|----------------|------------|
| Celery | Replay, retry, and retraining tasks | Must remain idempotent |
| n8n | Orchestration and workflow retries | Resume from safe checkpoints only |
| Prometheus/Grafana | Operational monitoring | Alert on degradation, not just outage |
| DLQ | Failure containment | Never hide failed mutation attempts |

## Scenarios

- [[Scenario - System Outage Handling]]
- [[Scenario - API Integration Failure]]

## Related Hubs

- [[AI Agents Hub]]
- [[Operations Strategy Hub]]

## Open Questions

- [ ] Build vs buy decisions for components?
- [ ] Cloud vs on-premise tradeoff?
- [ ] Monolith vs microservices?

---

*Technology enables. Architecture scales.*
