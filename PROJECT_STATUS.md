# Zippy Logitech - Project Integration Status

**Date:** April 10, 2026  
**Status:** M1+M2+M4 Backend Complete, M3 Frontend Scaffolded  
**Next Phase:** Docker startup, Frontend-Bapi integration, ML model training

---

## Quick Status Overview

| Component | Status | Notes |
|-----------|--------|-------|
| **Obsidian Knowledge Base** | ✅ 32 files, ~8,400 lines | Complete documentation |
| **FastAPI Backend** | ✅ 32 endpoints, ~2,500 lines | M1+M2+M4 complete |
| **PostgreSQL Database** | ✅ 4 models, Alembic migrations | vehicle_models + orders + bids + matches |
| **Docker Compose** | ✅ Multi-service setup | Backend + DB (Docker Desktop not running) |
| **Alembic Migrations** | ✅ Initial schema migration | 4 tables with indexes |
| **Frontend** | ⚠️ Scaffolded (no files in current workspace) | 6 pages, Vite + React 18 + TS + Tailwind |
| **ML Pricing Service** | ✅ LightGBM + rule-based fallback | 17-feature surge model, training pipeline |
| **Route Optimization** | ✅ OR-Tools VRPTW + nearest-neighbor fallback | DRL4Route confidence gating |
| **GSD Configuration** | ⚠️ DeepSeek API 401 | Needs key refresh |
| **Unit Tests** | ✅ 20 tests | Orders, vehicles, pricing |

---

## API Endpoints (32 total)

### Health (2)
- `GET /api/v1/health` — Service health check
- `GET /api/v1/health/live` — Liveness probe

### Vehicles (7)
- `GET /vehicles` — List with filters (category, manufacturer, payload, pagination)
- `GET /vehicles/{id}` — Get by ID
- `GET /vehicles/category/{category}` — Filter by category
- `GET /vehicles/manufacturer/{mfg}` — Filter by manufacturer
- `GET /vehicles/recommend` — AI-powered vehicle recommendation
- `GET /manufacturers` — List all manufacturers
- `GET /categories` — List all vehicle categories

### Orders (6)
- `POST /orders` — Create freight transport order
- `GET /orders` — List with filters (status, city, weight, cargo_type)
- `GET /orders/{id}` — Get order details
- `PATCH /orders/{id}` — Update order status/price
- `POST /orders/{id}/cancel` — Cancel order
- `GET /orders/stats/summary` — Order statistics dashboard

### Matching (5)
- `GET /orders/{id}/match` — Find best vehicles for order (scoring algorithm)
- `POST /matches/{id}/accept` — Accept a match
- `POST /matches/{id}/reject` — Reject a match
- `GET /matches` — List matches with filters
- `GET /matches/stats` — Match statistics

### Bidding (5)
- `POST /orders/{id}/bids` — Driver places bid on order
- `GET /orders/{id}/bids` — List bids for order
- `POST /bids/{id}/accept` — Shipper accepts bid
- `POST /bids/{id}/reject` — Shipper rejects bid
- `POST /bids/{id}/counter` — Counter-offer on bid

### Pricing (2) — Rule-based
- `POST /pricing/estimate` — Basic price estimation (GST + surcharges)
- `GET /pricing/rates` — Current rate card

### ML Pricing (4) — NEW
- `POST /api/v1/pricing/ml-estimate` — ML-enhanced dynamic pricing (LightGBM surge + full breakdown)
- `POST /api/v1/pricing/surge-predict` — Demand-supply surge multiplier prediction
- `GET /api/v1/pricing/rate-card` — Detailed rate card with all multipliers
- `POST /api/v1/pricing/compare` — Zippy vs broker pricing comparison (18-25% savings)

### Route Optimization (4) — NEW
- `POST /api/v1/optimize/route` — OR-Tools VRPTW solver (multi-vehicle, time windows)
- `GET /api/v1/optimize/distance` — Haversine distance + travel time estimation
- `GET /api/v1/optimize/gst-zone` — GST zone classification for Indian cities
- `POST /api/v1/optimize/multi-stop` — Single-vehicle multi-stop route optimization

