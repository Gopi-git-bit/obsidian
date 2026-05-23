# Technology Stack & ML Systems Architecture

> **Production-Grade ML Pipeline, Algorithms & Infrastructure**

---

## Executive Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **ML Prediction** | LightGBM/XGBoost | Surge pricing, demand forecasting |
| **Optimization** | OR-Tools + DRL4Route | Route planning (VRP/VRPTW) |
| **Streaming** | Kafka/Redis Streams | Real-time event processing |
| **Feature Store** | Redis + PostgreSQL | Fast feature access |
| **API Serving** | FastAPI | Model inference endpoints |
| **Monitoring** | Prometheus + Grafana | Performance tracking |

---

## Part 1: LightGBM Surge Prediction Model

### Feature Engineering

#### Core Features (17 Total)
```python
features = [
    # Demand-Supply (2)
    "demand",
    "supply", 
    "demand_supply_ratio",  # demand / supply
    
    # Location (3)
    "city_tier",           # 1, 2, 3
    "is_remote",           # Boolean
    "is_hill",             # Boolean
    
    # Time (4)
    "hour",                # 0-23
    "day_of_week",         # 0-6
    "is_weekend",          # day in [5,6]
    "is_festival",         # Boolean
    
    # Route (2)
    "distance_km",
    "rds_score",           # Route Difficulty Score 0-1
    
    # Traffic (1)
    "congestion_level",    # 0-1
    
    # Vehicle (2)
    "vehicle_type",        # Encoded
    "vehicle_age",         # Years
    
    # Market (1)
    "diesel_price",
    
    # Customer (1)
    "customer_type"        # Encoded
]
```

### Model Architecture
```python
import lightgbm as lgb

model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8
)
```

### Training Pipeline
```python
# 1. Feature Engineering
df["demand_supply_ratio"] = df["demand"] / df["supply"].replace(0, 1)
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Training
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric="rmse",
    verbose=50
)

# 4. Evaluation
preds = model.predict(X_test)
rmse = mean_squared_error(y_test, preds, squared=False)

# 5. Save
joblib.dump(model, "surge_model.pkl")
```

### Real-Time Inference
```python
class SurgePredictor:
    def __init__(self, model_path="surge_model.pkl"):
        self.model = joblib.load(model_path)
    
    def predict(self, input_data: dict) -> float:
        features = np.array([[
            input_data["demand"],
            input_data["supply"],
            input_data["demand"] / max(input_data["supply"], 1),
            input_data["city_tier"],
            int(input_data["is_remote"]),
            int(input_data["is_hill"]),
            input_data["hour"],
            input_data["day_of_week"],
            int(input_data["day_of_week"] in [5, 6]),
            int(input_data["is_festival"]),
            input_data["distance_km"],
            input_data["rds_score"],
            input_data["congestion_level"],
            input_data["vehicle_type"],
            input_data["vehicle_age"],
            input_data["diesel_price"],
            input_data["customer_type"]
        ]])
        
        prediction = self.model.predict(features)[0]
        return max(1.0, min(prediction, 3.0))  # Clamp 1.0-3.0
```

---

## Part 2: Industry Algorithms by System

### OMS (Order Management System)

| Problem | Algorithm | Real-World Example |
|---------|-----------|-------------------|
| **Order Routing** | MILP, Constraint Satisfaction, Contextual Bandits | Amazon: MILP + RL for fulfillment center routing |
| **Dynamic Pricing** | XGBoost/LightGBM, Prophet, TFT, RL | Uber Freight: XGBoost + contextual pricing |
| **Fraud Detection** | Isolation Forest, GNN, Rule+ML Hybrid | DHL Commerce: GNN for shipment fraud rings |
| **Demand Sensing** | Hierarchical Bayesian, Croston's Method, Kalman Filter | Walmart: Bayesian demand sensing |

### IMS (Inventory Management System)

