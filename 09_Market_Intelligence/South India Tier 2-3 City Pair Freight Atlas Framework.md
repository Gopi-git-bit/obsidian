---
title: South India Tier 2-3 City Pair Freight Atlas Framework
type: market-intelligence-framework
category: city-pair-database
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - city-pairs
  - tier-2
  - tier-3
  - south-india
  - freight-atlas
  - corridor-scoring
related:
  - South India City Pair Master
  - South India Multimodal Freight Strategy
  - Optimized Solution Framework for Current Logistics Project
  - Multimodal Freight Decision Planning Framework
---

# South India Tier 2-3 City Pair Freight Atlas Framework

## Core Idea

Build the freight database like an atlas, not like one giant note.

A city-pair database should let the startup answer:

```text
Which corridors should we launch first?
Which corridors need validation?
Which corridors have backhaul opportunity?
Which corridors are port-linked, rail-feasible, or road-only?
Which corridors are fragmented enough for a startup to enter?
```

The best database object is the city pair.

Industries explain cargo.
Cities explain supply and demand nodes.
But city pairs explain the actual business.

---

# 1. Recommended Vault Structure

Use this structure inside the existing vault rather than creating a disconnected mini-vault.

```text
09_Market_Intelligence/
├── Cities/
├── City_Pairs/
├── Industries/
├── Nodes/
├── Partners/
└── Research/

12_Dashboards/
└── South India City Pair Master.md

00_System/Templates/
├── City Template.md
├── City Pair Template.md
├── Industry Template.md
├── Node Template.md
└── Partner Template.md
```

## Rule

```text
One city = one reusable note.
One city pair = one corridor note.
One dashboard = many filtered views.
```

This prevents the freight database from becoming a digital godown where everything exists but nothing can be found.

---

# 2. City Pair Scoring Model

Use this corridor scoring formula:

```text
Corridor Score =
0.25 x Volume Score
+ 0.20 x Backhaul Score
+ 0.20 x Margin Score
+ 0.15 x Tier-2/3 Advantage
+ 0.10 x Industry Fragmentation
+ 0.10 x Operational Ease
```

## Score Meaning

| Score | Meaning |
| ---: | --- |
| 8.0-10 | launch priority |
| 6.5-7.9 | validate deeply |
| 5.0-6.4 | watchlist |
| below 5 | do not launch now |

## Why These Weights

| Factor | Why It Matters |
| --- | --- |
| Volume | no volume means no business |
| Backhaul | reduces empty return and protects carrier economics |
| Margin | avoids chasing busy but unprofitable lanes |
| Tier-2/3 advantage | where large platforms may be weaker and MSME friction is higher |
| Fragmentation | creates room for verified partner orchestration |
| Operational ease | protects MVP execution from drowning in complexity |

---

# 3. Starter Corridor Prioritization

## Active / High Priority

| City Pair | State Pair | Industry | Mode | Why It Matters |
| --- | --- | --- | --- | --- |
| Chennai <-> Bengaluru | TN-KA | auto, FMCG, electronics | road | dense high-frequency corridor |
| Hosur <-> Bengaluru | TN-KA | EV, auto components | road | short JIT lane with milk-run potential |
| Tiruppur <-> Chennai Port | TN | textiles/export | road + port | export-linked MSME cluster |
| Hyderabad <-> Chennai | TG-TN | pharma, FMCG | road + rail | road-vs-rail decision lane |
| Hyderabad <-> Vizag | TG-AP | pharma/export, bulk | road + rail + port | port-linked multimodal opportunity |
| Coimbatore <-> Tiruppur | TN | textiles | road | short cluster lane with frequent SME movement |
| Coimbatore <-> Erode | TN | textiles, agri | road | western TN industrial/agri flow |
| Vizag <-> Vijayawada | AP | port, fertilizer, seafood, chemicals | road + rail | coastal/port-linked AP lane |
| Vijayawada <-> Guntur | AP | agri, food, tobacco, chilli | road | dense agri/MSME lane |
| Kochi <-> Coimbatore | KL-TN | port, machinery, perishables | road | port-to-industrial connection |

## Validation Corridors

