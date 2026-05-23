# Vehicle Model Database

> **Commercial Vehicle Specifications for Logistics Platform**
> **Last Updated:** April 7, 2026
> **Total Records:** 26 vehicles across 4 manufacturers

---

## 1. Database Schema

### Table: `vehicle_models`

| Column              | Type         | Description                                                  |
| ------------------- | ------------ | ------------------------------------------------------------ |
| `id`                | UUID         | Primary key (auto-generated)                                 |
| `manufacturer`      | VARCHAR(50)  | Vehicle manufacturer (Tata, Ashok Leyland, Eicher, Mahindra) |
| `model_name`        | VARCHAR(100) | Model name (e.g., 'BOSS 1215', 'Ultra 1014')                 |
| `variant`           | VARCHAR(50)  | Specific variant (e.g., 'HB', 'XP', '4x2')                   |
| `category`          | VARCHAR(30)  | Vehicle category: LCV, ICV, HCV, Tipper, Tractor             |
| `body_type`         | VARCHAR(20)  | Body configuration: open, closed, tipper, tanker, trailer    |
| `gvw_kg`            | NUMERIC      | Gross Vehicle Weight in kg                                   |
| `payload_kg`        | NUMERIC      | Maximum payload capacity in kg                               |
| `tonnage_class`     | VARCHAR(20)  | Tonnage classification (e.g., '12-ton')                      |
| `length_mm`         | NUMERIC      | Overall length in mm                                         |
| `width_mm`          | NUMERIC      | Overall width in mm                                          |
| `height_mm`         | NUMERIC      | Overall height in mm                                         |
| `wheelbase_mm`      | NUMERIC      | Wheelbase in mm                                              |
| `loading_length_mm` | NUMERIC      | Cargo loading length in mm                                   |
| `loading_width_mm`  | NUMERIC      | Cargo loading width in mm                                    |
| `loading_height_mm` | NUMERIC      | Cargo loading height in mm                                   |
| `engine_cc`         | NUMERIC      | Engine displacement in cc                                    |
| `engine_cylinders`  | SMALLINT     | Number of engine cylinders                                   |
| `power_hp`          | NUMERIC      | Engine power in HP                                           |
| `torque_nm`         | NUMERIC      | Engine torque in Nm                                          |
| `fuel_tank_ltr`     | NUMERIC      | Fuel tank capacity in liters                                 |
| `mileage_kmpl`      | NUMERIC      | Fuel efficiency in km/l                                      |
| `emission_norm`     | VARCHAR(10)  | Emission standard (BS-IV, BS-VI)                             |
| `axle_config`       | VARCHAR(20)  | Axle configuration (4x2, 6x2, 6x4, 8x4)                      |
| `tyres`             | SMALLINT     | Number of tyres                                              |
| `price_ex_showroom` | NUMERIC      | Ex-showroom price in INR                                     |
| `is_active`         | BOOLEAN      | Active/inactive status                                       |
| `created_at`        | TIMESTAMPTZ  | Creation timestamp                                           |

### Indexes

```sql
CREATE INDEX idx_vm_manufacturer ON vehicle_models(manufacturer);
CREATE INDEX idx_vm_category ON vehicle_models(category);
CREATE INDEX idx_vm_tonnage ON vehicle_models(tonnage_class);
```

---

## 2. Vehicle Categories

### LCV (Light Commercial Vehicle)
- **GVW Range:** 3.5 - 8.5 tonnes
- **Payload:** 1,500 - 5,000 kg
- **Typical Use:** Urban delivery, small shipments, intra-city transport
- **Examples:** Tata 407, Ashok Leyland Partner, Mahindra Bolero

### ICV (Intermediate Commercial Vehicle)
- **GVW Range:** 8.5 - 16 tonnes
- **Payload:** 5,000 - 11,000 kg
- **Typical Use:** Regional transport, medium distances (100-500 km)
- **Examples:** Tata Ultra, Ashok Leyland BOSS, Eicher Pro 20

### HCV (Heavy Commercial Vehicle)
- **GVW Range:** 16 - 42 tonnes
- **Payload:** 11,000 - 28,000 kg
- **Typical Use:** Long-distance freight, industrial goods, multi-state transport
- **Examples:** Tata Signa, Mahindra Blazo, Ashok Leyland Ecomet

