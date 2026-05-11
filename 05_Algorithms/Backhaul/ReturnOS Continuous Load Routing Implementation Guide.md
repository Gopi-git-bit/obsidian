---
title: ReturnOS Continuous Load Routing Implementation Guide
type: algorithm-implementation
domain: logistics
created: 2026-05-02
source_file: C:\Users\user\Downloads\return trip math.txt
tags:
  - backhaul
  - return-trip
  - deadhead
  - triangle-routing
  - quadrilateral-routing
  - returnos
  - implementation
  - zippy
---

# ReturnOS Continuous Load Routing Implementation Guide

## Core Idea

The strongest return-trip tactic is **continuous-load routing**, not simple backhaul matching.

Simple backhaul matching asks:

```text
Can I find B -> A after A -> B?
```

ReturnOS should ask:

```text
After A -> B, what is the next best paid city C or D that moves the truck closer to a profitable cluster?
```

The useful route shapes are:

```text
A -> B -> C -> A
A -> B -> C -> D -> A
```

This is stronger for South India Tier-2/Tier-3 logistics because direct returns are often weak, but nearby cluster-to-cluster freight is strong.

## Strategy Ranking

| Rank | Strategy | Impact | Why |
|---:|---|---|---|
| 1 | Cluster-based triangle / quad routing | Highest | Solves weak direct returns by chaining paid legs |
| 2 | Predictive load matching before delivery | Very high | Finds the next load before the truck becomes idle |
| 3 | Return-to-cluster planning | High | Truck returns to the freight cluster, not exact origin city |
| 4 | Dynamic return-leg pricing | Medium-high | Discounts weak legs when truck surplus is high |
| 5 | Collaborative freight pool | Medium-high | Uses carriers, brokers, warehouses, MSMEs, and partners |
| 6 | Simple load board | Medium | Improves visibility but depends on direct load availability |

## Key Metrics

### Deadhead Percentage

```text
Deadhead % = Empty km / Total km * 100
```

Targets:

| Stage | Deadhead Target |
|---|---:|
| Before ReturnOS | 30-50% |
| Good triangle routing | Below 20-25% |
| Strong system | Below 15-20% |

### Loaded-Km Ratio

```text
Loaded Km Ratio = Loaded km / Total km
```

| Loaded-Km Ratio | Meaning |
|---:|---|
| 85-95% | Excellent |
| 75-85% | Strong |
| 60-75% | Average |
| Below 60% | Backhaul problem |

### Revenue Per Vehicle Day

This is the king metric.

```text
Revenue per Vehicle Day = Total Route Revenue / Total Cycle Time in Days
```

A triangle is only good if it improves revenue per vehicle day, not just if it looks geographically neat.

### Directional Imbalance

```text
Directional Imbalance = ABS(Volume_AB - Volume_BA) / MAX(Volume_AB, Volume_BA)
```

| Imbalance | Meaning | Action |
|---:|---|---|
| 0-20% | Balanced | Direct backhaul can work |
| 20-40% | Mild imbalance | Use pricing incentives |
| 40-60% | Serious imbalance | Test triangle routes |
| 60%+ | Severe imbalance | Triangle / quad required |

### Backhaul Probability

```text
Backhaul Probability = Successful direct return loads / Trucks needing return load
```

Rule:

```text
If direct backhaul probability < 50%, generate triangle or quad candidates.
```

## Profit Formulas

### Direct Return Profit

```text
Direct Profit =
Revenue_AB + Revenue_BA
- Cost_AB - Cost_BA
- Waiting Cost
```

### Triangle Profit

```text
Triangle Profit =
Revenue_AB + Revenue_BC + Revenue_CA
- Cost_AB - Cost_BC - Cost_CA
- Waiting Cost
- Detour Cost
```

Choose triangle if:

```text
Triangle Profit > Direct Profit
AND Triangle Deadhead % < Direct Deadhead %
AND Triangle Revenue/Vehicle/Day > Direct Revenue/Vehicle/Day
```

### Quadrilateral Profit

