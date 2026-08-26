-- Zippy Logistics — Secondary schema additions
-- Adds event-logging and SOP tables used by Edge Functions + Realtime.

-- ============================================================
-- 0. HELPER FUNCTIONS
-- ============================================================

-- Atomic order-number generator per year.
CREATE SEQUENCE IF NOT EXISTS public.order_number_seq START 1;

CREATE OR REPLACE FUNCTION public.next_order_number(year_str TEXT)
RETURNS BIGINT AS $$
DECLARE
    next_val BIGINT;
BEGIN
    SELECT nextval('public.order_number_seq') INTO next_val;
    RETURN next_val;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- Find eligible vehicles/drivers for an order.
CREATE OR REPLACE FUNCTION public.find_dispatch_candidates(p_order_id UUID, p_radius_km INTEGER DEFAULT 25)
RETURNS TABLE (
    vehicle_id UUID,
    driver_id UUID,
    vendor_id UUID,
    registration_number VARCHAR,
    distance_km DECIMAL,
    eta_minutes INTEGER
) AS $$
DECLARE
    v_origin_city_id UUID;
    v_required_body VARCHAR;
    v_weight DECIMAL;
BEGIN
    SELECT o.origin_city_id, mt.required_body, o.cargo_weight_tons
    INTO v_origin_city_id, v_required_body, v_weight
    FROM public.orders o
    JOIN public.material_types mt ON mt.id = o.material_type_id
    WHERE o.id = p_order_id;

    RETURN QUERY
    SELECT
        v.id AS vehicle_id,
        v.driver_id,
        v.vendor_id,
        v.registration_number,
        ROUND(
            SQRT(
                POWER(111.32 * (c.latitude - oc.latitude), 2) +
                POWER(111.32 * (c.longitude - oc.longitude) * COS(RADIANS(oc.latitude)), 2)
            )::numeric, 2
        ) AS distance_km,
        15 AS eta_minutes
    FROM public.vehicles v
    JOIN public.vehicle_models vm ON vm.id = v.model_id
    JOIN public.cities c ON c.id = v.current_city_id
    JOIN public.cities oc ON oc.id = v_origin_city_id
    WHERE v.current_status = 'idle'
      AND v.is_online = TRUE
      AND vm.body_type = v_required_body
      AND vm.tonnage_capacity >= v_weight
      AND v.insurance_valid_until >= CURRENT_DATE
      AND v.fitness_cert_until >= CURRENT_DATE
      AND (
          v.current_city_id = v_origin_city_id
          OR SQRT(
              POWER(111.32 * (c.latitude - oc.latitude), 2) +
              POWER(111.32 * (c.longitude - oc.longitude) * COS(RADIANS(oc.latitude)), 2)
          ) <= p_radius_km
      )
    ORDER BY distance_km ASC, vm.tonnage_capacity ASC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


-- ============================================================
-- 1. ORDER EVENT LOG (for Supabase Realtime + event bus)
-- ============================================================
CREATE TABLE IF NOT EXISTS public.order_event_log (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id        UUID NOT NULL REFERENCES public.orders(id) ON DELETE CASCADE,
    event_type      VARCHAR(80) NOT NULL,
    payload         JSONB NOT NULL DEFAULT '{}',
    source          VARCHAR(40) NOT NULL CHECK (source IN ('customer_app', 'driver_app', 'transport_app', 'admin_panel', 'system', 'edge_function')),
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_order_event_log_order ON public.order_event_log(order_id);
CREATE INDEX IF NOT EXISTS idx_order_event_log_created ON public.order_event_log(created_at DESC);

ALTER TABLE public.order_event_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "order_event_log_admin_all" ON public.order_event_log
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "order_event_log_related_read" ON public.order_event_log
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = order_event_log.order_id
        AND (
          o.customer_id = public.current_customer_id()
          OR o.assigned_driver_id = public.current_driver_id()
          OR EXISTS (
            SELECT 1 FROM public.vehicles v
            WHERE v.id = o.assigned_vehicle_id
              AND v.vendor_id = public.current_vendor_id()
          )
        )
    )
  );


-- ============================================================
-- 2. SOP SECTIONS (machine-readable SOP knowledge base)
-- ============================================================
CREATE TABLE IF NOT EXISTS public.sop_sections (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sop_version         TEXT NOT NULL,
    section_id          TEXT NOT NULL,
    section_title       TEXT NOT NULL,
    agent               TEXT,
    workflow_category   TEXT,
    procedure           JSONB NOT NULL DEFAULT '[]'::jsonb,
    key_rules           TEXT[] DEFAULT '{}',
    inputs              TEXT[] DEFAULT '{}',
    outputs             TEXT[] DEFAULT '{}',
    related_tables      TEXT[] DEFAULT '{}',
    related_apis        TEXT[] DEFAULT '{}',
    related_agents       TEXT[] DEFAULT '{}',
    created_at          TIMESTAMP DEFAULT NOW(),
    UNIQUE(sop_version, section_id)
);

CREATE INDEX IF NOT EXISTS idx_sop_sections_agent ON public.sop_sections(agent);
CREATE INDEX IF NOT EXISTS idx_sop_sections_category ON public.sop_sections(workflow_category);

ALTER TABLE public.sop_sections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "sop_sections_read_all" ON public.sop_sections
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "sop_sections_admin_write" ON public.sop_sections
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');


