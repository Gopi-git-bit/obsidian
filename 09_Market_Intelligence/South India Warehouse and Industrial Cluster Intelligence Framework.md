---
title: South India Warehouse and Industrial Cluster Intelligence Framework
type: market-intelligence-framework
category: cluster-intelligence
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - warehouse-clusters
  - industrial-clusters
  - postgis
  - backhaul
  - triangle-route
  - south-india
related:
  - Deadhead Reduction Intelligence Layer for Tier 2-3 Freight
  - Triangle Route Engine for Return Trip Optimization
  - South India Trading Pair City Research System
  - Directed Lane Master
  - Triangle Route Master
---

# South India Warehouse and Industrial Cluster Intelligence Framework

## Core Idea

Freight does not really move from city to city.

It moves from cluster to cluster.

The system should not only match:

```text
Chennai -> Coimbatore
```

It should match:

```text
Madhavaram Warehouse Zone -> SIPCOT Irugur / Coimbatore industrial belt
```

This is the cluster-aware version of the triangle backhaul strategy.

## Core Principle

```text
Cluster-centric routing beats city-centric routing.
```

City pairs are useful for market mapping.

Warehouse and industrial clusters are useful for actual dispatch, pickup, loading, waiting-time control, and return-load planning.

---

# 1. Why Cluster Intelligence Matters

Cluster data improves:

- pickup accuracy
- loading time estimates
- cargo compatibility
- vehicle fit
- backhaul probability
- triangle route quality
- warehouse wait-time prediction
- partner acquisition targeting
- pricing by local demand pocket

## Example

A city-level route says:

```text
Chennai -> Tiruppur
```

A cluster-level route says:

```text
Madhavaram Logistics Hub -> Tiruppur Export ICD
```

The second version is operationally useful because it tells the platform:

- where the truck actually starts
- what cargo is likely
- which vehicle is needed
- which loading window matters
- which return cluster can feed the next leg

---

# 2. Warehouse Cluster Data Object

## Obsidian / Database Fields

```yaml
type: warehouse_cluster
city:
cluster_name:
coordinates:
  lat:
  lng:
radius_km:
industries:
  -
warehouse_types:
  - grade_a
  - cross_dock
  - cold_storage
  - bonded
  - hazmat
connectivity:
  highways:
    -
  rail:
  port:
  airport:
cargo_profile:
  outbound:
    -
  inbound:
    -
avg_daily_truck_movements:
peak_hours:
  -
tier:
backhaul_potential:
data_confidence:
last_updated:
idempotency_key:
```

## Important Rule

```text
Store outbound_cargo and inbound_cargo separately.
```

Because:

```text
Coimbatore -> Chennai may be machinery/textile cargo.
Chennai -> Coimbatore may be FMCG, chemicals, packaging, retail goods.
```

---

# 3. Priority Cluster Categories

## Tamil Nadu

### Chennai Metropolitan Region

| Cluster | Location | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Madhavaram Logistics Hub | North Chennai / NH 16 zone | FMCG, retail, e-commerce | Grade-A, cross-dock | primary origin for TN/KL/AP lanes |
| SIPCOT Sriperumbudur | Southwest Chennai | auto OEMs, EV, electronics | bonded, VAS, JIT | high-volume outbound to Tier 2/3 |
| Manali Industrial Belt | North Chennai | chemicals, fertilizers, petrochem | hazmat, tankers | return-leg cargo for textile clusters |
| Ambattur Industrial Estate | Northwest Chennai | engineering, auto components, textiles | SME-focused warehousing | feeder for Coimbatore/Tiruppur lanes |

### Coimbatore Belt

| Cluster | Location | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| SIPCOT Irugur / East Coimbatore | NH 544 side | textiles, engineering, pumps | industrial warehousing, cross-dock | central connector for TN/KL triangles |
| Peelamedu-Singanallur Textile Belt | Coimbatore city belt | spinning, weaving, dyeing | yarn godowns, raw material storage | origin for textile/industrial lanes |
| Coimbatore Engineering Belt | city/peripheral zones | pumps, motors, machinery | SME warehouses | machinery flow to metros and ports |

