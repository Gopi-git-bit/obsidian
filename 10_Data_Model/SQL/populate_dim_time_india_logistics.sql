-- ==========================================
-- DIM_TIME POPULATION: INDIA HOLIDAYS AND LOGISTICS SEASONALITY
-- Target: PostgreSQL 14+
-- Scope: 2024-01-01 to 2028-12-31
-- Schema: zippy_logistics
-- Notes:
--   - Fixed national holidays are deterministic.
--   - Lunar/regional festival dates are approximate planning signals unless refreshed by an official/API source.
--   - Safe to re-run. Uses UPSERT and does not truncate dependent fact tables.
-- ==========================================

CREATE SCHEMA IF NOT EXISTS zippy_logistics;
SET search_path TO zippy_logistics;

-- Ensure dim_time exists. Main definition lives in zippy_logistics_analytics_star_schema.sql.
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

-- Add logistics-specific calendar columns if the base star schema is already installed.
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS holiday_type TEXT;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_textile_export_peak BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_agri_harvest_kharif BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_agri_harvest_rabi BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_monsoon_southwest BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_monsoon_northeast BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_festival_retail_peak BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_construction_season BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_port_congestion_peak BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_driver_shortage_risk BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS is_ghat_route_risk BOOLEAN DEFAULT false;
ALTER TABLE dim_time ADD COLUMN IF NOT EXISTS last_updated TIMESTAMPTZ DEFAULT NOW();

