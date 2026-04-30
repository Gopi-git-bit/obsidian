---
type: dashboard_metrics_framework
name: Corridor Delay Trends Dashboard Essential Metrics
domain: logistics_control_tower
status: active
created_at: 2026-04-30
linked_dashboard: "Corridor Delay Trends and Performance Dashboard Template"
---
# Corridor Delay Trends Dashboard Essential Metrics Framework

## Purpose

This framework defines the essential metrics for monitoring South India corridor delays across executive, tactical and operational views.

The dashboard must answer three questions in less than 10 seconds:

```text
1. Are we meeting delivery targets?
2. Which lanes are failing?
3. What is causing the delay?
```

## Tier 1: Core Delay KPIs

These metrics should appear on every dashboard view.

| Metric | Formula | Target | Alert Threshold | Best Visual |
|---|---|---:|---:|---|
| avg_delay_min | AVG(total_delay_min) | <= 120 min | > 180 min | Trend line + target marker |
| on_time_pct | on-time shipments / total shipments x 100 | >= 85 percent | < 75 percent | Gauge + weekly trend |
| p90_delay_min | 90th percentile total delay | <= 240 min | > 300 min | Box plot / percentile card |
| p95_delay_min | 95th percentile total delay | <= 300 min | > 360 min | Histogram / distribution |
| delay_stddev_min | STDDEV(total_delay_min) | <= 90 min | > 120 min | Control chart |
| otif_pct | on-time and in-full shipments / total shipments x 100 | >= 80 percent | < 70 percent | Dual-axis with on-time pct |

## Tier 2: Delay Component Metrics

These explain why the delay is happening.

| Metric | Target | Why It Matters | Drill-Down Path |
|---|---:|---|---|
| pickup_delay_min | <= 30 min | Origin-side reliability | Carrier -> shipper readiness |
| transit_delay_min | <= 60 min | Route, congestion, breakdown and weather risk | Highway -> weather -> route plan |
| terminal_dwell_delay_min | <= 45 min | Hub/port/warehouse handoff efficiency | Terminal -> slot -> queue |
| documentation_delay_min | <= 15 min | Compliance and admin friction | E-way bill -> invoice -> POD |
| last_mile_delay_min | <= 30 min | Customer-facing experience | Consignee -> unloading -> city restriction |

## Tier 3: Lane-Specific Performance Metrics

These compare corridors and expose structural issues.

| Metric | Formula | Target | Use Case | Visual |
|---|---|---:|---|---|
| lane_reliability_score | Weighted composite | >= 75 | Lane ranking | Corridor heatmap |
| delay_trend_7d | (avg today - avg 7d ago) / avg 7d ago | <= 0 percent | Degradation detection | Sparkline |
| backhaul_delay_gap | avg outbound delay - avg return delay | <= 30 min | Directional imbalance | Paired bar |
| peak_vs_offpeak_delay | avg peak delay / avg off-peak delay | <= 1.3 | Capacity planning | Ratio gauge |
| carrier_delay_variance | STDDEV(avg delay by carrier) | <= 45 min | Carrier consistency | Box plot |

## Tier 4: Predictive and Leading Indicators

These warn before delays happen.

| Metric | Target | Trigger | Agent Action |
|---|---:|---|---|
| congestion_index | >= 0.85 | < 0.70 | Reroute or add buffer |
| weather_risk_score | <= 3/10 | >= 7/10 | Add buffer or require confirmation |
| capacity_utilization | <= 80 percent | >= 90 percent | Shortage alert and surge pricing |
| driver_availability_gap | <= 5 percent | >= 15 percent | Add partner fleet or reschedule |
| terminal_queue_length | <= 10 trucks | >= 20 trucks | Shift slot or alternate hub |

## Tier 5: Financial Impact Metrics

These convert delays into business cost.

