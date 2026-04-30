---
type: algorithm
domain: allocation
decision_value: high
status: draft
related_hubs:
  - Algorithms Hub
  - Operations Strategy Hub
  - Technology Stack Hub
tags:
  - network-design
  - hub-and-spoke
  - facility-location
  - postgis
  - optimization
---

# Hub-and-Spoke Network Design Algorithm

## Purpose

Select hub locations, spoke coverage, routing mode, and pilot corridors for Zippy's warehouse-first logistics network.

Derived from [[Logistics Network Implementation Source]] and used by [[Logistics Network Implementation Roadmap]].

## Inputs

| Input | Examples |
|-------|----------|
| demand points | customer pincode, warehouse location, order volume, service tier |
| supply points | vehicle location, carrier base, transport nagar, partner warehouse |
| facility candidates | warehouse clusters, truck terminals, cross-docks, 3PL hubs |
| corridor data | distance, time, toll, fuel, traffic, failure rate, return-load probability |
| customer segment | Standard, Express, Premium, Dedicated |
| material type | FMCG, textile, cold-chain, high-value, hazardous, bulk |
| constraints | hub capacity, dock capacity, radius, cut-off time, compliance, handling fit |

## Decision Outputs

- recommended hub candidates
- spoke assignment per hub
- direct versus hub-routed decision
- hub radius recommendation
- corridor profitability score
- pilot lane shortlist
- capacity and vehicle pool requirement
- fallback hub or direct route
- return-trip matching corridors and hub-aware loop opportunities

## Algorithm Flow

```text
1. cluster demand points by pincode / warehouse / industrial zone
2. score facility candidates by weighted distance, demand density, carrier proximity, labor access, and compliance fit
3. assign demand clusters to nearest feasible hub within service radius
4. evaluate direct, hub-and-spoke, cross-dock, and milk-run alternatives
5. calculate corridor profitability and empty-leg risk
6. choose hub/spoke topology by service tier and material constraints
7. simulate pilot KPIs before launch
8. monitor actual KPIs and update hub radius, partner pool, and routing rules
```

## Scoring Model

```text
hub_score =
  demand_density_score
+ carrier_proximity_score
+ warehouse_cluster_score
+ road_access_score
+ labor_availability_score
+ compliance_readiness_score
- congestion_penalty
- facility_cost_penalty
- handling_mismatch_penalty
```

```text
corridor_profitability_score =
  revenue_per_order
- linehaul_cost
- hub_handling_cost
- spoke_delivery_cost
- expected_exception_cost
+ return_load_value
+ consolidation_savings
```

## Routing Decision Rule

```text
if cargo is high-value, urgent, cold-chain, hazardous, or port deadline:
  evaluate direct or specialized workflow first

elif demand_cluster_density is high and orders share corridor:
  prefer hub-and-spoke or consolidation

elif many nearby stops have repeat windows:
  prefer milk run

elif inbound and outbound timing is synchronized:
  prefer cross-dock

elif hub_route adds excessive dwell or distance:
  use direct route

else:
  choose lowest total cost route that satisfies SLA and risk constraints
```

## PostGIS Query Pattern

```sql
-- Cluster demand points for candidate spoke planning.
SELECT
  ST_ClusterDBSCAN(geom, eps := 0.25, minpoints := 5) OVER () AS cluster_id,
  COUNT(*) AS order_count,
  SUM(order_value) AS demand_value,
  ST_Centroid(ST_Collect(geom)) AS cluster_center
FROM order_demand_points
WHERE created_at >= NOW() - INTERVAL '90 days'
GROUP BY cluster_id;
```

```sql
-- Score candidate hubs by nearby demand and carrier availability.
SELECT
  h.hub_id,
  h.name,
  COUNT(DISTINCT o.order_id) AS nearby_orders,
  COUNT(DISTINCT v.vehicle_id) AS nearby_vehicles,
  AVG(ST_Distance(h.geom::geography, o.geom::geography)) AS avg_order_distance_m
FROM hub_candidates h
LEFT JOIN order_demand_points o
  ON ST_DWithin(h.geom::geography, o.geom::geography, 200000)
LEFT JOIN vehicle_supply_points v
  ON ST_DWithin(h.geom::geography, v.geom::geography, 50000)
GROUP BY h.hub_id, h.name;
```

## Pilot Gate

| Metric | Pass Condition |
|--------|----------------|
| hub dwell time | under 45 minutes average |
| empty-leg reduction | at least 20% versus baseline |
| on-time delivery | at least 92% |
| cost per order | at least 15% lower than direct routing baseline |
| tracking event completeness | at least 95% |
| driver feedback | at least 4.0/5 |
| customer NPS | at least 35 |

## Learning Loop

```text
daily:
  compare planned vs actual hub dwell, ETA, utilization, and cost
  flag poor corridors and overloaded hubs
  adjust hub radius, cut-off time, and partner allocation

weekly:
  update corridor profitability
  identify new spoke candidates
  run A/B test on 150 km vs 200 km hub radius

monthly:
  approve expansion, pause weak lanes, or add redundancy
```

## Related Notes

- [[Logistics Network Implementation Roadmap]]
- [[Warehouse Transport Correlation Algorithm]]
- [[Lane Intelligence Model]]
- [[Return Load Optimization]]
- [[Hub-Aware Return Trip Matching]]
- [[Route Optimization Logic]]
- [[Customer Segment Value Creation Framework]]