### Tipper
- **GVW Range:** 25 - 40 tonnes
- **Payload:** 20,000 - 35,000 kg
- **Typical Use:** Construction material, aggregates, mining
- **Examples:** Tata Tipper, Ashok Leyland Tipper

---

## 3. Complete Vehicle Inventory

### Ashok Leyland (6 models)

| Model             | Variant | Category | Body   | GVW (kg) | Payload (kg) | Tonnage | Engine  | Power (HP) | Price (₹) |
| ----------------- | ------- | -------- | ------ | -------- | ------------ | ------- | ------- | ---------- | --------- |
| **BOSS 1215**     | HB      | ICV      | closed | 11,990   | 7,710        | 12-ton  | 3,839cc | 123        | 19,50,000 |
| **BOSS 1415**     | HB      | ICV      | closed | 11,500   | 7,859        | 14-ton  | 3,839cc | 150        | 22,50,000 |
| **BOSS 1615**     | HB      | HCV      | closed | 16,500   | 11,000       | 16-ton  | 5,880cc | 160        | 28,00,000 |
| **BOSS 1915**     | HB      | HCV      | closed | 18,490   | 12,500       | 19-ton  | 5,880cc | 200        | 35,00,000 |
| **Partner Super** | 4T      | LCV      | closed | 7,490    | 4,500        | 4-ton   | 2,956cc | 100        | 18,00,000 |
| **ecomet Star**   | 1515    | ICV      | closed | 15,200   | 10,000       | 15-ton  | 5,880cc | 150        | 26,00,000 |
| **Tipper 8x4**    | 2518    | Tipper   | tipper | 31,000   | 20,000       | 25-ton  | 5,880cc | 250        | 45,00,000 |

**Key Features:**
- BS-VI emission compliant
- H-series engines with iGen6 technology
- Fuel efficiency: 6.0-7.5 kmpl
- Available in 4x2, 6x2, 8x4 configurations

---

### Tata Motors (7 models)

| Model            | Variant | Category | Body   | GVW (kg) | Payload (kg) | Tonnage | Engine  | Power (HP) | Price (₹) |
| ---------------- | ------- | -------- | ------ | -------- | ------------ | ------- | ------- | ---------- | --------- |
| **407 Gold SFC** | 29 WB   | LCV      | closed | 4,650    | 2,267        | 2-ton   | 2,956cc | 100        | 8,50,000  |
| **407 Gold SFC** | 35 WB   | LCV      | closed | 5,550    | 2,800        | 3-ton   | 3,783cc | 115        | 9,50,000  |
| **Ultra 814**    | 4x2     | LCV      | closed | 8,250    | 5,000        | 5-ton   | 2,956cc | 125        | 14,50,000 |
| **Ultra 1014**   | 4x2     | ICV      | closed | 10,500   | 7,000        | 10-ton  | 3,700cc | 140        | 21,00,000 |
| **SIGNA 2523**   | 6x4     | HCV      | closed | 25,000   | 16,000       | 25-ton  | 6,700cc | 250        | 42,00,000 |
| **SIGNA 4225**   | 10x2    | HCV      | closed | 42,000   | 28,000       | 40-ton  | 6,700cc | 280        | 55,00,000 |
| **Tipper 10x4**  | 3523    | Tipper   | tipper | 35,000   | 23,000       | 35-ton  | 6,700cc | 280        | 55,00,000 |

**Key Features:**
- 3S technology (Safe, Smart, Sleek)
- Cummins and Tata engines
- Fuel efficiency: 4.0-10.0 kmpl
- India's largest commercial vehicle manufacturer

---

### Eicher (4 models)

| Model        | Variant | Category | Body   | GVW (kg) | Payload (kg) | Tonnage | Engine  | Power (HP) | Price (₹) |
| ------------ | ------- | -------- | ------ | -------- | ------------ | ------- | ------- | ---------- | --------- |
| **Pro 2095** | XP      | ICV      | closed | 11,280   | 7,500        | 10-ton  | 3,000cc | 140        | 19,50,000 |
| **Pro 2095** | XP 16ft | ICV      | closed | 11,449   | 7,800        | 11-ton  | 3,000cc | 140        | 20,50,000 |
| **Pro 3015** | 6x2     | HCV      | closed | 16,500   | 11,000       | 16-ton  | 4,700cc | 180        | 28,00,000 |
| **Pro 6015** | 6x4     | HCV      | closed | 28,000   | 19,000       | 28-ton  | 6,700cc | 250        | 45,00,000 |

