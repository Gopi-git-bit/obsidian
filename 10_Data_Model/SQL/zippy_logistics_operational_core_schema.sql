-- ==========================================
-- ZIPPY LOGISTICS OPERATIONAL CORE SCHEMA
-- Target: PostgreSQL 14+
-- Purpose: OMS + IMS + TMS + finance transaction layer
-- ==========================================

CREATE SCHEMA IF NOT EXISTS zippy_core;
SET search_path TO zippy_core;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ==========================================
-- ENUMS
-- ==========================================

CREATE TYPE user_role AS ENUM (
    'driver',
    'customer',
    'transport_company',
    'admin',
    'ops'
);

CREATE TYPE vehicle_owner_type AS ENUM (
    'driver_owner',
    'transport_company'
);

CREATE TYPE vehicle_class AS ENUM (
    'LCV',
    'MCV',
    'HCV',
    'tipper',
    'tractor',
    'trailer',
    'reefer'
);

CREATE TYPE body_type AS ENUM (
    'open',
    'closed',
    'container',
    'tipper',
    'tanker',
    'trailer',
    'reefer'
);

CREATE TYPE cargo_group AS ENUM (
    'general',
    'textiles',
    'fmcg',
    'agri',
    'pharma',
    'electronics',
    'auto',
    'chemicals',
    'port',
    'oversized',
    'hazardous'
);

CREATE TYPE order_status AS ENUM (
    'draft',
    'payment_pending',
    'confirmed',
    'vehicle_search',
    'bidding',
    'matched',
    'driver_assigned',
    'enroute_pickup',
    'loaded',
    'in_transit',
    'out_for_delivery',
    'delivered',
    'settlement_pending',
    'closed',
    'cancelled',
    'expired'
);

CREATE TYPE stop_type AS ENUM (
    'pickup',
    'delivery',
    'intermediate',
    'hub',
    'port',
    'warehouse'
);

CREATE TYPE bid_status AS ENUM (
    'pending',
    'accepted',
    'rejected',
    'countered',
    'expired',
    'withdrawn'
);

CREATE TYPE match_status AS ENUM (
    'proposed',
    'approved',
    'rejected',
    'assigned',
    'cancelled',
    'completed'
);

CREATE TYPE trip_status AS ENUM (
    'planned',
    'assigned',
    'started',
    'at_pickup',
    'loaded',
    'in_transit',
    'at_delivery',
    'completed',
    'cancelled',
    'exception'
);

CREATE TYPE shipment_event_type AS ENUM (
    'order_assigned',
    'driver_assigned',
    'departed_for_pickup',
    'arrived_pickup',
    'loaded',
    'departed_origin',
    'arrived_hub',
    'departed_hub',
    'arrived_destination',
    'unloaded',
    'pod_uploaded',
    'delivered',
    'delay_alert',
    'incident_reported',
    'route_changed'
);

CREATE TYPE payment_mode AS ENUM (
    'full_advance',
    'partial_advance',
    'to_pay',
    'credit'
);

CREATE TYPE payment_status AS ENUM (
    'pending',
    'authorized',
    'paid',
    'failed',
    'partially_paid',
    'refunded',
    'written_off'
);

CREATE TYPE invoice_status AS ENUM (
    'draft',
    'issued',
    'sent',
    'paid',
    'void'
);

CREATE TYPE service_level_code AS ENUM (
    'economy',
    'standard',
    'guaranteed'
);

CREATE TYPE notification_type AS ENUM (
    'order',
    'payment',
    'document',
    'system',
    'incident'
);

CREATE TYPE incident_severity AS ENUM (
    'info',
    'warning',
    'critical'
);

CREATE TYPE partner_relationship_level AS ENUM (
    'spot_partner',
    'preferred_partner',
    'collaboration_pool',
    'strategic_network_partner'
);

-- ==========================================
-- IDENTITY
-- ==========================================

