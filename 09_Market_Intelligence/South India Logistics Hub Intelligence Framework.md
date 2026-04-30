---
title: South India Logistics Hub Intelligence Framework
type: market-intelligence-framework
category: logistics-hub-intelligence
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - logistics-hubs
  - multimodal
  - triangle-route
  - deadhead
  - south-india
  - postgis
related:
  - South India Warehouse and Industrial Cluster Intelligence Framework
  - Warehouse Placement Strategy for Triangle Backhaul Optimization
  - Deadhead Reduction Intelligence Layer for Tier 2-3 Freight
  - Triangle Route Engine for Return Trip Optimization
  - Directed Lane Master
  - Triangle Route Master
---

# South India Logistics Hub Intelligence Framework

## Core Idea

Logistics hubs are not just warehouses near cities.

They are strategic connectivity nodes where:

- outbound volume
- inbound return potential
- highway access
- rail/port/airport links
- warehouse capacity
- truck parking
- cargo compatibility
- triangle route feasibility

come together.

## Core Principle

```text
Hub-centric routing beats city-centric routing.
```

Do not only match:

```text
Chennai -> Coimbatore
```

Match:

```text
Madhavaram Logistics Hub -> SIPCOT Irugur via NH544 / NH network
```

City pair tells you the market.

Directed lane tells you the imbalance.

Warehouse cluster tells you pickup/drop reality.

Logistics hub tells you whether the route can scale.

---

# 1. Hub vs Warehouse Cluster

| Object | Meaning | Example |
| --- | --- | --- |
| City | broad market node | Chennai |
| City pair | trading relationship | Chennai <-> Coimbatore |
| Directed lane | one-way demand | Chennai -> Coimbatore |
| Warehouse cluster | local pickup/drop zone | Madhavaram warehouse belt |
| Logistics hub | connectivity and consolidation node | Madhavaram Logistics Hub with highway, port, warehouse, truck flows |

## Rule

```text
Use warehouse clusters for operations.
Use logistics hubs for network design.
```

---

# 2. Logistics Hub Data Object

```yaml
type: logistics_hub
name:
city:
tier:
coordinates:
  lat:
  lng:
radius_km:
hub_type:
  - port_gateway
  - cross_dock
  - grade_a_warehousing
  - truck_terminal
  - icd_cfs
connectivity:
  highways:
    -
  rail_links:
    -
  port_links:
    -
  airport_links:
    -
cargo_profile:
  inbound:
    -
  outbound:
    -
avg_daily_truck_movements:
peak_hours:
  -
backhaul_potential:
triangle_feasibility_score:
data_confidence:
last_updated:
idempotency_key:
status:
```

## Directional Cargo Rule

```text
Store inbound_cargo and outbound_cargo separately.
```

Because hub direction matters.

---

# 3. Tier 1 Anchor Logistics Hubs

## Chennai Metropolitan Logistics Corridor

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Madhavaram Logistics Hub | North Chennai / NH16 side | Grade-A, cross-dock, e-commerce, FMCG | NH16, Chennai port links, airport access | primary origin/return-origin for TN/KL/AP routes |
| Sriperumbudur Logistics Belt | Southwest Chennai | bonded, JIT, auto-OEM linked | NH48, port connectivity, industrial belt | high-volume outbound to Tier 2/3 clusters |
| Ennore/Kattupalli Port Zone | North Chennai coastal | port-linked, hazmat, reefer | port, NH16, coastal access | coastal triangle anchor |
| Ambattur Industrial Logistics | Northwest Chennai | SME, engineering, cross-dock | NH48, industrial estate links | feeder for Coimbatore/Tiruppur loops |

## Visakhapatnam Port Logistics Hub

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Vizag Port / Industrial Logistics | Visakhapatnam port belt | bonded, reefer, hazmat, container | port, NH16, East Coast rail | AP coastal triangle anchor |
| Gajuwaka Industrial Logistics | Vizag outskirts | industrial, agri/seafood, cross-dock | NH16, airport, rail sidings | inland connector for Vijayawada/Guntur |
| Pendurthi Logistics Node | Vizag junction side | truck terminal, multimodal | NH16/NH26 style connectivity, rail access | feeder for coastal closure |

## Kochi Port + Infopark Logistics Corridor

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Kochi Port / Willingdon Island | Kochi port belt | bonded, reefer, spice/seafood | port, NH66, airport | Kerala-TN cross-border anchor |
| Kakkanad / Infopark-SmartCity | Kochi | tech-enabled, Grade-A, high-value cargo | city/airport/highway access | high-value cargo to Coimbatore/TN |
| Aluva Logistics Node | Kochi outskirts | agri/spice, cross-dock, truck terminal | highway, rail, airport access | feeder to Coimbatore/Palakkad/Tiruppur |

