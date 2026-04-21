---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline TMS execution spec
notes: Refined TMS execution specification covering routing hierarchy, deterministic ETA bounds, GPS validation, SLA monitoring, event contracts, fallback handling, and Codex-safe enforcement rules
---

# TMS Execution Spec Source

## Overview

This source refines the TMS layer around:

- explicit TMS, OMS, IMS, and supervisor boundaries
- one routing-engine hierarchy with deterministic fallback order
- clamped ETA computation and bounded realtime multipliers
- canonical GPS ingestion validation and deduplication rules
- SLA and deviation thresholds for live transportation monitoring
- a single event schema for inter-agent and workflow traffic
- DLQ and retry policy for resilient execution

## Core Takeaways

### 1. TMS Needs Hard Operational Boundaries

- TMS should route, predict ETA, ingest telemetry, and monitor SLA.
- TMS should not change pricing, reassign drivers, or mutate order state directly.

### 2. Routing Needs a Clear Primary and Fallback Chain

- Parallel mention of multiple routing engines creates execution ambiguity.
- Valhalla, then OSRM, then heuristic, then cache is a clean production hierarchy.

### 3. ETA Must Stay Deterministic

- Realtime multipliers can tune ETA, but they should remain clamped.
- ML must not override hard ETA bounds or lifecycle rules.

### 4. Telemetry Requires Strict Validation

- GPS pings should be state-bounded, accuracy-filtered, and replay-safe.
- Deviation and silence thresholds should be explicit enough for automation.

## Derived Notes

- [[TMS Execution Architecture]]
- [[Transportation Agent]]
- [[Unified Routing & Optimization Algorithm]]
- [[Logistics SLA]]

## Related Notes

- [[unified_routing_optimization_source]]
- [[enhanced_eta_algorithm_source]]
- [[fallback_resilience_architecture_source]]

