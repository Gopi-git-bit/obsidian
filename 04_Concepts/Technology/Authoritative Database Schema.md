---
type: concept
domain: technology
decision_value: high
status: verified
related_hubs:
  - Technology Stack Hub
  - Operations Strategy Hub
tags:
  - concept
  - database
  - postgres
  - postgis
  - supabase
  - event-sourcing
---

# Authoritative Database Schema

## Purpose

Define the core database structure for the autonomous logistics platform so state, geography, fleet, finance, telemetry, and AI decisions remain queryable, auditable, and operationally safe.

## Recommended Domain Split

| Domain | Typical Tables | Responsibility |
|--------|----------------|----------------|
| Identity | users, customer_profiles, driver_profiles, transport_companies | Actor identity and operational roles |
| Geography | city_tiers, pricing_rules, trade_corridors | Spatial pricing and corridor intelligence |
| Fleet | vehicles, driver_vehicle_assignments, compliance_documents | Fleet availability and compliance status |
| Orders | orders, order_event_logs, return_trip_offers | Lifecycle projection and event truth |
| Telemetry | gps_pings | Real-time movement and ETA inputs |
| Finance | payments, settlements, invoices, ledger_entries | Deterministic money flow and auditability |
| AI audit | agent_decisions_audit, model_versions, feature_flags | Controlled autonomy and observability |
| Security | timestamp and hash-chain triggers | Integrity and traceability controls |

## Core Design Principles

1. Keep event logs as the durable record of order behavior.
2. Use the `orders` table as a read model, not the only truth surface.
3. Make PostGIS native for routing, matching, and corridor economics.
4. Separate payments, settlements, invoices, and ledger entries clearly.
5. Record AI decisions and feature-rollout state explicitly.

## Order and Event Pattern

- `orders.status` should reflect the latest accepted projection of the lifecycle.
- `order_event_logs` should capture the actual event stream emitted by apps and agents.
- Return-trip offers should remain metadata-safe until explicitly accepted.
- Loop or return linkage should enrich operations without collapsing per-order accounting.

## Spatial Pattern

- Store city, route, vehicle, and ping geometry in PostGIS-ready columns.
- Add GIST indexes for city lookup, corridor discovery, online vehicle search, and GPS history.
- Use spatial tables to support radius expansion, trade-corridor ranking, and backhaul discovery.

## AI and Autonomy Pattern

- Log agent decisions with `agent_code`, decision path, confidence, model version, and output payload.
- Keep feature flags in the database so autonomy changes can be rolled out gradually and reversed quickly.
- Prefer explicit audit chains and timestamps over hidden model-side state.
- Keep policy registries and policy history tables for strategic changes that should not require code edits.

## Finance Pattern

- Capture provider payment facts separately from internal settlements.
- Treat ledger entries as the final audit-proof financial trace.
- Enforce settlement release rules from lifecycle state and policy, not from UI assumptions.

## Implementation Guardrails

- Do not let agents mutate lifecycle state outside the approved transition path.
- Avoid storing raw sensitive identity artifacts when hashes or references are sufficient.
- Use generated geometry columns or normalized spatial storage to reduce duplication.
- Partition or otherwise manage high-volume telemetry tables as scale grows.
- Preserve contract, compliance-document, POD, and tax evidence in ways that support audit and dispute review.

## Related Notes

- [[Hybrid Logistics Data Architecture]]
- [[Order Lifecycle]]
- [[Technology Stack Hub]]
- [[ETA Prediction Logic]]
- [[IMS Matching Engine]]
- [[Dynamic Pricing Logic]]
- [[Scenario Management Framework]]
- [[Legal Compliance Framework]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