**Key Features:**
- Volvo Eicher Commercial Vehicles partnership
- Pro series with advanced cab design
- Fuel efficiency: 5.0-7.5 kmpl
- Focus on driver comfort and safety

---

### Mahindra (8 models)

| Model             | Variant | Category | Body   | GVW (kg) | Payload (kg) | Tonnage | Engine  | Power (HP) | Price (₹) |
| ----------------- | ------- | -------- | ------ | -------- | ------------ | ------- | ------- | ---------- | --------- |
| **Bolero Camper** | Pickup  | LCV      | open   | 3,490    | 1,500        | 1.5-ton | 2,520cc | 75         | 7,50,000  |
| **Maxx HD**       | Pickup  | LCV      | open   | 4,990    | 2,800        | 3-ton   | 2,520cc | 85         | 9,50,000  |
| **Jayo**          | 2518    | ICV      | closed | 12,900   | 8,500        | 12-ton  | 3,700cc | 150        | 21,00,000 |
| **Blazo X 25**    | 6x2     | HCV      | closed | 25,000   | 17,000       | 25-ton  | 7,200cc | 200        | 38,00,000 |
| **Blazo X 28**    | 6x2     | HCV      | closed | 28,000   | 19,000       | 28-ton  | 7,200cc | 206        | 42,00,000 |
| **Blazo X 35**    | 8x2     | HCV      | closed | 35,000   | 24,000       | 35-ton  | 7,200cc | 206        | 52,00,000 |
| **Blazo X 42**    | 10x2    | HCV      | closed | 42,000   | 28,000       | 40-ton  | 7,200cc | 206        | 60,00,000 |

**Key Features:**
- m-POWER engines with FuelSmart technology
- Fuel efficiency: 3.8-5.0 kmpl for HCV
- Strong presence in pickup/pickup segments
- Blazo series for heavy haulage

---

## 4. Usage by Cargo Type

### Small Parcels & E-commerce (< 2 tonnes)
**Recommended:** Tata 407 Gold SFC, Mahindra Bolero Camper
- **Loading Volume:** 5-8 cubic meters
- **Typical Use:** E-commerce deliveries, small shipments, last-mile delivery

### General Cargo (2-5 tonnes)
**Recommended:** Tata Ultra 814, Ashok Leyland Partner Super
- **Loading Volume:** 12-18 cubic meters
- **Typical Use:** Consumer goods, FMCG, electronics

### Medium Freight (5-12 tonnes)
**Recommended:** Tata Ultra 1014, Ashok Leyland BOSS 1215/1415, Eicher Pro 2095
- **Loading Volume:** 20-35 cubic meters
- **Typical Use:** Industrial goods, machinery parts, packaged materials

### Heavy Freight (12-20 tonnes)
**Recommended:** Ashok Leyland BOSS 1615/1915, Mahindra Jayo
- **Loading Volume:** 40-55 cubic meters
- **Typical Use:** Construction materials, steel, cement

### Bulk & Heavy Haulage (20-42 tonnes)
**Recommended:** Tata SIGNA series, Mahindra Blazo series, Ashok Leyland Ecomet
- **Loading Volume:** 60-90 cubic meters
- **Typical Use:** Industrial raw materials, project cargo, multi-state transport

### Construction & Mining
**Recommended:** Tata Tipper, Ashok Leyland Tipper
- **Body Type:** Tipper (open hydraulic)
- **Typical Use:** Sand, aggregate, construction debris, mining materials

---

## 5. Pricing Reference Matrix

### By Category

| Category | Min Price (₹) | Max Price (₹) | Average (₹) |
| -------- | ------------- | ------------- | ----------- |
| LCV      | 7,50,000      | 18,00,000     | 11,25,000   |
| ICV      | 19,50,000     | 28,00,000     | 23,75,000   |
| HCV      | 35,00,000     | 60,00,000     | 47,50,000   |
| Tipper   | 45,00,000     | 55,00,000     | 50,00,000   |