-- ============================================================
-- 3. DISPATCH OFFERS (for driver assignment workflow)
-- ============================================================
CREATE TABLE IF NOT EXISTS public.dispatch_offers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id        UUID NOT NULL REFERENCES public.orders(id) ON DELETE CASCADE,
    driver_id       UUID REFERENCES public.drivers(id),
    vendor_id       UUID REFERENCES public.vendors(id),
    vehicle_id      UUID REFERENCES public.vehicles(id),
    expires_at      TIMESTAMP NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'expired')),
    responded_at    TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dispatch_offers_order ON public.dispatch_offers(order_id);
CREATE INDEX IF NOT EXISTS idx_dispatch_offers_driver ON public.dispatch_offers(driver_id);
CREATE INDEX IF NOT EXISTS idx_dispatch_offers_status ON public.dispatch_offers(status);

ALTER TABLE public.dispatch_offers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "dispatch_offers_admin_all" ON public.dispatch_offers
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "dispatch_offers_driver_read_update" ON public.dispatch_offers
  FOR ALL TO authenticated
  USING (driver_id = public.current_driver_id())
  WITH CHECK (driver_id = public.current_driver_id());


-- ============================================================
-- 4. DEFAULT PRICING FACTORS (initial seed)
-- ============================================================
INSERT INTO public.pricing_factors (factor_type, factor_value, description, is_active) VALUES
('hill_station',        1.200, 'Hill station surcharge',           true),
('remote_area',         1.150, 'Remote area surcharge',            true),
('peak_season',         1.250, 'Peak season demand multiplier',    true),
('weather_surge',       1.180, 'Weather disruption surcharge',     true),
('metro_congestion',    1.100, 'Metro congestion surcharge',        true),
('interstate_permit',   1.080, 'Interstate permit surcharge',      true),
('return_trip_bonus',   0.950, 'Return-trip discount',             true),
('no_return_trip',      1.120, 'No return trip penalty',           true),
('express_multiplier',  1.300, 'Express delivery multiplier',      true),
('premium_multiplier',  1.500, 'Premium service multiplier',       true)
ON CONFLICT (factor_type) DO NOTHING;


-- ============================================================
-- 5. SOP SECTIONS SEED (minimal sample)
-- ============================================================
INSERT INTO public.sop_sections (sop_version, section_id, section_title, agent, workflow_category, procedure, key_rules, inputs, outputs, related_tables, related_apis, related_agents) VALUES
('1.0.0', '2.1', 'Order Creation', 'OMS', 'Order Lifecycle Workflow',
 '["Customer submits request via app/web", "OMS validates locations and cargo", "System assigns order_id", "Order stored with status=draft", "Customer receives confirmation"]'::jsonb,
 ARRAY['Valid pickup and delivery locations required', 'Cargo weight and type mandatory', 'Pricing calculated only after validation'],
 ARRAY['customer_request_payload', 'cargo_data', 'pickup_location', 'delivery_location'],
 ARRAY['order_id', 'order_status', 'customer_notification'],
 ARRAY['orders', 'customers', 'cities'],
 ARRAY['Mapbox Geocoding API'],
 ARRAY['OMS Agent', 'Verification Agent']
)
ON CONFLICT (sop_version, section_id) DO NOTHING;

INSERT INTO public.sop_sections (sop_version, section_id, section_title, agent, workflow_category, procedure, key_rules, inputs, outputs, related_tables, related_apis, related_agents) VALUES
('1.0.0', '3.1', 'Provider Assignment', 'TMS', 'Order Lifecycle Workflow',
 '["Identify available drivers/companies", "Score and rank candidates", "Assign best match", "Send assignment notification", "Wait for response or escalate"]'::jsonb,
 ARRAY['Vehicle capacity must exceed cargo weight', 'Body type must match material', 'Driver license and fitness valid'],
 ARRAY['order_id', 'vehicle_requirements'],
 ARRAY['assigned_driver_id', 'assigned_vehicle_id', 'dispatch_alert'],
 ARRAY['orders', 'drivers', 'vehicles', 'vendors'],
 ARRAY['Internal scoring engine'],
 ARRAY['TMS Agent', 'Resource Management Agent']
)
ON CONFLICT (sop_version, section_id) DO NOTHING;

INSERT INTO public.sop_sections (sop_version, section_id, section_title, agent, workflow_category, procedure, key_rules, inputs, outputs, related_tables, related_apis, related_agents) VALUES
('1.0.0', '5.1', 'Payment Initiation', 'Payment', 'Payment Workflow',
 '["Initiate payment based on order status", "Record payment in payments table", "Log transaction in payment_transactions", "Send payment confirmation"]'::jsonb,
 ARRAY['Total payments cannot exceed final price', 'Vendor settlement requires verified POD', 'Refunds above threshold require admin approval'],
 ARRAY['order_id', 'payment_amount', 'payment_method'],
 ARRAY['payment_id', 'transaction_records', 'payment_status'],
 ARRAY['payments', 'payment_transactions', 'payment_holds', 'refunds'],
 ARRAY['Razorpay API'],
 ARRAY['Payment & Settlement Agent']
)
ON CONFLICT (sop_version, section_id) DO NOTHING;


-- ============================================================
-- 6. REALTIME PUBLICATION (so clients can subscribe to changes)
-- ============================================================
-- Create a dedicated publication for Zippy realtime tables.
-- This is idempotent and does not conflict with the default supabase_realtime publication.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_publication WHERE pubname = 'zippy_realtime'
    ) THEN
        CREATE PUBLICATION zippy_realtime
            FOR TABLE public.orders,
                       public.order_event_log,
                       public.live_tracking,
                       public.vehicles,
                       public.notifications,
                       public.dispatch_offers;
    END IF;
END
$$;
