---
type: dashboard_spec
name: Corridor Delay Trends and Performance Dashboard
domain: logistics_control_tower
status: active
created_at: 2026-04-30
linked_data:
  - lane_delay_events
  - lane_reliability_scores
  - shipments
  - vehicles
  - carriers
linked_agents:
  - matching_agent
  - pricing_agent
  - risk_agent
  - control_tower_agent
---
# Corridor Delay Trends and Performance Dashboard

## Purpose

This dashboard turns corridor delay data into actionable intelligence for operations, pricing, route planning and executive decision-making.

It answers:

```text
Which lanes are reliable?
Which lanes are worsening?
Which delay component is driving failures?
Which carrier or hub needs intervention?
Where should agents add buffer, price risk, reroute or escalate?
```

## Users

| User | Primary Need |
|---|---|
| Operations manager | Monitor active lane health and intervene quickly |
| Lane controller | Diagnose root causes and coordinate fixes |
| Pricing analyst | Apply risk premiums based on reliability |
| Executive leadership | Track network quality, utilization and profitability |
| Control tower agent | Convert alerts into operating actions |

## Refresh Rhythm

| Layer | Refresh |
|---|---|
| Near real-time operations | Every 15 minutes |
| Daily lane aggregates | 02:00 IST |
| Weekly executive summary | Monday 06:00 IST |
| Scorecard recalculation | Rolling 90-day window |

## Data Model

### Fact Tables

| Table | Purpose |
|---|---|
| fact_shipment_delays | Shipment-level delay and OTIF facts |
| fact_lane_performance_daily | Daily lane score, volume and backhaul performance |
| fact_route_optimization_events | Adaptive routing and route-change impact |

### Dimension Tables

| Table | Purpose |
|---|---|
| dim_lanes | Directed lane metadata |
| dim_carriers | Carrier profile and reliability |
| dim_time | Calendar, peak season and holiday logic |
| dim_cargo_type | Cargo category and handling needs |
| dim_vehicle | Vehicle class and capability |

## Page 1: Executive Overview

### KPI Cards

| KPI | Definition | Decision Use |
|---|---|---|
| OTIF % | On-time and in-full shipments / total shipments | Network trust score |
| Average Delay Hours | Average total delay in hours | Operational drag |
| Active Lanes | Distinct lanes with recent shipments | Network scale |
| Fleet Utilization % | In-transit vehicles / available vehicles | Supply health |
| Backhaul Fill Rate | Average reverse/return fill performance | Deadhead reduction health |
| Average Reliability Score | Mean lane score | Executive lane quality signal |

### Visuals

| Visual | Configuration | Insight |
|---|---|---|
| Corridor performance map | Color by reliability score, size by shipment volume | Where the network is weak/strong |
| Delay trend line | Avg delay, P90 delay, target threshold | Whether network reliability is improving |
| Worst 5 lanes bar chart | Sort by avg delay or low score | Where ops should focus today |
| Reliability distribution gauge | A/B/C/D score ranges | Overall network grade |

## Page 2: Corridor Deep Dive

### Filters

```text
Lane
Date range
Cargo type
Carrier
Vehicle type
Tier combination
Reliability grade
```

### Visuals

| Visual | Configuration | Insight |
|---|---|---|
| Delay component waterfall | pickup, transit, terminal, documentation, last-mile | Where time is being lost |
| Delay vs volume scatter | X = volume, Y = delay, size = revenue, color = grade | High-volume lanes needing intervention |
| Day-of-week matrix | Lane x day with avg delay and OTIF | Best dispatch days and risk days |
| Volume vs delay trend | Shipment count bars + delay line | Whether volume spikes cause failures |
| Carrier ranking table | OTIF, avg delay, GPS, damage-free, score | Which carriers to prioritize or audit |

## Page 3: Adaptive Routing and Triangle Performance

This page tracks whether routing intelligence is actually reducing delay, cost and deadhead.

### KPI Cards

