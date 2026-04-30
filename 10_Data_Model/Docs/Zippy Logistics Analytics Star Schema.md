---
type: data_model_doc
schema: zippy_logistics
status: active
created_at: 2026-04-30
linked_dashboard:
  - Corridor Delay Trends and Performance Dashboard Template
  - Tableau Workbook Spec: ZippyLogitech Corridor Delay Analytics
---
# Zippy Logistics Analytics Star Schema

## Purpose

This schema supports corridor delay analytics, OTIF tracking, ASCT performance, lane reliability scorecards and Power BI/Tableau reporting.

The production SQL lives here:

```text
10_Data_Model/SQL/zippy_logistics_analytics_star_schema.sql
```

## Design Pattern

```text
Star schema:
Dimension tables -> Fact tables -> Aggregates -> BI dashboards
```

## Dimensions

| Table | Purpose |
|---|---|
| dim_time | Calendar, holiday and seasonality filtering |
| dim_lanes | Directed corridor metadata |
| dim_carriers | Carrier performance and compliance metadata |
| dim_cargo_type | Cargo category and handling requirements |
| dim_vehicle | Vehicle class and capability metadata |

## Facts

| Table | Grain | Purpose |
|---|---|---|
| fact_shipment_delays | One row per shipment | Atomic delay, OTIF, tracking and cost facts |
| fact_lane_performance_daily | One row per lane per day | Pre-aggregated lane dashboard metrics |
| fact_asct_performance | One row per route optimization event | ASCT/time saved/cost saved/triangle impact |

## Generated Columns

| Column | Table | Rule |
|---|---|---|
| total_delay_min | fact_shipment_delays | Sum of delay components |
| otif_status | fact_shipment_delays | delivered_on_time AND delivered_in_full AND not damaged |

Important:

```text
Do not update generated columns in UPSERT statements.
Update the source fields and let PostgreSQL recompute them.
```

## Dashboard Mapping

| Dashboard Visual | Source Tables |
|---|---|
| OTIF KPI | fact_shipment_delays |
| Average delay and P90/P95 trends | fact_lane_performance_daily |
| Delay waterfall | fact_shipment_delays |
| Lane reliability heatmap | dim_lanes + fact_lane_performance_daily |
| ASCT before/after ETA | fact_asct_performance |
| Carrier scorecard | dim_carriers + fact_shipment_delays |

## Maintenance Jobs

| Job | Frequency | Action |
|---|---|---|
| Load shipment delay events | Near real time / batch | Upsert into fact_shipment_delays by idempotency_key |
| Refresh daily lane performance | Daily 02:00 IST | Run refresh_fact_lane_performance_daily() |
| Refresh BI extracts | Hourly/daily | Tableau/Power BI refresh from aggregate tables |
| Rebuild dim_time | Annual | Extend calendar and holiday flags |

## Notes and Corrections Applied

The source proposal included a generated `total_delay_min` column and then attempted to update it during an upsert. PostgreSQL does not allow direct updates to generated columns. The final schema fixes this by updating only delay component fields.

The schema also uses nonnegative stage-level delay components. If early-arrival analytics are needed later, add a separate field such as `schedule_variance_min` instead of making delay components negative.

## dim_time Population Script

The India logistics calendar population script is available here:

```text
10_Data_Model/SQL/populate_dim_time_india_logistics.sql
```

It adds holiday and logistics seasonality flags used by pricing, matching, risk and dashboard workflows. See [[dim_time India Logistics Calendar]] for usage notes.