---

## Backend Architecture

### Services Layer (NEW)

```
app/services/
├── __init__.py              # Package init with exports
├── pricing_service.py       # DynamicPricingEngine + SurgePredictor
└── route_optimizer.py       # ORToolsSolver + DRL4RouteAgent
```

### ML Pricing Pipeline (`app/services/pricing_service.py`)
- **DynamicPricingEngine**: Full cost model with 17 features
  - City tier pricing (Metro 0.95x, Tier-2 1.0x, Rural 1.15x)
  - Festival/remote/hill/congestion surcharges
  - Demand-supply dynamic surge (1.0x → 1.6x)
  - Service type multiplier (standard/express/priority)
  - Customer tier adjustments (high  value -10%, low +5%)
  - Platform fee (3-5%) vs broker (8-12%)
  - GST breakdown (12% transport + 18% services)
  - Per-km breakdown calculation
- **SurgePredictor**: LightGBM model with rule-based fallback
  - Loads trained model from `models/pricing/surge_model.pkl`
  - Falls back to rule-based if model unavailable
  - 17 engineered features per BI_Tech_Stack_ML_Systems.md
  - Festival detection, city tier mapping, route difficulty scoring

### Route Optimization (`app/services/route_optimizer.py`)
- **ORToolsSolver**: VRPTW with capacity + time window constraints
  - Haversine distance matrix with road factor adjustment
  - Multi-vehicle routing with cost optimization
  - GST zone detection (6 zones for Indian cities)
  - Falls back to nearest-neighbor heuristic if OR-Tools unavailable
- **DRL4RouteAgent**: Confidence-gated switching between OR-Tools and DRL
  - If confidence >= 0.75: use DRL routing
  - If confidence < 0.75: fallback to OR-Tools deterministic
- **Indian logistics specifics**: Road speed averages, GST zone classification, road distance factors

### ML Training Pipeline (`ml/train_pricing_model.py`)
- Generates 50,000 synthetic Indian logistics samples
- 21 Indian cities (Tier 1/2/3), 21 popular corridors
- Festival seasonality, diesel price variation, demand-supply dynamics
- Trains LightGBM regression model for surge prediction
- Outputs: `surge_model.pkl`, `feature_config.json`, `feature_importance.json`
- Metrics: RMSE, MAE, R² score

---

## Database Models (4)

### vehicle_models (8 seeded)
- id, manufacturer, model_name, variant, category, body_type
- gvw_kg, payload_kg, tonnage_class
- dimensions, engine specs, mileage, axle_config, tyres, price

### orders
- Shipper info (name, phone, email)
- Origin/Destination (city, state, pincode, lat/lng)
- Cargo (type, description, weight, volume, packages)
- Flags (interstate, festival, remote, hill)
- Pricing (offered_price, negotiated_price)
- Status lifecycle: created → pending_match → matched → bidding → bid_accepted → in_transit → delivered

### bids
- order_id, vehicle_id, driver info
- bid_amount, counter_amount
- ETA estimates, status lifecycle

### matches
- order_id, vehicle_id, bid_id
- match_score (weighted: utilization 45%, mileage 25%, price 20%, interstate 10%)
- pricing breakdown (agreed_price, platform_fee, gst_amount, total_amount)
- Status lifecycle: proposed → accepted → in_progress → completed

---

## Quick Start

```bash
# Backend (requires Docker Desktop running)
cd "C:\Users\user\Downloads\MiniMax Agent_ Minimize Effort, Maximize Intelligence_files"
docker-compose up -d

# Train ML pricing model
cd backend
pip install lightgbm scikit-learn numpy joblib
python -m ml.train_pricing_model --samples 50000

# Access API docs
curl http://localhost:8000/docs
```

---

## File Structure