### Tiruppur Export Cluster

| Cluster | Location | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Tiruppur Export ICD / Avinashi Road belt | Tiruppur | knitwear, garment finishing | export compliance, carton/hanging storage | primary origin for Chennai port lanes |
| Dyeing and Processing Belt | Noyyal/peripheral Tiruppur | dyeing, chemical treatment | compliant storage, chemicals | return-leg chemical input demand |
| Packaging and Trims Hub | peripheral Tiruppur | labels, buttons, polybags | SME warehousing | short feeder for Coimbatore triangles |

### Salem-Erode Corridor

| Cluster | Location | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Salem Steel / Foundry Belt | Salem / NH 44 | steel, magnesite, foundry | heavy-load staging | industrial input source for metros |
| Erode Textile Belt | Erode / Bhavani side | textiles, powerloom, turmeric | yarn storage, dry godowns | feeder to Coimbatore/Chennai |
| Perundurai Agri-Mandi Zone | Erode district | turmeric, pulses, spices | ventilated storage | seasonal triangle cargo |

### Madurai-Trichy-Karur Triangle

| Cluster | Location | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Madurai Industrial / ELCOT Belt | Madurai / NH 44 | handloom, agri-processing, SME | multi-tenant, SME | southern TN redistribution node |
| Trichy BHEL / Heavy Engineering Zone | Trichy | engineering, cement, project cargo | heavy-load staging | central TN connector |
| Karur Home Textiles Hub | Karur | home textiles, bus bodies | export-compliant staging | feeder for Coimbatore/Erode |

---

## Karnataka

| Cluster | City | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Hosur Industrial Belt | Hosur | EV, auto components, pharma | JIT, ESD-safe, hazmat | Chennai/Bengaluru suburban link |
| Dobbaspet Logistics Park | Bengaluru periphery | e-commerce, retail, FMCG | Grade-A, automation-ready | origin for KA interior lanes |
| Peenya Industrial Area | Bengaluru | engineering, auto, electronics | SME warehousing | feeder for Coimbatore/Tiruppur lanes |
| Hubballi Logistics Hub | Hubballi | textiles, auto components, warehousing | Grade-B, cross-dock | North Karnataka redistribution |
| Belagavi Industrial Area | Belagavi | sugar, foundry, auto parts | heavy-load, raw material storage | KA-MH cross-border link |

---

## Andhra Pradesh / Telangana

| Cluster | City | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Vizag Port / Industrial SEZ | Visakhapatnam | port cargo, steel, seafood, fertilizers | bonded, reefer, hazmat | east coast port anchor |
| Vijayawada Agri / Distribution Hub | Vijayawada | rice mills, spices, FMCG | temp-controlled, cross-dock | inland connector |
| Guntur Spice Market | Guntur | chilli, turmeric, agri exports | dry storage, ventilated godowns | seasonal cargo source |
| Sri City SEZ | Sri City | auto, EV, electronics, pharma | Grade-A, JIT, bonded | AP-TN triangle node |
| Nellore Aquaculture Zone | Nellore | seafood, rice mills | reefer, cold storage | coastal seafood cargo |
| Hyderabad Pharma/FMCG Belt | Hyderabad | pharma, FMCG, electronics | temperature-controlled, Grade-A | TG/AP/TN trunk origin |

---

## Kerala

| Cluster | City | Primary Industries | Warehouse Types | Triangle Role |
| --- | --- | --- | --- | --- |
| Kochi Port / Willingdon Island | Kochi | spices, marine products, petroleum | bonded, reefer, multi-tenant | Kerala-TN triangle anchor |
| Kakkanad / Infopark-SmartCity Belt | Kochi | electronics, IT, high-value cargo | Grade-A, tech-enabled | high-value cargo node |
| Mattancherry Spice Trading Hub | Kochi | cardamom, pepper, ginger | dry/humidity-controlled | return-leg cargo for textile clusters |
| Palakkad Industrial Belt | Palakkad | food, light manufacturing, logistics | dry/cross-dock | Kerala-TN gateway |

