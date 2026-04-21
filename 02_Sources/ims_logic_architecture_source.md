---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline IMS architecture brief
notes: Optimized IMS logic for deterministic vehicle matching, atomic reservations, loop-aware scoring, and event-driven OMS separation
---

# IMS Logic Architecture Source

## Overview

This source refines the Zippy IMS architecture around:

- strict separation between IMS suggestion logic and OMS state mutation
- deterministic hard filters before any advisory or ML scoring
- atomic vehicle reservation with bounded TTL
- explicit fallback cascades for exhausted searches
- loop-aware matching to reduce empty miles
- compliance-first dispatch eligibility

## Core Takeaways

### 1. IMS Suggests, OMS Commits

- IMS should never mutate order state directly.
- The output of IMS is candidate and exhaustion events, not assignment finality.
- Reservation and suggestion logic must stay decoupled from lifecycle transitions.

### 2. Determinism Comes Before Intelligence

- Hard filters should reject ineligible vehicles immediately.
- Cache and rule logic should run before ML scoring.
- ML can refine ranking but must not override feasibility rules.

### 3. Matching Needs Concurrency Control

- Atomic reservations prevent double-booking under parallel searches.
- Reservation TTLs must expire cleanly and never create implied assignments.

### 4. Return Logic Belongs Inside Matching Economics

- Vehicles with stronger loop or return-trip history should be favored where commercially valid.
- Loop metadata can enrich OMS and FIN without merging settlement flows.

### 5. Exhaustion Is a First-Class Outcome

- No-match cases should trigger a deterministic escalation ladder.
- Fallbacks should be observable, time-bounded, and event-driven.

## Derived Notes

- [[IMS Matching Engine]]
- [[Load Matching Algorithm]]
- [[Vehicle Assignment Logic]]
- [[Resource Management Agent]]
- [[Fallback & Resilience Architecture]]

## Related Notes

- [[unified_routing_optimization_source]]
- [[pricing_engine_architecture_source]]
- [[grok_algo_source_reference]]