```text
Quad Profit =
Revenue_AB + Revenue_BC + Revenue_CD + Revenue_DA
- Cost_AB - Cost_BC - Cost_CD - Cost_DA
- Waiting Cost
- Detour Cost
```

Use quadrilateral routes when no single C-city solves the return problem.

## Scoring Engine

Use scoring before advanced ML. It is easier to validate with live trips.

### Triangle Score

```text
Triangle Score =
0.25 * Revenue Gain Score
+ 0.25 * Empty-Km Reduction Score
+ 0.20 * Load Probability Score
+ 0.15 * Time Feasibility Score
+ 0.10 * Vehicle Compatibility Score
+ 0.05 * Payment Reliability Score
```

| Score | Action |
|---:|---|
| 85-100 | Launch route |
| 70-84 | Validate with 10-20 live trips |
| 55-69 | Occasional use |
| Below 55 | Avoid |

### Quad Score

```text
Quad Score =
0.20 * Revenue Gain Score
+ 0.20 * Empty-Km Reduction Score
+ 0.20 * Load Probability Score
+ 0.15 * Time Feasibility Score
+ 0.10 * Cluster Return Fit Score
+ 0.10 * Vehicle Compatibility Score
+ 0.05 * Payment Reliability Score
```

Quad routes need stronger time-window checks because they add more legs.

## Candidate Generation Rules

For primary lane:

```text
A -> B
```

First check direct return:

```text
B -> A
```

If direct return is weak, search for C where at least one is true:

- C is near origin A.
- C is inside A's freight cluster.
- B -> C has strong cargo.
- C -> A is short.
- C has port, airport, warehouse, ICD, mandi, or industrial role.
- C lies on a major highway corridor.

If no good C exists, search for D and create:

```text
A -> B -> C -> D -> A
```

## Greedy MVP Algorithm

```text
For every truck finishing A -> B:
  1. Check direct return B -> A.
  2. If strong return load exists:
       recommend B -> A.
  3. If weak:
       list candidate cities C near A or inside A_cluster.
  4. For each C:
       calculate B -> C load probability.
       calculate C -> A_cluster load probability.
       calculate revenue per vehicle day.
       calculate empty-km reduction.
       calculate wait-time risk.
       calculate vehicle compatibility.
  5. Pick C with highest triangle score.
  6. If best triangle score >= 70:
       recommend A -> B -> C -> A_cluster.
  7. If no triangle score >= 70:
       generate quad candidates A -> B -> C -> D -> A_cluster.
  8. Choose route with:
       highest revenue per vehicle day,
       lowest deadhead percentage,
       acceptable time and risk.
```

## Return-To-Cluster Rule

Do not force the truck to return to the exact origin city.

Return it to the origin freight cluster.

Example cluster:

```text
Western Tamil Nadu =
Coimbatore + Tiruppur + Erode + Salem + Karur
```

If the origin is Tiruppur, the system does not always need:

```text
Chennai -> Tiruppur
```

It can recommend:

```text
Chennai -> Coimbatore -> Tiruppur
Chennai -> Erode -> Tiruppur
Chennai -> Salem -> Tiruppur
```

This works because the cluster behaves like one regional freight pool.

## South India Route Examples

| Route Chain | Demand Logic | Use Case |
|---|---|---|
| Tiruppur -> Chennai -> Coimbatore -> Tiruppur | Garments to port; FMCG/machinery to Coimbatore; textile movement back to Tiruppur | When Chennai -> Tiruppur is weak |
| Erode -> Chennai -> Coimbatore -> Erode | Textiles/agri to Chennai; industrial/FMCG to Coimbatore; yarn/agri inputs to Erode | Western TN return-to-cluster |
| Salem -> Chennai -> Coimbatore -> Salem | Steel/foundry to Chennai; FMCG/machinery to Coimbatore; industrial backflow | Construction and industrial lanes |
| Bengaluru -> Sri City -> Chennai -> Bengaluru | Electronics/auto/EV to Sri City; feeder to Chennai; retail/FMCG back to Bengaluru | Industrial triangle |
| Karur -> Chennai -> Bengaluru -> Karur cluster | Home textiles to Chennai; consumer goods to Bengaluru; cluster return | Festival-season textile routing |

