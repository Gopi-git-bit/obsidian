# Logistics Intelligence: Master Index

> **Complete Knowledge Base Navigation**

---

## 📊 Quick Statistics Dashboard

| Category | Key Metric | Value |
|----------|-----------|-------|
| **Last-Mile Cost** | % of Total Shipping | 53% |
| **TMS ROI** | Cost Savings | 10-20% |
| **DRL4Route AI** | Transport Efficiency | +25% |
| **Location Accuracy** | Improvement | +2.4-3.2% |
| **India Logistics Cost** | % of GDP | 8-9% |
| **Hub-Spoke Reduction** | Logistics Cost | 15-20% |
| **Platform Fee** | vs Traditional Brokers | 3-5% |
| **User Savings** | vs Market Rate | 18-25% |
| **FTL Rate** | per km (Standard) | ₹15-25 |
| **Diesel Cost Share** | of Operating Cost | 55-70% |

---

## 1. Core TMS Knowledge (Consolidated)

### Primary Files (Unique Content)
| File | Topic | Lines |
|------|-------|-------|
| `BI_TMS_Implementation_Consolidated.md` | 7-Stage Lifecycle + PID + Architecture | ~300 |
| `BI_TMS_Operational_Logic.md` | Master Data, Transactional, KPIs | 77 |
| `BI_TMS_India_Transport_Stats.md` | India Modal Stats | 62 |
| `BI_Sustainable_TMS_Operations_5G_Edge.md` | Descartes + 5G/Edge | 97 |
| `BI_Transportation_Process_Decomposition.md` | 6-Step Framework | 175 |

**Total TMS:** ~711 lines (vs 727 duplicate lines before)

---

## 2. AI & Optimization (DRL4Route)

### Primary File (Consolidated)
| File | Topic | Lines |
|------|-------|-------|
| `BI_DRL4Route_Complete_Guide.md` | Architecture + Execution + TOE Integration | ~200 |

**Total AI:** ~200 lines (vs 388 duplicate lines before)

---

## 3. Order Management System (OMS)

### Primary Files
| File | Topic | Lines |
|------|-------|-------|
| `BI_Order_Management_System_Lifecycle.md` | CODP Strategies + SOPs + Tech Stack | ~400 |
| `BI_Autonomous_OMS_Agent_Business_Logic.md` | Customer tiers, vehicle assignment cascades, IMS matching algorithm (4-phase), order state machine, cancel/reschedule, delivery/POD/settlement, GPS tracking, graceful degradation, deterministic rules, decision engine, cache strategy | ~700 |
| `BI_Agent_System_Architecture.md` | 5-Agent system, communication model, SLAs, policies, admin playbook, Celery integration, simulation framework, monitoring, chaos testing, circuit breakers, SLOs, incident runbooks, GLM-4.6 targets | ~800 |

