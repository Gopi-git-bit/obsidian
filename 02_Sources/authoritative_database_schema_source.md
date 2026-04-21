---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline authoritative database schema brief
notes: Supabase and PostgreSQL schema for identity, geography, fleet, orders, telemetry, finance, AI audit, feature flags, and compliance-safe triggers
---

# Authoritative Database Schema Source

## Overview

This source consolidates Zippy's database architecture around:

- eight operational domains spanning identity, geography, fleet, orders, tracking, finance, AI audit, and security
- Supabase and PostgreSQL compatibility with PostGIS support
- event-sourced order truth with lightweight order projections
- spatial indexing for city, corridor, vehicle, and telemetry lookups
- finance-safe settlement and ledger structures
- audit-safe AI decision logging and feature-flagged autonomy control

## Core Takeaways

### 1. Orders Should Be Event-Centered

- `orders` is a projection for fast operational reads.
- `order_event_logs` is the durable behavioral history.
- This keeps the lifecycle observable and replay-friendly.

### 2. Spatial Data Is First-Class

- City tiers, trade corridors, vehicle positions, and GPS pings should be queryable with PostGIS.
- Return-trip and matching logic become materially stronger when spatial indexes are built in from the start.

### 3. AI Needs Audit and Release Controls

- Agent decisions should be logged with path, confidence, model version, and chainable audit context.
- Feature flags should control rollout instead of burying autonomy changes inside code alone.

### 4. Finance Must Stay Deterministic

- Payments, settlements, invoices, and ledger entries need explicit separation.
- Settlement release should remain policy-bound to lifecycle milestones.

## Derived Notes

- [[Authoritative Database Schema]]
- [[Hybrid Logistics Data Architecture]]
- [[Order Lifecycle]]
- [[Technology Stack Hub]]

## Related Notes

- [[pricing_engine_architecture_source]]
- [[unified_routing_optimization_source]]
- [[ims_logic_architecture_source]]

