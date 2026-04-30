---
title: South India City Pair Master
type: dashboard
category: freight-atlas
status: active
region: South India
created: 2026-04-30
tags:
  - dashboard
  - city-pairs
  - tier-2
  - tier-3
  - south-india
  - corridor-priority
related:
  - South India Tier 2-3 City Pair Freight Atlas Framework
  - South India Multimodal Freight Strategy
---

# South India City Pair Master

## Purpose

This is the map-room dashboard for South India tier-2 and tier-3 city-pair freight opportunities.

Use it to decide:

```text
launch now
validate next
watchlist
avoid for now
```

---

# Master Corridor Table

| City Pair | State Pair | Industry | Mode | Priority | Backhaul | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Chennai <-> Bengaluru | TN-KA | Auto, FMCG, electronics | Road | High | High | active |
| Hosur <-> Bengaluru | TN-KA | EV, auto components | Road | High | High | active |
| Tiruppur <-> Chennai Port | TN | Textiles/export | Road + port | High | Medium | active |
| Hyderabad <-> Chennai | TG-TN | Pharma, FMCG | Road + rail | High | High | active |
| Hyderabad <-> Vizag | TG-AP | Pharma/export, bulk | Road + rail + port | High | Medium | active |
| Coimbatore <-> Tiruppur | TN | Textiles | Road | High | High | validate |
| Coimbatore <-> Erode | TN | Textiles, agri | Road | High | Medium | validate |
| Vizag <-> Vijayawada | AP | Port, fertilizer, seafood, chemicals | Road + rail | High | Medium | validate |
| Vijayawada <-> Guntur | AP | Agri, food, tobacco, chilli | Road | High | High | validate |
| Kochi <-> Coimbatore | KL-TN | Port, machinery, perishables | Road | Medium | Medium | validate |
| Trichy <-> Karur | TN | Home textiles, cement, engineering | Road | Medium | High | validate |
| Madurai <-> Trichy | TN | FMCG, retail, agri | Road | Medium | Medium | validate |
| Salem <-> Bengaluru | TN-KA | Steel, textiles, FMCG | Road | Medium | Medium | validate |
| Hubballi <-> Bengaluru | KA | FMCG, engineering, agri | Road + rail | Medium | Medium | validate |
| Hubballi <-> Belagavi | KA | Engineering, sugar, FMCG | Road | Medium | High | validate |
| Bengaluru <-> Mysuru | KA | FMCG, food, industrial | Road | Medium | High | validate |
| Nellore <-> Guntur | AP | Rice, seafood, construction | Road | Medium | Medium | validate |
| Kakinada <-> Vijayawada | AP | Port, agri, aqua | Road + port | Medium | Medium | validate |
| Mangaluru <-> Hubballi | KA | Port, FMCG, agri | Road + port | Medium | Medium | validate |
| Palakkad <-> Coimbatore | KL-TN | FMCG, textiles, food | Road | Medium | Medium | validate |
| Dindigul <-> Madurai | TN | Food, textiles, leather | Road | Low | Medium | watchlist |
| Namakkal <-> Salem | TN | Poultry, transport, textiles | Road | Low | Medium | watchlist |
| Thoothukudi <-> Madurai | TN | Port, salt, agri | Road + port | Medium | Medium | watchlist |
| Rajahmundry <-> Vizag | AP | Agri, aqua, port | Road | Low | Medium | watchlist |
| Tirupati <-> Chennai | AP-TN | Electronics, food, FMCG | Road | Medium | Medium | watchlist |
| Davangere <-> Hubballi | KA | Agri, textiles | Road | Low | Medium | watchlist |
| Ballari <-> Bengaluru | KA | Mining, steel, industrial | Road + rail | Medium | Low | watchlist |
| Kozhikode <-> Kochi | KL | FMCG, seafood, retail | Road | Low | Medium | watchlist |
| Warangal <-> Hyderabad | TG | Agri, textiles, pharma distribution | Road | Medium | High | watchlist |
| Khammam <-> Vijayawada | TG-AP | Agri, rice, FMCG | Road | Medium | Medium | watchlist |

---

# Scoring Model

```text
Corridor Score =
0.25 x Volume Score
+ 0.20 x Backhaul Score
+ 0.20 x Margin Score
+ 0.15 x Tier-2/3 Advantage
+ 0.10 x Industry Fragmentation
+ 0.10 x Operational Ease
```

---

# Starter Scoring Table

| City Pair | Volume | Backhaul | Margin | Tier 2/3 | Fragmentation | Ease | Final | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Coimbatore <-> Tiruppur | 8 | 8 | 6 | 10 | 9 | 8 | 8.1 | Launch |
| Tiruppur <-> Chennai Port | 9 | 6 | 8 | 8 | 9 | 7 | 8.0 | Launch |
| Chennai <-> Bengaluru | 10 | 8 | 7 | 6 | 7 | 8 | 8.0 | Launch |
| Hosur <-> Bengaluru | 9 | 8 | 7 | 8 | 8 | 9 | 8.2 | Launch |
| Hyderabad <-> Vizag | 8 | 6 | 8 | 7 | 7 | 6 | 7.2 | Validate |
| Vizag <-> Vijayawada | 8 | 7 | 7 | 8 | 7 | 7 | 7.4 | Validate |
| Kochi <-> Coimbatore | 7 | 6 | 7 | 8 | 7 | 6 | 6.9 | Validate |
| Hubballi <-> Bengaluru | 7 | 6 | 7 | 8 | 7 | 6 | 6.9 | Validate |

---

# Dataview: High Priority Corridors

```dataview
TABLE origin, destination, primary_industries, best_mode, final_corridor_score, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE type = "city_pair" AND final_corridor_score >= 8
SORT final_corridor_score DESC
```

# Dataview: Validate Next

```dataview
TABLE origin, destination, final_corridor_score, data_confidence, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE status = "validate"
SORT final_corridor_score DESC
```

# Dataview: Port-Linked Corridors

```dataview
TABLE origin, destination, primary_industries, best_mode, priority, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE port_linked = true OR contains(best_mode, "port")
SORT priority DESC
```

# Dataview: Backhaul Opportunities

```dataview
TABLE origin, destination, primary_industries, backhaul_potential, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE backhaul_potential = "medium" OR backhaul_potential = "low"
SORT final_corridor_score DESC
```

---

# Monthly Promotion Rule

```text
watchlist -> validate -> launch -> active
```

Promote only when evidence improves.

Do not promote a corridor because it looks exciting in a table.

A table is a map. The road still has potholes.