### By Manufacturer

| Manufacturer  | Entry Level (₹) | Premium (₹) | Fleet Focus      |
| ------------- | --------------- | ----------- | ---------------- |
| Tata Motors   | 8,50,000        | 55,00,000   | All segments     |
| Ashok Leyland | 18,00,000       | 45,00,000   | ICV, HCV, Tipper |
| Mahindra      | 7,50,000        | 60,00,000   | Pickup, HCV      |
| Eicher        | 19,50,000       | 45,00,000   | ICV, HCV         |

---

## 6. Technical Specifications Summary

### Fuel Efficiency by Category

| Category | Best (kmpl)   | Worst (kmpl)     | Average (kmpl) |
| -------- | ------------- | ---------------- | -------------- |
| LCV      | 11.0 (Bolero) | 9.0 (Ultra 814)  | 10.2           |
| ICV      | 7.5 (Eicher)  | 6.0 (BOSS 1415)  | 6.8            |
| HCV      | 5.0 (Blazo)   | 3.8 (Blazo X 42) | 4.6            |
| Tipper   | 4.0 (AL)      | 3.8 (Tata)       | 3.9            |

### Engine Power by Category

| Category | Min (HP) | Max (HP) | Typical |
| -------- | -------- | -------- | ------- |
| LCV      | 75       | 125      | 100     |
| ICV      | 123      | 180      | 150     |
| HCV      | 160      | 280      | 220     |
| Tipper   | 250      | 280      | 265     |

### Axle Configurations

| Config | GVW Range       | Use Case                | Models               |
| ------ | --------------- | ----------------------- | -------------------- |
| 4x2    | 3.5 - 19 tonnes | Light to medium freight | Most common          |
| 6x2    | 16 - 28 tonnes  | Heavy freight           | Eicher, Mahindra     |
| 6x4    | 25 - 35 tonnes  | Heavy haulage           | Tata, Eicher         |
| 8x2    | 35 tonnes       | Heavy freight           | Mahindra Blazo       |
| 8x4    | 31 tonnes       | Tipper, heavy duty      | Ashok Leyland Tipper |
| 10x2   | 42 tonnes       | Maximum payload         | Tata, Mahindra       |
| 10x4   | 35 tonnes       | Tipper                  | Tata Tipper          |

---

## 7. SQL Insert Statements

### Create Table

```sql
CREATE TABLE IF NOT EXISTS vehicle_models (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  manufacturer VARCHAR(50) NOT NULL,
  model_name VARCHAR(100) NOT NULL,
  variant VARCHAR(50),
  category VARCHAR(30) CHECK (category IN ('LCV', 'ICV', 'HCV', 'Tipper', 'Tractor')),
  body_type VARCHAR(20) CHECK (body_type IN ('open', 'closed', 'tipper', 'tanker', 'trailer')),
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

CREATE INDEX IF NOT EXISTS idx_vm_manufacturer ON vehicle_models(manufacturer);
CREATE INDEX IF NOT EXISTS idx_vm_category ON vehicle_models(category);
CREATE INDEX IF NOT EXISTS idx_vm_tonnage ON vehicle_models(tonnage_class);
```

### Insert Data

