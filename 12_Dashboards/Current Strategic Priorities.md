---
type: concept
domain: dashboard
scope: executive
status: active
last_updated: 2026-04-30
related_hubs:
  - Operations Strategy Hub
  - Business Models Hub
tags:
  - dashboard
  - strategy
---

# Current Strategic Priorities

## Overview

High-level snapshot of current strategic focus areas for the logistics platform.

Related dashboard notes:

- [[Transport Control Tower KPI Framework]]
- [[Corridor Delay Trends and Performance Dashboard Template]]
- [[Triangle Route Master]]
- [[Lane Reliability Scorecard Master]]
- [[Competitive Advantage Framework]]

## Active Priorities

### 1. Return-Trip Intelligence

- **Focus**: Convert weak direct returns into earning loops
- **Target**: Tiruppur -> Chennai -> Coimbatore -> Tiruppur as first validated triangle
- **Success Metric**: 15 percent+ revenue per vehicle day lift and 20 percent+ empty km reduction

### 2. Corridor Reliability

- **Focus**: Stage-level delay capture and lane scorecards
- **Target**: Chennai -> Coimbatore, Tiruppur -> Chennai Port, Bengaluru -> Hosur
- **Success Metric**: P90 delay tracked and reliability grades generated for first three lanes

### 3. Tier 2/3 Market Expansion

- **Focus**: Western Tamil Nadu + Chennai + Bengaluru/Sri City wedge
- **Target**: 30 directed lanes and 3 triangle routes in validation
- **Success Metric**: 3 validated corridors promoted from research to active operating lanes

### 4. Finance and Trust Layer

- **Focus**: Unified finance + invoice event lifecycle
- **Target**: Order -> Payment -> Invoice -> Settlement -> Accounting -> Closure
- **Success Metric**: Every financial event produces an accounting record

### 5. Analytics/Data Layer

- **Focus**: BI-ready PostgreSQL schema and dashboard assets
- **Target**: Star schema, dim_time calendar, Tableau prototype, corridor delay dashboard
- **Success Metric**: Dashboard answers in under 10 seconds: are we on target, which lane is failing, why?

## Key Metrics This Month

| Metric | Target | Current | Status |
|---|---:|---:|---|
| Triangle candidates documented | 3 | 3+ | active |
| Directed lanes documented | 30 target | started | active |
| Lane reliability scorecards | 3 MVP lanes | framework ready | build next |
| SQL schema files | 5 | 5 | ready for DB test |
| Dashboard assets | Tableau + Power BI | drafted | prototype next |

## Known Bottlenecks

- [ ] Need real shipment/WhatsApp/load-board data to replace sample assumptions
- [ ] SQL scripts need execution against Supabase/PostgreSQL
- [ ] Tableau/Power BI dashboards need rebuild from provided specs
- [ ] Wikilink resolution audit still pending

## High Risk Areas

- [ ] Over-documenting before validating field data
- [ ] Treating sample route assumptions as facts
- [ ] Letting dashboard grow beyond core operator metrics
- [ ] Mixing active agent architecture with legacy `10_AI_Agents` notes

## Next Review

- **Date:** Weekly
- **Main question:** Which 3 lanes or triangles can we validate with actual transporter/customer data first?