**Key Insights:**
- **CODP Strategies:** MTS, MTO, ATO, ETO
- **Priority Logic:** High-value → second-grade → least-value order servicing
- **Vehicle Matching Rules:** body type → dimensions → model → tonnage → ETA fallback
- **IMS Matching Algorithm:** Phase 1 (pre-filter) → Phase 2 (ML scoring: ETA 40%, reliability 25%, eco 15%, return-trip 10%, 3D packing 10%) → Phase 3 (stable matching) → Phase 4 (cascade fallbacks)
- **Express vs Standard:** newer fleet + tighter score thresholds for premium fulfillment
- **Order State Machine:** 11 canonical states with enforced transitions (draft → confirmed → driver_assigned → enroute → delivered → pod → settlement → completed)
- **Cancel/Reschedule:** Cancel allowed from draft/confirmed/driver_assigned; reschedule only before enroute
- **Driver Assignment:** Accept/reject/timeout cascade (10 min window); 5km → 10km → TC → WhatsApp RAG → exhaust
- **Delivery Flow:** Driver arrival → loading → unloading → shipment delivered (OTP-gated) → POD upload → settlement
- **GPS Tracking:** Allowed only during enroute; signal loss detection (5 min threshold); route deviation detection
- **Decision Engine:** Deterministic guardrails → Rule engine → Cached cases DB → ML model → Fallback. No model can override rules.
- **Cache Strategy:** L1 Redis (real-time state), L2 PostgreSQL (persistent), L3 TimescaleDB (time-series), L4 S3 (cold archive)
- **Circuit Breakers:** MapmyIndia, Razorpay, Twilio with timeout/error threshold/reset timeout configuration
- **SLOs:** Assignment p99 < 30s, ETA p90 < 15min, Payment > 99.5%, API uptime 99.9%
- **Incident Runbooks:** Payment gateway down, No-match surge, DB replication lag, SMS delivery failure
- **GLM-4.6 Targets:** Confidence > 92%, Self-healing > 95%, Human interventions < 2/1000
- **Graceful Degradation:** 4 levels (normal → degraded → limited → emergency) based on fallback rate and AI health
- **Simulation:** Decision simulator validates AI against historical data; retrains if metrics degrade
- **Monitoring:** Decision auditing, anomaly detection, Prometheus metrics, Slack/PagerDuty alerting
- **Agent Architecture:** Supervisor + Operations + Transport + Finance + RAG
- **Communication:** Redis Streams / Kafka with idempotency + DLQ
- **Policies:** 8 Supervisor policies (advance, settlement, blacklist, hazardous, RDS, DLQ)
- **SLAs:** Driver accept 10 min, reservation TTL 300s, express assignment ≤2 min
- **6 SOPs:** Order processing → Picking → Dispatch → Delivery → Returns → Billing
- **KPIs:** Processing ≤2 min, Picking ≤5 min, Dispatch ≤2 hours, Express assignment ≤2 min

---

## 4. Last-Mile Delivery

### Primary File (Consolidated)
| File | Topic | Lines |
|------|-------|-------|
| `BI_Last_Mile_Complete_Analysis.md` | Amazon/Flipkart/Delhivery/DHL + TMS Integration | ~150 |

**Total Last-Mile:** ~150 lines (vs 185 duplicate lines before)

---

## 5. Pricing Mechanism & Cost Structure

### Primary File
| File | Topic | Lines |
|------|-------|-------|
| `BI_Pricing_Mechanism_Cost_Structure.md` | Dynamic Pricing + Cost Benchmarks + Forecasting | ~500 |

**Key Insights:**
- **India Cost Benchmarks:** Logistics 8-9% GDP, FTL ₹15-25/km, Diesel 55-70% operating cost
- **Pricing Formula:** Base cost + Scenario surcharges + Service multipliers + Platform fee + GST
- **Scenario Surcharges:** Festival (+20-60%), Remote (+25-50%), Hill (+35-60%), Congestion (+10-25%)
- **Tier Multipliers:** Tier 1 (0.95x), Tier 2 (1.0x), Tier 3 (1.1-1.25x)
- **Strategic Cost Management:** 4 levers → 18-25% user savings
- **Weekly Forecasting:** GPT-4o AI-powered rate prediction

---

## 6. Technology Stack & ML Systems

### Primary File
| File | Topic | Lines |
|------|-------|-------|
| `BI_Tech_Stack_ML_Systems.md` | LightGBM + OR-Tools + ACO + RDS + Speed Factor + Streaming | ~700 |

