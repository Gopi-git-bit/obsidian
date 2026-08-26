-- Zippy Logistics — Row-Level Security (RLS) Policies
-- Enables multi-tenant isolation across customers, drivers, vendors, and admins.

-- ============================================================
-- 0. HELPERS
-- ============================================================

-- Returns the role of the currently authenticated application user.
CREATE OR REPLACE FUNCTION public.current_user_role()
RETURNS TEXT AS $$
  SELECT role FROM public.users WHERE id = auth.uid();
$$ LANGUAGE sql SECURITY DEFINER;

-- Returns the customer.id for the current auth user (if any).
CREATE OR REPLACE FUNCTION public.current_customer_id()
RETURNS UUID AS $$
  SELECT id FROM public.customers WHERE user_id = auth.uid() LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER;

-- Returns the driver.id for the current auth user (if any).
CREATE OR REPLACE FUNCTION public.current_driver_id()
RETURNS UUID AS $$
  SELECT id FROM public.drivers WHERE user_id = auth.uid() LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER;

-- Returns the vendor.id for the current auth user (if any).
CREATE OR REPLACE FUNCTION public.current_vendor_id()
RETURNS UUID AS $$
  SELECT id FROM public.vendors WHERE user_id = auth.uid() LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER;


-- ============================================================
-- 1. USERS
-- ============================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_admin_all" ON public.users
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "users_self_read_update" ON public.users
  FOR SELECT TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "users_self_update" ON public.users
  FOR UPDATE TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);


-- ============================================================
-- 2. CUSTOMERS
-- ============================================================
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "customers_admin_all" ON public.customers
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "customers_own_read" ON public.customers
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "customers_own_update" ON public.customers
  FOR UPDATE TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "customers_insert_self" ON public.customers
  FOR INSERT TO authenticated
  WITH CHECK (user_id = auth.uid());


-- ============================================================
-- 3. VENDORS
-- ============================================================
ALTER TABLE public.vendors ENABLE ROW LEVEL SECURITY;

CREATE POLICY "vendors_admin_all" ON public.vendors
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "vendors_own_read" ON public.vendors
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "vendors_own_update" ON public.vendors
  FOR UPDATE TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "vendors_insert_self" ON public.vendors
  FOR INSERT TO authenticated
  WITH CHECK (user_id = auth.uid());


-- ============================================================
-- 4. DRIVERS
-- ============================================================
ALTER TABLE public.drivers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "drivers_admin_all" ON public.drivers
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "drivers_own_read" ON public.drivers
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "drivers_own_update" ON public.drivers
  FOR UPDATE TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "drivers_vendor_read" ON public.drivers
  FOR SELECT TO authenticated
  USING (vendor_id = public.current_vendor_id());


-- ============================================================
-- 5. VEHICLE MODELS (read-only reference data)
-- ============================================================
ALTER TABLE public.vehicle_models ENABLE ROW LEVEL SECURITY;

CREATE POLICY "vehicle_models_read_all" ON public.vehicle_models
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "vehicle_models_admin_write" ON public.vehicle_models
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');


-- ============================================================
-- 6. VEHICLES
-- ============================================================
ALTER TABLE public.vehicles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "vehicles_admin_all" ON public.vehicles
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "vehicles_vendor_all" ON public.vehicles
  FOR ALL TO authenticated
  USING (vendor_id = public.current_vendor_id())
  WITH CHECK (vendor_id = public.current_vendor_id());

CREATE POLICY "vehicles_driver_read_assigned" ON public.vehicles
  FOR SELECT TO authenticated
  USING (driver_id = public.current_driver_id());


-- ============================================================
-- 7. MATERIAL TYPES (read-only reference data)
-- ============================================================
ALTER TABLE public.material_types ENABLE ROW LEVEL SECURITY;

CREATE POLICY "material_types_read_all" ON public.material_types
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "material_types_admin_write" ON public.material_types
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');


-- ============================================================
-- 8. ORDERS
-- ============================================================
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "orders_admin_all" ON public.orders
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "orders_customer_all" ON public.orders
  FOR ALL TO authenticated
  USING (customer_id = public.current_customer_id())
  WITH CHECK (customer_id = public.current_customer_id());

CREATE POLICY "orders_driver_read_update" ON public.orders
  FOR SELECT TO authenticated
  USING (assigned_driver_id = public.current_driver_id());

CREATE POLICY "orders_driver_update_assigned" ON public.orders
  FOR UPDATE TO authenticated
  USING (assigned_driver_id = public.current_driver_id())
  WITH CHECK (assigned_driver_id = public.current_driver_id());

CREATE POLICY "orders_vendor_read" ON public.orders
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.vehicles v
      WHERE v.id = orders.assigned_vehicle_id
        AND v.vendor_id = public.current_vendor_id()
    )
  );


-- ============================================================
-- 9. ORDER STATE HISTORY
-- ============================================================
ALTER TABLE public.order_state_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "order_state_history_admin_all" ON public.order_state_history
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "order_state_history_related_read" ON public.order_state_history
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = order_state_history.order_id
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
-- 10. INVOICES & POD DOCUMENTS
-- ============================================================
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pod_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "invoices_admin_all" ON public.invoices
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "invoices_related_read" ON public.invoices
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = invoices.order_id
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

CREATE POLICY "pod_admin_all" ON public.pod_documents
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

-- Drivers can upload PODs for their assigned orders.
CREATE POLICY "pod_driver_insert" ON public.pod_documents
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = pod_documents.order_id
        AND o.assigned_driver_id = public.current_driver_id()
    )
  );

