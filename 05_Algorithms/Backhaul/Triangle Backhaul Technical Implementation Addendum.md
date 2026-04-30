---
title: Triangle Backhaul Technical Implementation Addendum
type: technical-implementation
category: backhaul-optimization
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - backhaul
  - triangle-route
  - postgis
  - n8n
  - pgrouting
  - data-pipeline
  - guardrails
related:
  - Triangle Route Engine for Return Trip Optimization
  - Triangle Route Master
  - Directed Lane Master
  - South India Trading Pair City Research System
  - TMS Execution Architecture
---

# Triangle Backhaul Technical Implementation Addendum

## Purpose

This note extracts the technically useful parts from the Qwen solution and adapts them to the current project.

The core strategic idea is already captured in the triangle route engine:

```text
If A -> B is strong and B -> A is weak,
search B -> C -> A.
```

This addendum turns that strategy into a technical MVP using:

- Obsidian for human-readable research
- PostgreSQL/PostGIS for spatial lane queries
- directed lane tables for asymmetric demand
- triangle route tables for backhaul candidates
- n8n workflows for scoring automation
- rule-based guardrails before advanced AI
- validation logs before production rollout

Important caveat:

```text
Do not depend on ULIP, GSTN, NHAI, WhatsApp, or marketplace scraping until access, legality, and data permissions are confirmed.
```

For MVP, use manually collected lane observations first.

---

# 1. Valid Qwen Takeaways To Keep

| Qwen Idea | Keep? | Optimized Use In This Project |
| --- | --- | --- |
| Triangle filter | Yes | Core rule for weak return lane detection |
| Directed lane inventory | Yes | Required because freight demand is asymmetric |
| PostGIS candidate-city query | Yes | Useful for finding C cities near A or B |
| 14-day validation protocol | Yes | Strong MVP proof method |
| Go/no-go criteria | Yes | Prevents emotional route launching |
| Guardrails | Yes | Avoids bad AI route recommendations |
| n8n workflow | Yes | Good orchestration layer for MVP automation |
| GLM/LLM parsing | Later | Use only after source permissions and data quality exist |
| Autoclaw scraping | Later | Legal/access review required before scraping |
| PGVector semantic matching | Later | Useful after enough load-post text exists |
| PyVRP/pgRouting | Later | Useful after rule-based scoring works |

## Biggest Technical Upgrade

The best takeaway is not a model name.

It is this data structure:

```text
city_nodes
+ directed_lanes
+ triangle_routes
+ lane_observations
+ triangle_validation_runs
```

That is the technical skeleton.

---

# 2. MVP Data Architecture

## Database Objects

| Table | Purpose |
| --- | --- |
| city_nodes | cities, coordinates, tier, cluster tags |
| directed_lanes | one-way lane strength and economics |
| lane_observations | daily load/rate/wait/payment observations |
| triangle_routes | candidate A -> B -> C -> A loops |
| triangle_validation_runs | 14-day experiment metrics |
| triangle_decision_logs | audit trail for recommendation decisions |

## Rule

```text
Obsidian explains why.
PostgreSQL stores what.
PostGIS finds where.
n8n runs when.
```

---

# 3. PostgreSQL + PostGIS Schema Draft

