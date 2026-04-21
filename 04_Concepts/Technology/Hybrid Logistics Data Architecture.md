---
type: concept
domain: technology
decision_value: high
status: evergreen
related_hubs:
  - Technology Stack Hub
  - Operations Strategy Hub
tags:
  - concept
  - technology
  - data
  - architecture
---

# Hybrid Logistics Data Architecture

## Definition

A system design pattern that splits logistics data across specialized stores, typically using relational databases for transactional truth and graph databases for network-aware decisions.

## Why It Matters

- Pricing and settlement require deterministic, auditable records.
- Routing, backhaul, and driver familiarity are relationship-heavy problems.
- One storage model rarely serves both equally well at scale.

## Recommended Split

| Layer | Best Fit | Typical Responsibility |
|-------|----------|------------------------|
| SQLite / relational | Financial truth | Quotes, fees, fuel prices, service tiers, audit logs |
| Neo4j / graph | Network intelligence | Routes, nearby alternatives, driver familiarity, backhaul detection |
| GraphQL gateway | Orchestration | Unified API for pricing, fleet, and route decisions |
| Supabase/PostgreSQL + PostGIS | Operational system of record | Identity, orders, events, fleet, telemetry, settlement, spatial search |

## Design Principles

1. Keep quote calculations reproducible from relational inputs.
2. Use graph lookups to enrich decisions, not to store every financial field.
3. Persist graph-derived discounts and signals back into relational audit records.
4. Centralize configuration so pricing rules can be tuned without full redeploys.
5. Preserve an event log for lifecycle truth and a spatial layer for corridor-aware operations.

## Decision Impact

- Strengthens [[Dynamic Pricing Logic]]
- Enables [[Return Load Optimization]]
- Supports [[Multi-Objective Vehicle Scoring]]
- Improves quote explainability for shippers and operators

## Risks

- Cross-store consistency can drift if orchestration is weak.
- Graph enrichments may look authoritative even when data freshness is poor.
- Operational complexity rises if each store owns overlapping truth.
- Telemetry and event volumes can overwhelm naive table design without indexing or partition strategy.

## Related Notes

- [[Technology Stack Hub]]
- [[Authoritative Database Schema]]
- [[Dynamic Pricing Logic]]
- [[Return Load Optimization]]
- [[Digital Freight Marketplace]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