**Key Insights:**
- **ML Prediction:** LightGBM/XGBoost for surge pricing (17 features, RMSE optimization)
- **Route Optimization:** OR-Tools CP-SAT (deterministic) + ACO variants (return trip, backhaul, hybrid) + DRL4Route-GAE
- **Speed Factor:** `1 - RDS × 0.6` (capped at 60% slowdown) for ETA prediction
- **Enhanced Features:** 14 LightGBM features including speed_factor, effective_speed, return_trip_probability, 3d_packing_efficiency
- **RDS System:** OSM bulk import + Overpass API fallback + Redis cache + nightly auto-refresh
- **ACO Variants:** ReturnTripOptimizer (speculative), BackhaulOptimizer (VRPB confirmed), HybridACO_LightGBM (ML-enhanced)
- **Streaming:** Kafka/Redis Streams for real-time event processing
- **Feature Store:** Redis (<1ms access) + PostgreSQL (historical)
- **5-Phase Rollout:** Shadow → Canary 5% → Canary 25% → Full production

---

## 7. Frontend & Mobile Architecture

### Web Frontend
| File | Topic | Lines |
|------|-------|-------|
| `BI_Frontend_React_Architecture.md` | React 18 + TypeScript + Tailwind CSS | ~600 |

**Key Components:**
- **Framework:** React 18.2+ with TypeScript 5.0+
- **Styling:** Tailwind CSS 3.4+, Headless UI
- **State:** Zustand + TanStack Query
- **Real-time:** Socket.io for tracking + job matching
- **Maps:** Mapbox GL JS / Google Maps
- **Screens:** Customer Dashboard, Booking Flow, Live Tracking, Admin Panel

### Mobile Applications
| File | Topic | Lines |
|------|-------|-------|
| `BI_Mobile_App_Specs.md` | React Native - Driver & Customer Apps | ~800 |

**Key Features:**
- **Driver App:** Job matching (5-min accept), earnings tracking, status updates, navigation
- **Customer App:** Post requirement, live tracking, price estimator, payment
- **Framework:** React Native 0.73+ (Expo SDK 50+)
- **Notifications:** Firebase Cloud Messaging (FCM)
- **Location:** Background tracking for drivers

---

## 8. Payment & Compliance

### Primary File
| File | Topic | Lines |
|------|-------|-------|
| `BI_Payment_Compliance_Guide.md` | Razorpay + GST + E-Way Bill + Insurance | ~500 |

**Key Components:**
- **Payments:** Razorpay (Primary) - UPI, Cards, Net Banking, Wallets
- **GST:** 12% transport + 18% services, HSN codes, invoice generation
- **E-Way Bill:** NIC API integration (₹50,000+ threshold)
- **Insurance:** Transit insurance (1% of value), claim processing
- **KYC:** Driver document verification (DL, RC, Insurance, PAN)

---

## 9. Vehicle Models Database

### Primary File
| File | Topic | Lines |
|------|-------|-------|
| `BI_Vehicle_Models_Database.md` | 26 Commercial Vehicle Specs + SQL Schema | ~1,200 |

**Key Insights:**
- **Manufacturers:** Ashok Leyland (7), Tata Motors (7), Eicher (4), Mahindra (8)
- **Categories:** LCV, ICV, HCV, Tipper with complete specifications
- **Specifications:** GVW, payload, dimensions, engine, price, mileage
- **Usage:** Cargo matching by weight/volume, vehicle recommendations
- **Database:** PostgreSQL table with 26 vehicle records

---

## 10. Strategic Planning

### Files (Unique Content)
| File | Topic | Lines |
|------|-------|-------|
| `BI_Innovative_TMS_Models.md` | AI, IoT, Blockchain, Hub-Spoke Models | 92 |
| `BI_Operational_Planning_Strategies.md` | Mode Selection, Regional Scenarios | 99 |
| `BI_Hub_Spoke_RDC_GST_Impact.md` | GST Impact on Network Design | 117 |
| `BI_Strategic_Operations_Management_Framework.md` | CODP, VUCA Risk, TMS+AI Enablers | ~200 |
| `BI_Gati_Shakti_National_Master_Plan.md` | ₹100L Cr Platform, GCTs, ULIP, Mode Shift, Land Barriers | ~295 |
| `BI_EWay_Bill_Automation_Guide.md` | e-Way Bill Auto, Part A/B, Validity, GR/LR, NIC API | ~350 |
| `BI_Third_Party_Logistics_3PL.md` | 3PL/4PL/5PL, Ecosystem, Asset-Light, Advantages/Disadvantages, Control Towers | ~750 |