CREATE TABLE IF NOT EXISTS app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role user_role NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    password_hash TEXT,
    is_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customer_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES app_users(id) ON DELETE CASCADE,
    company_name TEXT,
    customer_category TEXT,
    gst_number TEXT,
    pan_number TEXT,
    billing_address TEXT,
    credit_days INTEGER CHECK (credit_days IS NULL OR credit_days >= 0),
    risk_score NUMERIC(6,2) CHECK (risk_score IS NULL OR (risk_score >= 0 AND risk_score <= 100)),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transport_companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES app_users(id) ON DELETE CASCADE,
    company_name TEXT NOT NULL,
    authorized_person TEXT,
    gst_number TEXT,
    pan_number TEXT,
    address TEXT,
    service_regions TEXT[],
    active_operating_role TEXT CHECK (active_operating_role IN ('customer', 'provider')),
    relationship_status TEXT DEFAULT 'active',
    rating NUMERIC(3,1) CHECK (rating IS NULL OR (rating >= 0 AND rating <= 5)),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS driver_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES app_users(id) ON DELETE CASCADE,
    transport_company_id UUID REFERENCES transport_companies(id) ON DELETE SET NULL,
    license_number TEXT NOT NULL UNIQUE,
    years_of_experience INTEGER CHECK (years_of_experience IS NULL OR years_of_experience >= 0),
    is_owner_driver BOOLEAN DEFAULT false,
    online_status BOOLEAN DEFAULT false,
    current_lat NUMERIC(9,6),
    current_lng NUMERIC(9,6),
    rating NUMERIC(3,1) CHECK (rating IS NULL OR (rating >= 0 AND rating <= 5)),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- FLEET
-- ==========================================

CREATE TABLE IF NOT EXISTS vehicle_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manufacturer TEXT NOT NULL,
    model_name TEXT NOT NULL,
    variant TEXT,
    vehicle_class vehicle_class NOT NULL,
    body_type body_type NOT NULL,
    payload_kg NUMERIC(10,2) CHECK (payload_kg IS NULL OR payload_kg > 0),
    volume_cbm NUMERIC(10,2) CHECK (volume_cbm IS NULL OR volume_cbm >= 0),
    loading_length_mm NUMERIC(10,2),
    loading_width_mm NUMERIC(10,2),
    loading_height_mm NUMERIC(10,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id UUID NOT NULL REFERENCES vehicle_models(id),
    owner_type vehicle_owner_type NOT NULL,
    owner_driver_id UUID REFERENCES driver_profiles(id) ON DELETE SET NULL,
    owner_company_id UUID REFERENCES transport_companies(id) ON DELETE SET NULL,
    assigned_driver_id UUID REFERENCES driver_profiles(id) ON DELETE SET NULL,
    registration_number TEXT NOT NULL UNIQUE,
    fitness_expiry DATE,
    insurance_expiry DATE,
    permit_expiry DATE,
    gps_device_id TEXT,
    is_available BOOLEAN DEFAULT true,
    current_city TEXT,
    current_lat NUMERIC(9,6),
    current_lng NUMERIC(9,6),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CHECK (
        (owner_type = 'driver_owner' AND owner_driver_id IS NOT NULL AND owner_company_id IS NULL) OR
        (owner_type = 'transport_company' AND owner_company_id IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS vehicle_availability_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    snapshot_ts TIMESTAMPTZ DEFAULT NOW(),
    availability_status TEXT NOT NULL,
    city TEXT,
    lat NUMERIC(9,6),
    lng NUMERIC(9,6),
    expected_free_at TIMESTAMPTZ,
    source_system TEXT,
    UNIQUE(vehicle_id, snapshot_ts)
);

-- ==========================================
-- NETWORK AND LANE MASTER
-- ==========================================

CREATE TABLE IF NOT EXISTS directed_lanes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_code TEXT NOT NULL UNIQUE,
    origin_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    cargo_group cargo_group,
    vehicle_class vehicle_class,
    distance_km NUMERIC(8,2) CHECK (distance_km IS NULL OR distance_km >= 0),
    typical_sla_hours NUMERIC(6,2),
    is_triangle_candidate BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lane_rate_bands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_id UUID NOT NULL REFERENCES directed_lanes(id) ON DELETE CASCADE,
    valid_from DATE NOT NULL,
    valid_to DATE,
    min_rate_per_km NUMERIC(10,2),
    median_rate_per_km NUMERIC(10,2),
    max_rate_per_km NUMERIC(10,2),
    source_note TEXT
);

CREATE TABLE IF NOT EXISTS partner_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transport_company_id UUID NOT NULL REFERENCES transport_companies(id) ON DELETE CASCADE,
    partner_company_id UUID NOT NULL REFERENCES transport_companies(id) ON DELETE CASCADE,
    relationship_level partner_relationship_level NOT NULL,
    agreement_id TEXT,
    active_from DATE,
    active_to DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(transport_company_id, partner_company_id)
);