---

# 4. Top 10 Clusters For MVP Validation

Start with three, not ten.

But keep this ranked list as the cluster roadmap.

| Priority | Cluster | City | Why Start Here | Expected Triangle Impact |
| ---: | --- | --- | --- | --- |
| 1 | Tiruppur Export ICD / Avinashi Road Belt | Tiruppur | garment/export origin, weak Chennai return hypothesis | high via Coimbatore feeder |
| 2 | SIPCOT Irugur / East Coimbatore | Coimbatore | central connector for TN/KL, short feeder to Tiruppur/Erode | high |
| 3 | Madhavaram Logistics Hub | Chennai | high FMCG/retail/port-linked origin | high for TN/AP/KL returns |
| 4 | Vizag Port / Industrial SEZ | Visakhapatnam | east coast port anchor | high via Vijayawada/Guntur |
| 5 | Hosur Industrial Belt | Hosur | EV/auto link between Bengaluru and Chennai | medium/high |
| 6 | Erode Textile Belt | Erode | powerloom/agri/textile hub | medium/high |
| 7 | Kochi Port / Willingdon Island | Kochi | Kerala-TN port anchor | medium/high |
| 8 | Hubballi Logistics Hub | Hubballi | North Karnataka redistribution | medium |
| 9 | Sri City SEZ | Sri City | AP-TN border industrial node | high for BLR/CHN loops |
| 10 | Karur Home Textiles Hub | Karur | export-focused textile node | medium |

## First 3 Clusters

```text
1. Tiruppur Export ICD / Avinashi Road Belt
2. SIPCOT Irugur / East Coimbatore
3. Madhavaram Logistics Hub
```

These are enough to test:

```text
Tiruppur cluster -> Chennai cluster -> Coimbatore cluster -> Tiruppur cluster
```

---

# 5. PostGIS Schema: warehouse_clusters

Use this as a draft table.

```sql
CREATE TABLE warehouse_clusters (
    cluster_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city_id UUID REFERENCES city_nodes(city_id),
    city TEXT NOT NULL,
    cluster_name TEXT NOT NULL,
    geom GEOGRAPHY(Point, 4326) NOT NULL,
    radius_km NUMERIC DEFAULT 5.0,
    industries TEXT[],
    warehouse_types TEXT[],
    highways TEXT[],
    rail_link TEXT,
    nearest_port TEXT,
    nearest_airport TEXT,
    outbound_cargo TEXT[],
    inbound_cargo TEXT[],
    avg_daily_truck_movements INTEGER,
    peak_hours TEXT[],
    tier INTEGER CHECK (tier IN (1, 2, 3)),
    backhaul_potential NUMERIC CHECK (backhaul_potential BETWEEN 0 AND 10),
    data_confidence TEXT CHECK (data_confidence IN ('high', 'medium', 'low')),
    last_updated TIMESTAMPTZ DEFAULT now(),
    idempotency_key TEXT UNIQUE,
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english',
            coalesce(array_to_string(industries, ' '), '') || ' ' ||
            coalesce(array_to_string(outbound_cargo, ' '), '') || ' ' ||
            coalesce(array_to_string(inbound_cargo, ' '), '')
        )
    ) STORED,
    UNIQUE (city, cluster_name)
);

CREATE INDEX idx_warehouse_clusters_geom
ON warehouse_clusters USING GIST (geom);

CREATE INDEX idx_warehouse_clusters_search
ON warehouse_clusters USING GIN (search_vector);

CREATE INDEX idx_warehouse_clusters_tier_backhaul
ON warehouse_clusters (tier, backhaul_potential DESC)
WHERE data_confidence IN ('high', 'medium');
```

---

# 6. Query: Find Cluster-Based Triangle Candidates

Given a completed trip:

```text
Cluster A -> Cluster B
```

Find:

```text
Cluster B -> Cluster C -> Cluster A
```

## Corrected Query Pattern