**Key Insights (Strategic Ops Framework):**
- **CODP Positioning:** MTS/ATO/MTO/ETO strategies mapped to Zippy's matching engine
- **6-Step Transportation Decomposition:** Mapped to Zippy API endpoints (Orders → Match → Bid → Transit)
- **VUCA Risk Mitigation:** COVID, Suez, Ukraine — crisis KPIs (δ², Δt, empty mile ratio)
- **TMS ROI:** 13-15% cost reduction (developed markets), 15-20% target for India
- **RBV Analysis:** Zippy's competitive moat (≤4hr matching, 3-5% fee, 18-25% savings)

---

## 8. Database Tables (Extracted from Reports)

### BI Insights Database
| Table | Count | Description |
|-------|-------|-------------|
| `bi_insights` | **245** | All insights extracted from 13 report files |
| `bi_metrics` | **93** | Key logistics metrics (TMS + OMS + Pricing + KPIs) |
| `vehicle_models` | **26** | Commercial vehicle specifications (LCV/ICV/HCV/Tipper) |

### Insights by Category
| Category | Count |
|----------|-------|
| supply_chain | 30 |
| market_analysis | 30 |
| transportation | 30 |
| fuel_prices | 30 |
| rail_transport | 30 |
| freight_rates | 30 |
| general | 30 |
| road_transport | 15 |
| trade_compliance | 6 |
| warehousing | 4 |
| container_shipping | 4 |
| vehicle_models | 3 |
| port_operations | 3 |

### Key Metrics Extracted
| Metric | Value | Category |
|--------|-------|----------|
| Last-Mile Cost Share | 53% | last_mile |
| TMS Cost Savings | 10-20% | tms |
| DRL4Route Transport Efficiency | +25% | ai_ml |
| DRL4Route Location Accuracy | +2.4-3.2% | ai_ml |
| India Logistics Cost (%GDP) | 8-9% | india |
| Road Modal Share | 68% | india |
| Hub-Spoke Logistics Reduction | 15-20% | network |
| Empty Running Rate (India) | 28-43% | india |
| **Order Processing Time** | **≤ 2 minutes** | **oms** |
| **Pick Accuracy** | **≥ 99.5%** | **oms** |
| **On-Time Dispatch** | **≥ 98%** | **oms** |
| **Platform Fee** | **3-5%** | **pricing** |
| **FTL Rate per km** | **₹15-25** | **pricing** |
| **Diesel Cost Share** | **55-70%** | **pricing** |
| **Festival Surcharge** | **+20-60%** | **pricing** |
| **User Savings** | **18-25%** | **pricing** |

---

## 6. Tactical Data

### Files (Stats Already Extracted)
| File | Topic | Lines |
|------|-------|-------|
| `BI_Modal_Split_Analysis.md` | Rail/Road/Air/Water Modal Share | 271 |
| `BI_Growth_Projections_2025-2030.md` | Growth Forecasts | 243 |
| `BI_Government_Schemes_Opportunities.md` | NLP, DFC, Schemes | 196 |
| `BI_Infrastructure_Bottlenecks.md` | Bottleneck Analysis | 147 |
| `BI_Route_Cost_Analysis.md` | Cost Benchmarks | 120 |
| `BI_Key_Trading_City_Pairs.md` | City Pair Volumes | 106 |

---

## 📋 Consolidation Status

| Original Files | Duplicates | After Consolidation | New Files | Total |
|----------------|------------|---------------------|-----------|-------|
| ~55 files | ~2000 lines | 34 unique files | +3 Frontend/Mobile/Compliance +1 Vehicle Models +1 Strategic Ops Framework +1 Gati Shakti +1 E-Way Bill Auto +1 3PL/4PL/5PL +1 Autonomous OMS Logic +1 Agent System Architecture | **34 files** |