CREATE TABLE IF NOT EXISTS city_market_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city_name TEXT NOT NULL UNIQUE,
    state_name TEXT,
    city_tier TEXT CHECK (city_tier IN ('tier_1', 'tier_2', 'tier_3')),
    urban_density_band TEXT CHECK (urban_density_band IN ('high', 'medium', 'low')),
    nearby_tier1_within_100km INTEGER DEFAULT 0 CHECK (nearby_tier1_within_100km >= 0),
    nearby_tier1_within_500km INTEGER DEFAULT 0 CHECK (nearby_tier1_within_500km >= 0),
    nearby_tier23_within_200km INTEGER DEFAULT 0 CHECK (nearby_tier23_within_200km >= 0),
    nearby_tier123_within_500km INTEGER DEFAULT 0 CHECK (nearby_tier123_within_500km >= 0),
    congestion_score NUMERIC(6,2) CHECK (congestion_score IS NULL OR (congestion_score >= 0 AND congestion_score <= 100)),
    demand_score NUMERIC(6,2) CHECK (demand_score IS NULL OR (demand_score >= 0 AND demand_score <= 100)),
    driver_cost_index NUMERIC(8,4),
    last_refreshed_at TIMESTAMPTZ DEFAULT NOW(),
    source_note TEXT
);

CREATE TABLE IF NOT EXISTS lane_pricing_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lane_id UUID NOT NULL REFERENCES directed_lanes(id) ON DELETE CASCADE,
    signal_date DATE NOT NULL,
    origin_city_profile_id UUID REFERENCES city_market_profiles(id) ON DELETE SET NULL,
    destination_city_profile_id UUID REFERENCES city_market_profiles(id) ON DELETE SET NULL,
    demand_supply_ratio NUMERIC(10,4) CHECK (demand_supply_ratio IS NULL OR demand_supply_ratio >= 0),
    congestion_multiplier NUMERIC(8,4) CHECK (congestion_multiplier IS NULL OR congestion_multiplier >= 0),
    deadhead_risk_score NUMERIC(6,2) CHECK (deadhead_risk_score IS NULL OR (deadhead_risk_score >= 0 AND deadhead_risk_score <= 100)),
    return_load_probability NUMERIC(5,4) CHECK (return_load_probability IS NULL OR (return_load_probability >= 0 AND return_load_probability <= 1)),
    seasonal_multiplier NUMERIC(8,4) CHECK (seasonal_multiplier IS NULL OR seasonal_multiplier >= 0),
    fuel_index NUMERIC(8,4),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(lane_id, signal_date)
);