```sql
WITH completed_trip AS (
    SELECT
        a.cluster_id AS cluster_a_id,
        b.cluster_id AS cluster_b_id,
        a.cluster_name AS cluster_a,
        b.cluster_name AS cluster_b,
        a.city AS city_a,
        b.city AS city_b,
        a.geom AS geom_a,
        b.geom AS geom_b,
        a.outbound_cargo AS cargo_from_a,
        b.inbound_cargo AS cargo_to_b
    FROM warehouse_clusters a
    CROSS JOIN warehouse_clusters b
    WHERE a.cluster_name = 'Tiruppur Export ICD / Avinashi Road Belt'
      AND b.cluster_name = 'Madhavaram Logistics Hub'
),
candidate_clusters AS (
    SELECT
        wc.*,
        ST_Distance(wc.geom, ct.geom_a) / 1000 AS km_to_a,
        ST_Distance(wc.geom, ct.geom_b) / 1000 AS km_from_b
    FROM warehouse_clusters wc
    CROSS JOIN completed_trip ct
    WHERE wc.cluster_id NOT IN (ct.cluster_a_id, ct.cluster_b_id)
      AND wc.tier IN (2, 3)
      AND wc.data_confidence IN ('high', 'medium')
      AND wc.backhaul_potential >= 6
      AND (
          ST_DWithin(wc.geom, ct.geom_a, 150000)
          OR ST_DWithin(wc.geom, ct.geom_b, 150000)
      )
)
SELECT
    cc.cluster_name AS candidate_cluster_c,
    cc.city AS city_c,
    cc.industries,
    cc.outbound_cargo,
    cc.inbound_cargo,
    cc.backhaul_potential,
    cc.avg_daily_truck_movements,
    cc.km_from_b,
    cc.km_to_a,
    ROUND(
        (cc.backhaul_potential * 0.40)
        + (
            CASE
                WHEN cc.inbound_cargo && (SELECT cargo_to_b FROM completed_trip) THEN 2
                WHEN cc.outbound_cargo && (SELECT cargo_from_a FROM completed_trip) THEN 1
                ELSE 0
            END * 0.30
        )
        + (
            CASE WHEN cc.km_to_a < 50 THEN 2 ELSE 0 END * 0.20
        )
        + (LEAST(coalesce(cc.avg_daily_truck_movements, 0), 1000) / 1000.0 * 10 * 0.10),
        2
    ) AS cluster_triangle_score
FROM candidate_clusters cc
ORDER BY cluster_triangle_score DESC, cc.km_to_a ASC
LIMIT 5;
```

## Query Logic

```text
Find C near A or B.
Prioritize Tier 2/3 clusters.
Require medium/high confidence.
Require backhaul potential >= 6.
Score by backhaul potential, cargo compatibility, proximity, and truck movement signal.
```

---

# 7. Cluster-Based n8n Workflow

## Workflow Name

```text
WF_BACKHAUL_02_cluster_triangle_recommendation
```

## Trigger

```text
trip_completed_at_cluster_b
```

## Steps

```text
1. Receive trip completion event from TMS.
2. Identify cluster A and cluster B.
3. Check direct return lane/cluster strength B -> A.
4. If direct return is weak, run cluster candidate query.
5. Score cluster C candidates.
6. Check guardrails:
   - wait time at C
   - vehicle compatibility
   - payment reliability
   - cargo compatibility
   - data confidence
7. Recommend B -> C -> A if score passes.
8. Escalate to dispatcher if confidence is low.
9. Log recommendation.
10. Update cluster backhaul potential after actual outcome.
```

## Output Example

```json
{
  "recommendation": "cluster_triangle_route",
  "route": "Madhavaram Logistics Hub -> SIPCOT Irugur -> Tiruppur Export ICD",
  "cluster_triangle_score": 82,
  "expected_revenue_lift_pct": 24,
  "expected_empty_km_reduction_pct": 65,
  "guardrail_status": "human_review_required",
  "reason_codes": [
    "direct_return_weak",
    "tier2_cluster_near_origin",
    "cargo_compatible",
    "high_backhaul_potential"
  ]
}
```

