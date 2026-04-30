---
type: tableau_workbook_spec
name: ZippyLogitech Corridor Delay Analytics
domain: logistics_control_tower
status: active
created_at: 2026-04-30
linked_dashboard: "Corridor Delay Trends and Performance Dashboard Template"
---
# Tableau Workbook Spec: ZippyLogitech Corridor Delay Analytics

## Workbook Overview

```yaml
workbook_name: "ZippyLogitech_Corridor_Delay_Analytics.twbx"
tableau_version: "2024.2 or later"
refresh_mode: "Live PostgreSQL or hourly extract"
dashboards:
  - Executive Overview
  - Corridor Deep Dive
  - ASCT Performance
  - Predictive Alerts
sample_data_folder: "12_Dashboards/Tableau/sample_data"
```

## Data Connections

### Prototype Mode

Use the sample CSV files:

```text
sample_lane_delay_events.csv
sample_lane_reliability_scores.csv
sample_asct_performance.csv
```

Relationships:

```text
lane_delay_events.lane_id = lane_reliability_scores.lane_id
lane_delay_events.shipment_id = asct_performance.shipment_id
```

### Production Mode

Connect Tableau Desktop to PostgreSQL and use the dashboard star schema or materialized views:

```text
mv_corridor_delay_core_daily
mv_corridor_delay_lane_rolling_90d
mv_carrier_delay_performance_rolling_90d
fact_route_optimization_events
```

## Tableau Calculated Fields

### On-Time Percentage

