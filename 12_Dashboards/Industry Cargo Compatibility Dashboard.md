---
title: Industry Cargo Compatibility Dashboard
type: dashboard
category: industry-cargo-compatibility
status: active
region: South India
created: 2026-04-30
tags:
  - dashboard
  - industry-verticals
  - cargo-compatibility
  - triangle-route
related:
  - Industry Hub Cargo Matrix for Triangle Backhaul Optimization
---

# Industry Cargo Compatibility Dashboard

## Purpose

Track which industries create strong triangle opportunities and which cargo combinations require guardrails.

---

# Core Industry Matrix

| Industry | Triangular Fit | Main Hubs | Best Return Fillers | Main Risk |
| --- | --- | --- | --- | --- |
| Textiles/apparel | very high | Tiruppur, Coimbatore, Erode, Karur | packaging, FMCG, yarn, fabric | moisture/damage, chemical contamination |
| Auto/EV | high | Chennai, Hosur, Sri City, Bengaluru | steel, rubber, tooling, packaging | JIT failure, battery compliance |
| Heavy engineering | medium/high | Coimbatore, Trichy, Salem, Vizag | raw metals, foundry inputs | vehicle/loading specialization |
| Agri/FMCG | high | Erode, Guntur, Vijayawada, Madurai | fertilizers, packaging | seasonality, temperature/humidity |
| Chemicals/pharma | high but strict | Manali, Vizag, Kochi, Hosur | packaging, solvents, lab equipment | hazmat/cold-chain compliance |
| Port/export/e-commerce | very high | Chennai, Vizag, Kochi, Sri City | packaging, retail restocking | customs/slot timing/security |

---

# Dataview: Industry Verticals

```dataview
TABLE industry_vertical, key_hubs, backhaul_gap, triangular_fit_score, status
FROM "09_Market_Intelligence/Industries"
WHERE type = "industry_vertical"
SORT triangular_fit_score DESC
```

# Dataview: High-Risk Cargo Routes

```dataview
TABLE origin, destination, primary_cargo, vehicle_types, data_confidence, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE contains(primary_cargo, "chemicals") OR contains(primary_cargo, "pharma") OR contains(primary_cargo, "EV_batteries")
SORT data_confidence ASC
```
