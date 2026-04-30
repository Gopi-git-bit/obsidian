---
type: data_model_doc
schema: zippy_logistics
table: dim_time
status: active
created_at: 2026-04-30
script: "10_Data_Model/SQL/populate_dim_time_india_logistics.sql"
---
# dim_time India Logistics Calendar

## Purpose

The `dim_time` logistics calendar turns dates into operating signals for South India corridor analytics.

It supports:

- holiday filtering
- peak season analysis
- textile export season buffers
- agri harvest season planning
- monsoon and ghat route risk
- port congestion buffers
- driver shortage risk
- fiscal-year reporting

## Script

```text
10_Data_Model/SQL/populate_dim_time_india_logistics.sql
```

## Important Implementation Notes

The script is safe to re-run.

It does not truncate `dim_time`, because fact tables may reference existing dates. Instead it uses:

```sql
INSERT ... ON CONFLICT (date_key) DO UPDATE
```

The script also adds missing logistics columns if the base star schema already exists.

## Precision Note

Fixed-date holidays are deterministic.

Lunar and regional festival dates are planning approximations unless refreshed from an official calendar/API. This is enough for dashboard seasonality and buffer planning, but not enough for legal holiday compliance.

## Key Flags

| Column | Meaning |
|---|---|
| is_holiday | National/regional holiday flag |
| holiday_name | Holiday or season name |
| holiday_type | national, regional_south or national_lunar |
| is_textile_export_peak | Aug-Jan textile/export cycle |
| is_agri_harvest_kharif | Oct-Nov harvest peak |
| is_agri_harvest_rabi | Mar-Apr harvest peak |
| is_monsoon_southwest | Jun-Sep weather/route risk |
| is_monsoon_northeast | Oct-Dec TN/coastal weather risk |
| is_festival_retail_peak | Oct-Jan retail surge |
| is_construction_season | Oct-Mar construction demand |
| is_port_congestion_peak | Nov-Feb export/port congestion risk |
| is_driver_shortage_risk | Festival/harvest availability risk |
| is_ghat_route_risk | Jun-Oct hill/ghat road risk |
| peak_season_type | Comma-separated season labels |

## Agent Usage

### Pricing Agent

```text
If is_peak_season = true, apply seasonal capacity/risk premium.
If is_driver_shortage_risk = true, increase backup carrier requirement.
```

### Matching Agent

```text
If is_ghat_route_risk = true and route includes ghat corridor, prefer safer alternate route or add buffer.
```

### Risk Agent

```text
If holiday + monsoon + time-sensitive cargo overlap, escalate to control tower before promise.
```

## Example Queries

Check date range:

```sql
SELECT MIN(date_key), MAX(date_key), COUNT(*)
FROM zippy_logistics.dim_time;
```

Average textile delay during export peak vs off-peak:

```sql
SELECT
    dt.is_textile_export_peak,
    AVG(fsd.total_delay_min) AS avg_delay_min,
    COUNT(*) AS shipment_count
FROM zippy_logistics.fact_shipment_delays fsd
JOIN zippy_logistics.dim_time dt ON fsd.date_key = dt.date_key
WHERE fsd.lane_id LIKE '%:textiles'
GROUP BY dt.is_textile_export_peak;
```

Holiday and monsoon overlap:

```sql
SELECT date_key, holiday_name
FROM zippy_logistics.dim_time
WHERE is_holiday = true
  AND (is_monsoon_southwest = true OR is_monsoon_northeast = true)
ORDER BY date_key;
```

## Dashboard Use

Use these fields as slicers and conditional formatting signals in Tableau/Power BI:

```text
is_peak_season
peak_season_type
is_textile_export_peak
is_port_congestion_peak
is_driver_shortage_risk
is_ghat_route_risk
```

## Takeaway

This table is not just a calendar.

It is a planning signal that helps Zippy promise carefully before the network gets stressed.
