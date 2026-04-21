---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline routing architecture brief
notes: Unified routing and optimization design covering Valhalla, OR-Tools, RDS penalties, return-trip marketing, and state-safe orchestration
---

# Unified Routing Optimization Source

## Overview

This source defines a production-oriented routing architecture for Zippy Logistics built around:

- deterministic routing gates before optimization
- Valhalla for truck-aware matrix and dynamic route costing
- LightGBM-based route difficulty penalties as bounded modifiers
- OR-Tools for VRP, PDP, and backhaul sequencing
- metadata-only return-trip suggestions until explicit acceptance
- hard separation between routing suggestions and state transitions

## Core Takeaways

### 1. Routing Must Stay State-Safe

- Routing engines should never mutate order state directly.
- OMS remains the only orchestrator that requests state transitions.
- Suggestions must be traceable through `trace_id`, `idempotency_key`, and `agent_code`.

### 2. Optimization Is Layered

- Gatekeeper rules run first.
- IMS pre-filters feasible capacity.
- Valhalla computes route metrics.
- RDS applies bounded penalties.
- OR-Tools optimizes route sequences and pickup-delivery pairings.

### 3. Return Trips Are Commercially Useful but Operationally Sensitive

- Return-trip matches stay as metadata until explicit acceptance.
- `loop_group_id` binds related orders without merging settlement logic.
- PCR thresholds should screen out weak backhaul campaigns.

### 4. SLA Enforcement Must Be Observable

- ETA and breach monitoring belongs to TMS.
- SLA breaches create disputes, not automatic refunds or fare changes.
- DLQ and supervisor alerts are part of the control plane, not an afterthought.

### 5. Fallbacks Need a Defined Hierarchy

- Prefer Valhalla first, then OSRM/static routing, then heuristics, then cache.
- Fallbacks must degrade gracefully without bypassing the state machine.

## Derived Notes

- [[Unified Routing & Optimization Algorithm]]
- [[Route Optimization Logic]]
- [[Return Load Optimization]]
- [[Logistics SLA]]
- [[Order Lifecycle]]
- [[Technology Stack Hub]]

## Related Notes

- [[pricing_engine_architecture_source]]
- [[grok_algo_source_reference]]
- [[Algorithms Hub]]