| Problem | Algorithm | Real-World Example |
|---------|-----------|-------------------|
| **Demand Forecasting** | SARIMA, TFT, Hierarchical Forecasting | Target: TFT + hierarchical reconciliation |
| **Safety Stock** | Newsvendor Model, (s,S) Policies, MEIO | Amazon: MEIO + stochastic optimization |
| **Slotting/Bin Packing** | FFD, Genetic Algorithms, Constraint Programming | Ocado: Genetic algorithms + CP |
| **Inventory Classification** | ABC/XYZ, K-Means, RFM Scoring | IKEA: ABC + demand variability clustering |
| **Markdown Optimization** | Price Elasticity, Survival Analysis, RL | H&M: Survival analysis + RL for clearance |

### TMS (Transportation Management System)

| Problem | Algorithm | Real-World Example |
|---------|-----------|-------------------|
| **Route Optimization (VRP)** | OR-Tools CP-SAT, Tabu Search, Simulated Annealing, DRL | UPS (ORION): Tabu search, Amazon: DRL4Route-GAE |
| **Load Optimization** | 3D Bin Packing, MILP, CP | Maersk: CP + MILP for container stowage |
| **Carrier Selection** | MCDA, Combinatorial Auctions, ML Classification | C.H. Robinson: MCDA + predictive reliability |
| **ETA Prediction** | GNN, Gradient Boosting, Kalman Filters, LSTM | Uber: GNN + gradient boosting |
| **Predictive Maintenance** | Survival Analysis, XGBoost, LSTM on Telematics | Schneider National: LSTM on engine hours |
| **Dynamic Dispatch** | Hungarian Algorithm, Contextual Bandits, DRL | Uber Freight: Contextual bandits + DRL |

---

## Part 2B: Route Optimization Algorithms for TMS

### Algorithm Comparison (Zippy-Specific)

| Algorithm | Use Case | Complexity | Speed (100+ stops) | India Strength | Zippy Fit |
|-----------|----------|------------|---------------------|----------------|-----------|
| **TSP** | Single-vehicle intra-city loops | Low | Fast | Basic return trip closure | Use OR-Tools in FastAPI; tie to OMS events |
| **VRP/VRPTW** | Multi-vehicle with time windows | Medium | Medium | Handles traffic delays | Core for TMS; fallback to radius expansion |
| **Genetic Algorithm** | Evolving complex fleets | High | Slow | Optimizes bin packing + returns | Hybrid with ACO in Celery tasks |
| **ACO** | Dynamic/real-time rerouting | High | Medium-Fast | Adapts to disruptions (weather/roads) | RAG-enhanced pheromones; loaded returns |
| **Tabu Search/Annealing** | Emergency/fallback optimization | Medium | Medium | Robust for variable conditions | Use in fallbacks; quick for mobile previews |
| **AI/ML Hybrids** | Predictive/full autonomy | Very High | Variable | 25-40% efficiency gains | LightGBM + DRL; predict return trips |

### ACO Variants for Zippy

| Variant | Purpose | Open Routes | Backhaul Support | ML Enhancement |
|---------|---------|-------------|------------------|----------------|
| **ACO_ReturnTripOptimizer** | Speculative return matching from historical patterns | Yes | No (probabilistic) | No |
| **ACO_BackhaulOptimizer** | Confirmed return/pickup orders (VRPB) | Yes | Yes (linehaul → backhaul) | No |
| **HybridACO_LightGBM** | ML-enhanced dynamic cost + VRPB | Yes | Yes | Yes (LightGBM edge cost prediction) |

### VRPB Constraint: Linehaul Before Backhaul

In the **Vehicle Routing Problem with Backhauls** variant:
- **Linehaul nodes** (deliveries) must be served FIRST in each route
- **Backhaul nodes** (pickups) served AFTER all linehauls in the route
- Routes end at last node (open VRP) → no forced return to depot
- Extra pheromone deposit on backhaul edges to favor loaded returns

---

## Part 2C: Speed Factor & ETA Prediction

