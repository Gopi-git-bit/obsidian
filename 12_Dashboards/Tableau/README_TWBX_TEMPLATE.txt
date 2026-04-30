================================================================================
ZIPPYLOGITECH CORRIDOR DELAY ANALYTICS - DATA SOURCE DOCUMENTATION
================================================================================
Workbook: ZippyLogitech_Corridor_Delay_Analytics.twbx
Version: 1.2.0
Last Updated: 2026-04-30
Owner: Zippy Logistics Operations Analytics
Obsidian Link: dashboards/corridor-analytics
================================================================================

1. WORKBOOK OVERVIEW
================================================================================
Purpose:
  Monitor corridor delay trends, lane reliability scores, and ASCT performance
  for South India logistics operations.

Target Users:
  - Operations Managers: real-time lane monitoring and exception handling
  - Pricing Analysts: risk premium calculations and buffer optimization
  - Executive Leadership: OTIF trends and corridor profitability overview
  - Data Engineers: source validation and extract refresh management

Refresh Schedule:
  - Live Dashboards: every 15 minutes via PostgreSQL/live connection
  - Extract-Based Views: daily at 02:00 IST via Hyper extract refresh
  - Weekly Aggregates: Monday 06:00 IST materialized view rebuild

2. EMBEDDED DATA SOURCES
================================================================================
This packaged workbook can contain:

  Source Name                 Type       Purpose
  corridors_extract.hyper     Extract    Lane-level reliability and corridor scores
  delay_events_sample.hyper   Extract    Shipment-level delay event records
  carriers_benchmarks.csv     CSV        Carrier performance reference
  south_india_cities.geojson  GeoJSON    Custom city/corridor map layer

Important:
  Live PostgreSQL connections are not embedded inside portable TWBX files.
  For production, replace extracts with Tableau Server-managed PostgreSQL
  connections or scheduled extracts.

3. DATA DICTIONARY: CORRIDORS EXTRACT
================================================================================
Table: lane_reliability_scores

  lane_id                  String   Unique corridor identifier, origin:destination:cargo
  origin_city              String   Source city
  destination_city         String   Destination city
  distance_km              Integer  Road distance in km
  primary_cargo            String   Dominant cargo category
  monthly_truckloads       Integer  Estimated monthly truck movements
  backhaul_fill_rate       Decimal  Return-leg utilization from 0.00 to 1.00
  reliability_score        Decimal  Composite lane score from 0 to 100
  reliability_grade        String   A >=85, B 70-84, C 55-69, D/F <55
  recommended_sla_window   Decimal  Suggested delivery window in hours
  requires_backup_carrier  Boolean  Whether backup carrier is needed
  requires_premium_buffer  Boolean  Whether additional buffer is needed
  calculation_date         Date     Score calculation date
  data_confidence          String   high, medium or low

4. DATA DICTIONARY: DELAY EVENTS
================================================================================
Table: lane_delay_events

  shipment_id                  String    Unique shipment identifier
  lane_id                      String    Foreign key to lane score data
  shipment_date                Date      Dispatch date
  scheduled_pickup             DateTime  Planned pickup timestamp
  actual_pickup                DateTime  Actual pickup timestamp
  scheduled_delivery           DateTime  Planned delivery timestamp
  actual_delivery              DateTime  Actual delivery timestamp
  total_delay_min              Integer   Actual minus scheduled delay in minutes
  pickup_delay_min             Integer   Origin-side delay
  transit_delay_min            Integer   En-route delay
  terminal_dwell_delay_min     Integer   Hub/port/warehouse waiting delay
  documentation_delay_min      Integer   E-way bill, invoice, POD or compliance delay
  last_mile_delay_min          Integer   Final delivery delay
  delivered_on_time            Boolean   Delivered inside promised window
  otif_status                  Boolean   On-time and in-full
  carrier_id                   String    Foreign key to carrier reference
  gps_coverage_pct             Decimal   Tracking compliance percentage
  exception_count              Integer   Alerts triggered
  resolution_time_min          Integer   Alert-to-resolution time

5. CALCULATED FIELDS
================================================================================
On_Time_Pct:
  { FIXED [Lane_ID]: SUM(IF [delivered_on_time] THEN 1 ELSE 0 END) / COUNT([shipment_id]) } * 100

