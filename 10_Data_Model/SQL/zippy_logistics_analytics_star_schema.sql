-- ==========================================
-- ZIPPY LOGISTICS ANALYTICS STAR SCHEMA
-- Target: PostgreSQL 14+
-- Purpose: Corridor delay analytics, OTIF tracking, ASCT performance, BI dashboards
-- ==========================================

CREATE SCHEMA IF NOT EXISTS zippy_logistics;
SET search_path TO zippy_logistics;

-- Required for gen_random_uuid(). Supabase usually enables this already.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ==========================================
-- DIMENSION TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_time (
    date_key DATE PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INT CHECK (day_of_week BETWEEN 0 AND 6),
    day_name TEXT,
    week_of_year INT,
    month INT CHECK (month BETWEEN 1 AND 12),
    month_name TEXT,
    quarter INT CHECK (quarter BETWEEN 1 AND 4),
    year INT,
    is_weekend BOOLEAN DEFAULT false,
    is_holiday BOOLEAN DEFAULT false,
    holiday_name TEXT,
    is_peak_season BOOLEAN DEFAULT false,
    peak_season_type TEXT,
    fiscal_year TEXT
);

COMMENT ON TABLE dim_time IS 'Calendar dimension for time-series filtering, holidays and seasonality analysis.';

CREATE TABLE IF NOT EXISTS dim_lanes (
    lane_id TEXT PRIMARY KEY,
    origin_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    distance_km NUMERIC(8,2) CHECK (distance_km IS NULL OR distance_km >= 0),
    highway TEXT,
    tier_combination TEXT CHECK (tier_combination IN ('T1-T1','T1-T2','T1-T3','T2-T1','T2-T2','T2-T3','T3-T1','T3-T2','T3-T3')),
    primary_cargo TEXT,
    monthly_truckloads_est INT CHECK (monthly_truckloads_est IS NULL OR monthly_truckloads_est >= 0),
    backhaul_fill_rate NUMERIC(5,4) CHECK (backhaul_fill_rate IS NULL OR (backhaul_fill_rate >= 0 AND backhaul_fill_rate <= 1)),
    base_reliability_score NUMERIC(5,2) CHECK (base_reliability_score IS NULL OR (base_reliability_score >= 0 AND base_reliability_score <= 100)),
    is_triangle_candidate BOOLEAN DEFAULT false,
    region TEXT DEFAULT 'south_india',
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    idempotency_key TEXT UNIQUE
);

COMMENT ON TABLE dim_lanes IS 'Master directed corridor table. Store Chennai->Tiruppur separately from Tiruppur->Chennai.';