### RDS-Based Speed Degradation

The speed factor adjusts vehicle speed based on **Road Difficulty Score (RDS)**:

```python
speed_factor = 1.0 - min(0.6, RDS_score * 0.6)  # capped at 60% slowdown
effective_speed = base_speed * speed_factor
```

| RDS | Speed Factor | Interpretation | Surcharge |
|-----|--------------|----------------|-----------|
| 0.0 | 1.0 | Full speed (paved highway) | 0% |
| 0.3 | 0.82 | 18% slowdown (typical rural) | +10% |
| 0.5 | 0.70 | 30% slowdown (gravel/unpaved) | +15% |
| 0.8 | 0.52 | 48% slowdown (poor monsoon) | +30% |
| 1.0 | 0.40 | 60% slowdown (near-impassable) | +40% |

### Base Speeds by Vehicle Type

| Vehicle Type | Base Speed (km/h) | Source |
|-------------|-------------------|--------|
| TRUCK | 30 | India highway average |
| MINI_TRUCK | 25 | India urban average |
| VAN | 35 | Mixed road average |
| BIKE | 40 | Urban delivery |

### ETA Calculation Formula

```text
travel_time_hours = distance_km / (base_speed × speed_factor × traffic_factor)
travel_time_minutes = travel_time_hours × 60
total_eta = travel_time_minutes + 5 (loading) + 15% buffer
```

---

## Part 2D: Enhanced LightGBM Feature Set

### Features for Route Cost Prediction (with speed_factor)

| Feature | Type | Description | Source |
|---------|------|-------------|--------|
| `distance` | float | Network distance (km) | PostGIS / MapmyIndia |
| `RDS_score` | float | Road Difficulty Score (0-1) | RoadDifficultyScore model |
| **`speed_factor`** | **float** | **Effective speed multiplier** | **`1.0 - min(0.6, RDS × 0.6)`** |
| `base_speed_kmph` | float | Nominal speed by vehicle type | Vehicle type lookup |
| `effective_speed_kmph` | float | Adjusted speed | `base_speed × speed_factor` |
| `traffic` | float | Congestion severity (0-10) | MapmyIndia / Google Maps API |
| `weather` | float | Rain/wind/temp impact (0-1) | OpenWeather API |
| `ETA_error_hist_p50` | float | Historical median ETA error (min) | OrderCompletion logs |
| `is_backhaul_edge` | bool | Flag if edge leads to pickup | to_node in backhaul_indices |
| `driver_rating` | float | Past reliability (1-5) | DriverProfile |
| `vehicle_age_years` | int | Age of assigned vehicle | Vehicle model |
| `3d_packing_efficiency` | float | Cargo fit score (0-1) | Bin-packing engine |
| `return_trip_probability` | float | Likelihood of return load | NN similarity on historical pairs |
| `customer_type` | int | Encoded customer tier | OMS scoring |

### Target Variable

`actual_route_cost` — composite of:
- Time-based: `actual_minutes`
- Cost-based: `fuel + labor + risk surcharge`
- Hybrid: `time × wage_rate + fuel_cost + RDS_surcharge`

### Why Include speed_factor?

- **Interpretability**: Traceable model behavior ("RDS 0.5 → speed_factor 0.7 → +43% time")
- **Generalization**: Reduces need for LightGBM to re-learn RDS → speed relationship from sparse data
- **Consistency**: ETA logic matches pricing and driver app
- **Efficiency**: Fewer tree splits → faster inference

---

## Part 2E: Road Difficulty Score (RDS) System

### RDS Data Sources

| Source | Method | Coverage | Freshness |
|--------|--------|----------|-----------|
| **Precomputed RDS** | OSM bulk import → PostGIS table | India-wide | Weekly refresh |
| **Overpass API fallback** | Real-time query at unmapped points | Any location | On-demand |
| **Redis cache** | Cache Overpass results for 7 days | Any queried point | 7-day TTL |
| **Sensor/manual** | Surveys + driver feedback | Operational routes | As submitted |

