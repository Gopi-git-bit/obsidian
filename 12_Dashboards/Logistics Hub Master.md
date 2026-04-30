---
title: Logistics Hub Master
type: dashboard
category: logistics-hub-intelligence
status: active
region: South India
created: 2026-04-30
tags:
  - dashboard
  - logistics-hubs
  - triangle-route
  - south-india
related:
  - South India Logistics Hub Intelligence Framework
  - South India Warehouse and Industrial Cluster Intelligence Framework
---

# Logistics Hub Master

## Purpose

Track major South India logistics hubs that can support continuous-load routing, triangle returns, and multimodal/cross-dock decisions.

---

# Top Hubs For Validation

| Priority | Hub | City | Tier | Role | Status |
| ---: | --- | --- | ---: | --- | --- |
| 1 | Madhavaram Logistics Hub | Chennai | 1 | metro/port/FMCG anchor | validate |
| 2 | SIPCOT Irugur / East Coimbatore | Coimbatore | 2 | central TN connector | validate |
| 3 | Tiruppur Export ICD / Avinashi Road | Tiruppur | 2 | textile export origin | validate |
| 4 | Vizag Port / Industrial Logistics | Vizag | 1/2 | east coast port anchor | watchlist |
| 5 | Sri City Integrated Logistics | Sri City | 2 | AP-TN cross-border hub | validate |
| 6 | Kochi Port / Willingdon Island | Kochi | 1/2 | Kerala-TN port anchor | watchlist |
| 7 | Dobbaspet Logistics Park | Bengaluru | 1 | KA distribution anchor | watchlist |

---

# Dataview: High-Potential Logistics Hubs

```dataview
TABLE city, name, hub_type, backhaul_potential, triangle_feasibility_score, data_confidence, status
FROM "09_Market_Intelligence/Logistics_Hubs"
WHERE type = "logistics_hub" AND triangle_feasibility_score >= 70
SORT triangle_feasibility_score DESC
```

# Dataview: Low-Confidence Hub Validation

```dataview
TABLE city, name, hub_type, backhaul_potential, last_updated
FROM "09_Market_Intelligence/Logistics_Hubs"
WHERE type = "logistics_hub" AND data_confidence = "low"
SORT city ASC
```
