---
title: Directed Lane Master
type: dashboard
category: corridor-intelligence
status: active
region: South India
created: 2026-04-30
tags:
  - dashboard
  - directed-lanes
  - trading-pairs
  - backhaul
  - south-india
related:
  - South India Trading Pair City Research System
  - South India City Pair Master
  - Triangle Route Master
---

# Directed Lane Master

## Purpose

Track each freight direction separately so the platform can detect imbalanced lanes.

The core question:

```text
Is this direction strong, weak, or a triangle candidate?
```

---

# Starter Directed Lane Table

| Lane | Cargo | Strength | Backhaul Score | Triangle Candidate | Status |
| --- | --- | --- | ---: | --- | --- |
| Tiruppur -> Chennai | garments, knitwear, export cargo | strong | 7 | yes | validate |
| Chennai -> Tiruppur | retail goods, raw materials, packaging | weak/medium | 3 | yes | validate |
| Chennai -> Coimbatore | FMCG, machinery, raw material | strong | 8 | yes | validate |
| Coimbatore -> Tiruppur | yarn, fabric, textile inputs | strong/short | 8 | yes | validate |
| Erode -> Chennai | textiles, turmeric, agri/FMCG | medium/strong | 6 | yes | validate |
| Chennai -> Erode | FMCG, raw material, retail | weak/medium | 4 | yes | validate |
| Salem -> Chennai | steel, foundry, textiles | medium/strong | 6 | yes | validate |
| Chennai -> Salem | FMCG, machinery, consumer goods | weak/medium | 4 | yes | validate |
| Bengaluru -> Sri City | electronics, components, FMCG | medium/strong | 6 | yes | validate |
| Sri City -> Chennai | industrial feeder | strong/short | 8 | yes | validate |
| Chennai -> Bengaluru | FMCG, electronics, auto | strong | 8 | no | active |
| Bengaluru -> Hosur | EV, auto parts, electronics | strong/short | 8 | no | active |
| Hosur -> Bengaluru | EV, auto parts, electronics | strong/short | 8 | no | active |
| Vizag -> Vijayawada | port cargo, fertilizer, seafood | strong | 7 | maybe | validate |
| Vijayawada -> Guntur | agri, chilli, FMCG | strong/short | 8 | maybe | validate |

---

# Directional Lane Score Fields

```text
load_frequency_score
rate_score
backhaul_score
payment_risk
demurrage_risk
vehicle_fit
lane_strength
data_confidence
```

---

# Dataview: Weak Return Lanes

```dataview
TABLE origin, destination, lane_strength, backhaul_score, triangle_candidate, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane" AND (lane_strength = "weak" OR backhaul_score <= 4)
SORT backhaul_score ASC
```

# Dataview: Triangle Candidate Lanes

```dataview
TABLE origin, destination, primary_cargo, lane_strength, nearby_substitute_city, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane" AND triangle_candidate = true
SORT origin ASC
```

# Dataview: Strong Outbound Lanes

```dataview
TABLE origin, destination, primary_cargo, load_frequency_score, rate_score, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane" AND lane_strength = "strong"
SORT load_frequency_score DESC
```

---

# Rule

A directed lane is promoted from `validate` to `active` only after:

```text
14 days of load-post observation
+ transporter interviews
+ rate benchmark
+ wait-time estimate
+ vehicle-fit validation
```