| Metric | Formula | Target | Business Use |
|---|---|---:|---|
| delay_cost_per_shipment | AVG(delay penalty + fuel waste + driver overtime) | <= INR 500 | Margin control |
| total_delay_cost_monthly | SUM(delay cost) | <= INR 5L/month | P&L impact |
| penalty_incurred_pct | penalty shipments / total shipments | <= 5 percent | Customer satisfaction |
| fuel_waste_liters | idle hours x fuel consumption rate | <= 2L/trip | Sustainability |
| revenue_at_risk | contract value x delay probability | <= 2 percent revenue | Churn prediction |

## Tier 6: Operational Efficiency Metrics

These show whether the network is becoming more efficient.

| Metric | Formula | Target | Insight |
|---|---|---:|---|
| avg_turnaround_time_hrs | unload to next-load time | <= 4 hrs | Asset utilization |
| empty_mile_pct | empty km / total km x 100 | <= 25 percent | Backhaul effectiveness |
| first_attempt_delivery_pct | first-attempt successes / total | >= 90 percent | Last-mile quality |
| exception_rate | exceptions / total shipments | <= 10 percent | Process stability |
| gps_coverage_pct | shipments with GPS / total shipments | >= 95 percent | Visibility quality |

## Conditional Formatting Rules

| Metric | Green | Yellow | Red |
|---|---:|---:|---:|
| avg_delay_min | <= 90 | 90-180 | > 180 |
| on_time_pct | >= 85 percent | 75-85 percent | < 75 percent |
| p90_delay_min | <= 240 | 240-360 | > 360 |
| delay_trend_7d | <= 0 percent | 0-10 percent | > 10 percent |
| lane_reliability_score | >= 80 | 60-80 | < 60 |
| backhaul_delay_gap | <= 30 min | 30-60 min | > 60 min |

## Dashboard Layout Recommendation

### Executive Overview

```text
KPI row:
Avg Delay | On-Time % | P90 Delay | OTIF % | Reliability Score

Main visual:
Delay Trend Last 90 Days
- Avg delay
- P90 delay
- Target threshold

Bottom row:
Top 5 worst lanes | Delay by day/hour heatmap
```

### Operational Deep Dive

```text
Filters:
Lane | Date range | Cargo type | Carrier | Vehicle type

Visuals:
Delay component waterfall
Volume vs delay scatter
Carrier performance table
Shipment drill-through
```

## DAX Starter Measures

```DAX
Avg Delay Min =
AVERAGE(fact_shipment_delays[total_delay_min])

On Time Pct =
DIVIDE(
    COUNTROWS(FILTER(fact_shipment_delays, fact_shipment_delays[delivered_on_time] = TRUE())),
    COUNTROWS(fact_shipment_delays),
    0
) * 100

OTIF Pct =
DIVIDE(
    COUNTROWS(FILTER(fact_shipment_delays, fact_shipment_delays[otif_status] = TRUE())),
    COUNTROWS(fact_shipment_delays),
    0
) * 100

P90 Delay Min =
PERCENTILE.INC(fact_shipment_delays[total_delay_min], 0.90)

P95 Delay Min =
PERCENTILE.INC(fact_shipment_delays[total_delay_min], 0.95)

Delay CV =
DIVIDE(
    STDEV.P(fact_shipment_delays[total_delay_min]),
    AVERAGE(fact_shipment_delays[total_delay_min]),
    0
)

Empty Mile Pct =
DIVIDE(
    SUM(fact_shipment_delays[empty_km]),
    SUM(fact_shipment_delays[empty_km]) + SUM(fact_shipment_delays[loaded_km]),
    0
) * 100
```

## Refresh Strategy

| Metric Category | Refresh Frequency | Source |
|---|---|---|
| Core KPIs | Every 15 min | PostgreSQL DirectQuery |
| Delay components | Every 30 min | Aggregated views |
| Lane performance | Hourly | Materialized views |
| Predictive indicators | Every 5 min | Traffic/weather APIs |
| Financial impact | Daily | Billing and settlement tables |

## MVP Rule

Start with five metrics only:

```text
Avg delay
On-time percentage
P90 delay
OTIF percentage
Lane reliability score
```

Then add component breakdown, predictive indicators and financial impact once operators trust the first dashboard.

## Takeaway

The dashboard should not become a colourful graveyard of metrics.

It should be a decision cockpit: every chart should point to a next action.