## Data Model

### City Nodes

```yaml
city:
  name:
  state:
  tier:
  latitude:
  longitude:
  industrial_clusters:
  outbound_cargo:
  inbound_cargo:
  nearby_port:
  nearby_airport:
  nearby_rail_terminal:
  nearby_highways:
  warehouse_density:
  transporter_density:
  distribution_role:
  priority_score:
```

### Directed Lanes

Store each direction separately.

```yaml
directed_lane:
  origin:
  destination:
  distance_km:
  highway_route:
  cargo_types:
  average_loads_per_day:
  average_rate_per_km:
  average_wait_hours:
  vehicle_types:
  lane_strength:
  return_strength:
  payment_risk:
  demurrage_risk:
  data_confidence:
```

### Freight Clusters

```yaml
cluster:
  name:
  cities:
  industries:
  common_cargo:
  main_ports:
  main_airports:
  major_highways:
  cluster_role:
```

### Ports, Airports, ICDs, And Highway Nodes

```yaml
freight_node:
  type: port | airport | icd | highway_node | warehouse_cluster | mandi
  name:
  city:
  cargo_types:
  connected_clusters:
  road_connectivity:
  rail_connectivity:
  role:
```

## Backend Services

| Service | Responsibility |
|---|---|
| Backhaul Probability Service | Predict direct B -> A load chance within 6/12/24 hours |
| Next Best City Service | Rank candidate C cities after delivery at B |
| Triangle / Quad Generator | Generate A -> B -> C -> A and A -> B -> C -> D -> A candidates |
| Route Scoring Service | Calculate profit, deadhead, revenue/day, wait risk, vehicle fit |
| Vehicle Compatibility Service | Check body type, cargo history, cleaning, temperature, hazmat, capacity |
| Dynamic Return Pricing Service | Discount weak-origin lanes when truck surplus is high |
| Seasonal Multiplier Service | Apply month, harvest, festival, monsoon, and weather effects |
| Experiment Tracking Service | Compare before/after route performance |

## Seasonality Layer

Seasonality should modify:

- Load probability.
- Route score.
- Vehicle allocation.
- Pricing.
- Warehouse pressure.
- Risk buffer.
- Return-trip probability.
- Triangle / quad recommendations.

Formula:

```text
Seasonal Route Score =
Base Route Score
+ Seasonal Demand Boost
- Seasonal Risk Penalty
```

Seasonal next-city probability:

```text
Seasonal Next-City Probability =
Base Next-City Probability
* Cargo Demand Multiplier
* City Seasonal Multiplier
* Lane Seasonal Multiplier
* Weather Risk Adjustment
```

## Seasonality MVP Tables

Start with these five tables:

```sql
CREATE TABLE seasons (
  season_id UUID PRIMARY KEY,
  season_name TEXT,
  start_month INT,
  end_month INT,
  states TEXT[],
  notes TEXT
);

CREATE TABLE seasonal_cargo_rules (
  rule_id UUID PRIMARY KEY,
  cargo_category TEXT,
  season_name TEXT,
  demand_multiplier NUMERIC,
  risk_multiplier NUMERIC,
  required_vehicle_type TEXT[],
  temperature_sensitive BOOLEAN,
  notes TEXT
);

CREATE TABLE city_seasonal_profiles (
  profile_id UUID PRIMARY KEY,
  city_id UUID,
  season_name TEXT,
  top_cargo_categories TEXT[],
  outbound_boost NUMERIC,
  inbound_boost NUMERIC,
  warehouse_pressure_score INT,
  vehicle_pressure_score INT,
  confidence_score INT
);

CREATE TABLE lane_seasonal_profiles (
  profile_id UUID PRIMARY KEY,
  origin_city_id UUID,
  destination_city_id UUID,
  season_name TEXT,
  cargo_category TEXT,
  expected_load_multiplier NUMERIC,
  expected_rate_multiplier NUMERIC,
  expected_wait_multiplier NUMERIC,
  risk_multiplier NUMERIC,
  backhaul_probability_multiplier NUMERIC
);

CREATE TABLE seasonal_forecasts (
  forecast_id UUID PRIMARY KEY,
  forecast_date DATE,
  origin_city_id UUID,
  destination_city_id UUID,
  cargo_category TEXT,
  season_name TEXT,
  predicted_loads INT,
  predicted_rate_per_km NUMERIC,
  predicted_wait_hours NUMERIC,
  predicted_backhaul_probability NUMERIC,
  model_version TEXT,
  confidence_score INT
);
```

