-- Materialized views for fast Power BI / Tableau corridor delay dashboards.
-- These views assume fact_shipment_delays, dim_lanes, dim_carriers and dim_time exist.

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_corridor_delay_core_daily AS
SELECT
    fsd.shipment_date AS date,
    fsd.lane_id,
    dl.origin_city,
    dl.destination_city,
    dl.tier_combination,
    dl.primary_cargo_type,
    COUNT(*) AS total_shipments,
    AVG(fsd.total_delay_min) AS avg_delay_min,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY fsd.total_delay_min) AS p90_delay_min,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY fsd.total_delay_min) AS p95_delay_min,
    STDDEV(fsd.total_delay_min) AS delay_stddev_min,
    COUNT(*) FILTER (WHERE fsd.delivered_on_time = true) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_pct,
    COUNT(*) FILTER (WHERE fsd.otif_status = true) * 100.0 / NULLIF(COUNT(*), 0) AS otif_pct,
    AVG(fsd.pickup_delay_min) AS pickup_delay_min,
    AVG(fsd.transit_delay_min) AS transit_delay_min,
    AVG(fsd.terminal_dwell_delay_min) AS terminal_dwell_delay_min,
    AVG(fsd.documentation_delay_min) AS documentation_delay_min,
    AVG(fsd.last_mile_delay_min) AS last_mile_delay_min,
    SUM(fsd.empty_km) / NULLIF(SUM(fsd.empty_km + fsd.loaded_km), 0) * 100.0 AS empty_mile_pct
FROM fact_shipment_delays fsd
LEFT JOIN dim_lanes dl ON fsd.lane_id = dl.lane_id
GROUP BY fsd.shipment_date, fsd.lane_id, dl.origin_city, dl.destination_city, dl.tier_combination, dl.primary_cargo_type;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_corridor_delay_core_daily_key
ON mv_corridor_delay_core_daily(date, lane_id);

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_corridor_delay_lane_rolling_90d AS
SELECT
    fsd.lane_id,
    dl.origin_city,
    dl.destination_city,
    dl.tier_combination,
    COUNT(*) AS total_shipments_90d,
    AVG(fsd.total_delay_min) AS avg_delay_min_90d,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY fsd.total_delay_min) AS p90_delay_min_90d,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY fsd.total_delay_min) AS p95_delay_min_90d,
    STDDEV(fsd.total_delay_min) AS delay_stddev_min_90d,
    STDDEV(fsd.total_delay_min) / NULLIF(AVG(fsd.total_delay_min), 0) AS delay_cv_90d,
    COUNT(*) FILTER (WHERE fsd.delivered_on_time = true) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_pct_90d,
    COUNT(*) FILTER (WHERE fsd.otif_status = true) * 100.0 / NULLIF(COUNT(*), 0) AS otif_pct_90d,
    AVG(fsd.pickup_delay_min) AS pickup_delay_min_90d,
    AVG(fsd.transit_delay_min) AS transit_delay_min_90d,
    AVG(fsd.terminal_dwell_delay_min) AS terminal_dwell_delay_min_90d,
    AVG(fsd.documentation_delay_min) AS documentation_delay_min_90d,
    AVG(fsd.last_mile_delay_min) AS last_mile_delay_min_90d,
    SUM(fsd.empty_km) / NULLIF(SUM(fsd.empty_km + fsd.loaded_km), 0) * 100.0 AS empty_mile_pct_90d
FROM fact_shipment_delays fsd
LEFT JOIN dim_lanes dl ON fsd.lane_id = dl.lane_id
WHERE fsd.shipment_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY fsd.lane_id, dl.origin_city, dl.destination_city, dl.tier_combination;

CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_corridor_delay_lane_rolling_90d_key
ON mv_corridor_delay_lane_rolling_90d(lane_id);

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_carrier_delay_performance_rolling_90d AS
SELECT
    fsd.carrier_id,
    dc.carrier_name,
    fsd.lane_id,
    COUNT(*) AS total_shipments_90d,
    AVG(fsd.total_delay_min) AS avg_delay_min_90d,
    COUNT(*) FILTER (WHERE fsd.delivered_on_time = true) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_pct_90d,
    COUNT(*) FILTER (WHERE fsd.otif_status = true) * 100.0 / NULLIF(COUNT(*), 0) AS otif_pct_90d,
    COUNT(*) FILTER (WHERE fsd.damaged = false) * 100.0 / NULLIF(COUNT(*), 0) AS damage_free_pct_90d,
    AVG(fsd.empty_km) AS avg_empty_km_90d,
    AVG(fsd.loaded_km) AS avg_loaded_km_90d
FROM fact_shipment_delays fsd
LEFT JOIN dim_carriers dc ON fsd.carrier_id = dc.carrier_id
WHERE fsd.shipment_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY fsd.carrier_id, dc.carrier_name, fsd.lane_id;

CREATE INDEX IF NOT EXISTS idx_mv_carrier_delay_performance_rolling_90d_lane
ON mv_carrier_delay_performance_rolling_90d(lane_id, avg_delay_min_90d DESC);

-- Refresh command for n8n / cron.
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_corridor_delay_core_daily;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_corridor_delay_lane_rolling_90d;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_carrier_delay_performance_rolling_90d;
