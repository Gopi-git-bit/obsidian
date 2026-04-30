-- Corridor dashboard star schema for Power BI / Tableau.
-- Designed to sit on top of operational tables such as lane_delay_events and lane_reliability_scores.

CREATE TABLE IF NOT EXISTS dim_lanes (
    lane_id TEXT PRIMARY KEY,
    origin_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    distance_km NUMERIC(10,2),
    highway TEXT,
    tier_combination TEXT,
    primary_cargo_type TEXT,
    backhaul_potential_score NUMERIC(5,2),
    is_triangle_candidate BOOLEAN DEFAULT false,
    region TEXT DEFAULT 'south_india'
);

CREATE TABLE IF NOT EXISTS dim_carriers (
    carrier_id TEXT PRIMARY KEY,
    carrier_name TEXT,
    fleet_size INTEGER,
    reliability_rating NUMERIC(5,2),
    on_time_pct NUMERIC(6,2),
    gps_compliance_pct NUMERIC(6,2),
    payment_reliability_score NUMERIC(5,2)
);

CREATE TABLE IF NOT EXISTS dim_cargo_type (
    cargo_type_id TEXT PRIMARY KEY,
    cargo_category TEXT NOT NULL,
    requires_special_handling BOOLEAN DEFAULT false,
    requires_reefer BOOLEAN DEFAULT false,
    requires_hazmat BOOLEAN DEFAULT false,
    requires_esd BOOLEAN DEFAULT false,
    avg_value_per_ton NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS dim_vehicle (
    vehicle_id TEXT PRIMARY KEY,
    vehicle_type TEXT,
    capacity_ton NUMERIC(8,2),
    body_type TEXT,
    reefer_enabled BOOLEAN DEFAULT false,
    hazmat_certified BOOLEAN DEFAULT false,
    esd_safe BOOLEAN DEFAULT false,
    current_status TEXT
);

CREATE TABLE IF NOT EXISTS dim_time (
    date DATE PRIMARY KEY,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
    day_name TEXT,
    week_of_year INTEGER,
    month INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_peak_season BOOLEAN DEFAULT false,
    is_holiday BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS fact_shipment_delays (
    shipment_id TEXT PRIMARY KEY,
    lane_id TEXT REFERENCES dim_lanes(lane_id),
    carrier_id TEXT REFERENCES dim_carriers(carrier_id),
    vehicle_id TEXT REFERENCES dim_vehicle(vehicle_id),
    cargo_type_id TEXT REFERENCES dim_cargo_type(cargo_type_id),
    shipment_date DATE REFERENCES dim_time(date),

    scheduled_pickup TIMESTAMPTZ,
    actual_pickup TIMESTAMPTZ,
    scheduled_delivery TIMESTAMPTZ,
    actual_delivery TIMESTAMPTZ,

    total_delay_min INTEGER DEFAULT 0,
    pickup_delay_min INTEGER DEFAULT 0,
    transit_delay_min INTEGER DEFAULT 0,
    terminal_dwell_delay_min INTEGER DEFAULT 0,
    documentation_delay_min INTEGER DEFAULT 0,
    last_mile_delay_min INTEGER DEFAULT 0,

    delivered_on_time BOOLEAN,
    otif_status BOOLEAN,
    damaged BOOLEAN DEFAULT false,
    revenue_inr NUMERIC(12,2),
    cost_inr NUMERIC(12,2),
    empty_km NUMERIC(10,2),
    loaded_km NUMERIC(10,2),
    idempotency_key TEXT UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_fact_shipment_delays_lane_date
ON fact_shipment_delays(lane_id, shipment_date DESC);

CREATE INDEX IF NOT EXISTS idx_fact_shipment_delays_carrier_date
ON fact_shipment_delays(carrier_id, shipment_date DESC);

CREATE TABLE IF NOT EXISTS fact_lane_performance_daily (
    date DATE REFERENCES dim_time(date),
    lane_id TEXT REFERENCES dim_lanes(lane_id),
    total_shipments INTEGER,
    on_time_count INTEGER,
    otif_count INTEGER,
    avg_delay_min NUMERIC(10,2),
    p90_delay_min NUMERIC(10,2),
    p95_delay_min NUMERIC(10,2),
    reliability_score NUMERIC(6,2),
    reliability_grade TEXT CHECK (reliability_grade IN ('A','B','C','D')),
    backhaul_fill_rate NUMERIC(6,4),
    avg_rate_per_km NUMERIC(10,2),
    revenue_per_vehicle_day NUMERIC(12,2),
    PRIMARY KEY (date, lane_id)
);

CREATE INDEX IF NOT EXISTS idx_fact_lane_performance_daily_score
ON fact_lane_performance_daily(reliability_score, date DESC);

CREATE TABLE IF NOT EXISTS fact_route_optimization_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    lane_id TEXT REFERENCES dim_lanes(lane_id),
    shipment_id TEXT,
    route_optimization_applied BOOLEAN DEFAULT false,
    optimization_reason TEXT,
    original_eta_min INTEGER,
    optimized_eta_min INTEGER,
    time_saved_min INTEGER,
    cost_saved_inr NUMERIC(12,2),
    congestion_avoided BOOLEAN DEFAULT false,
    alternative_route_used TEXT,
    triangle_route_id TEXT,
    empty_km_saved NUMERIC(10,2),
    revenue_lift_pct NUMERIC(8,2),
    idempotency_key TEXT UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_fact_route_optimization_events_lane_time
ON fact_route_optimization_events(lane_id, event_timestamp DESC);

-- Example daily aggregate upsert from fact_shipment_delays.
INSERT INTO fact_lane_performance_daily (
    date,
    lane_id,
    total_shipments,
    on_time_count,
    otif_count,
    avg_delay_min,
    p90_delay_min,
    p95_delay_min,
    reliability_score,
    reliability_grade,
    backhaul_fill_rate,
    avg_rate_per_km
)
SELECT
    shipment_date AS date,
    lane_id,
    COUNT(*) AS total_shipments,
    COUNT(*) FILTER (WHERE delivered_on_time = true) AS on_time_count,
    COUNT(*) FILTER (WHERE otif_status = true) AS otif_count,
    AVG(total_delay_min) AS avg_delay_min,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_delay_min) AS p90_delay_min,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_delay_min) AS p95_delay_min,
    NULL AS reliability_score,
    NULL AS reliability_grade,
    AVG(CASE WHEN loaded_km + empty_km > 0 THEN loaded_km / NULLIF(loaded_km + empty_km, 0) ELSE NULL END) AS backhaul_fill_rate,
    AVG(CASE WHEN loaded_km > 0 THEN revenue_inr / NULLIF(loaded_km, 0) ELSE NULL END) AS avg_rate_per_km
FROM fact_shipment_delays
GROUP BY shipment_date, lane_id
ON CONFLICT (date, lane_id) DO UPDATE SET
    total_shipments = EXCLUDED.total_shipments,
    on_time_count = EXCLUDED.on_time_count,
    otif_count = EXCLUDED.otif_count,
    avg_delay_min = EXCLUDED.avg_delay_min,
    p90_delay_min = EXCLUDED.p90_delay_min,
    p95_delay_min = EXCLUDED.p95_delay_min,
    backhaul_fill_rate = EXCLUDED.backhaul_fill_rate,
    avg_rate_per_km = EXCLUDED.avg_rate_per_km;
