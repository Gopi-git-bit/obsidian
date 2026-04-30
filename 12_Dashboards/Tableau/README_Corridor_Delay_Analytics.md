---
type: tableau_readme
workbook: "ZippyLogitech_Corridor_Delay_Analytics.twbx"
version: "1.2.0"
last_updated: "2026-04-30"
data_sources:
  - corridors_extract.hyper
  - delay_events_sample.hyper
  - carriers_benchmarks.csv
  - south_india_cities.geojson
obsidian_links:
  - dashboards/corridor-analytics
  - lane_scorecards
status: active
---
# README: ZippyLogitech Corridor Delay Analytics TWBX

```text
================================================================================
ZIPPYLOGITECH CORRIDOR DELAY ANALYTICS - DATA SOURCE DOCUMENTATION
================================================================================
Workbook: ZippyLogitech_Corridor_Delay_Analytics.twbx
Version: 1.2.0
Last Updated: 2026-04-30
Owner: Bharathi Raja / Operations Analytics
Obsidian Link: [[dashboards/corridor-analytics]]
================================================================================
```

## 1. Workbook Overview

Purpose:

```text
Monitor corridor delay trends, lane reliability scores and ASCT performance for South India logistics operations.
```

Target users:

| User | Purpose |
|---|---|
| Operations managers | Real-time lane monitoring and exception handling |
| Pricing analysts | Risk premium calculations and buffer optimization |
| Executive leadership | OTIF trends and corridor profitability overview |
| Data engineers | Source validation and extract refresh management |

Refresh schedule:

| View Type | Refresh |
|---|---|
| Live dashboards | Every 15 minutes via PostgreSQL/live connection |
| Extract-based views | Daily at 02:00 IST via Hyper extract refresh |
| Weekly aggregates | Monday 06:00 IST materialized view rebuild |

## 2. Embedded Data Sources

This packaged workbook can contain the following embedded data sources:

| Source Name | Type | Purpose |
|---|---|---|
| corridors_extract.hyper | Extract | Lane-level reliability and corridor score data |
| delay_events_sample.hyper | Extract | Shipment-level delay event records |
| carriers_benchmarks.csv | CSV | Carrier performance reference |
| south_india_cities.geojson | GeoJSON | Custom city/corridor map layer |

Important note:

```text
Live PostgreSQL connections are not embedded inside the portable TWBX.
For production, replace extracts with Tableau Server-managed PostgreSQL connections.
```

## 3. Data Dictionary: Corridors Extract

Table: `lane_reliability_scores`

| Field | Type | Description |
|---|---|---|
| lane_id | String | Unique corridor identifier, format origin:destination:cargo |
| origin_city | String | Source city |
| destination_city | String | Destination city |
| distance_km | Integer | Road distance in km |
| primary_cargo | String | Dominant cargo category |
| monthly_truckloads | Integer | Estimated 10-ton equivalent monthly truckloads |
| backhaul_fill_rate | Decimal | Return-leg utilization from 0.00 to 1.00 |
| reliability_score | Decimal | Composite lane score from 0 to 100 |
| reliability_grade | String | A >=85, B 70-84, C 55-69, D/F <55 |
| recommended_sla_window | Decimal | Suggested delivery window in hours |
| requires_backup_carrier | Boolean | Whether backup carrier is needed |
| requires_premium_buffer | Boolean | Whether additional buffer is needed |
| calculation_date | Date | Score calculation date |
| data_confidence | String | high, medium or low |

## 4. Data Dictionary: Delay Events

Table: `lane_delay_events`

| Field | Type | Description |
|---|---|---|
| shipment_id | String | Unique shipment identifier |
| lane_id | String | Foreign key to lane score data |
| shipment_date | Date | Dispatch date |
| scheduled_pickup | DateTime | Planned pickup timestamp |
| actual_pickup | DateTime | Actual pickup timestamp |
| scheduled_delivery | DateTime | Planned delivery timestamp |
| actual_delivery | DateTime | Actual delivery timestamp |
| total_delay_min | Integer | Actual minus scheduled delay in minutes |
| pickup_delay_min | Integer | Origin-side delay |
| transit_delay_min | Integer | En-route delay |
| terminal_dwell_delay_min | Integer | Hub/port/warehouse waiting delay |
| documentation_delay_min | Integer | E-way bill, invoice, POD or compliance delay |
| last_mile_delay_min | Integer | Final delivery delay |
| delivered_on_time | Boolean | Delivered inside promised window |
| otif_status | Boolean | On-time and in-full |
| carrier_id | String | Foreign key to carrier reference |
| gps_coverage_pct | Decimal | Tracking compliance percentage |
| exception_count | Integer | Alerts triggered |
| resolution_time_min | Integer | Alert-to-resolution time |

## 5. Calculated Fields

### On-Time Percentage