Use this as a product-facing schema draft, not final production DDL.

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE city_nodes (
    city_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    state TEXT NOT NULL,
    tier INTEGER,
    region TEXT DEFAULT 'South India',
    geom GEOGRAPHY(Point, 4326),
    cluster_tags TEXT[],
    primary_industries TEXT[],
    freight_role TEXT[],
    priority_score NUMERIC,
    data_confidence TEXT CHECK (data_confidence IN ('low', 'medium', 'high')) DEFAULT 'low',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_city_nodes_geom ON city_nodes USING GIST (geom);
CREATE INDEX idx_city_nodes_tier ON city_nodes (tier);
CREATE INDEX idx_city_nodes_cluster_tags ON city_nodes USING GIN (cluster_tags);
```

```sql
CREATE TABLE directed_lanes (
    lane_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    origin_city_id UUID NOT NULL REFERENCES city_nodes(city_id),
    destination_city_id UUID NOT NULL REFERENCES city_nodes(city_id),
    distance_km NUMERIC,
    primary_cargo TEXT[],
    vehicle_types TEXT[],
    best_mode TEXT,
    lane_strength TEXT CHECK (lane_strength IN ('strong', 'medium', 'weak')),
    load_frequency_score NUMERIC CHECK (load_frequency_score BETWEEN 0 AND 10),
    rate_score NUMERIC CHECK (rate_score BETWEEN 0 AND 10),
    backhaul_score NUMERIC CHECK (backhaul_score BETWEEN 0 AND 10),
    margin_score NUMERIC CHECK (margin_score BETWEEN 0 AND 10),
    payment_reliability_score NUMERIC CHECK (payment_reliability_score BETWEEN 0 AND 10),
    demurrage_risk_score NUMERIC CHECK (demurrage_risk_score BETWEEN 0 AND 10),
    triangle_candidate BOOLEAN DEFAULT false,
    nearby_substitute_city_id UUID REFERENCES city_nodes(city_id),
    data_confidence TEXT CHECK (data_confidence IN ('low', 'medium', 'high')) DEFAULT 'low',
    status TEXT CHECK (status IN ('watchlist', 'validate', 'active', 'archived')) DEFAULT 'validate',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (origin_city_id, destination_city_id)
);

CREATE INDEX idx_directed_lanes_origin ON directed_lanes (origin_city_id);
CREATE INDEX idx_directed_lanes_destination ON directed_lanes (destination_city_id);
CREATE INDEX idx_directed_lanes_scores ON directed_lanes (backhaul_score, load_frequency_score, rate_score);
CREATE INDEX idx_directed_lanes_triangle_candidate ON directed_lanes (triangle_candidate);
```

```sql
CREATE TABLE lane_observations (
    observation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_id UUID NOT NULL REFERENCES directed_lanes(lane_id),
    observation_date DATE NOT NULL,
    source_type TEXT CHECK (source_type IN ('official', 'association', 'field', 'whatsapp', 'interview', 'estimate', 'shipment_data')),
    load_posts_count INTEGER,
    quoted_rate_per_km NUMERIC,
    quoted_rate_total NUMERIC,
    average_wait_hours NUMERIC,
    vehicle_type TEXT,
    cargo_type TEXT,
    payment_terms TEXT,
    payment_reliability_score NUMERIC CHECK (payment_reliability_score BETWEEN 0 AND 10),
    notes TEXT,
    confidence TEXT CHECK (confidence IN ('low', 'medium', 'high')) DEFAULT 'low',
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (lane_id, observation_date, source_type, vehicle_type, cargo_type)
);

CREATE INDEX idx_lane_observations_lane_date ON lane_observations (lane_id, observation_date);
CREATE INDEX idx_lane_observations_source ON lane_observations (source_type);
```

```sql
CREATE TABLE triangle_routes (
    triangle_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    city_a_id UUID NOT NULL REFERENCES city_nodes(city_id),
    city_b_id UUID NOT NULL REFERENCES city_nodes(city_id),
    city_c_id UUID NOT NULL REFERENCES city_nodes(city_id),
    primary_lane_id UUID REFERENCES directed_lanes(lane_id),
    weak_return_lane_id UUID REFERENCES directed_lanes(lane_id),
    substitute_leg_1_id UUID REFERENCES directed_lanes(lane_id),
    substitute_leg_2_id UUID REFERENCES directed_lanes(lane_id),
    vehicle_types TEXT[],
    target_industries TEXT[],
    expected_empty_km_reduction NUMERIC,
    expected_revenue_gain_pct NUMERIC,
    time_penalty_hours NUMERIC,
    triangle_score NUMERIC CHECK (triangle_score BETWEEN 0 AND 100),
    status TEXT CHECK (status IN ('watchlist', 'validate', 'active', 'archived', 'rejected')) DEFAULT 'validate',
    data_confidence TEXT CHECK (data_confidence IN ('low', 'medium', 'high')) DEFAULT 'low',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    CHECK (city_a_id <> city_b_id AND city_b_id <> city_c_id AND city_a_id <> city_c_id)
);

CREATE INDEX idx_triangle_routes_score ON triangle_routes (triangle_score DESC);
CREATE INDEX idx_triangle_routes_status ON triangle_routes (status);
```

```sql
CREATE TABLE triangle_validation_runs (
    validation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    triangle_id UUID NOT NULL REFERENCES triangle_routes(triangle_id),
    validation_start DATE NOT NULL,
    validation_end DATE NOT NULL,
    direct_return_loads_per_day NUMERIC,
    substitute_leg_1_loads_per_day NUMERIC,
    substitute_leg_2_loads_per_day NUMERIC,
    direct_revenue_per_vehicle_day NUMERIC,
    triangle_revenue_per_vehicle_day NUMERIC,
    revenue_gain_pct NUMERIC,
    direct_empty_km NUMERIC,
    triangle_empty_km NUMERIC,
    empty_km_reduction_pct NUMERIC,
    driver_acceptance_pct NUMERIC,
    payment_reliability_min NUMERIC,
    cycle_time_hours NUMERIC,
    recommendation TEXT CHECK (recommendation IN ('approve', 'iterate', 'reject')),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

```sql
CREATE TABLE triangle_decision_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    triangle_id UUID REFERENCES triangle_routes(triangle_id),
    vehicle_id TEXT,
    current_city_id UUID REFERENCES city_nodes(city_id),
    home_city_id UUID REFERENCES city_nodes(city_id),
    decision TEXT CHECK (decision IN ('direct_return', 'triangle_route', 'wait', 'escalate', 'reject')),
    reason_codes TEXT[],
    input_snapshot JSONB,
    score_snapshot JSONB,
    human_override BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_triangle_decision_logs_created ON triangle_decision_logs (created_at);
CREATE INDEX idx_triangle_decision_logs_decision ON triangle_decision_logs (decision);
```

---

# 4. Candidate City Query

Use this to find candidate city C for a weak return lane B -> A.

## Corrected PostGIS Query

```sql
WITH weak_lane AS (
    SELECT
        dl.lane_id,
        origin.name AS city_b,
        destination.name AS city_a,
        dl.origin_city_id AS city_b_id,
        dl.destination_city_id AS city_a_id,
        origin.geom AS city_b_geom,
        destination.geom AS city_a_geom,
        dl.backhaul_score
    FROM directed_lanes dl
    JOIN city_nodes origin ON origin.city_id = dl.origin_city_id
    JOIN city_nodes destination ON destination.city_id = dl.destination_city_id
    WHERE origin.name = 'Chennai'
      AND destination.name = 'Tiruppur'
      AND dl.backhaul_score < 5
),
candidate_cities AS (
    SELECT
        c.city_id,
        c.name,
        c.geom,
        ST_Distance(c.geom, w.city_a_geom) / 1000 AS km_from_a,
        ST_Distance(c.geom, w.city_b_geom) / 1000 AS km_from_b
    FROM city_nodes c
    CROSS JOIN weak_lane w
    WHERE c.city_id NOT IN (w.city_a_id, w.city_b_id)
      AND c.tier IN (2, 3)
      AND (
          ST_DWithin(c.geom, w.city_a_geom, 150000)
          OR ST_DWithin(c.geom, w.city_b_geom, 150000)
      )
)
SELECT
    cc.name AS candidate_c,
    dl_bc.load_frequency_score AS score_b_c,
    dl_ca.load_frequency_score AS score_c_a,
    dl_bc.rate_score AS rate_b_c,
    dl_ca.rate_score AS rate_c_a,
    dl_bc.distance_km + dl_ca.distance_km AS triangle_distance_km,
    (dl_bc.load_frequency_score + dl_ca.load_frequency_score) AS combined_strength,
    cc.km_from_a,
    cc.km_from_b
FROM candidate_cities cc
CROSS JOIN weak_lane w
LEFT JOIN directed_lanes dl_bc
    ON dl_bc.origin_city_id = w.city_b_id
   AND dl_bc.destination_city_id = cc.city_id
LEFT JOIN directed_lanes dl_ca
    ON dl_ca.origin_city_id = cc.city_id
   AND dl_ca.destination_city_id = w.city_a_id
WHERE dl_bc.load_frequency_score >= 6
  AND dl_ca.load_frequency_score >= 5
ORDER BY combined_strength DESC, triangle_distance_km ASC
LIMIT 5;
```

## Query Logic

```text
Weak lane = B -> A
Candidate C must be near A or B
B -> C must be strong enough
C -> A must be strong enough
Rank by combined strength and shorter triangle distance
```

---

# 5. Triangle Scoring Function

Use this first as application logic or SQL view.

```text
Triangle Score =
0.25 x Revenue Gain Score
+ 0.25 x Empty Km Reduction Score
+ 0.20 x Load Probability Score
+ 0.15 x Time Feasibility Score
+ 0.10 x Vehicle Compatibility Score
+ 0.05 x Payment Reliability Score
```

## Score Inputs

| Score | Calculation Direction |
| --- | --- |
| Revenue Gain | triangle revenue per day vs direct revenue per day |
| Empty Km Reduction | direct empty km minus triangle empty km |
| Load Probability | average load availability for B -> C and C -> A |
| Time Feasibility | full cycle within allowed operating window |
| Vehicle Compatibility | one vehicle can serve all legs safely |
| Payment Reliability | minimum shipper/payment score across legs |

## Decision Thresholds

| Score | Decision |
| ---: | --- |
| 85-100 | approve / launch |
| 70-84 | validate |
| 55-69 | watchlist |
| below 55 | reject |

---

# 6. Guardrails

The technical system should refuse clever but bad routes.

## Auto-Reject If

```text
payment_reliability < 50 on any leg
vehicle compatibility fails
cycle time > 60 hours for short/medium regional loop
expected wait at C > 12 hours without premium revenue
cargo compatibility fails
cold-chain cargo lacks cold-chain vehicle and monitoring
driver hours unsafe
route requires unverified partner
```

## Escalate To Human If

```text
triangle_score between 55 and 70
payment score between 50 and 60
wait time forecast between 8 and 12 hours
new shipper or new pickup point involved
high cargo value involved
route includes port/CFS/document risk
```

## Auto-Approve Only If

```text
triangle_score >= 85
payment reliability >= 70 on all legs
vehicle compatibility is clean
cycle time within target
no active dispute history on shippers
load availability confirmed
```

---

# 7. n8n Workflow Draft

## Workflow Name

```text
WF_BACKHAUL_01_triangle_recommendation
```

## Trigger

```text
trip_completed
or
vehicle_available_at_destination
```

## Workflow Steps

```text
1. Receive trip completion event from TMS.
2. Read current city B and home/origin city A.
3. Query directed_lanes for B -> A.
4. If B -> A strength is good, recommend direct return.
5. If B -> A backhaul_score < 5, run candidate-city query.
6. Generate B -> C -> A candidates.
7. Score each triangle candidate.
8. Apply guardrails.
9. If approved, notify dispatcher with recommended triangle.
10. If uncertain, create human review task.
11. Log decision to triangle_decision_logs.
12. Update Obsidian triangle route note manually or through controlled sync.
```

## Event Input

```json
{
  "event": "vehicle_available_at_destination",
  "vehicle_id": "VEH-001",
  "driver_id": "DRV-001",
  "last_order_id": "ORD-001",
  "current_city": "Chennai",
  "home_cluster": "Tiruppur",
  "vehicle_type": "20ft_closed_body",
  "available_from": "2026-04-30T18:00:00+05:30",
  "max_wait_hours": 12
}
```

## Recommendation Output

```json
{
  "recommendation": "triangle_route",
  "route": "Chennai -> Coimbatore -> Tiruppur",
  "triangle_score": 82,
  "expected_revenue_gain_pct": 22,
  "expected_empty_km_reduction_pct": 70,
  "guardrail_status": "passed",
  "reason_codes": [
    "direct_return_weak",
    "substitute_leg_available",
    "feeder_leg_short",
    "revenue_per_vehicle_day_positive"
  ],
  "requires_human_approval": true
}
```

---

# 8. 14-Day Validation Protocol

## Daily Metrics

| Metric | Why It Matters |
| --- | --- |
| direct return load count | measures B -> A weakness |
| substitute B -> C load count | measures triangle leg 1 availability |
| feeder C -> A load count | measures triangle leg 2 availability |
| rate/km | revenue quality |
| wait hours | time cost |
| empty km | utilization |
| driver acceptance | operational realism |
| payment terms | cash-flow risk |

## Go / No-Go Criteria

Approve if:

```text
Revenue per vehicle day improves by >= 15 percent
AND empty km reduction >= 50 percent
AND driver acceptance >= 80 percent
AND payment reliability >= 60 on every leg
```

Iterate if:

```text
Revenue improvement = 10-15 percent
OR one leg has load availability below 3/day
OR wait hours are higher than expected but manageable
```

Reject if:

```text
Revenue improvement < 10 percent
OR cycle time > 60 hours
OR payment reliability < 50 on any leg
OR vehicle/cargo compatibility repeatedly fails
```

---

# 9. Phase Checklist

## Phase 1: Desktop Research

```text
Goal: seed the database with reliable starting assumptions.
```

Tasks:

- [ ] Confirm 25 target cities with coordinates.
- [ ] Tag each city by cluster type: textile, agri, auto, port, FMCG, pharma.
- [ ] Create 25-30 directed lanes.
- [ ] Mark lanes with backhaul_score < 5 as triangle candidates.
- [ ] Seed at least 5 triangle routes.
- [ ] Record data confidence for every lane.
- [ ] Build the first lane strength matrix.

Exit criteria:

- [ ] 25 directed lanes scored.
- [ ] 5 triangle candidates identified.
- [ ] 3 triangles selected for 14-day validation.

---

## Phase 2: Field Validation

Tasks:

- [ ] Track load posts for target lanes for 14 days.
- [ ] Collect rate/km for each leg.
- [ ] Interview transporters.
- [ ] Interview drivers.
- [ ] Capture payment terms.
- [ ] Estimate waiting time.
- [ ] Compare direct vs triangle revenue per vehicle day.

Exit criteria:

- [ ] Revenue/day delta calculated.
- [ ] Empty-km delta calculated.
- [ ] Driver acceptance measured.
- [ ] Go/no-go decision made.

---

## Phase 3: Automation MVP

Tasks:

- [ ] Create PostGIS schema.
- [ ] Insert city nodes and directed lanes.
- [ ] Implement candidate-city SQL query.
- [ ] Implement scoring function.
- [ ] Create n8n workflow skeleton.
- [ ] Log decisions.
- [ ] Keep human approval for all recommendations.

Exit criteria:

- [ ] Dispatcher can receive recommendation after trip completion.
- [ ] Every recommendation has score and reason codes.
- [ ] Every recommendation can be audited.

---

# 10. What To Delay

Delay these until the rule-based engine works:

- live ULIP/GSTN integration
- automated scraping of restricted sites
- WhatsApp ingestion without consent and privacy rules
- PGVector semantic load matching
- PyVRP fleet-wide optimization
- reinforcement learning
- fully automated driver dispatch

## Reason

```text
The first bottleneck is not AI.
The first bottleneck is clean lane data.
```

Do not summon the optimization dragon before the map has roads.

---

# 11. Immediate Next Actions

## This Week

```text
1. Seed city_nodes for the first 10 cities.
2. Seed directed_lanes for the first 20 lanes.
3. Add 3 triangle_routes.
4. Run the candidate-city query for Chennai -> Tiruppur.
5. Start the 14-day validation for Tiruppur -> Chennai -> Coimbatore -> Tiruppur.
```

## First 10 City Nodes

```text
Tiruppur
Chennai
Coimbatore
Erode
Salem
Bengaluru
Hosur
Sri City
Madurai
Trichy
```

## First 3 Triangle Routes

```text
Tiruppur -> Chennai -> Coimbatore -> Tiruppur
Erode -> Chennai -> Coimbatore -> Erode
Bengaluru -> Sri City -> Chennai -> Bengaluru
```

---

# Final Takeaway

Qwen's strongest contribution is the technical path from idea to system:

```text
directed lane data
+ PostGIS candidate-city search
+ triangle scoring
+ n8n recommendation workflow
+ guardrails
+ 14-day validation logs
```

That is worth keeping.

But do not overbuild the AI stack yet.

The startup moat starts with:

```text
clean lane data
reliable field validation
repeatable triangle decisions
```

Then AI becomes useful.

Before that, it is just a shiny lorry horn.