WITH base_calendar AS (
    SELECT
        gs::date AS date_key,
        EXTRACT(DOW FROM gs)::int AS day_of_week,
        TRIM(TO_CHAR(gs, 'Day')) AS day_name,
        EXTRACT(WEEK FROM gs)::int AS week_of_year,
        EXTRACT(MONTH FROM gs)::int AS month,
        TRIM(TO_CHAR(gs, 'Month')) AS month_name,
        EXTRACT(QUARTER FROM gs)::int AS quarter,
        EXTRACT(YEAR FROM gs)::int AS year,
        CASE WHEN EXTRACT(DOW FROM gs) IN (0, 6) THEN true ELSE false END AS is_weekend,
        CASE
            WHEN EXTRACT(MONTH FROM gs) >= 4
            THEN EXTRACT(YEAR FROM gs)::text || '-' || (EXTRACT(YEAR FROM gs) + 1)::text
            ELSE (EXTRACT(YEAR FROM gs) - 1)::text || '-' || EXTRACT(YEAR FROM gs)::text
        END AS fiscal_year
    FROM generate_series(DATE '2024-01-01', DATE '2028-12-31', INTERVAL '1 day') AS gs
), holiday_seed AS (
    -- Fixed national holidays
    SELECT make_date(year, 1, 26) AS date_key, 'Republic Day' AS holiday_name, 'national' AS holiday_type FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 8, 15), 'Independence Day', 'national' FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 10, 2), 'Gandhi Jayanti', 'national' FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 12, 25), 'Christmas', 'national' FROM generate_series(2024, 2028) AS year

    -- Fixed/approx South India planning holidays
    UNION ALL SELECT make_date(year, 1, 13), 'Pongal Day 1 / Bhogi', 'regional_south' FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 1, 14), 'Thai Pongal', 'regional_south' FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 1, 15), 'Mattu Pongal / Kanuma', 'regional_south' FROM generate_series(2024, 2028) AS year
    UNION ALL SELECT make_date(year, 4, 14), 'Tamil New Year / Vishu', 'regional_south' FROM generate_series(2024, 2028) AS year

    -- Approximate lunar/festival dates for planning only. Refresh with API/official source for production precision.
    UNION ALL SELECT DATE '2024-11-01', 'Diwali / Deepavali approx', 'national_lunar'
    UNION ALL SELECT DATE '2025-10-20', 'Diwali / Deepavali approx', 'national_lunar'
    UNION ALL SELECT DATE '2026-11-08', 'Diwali / Deepavali approx', 'national_lunar'
    UNION ALL SELECT DATE '2027-10-28', 'Diwali / Deepavali approx', 'national_lunar'
    UNION ALL SELECT DATE '2028-11-16', 'Diwali / Deepavali approx', 'national_lunar'

    UNION ALL SELECT DATE '2024-03-25', 'Holi approx', 'national_lunar'
    UNION ALL SELECT DATE '2025-03-14', 'Holi approx', 'national_lunar'
    UNION ALL SELECT DATE '2026-03-03', 'Holi approx', 'national_lunar'
    UNION ALL SELECT DATE '2027-03-22', 'Holi approx', 'national_lunar'
    UNION ALL SELECT DATE '2028-03-11', 'Holi approx', 'national_lunar'

    UNION ALL SELECT DATE '2024-10-12', 'Dussehra / Vijayadashami approx', 'national_lunar'
    UNION ALL SELECT DATE '2025-10-02', 'Dussehra / Vijayadashami approx', 'national_lunar'
    UNION ALL SELECT DATE '2026-10-21', 'Dussehra / Vijayadashami approx', 'national_lunar'
    UNION ALL SELECT DATE '2027-10-10', 'Dussehra / Vijayadashami approx', 'national_lunar'
    UNION ALL SELECT DATE '2028-10-28', 'Dussehra / Vijayadashami approx', 'national_lunar'

    UNION ALL SELECT DATE '2024-03-29', 'Good Friday approx', 'national_lunar'
    UNION ALL SELECT DATE '2025-04-18', 'Good Friday approx', 'national_lunar'
    UNION ALL SELECT DATE '2026-04-03', 'Good Friday approx', 'national_lunar'
    UNION ALL SELECT DATE '2027-03-26', 'Good Friday approx', 'national_lunar'
    UNION ALL SELECT DATE '2028-04-14', 'Good Friday approx', 'national_lunar'

    UNION ALL SELECT DATE '2024-04-11', 'Eid al-Fitr approx', 'national_lunar'
    UNION ALL SELECT DATE '2025-03-31', 'Eid al-Fitr approx', 'national_lunar'
    UNION ALL SELECT DATE '2026-03-20', 'Eid al-Fitr approx', 'national_lunar'
    UNION ALL SELECT DATE '2027-03-10', 'Eid al-Fitr approx', 'national_lunar'
    UNION ALL SELECT DATE '2028-02-28', 'Eid al-Fitr approx', 'national_lunar'
), onam_ranges AS (
    SELECT gs::date AS date_key, 'Onam season approx' AS holiday_name, 'regional_south' AS holiday_type
    FROM generate_series(DATE '2024-08-15', DATE '2024-08-23', INTERVAL '1 day') AS gs
    UNION ALL SELECT gs::date, 'Onam season approx', 'regional_south' FROM generate_series(DATE '2025-09-01', DATE '2025-09-09', INTERVAL '1 day') AS gs
    UNION ALL SELECT gs::date, 'Onam season approx', 'regional_south' FROM generate_series(DATE '2026-08-20', DATE '2026-08-28', INTERVAL '1 day') AS gs
    UNION ALL SELECT gs::date, 'Onam season approx', 'regional_south' FROM generate_series(DATE '2027-09-10', DATE '2027-09-18', INTERVAL '1 day') AS gs
    UNION ALL SELECT gs::date, 'Onam season approx', 'regional_south' FROM generate_series(DATE '2028-08-25', DATE '2028-09-02', INTERVAL '1 day') AS gs
), holidays AS (
    SELECT * FROM holiday_seed
    UNION ALL
    SELECT * FROM onam_ranges
), holidays_grouped AS (
    SELECT
        date_key,
        STRING_AGG(DISTINCT holiday_name, ' / ' ORDER BY holiday_name) AS holiday_name,
        STRING_AGG(DISTINCT holiday_type, ',' ORDER BY holiday_type) AS holiday_type
    FROM holidays
    GROUP BY date_key
), logistics_seasonality AS (
    SELECT
        date_key,
        month,
        CASE WHEN month IN (8, 9, 10, 11, 12, 1) THEN true ELSE false END AS is_textile_export_peak,
        CASE WHEN month IN (10, 11) THEN true ELSE false END AS is_agri_harvest_kharif,
        CASE WHEN month IN (3, 4) THEN true ELSE false END AS is_agri_harvest_rabi,
        CASE WHEN month IN (6, 7, 8, 9) THEN true ELSE false END AS is_monsoon_southwest,
        CASE WHEN month IN (10, 11, 12) THEN true ELSE false END AS is_monsoon_northeast,
        CASE WHEN month IN (10, 11, 12, 1) THEN true ELSE false END AS is_festival_retail_peak,
        CASE WHEN month IN (10, 11, 12, 1, 2, 3) THEN true ELSE false END AS is_construction_season,
        CASE WHEN month IN (11, 12, 1, 2) THEN true ELSE false END AS is_port_congestion_peak,
        CASE WHEN month IN (10, 11, 12, 1, 3, 4) THEN true ELSE false END AS is_driver_shortage_risk,
        CASE WHEN month IN (6, 7, 8, 9, 10) THEN true ELSE false END AS is_ghat_route_risk
    FROM base_calendar
), final_calendar AS (
    SELECT
        bc.date_key,
        bc.date_key AS full_date,
        bc.day_of_week,
        bc.day_name,
        bc.week_of_year,
        bc.month,
        bc.month_name,
        bc.quarter,
        bc.year,
        bc.is_weekend,
        (hg.date_key IS NOT NULL) AS is_holiday,
        hg.holiday_name,
        hg.holiday_type,
        ls.is_textile_export_peak,
        ls.is_agri_harvest_kharif,
        ls.is_agri_harvest_rabi,
        ls.is_monsoon_southwest,
        ls.is_monsoon_northeast,
        ls.is_festival_retail_peak,
        ls.is_construction_season,
        ls.is_port_congestion_peak,
        ls.is_driver_shortage_risk,
        ls.is_ghat_route_risk,
        CASE
            WHEN ls.is_textile_export_peak OR ls.is_festival_retail_peak OR ls.is_port_congestion_peak OR hg.date_key IS NOT NULL
            THEN true ELSE false
        END AS is_peak_season,
        CONCAT_WS(',',
            CASE WHEN ls.is_textile_export_peak THEN 'textile_export' END,
            CASE WHEN ls.is_agri_harvest_kharif THEN 'agri_kharif' END,
            CASE WHEN ls.is_agri_harvest_rabi THEN 'agri_rabi' END,
            CASE WHEN ls.is_monsoon_southwest THEN 'monsoon_southwest' END,
            CASE WHEN ls.is_monsoon_northeast THEN 'monsoon_northeast' END,
            CASE WHEN ls.is_festival_retail_peak THEN 'festival_retail' END,
            CASE WHEN ls.is_construction_season THEN 'construction' END,
            CASE WHEN ls.is_port_congestion_peak THEN 'port_congestion' END,
            CASE WHEN ls.is_driver_shortage_risk THEN 'driver_shortage' END,
            CASE WHEN ls.is_ghat_route_risk THEN 'ghat_route_risk' END
        ) AS peak_season_type,
        bc.fiscal_year
    FROM base_calendar bc
    LEFT JOIN holidays_grouped hg ON bc.date_key = hg.date_key
    JOIN logistics_seasonality ls ON bc.date_key = ls.date_key
)
INSERT INTO dim_time (
    date_key, full_date, day_of_week, day_name, week_of_year,
    month, month_name, quarter, year, is_weekend, is_holiday,
    holiday_name, holiday_type, is_peak_season, peak_season_type, fiscal_year,
    is_textile_export_peak, is_agri_harvest_kharif, is_agri_harvest_rabi,
    is_monsoon_southwest, is_monsoon_northeast, is_festival_retail_peak,
    is_construction_season, is_port_congestion_peak, is_driver_shortage_risk,
    is_ghat_route_risk, last_updated
)
SELECT
    date_key, full_date, day_of_week, day_name, week_of_year,
    month, month_name, quarter, year, is_weekend, is_holiday,
    holiday_name, holiday_type, is_peak_season, peak_season_type, fiscal_year,
    is_textile_export_peak, is_agri_harvest_kharif, is_agri_harvest_rabi,
    is_monsoon_southwest, is_monsoon_northeast, is_festival_retail_peak,
    is_construction_season, is_port_congestion_peak, is_driver_shortage_risk,
    is_ghat_route_risk, NOW()