## Bengaluru Peripheral Logistics Belt

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Dobbaspet Logistics Park | North Bengaluru / NH44 side | Grade-A, e-commerce, automation-ready | NH44, airport-region access | KA interior origin |
| Hosur Industrial Logistics Corridor | TN-KA border | JIT, ESD-safe, EV/auto-linked | NH44, Chennai-Bengaluru corridor | cross-border triangle hub |
| Peenya Industrial Logistics | Northwest Bengaluru | SME, engineering, cross-dock | industrial links, highway access | feeder for Coimbatore/Tiruppur lanes |

---

# 4. Tier 2 Regional Connector Hubs

## Coimbatore-Irugur-Sulur Logistics Belt

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| SIPCOT Irugur / East Coimbatore | NH544 side | textile, engineering, cross-dock | NH544, rail, airport | central TN/KL/KA connector |
| Sulur / East Coimbatore Logistics Node | Coimbatore periphery | truck staging, industrial | NH544 / airport side | feeder to Tiruppur/Erode |
| Peelamedu-Singanallur Textile Logistics | Coimbatore city belt | yarn/garment, dry storage | city/rail/highway access | origin hub for Chennai export triangles |

## Tiruppur Export Logistics Zone

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Tiruppur Export ICD / Avinashi Road | Tiruppur | export-compliant, hanging/carton storage | road, rail, Coimbatore airport | primary origin for Chennai port lanes |
| Dyeing Zone Logistics Node | Tiruppur belt | chemical/dyeing support | local trucking, compliance needs | return-leg input demand |
| Packaging and Trims Logistics Hub | Tiruppur periphery | SME, flatbed, cross-dock | local feeder links | short feeder to Coimbatore/Erode |

## Salem-Erode Corridor Logistics Nodes

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Salem Steel / Foundry Logistics | Salem | heavy-load, flatbed | NH44, rail, industrial links | industrial input source |
| Erode Textile Logistics Belt | Erode | yarn/fabric, dry storage | NH544, rail, local truck terminals | feeder to Coimbatore/Chennai |
| Perundurai Agri-Mandi Logistics | Erode district | agri, ventilated/cold storage | highway/mandi links | seasonal cargo source |

## Madurai-Trichy-Karur Triangle Logistics

| Hub | Location | Hub Type | Key Connectivity | Triangle Role |
| --- | --- | --- | --- | --- |
| Madurai Industrial / ELCOT Logistics | Madurai | SME, agri, distribution | NH44, rail, airport | southern TN redistribution |
| Trichy BHEL / Heavy Engineering Zone | Trichy | heavy-load, project cargo | NH links, rail, airport | central TN closure hub |
| Karur Home Textiles Logistics | Karur | dry/export, flatbed | NH38 style corridor, rail | feeder for Coimbatore/Erode/Trichy |

---

# 5. Tier 3 Feeder Nodes

| Hub | City | Hub Type | Triangle Role |
| --- | --- | --- | --- |
| Namakkal Truck Body / Logistics Cluster | Namakkal | truck body, oversize, staging | return-leg optimizer for Chennai/Bengaluru/TN loops |
| Sri City Integrated Logistics | Sri City | Grade-A, JIT, bonded, auto/EV | AP-TN cross-border Chennai/Bengaluru triangle node |
| Vijayawada Agri / Distribution Hub | Vijayawada | agri, FMCG, cross-dock | Vizag inland connector |
| Guntur Spice / Agri Logistics | Guntur | chilli, turmeric, dry storage | AP seasonal cargo feeder |
| Palakkad Industrial Gateway | Palakkad | Kerala-TN feeder, dry/cross-dock | Kochi-Coimbatore connector |

---

# 6. Top 7 Logistics Hubs For Triangle Validation

Start with three, but track seven.

| Priority | Hub | City | Tier | Why Start Here | Expected Triangle Impact |
| ---: | --- | --- | ---: | --- | --- |
| 1 | Madhavaram Logistics Hub | Chennai | 1 | metro/port/FMCG anchor, weak direct return hypotheses to Tier 2/3 | high via Coimbatore/Sri City triangles |
| 2 | SIPCOT Irugur / East Coimbatore | Coimbatore | 2 | central connector for TN/KL/KA | high via Erode/Karur/Salem feeder loops |
| 3 | Tiruppur Export ICD / Avinashi Road | Tiruppur | 2 | garment export origin, Chennai port lane | very high via Coimbatore closure |
| 4 | Vizag Port / Industrial Logistics | Vizag | 1/2 | east coast port anchor | high via Vijayawada/Guntur |
| 5 | Sri City Integrated Logistics | Sri City | 2 | AP-TN border auto/EV hub | high via Chennai/Bengaluru |
| 6 | Kochi Port / Willingdon Island | Kochi | 1/2 | Kerala-TN port/cross-border anchor | medium/high via Coimbatore/Tiruppur |
| 7 | Dobbaspet Logistics Park | Bengaluru | 1 | tech/retail distribution anchor | medium/high via Hosur/Namakkal/Coimbatore |

