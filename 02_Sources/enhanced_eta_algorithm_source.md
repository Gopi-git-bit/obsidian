---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline ETA architecture brief
notes: Enhanced ETA architecture covering deterministic base ETA, real-time correction factors, ML residual prediction, confidence intervals, and event-driven recalculation
---

# Enhanced ETA Algorithm Source

## Overview

This source refines Zippy's ETA architecture around:

- a deterministic base ETA layer grounded in route segments and historical speeds
- live ETA correction using traffic, weather, incidents, driver behavior, and load context
- an optional ML residual model that improves accuracy without replacing hard operational logic
- confidence-scored outputs with explainable factor summaries
- event-driven recalculation on significant movement and external-context change
- safe fallback behavior when APIs or models degrade

## Core Takeaways

### 1. ETA Should Be Layered, Not Single-Pass

- Start from a deterministic route-and-history baseline.
- Apply live adjustment factors only after a stable base ETA exists.
- Use ML as a correction layer, not as the sole ETA source.

### 2. Confidence Is a First-Class Output

- ETA should include confidence bounds, not just a single timestamp.
- Low-confidence ETA should trigger escalation and conservative communication.
- Confidence quality should be monitored for calibration drift.

### 3. Recalculation Must Be Event-Driven

- Significant GPS movement, traffic change, or weather change should trigger recalculation.
- Recalculation belongs in asynchronous workflows so route ingestion stays responsive.

### 4. ETA Needs Explainability

- Customer-facing and operator-facing systems should understand why ETA moved.
- Factor summaries make delay communication and supervisor review more trustworthy.

### 5. Degraded Inputs Must Not Break Operations

- External API failures should fall back to historical or cached logic.
- Stale data should be surfaced as warnings instead of silently trusted.

## Derived Notes

- [[ETA Prediction Logic]]
- [[Route Optimization Logic]]
- [[Unified Routing & Optimization Algorithm]]
- [[Transportation Agent]]
- [[Logistics SLA]]

## Related Notes

- [[unified_routing_optimization_source]]
- [[fallback_resilience_architecture_source]]
- [[pricing_engine_architecture_source]]