```tableau
{ FIXED [Lane_ID]:
    SUM(IF [delivered_on_time] THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

### OTIF Percentage

```tableau
{ FIXED [Lane_ID]:
    SUM(IF [otif_status] THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

### P90 Delay Minutes

```tableau
{ FIXED [Lane_ID]: PERCENTILE([total_delay_min], 0.90) }
```

### Delay CV

```tableau
STDEV([total_delay_min]) / AVG([total_delay_min])
```

### Reliability Grade

```tableau
IF [reliability_score] >= 85 THEN "A"
ELSEIF [reliability_score] >= 70 THEN "B"
ELSEIF [reliability_score] >= 55 THEN "C"
ELSE "D/F"
END
```

### Alert Flag

```tableau
IF [reliability_score] < 55 OR [avg_delay_min] > 300 OR [on_time_pct] < 70 THEN "Critical"
ELSEIF [reliability_score] < 70 OR [avg_delay_min] > 180 THEN "Warning"
ELSE "Normal"
END
```

### ASCT Time Saved Hours

```tableau
SUM([time_saved_min]) / 60
```

### ASCT Cost Saved Lakhs

```tableau
SUM([cost_saved_inr]) / 100000
```

### Optimization Rate

```tableau
{ FIXED [Lane_ID]:
    SUM(IF [route_optimization_applied] THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

## 6. Data Lineage

```text
PostgreSQL Production DB
-> Autoclaw / Python ETL
-> Hyper extract or CSV snapshot
-> Tableau TWBX
-> Obsidian embed / Tableau Server
```

Source systems:

| Source | Role |
|---|---|
| lane_delay_events | Raw delay events |
| lane_reliability_scores | Aggregated scorecards |
| dim_lanes | Lane metadata |
| dim_carriers | Carrier metadata |
| fact_route_optimization_events | ASCT and route optimization impact |

Autoclaw configuration:

```yaml
config_file: autoclaw-configs/corridor-extract.yml
schedule: daily_0130_ist
idempotency: "md5(lane_id + cargo_type + extraction_date)"
validation: "reject records with data_confidence = low"
```

Obsidian integration:

```text
Extracted data updates: data/corridors/{lane_id}.md
Scorecards auto-generated: lane_scorecards/{lane_id}.md
Dashboard embedded in: soul.md via iframe
```

## 7. Refresh Instructions

### Offline Sample TWBX

1. Open the packaged workbook in Tableau Desktop.
2. Go to Data -> Extract Data -> Replace Extract.
3. Select the new `.hyper` or CSV source.
4. Save as Tableau Packaged Workbook `.twbx`.
5. Test offline before sharing.

### Production PostgreSQL

1. Data -> New Data Source -> PostgreSQL.
2. Connect to the `zippylogitech` database.
3. Replace sample extracts with live or extract connection.
4. Publish to Tableau Server/Online.
5. Configure hourly extract refresh or live connection.
6. Send failure alerts to the ops/data team.

### Autoclaw Triggered Refresh

```yaml
webhook: "POST Tableau Server REST API refresh endpoint"
trigger: "volume change > 20 percent or lane score drop > 10 points"
payload:
  datasource_id: "<tableau-datasource-id>"
  action: "refresh_now"
```

## 8. Known Limitations and Workarounds

| Limitation | Workaround |
|---|---|
| TWBX cannot embed live DB credentials | Use extract mode for sharing and Tableau Server for live data |
| Sample data may cover only 90 days | Regenerate extract with a wider window |
| Tier 2/3 geocoding may be imprecise | Include custom GeoJSON and validate coordinates |
| ASCT metrics require production routing events | Use sample data for demo, live ASCT table for production |
| Large extracts may slow dashboards | Pre-aggregate to daily/lane materialized views |

## 9. Troubleshooting

| Issue | Check | Action |
|---|---|---|
| Dashboard shows no data | Date filter, source connection, extract timestamp | Widen date filter or refresh extract |
| Lane scores stale | calculation_date in score table | Refresh Autoclaw/Tableau extract |
| Map locations wrong | Geographic role and GeoJSON coordinates | Update custom city coordinates |
| Calculated fields return null | Field names and data types | Use Tableau Describe field |
| Dashboard slow | Extract size and filters | Use materialized views and context filters |

## 10. Support and Ownership

| Area | Owner |
|---|---|
| Business owner | Operations lead |
| Data engineering | Data engineering team |
| Tableau admin | Analytics platform admin |
| Autoclaw issues | Automation/ETL owner |
| Emergency lane issue | Control tower / ops hotline |

## 11. Version History

| Version | Date | Changes |
|---|---|---|
| 1.2.0 | 2026-04-30 | Added ASCT dashboard, Alert_Flag and 90-day sample data |
| 1.1.0 | 2026-04-15 | Added corridor reliability scoring and Obsidian links |
| 1.0.0 | 2026-04-01 | Initial corridor delay dashboard release |

## 12. Quick Reference Commands

Regenerate Hyper extract:

```bash
python scripts/refresh_extract.py --config autoclaw-configs/corridor-extract.yml --output data/extracts/corridors_2026Q2.hyper --days 90
```

Inspect packaged workbook contents:

```bash
unzip -l ZippyLogitech_Corridor_Delay_Analytics.twbx | grep -E "hyper|csv|twb"
```

Obsidian Dataview query:

```dataview
TABLE reliability_score, reliability_grade, avg_delay_min, on_time_pct
FROM "lane_scorecards"
WHERE reliability_grade != "A"
SORT reliability_score ASC
```

## Final Note

This README turns the workbook from a black-box dashboard into a maintainable analytics asset.

Keep it updated whenever data sources, calculated fields, extract schedules or dashboard ownership changes.