FROM final_calendar
ON CONFLICT (date_key) DO UPDATE SET
    full_date = EXCLUDED.full_date,
    day_of_week = EXCLUDED.day_of_week,
    day_name = EXCLUDED.day_name,
    week_of_year = EXCLUDED.week_of_year,
    month = EXCLUDED.month,
    month_name = EXCLUDED.month_name,
    quarter = EXCLUDED.quarter,
    year = EXCLUDED.year,
    is_weekend = EXCLUDED.is_weekend,
    is_holiday = EXCLUDED.is_holiday,
    holiday_name = EXCLUDED.holiday_name,
    holiday_type = EXCLUDED.holiday_type,
    is_peak_season = EXCLUDED.is_peak_season,
    peak_season_type = EXCLUDED.peak_season_type,
    fiscal_year = EXCLUDED.fiscal_year,
    is_textile_export_peak = EXCLUDED.is_textile_export_peak,
    is_agri_harvest_kharif = EXCLUDED.is_agri_harvest_kharif,
    is_agri_harvest_rabi = EXCLUDED.is_agri_harvest_rabi,
    is_monsoon_southwest = EXCLUDED.is_monsoon_southwest,
    is_monsoon_northeast = EXCLUDED.is_monsoon_northeast,
    is_festival_retail_peak = EXCLUDED.is_festival_retail_peak,
    is_construction_season = EXCLUDED.is_construction_season,
    is_port_congestion_peak = EXCLUDED.is_port_congestion_peak,
    is_driver_shortage_risk = EXCLUDED.is_driver_shortage_risk,
    is_ghat_route_risk = EXCLUDED.is_ghat_route_risk,
    last_updated = NOW();

