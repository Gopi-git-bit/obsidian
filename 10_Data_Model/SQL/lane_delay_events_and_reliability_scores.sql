-- Lane delay events and reliability score tables for Zippy Logistics.
-- Purpose: stage-level delay attribution for lane reliability scoring.

CREATE TABLE IF NOT EXISTS lane_delay_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_id TEXT NOT NULL,
    shipment_id TEXT,
    order_id TEXT,
    leg_id TEXT,

    origin TEXT,
    destination TEXT,
    cargo_type TEXT,
    vehicle_type TEXT,
    carrier_id TEXT,
    driver_id TEXT,

    pickup_delay_min INTEGER DEFAULT 0 CHECK (pickup_delay_min >= 0),
    transit_delay_min INTEGER DEFAULT 0 CHECK (transit_delay_min >= 0),
    terminal_dwell_delay_min INTEGER DEFAULT 0 CHECK (terminal_dwell_delay_min >= 0),
    documentation_delay_min INTEGER DEFAULT 0 CHECK (documentation_delay_min >= 0),
    last_mile_delay_min INTEGER DEFAULT 0 CHECK (last_mile_delay_min >= 0),
    total_delay_min INTEGER GENERATED ALWAYS AS (
        pickup_delay_min + transit_delay_min + terminal_dwell_delay_min + documentation_delay_min + last_mile_delay_min
    ) STORED,

    primary_delay_stage TEXT CHECK (primary_delay_stage IN ('pickup','transit','terminal','documentation','last_mile','none')),
    root_cause_code TEXT,
    weather_condition TEXT,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
    is_peak_season BOOLEAN DEFAULT false,

    delivered_on_time BOOLEAN,
    delivered_in_full BOOLEAN,
    damaged BOOLEAN DEFAULT false,
    gps_coverage_pct NUMERIC(5,2) CHECK (gps_coverage_pct BETWEEN 0 AND 100),
    exception_count INTEGER DEFAULT 0 CHECK (exception_count >= 0),
    resolution_time_min INTEGER CHECK (resolution_time_min IS NULL OR resolution_time_min >= 0),

    source_system TEXT,
    data_confidence TEXT CHECK (data_confidence IN ('high','medium','low')) DEFAULT 'medium',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    event_date DATE DEFAULT CURRENT_DATE,
    idempotency_key TEXT UNIQUE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lane_delay_events_lane_date
ON lane_delay_events(lane_id, event_date DESC);

CREATE INDEX IF NOT EXISTS idx_lane_delay_events_context
ON lane_delay_events(cargo_type, vehicle_type, data_confidence);

CREATE INDEX IF NOT EXISTS idx_lane_delay_events_root_cause
ON lane_delay_events(primary_delay_stage, root_cause_code);

CREATE TABLE IF NOT EXISTS lane_reliability_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_id TEXT NOT NULL,
    origin TEXT,
    destination TEXT,
    cargo_type TEXT,
    vehicle_type TEXT,
    calculation_window_days INTEGER DEFAULT 90,
    calculation_date DATE DEFAULT CURRENT_DATE,

    total_shipments INTEGER NOT NULL,
    on_time_pct NUMERIC(6,2),
    otif_pct NUMERIC(6,2),
    avg_delay_min NUMERIC(10,2),
    p50_delay_min NUMERIC(10,2),
    p90_delay_min NUMERIC(10,2),
    p99_delay_min NUMERIC(10,2),
    delay_stddev_min NUMERIC(10,2),
    delay_cv NUMERIC(10,4),

    carrier_consistency_score NUMERIC(6,2),
    terminal_reliability_pct NUMERIC(6,2),
    tracking_coverage_pct NUMERIC(6,2),
    exception_resolution_speed NUMERIC(6,2),
    reliability_score NUMERIC(6,2),
    reliability_grade TEXT CHECK (reliability_grade IN ('A','B','C','D')),

    agent_action TEXT,
    recommended_sla_window_hours NUMERIC(6,2),
    requires_backup_carrier BOOLEAN DEFAULT false,
    pricing_premium_pct NUMERIC(6,2) DEFAULT 0,
    data_confidence TEXT CHECK (data_confidence IN ('high','medium','low')) DEFAULT 'medium',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    idempotency_key TEXT UNIQUE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_lane_reliability_scores_lane_date