CREATE POLICY "pod_related_read" ON public.pod_documents
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = pod_documents.order_id
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
-- 11. PAYMENTS, HOLDS, REFUNDS
-- ============================================================
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_holds ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.refunds ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_terms ENABLE ROW LEVEL SECURITY;

CREATE POLICY "payments_admin_all" ON public.payments
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "payments_related_read" ON public.payments
  FOR SELECT TO authenticated
  USING (
    (party_type = 'customer' AND party_id = public.current_customer_id())
    OR (party_type = 'vendor' AND party_id = public.current_vendor_id())
  );

CREATE POLICY "payment_holds_admin_all" ON public.payment_holds
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "refunds_admin_all" ON public.refunds
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "payment_terms_admin_all" ON public.payment_terms
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "payment_terms_own_read" ON public.payment_terms
  FOR SELECT TO authenticated
  USING (
    (party_type = 'customer' AND party_id = public.current_customer_id())
    OR (party_type = 'vendor' AND party_id = public.current_vendor_id())
  );


-- ============================================================
-- 12. PRICING & ROUTES (read-only reference data)
-- ============================================================
ALTER TABLE public.pricing_base_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pricing_factors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.route_distances ENABLE ROW LEVEL SECURITY;

CREATE POLICY "pricing_read_all" ON public.pricing_base_rates
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "pricing_factors_read_all" ON public.pricing_factors
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "route_distances_read_all" ON public.route_distances
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "pricing_admin_write" ON public.pricing_base_rates
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "pricing_factors_admin_write" ON public.pricing_factors
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "route_distances_admin_write" ON public.route_distances
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');


-- ============================================================
-- 13. SCORING & METRICS
-- ============================================================
ALTER TABLE public.driver_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customer_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.driver_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customer_scores ENABLE ROW LEVEL SECURITY;

CREATE POLICY "driver_metrics_admin_all" ON public.driver_metrics
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "driver_metrics_own_read" ON public.driver_metrics
  FOR SELECT TO authenticated
  USING (driver_id = public.current_driver_id());

CREATE POLICY "customer_metrics_admin_all" ON public.customer_metrics
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "customer_metrics_own_read" ON public.customer_metrics
  FOR SELECT TO authenticated
  USING (customer_id = public.current_customer_id());

CREATE POLICY "driver_scores_admin_all" ON public.driver_scores
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "driver_scores_own_read" ON public.driver_scores
  FOR SELECT TO authenticated
  USING (driver_id = public.current_driver_id());

CREATE POLICY "customer_scores_admin_all" ON public.customer_scores
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "customer_scores_own_read" ON public.customer_scores
  FOR SELECT TO authenticated
  USING (customer_id = public.current_customer_id());


-- ============================================================
-- 14. LIVE TRACKING & FORECASTING
-- ============================================================
ALTER TABLE public.live_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vehicle_arrival_forecast ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vehicle_inventory_snapshot ENABLE ROW LEVEL SECURITY;

CREATE POLICY "live_tracking_admin_all" ON public.live_tracking
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "live_tracking_driver_insert" ON public.live_tracking
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.vehicles v
      WHERE v.id = live_tracking.vehicle_id
        AND v.driver_id = public.current_driver_id()
    )
  );

CREATE POLICY "live_tracking_related_read" ON public.live_tracking
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.id = live_tracking.order_id
        AND (
          o.customer_id = public.current_customer_id()
          OR o.assigned_driver_id = public.current_driver_id()
        )
    )
  );

CREATE POLICY "vehicle_arrival_forecast_read_all" ON public.vehicle_arrival_forecast
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "vehicle_inventory_snapshot_read_all" ON public.vehicle_inventory_snapshot
  FOR SELECT TO authenticated
  USING (true);


-- ============================================================
-- 15. CONSIGNEES
-- ============================================================
ALTER TABLE public.consignees ENABLE ROW LEVEL SECURITY;

CREATE POLICY "consignees_admin_all" ON public.consignees
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "consignees_read_related" ON public.consignees
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.orders o
      WHERE o.consignee_name = consignees.name
        AND o.consignee_phone = consignees.phone
        AND o.customer_id = public.current_customer_id()
    )
  );


-- ============================================================
-- 16. AUDIT LOGS
-- ============================================================
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "audit_logs_admin_all" ON public.audit_logs
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "audit_logs_self_read" ON public.audit_logs
  FOR SELECT TO authenticated
  USING (performed_by = auth.uid());


-- ============================================================
-- 17. TERMS & CONDITIONS / ACCEPTANCE
-- ============================================================
ALTER TABLE public.terms_conditions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.terms_acceptance ENABLE ROW LEVEL SECURITY;

CREATE POLICY "terms_conditions_read_all" ON public.terms_conditions
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "terms_conditions_admin_write" ON public.terms_conditions
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "terms_acceptance_admin_all" ON public.terms_acceptance
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "terms_acceptance_own_read" ON public.terms_acceptance
  FOR SELECT TO authenticated
  USING (user_id = auth.uid());


-- ============================================================
-- 18. NOTIFICATIONS
-- ============================================================
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "notifications_admin_all" ON public.notifications
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');

CREATE POLICY "notifications_own_all" ON public.notifications
  FOR ALL TO authenticated
  USING (recipient_id = auth.uid())
  WITH CHECK (recipient_id = auth.uid());


-- ============================================================
-- 19. CITIES (reference data, read-only for app users)
-- ============================================================
ALTER TABLE public.cities ENABLE ROW LEVEL SECURITY;

CREATE POLICY "cities_read_all" ON public.cities
  FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "cities_admin_write" ON public.cities
  FOR ALL TO authenticated
  USING (public.current_user_role() = 'admin')
  WITH CHECK (public.current_user_role() = 'admin');