CREATE TABLE IF NOT EXISTS service_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_code service_level_code NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    description TEXT,
    priority_rank INTEGER NOT NULL CHECK (priority_rank >= 1),
    target_pickup_window_hours NUMERIC(6,2),
    target_delivery_window_hours NUMERIC(6,2),
    default_backup_required BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sla_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_name TEXT NOT NULL,
    service_level_id UUID NOT NULL REFERENCES service_levels(id) ON DELETE CASCADE,
    lane_id UUID REFERENCES directed_lanes(id) ON DELETE CASCADE,
    cargo_group cargo_group,
    vehicle_class vehicle_class,
    max_pickup_buffer_hours NUMERIC(6,2),
    max_delivery_buffer_hours NUMERIC(6,2),
    max_eta_variance_pct NUMERIC(6,2),
    backup_carrier_required BOOLEAN DEFAULT false,
    proof_of_delivery_required BOOLEAN DEFAULT true,
    min_tracking_coverage_pct NUMERIC(5,2) CHECK (min_tracking_coverage_pct IS NULL OR (min_tracking_coverage_pct >= 0 AND min_tracking_coverage_pct <= 100)),
    active_from DATE,
    active_to DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- OMS
-- ==========================================

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_account_id UUID NOT NULL REFERENCES customer_accounts(id),
    transport_company_customer_id UUID REFERENCES transport_companies(id),
    requested_vehicle_class vehicle_class,
    requested_body_type body_type,
    cargo_group cargo_group NOT NULL,
    cargo_description TEXT,
    weight_kg NUMERIC(10,2) NOT NULL CHECK (weight_kg > 0),
    volume_cbm NUMERIC(10,2) CHECK (volume_cbm IS NULL OR volume_cbm >= 0),
    package_count INTEGER DEFAULT 1 CHECK (package_count >= 1),
    payment_mode payment_mode NOT NULL,
    advance_percentage NUMERIC(5,2) CHECK (advance_percentage IS NULL OR (advance_percentage >= 0 AND advance_percentage <= 100)),
    quoted_amount NUMERIC(12,2),
    agreed_amount NUMERIC(12,2),
    lane_id UUID REFERENCES directed_lanes(id),
    service_tier TEXT,
    promised_pickup_at TIMESTAMPTZ,
    promised_delivery_at TIMESTAMPTZ,
    status order_status NOT NULL DEFAULT 'draft',
    cancellation_reason TEXT,
    created_by UUID REFERENCES app_users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_sla_commitments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL UNIQUE REFERENCES orders(id) ON DELETE CASCADE,
    service_level_id UUID REFERENCES service_levels(id) ON DELETE SET NULL,
    sla_policy_id UUID REFERENCES sla_policies(id) ON DELETE SET NULL,
    promised_pickup_at TIMESTAMPTZ,
    promised_delivery_at TIMESTAMPTZ,
    promised_pickup_window_start TIMESTAMPTZ,
    promised_pickup_window_end TIMESTAMPTZ,
    promised_delivery_window_start TIMESTAMPTZ,
    promised_delivery_window_end TIMESTAMPTZ,
    backup_required BOOLEAN DEFAULT false,
    pod_required BOOLEAN DEFAULT true,
    otif_required BOOLEAN DEFAULT true,
    current_risk_level TEXT CHECK (current_risk_level IN ('low', 'medium', 'high')),
    breached_at TIMESTAMPTZ,
    breach_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_stops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    stop_sequence INTEGER NOT NULL CHECK (stop_sequence >= 1),
    stop_type stop_type NOT NULL,
    party_name TEXT,
    contact_name TEXT,
    contact_phone TEXT,
    address_text TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT,
    pincode TEXT,
    lat NUMERIC(9,6),
    lng NUMERIC(9,6),
    scheduled_at TIMESTAMPTZ,
    actual_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(order_id, stop_sequence)
);

CREATE TABLE IF NOT EXISTS order_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    document_type TEXT NOT NULL,
    document_url TEXT NOT NULL,
    uploaded_by UUID REFERENCES app_users(id),
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_state_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    from_status order_status,
    to_status order_status NOT NULL,
    actor_user_id UUID REFERENCES app_users(id),
    reason TEXT,
    event_ts TIMESTAMPTZ DEFAULT NOW(),
    idempotency_key TEXT UNIQUE
);

-- ==========================================
-- MATCHING
-- ==========================================