```tableau
{ FIXED [lane_id]:
    SUM(IF [delivered_on_time] = TRUE THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

### OTIF Percentage

```tableau
{ FIXED [lane_id]:
    SUM(IF [otif_status] = TRUE THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

### Average Delay Hours

```tableau
AVG([total_delay_min]) / 60
```

### P90 Delay Minutes

```tableau
{ FIXED [lane_id]:
    PERCENTILE([total_delay_min], 0.90)
}
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

### Delay Category

```tableau
IF [total_delay_min] <= 60 THEN "On Time <=1hr"
ELSEIF [total_delay_min] <= 180 THEN "Moderate 1-3hrs"
ELSEIF [total_delay_min] <= 300 THEN "High 3-5hrs"
ELSE "Critical >5hrs"
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
{ FIXED [lane_id]:
    SUM(IF [route_optimization_applied] = TRUE THEN 1 ELSE 0 END)
    / COUNT([shipment_id])
} * 100
```

### Alert Flag

```tableau
IF [reliability_score] < 55 OR [avg_delay_min] > 300 OR [on_time_pct] < 70 THEN "Critical"
ELSEIF [reliability_score] < 70 OR [avg_delay_min] > 180 THEN "Warning"
ELSE "Normal"
END
```

### Recommended Action

```tableau
IF [Alert_Flag] = "Critical" THEN "Immediate ops review + carrier audit"
ELSEIF [Alert_Flag] = "Warning" THEN "Add buffer + monitor 7-day trend"
ELSE "No action required"
END
```

## Parameters

| Parameter | Type | Values | Use |
|---|---|---|---|
| Buffer_Adjustment_Min | Integer | -30 to +60 step 5 | SLA buffer what-if |
| Date_Range | Date range | 7/30/90 days | Time filtering |
| Cargo_Type_Filter | String | All/list | Cargo-specific analysis |
| Carrier_Filter | String | All/list | Carrier performance |
| Tier_Combination | String | T1-T2, T2-T3, T1-T3 | Tier segmentation |

## Worksheet Specifications

### WS1: KPI Cards

| Card | Calculation | Format | Color Logic |
|---|---|---|---|
| On-Time % | On-Time Percentage | 1 decimal | Green >=85, Yellow 75-85, Red <75 |
| Avg Delay | Average Delay Hours | 1 decimal hrs | Green <=2, Yellow 2-4, Red >4 |
| P90 Delay | P90 Delay Minutes | 0 decimals | Green <=180, Yellow 180-300, Red >300 |
| Active Lanes | COUNTD(lane_id) | number | neutral |
| ASCT Time Saved | ASCT Time Saved Hours | 1 decimal hrs | blue accent |

### WS2: Corridor Heatmap Map

Marks:

```text
Color: Reliability Grade
Size: total shipments
Tooltip: lane_id, reliability score, avg delay, OTIF, backhaul fill rate
```

### WS3: Delay Trend Line

```text
Columns: shipment_date continuous day
Rows: AVG(total_delay_min), P90 Delay Minutes
Reference line: 120 min target
Forecast: 7 days
```

### WS4: Delay Component Waterfall

Components:

```text
Pickup -> Transit -> Terminal Dwell -> Documentation -> Last Mile
```

Measure:

```text
AVG(component delay minutes)
```

### WS5: Volume vs Delay Scatter

```text
X: monthly truckloads or total shipments
Y: avg delay minutes
Size: revenue or shipments
Color: reliability grade
Detail: lane_id
Reference lines: median volume, 120-min delay target
```

### WS6: ASCT Before/After Comparison

```text
Columns: optimization status
Rows: original_eta_min and optimized_eta_min
Tooltip: time saved, cost saved, reason
```

### WS7: Alert Table

Columns:

```text
lane_id
reliability_grade
avg_delay_min
on_time_pct
alert_flag
recommended_action
```

Filter:

```text
Alert_Flag != Normal
```

## Dashboard Layouts

### Dashboard 1: Executive Overview

```text
KPI Cards Row
Corridor Heatmap Map | Delay Trend Line
Top 5 Problem Lanes | Volume vs Delay Scatter
```

### Dashboard 2: Corridor Deep Dive

```text
Left filters: Lane, Date, Cargo, Carrier, Tier
Delay Component Waterfall
Performance by Day/Hour Heatmap
Volume and Delay Dual-Axis Trend
```

### Dashboard 3: ASCT Performance

```text
ASCT KPI Cards
Before/After ETA Comparison
Alternative Routes Map
Optimization Reasons Pareto
```

### Dashboard 4: Predictive Alerts

```text
Critical Alert Table
Delay Risk by Hour/Day Heatmap
7-Day Delay Forecast
Buffer What-If Analysis
```

## Conditional Formatting

| Metric | Green | Yellow | Red |
|---|---:|---:|---:|
| on_time_pct | >=85 percent | 75-85 percent | <75 percent |
| avg_delay_min | <=120 | 120-240 | >240 |
| p90_delay_min | <=180 | 180-300 | >300 |
| reliability_score | >=85 | 70-85 | <70 |
| backhaul_fill_rate | >=0.75 | 0.60-0.75 | <0.60 |

## Build Steps

1. Connect to sample CSV files.
2. Create relationships on lane_id and shipment_id.
3. Add calculated fields.
4. Create parameters and global filters.
5. Build worksheets WS1-WS7.
6. Assemble four dashboards.
7. Apply Tableau theme from `zippy_tableau_theme.json`.
8. Publish to Tableau Server/Online.
9. Configure subscriptions and critical alerts.

## Publishing Rules

```yaml
project: "ZippyLogitech_Operations"
permissions:
  ops_team: "View + Interact"
  management: "View + Export"
  data_engineers: "Edit + Refresh"
extract_schedule:
  mode: "Incremental"
  key_field: "shipment_date"
  frequency: "Every 1 hour"
  timezone: "Asia/Kolkata"
```

## Takeaway

This workbook should be treated as an operations cockpit, not a presentation deck.

If a chart does not help someone reroute, add buffer, audit a carrier, change a hub, price risk or escalate, remove it.

## Packaged Workbook Guidance

For `.twbx` packaging rules, supported embeddable data sources, portability checklist and README guidance, see [[Tableau Packaged Workbook Data Source Guide]].

Additional compact prototype samples are available:

```text
sample_data/sample_corridors.csv
sample_data/sample_carriers.csv
README_TWBX_TEMPLATE.txt
```
