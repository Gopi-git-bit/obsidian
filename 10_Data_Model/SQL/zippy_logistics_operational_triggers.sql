-- ==========================================
-- ZIPPY LOGISTICS OPERATIONAL TRIGGERS
-- Target: PostgreSQL 14+
-- Purpose: lifecycle enforcement and realtime event emission
-- Depends on: zippy_logistics_operational_core_schema.sql
-- ==========================================

SET search_path TO zippy_core;

-- ==========================================
-- TIMESTAMP TOUCH TRIGGER
-- ==========================================

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- ORDER LIFECYCLE ENFORCEMENT
-- ==========================================

CREATE OR REPLACE FUNCTION enforce_order_lifecycle()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.status IS DISTINCT FROM OLD.status THEN
        IF OLD.status = 'draft' AND NEW.status NOT IN ('payment_pending', 'cancelled', 'expired') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'payment_pending' AND NEW.status NOT IN ('confirmed', 'cancelled', 'expired') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'confirmed' AND NEW.status NOT IN ('vehicle_search', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'vehicle_search' AND NEW.status NOT IN ('bidding', 'matched', 'cancelled', 'expired') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'bidding' AND NEW.status NOT IN ('matched', 'cancelled', 'expired') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'matched' AND NEW.status NOT IN ('driver_assigned', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'driver_assigned' AND NEW.status NOT IN ('enroute_pickup', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'enroute_pickup' AND NEW.status NOT IN ('loaded', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'loaded' AND NEW.status NOT IN ('in_transit', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'in_transit' AND NEW.status NOT IN ('out_for_delivery', 'delivered', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'out_for_delivery' AND NEW.status NOT IN ('delivered', 'cancelled') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'delivered' AND NEW.status NOT IN ('settlement_pending', 'closed') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status = 'settlement_pending' AND NEW.status NOT IN ('closed') THEN
            RAISE EXCEPTION 'Illegal status transition: % -> %', OLD.status, NEW.status;
        ELSIF OLD.status IN ('closed', 'cancelled', 'expired') THEN
            RAISE EXCEPTION 'Terminal status transition not allowed: % -> %', OLD.status, NEW.status;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_order_state_event()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO order_state_events (
            order_id,
            from_status,
            to_status,
            event_ts,
            reason
        ) VALUES (
            NEW.id,
            OLD.status,
            NEW.status,
            NOW(),
            'automatic lifecycle log'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION notify_order_change()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
BEGIN
    payload := json_build_object(
        'order_id', NEW.id,
        'status', NEW.status,
        'changed_at', NOW()
    );

    PERFORM pg_notify('order_updates', payload::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- TRIGGERS
-- ==========================================

DROP TRIGGER IF EXISTS trg_orders_set_updated_at ON orders;
CREATE TRIGGER trg_orders_set_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_orders_enforce_lifecycle ON orders;
CREATE TRIGGER trg_orders_enforce_lifecycle
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION enforce_order_lifecycle();

DROP TRIGGER IF EXISTS trg_orders_log_state_event ON orders;
CREATE TRIGGER trg_orders_log_state_event
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION log_order_state_event();

DROP TRIGGER IF EXISTS trg_orders_notify_change ON orders;
CREATE TRIGGER trg_orders_notify_change
AFTER INSERT OR UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION notify_order_change();

-- ==========================================
-- OPTIONAL EXPIRY JOB EXAMPLE
-- Run via pg_cron, Supabase scheduled function, or external scheduler.
-- ==========================================

-- UPDATE orders
-- SET status = 'expired'
-- WHERE status IN ('draft', 'payment_pending', 'vehicle_search', 'bidding')
--   AND promised_pickup_at IS NOT NULL
--   AND promised_pickup_at < NOW();