CREATE TABLE IF NOT EXISTS dim_carriers (
    carrier_id TEXT PRIMARY KEY,
    carrier_name TEXT NOT NULL,
    fleet_size INT CHECK (fleet_size IS NULL OR fleet_size >= 0),
    base_on_time_pct NUMERIC(5,2) CHECK (base_on_time_pct IS NULL OR (base_on_time_pct >= 0 AND base_on_time_pct <= 100)),
    avg_rating NUMERIC(3,1) CHECK (avg_rating IS NULL OR (avg_rating >= 0 AND avg_rating <= 5)),
    compliance_status TEXT CHECK (compliance_status IN ('active','suspended','pending_review')) DEFAULT 'pending_review',
    gps_compliance_pct NUMERIC(5,2) CHECK (gps_compliance_pct IS NULL OR (gps_compliance_pct >= 0 AND gps_compliance_pct <= 100)),
    payment_reliability_score NUMERIC(5,2) CHECK (payment_reliability_score IS NULL OR (payment_reliability_score >= 0 AND payment_reliability_score <= 100)),
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dim_cargo_type (
    cargo_type_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    sub_category TEXT,
    requires_special_handling BOOLEAN DEFAULT false,
    handling_type TEXT CHECK (handling_type IS NULL OR handling_type IN ('reefer','hazmat','esd_safe','moisture_control','covered','low_bed','standard')),
    avg_value_per_ton NUMERIC(12,2) CHECK (avg_value_per_ton IS NULL OR avg_value_per_ton >= 0)
);

CREATE TABLE IF NOT EXISTS dim_vehicle (
    vehicle_type_id TEXT PRIMARY KEY,
    vehicle_class TEXT,
    capacity_tons NUMERIC(6,2) CHECK (capacity_tons IS NULL OR capacity_tons >= 0),
    is_reefer BOOLEAN DEFAULT false,
    is_hazmat_certified BOOLEAN DEFAULT false,
    is_esd_safe BOOLEAN DEFAULT false,
    body_type TEXT
);

-- ==========================================
-- FACT TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_shipment_delays (
    shipment_id TEXT PRIMARY KEY,
    date_key DATE REFERENCES dim_time(date_key),
    lane_id TEXT REFERENCES dim_lanes(lane_id),
    carrier_id TEXT REFERENCES dim_carriers(carrier_id),
    cargo_type_id TEXT REFERENCES dim_cargo_type(cargo_type_id),
    vehicle_type_id TEXT REFERENCES dim_vehicle(vehicle_type_id),

    scheduled_pickup TIMESTAMPTZ,
    actual_pickup TIMESTAMPTZ,
    scheduled_delivery TIMESTAMPTZ,
    actual_delivery TIMESTAMPTZ,

    pickup_delay_min INT DEFAULT 0 CHECK (pickup_delay_min >= 0),
    transit_delay_min INT DEFAULT 0 CHECK (transit_delay_min >= 0),
    terminal_dwell_delay_min INT DEFAULT 0 CHECK (terminal_dwell_delay_min >= 0),
    documentation_delay_min INT DEFAULT 0 CHECK (documentation_delay_min >= 0),
    last_mile_delay_min INT DEFAULT 0 CHECK (last_mile_delay_min >= 0),

    total_delay_min INT GENERATED ALWAYS AS (
        pickup_delay_min + transit_delay_min + terminal_dwell_delay_min + documentation_delay_min + last_mile_delay_min
    ) STORED,

    delivered_on_time BOOLEAN,
    delivered_in_full BOOLEAN,
    damaged BOOLEAN DEFAULT false,
    otif_status BOOLEAN GENERATED ALWAYS AS (
        COALESCE(delivered_on_time, false) AND COALESCE(delivered_in_full, false) AND NOT COALESCE(damaged, false)
    ) STORED,

    gps_coverage_pct NUMERIC(5,2) CHECK (gps_coverage_pct IS NULL OR (gps_coverage_pct >= 0 AND gps_coverage_pct <= 100)),
    exception_count INT DEFAULT 0 CHECK (exception_count >= 0),
    resolution_time_min INT CHECK (resolution_time_min IS NULL OR resolution_time_min >= 0),

    revenue_inr NUMERIC(14,2) CHECK (revenue_inr IS NULL OR revenue_inr >= 0),
    cost_inr NUMERIC(14,2) CHECK (cost_inr IS NULL OR cost_inr >= 0),
    loaded_km NUMERIC(10,2) CHECK (loaded_km IS NULL OR loaded_km >= 0),
    empty_km NUMERIC(10,2) CHECK (empty_km IS NULL OR empty_km >= 0),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    idempotency_key TEXT UNIQUE
);

COMMENT ON TABLE fact_shipment_delays IS 'Atomic shipment-level delay data. Feeds OTIF, P90 delay, waterfall charts and carrier scorecards.';
COMMENT ON COLUMN fact_shipment_delays.total_delay_min IS 'Generated from nonnegative stage-level delay components. Do not update directly in upserts.';
COMMENT ON COLUMN fact_shipment_delays.otif_status IS 'Generated: delivered_on_time AND delivered_in_full AND not damaged.';

CREATE TABLE IF NOT EXISTS fact_lane_performance_daily (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date_key DATE REFERENCES dim_time(date_key),
    lane_id TEXT REFERENCES dim_lanes(lane_id),

    total_shipments INT DEFAULT 0 CHECK (total_shipments >= 0),
    on_time_count INT DEFAULT 0 CHECK (on_time_count >= 0),
    otif_count INT DEFAULT 0 CHECK (otif_count >= 0),
    damaged_count INT DEFAULT 0 CHECK (damaged_count >= 0),

    avg_delay_min NUMERIC(8,2),
    p50_delay_min NUMERIC(8,2),
    p90_delay_min NUMERIC(8,2),
    p95_delay_min NUMERIC(8,2),
    delay_stddev NUMERIC(8,2),

    avg_gps_coverage NUMERIC(5,2),
    avg_exceptions NUMERIC(6,2),
    backhaul_fill_rate_observed NUMERIC(5,4) CHECK (backhaul_fill_rate_observed IS NULL OR (backhaul_fill_rate_observed >= 0 AND backhaul_fill_rate_observed <= 1)),
    avg_rate_per_km NUMERIC(10,2),
    revenue_per_vehicle_day NUMERIC(14,2),

    reliability_score_calculated NUMERIC(5,2) CHECK (reliability_score_calculated IS NULL OR (reliability_score_calculated >= 0 AND reliability_score_calculated <= 100)),
    reliability_grade TEXT CHECK (reliability_grade IS NULL OR reliability_grade IN ('A','B','C','D')),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(date_key, lane_id)
);

COMMENT ON TABLE fact_lane_performance_daily IS 'Pre-aggregated daily metrics optimized for BI trend lines, heatmaps and lane scorecards.';

CREATE TABLE IF NOT EXISTS fact_asct_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    shipment_id TEXT REFERENCES fact_shipment_delays(shipment_id),
    lane_id TEXT REFERENCES dim_lanes(lane_id),

    route_optimization_applied BOOLEAN DEFAULT false,
    original_eta_min NUMERIC(8,2),
    optimized_eta_min NUMERIC(8,2),
    time_saved_min NUMERIC(8,2),
    cost_saved_inr NUMERIC(12,2),

    congestion_avoided BOOLEAN DEFAULT false,
    alternative_route_used TEXT,
    optimization_reason TEXT CHECK (optimization_reason IS NULL OR optimization_reason IN ('traffic','weather','carrier_optimization','accident_avoidance','terminal_dwell','documentation_risk','backhaul_optimization','other')),
    triangle_route_id TEXT,
    empty_km_saved NUMERIC(10,2),
    revenue_lift_pct NUMERIC(8,2),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    idempotency_key TEXT UNIQUE
);