| City Pair | State Pair | Industry | Mode | Validation Focus |
| --- | --- | --- | --- | --- |
| Trichy <-> Karur | TN | home textiles, cement, engineering | road | recurring textile and industrial loads |
| Madurai <-> Trichy | TN | FMCG, retail, agri | road | regional distribution density |
| Salem <-> Bengaluru | TN-KA | steel, textiles, FMCG | road | backhaul and partner depth |
| Hubballi <-> Bengaluru | KA | FMCG, engineering, agri | road + rail | north Karnataka demand |
| Hubballi <-> Belagavi | KA | engineering, sugar, FMCG | road | high local/regional movement |
| Bengaluru <-> Mysuru | KA | FMCG, food, industrial | road | high-frequency intra-state freight |
| Nellore <-> Guntur | AP | rice, seafood, construction | road | agri/seafood validation |
| Kakinada <-> Vijayawada | AP | port, agri, aqua | road + port | port-linked cargo |
| Mangaluru <-> Hubballi | KA | port, FMCG, agri | road + port | ghat/port buffer needed |
| Palakkad <-> Coimbatore | KL-TN | FMCG, textiles, food | road | cross-border cluster movement |

## Watchlist Corridors

| City Pair | State Pair | Industry | Mode | Why Watch |
| --- | --- | --- | --- | --- |
| Dindigul <-> Madurai | TN | food, textiles, leather | road | local density needs proof |
| Namakkal <-> Salem | TN | poultry, transport, textiles | road | potential but needs field data |
| Thoothukudi <-> Madurai | TN | port, salt, agri | road + port | port-linked but may be seasonal |
| Rajahmundry <-> Vizag | AP | agri, aqua, port | road | coastal demand validation |
| Tirupati <-> Chennai | AP-TN | electronics, food, FMCG | road | strong but competitive |
| Davangere <-> Hubballi | KA | agri, textiles | road | demand depth unclear |
| Ballari <-> Bengaluru | KA | mining, steel, industrial | road + rail | commodity-heavy complexity |
| Kozhikode <-> Kochi | KL | FMCG, seafood, retail | road | Kerala intra-state congestion |
| Warangal <-> Hyderabad | TG | agri, textiles, pharma distribution | road | good regional lane candidate |
| Khammam <-> Vijayawada | TG-AP | agri, rice, FMCG | road | cross-state agri validation |

---

# 4. Data Fields Never To Skip

Every city-pair note should include these YAML fields:

```yaml
type: city_pair
origin:
destination:
distance_km:
state_pair:
tier_pair:
primary_industries:
cargo_flows:
best_mode:
alternative_mode:
rail_feasible:
port_linked:
airport_linked:
warehouse_needed:
backhaul_potential:
seasonality:
demurrage_risk:
payment_risk:
customer_type:
carrier_type_needed:
competition_level:
data_confidence:
score_volume:
score_backhaul:
score_margin:
score_tier23:
score_fragmentation:
score_operational_ease:
final_corridor_score:
status:
```

Why this matters:

```text
If these fields are consistent, the Obsidian database can later become Airtable, Supabase, PostgreSQL, or an app database.
```

---

# 5. Evidence Discipline

Do not mix evidence and assumptions.

Use this label system:

| Label | Meaning |
| --- | --- |
| Evidence | verified from official source, data, interview, or shipment record |
| Assumption | logical but not verified |
| Hypothesis | needs testing |
| Field note | observed manually |
| Quote | from transporter/customer |
| Estimate | rough number |

## Evidence Log Format

```md
## Evidence Log

| Claim | Type | Source | Confidence |
| --- | --- | --- | --- |
| Corridor has textile freight demand | Evidence | association/source/interview | High |
| Backhaul from destination is weaker | Hypothesis | needs transporter calls | Medium |
| Road is best mode | Assumption | distance and cargo profile | High |
```

## Data Confidence Levels

| Confidence | Meaning |
| --- | --- |
| High | verified by multiple sources or shipment data |
| Medium | supported by one source and logical pattern |
| Low | assumption or early field hypothesis |

---

# 6. Corridor Selection Rule

Pick city pairs where at least three are true:

```text
1. There is an industrial cluster.
2. There is recurring MSME shipment demand.
3. There is a return-load problem.
4. There is port/rail/warehouse linkage.
5. There is high fragmentation.
6. Big platforms are less dominant.
7. There are payment and documentation pain points.
8. Partner depth can be built quickly.
```

If a corridor has volume but no margin, be careful.
If a corridor has margin but no frequency, validate before launch.
If a corridor has frequency, fragmentation, and backhaul pain, it becomes interesting.

---

# 7. Research Workflow

For every new city pair:

```text
Step 1: Create city notes.
Step 2: Create city-pair note.
Step 3: Add industries.
Step 4: Add cargo types.
Step 5: Add route distance.
Step 6: Add available modes.
Step 7: Add nodes: port, rail, warehouse, airport.
Step 8: Estimate backhaul strength.
Step 9: Score corridor.
Step 10: Add validation tasks.
Step 11: Interview transporters/MSMEs.
Step 12: Update confidence score.
```

## Field Validation Minimum

Before promoting a corridor to launch:

```text
10 transporter calls
5 shipper/MSME interviews
3 rate-card samples
2 loading/unloading observations
1 backhaul validation pass
```

This keeps the atlas from becoming beautiful fiction.

---

# 8. Suggested City Notes To Create Next

## Tamil Nadu

```text
Coimbatore
Tiruppur
Erode
Salem
Karur
Madurai
Trichy
Thoothukudi
Dindigul
Namakkal
Hosur
```

## Kerala

```text
Kochi
Thrissur
Kozhikode
Palakkad
Alappuzha
Kollam
Kannur
```

## Karnataka

```text
Mysuru
Hubballi
Dharwad
Belagavi
Mangaluru
Tumakuru
Davangere
Ballari
Hassan
```

## Andhra Pradesh

```text
Visakhapatnam
Vijayawada
Guntur
Nellore
Kurnool
Anantapur
Rajahmundry
Kakinada
Tirupati
Kadapa
```

## Telangana

```text
Hyderabad
Warangal
Karimnagar
Nizamabad
Khammam
Mahbubnagar
```

---

# 9. Dataview Dashboards

## High Priority Corridors

```dataview
TABLE origin, destination, primary_industries, best_mode, final_corridor_score, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE type = "city_pair" AND final_corridor_score >= 8
SORT final_corridor_score DESC
```

## Port-Linked Corridors

```dataview
TABLE origin, destination, primary_industries, best_mode, priority, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE port_linked = true OR contains(best_mode, "port")
SORT priority DESC
```

## Backhaul Gap Corridors

```dataview
TABLE origin, destination, primary_industries, backhaul_potential, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE backhaul_potential = "low" OR backhaul_potential = "medium"
SORT final_corridor_score DESC
```

## Validate Next

```dataview
TABLE origin, destination, final_corridor_score, data_confidence, status
FROM "09_Market_Intelligence/City_Pairs"
WHERE status = "validate"
SORT final_corridor_score DESC
```

---

# 10. Operating Rhythm

```text
Daily:
Add or improve 1 city-pair note.

Weekly:
Update the city-pair master dashboard.

Every 2 weeks:
Validate 3 corridors through calls/interviews.

Monthly:
Promote corridors:
watchlist -> validate -> launch -> active.
```

## First Database Target

```text
30 city-pair notes
25 city notes
8 industry notes
10 node notes
1 master dashboard
1 validation dashboard
1 source index
```

This is enough to become dangerous in a useful way.

Not a research attic.

A freight command room.

---

# Source Links

- [SLBC Tamil Nadu - Industries](https://www.slbctn.com/Industries.aspx)
- [MoSPI - Inter-State Movement/Flows of Goods](https://www.mospi.gov.in/63-inter-state-movementflows-goods)
- [Economic Times - India logistics cost estimated at 7.97 percent of GDP in 2023-24](https://economictimes.indiatimes.com/news/economy/indias-logistics-cost-estimated-at-7-97-of-gdp-in-2023-24-says-dpiit-report/articleshow/124118364.cms)
- [[South India City Pair Master]]
- [[South India Multimodal Freight Strategy]]
- [[Logistics Cost Analysis Template for Multimodal Freight]]
- [[Optimized Solution Framework for Current Logistics Project]]
