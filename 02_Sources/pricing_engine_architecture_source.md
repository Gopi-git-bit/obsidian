---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: inline architecture brief
notes: Architecture-first pricing engine refactor for SQLite, Neo4j, GraphQL, and Obsidian integration
---

# Pricing Engine Architecture Source

## Overview

This source describes a production-ready pricing architecture for Zippy Logistics built around:

- SQLite for deterministic financial data and quote audit trails
- Neo4j for route topology, backhaul discovery, and familiarity signals
- GraphQL as an orchestration layer across relational and graph stores
- high-precision quote calculation using decimal arithmetic
- multi-objective vehicle scoring instead of simple weighted averages

## Core Takeaways

### 1. Pricing Needs Two Data Planes

- Financial truth belongs in relational storage.
- Route relationships and backhaul eligibility belong in graph storage.
- Quote generation should combine both in a single service boundary.

### 2. Pricing Should Be Auditable

- Persist quote calculations with route, vehicle, fee, discount, tax, and acceptance status.
- Index pricing history for customer, vehicle, route, and time-based audit queries.

### 3. Backhaul Should Affect Commercial Logic

- Return-route topology and available capacity can justify automated discounts.
- Backhaul discounting should be explicit, measurable, and reversible in the quote trail.

### 4. Vehicle Choice Is Multi-Objective

- Price alone is insufficient.
- Route familiarity, operational reliability, utilization, and expertise should influence allocation.
- Objective normalization prevents one metric from dominating the decision.

### 5. Knowledge Outputs Matter

- Quotes and graph insights can be exported into Obsidian-friendly markdown.
- Configuration should be hot-reloadable instead of hard-coded.

## Derived Notes

- [[Dynamic Pricing Logic]]
- [[Distance Based Pricing]]
- [[Commission vs Flat Fee]]
- [[Hybrid Logistics Data Architecture]]
- [[Multi-Objective Vehicle Scoring]]
- [[Technology Stack Hub]]
- [[Business Models Hub]]

## Source Handling Note

This source is architecture-heavy and implementation-oriented. Use it to enrich pricing, technology, and optimization notes rather than to replace existing operational notes.

## Related Notes

- [[grok_algo_source_reference]]
- [[Algorithms Hub]]
- [[Technology Stack Hub]]