CREATE TABLE IF NOT EXISTS order_bids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    vehicle_id UUID NOT NULL REFERENCES vehicles(id),
    driver_id UUID REFERENCES driver_profiles(id),
    bidder_company_id UUID REFERENCES transport_companies(id),
    bid_amount NUMERIC(12,2) NOT NULL CHECK (bid_amount > 0),
    estimated_eta_hours NUMERIC(6,2),
    notes TEXT,
    status bid_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    vehicle_id UUID NOT NULL REFERENCES vehicles(id),
    driver_id UUID REFERENCES driver_profiles(id),
    bidder_company_id UUID REFERENCES transport_companies(id),
    bid_id UUID REFERENCES order_bids(id),
    match_score NUMERIC(6,2),
    route_type TEXT CHECK (route_type IN ('direct','triangular')),
    selected_triangle_code TEXT,
    required_backup_carrier BOOLEAN DEFAULT false,
    pricing_premium_pct NUMERIC(6,2),
    status match_status NOT NULL DEFAULT 'proposed',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- TMS
-- ==========================================

CREATE TABLE IF NOT EXISTS trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_match_id UUID NOT NULL REFERENCES order_matches(id) ON DELETE CASCADE,
    order_id UUID NOT NULL REFERENCES orders(id),
    vehicle_id UUID NOT NULL REFERENCES vehicles(id),
    driver_id UUID REFERENCES driver_profiles(id),
    primary_lane_id UUID REFERENCES directed_lanes(id),
    trip_status trip_status NOT NULL DEFAULT 'planned',
    planned_start_at TIMESTAMPTZ,
    actual_start_at TIMESTAMPTZ,
    planned_end_at TIMESTAMPTZ,
    actual_end_at TIMESTAMPTZ,
    distance_km NUMERIC(10,2),
    estimated_cost_inr NUMERIC(12,2),
    actual_cost_inr NUMERIC(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trip_legs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    leg_sequence INTEGER NOT NULL CHECK (leg_sequence >= 1),
    leg_lane_id UUID REFERENCES directed_lanes(id),
    origin_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    planned_departure_at TIMESTAMPTZ,
    actual_departure_at TIMESTAMPTZ,
    planned_arrival_at TIMESTAMPTZ,
    actual_arrival_at TIMESTAMPTZ,
    planned_distance_km NUMERIC(10,2),
    actual_distance_km NUMERIC(10,2),
    is_backhaul_leg BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(trip_id, leg_sequence)
);

CREATE TABLE IF NOT EXISTS shipment_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES trips(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    trip_leg_id UUID REFERENCES trip_legs(id) ON DELETE SET NULL,
    event_type shipment_event_type NOT NULL,
    event_ts TIMESTAMPTZ DEFAULT NOW(),
    city TEXT,
    lat NUMERIC(9,6),
    lng NUMERIC(9,6),
    description TEXT,
    source_system TEXT,
    idempotency_key TEXT UNIQUE
);

-- ==========================================
-- FINANCE
-- ==========================================