COMMENT ON TABLE fact_asct_performance IS 'Tracks adaptive supply chain / route optimization impact for before-after ETA, cost savings and triangle performance.';

-- ==========================================
-- INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_fact_delays_date ON fact_shipment_delays(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_delays_lane ON fact_shipment_delays(lane_id);
CREATE INDEX IF NOT EXISTS idx_fact_delays_carrier ON fact_shipment_delays(carrier_id);
CREATE INDEX IF NOT EXISTS idx_fact_delays_cargo ON fact_shipment_delays(cargo_type_id);
CREATE INDEX IF NOT EXISTS idx_fact_delays_otif ON fact_shipment_delays(otif_status, date_key);
CREATE INDEX IF NOT EXISTS idx_fact_delays_lane_date ON fact_shipment_delays(lane_id, date_key DESC);

CREATE INDEX IF NOT EXISTS idx_fact_daily_lane_score ON fact_lane_performance_daily(reliability_score_calculated DESC, date_key DESC);
CREATE INDEX IF NOT EXISTS idx_fact_daily_lane_date ON fact_lane_performance_daily(lane_id, date_key DESC);

CREATE INDEX IF NOT EXISTS idx_asct_optimization_lane ON fact_asct_performance(lane_id, route_optimization_applied);
CREATE INDEX IF NOT EXISTS idx_asct_shipment ON fact_asct_performance(shipment_id);
CREATE INDEX IF NOT EXISTS idx_asct_reason_gin ON fact_asct_performance USING GIN(to_tsvector('english', COALESCE(optimization_reason, '')));

-- ==========================================
-- DAILY AGGREGATE REFRESH FUNCTION
-- ==========================================

CREATE OR REPLACE FUNCTION refresh_fact_lane_performance_daily(p_start_date DATE DEFAULT CURRENT_DATE - INTERVAL '7 days')
RETURNS VOID AS $$
BEGIN
    INSERT INTO fact_lane_performance_daily (
        date_key,
        lane_id,
        total_shipments,
        on_time_count,
        otif_count,
        damaged_count,
        avg_delay_min,
        p50_delay_min,
        p90_delay_min,
        p95_delay_min,
        delay_stddev,
        avg_gps_coverage,
        avg_exceptions,
        backhaul_fill_rate_observed,
        avg_rate_per_km,
        reliability_score_calculated,
        reliability_grade,
        updated_at
    )
    WITH agg AS (
        SELECT
            date_key,
            lane_id,
            COUNT(*) AS total_shipments,
            COUNT(*) FILTER (WHERE delivered_on_time = true) AS on_time_count,
            COUNT(*) FILTER (WHERE otif_status = true) AS otif_count,
            COUNT(*) FILTER (WHERE damaged = true) AS damaged_count,
            AVG(total_delay_min) AS avg_delay_min,
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_delay_min) AS p50_delay_min,
            PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_delay_min) AS p90_delay_min,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_delay_min) AS p95_delay_min,
            STDDEV(total_delay_min) AS delay_stddev,
            AVG(gps_coverage_pct) AS avg_gps_coverage,
            AVG(exception_count) AS avg_exceptions,
            SUM(loaded_km) / NULLIF(SUM(loaded_km + empty_km), 0) AS backhaul_fill_rate_observed,
            AVG(revenue_inr / NULLIF(loaded_km, 0)) AS avg_rate_per_km
        FROM fact_shipment_delays
        WHERE date_key >= p_start_date
          AND lane_id IS NOT NULL
        GROUP BY date_key, lane_id
    ), scored AS (
        SELECT
            *,
            LEAST((on_time_count * 100.0 / NULLIF(total_shipments, 0)) * 1.09, 100) AS on_time_score,
            GREATEST(100 - ((COALESCE(delay_stddev, 0) / NULLIF(avg_delay_min, 1)) * 133), 0) AS variability_score,
            COALESCE(avg_gps_coverage, 0) AS tracking_score,
            GREATEST(100 - (COALESCE(avg_exceptions, 0) * 10), 0) AS exception_score
        FROM agg
    ), final_score AS (
        SELECT
            *,
            ROUND((on_time_score * 0.35 + variability_score * 0.25 + tracking_score * 0.20 + exception_score * 0.20)::numeric, 2) AS reliability_score
        FROM scored
    )
    SELECT
        date_key,
        lane_id,
        total_shipments,
        on_time_count,
        otif_count,
        damaged_count,
        ROUND(avg_delay_min::numeric, 2),
        ROUND(p50_delay_min::numeric, 2),
        ROUND(p90_delay_min::numeric, 2),
        ROUND(p95_delay_min::numeric, 2),
        ROUND(delay_stddev::numeric, 2),
        ROUND(avg_gps_coverage::numeric, 2),
        ROUND(avg_exceptions::numeric, 2),
        ROUND(backhaul_fill_rate_observed::numeric, 4),
        ROUND(avg_rate_per_km::numeric, 2),
        reliability_score,
        CASE
            WHEN reliability_score >= 85 THEN 'A'
            WHEN reliability_score >= 70 THEN 'B'
            WHEN reliability_score >= 55 THEN 'C'
            ELSE 'D'
        END AS reliability_grade,
        NOW()
    FROM final_score
    ON CONFLICT (date_key, lane_id) DO UPDATE SET
        total_shipments = EXCLUDED.total_shipments,
        on_time_count = EXCLUDED.on_time_count,
        otif_count = EXCLUDED.otif_count,
        damaged_count = EXCLUDED.damaged_count,
        avg_delay_min = EXCLUDED.avg_delay_min,
        p50_delay_min = EXCLUDED.p50_delay_min,
        p90_delay_min = EXCLUDED.p90_delay_min,
        p95_delay_min = EXCLUDED.p95_delay_min,
        delay_stddev = EXCLUDED.delay_stddev,
        avg_gps_coverage = EXCLUDED.avg_gps_coverage,
        avg_exceptions = EXCLUDED.avg_exceptions,
        backhaul_fill_rate_observed = EXCLUDED.backhaul_fill_rate_observed,
        avg_rate_per_km = EXCLUDED.avg_rate_per_km,
        reliability_score_calculated = EXCLUDED.reliability_score_calculated,
        reliability_grade = EXCLUDED.reliability_grade,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- SAFE UPSERT PATTERN EXAMPLE