### RDS Auto-Refresh (Celery Nightly Task)

- Fetch top N high-traffic routes from OrderCompletion logs
- Subdivide into ~100m segments
- Re-estimate RDS via Overpass or sensor fallback
- Update RoadDifficultyScore table
- Schedule: Every 24 hours via Celery Beat

### RDS Mapping (OSM Tags → RDS Value)

| OSM Surface | RDS Value | Interpretation |
|-------------|-----------|----------------|
| asphalt, paved, concrete | 0.1 | Smooth highway |
| primary, secondary road | 0.2 | Good regional road |
| tertiary, residential | 0.3 | Moderate local road |
| gravel, dirt, earth | 0.7 | Difficult rural |
| track (unpaved) | 0.85 | Very difficult |
| very_bad/horrible smoothness | 0.9 | Extreme difficulty |

---

## Part 3: OR-Tools + DRL4Route Integration

### 5-Phase Integration Plan

#### Phase 0: Environment Setup
| Step | Action | Test | Debug |
|------|--------|------|-------|
| 1 | Create isolated routing service | `pwd` returns correct path | Permission denied → `chmod 755` |
| 2 | Initialize Python venv | `python --version` → 3.11+ | venv issues → use `pipenv` |
| 3 | Install dependencies | `import ortools` succeeds | OR-Tools install fails on M1/M2 → `--prefer-binary` |
| 4 | Containerize with Docker | `docker build` succeeds | Remove CUDA deps for CPU-only |
| 5 | LangSmith setup | Trace appears in dashboard | Verify env vars at runtime |

**Dependencies:**
```text
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
ortools==9.9.3963
torch==2.2.0
numpy==1.26.0
geopy==2.4.1
python-dotenv==1.0.0
```

#### Phase 1: OR-Tools Baseline (VRPTW)
```python
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

# 1. Build Distance Matrix (Haversine)
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# 2. Setup Routing Model
manager = pywrapcp.RoutingIndexManager(size, vehicle_count, 0)
routing = pywrapcp.RoutingModel(manager)

# 3. Add Constraints
# - Distance (cost)
# - Capacity (vehicle load)
# - Time Windows (delivery slots)

# 4. Solve
search_params = pywrapcp.DefaultRoutingSearchParameters()
search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
search_params.time_limit.FromSeconds(2)

solution = routing.SolveWithParameters(search_params)
```

**Target:** Solve < 2s for ≤50 nodes, respect all constraints

#### Phase 2: DRL4Route-GAE Dynamic Adaptation
```python
import torch

class MockGAEModel(torch.nn.Module):
    def __init__(self, state_dim=10, hidden_dim=64):
        super().__init__()
        self.encoder = torch.nn.Linear(state_dim, hidden_dim)
        self.confidence_head = torch.nn.Linear(hidden_dim, 1)
        self.action_head = torch.nn.Linear(hidden_dim, 3)  # reroute, wait, skip
        
    def forward(self, state_tensor):
        h = torch.relu(self.encoder(state_tensor))
        conf = torch.sigmoid(self.confidence_head(h)).item()
        action = torch.argmax(self.action_head(h)).item()
        return conf, action

# Confidence Gating
if confidence < 0.75:
    return {
        "model_used": "ortools",
        "confidence": confidence,
        "fallback_reason": "low_confidence"
    }
```

#### Phase 3: FastAPI Service Integration
```python
from fastapi import FastAPI

app = FastAPI(title="Zippy TMS Routing Service", version="1.0.0")
ortools_solver = ORToolsSolver()
drl_agent = DRL4RouteAgent()

@app.post("/optimize/static")
def optimize_static(req: OptimizeStaticRequest) -> RouteResponse:
    # OR-Tools deterministic routing
    pass

@app.post("/optimize/dynamic")
def optimize_dynamic(req: OptimizeDynamicRequest) -> RouteResponse:
    # DRL + confidence gating + fallback
    pass
```