## Event Flow

### Event: load_created

```json
{
  "origin": "Chennai",
  "destination": "Coimbatore",
  "cargo": "AC_fans_coolers",
  "date": "2026-04-15"
}
```

Backend actions:

- Detect active season.
- Apply cargo and lane multiplier.
- Check suitable vehicle.
- Check warehouse pressure.
- Update price and margin estimate.

### Event: truck_delivered

```json
{
  "truck_id": "TRK001",
  "current_city": "Chennai",
  "home_cluster": "Western_TN",
  "date": "2026-04-15",
  "vehicle_type": "closed_body_20ft"
}
```

Backend actions:

- Check direct return probability.
- If direct probability is weak, generate triangle candidates.
- Apply seasonality boost.
- Apply vehicle compatibility rules.
- Recommend best B -> C -> A_cluster route.

## MVP Build Plan

### Phase 1: Scoring Engine

Build:

- City nodes.
- Directed lanes.
- Freight clusters.
- Vehicle compatibility rules.
- Triangle score.
- Deadhead and revenue/day metrics.

Do not start with advanced ML. Start with a transparent scoring engine.

### Phase 2: ReturnOS Recommendation

For each delivered truck, return:

```json
{
  "recommended_route": ["Chennai", "Coimbatore", "Tiruppur"],
  "route_type": "triangle",
  "triangle_score": 82,
  "deadhead_reduction_percent": 31,
  "revenue_per_vehicle_day_lift_percent": 18,
  "reason": [
    "direct Chennai -> Tiruppur probability is weak",
    "Chennai -> Coimbatore summer demand is strong",
    "Coimbatore is inside Western TN cluster"
  ]
}
```

### Phase 3: Seasonality

Add:

- Seasons.
- Seasonal cargo rules.
- City seasonal profiles.
- Lane seasonal profiles.
- Seasonal forecasts.

### Phase 4: Optimization

Later, add:

- Batch optimization.
- VRP with time windows.
- Multi-truck assignment.
- Warehouse slot constraints.
- Driver-hour constraints.
- Dynamic pricing optimization.

## Experiment Metrics

Track before and after for each route experiment:

| Metric | Target |
|---|---:|
| Empty km reduction | At least 20% |
| Revenue per vehicle day lift | At least 15% |
| Waiting time increase | Not more than 20% |
| Driver acceptance | At least 70% |
| Delivery failure | No increase |
| Customer price reduction | Track by lane |
| Triangle conversion rate | Track by route and vehicle type |
| Backhaul match rate | Track direct and cluster returns separately |

## Product Rules

1. If direct return probability is strong, recommend direct return.
2. If direct return probability is below 50%, search triangle routes.
3. If directional imbalance is above 60%, triangle or quad is required.
4. Return to the origin cluster, not necessarily the exact origin city.
5. Never recommend incompatible return cargo just because it is nearby.
6. Rank by revenue per vehicle day, not trip revenue alone.
7. Penalize waiting time, payment risk, weather risk, and vehicle mismatch.
8. Use seasonality to change next-city probabilities by month and cargo type.

## Related Notes

- [[South India Empty Return Red Zones]]
- [[South India Transport Price Variation Framework]]
- [[South India Logistics Seasonality Calendar]]
- [[South India Distribution Hub Strategy]]
- [[South India Commercial Vehicle Model Demand]]
- [[Triangle Route Engine for Return Trip Optimization]]
- [[Triangle Backhaul Technical Implementation Addendum]]
- [[Deadhead Reduction Intelligence Layer for Tier 2-3 Freight]]
- [[Return Trip Streamlined Operations v1]]