```sql
INSERT INTO vehicle_models (manufacturer, model_name, variant, category, body_type, gvw_kg, payload_kg, tonnage_class, length_mm, width_mm, height_mm, wheelbase_mm, loading_length_mm, loading_width_mm, loading_height_mm, engine_cc, engine_cylinders, power_hp, torque_nm, fuel_tank_ltr, mileage_kmpl, emission_norm, axle_config, tyres, price_ex_showroom) VALUES
('Ashok Leyland','BOSS 1215','HB','ICV','closed',11990,7710,'12-ton',6422,2220,2670,3400,6422,2270,590,3839,4,123,400,208,7.0,'BS-VI','4x2',6,1950000),
('Ashok Leyland','BOSS 1415','HB','ICV','closed',11500,7859,'14-ton',6422,2220,2670,3400,6422,2270,590,3839,4,150,450,208,7.5,'BS-VI','4x2',6,2250000),
('Ashok Leyland','BOSS 1615','HB','HCV','closed',16500,11000,'16-ton',8535,2350,2850,4200,6700,2350,600,5880,4,160,500,300,6.5,'BS-VI','4x2',6,2800000),
('Ashok Leyland','BOSS 1915','HB','HCV','closed',18490,12500,'19-ton',9145,2350,2900,5200,7315,2350,600,5880,4,200,650,350,6.0,'BS-VI','4x2',6,3500000),
('Ashok Leyland','Partner Super','4T','LCV','closed',7490,4500,'4-ton',5490,2100,2650,3300,4200,2100,550,2956,4,100,300,90,10.0,'BS-VI','4x2',4,1800000),
('Ashok Leyland','ecomet Star','1515','ICV','closed',15200,10000,'15-ton',7620,2350,2850,3800,6100,2350,600,5880,4,150,480,250,6.5,'BS-VI','4x2',6,2600000),
('Tata Motors','407 Gold SFC','29 WB','LCV','closed',4650,2267,'2-ton',4850,2100,2270,2955,3050,1900,400,2956,4,100,300,60,10.0,'BS-VI','4x2',4,850000),
('Tata Motors','407 Gold SFC','35 WB','LCV','closed',5550,2800,'3-ton',5350,2100,2350,3350,3500,1900,450,3783,4,115,325,60,9.5,'BS-VI','4x2',4,950000),
('Tata Motors','Ultra 814','4x2','LCV','closed',8250,5000,'5-ton',6125,2200,2680,3650,4270,2200,550,2956,4,125,380,90,9.0,'BS-VI','4x2',4,1450000),
('Tata Motors','Ultra 1014','4x2','ICV','closed',10500,7000,'10-ton',7620,2350,2800,4200,5490,2350,600,3700,4,140,450,150,8.0,'BS-VI','4x2',6,2100000),
('Tata Motors','SIGNA 2523','6x4','HCV','closed',25000,16000,'25-ton',10325,2550,3150,5800,8530,2550,650,6700,6,250,950,365,4.5,'BS-VI','6x4',10,4200000),
('Tata Motors','SIGNA 4225','10x2','HCV','closed',42000,28000,'40-ton',12350,2550,3200,6800,10000,2550,700,6700,6,280,1050,400,4.0,'BS-VI','10x2',14,5500000),
('Eicher','Pro 2095','XP','ICV','closed',11280,7500,'10-ton',7395,2350,2800,4420,5355,2002,600,3000,4,140,400,190,7.5,'BS-VI','4x2',6,1950000),
('Eicher','Pro 2095','XP 16ft','ICV','closed',11449,7800,'11-ton',7685,2350,2800,4770,5500,2002,600,3000,4,140,400,190,7.5,'BS-VI','4x2',6,2050000),
('Eicher','Pro 3015','6x2','HCV','closed',16500,11000,'16-ton',9145,2450,2950,5200,7315,2450,650,4700,4,180,600,250,6.0,'BS-VI','6x2',8,2800000),
('Eicher','Pro 6015','6x4','HCV','closed',28000,19000,'28-ton',10500,2550,3100,6100,8530,2550,700,6700,6,250,900,350,5.0,'BS-VI','6x4',10,4500000),
('Mahindra','Bolero Camper','Pickup','LCV','open',3490,1500,'1.5-ton',4750,1900,2050,3050,2700,1800,400,2520,4,75,200,50,11.0,'BS-VI','4x2',4,750000),
('Mahindra','Maxx HD','Pickup','LCV','open',4990,2800,'3-ton',5490,2000,2450,3300,3200,1900,450,2520,4,85,250,60,10.5,'BS-VI','4x2',4,950000),
('Mahindra','Jayo','2518','ICV','closed',12900,8500,'12-ton',7620,2350,2850,4200,6100,2350,600,3700,4,150,500,180,7.5,'BS-VI','4x2',6,2100000),
('Mahindra','Blazo X 25','6x2','HCV','closed',25000,17000,'25-ton',9750,2550,3100,5350,7800,2550,650,7200,6,200,850,365,5.0,'BS-VI','6x2',8,3800000),
('Mahindra','Blazo X 28','6x2','HCV','closed',28000,19000,'28-ton',10250,2550,3150,6100,8200,2550,700,7200,6,206,950,415,4.5,'BS-VI','6x2',10,4200000),
('Mahindra','Blazo X 35','8x2','HCV','closed',35000,24000,'35-ton',11500,2550,3200,6800,9500,2550,700,7200,6,206,1050,415,4.0,'BS-VI','8x2',12,5200000),
('Mahindra','Blazo X 42','10x2','HCV','closed',42000,28000,'40-ton',12500,2550,3200,6770,10500,2550,700,7200,6,206,1050,415,3.8,'BS-VI','10x2',14,6000000),
('Ashok Leyland','Tipper 8x4','2518','Tipper','tipper',31000,20000,'25-ton',8950,2550,3200,5400,4800,2350,1200,5880,6,250,850,300,4.0,'BS-VI','8x4',12,4500000),
('Tata Motors','Tipper 10x4','3523','Tipper','tipper',35000,23000,'35-ton',9850,2550,3400,6200,5200,2350,1300,6700,6,280,950,350,3.8,'BS-VI','10x4',14,5500000)
ON CONFLICT (manufacturer, model_name, variant) DO NOTHING;
```