ON lane_reliability_scores(lane_id, calculation_date DESC);

CREATE INDEX IF NOT EXISTS idx_lane_reliability_scores_grade
ON lane_reliability_scores(reliability_grade, reliability_score DESC);

-- Daily calculation query skeleton. Use as a materialization job or n8n PostgreSQL node.
WITH lane_aggregates AS (
    SELECT
        lane_id,
        origin,
        destination,
        cargo_type,
        vehicle_type,
        COUNT(*) AS total_shipments,
        COUNT(*) FILTER (WHERE delivered_on_time = true) * 100.0 / NULLIF(COUNT(*), 0) AS on_time_pct,
        COUNT(*) FILTER (WHERE delivered_on_time = true AND delivered_in_full = true) * 100.0 / NULLIF(COUNT(*), 0) AS otif_pct,
        AVG(total_delay_min) AS avg_delay_min,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_delay_min) AS p50_delay_min,
        PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_delay_min) AS p90_delay_min,
        PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY total_delay_min) AS p99_delay_min,
        STDDEV(total_delay_min) AS delay_stddev_min,
        COUNT(DISTINCT carrier_id) AS unique_carriers,
        AVG(gps_coverage_pct) AS avg_gps_coverage,
        AVG(CASE WHEN exception_count > 0 THEN resolution_time_min END) AS avg_resolution_time,
        AVG(CASE WHEN terminal_dwell_delay_min > 0 THEN terminal_dwell_delay_min END) AS avg_terminal_dwell
    FROM lane_delay_events
    WHERE event_date >= CURRENT_DATE - INTERVAL '90 days'
      AND data_confidence IN ('high','medium')
    GROUP BY lane_id, origin, destination, cargo_type, vehicle_type
    HAVING COUNT(*) >= 30
), scored AS (
    SELECT
        *,
        delay_stddev_min / NULLIF(avg_delay_min, 1) AS delay_cv,
        LEAST(on_time_pct * 1.09, 100) AS on_time_score,
        GREATEST(100 - ((delay_stddev_min / NULLIF(avg_delay_min, 1)) * 133), 0) AS variability_score,
        GREATEST(100 - ((unique_carriers - 1) * 20), 0) AS carrier_consistency_score,
        GREATEST(100 - (COALESCE(avg_terminal_dwell, 0) / 60.0 * 25), 0) AS terminal_reliability_pct,
        COALESCE(avg_gps_coverage, 0) AS tracking_coverage_pct,
        GREATEST(100 - ((COALESCE(avg_resolution_time, 60) - 30) / 90.0 * 100), 0) AS exception_resolution_speed
    FROM lane_aggregates
)
SELECT
    lane_id,
    origin,
    destination,
    cargo_type,
    vehicle_type,
    total_shipments,
    ROUND(on_time_pct, 2) AS on_time_pct,
    ROUND(otif_pct, 2) AS otif_pct,
    ROUND(avg_delay_min, 2) AS avg_delay_min,
    ROUND(p50_delay_min::numeric, 2) AS p50_delay_min,
    ROUND(p90_delay_min::numeric, 2) AS p90_delay_min,
    ROUND(p99_delay_min::numeric, 2) AS p99_delay_min,
    ROUND(delay_stddev_min, 2) AS delay_stddev_min,
    ROUND(delay_cv, 4) AS delay_cv,
    ROUND((
        on_time_score * 0.30 +
        variability_score * 0.20 +
        carrier_consistency_score * 0.15 +
        terminal_reliability_pct * 0.15 +
        tracking_coverage_pct * 0.10 +
        exception_resolution_speed * 0.10
    ), 2) AS reliability_score
FROM scored;