**Total Knowledge Base:**
- **34 consolidated files** (from ~55 original)
- **~9,150+ lines** of logistics intelligence
- **4,038 database records** (insights + metrics + vehicle_models + raw data)
- **Complete coverage:** TMS + OMS + **Autonomous OMS Logic** + **Agent Architecture** + **Pricing** + **Tech Stack** + AI/ML + Last-Mile + **Frontend** + **Mobile** + **Compliance** + **Vehicle Models** + Strategy + **Gati Shakti** + **E-Way Bill Auto** + **3PL**

---

## Cross-Reference Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOGISTICS KNOWLEDGE BASE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  TMS Core   │────▶│  Last-Mile  │────▶│  AI/ML      │       │
│  │  Systems    │     │  Delivery   │     │  DRL4Route  │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              AI/ML & Tech Stack                      │      │
│  │  • LightGBM/XGBoost  • OR-Tools + DRL4Route         │      │
│  │  • Kafka/Redis Streams • Feature Store (Redis)      │      │
│  │  • Real-time ML Inference • 5G/Edge Computing       │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Frontend & Mobile                       │      │
│  │  • React 18 + TypeScript • Tailwind CSS              │      │
│  │  • React Native Driver App • React Native Customer   │      │
│  │  • Real-time WebSocket • Map Integration             │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Pricing & Cost Management               │      │
│  │  • Dynamic Pricing    • Cost Benchmarks             │      │
│  │  • Freight Forecasting • Strategic Cost Mgmt        │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Payment & Compliance                    │      │
│  │  • Razorpay Integration  • GST Invoicing            │      │
│  │  • E-Way Bill System   • Insurance Integration      │      │
│  │  • KYC Verification    • Driver Document Checks     │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Vehicle Models Database                 │      │
│  │  • 26 Commercial Vehicles  • LCV/ICV/HCV/Tipper   │      │
│  │  • Full Specifications     • Cargo Matching         │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Strategic Planning                       │      │
│  │  • Hub-Spoke Model    • GST Impact                   │      │
│  │  • Regional Scenarios • Innovative Models            │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Tactical Data                           │      │
│  │  • Modal Split    • Growth Projections              │      │
│  │  • Government Schemes • Infrastructure              │      │
│  └─────────────────────────────────────────────────────┘      │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Database (Raw Reports)                  │      │
│  │  • Freight Rates   • Fuel Prices                     │      │
│  │  • Market Analysis • Transport Data                  │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Metrics Quick Reference

### Cost & Efficiency
| Metric | Value | Source |
|--------|-------|--------|
| Last-Mile Shipping Cost | 53% | Last-Mile Analysis |
| TMS Cost Reduction | 10-20% | TMS Implementation |
| Hub-Spoke Reduction | 15-20% | Hub-Spoke Impact |
| DRL4Route Efficiency | +25% | AI/ML Guide |
| Empty Running (India) | 28-43% | India Transport Stats |

### India Logistics
| Metric | Value | Source |
|--------|-------|--------|
| Logistics Cost (GDP) | 8-9% | Growth Projections |
| Road Modal Share | 68% | Modal Split |
| Rail Modal Share | 30-32% | Modal Split |
| Organized Sector | 5-6% | India Stats |

### AI/Technology
| Metric | Value | Source |
|--------|-------|--------|
| Location Accuracy Improvement | +2.4-3.2% | DRL4Route |
| Location Bias Reduction | 0.9-2.7% | DRL4Route |
| 5G IoT Expansion | Massive | 5G-Edge |
| Edge Computing Latency | Near-zero | 5G-Edge |

---

*Last Updated: April 13, 2026 | 34 consolidated files | Deterministic rules, decision engine, cache strategy, circuit breakers, SLOs, incident runbooks, GLM-4.6 autonomy targets*