### Verify Data

```sql
-- Count by manufacturer
SELECT manufacturer, COUNT(*) as count 
FROM vehicle_models 
GROUP BY manufacturer 
ORDER BY manufacturer;

-- Count by category
SELECT category, COUNT(*) as count 
FROM vehicle_models 
GROUP BY category 
ORDER BY count DESC;

-- View all active vehicles
SELECT manufacturer, model_name, variant, category, tonnage_class, payload_kg, price_ex_showroom
FROM vehicle_models 
WHERE is_active = true
ORDER BY category, payload_kg;
```

---

## 8. API Integration

### Backend Endpoints (FastAPI)

```python
# vehicles/router.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/models", response_model=List[VehicleModelResponse])
async def list_vehicle_models(
    category: Optional[str] = Query(None, enum=["LCV", "ICV", "HCV", "Tipper"]),
    manufacturer: Optional[str] = None,
    min_payload: Optional[int] = Query(None, ge=0),
    max_payload: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """
    List all vehicle models with optional filtering.
    
    Query Parameters:
    - category: Vehicle category (LCV, ICV, HCV, Tipper)
    - manufacturer: Filter by manufacturer
    - min_payload: Minimum payload capacity (kg)
    - max_payload: Maximum payload capacity (kg)
    """
    query = db.query(VehicleModel).filter(VehicleModel.is_active == True)
    
    if category:
        query = query.filter(VehicleModel.category == category)
    if manufacturer:
        query = query.filter(VehicleModel.manufacturer == manufacturer)
    if min_payload:
        query = query.filter(VehicleModel.payload_kg >= min_payload)
    if max_payload:
        query = query.filter(VehicleModel.payload_kg <= max_payload)
    
    return query.order_by(VehicleModel.payload_kg).all()

@router.get("/models/{model_id}", response_model=VehicleModelDetailResponse)
async def get_vehicle_model(model_id: UUID, db: Session = Depends(get_db)):
    """Get detailed information about a specific vehicle model"""
    model = db.query(VehicleModel).filter(VehicleModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Vehicle model not found")
    return model

@router.get("/recommend", response_model=List[VehicleRecommendation])
async def recommend_vehicles(
    weight_kg: float = Query(..., gt=0, description="Cargo weight in kg"),
    volume_cbm: Optional[float] = Query(None, gt=0, description="Cargo volume in cubic meters"),
    distance_km: Optional[float] = Query(None, gt=0, description="Transport distance in km"),
    db: Session = Depends(get_db)
):
    """
    Recommend suitable vehicles based on cargo requirements.
    
    Returns vehicles with payload capacity >= required weight,
    sorted by efficiency score.
    """
    # Add 20% buffer to weight
    required_payload = weight_kg * 1.2
    
    candidates = db.query(VehicleModel).filter(
        VehicleModel.is_active == True,
        VehicleModel.payload_kg >= required_payload
    ).order_by(VehicleModel.payload_kg).all()
    
    recommendations = []
    for vehicle in candidates[:5]:  # Top 5 recommendations
        efficiency_score = calculate_efficiency_score(vehicle, distance_km)
        recommendations.append({
            "vehicle": vehicle,
            "efficiency_score": efficiency_score,
            "recommended": efficiency_score > 0.7
        })
    
    return recommendations

@router.get("/manufacturers")
async def get_manufacturers(db: Session = Depends(get_db)):
    """Get list of all manufacturers"""
    manufacturers = db.query(VehicleModel.manufacturer).distinct().all()
    return [m[0] for m in manufacturers]
```