## First 3 Hubs

```text
Madhavaram Logistics Hub
SIPCOT Irugur / East Coimbatore
Tiruppur Export ICD / Avinashi Road
```

---

# 7. PostGIS Schema: logistics_hubs

Use this as a draft schema separate from warehouse_clusters if you want hubs to represent broader connectivity zones.

```sql
CREATE TABLE logistics_hubs (
    hub_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    city_id UUID REFERENCES city_nodes(city_id),
    tier INTEGER CHECK (tier IN (1, 2, 3)),
    geom GEOGRAPHY(Point, 4326) NOT NULL,
    radius_km NUMERIC DEFAULT 12.0,
    hub_type TEXT[],
    highways TEXT[],
    rail_links TEXT[],
    port_links TEXT[],
    airport_links TEXT[],
    inbound_cargo TEXT[],
    outbound_cargo TEXT[],
    avg_daily_truck_movements INTEGER,
    peak_hours TEXT[],
    backhaul_potential NUMERIC CHECK (backhaul_potential BETWEEN 0 AND 10),
    triangle_feasibility_score NUMERIC CHECK (triangle_feasibility_score BETWEEN 0 AND 100),
    data_confidence TEXT CHECK (data_confidence IN ('high', 'medium', 'low')),
    last_updated TIMESTAMPTZ DEFAULT now(),
    idempotency_key TEXT UNIQUE,
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english',
            coalesce(array_to_string(hub_type, ' '), '') || ' ' ||
            coalesce(array_to_string(inbound_cargo, ' '), '') || ' ' ||
            coalesce(array_to_string(outbound_cargo, ' '), '')
        )
    ) STORED,
    UNIQUE (city, name)
);

CREATE INDEX idx_logistics_hubs_geom
ON logistics_hubs USING GIST (geom);

CREATE INDEX idx_logistics_hubs_search
ON logistics_hubs USING GIN (search_vector);

CREATE INDEX idx_logistics_hubs_tier_backhaul
ON logistics_hubs (tier, backhaul_potential DESC, triangle_feasibility_score DESC)
WHERE data_confidence IN ('high', 'medium');
```

---

# 8. Query: Find Optimal Hub For Triangle Closure

Given a weak return lane:

```text
B -> A
```

Find hub C for:

```text
B -> C -> A
```

```sql
WITH weak_return AS (
    SELECT
        b.city_id AS city_b_id,
        a.city_id AS city_a_id,
        b.name AS city_b,
        a.name AS city_a,
        b.geom AS geom_b,
        a.geom AS geom_a,
        dl.backhaul_score
    FROM directed_lanes dl
    JOIN city_nodes b ON b.city_id = dl.origin_city_id
    JOIN city_nodes a ON a.city_id = dl.destination_city_id
    WHERE b.name = 'Chennai'
      AND a.name = 'Tiruppur'
      AND dl.backhaul_score < 5
),
candidate_hubs AS (
    SELECT
        lh.*,
        ST_Distance(lh.geom, wr.geom_b) / 1000 AS km_from_b,
        ST_Distance(lh.geom, wr.geom_a) / 1000 AS km_to_a
    FROM logistics_hubs lh
    CROSS JOIN weak_return wr
    WHERE lh.city_id NOT IN (wr.city_a_id, wr.city_b_id)
      AND lh.tier IN (2, 3)
      AND lh.backhaul_potential >= 6
      AND lh.triangle_feasibility_score >= 70
      AND lh.data_confidence IN ('high', 'medium')
      AND (
          ST_DWithin(lh.geom, wr.geom_a, 150000)
          OR ST_DWithin(lh.geom, wr.geom_b, 150000)
      )
)
SELECT
    ch.name AS hub_name,
    ch.city,
    ch.hub_type,
    ch.outbound_cargo,
    ch.inbound_cargo,
    ch.backhaul_potential,
    ch.triangle_feasibility_score,
    ch.km_from_b,
    ch.km_to_a,
    ch.highways,
    ch.rail_links,
    ch.port_links
FROM candidate_hubs ch
ORDER BY ch.triangle_feasibility_score DESC,
         ch.backhaul_potential DESC,
         ch.km_to_a ASC
LIMIT 5;
```