| KPI | Meaning |
|---|---|
| Time Saved Hours | Total minutes saved from route optimization / 60 |
| Cost Saved INR | Sum of estimated cost saved |
| Optimization Rate | Optimized shipments / total eligible shipments |
| Congestion Avoided Count | Route changes due to congestion |
| Triangle Conversion Rate | Accepted triangle routes / triangle opportunities |
| Revenue per Vehicle Day Lift | Triangle revenue/day vs baseline direct return |

### Visuals

| Visual | Configuration | Insight |
|---|---|---|
| Before/after ETA accuracy | Baseline vs optimized | Whether ASCT improves promise quality |
| Alternative route map | Primary vs alternate route flows | Where rerouting happens |
| Optimization adoption trend | Weekly optimization rate | Agent adoption and trust |
| Pareto chart of optimization reasons | congestion, weather, dwell, documentation, backhaul | Main reasons for route intervention |
| Triangle performance table | route, empty km saved, revenue lift, delay impact | Which return loops to scale |

## Page 4: Predictive Analytics and Alerts

### Visuals

| Visual | Configuration | Insight |
|---|---|---|
| 7-day delay forecast | Last 90 days + forecast band | Future risk planning |
| Alert table | Critical/warning/normal | Where to act now |
| Delay risk by hour/day heatmap | Hour x day average delay | Best dispatch windows |
| Buffer what-if parameter | Adjust buffer minutes and recalc OTIF | SLA promise tuning |

## Alert Rules

| Trigger | Level | Action |
|---|---|---|
| reliability_score < 55 | Critical | Block auto-match and notify ops |
| avg_delay_min > 300 | Critical | Require lane controller review |
| OTIF < 70 percent | Critical | Pause premium SLA |
| reliability_score 55-70 | Warning | Add backup carrier and pricing premium |
| p90_delay_min rising week-over-week > 10 percent | Warning | Root cause analysis |
| GPS coverage < 80 percent | Warning | Carrier tracking audit |

## Power BI Measures Starter

```DAX
OTIF Percentage =
DIVIDE(
    COUNTROWS(FILTER(fact_shipment_delays, fact_shipment_delays[otif_status] = TRUE())),
    COUNTROWS(fact_shipment_delays),
    0
) * 100

Average Delay Hours =
AVERAGE(fact_shipment_delays[total_delay_min]) / 60

Active Lanes =
DISTINCTCOUNT(fact_shipment_delays[lane_id])

Backhaul Fill Rate =
AVERAGE(fact_lane_performance_daily[backhaul_fill_rate]) * 100

Critical Lane Count =
COUNTROWS(FILTER(fact_lane_performance_daily, fact_lane_performance_daily[reliability_score] < 55))

Optimization Rate =
DIVIDE(
    COUNTROWS(FILTER(fact_route_optimization_events, fact_route_optimization_events[route_optimization_applied] = TRUE())),
    COUNTROWS(fact_route_optimization_events),
    0
) * 100

ASCT Time Saved Hours =
SUM(fact_route_optimization_events[time_saved_min]) / 60

ASCT Cost Saved Lakhs =
SUM(fact_route_optimization_events[cost_saved_inr]) / 100000
```

## Color Rules

| Grade | Score | Color |
|---|---:|---|
| A | 85-100 | Green |
| B | 70-84 | Yellow |
| C | 55-69 | Orange |
| D | below 55 | Red |

## Build Order

| Week | Work |
|---:|---|
| 1 | Connect PostgreSQL, create star schema, load sample data |
| 2 | Build executive overview and corridor deep dive |
| 3 | Add adaptive routing and alert pages |
| 4 | Pilot with ops users, tune alerts and mobile layout |

## MVP Rule

Start with three core KPIs:

```text
OTIF %
Average Delay
Lane Reliability Score
```

Then expand into route optimization, triangle performance and predictive alerts.

## Takeaway

This dashboard is not only a reporting tool.

It is the control surface for the Zippy operating system: it tells humans and agents where the network is leaking time, trust and margin.

## Linked Metrics Framework

The dashboard metric hierarchy is defined in [[Corridor Delay Trends Essential Metrics Framework]]. Use that note as the source of truth for KPI targets, alert thresholds, conditional formatting and MVP metric scope.