CREATE INDEX IF NOT EXISTS idx_dim_time_seasonality
ON dim_time(is_peak_season, is_textile_export_peak, is_monsoon_southwest, is_festival_retail_peak);

CREATE INDEX IF NOT EXISTS idx_dim_time_holidays
ON dim_time(is_holiday, holiday_type) WHERE is_holiday = true;

CREATE INDEX IF NOT EXISTS idx_dim_time_month_year
ON dim_time(year, month);

COMMENT ON TABLE dim_time IS 'Calendar dimension with Indian holidays and South India logistics seasonality flags for corridor analytics.';
COMMENT ON COLUMN dim_time.is_textile_export_peak IS 'Aug-Jan: textile/export cycle planning flag for Tiruppur/Coimbatore corridors.';
COMMENT ON COLUMN dim_time.is_agri_harvest_kharif IS 'Oct-Nov: kharif harvest planning flag.';
COMMENT ON COLUMN dim_time.is_monsoon_southwest IS 'Jun-Sep: southwest monsoon route risk planning flag.';
COMMENT ON COLUMN dim_time.is_festival_retail_peak IS 'Oct-Jan: retail surge planning flag.';
COMMENT ON COLUMN dim_time.is_port_congestion_peak IS 'Nov-Feb: export/port congestion planning flag.';
COMMENT ON COLUMN dim_time.is_ghat_route_risk IS 'Jun-Oct: ghat road risk planning flag.';

-- Verification helpers:
-- SELECT MIN(date_key), MAX(date_key), COUNT(*) FROM dim_time;
-- SELECT date_key, holiday_name, holiday_type FROM dim_time WHERE is_holiday = true ORDER BY date_key LIMIT 20;
-- SELECT date_key, peak_season_type FROM dim_time WHERE is_peak_season = true AND year = 2026 AND month = 11 ORDER BY date_key LIMIT 10;