---

# 9. Hub-Based n8n Workflow

## Workflow Name

```text
WF_HUB_01_triangle_recommendation
```

## Trigger

```text
trip_completed_at_hub_b
```

## Steps

```text
1. Receive trip completion event from TMS.
2. Identify Hub A and Hub B.
3. Check direct return strength B -> A.
4. If weak, find candidate hubs C within 150 km of A or B.
5. Score hubs by cargo compatibility, backhaul potential, connectivity, and confidence.
6. Apply guardrails:
   - wait time at Hub C
   - vehicle compatibility
   - payment reliability
   - data confidence
7. Recommend B -> C -> A or escalate.
8. Log decision and update hub backhaul potential after actual outcome.
```

## Output Example

```json
{
  "recommendation": "hub_triangle_route",
  "route": "Madhavaram Logistics Hub -> SIPCOT Irugur -> Tiruppur Export ICD",
  "triangle_feasibility_score": 88,
  "expected_revenue_lift_pct": 25,
  "expected_empty_km_reduction_pct": 60,
  "connectivity": {
    "highways": ["NH16", "NH544"],
    "rail_links": ["available_or_validate"],
    "port_links": ["Chennai Port"]
  },
  "guardrail_status": "human_review_required"
}
```

---

# 10. Data Collection Checklist

| Data Point | MVP Source | Later Automation |
| --- | --- | --- |
| hub boundaries | maps, field visits, industrial park documents | GIS import |
| warehouse capacity | transporter/warehouse interviews | partner WMS data |
| truck movements | field estimates, toll proxy, interviews | API/GPS/telematics |
| cargo type mapping | MSME interviews, market observation | NLP extraction after permission |
| peak hours | driver interviews, gate observation | geofence event logs |
| backhaul potential | reverse lane observations | automated trip learning |
| connectivity metadata | NHAI/ports/rail/maps | parser/API later |

## Data Policy

```text
For MVP, validate manually.
Do not rely on unverified scraped/API data.
```

---

# 11. Obsidian Dashboard Queries

## High-Potential Logistics Hubs

```dataview
TABLE city, name, hub_type, backhaul_potential, triangle_feasibility_score, data_confidence, status
FROM "09_Market_Intelligence/Logistics_Hubs"
WHERE type = "logistics_hub" AND triangle_feasibility_score >= 70
SORT triangle_feasibility_score DESC
```

## Low-Confidence Hubs Needing Field Validation

```dataview
TABLE city, name, hub_type, backhaul_potential, last_updated
FROM "09_Market_Intelligence/Logistics_Hubs"
WHERE type = "logistics_hub" AND data_confidence = "low"
SORT city ASC
```

## Port-Linked Hubs

```dataview
TABLE city, name, hub_type, port_links, inbound_cargo, outbound_cargo, status
FROM "09_Market_Intelligence/Logistics_Hubs"
WHERE type = "logistics_hub" AND length(port_links) > 0
SORT city ASC
```

---

# 12. Practical MVP Advice

Start with hub validation, not hub ownership.

## Phase 1

```text
Map hubs manually.
Interview transporters.
Estimate cargo flows.
Track wait time.
Use partner warehouses.
```

## Phase 2

```text
Score hubs.
Run 3 triangle tests.
Compare revenue/day and empty km.
```

## Phase 3

```text
Sign preferred access with useful hubs.
Add gate-in/out logging.
Add DWIS waiting-time scoring.
```

## Phase 4

```text
Only then consider dedicated micro-hub or leased cross-dock.
```

---

# Final Takeaway

The next level after cluster intelligence is hub intelligence.

```text
Warehouse cluster = where freight is handled.
Logistics hub = where freight can be re-routed, consolidated, and connected.
```

The moat becomes:

```text
hub-aware continuous-load routing for South India MSME corridors
```

A normal broker asks:

```text
Where is the return load?
```

Your system asks:

```text
Which hub should this truck move to next so it stays earning?
```

That is a much sharper question.

---

# Related Notes

- [[South India Warehouse and Industrial Cluster Intelligence Framework]]
- [[Warehouse Placement Strategy for Triangle Backhaul Optimization]]
- [[Deadhead Reduction Intelligence Layer for Tier 2-3 Freight]]
- [[Triangle Route Engine for Return Trip Optimization]]
- [[Directed Lane Master]]
- [[Triangle Route Master]]