---

## 9. Integration with Pricing Engine

### Vehicle Selection in Booking Flow

```python
# pricing/vehicle_selector.py

async def select_optimal_vehicle(
    cargo_weight: float,
    cargo_volume: float,
    route_distance: float,
    preferred_category: Optional[str] = None
) -> VehicleModel:
    """
    Select optimal vehicle based on cargo and route characteristics.
    
    Logic:
    1. Filter by minimum payload capacity (weight + 20% buffer)
    2. Filter by volume if specified
    3. Score by efficiency (mileage, fuel cost, utilization %)
    4. Return top recommendation
    """
    
    # Minimum payload with buffer
    min_payload = cargo_weight * 1.2
    
    # Query candidates
    query = db.query(VehicleModel).filter(
        VehicleModel.is_active == True,
        VehicleModel.payload_kg >= min_payload
    )
    
    if preferred_category:
        query = query.filter(VehicleModel.category == preferred_category)
    
    candidates = query.all()
    
    if not candidates:
        raise ValueError(f"No vehicles available for {cargo_weight}kg payload")
    
    # Score each candidate
    scored_vehicles = []
    for vehicle in candidates:
        # Utilization score (higher is better, max 1.0)
        utilization = cargo_weight / vehicle.payload_kg
        utilization_score = min(utilization / 0.85, 1.0)  # Optimal at 85% utilization
        
        # Fuel efficiency score
        fuel_score = vehicle.mileage_kmpl / 10.0  # Normalize to 10 kmpl
        
        # Cost score (lower price = better)
        price_score = 1 - (vehicle.price_ex_showroom / 6000000)
        
        # Combined score
        total_score = (utilization_score * 0.5) + (fuel_score * 0.3) + (price_score * 0.2)
        
        scored_vehicles.append({
            "vehicle": vehicle,
            "score": total_score,
            "utilization": utilization,
        })
    
    # Sort by score descending
    scored_vehicles.sort(key=lambda x: x["score"], reverse=True)
    
    return scored_vehicles[0]["vehicle"]
```

---

## 10. Statistics Summary

### By Manufacturer
| Manufacturer  | Count | Avg Price (₹) | Avg Payload (kg) |
| ------------- | ----- | ------------- | ---------------- |
| Ashok Leyland | 7     | 29,14,286     | 10,838           |
| Tata Motors   | 7     | 27,07,143     | 11,438           |
| Eicher        | 4     | 28,12,500     | 10,325           |
| Mahindra      | 8     | 27,18,750     | 13,388           |

### By Category
| Category | Count | Payload Range (kg) | Price Range (₹)       |
| -------- | ----- | ------------------ | --------------------- |
| LCV      | 7     | 1,500 - 5,000      | 7,50,000 - 18,00,000  |
| ICV      | 8     | 5,000 - 11,000     | 18,00,000 - 28,00,000 |
| HCV      | 9     | 11,000 - 28,000    | 28,00,000 - 60,00,000 |
| Tipper   | 2     | 20,000 - 23,000    | 45,00,000 - 55,00,000 |

### Tonnage Classes
| Class            | Count | Use Case               |
| ---------------- | ----- | ---------------------- |
| 1.5-ton to 5-ton | 7     | Last-mile, small cargo |
| 10-ton to 16-ton | 8     | Regional transport     |
| 19-ton to 28-ton | 8     | Long-distance freight  |
| 35-ton to 40-ton | 3     | Heavy haulage          |

---

*Document Version: 1.0*
*Last Updated: April 7, 2026*
*Total Vehicles: 26 models across 4 manufacturers*