OTIF_Pct:
  { FIXED [Lane_ID]: SUM(IF [otif_status] THEN 1 ELSE 0 END) / COUNT([shipment_id]) } * 100

P90_Delay_Min:
  { FIXED [Lane_ID]: PERCENTILE([total_delay_min], 0.90) }

Delay_CV:
  STDEV([total_delay_min]) / AVG([total_delay_min])

Reliability_Grade:
  IF [reliability_score] >= 85 THEN "A"
  ELSEIF [reliability_score] >= 70 THEN "B"
  ELSEIF [reliability_score] >= 55 THEN "C"
  ELSE "D/F" END

Alert_Flag:
  IF [reliability_score] < 55 OR [avg_delay_min] > 300 OR [on_time_pct] < 70 THEN "Critical"
  ELSEIF [reliability_score] < 70 OR [avg_delay_min] > 180 THEN "Warning"
  ELSE "Normal" END

ASCT_Time_Saved_Hrs:
  SUM([time_saved_min]) / 60

ASCT_Cost_Saved_Lakhs:
  SUM([cost_saved_inr]) / 100000

Optimization_Rate:
  { FIXED [Lane_ID]: SUM(IF [route_optimization_applied] THEN 1 ELSE 0 END) / COUNT([shipment_id]) } * 100

6. DATA LINEAGE
================================================================================
PostgreSQL Production DB -> Autoclaw/Python ETL -> Hyper extract or CSV snapshot -> Tableau TWBX -> Obsidian embed/Tableau Server

Source systems:
  - lane_delay_events
  - lane_reliability_scores
  - dim_lanes
  - dim_carriers
  - fact_route_optimization_events

Autoclaw configuration:
  Config File: autoclaw-configs/corridor-extract.yml
  Schedule: Daily 01:30 IST
  Idempotency: md5(lane_id + cargo_type + extraction_date)
  Validation: reject records with data_confidence = low

7. REFRESH INSTRUCTIONS
================================================================================
Offline sample TWBX:
  1. Open workbook in Tableau Desktop.
  2. Data -> Extract Data -> Replace Extract.
  3. Select new Hyper or CSV source.
  4. Save as Tableau Packaged Workbook (.twbx).
  5. Test offline before sharing.

Production PostgreSQL:
  1. Data -> New Data Source -> PostgreSQL.
  2. Connect to zippylogitech database.
  3. Replace sample extracts with live/extract connection.
  4. Publish to Tableau Server/Online.
  5. Configure hourly extract refresh or live connection.

8. KNOWN LIMITATIONS AND WORKAROUNDS
================================================================================
  TWBX cannot embed live DB credentials -> Use extract mode for sharing and Tableau Server for live data.
  Sample data may cover only 90 days -> Regenerate extract with wider window.
  Tier 2/3 geocoding may be imprecise -> Include custom GeoJSON and validate coordinates.
  ASCT metrics need production routing events -> Use sample data for demo, live table for production.
  Large extracts may be slow -> Pre-aggregate to daily/lane materialized views.

9. TROUBLESHOOTING
================================================================================
No data:
  Check date filter, source connection and extract timestamp.

Stale lane scores:
  Check calculation_date and refresh Autoclaw/Tableau extract.

Wrong map locations:
  Check geographic role and custom city coordinates.

Null calculated fields:
  Check field names and data types.

Slow dashboard:
  Use materialized views, extracts and context filters.

10. SUPPORT AND OWNERSHIP
================================================================================
Business owner: Operations lead
Data engineering: Data engineering team
Tableau admin: Analytics platform admin
Autoclaw issues: Automation/ETL owner
Emergency lane issue: Control tower / operations hotline

11. VERSION HISTORY
================================================================================
Version  Date        Changes
1.2.0    2026-04-30  Added ASCT dashboard, Alert_Flag and 90-day sample data
1.1.0    2026-04-15  Added corridor reliability scoring and Obsidian links
1.0.0    2026-04-01  Initial corridor delay dashboard release

12. QUICK REFERENCE COMMANDS
================================================================================
Regenerate Hyper extract:
  python scripts/refresh_extract.py --config autoclaw-configs/corridor-extract.yml --output data/extracts/corridors_2026Q2.hyper --days 90

Inspect packaged workbook contents:
  unzip -l ZippyLogitech_Corridor_Delay_Analytics.twbx | grep -E "hyper|csv|twb"

END OF README
================================================================================