**API Contracts:**
```python
class Node(BaseModel):
    id: str
    lat: float
    lng: float
    time_window_start: int  # minutes from 00:00
    time_window_end: int
    demand: float
    service_time_min: int = 15

class RouteResponse(BaseModel):
    order_id: str
    trace_id: str
    model_used: Literal["ortools", "drl4route"]
    route: List[RouteLeg]
    total_distance_km: float
    total_duration_min: float
    confidence: float
    fallback_reason: Optional[str] = None
    solve_time_ms: int
```

#### Phase 4: Testing & Validation
1. **Unit Tests** (pytest)
   - OR-Tools constraint satisfaction (0 violations)
   - DRL env step/reward bounds
   - FastAPI contract validation

2. **Integration Tests**
   - n8n → Routing API → DB write
   - Idempotency replay
   - Fallback path

3. **Shadow Simulation**
   - Replay 10,000 historical trips
   - Compare predicted vs actual ETA
   - Target: `p90_eta_error < 15 min`, `fallback_rate < 10%`

4. **Chaos Testing**
   - Kill MapmyIndia API → use cached matrix
   - Inject GPS dropout → fallback triggers
   - Duplicate event → n8n stops, DB unchanged

#### Phase 5: Production Rollout
| Phase | Traffic | Features | Success Metric |
|-------|---------|----------|----------------|
| **Shadow** | 100% | Logging only | ≥95% alignment with manual |
| **Canary 5%** | Low-value | DRL active | `p90_eta_error ↓ 15%`, 0 Sev-1 |
| **Canary 25%** | Regional | Auto-apply routes | `fallback_rate < 8%` |
| **Full 100%** | All | Full DRL+OR-Tools | Cost/order ↓, ETA ≥98% |

---

## Part 4: Real-Time Streaming ML Architecture

### Event Flow
```
OMS / IMS / TMS (events)
        ↓
Kafka / Redis Streams
        ↓
Stream Processor (Flink/Python)
        ↓
Real-time Feature Store (Redis)
        ↓
ML Inference Service (LightGBM)
        ↓
Pricing Engine
        ↓
Customer Price (instant)
```

### Kafka Topics
| Topic | Events | Frequency |
|-------|--------|-----------|
| `order_events` | Order created, updated, cancelled | High |
| `vehicle_events` | Vehicle available, assigned, completed | High |
| `traffic_events` | Congestion alerts, road closures | Medium |
| `pricing_events` | Price calculated, surge applied | Low |

### Stream Processor
```python
# stream_processor.py
import redis
from collections import defaultdict

r = redis.Redis(host="localhost", port=6379)

# In-memory counters
demand_counter = defaultdict(int)
supply_counter = defaultdict(int)

def process_event(event):
    city = event["city"]
    
    if event["type"] == "order_created":
        demand_counter[city] += 1
    elif event["type"] == "vehicle_available":
        supply_counter[city] += 1
    
    # Compute real-time features
    features = {
        "demand": demand_counter[city],
        "supply": supply_counter[city],
        "timestamp": event["timestamp"]
    }
    
    # Store in Redis (Feature Store)
    r.set(f"features:{city}", json.dumps(features))
```

### Window-Based Features
```python
# Last 5 minutes demand
demand_last_5min = count(events in last 5 min)

# Rolling windows
- 5 min (immediate reaction)
- 15 min (short-term trend)
- 1 hour (pattern recognition)
```

### Real-Time ML Inference
```python
# ml_service.py
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("models/surge_model.pkl")

@app.get("/predict/{city}")
def predict(city: str):
    features = get_city_features(city)  # From Redis
    
    demand = features["demand"]
    supply = max(features["supply"], 1)
    
    input_vector = np.array([[demand, supply, demand / supply]])
    surge = model.predict(input_vector)[0]
    
    return {
        "city": city,
        "surge_multiplier": max(1.0, min(surge, 3.0))
    }
```