---

# 8. Data Collection Checklist

| Data Point | Source | MVP Method | Later Automation |
| --- | --- | --- | --- |
| cluster boundaries | Google Maps, industrial park maps, field visit | manual polygon/point estimate | GIS import |
| warehouse capacity | transporter interviews, brokers | structured notes | partner records |
| daily truck movements | interviews, toll proxy, field observation | estimate range | API / sensor / toll data if available |
| cargo type mapping | MSME interviews, IndiaMART, field | manual tagging | NLP extraction after permission |
| peak hours | drivers, gate observation | field note | GPS/geofence logs |
| backhaul potential | reverse lane observations | scoring | automated update from trips |
| connectivity metadata | NHAI, rail, ports, maps | desk research | parser/API later |

## Rule

```text
For MVP, manually validate cluster data.
Do not depend on unverified scraper pipelines.
```

---

# 9. Cluster-Level Scoring

Use the same corridor formula, but at cluster level.

```text
Cluster Corridor Score =
0.30 x Volume Score
+ 0.25 x Margin Potential
+ 0.20 x Backhaul Potential
+ 0.15 x Tier 2/3 Advantage
+ 0.10 x Industry Fragmentation
```

## Cluster Triangle Score

```text
Cluster Triangle Score =
0.30 x Backhaul Potential
+ 0.25 x Cargo Compatibility
+ 0.20 x Proximity / Detour Efficiency
+ 0.15 x Truck Movement Signal
+ 0.10 x Payment Reliability
```

## Guardrail

```text
If data_confidence = low,
do not auto-recommend.
Escalate to human validation.
```

---

# 10. Obsidian Dashboard Queries

## High-Potential Warehouse Clusters

```dataview
TABLE city, cluster_name, industries, backhaul_potential, data_confidence, status
FROM "09_Market_Intelligence/Warehouse_Clusters"
WHERE type = "warehouse_cluster" AND backhaul_potential >= 6
SORT backhaul_potential DESC
```

## Low-Confidence Clusters Needing Validation

```dataview
TABLE city, cluster_name, industries, backhaul_potential, last_updated
FROM "09_Market_Intelligence/Warehouse_Clusters"
WHERE type = "warehouse_cluster" AND data_confidence = "low"
SORT city ASC
```

## Cluster Triangle Candidates

```dataview
TABLE city, cluster_name, outbound_cargo, inbound_cargo, backhaul_potential, data_confidence
FROM "09_Market_Intelligence/Warehouse_Clusters"
WHERE type = "warehouse_cluster" AND contains(tags, "triangle-candidate")
SORT backhaul_potential DESC
```

---

# 11. Immediate MVP Action

## Start With 3 Clusters

```text
Tiruppur Export ICD / Avinashi Road Belt
SIPCOT Irugur / East Coimbatore
Madhavaram Logistics Hub
```

## First Cluster Triangle

```text
Tiruppur Export ICD / Avinashi Road Belt
-> Madhavaram Logistics Hub
-> SIPCOT Irugur / East Coimbatore
-> Tiruppur Export ICD / Avinashi Road Belt
```

## Measure

```text
empty km reduction
revenue per vehicle day
wait time at Madhavaram
wait time at SIPCOT Irugur
cargo compatibility
payment reliability
```

---

# Final Takeaway

The next level of your system is not city intelligence.

It is cluster intelligence.

```text
City pair = market map
Directed lane = demand imbalance
Triangle route = return strategy
Warehouse cluster = operational pickup/drop reality
```

The moat becomes:

```text
cluster-aware continuous-load routing for South India MSME freight
```

That is more defensible than a simple return-load board.

---

# Related Notes

- [[Deadhead Reduction Intelligence Layer for Tier 2-3 Freight]]
- [[Triangle Route Engine for Return Trip Optimization]]
- [[South India Trading Pair City Research System]]
- [[Directed Lane Master]]
- [[Triangle Route Master]]