-- ==========================================

-- Do not update generated columns total_delay_min or otif_status directly.
-- Update the component fields and outcome flags; PostgreSQL recalculates generated columns.

/*
INSERT INTO fact_shipment_delays (
    shipment_id, date_key, lane_id, carrier_id, cargo_type_id, vehicle_type_id,
    scheduled_pickup, actual_pickup, scheduled_delivery, actual_delivery,
    pickup_delay_min, transit_delay_min, terminal_dwell_delay_min, documentation_delay_min, last_mile_delay_min,
    delivered_on_time, delivered_in_full, damaged,
    gps_coverage_pct, exception_count, resolution_time_min,
    revenue_inr, cost_inr, loaded_km, empty_km,
    idempotency_key
) VALUES (...)
ON CONFLICT (idempotency_key) DO UPDATE SET
    actual_pickup = EXCLUDED.actual_pickup,
    actual_delivery = EXCLUDED.actual_delivery,
    pickup_delay_min = EXCLUDED.pickup_delay_min,
    transit_delay_min = EXCLUDED.transit_delay_min,
    terminal_dwell_delay_min = EXCLUDED.terminal_dwell_delay_min,
    documentation_delay_min = EXCLUDED.documentation_delay_min,
    last_mile_delay_min = EXCLUDED.last_mile_delay_min,
    delivered_on_time = EXCLUDED.delivered_on_time,
    delivered_in_full = EXCLUDED.delivered_in_full,
    damaged = EXCLUDED.damaged,
    gps_coverage_pct = EXCLUDED.gps_coverage_pct,
    exception_count = EXCLUDED.exception_count,
    resolution_time_min = EXCLUDED.resolution_time_min,
    updated_at = NOW();
*/