```
backend/
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── __init__.py          # 8 router imports
│   │   ├── health.py            # Health check (2 endpoints)
│   │   ├── vehicles.py          # Vehicle CRUD + recommend (7 endpoints)
│   │   ├── pricing.py           # Rule-based pricing (2 endpoints)
│   │   ├── orders.py            # Order lifecycle (6 endpoints)
│   │   ├── matches.py           # Vehicle-load matching (5 endpoints)
│   │   ├── bids.py              # Driver bidding (5 endpoints)
│   │   ├── ml_pricing.py        # ML dynamic pricing (4 endpoints) ✨
│   │   └── routing.py            # Route optimization (4 endpoints) ✨
│   ├── database/
│   │   └── __init__.py          # SQLAlchemy config (env vars)
│   ├── models/
│   │   ├── vehicle_model.py     # Vehicle DB model
│   │   └── order_model.py       # Order, Bid, Match models
│   ├── schemas/
│   │   ├── vehicle.py           # Vehicle Pydantic schemas
│   │   └── order.py             # Order/Bid/Match schemas
│   ├── services/
│   │   ├── __init__.py          # Package exports
│   │   ├── pricing_service.py   # DynamicPricingEngine + SurgePredictor ✨
│   │   └── route_optimizer.py   # ORToolsSolver + DRL4RouteAgent ✨
│   └── main.py                 # FastAPI app (8 routers)
├── ml/
│   ├── __init__.py
│   └── train_pricing_model.py   # LightGBM training pipeline ✨
├── models/pricing/              # Trained model output dir
├── tests/
│   ├── test_api.py              # 9 vehicle/pricing tests
│   └── test_orders.py           # 11 order/match tests
├── alembic.ini
└── requirements.txt             # Updated with lightgbm, ortools, geopy

Root:
├── .env.example                 # No real keys
├── .gitignore                   # Expanded
├── docker-compose.yml           # PostgreSQL + FastAPI
├── Dockerfile                   # Python 3.11-slim
├── init.sql                     # 8 seeded vehicles
├── PROJECT.md, ROADMAP.md, KNOWLEDGE.md, DECISIONS.md
├── PROJECT_STATUS.md            # This file
└── zippy_logistics_analysis.py  # Analysis scripts
```

---

## What's New (April 10, 2026)

### ✨ M4 ML & Advanced Features — Backend Complete
1. **ML Dynamic Pricing Service** (`app/services/pricing_service.py`)
   - `DynamicPricingEngine`: 20+ parameter pricing model
   - `SurgePredictor`: LightGBM + rule-based fallback
   - `FeatureEngineer`: 17 features with Indian logistics context
   - Festival detection, city tier mapping, route difficulty scoring
   - Customer discount system, service type multiplier

2. **Route Optimization Service** (`app/services/route_optimizer.py`)
   - `ORToolsSolver`: Full VRPTW with capacity + time windows
   - `DRL4RouteAgent`: Confidence-gated model switching
   - `RouteOptimizationService`: Unified solve/dispatch layer
   - Haversine + road factor distance calculation
   - Indian city GST zone classification
   - Nearest-neighbor fallback algorithm

3. **ML Pricing API** (`app/api/ml_pricing.py`) — 4 endpoints
   - POST `/pricing/ml-estimate` — Full ML pricing breakdown
   - POST `/pricing/surge-predict` — Surge multiplier prediction
   - GET `/pricing/rate-card` — Detailed rate card
   - POST `/pricing/compare` — Zippy vs broker comparison

4. **Route Optimization API** (`app/api/routing.py`) — 4 endpoints
   - POST `/optimize/route` — Multi-vehicle VRPTW routing
   - GET `/optimize/distance` — Distance + travel time estimation
   - GET `/optimize/gst-zone` — GST zone classification
   - POST `/optimize/multi-stop` — Single-vehicle multi-stop optimization

5. **ML Training Pipeline** (`ml/train_pricing_model.py`)
   - 50K synthetic Indian logistics samples
   - 21 cities × 21 corridors × seasonal variation
   - LightGBM regression with early stopping
   - Feature importance analysis
   - Model persistence + config export

6. **Missing `matches.py` API** — Recreated with full scoring algorithm