CREATE TABLE IF NOT EXISTS payment_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payer_user_id UUID REFERENCES app_users(id),
    payee_company_id UUID REFERENCES transport_companies(id),
    amount_inr NUMERIC(12,2) NOT NULL CHECK (amount_inr >= 0),
    payment_mode payment_mode NOT NULL,
    payment_status payment_status NOT NULL DEFAULT 'pending',
    gateway_reference TEXT,
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoice_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    invoice_number TEXT NOT NULL UNIQUE,
    invoice_status invoice_status NOT NULL DEFAULT 'draft',
    taxable_amount_inr NUMERIC(12,2) NOT NULL CHECK (taxable_amount_inr >= 0),
    gst_amount_inr NUMERIC(12,2) NOT NULL CHECK (gst_amount_inr >= 0),
    total_amount_inr NUMERIC(12,2) NOT NULL CHECK (total_amount_inr >= 0),
    issued_at TIMESTAMPTZ,
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS finance_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    payment_record_id UUID REFERENCES payment_records(id) ON DELETE SET NULL,
    invoice_record_id UUID REFERENCES invoice_records(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    event_ts TIMESTAMPTZ DEFAULT NOW(),
    amount_inr NUMERIC(12,2),
    metadata JSONB DEFAULT '{}'::jsonb,
    idempotency_key TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS payment_intents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES app_users(id),
    payment_provider TEXT,
    amount_minor_units BIGINT NOT NULL CHECK (amount_minor_units >= 0),
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL,
    idempotency_key TEXT UNIQUE,
    payment_reference TEXT,
    failure_reason TEXT,
    initiated_at TIMESTAMPTZ DEFAULT NOW(),
    confirmed_at TIMESTAMPTZ,
    refunded_at TIMESTAMPTZ,
    context JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS price_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    lane_id UUID REFERENCES directed_lanes(id) ON DELETE SET NULL,
    quoted_at TIMESTAMPTZ DEFAULT NOW(),
    base_cost_inr NUMERIC(12,2) NOT NULL CHECK (base_cost_inr >= 0),
    distance_cost_inr NUMERIC(12,2),
    demand_adjustment_inr NUMERIC(12,2) DEFAULT 0,
    congestion_adjustment_inr NUMERIC(12,2) DEFAULT 0,
    backhaul_adjustment_inr NUMERIC(12,2) DEFAULT 0,
    seasonal_adjustment_inr NUMERIC(12,2) DEFAULT 0,
    risk_adjustment_inr NUMERIC(12,2) DEFAULT 0,
    discount_inr NUMERIC(12,2) DEFAULT 0,
    final_quote_inr NUMERIC(12,2) NOT NULL CHECK (final_quote_inr >= 0),
    pricing_method TEXT,
    pricing_explanation TEXT,
    signal_snapshot JSONB DEFAULT '{}'::jsonb,
    created_by_agent TEXT
);

-- ==========================================
-- TRUST, SUPPORT, AND AUDIT
-- ==========================================

CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_type notification_type NOT NULL,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS push_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    device_platform TEXT,
    push_token TEXT NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS driver_ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID NOT NULL REFERENCES driver_profiles(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    customer_account_id UUID REFERENCES customer_accounts(id) ON DELETE SET NULL,
    rating NUMERIC(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transport_company_ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transport_company_id UUID NOT NULL REFERENCES transport_companies(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    customer_account_id UUID REFERENCES customer_accounts(id) ON DELETE SET NULL,
    rating NUMERIC(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS admin_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_user_id UUID REFERENCES app_users(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    target_type TEXT,
    target_id UUID,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
    source_service TEXT,
    related_entity_type TEXT,
    related_entity_id UUID,
    severity incident_severity NOT NULL DEFAULT 'info',
    message TEXT NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolved_by UUID REFERENCES app_users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS driver_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id UUID NOT NULL REFERENCES driver_profiles(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    trip_id UUID REFERENCES trips(id) ON DELETE SET NULL,
    alert_type TEXT NOT NULL CHECK (alert_type IN ('long_halt', 'route_deviation', 'breakdown', 'accident', 'gps_loss', 'temperature_deviation')),
    alert_status TEXT NOT NULL DEFAULT 'active' CHECK (alert_status IN ('active', 'acknowledged', 'suppressed', 'resolved')),
    lat NUMERIC(9,6),
    lng NUMERIC(9,6),
    alert_details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    acknowledged_at TIMESTAMPTZ,
    acknowledged_by UUID REFERENCES app_users(id) ON DELETE SET NULL,
    suppressed_at TIMESTAMPTZ,
    suppressed_by UUID REFERENCES app_users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMPTZ,
    resolved_by UUID REFERENCES app_users(id) ON DELETE SET NULL
);

-- ==========================================
-- INDEXES
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_orders_status_created
ON orders(status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_orders_lane_status
ON orders(lane_id, status);

CREATE INDEX IF NOT EXISTS idx_order_stops_city_type
ON order_stops(city, stop_type);

CREATE INDEX IF NOT EXISTS idx_order_bids_order_status
ON order_bids(order_id, status);

CREATE INDEX IF NOT EXISTS idx_order_matches_order_status
ON order_matches(order_id, status);

CREATE INDEX IF NOT EXISTS idx_trips_status
ON trips(trip_status, planned_start_at DESC);

CREATE INDEX IF NOT EXISTS idx_trip_legs_lane
ON trip_legs(leg_lane_id, leg_sequence);

CREATE INDEX IF NOT EXISTS idx_shipment_events_order_ts
ON shipment_events(order_id, event_ts DESC);

CREATE INDEX IF NOT EXISTS idx_shipment_events_trip_ts
ON shipment_events(trip_id, event_ts DESC);

CREATE INDEX IF NOT EXISTS idx_vehicle_availability_vehicle_ts
ON vehicle_availability_snapshots(vehicle_id, snapshot_ts DESC);

CREATE INDEX IF NOT EXISTS idx_directed_lanes_od
ON directed_lanes(origin_city, destination_city);

CREATE INDEX IF NOT EXISTS idx_city_market_profiles_tier
ON city_market_profiles(city_tier, city_name);

CREATE INDEX IF NOT EXISTS idx_lane_pricing_signals_lane_date
ON lane_pricing_signals(lane_id, signal_date DESC);

CREATE INDEX IF NOT EXISTS idx_sla_policies_lane_service
ON sla_policies(lane_id, service_level_id, is_active);

CREATE INDEX IF NOT EXISTS idx_finance_events_order_ts
ON finance_events(order_id, event_ts DESC);

CREATE INDEX IF NOT EXISTS idx_payment_intents_order_status
ON payment_intents(order_id, status, initiated_at DESC);

CREATE INDEX IF NOT EXISTS idx_notifications_user_created
ON notifications(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_driver_ratings_driver
ON driver_ratings(driver_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_transport_company_ratings_company
ON transport_company_ratings(transport_company_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_incident_logs_created
ON incident_logs(created_at DESC, severity);

CREATE INDEX IF NOT EXISTS idx_price_quotes_order_time
ON price_quotes(order_id, quoted_at DESC);

CREATE INDEX IF NOT EXISTS idx_driver_alerts_driver_created
ON driver_alerts(driver_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_order_sla_commitments_risk
ON order_sla_commitments(current_risk_level, promised_delivery_at);

-- ==========================================
-- NOTES
-- ==========================================

COMMENT ON TABLE directed_lanes IS 'Operational directed lane master. Preserve direction and optional cargo/vehicle specificity.';
COMMENT ON TABLE city_market_profiles IS 'City-level pricing context for tier, density, congestion and demand-aware quote logic.';
COMMENT ON TABLE lane_pricing_signals IS 'Daily or periodic lane pricing inputs including demand-supply balance and return-load risk.';
COMMENT ON TABLE price_quotes IS 'Audit trail of deterministic quote construction and pricing-factor breakdown.';
COMMENT ON TABLE service_levels IS 'Customer-facing delivery products such as economy, standard and guaranteed.';
COMMENT ON TABLE sla_policies IS 'Lane-aware and cargo-aware SLA rules that define allowed buffers and operational controls.';
COMMENT ON TABLE order_sla_commitments IS 'Order-level promise commitments used to track promised windows, backup requirements and SLA breach state.';
COMMENT ON TABLE order_state_events IS 'Immutable order lifecycle transition log for replay-safe OMS state changes.';
COMMENT ON TABLE trip_legs IS 'Supports direct and triangular execution. One trip can contain multiple legs.';
COMMENT ON TABLE shipment_events IS 'Operational event stream that can feed lane_delay_events and shipment-level analytics facts.';
COMMENT ON TABLE payment_intents IS 'Gateway-facing payment orchestration table with idempotency and provider reference support.';
COMMENT ON TABLE incident_logs IS 'Operational incident and exception audit trail for support, risk and control-tower workflows.';
COMMENT ON TABLE driver_alerts IS 'Structured driver and trip execution alerts for control-tower monitoring and response.';
