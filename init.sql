-- Database initialization script
-- Run automatically by docker-compose on first startup

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create vehicle_models table
CREATE TABLE IF NOT EXISTS vehicle_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    manufacturer VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    variant VARCHAR(50),
    category VARCHAR(30) NOT NULL CHECK (category IN ('LCV', 'ICV', 'HCV', 'Tipper', 'Tractor')),
    body_type VARCHAR(20) NOT NULL CHECK (body_type IN ('open', 'closed', 'tipper', 'tanker', 'trailer')),
    gvw_kg NUMERIC(10,2),
    payload_kg NUMERIC(10,2),
    tonnage_class VARCHAR(20),
    length_mm NUMERIC(10,2),
    width_mm NUMERIC(10,2),
    height_mm NUMERIC(10,2),
    wheelbase_mm NUMERIC(10,2),
    loading_length_mm NUMERIC(10,2),
    loading_width_mm NUMERIC(10,2),
    loading_height_mm NUMERIC(10,2),
    engine_cc NUMERIC(10,2),
    engine_cylinders SMALLINT,
    power_hp NUMERIC(10,2),
    torque_nm NUMERIC(10,2),
    fuel_tank_ltr NUMERIC(10,2),
    mileage_kmpl NUMERIC(5,2),
    emission_norm VARCHAR(10),
    axle_config VARCHAR(20),
    tyres SMALLINT,
    price_ex_showroom NUMERIC(15,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(manufacturer, model_name, variant)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_vm_manufacturer ON vehicle_models(manufacturer);
CREATE INDEX IF NOT EXISTS idx_vm_category ON vehicle_models(category);
CREATE INDEX IF NOT EXISTS idx_vm_tonnage ON vehicle_models(tonnage_class);
CREATE INDEX IF NOT EXISTS idx_vm_payload ON vehicle_models(payload_kg);

-- Insert sample vehicles (Ashok Leyland, Tata, Eicher, Mahindra)
INSERT INTO vehicle_models (manufacturer, model_name, variant, category, body_type, gvw_kg, payload_kg, tonnage_class, length_mm, width_mm, height_mm, wheelbase_mm, loading_length_mm, loading_width_mm, loading_height_mm, engine_cc, engine_cylinders, power_hp, torque_nm, fuel_tank_ltr, mileage_kmpl, emission_norm, axle_config, tyres, price_ex_showroom) VALUES
('Ashok Leyland', 'BOSS 1215', 'HB', 'ICV', 'closed', 11990, 7710, '12-ton', 6422, 2220, 2670, 3400, 6422, 2270, 590, 3839, 4, 123, 400, 208, 7.0, 'BS-VI', '4x2', 6, 1950000),
('Ashok Leyland', 'BOSS 1415', 'HB', 'ICV', 'closed', 11500, 7859, '14-ton', 6422, 2220, 2670, 3400, 6422, 2270, 590, 3839, 4, 150, 450, 208, 7.5, 'BS-VI', '4x2', 6, 2250000),
('Ashok Leyland', 'BOSS 1615', 'HB', 'HCV', 'closed', 16500, 11000, '16-ton', 8535, 2350, 2850, 4200, 6700, 2350, 600, 5880, 4, 160, 500, 300, 6.5, 'BS-VI', '4x2', 6, 2800000),
('Tata Motors', '407 Gold SFC', '29 WB', 'LCV', 'closed', 4650, 2267, '2-ton', 4850, 2100, 2270, 2955, 3050, 1900, 400, 2956, 4, 100, 300, 60, 10.0, 'BS-VI', '4x2', 4, 850000),
('Tata Motors', 'Ultra 1014', '4x2', 'ICV', 'closed', 10500, 7000, '10-ton', 7620, 2350, 2800, 4200, 5490, 2350, 600, 3700, 4, 140, 450, 150, 8.0, 'BS-VI', '4x2', 6, 2100000),
('Eicher', 'Pro 2095', 'XP', 'ICV', 'closed', 11280, 7500, '10-ton', 7395, 2350, 2800, 4420, 5355, 2002, 600, 3000, 4, 140, 400, 190, 7.5, 'BS-VI', '4x2', 6, 1950000),
('Mahindra', 'Bolero Camper', 'Pickup', 'LCV', 'open', 3490, 1500, '1.5-ton', 4750, 1900, 2050, 3050, 2700, 1800, 400, 2520, 4, 75, 200, 50, 11.0, 'BS-VI', '4x2', 4, 750000),
('Mahindra', 'Blazo X 25', '6x2', 'HCV', 'closed', 25000, 17000, '25-ton', 9750, 2550, 3100, 5350, 7800, 2550, 650, 7200, 6, 200, 850, 365, 5.0, 'BS-VI', '6x2', 8, 3800000)
ON CONFLICT (manufacturer, model_name, variant) DO NOTHING;

-- Verify data
SELECT '✅ Loaded ' || COUNT(*) || ' vehicle models' AS status FROM vehicle_models;