### Integration with Pricing Engine
```python
# Inside pricing engine
import requests

def get_surge(city):
    res = requests.get(f"http://ml-service:8000/predict/{city}")
    return res.json()["surge_multiplier"]

final_price *= get_surge(city)
```

---

## Part 5: Production Infrastructure Stack

| Component | Tool | Purpose |
|-------------|------|---------|
| **Streaming** | Kafka / Redis Streams | Event ingestion |
| **Processing** | Python Workers / Apache Flink | Stream processing |
| **Feature Store** | Redis + PostgreSQL | Fast feature access |
| **Model Serving** | FastAPI | Real-time inference |
| **Training** | Celery / Airflow | Scheduled retraining |
| **Monitoring** | Prometheus + Grafana | Metrics & alerts |
| **Storage** | S3 / Supabase | Model artifacts & logs |

### Monitoring & Alerting
```python
# monitor.py
def detect_drift(predictions):
    mean_pred = np.mean(predictions)
    
    if mean_pred > 2.5:
        alert("⚠ Surge too high → possible issue")
    
    if mean_pred < 1.1:
        alert("⚠ Surge too low → revenue loss")
```

**Metrics to Track:**
- `route_optimize_duration_seconds`
- `drl_confidence`
- `fallback_count`
- `eta_error_seconds`
- `surge_multiplier_mean`
- `prediction_drift_score`

---

## Part 6: ML System Integration with Zippy Architecture

### Agent Responsibilities
| Agent | ML Role | Data Contribution |
|-------|---------|-------------------|
| **OMS** | emits order events | demand data |
| **IMS** | emits vehicle availability | supply data |
| **TMS** | emits traffic/RDS | route difficulty |
| **Pricing Engine** | applies final price | customer behavior |
| **ML Service** | predicts surge | real-time inference |

### Data Flow
```
OMS → order_created → Kafka → Stream Processor → Feature Store
IMS → vehicle_available → Kafka → Stream Processor → Feature Store
TMS → traffic_update → Kafka → Stream Processor → Feature Store
                                        ↓
                              ML Service (FastAPI)
                                        ↓
                              Pricing Engine
                                        ↓
                              Final Price to Customer
```

---

## Key Takeaways

1. **LightGBM** for surge prediction (17 features, RMSE optimization)
2. **OR-Tools CP-SAT** for deterministic VRP (constraint satisfaction)
3. **DRL4Route-GAE** for dynamic adaptation (confidence gating)
4. **Kafka/Redis Streams** for real-time event processing
5. **Feature Store** (Redis) for <1ms feature access
6. **Confidence Threshold** 0.75 for DRL fallback to OR-Tools
7. **5-Phase Rollout** Shadow → Canary 5% → Canary 25% → Full
8. **Monitoring** Prometheus metrics + drift detection
9. **Industry Standards** Uber (GNN), Amazon (DRL), UPS (OR-Tools)
10. **Integration** Deterministic → Cache → ML → Human fallback chain

---

## Quick Reference: Code Templates

### Start ML Service
```bash
# Install
pip install lightgbm pandas scikit-learn joblib fastapi uvicorn

# Train
python train_surge_model.py

# Serve
python ml_service.py

# Test
curl http://localhost:8000/predict/Chennai
```

### Start Routing Service
```bash
# Install
pip install ortools torch fastapi uvicorn geopy

# Run
python main.py

# Test Static
curl -X POST http://localhost:8005/optimize/static \
  -H "Idempotency-Key: test-01" \
  -d '{"order_id": "ORD-123", "nodes": [...]}'

# Test Dynamic
curl -X POST http://localhost:8005/optimize/dynamic \
  -H "Idempotency-Key: test-02" \
  -d '{"order_id": "ORD-123", "context": {...}}'
```

---

*Source: Production ML Pipelines + OR-Tools/DRL4Route Integration + Real-time Streaming Architecture*