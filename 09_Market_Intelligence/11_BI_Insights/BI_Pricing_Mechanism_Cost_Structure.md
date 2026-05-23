# Pricing Mechanism & Cost Structure

> **Dynamic Pricing Engine for Logistics Operations**

---

## Executive Summary

| Cost Component | Industry Benchmark | Your Target |
|----------------|-------------------|-------------|
| **Platform Fee** | 8-12% (brokers) | **3-5%** (digital) |
| **Cost per Match** | 3-6% | **≤4%** |
| **Empty Mile Reduction** | 20-30% of total cost | **Reduce by 20-30%** |
| **User Savings** | 15-30% | **18-25%** |
| **Idle Vehicle Cost** | ₹1,500-3,000/day | **≤₹800/day** |

---

## Part 1: India Logistics Cost Benchmarks (2026)

### National-Level Metrics
| Metric | Value | Trend |
|--------|-------|-------|
| **Logistics Cost as % of GDP** | 8-9% | ↓ Down from 13-14% |
| **Road Freight Market Size** | ₹1,40,000+ crore | Growing |
| **Digital Platform Savings** | 15-30% vs traditional | Significant |

### Road Freight Rates (FTL - Full Truck Load)
| Truck Type | Rate per km | Rate per tonne-km | Best For |
|------------|-------------|-------------------|----------|
| **Mini / Tata Ace** | ₹10-25 | — | Last-mile / small loads |
| **Medium Trucks** | ₹18-40 | ₹2.5-3.0 | Inter-city standard |
| **Standard FTL (20-30T)** | **₹15-25** | ₹2.5-3.0 | Most common |
| **Large Container / HCV** | ₹35-85 | Higher on long hauls | High-value / bulk |

### Key Cost Drivers (2026)
| Driver | Impact | Trend |
|--------|--------|-------|
| **Diesel Price** | 55-70% of operating cost | Biggest rate driver |
| **Seasonal Spikes** | +15-25% | Festivals, harvest, monsoon |
| **Empty Miles** | 20-30% of total freight cost | Major inefficiency |
| **Idle Vehicles** | ₹1,500-3,000/day | Opportunity cost |

---

## Part 2: Base Cost Formula

### Core Pricing Components
```
┌─────────────────────────────────────────────────────────────────┐
│                    BASE COST CALCULATION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TOTAL_BASE_COST =                                              │
│    Fuel Cost                                                    │
│  + Driver Cost                                                  │
│  + Depreciation                                                 │
│  + Insurance                                                    │
│  + Maintenance                                                  │
│  + Toll                                                         │
│  + Permit & Miscellaneous                                       │
│  + Loading Cost                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Cost Element | Formula | Typical Range |
|--------------|---------|---------------|
| **Fuel Cost** | (Distance / KMPL) × Diesel Price | ₹3-5/km |
| **Toll Cost** | Toll Rate per km × Distance | ₹2-8/km |
| **Driver Cost** | (Annual Salary / 12) × Trip Ratio | ₹2-4/km |
| **Depreciation** | (Annual Depreciation / 12) × Trip Ratio | ₹1.5-3/km |
| **Insurance** | (Annual Premium / 12) × Trip Ratio | ₹0.5-1/km |
| **Permit Fees** | (Annual Permit / 12) × Trip Ratio | ₹0.2-0.5/km |
| **Maintenance** | (Maint per km + Tire cost per km) × Distance | ₹2-4/km |
| **Loading Cost** | Fixed per trip | ₹500-2,000 |

---

## Part 3: Scenario-Based Pricing Layers

### Dynamic Surcharge Matrix

| Scenario | Condition | Surcharge | Application |
|----------|-----------|-----------|-------------|
| **Festival Season** | Diwali, Pongal, etc. | **+20-60%** | High demand periods |
| **Tier 1 City** | Metro/urban | **0.95x** (discount) | Competitive market |
| **Tier 2 City** | Secondary cities | **1.0x** (base) | Standard pricing |
| **Tier 3 City** | Rural/remote | **1.1-1.25x** | Lower volume, higher cost |
| **Remote Area** | Poor infrastructure | **+25-50%** | Difficult access |
| **Hill Station** | Mountain routes | **+35-60%** | Steep gradients, return difficulty |
| **Congestion** | Heavy traffic areas | **+10-25%** | Idle time cost |
| **RDS (Route Difficulty)** | 0-1 score | **1 + (RDS × 0.5)** | Road quality factor |
| **Express Service** | Priority delivery | **1.5x** (50% surge) | Urgent shipments |
| **Standard Service** | Regular delivery | **1.0x** (base) | Normal timeline |

### Seasonal Demand Patterns
```
┌─────────────────────────────────────────────────────────────────┐
│                    SEASONAL PRICING CALENDAR                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  JAN  FEB  MAR  APR  MAY  JUN  JUL  AUG  SEP  OCT  NOV  DEC   │
│   │    │    │    │    │    │    │    │    │    │    │        │
│   │    │    │    │    │    │    │    │    │    │    │        │
│   ▼    │    ▼    │    │    ▼    │    │    ▼    │    ▼        │
│ Harvest│    │Festi│    │    │Monsoon│    │    │Festi│    │Festi│
│ Season │    │val  │    │    │       │    │    │val  │    │val  │
│   +15% │    │+35% │    │    │  +20% │    │    │+25% │    │+40% │
│        │    │     │    │    │       │    │    │     │    │     │
│        │    │     │    │    │       │    │    │     │    │     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Advanced Pricing Adjustments

### Customer Segmentation
| Customer Type | Adjustment | Rationale |
|---------------|------------|-----------|
| **High-Value** | **-5-15%** (discount) | Loyalty reward, volume commitment |
| **Second-Grade** | **0%** (base) | Standard pricing |
| **Least-Value** | **+10%** (surcharge) | Higher service cost, risk mitigation |

> See also: `BI_Autonomous_OMS_Agent_Business_Logic.md` §2 (Customer Tiers)

### Return Trip Logic
| Trip Type | Adjustment | Benefit |
|-----------|------------|---------|
| **One-Way** | Base rate | Standard pricing |
| **Round-Trip** | **-15-25%** | Reduce empty miles, improve utilization |
| **Return Load Available** | **-20-30%** | Maximum efficiency |

### Demand-Supply Dynamic Surge
```
Demand/Supply Ratio = Current Demand ÷ Available Vehicles

Surge Multiplier:
• Ratio 1:1 → 1.0x (normal)
• Ratio 2:1 → 1.2x (+20%)
• Ratio 3:1 → 1.4x (+40%)
• Ratio 4:1+ → 1.6x (+60%, capped)
```

---

## Part 5: Complete Pricing Formula

### Master Pricing Equation
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FINAL PRICE CALCULATION                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SUBTOTAL =                                                             │
│    (BASE_COST × Tier_City_Multiplier × Fuel_Index)                    │
│  + (Festival_Surcharge + Remote_Surcharge + Hill_Surcharge            │
│      + Congestion_Fee + RDS_Adjustment + Demand_Supply_Surge)         │
│                                                                         │
│  ADJUSTED_SUBTOTAL = SUBTOTAL × Service_Type_Multiplier                │
│                                                                         │
│  CUSTOMER_PRICE = ADJUSTED_SUBTOTAL + Customer_Adjustment              │
│                                                                         │
│  FINAL_PRICE =                                                          │
│    CUSTOMER_PRICE                                                       │
│  + Platform_Fee (3-5% Zippy target vs 8-12% brokers)                   │
│  + Insurance (1% of declared value)                                    │
│  + GST: 12% on transport + 18% on platform services                    │
│                                                                         │
│  NOTE: Generic formula shows 10% broker fee. Zippy target is 3-5%.    │
│  See: BI_Autonomous_OMS_Agent_Business_Logic.md §6                     │
│  See: BI_Payment_Compliance_Guide.md §4 (GST split)                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pricing Breakdown Example
```
Base Costs:
├── Fuel: ₹3,200
├── Driver: ₹1,500
├── Depreciation: ₹800
├── Insurance: ₹500
├── Toll: ₹800
├── Maintenance: ₹500
└── Loading: ₹1,000
    Total Base: ₹8,000

Adjustments:
├── Festival Surge (+30%): +₹2,400
├── Remote Area (+25%): +₹2,000
├── Congestion (+15%): +₹1,200
└── Tier 2 City (1.0x): ₹0
    Adjustments: +₹5,600

Service Multiplier:
├── Express (1.5x): +₹6,840

Platform & Taxes:
├── Platform Fee (5%): +₹1,012 (Zippy target: 3-5%, broker: 10%)
├── Insurance (1%): +₹2,000
├── GST Transport (12%): +₹960
└── GST Services (18%): +₹182
═══════════════════════════════════════
FINAL PRICE: ₹25,948 (Zippy) vs ₹32,232 (broker @10%)
SAVINGS: ~19%
═══════════════════════════════════════
```

---

## Part 6: Strategic Cost Management (4 Levers)

### Academic Framework (2021 Research)
| Lever | Definition | Application |
|-------|------------|-------------|
| **1. Organizational Structures** | Build systems to cut waste at every level | Central AI + PostgreSQL as cost-control backbone |
| **2. Implementation Effectiveness** | Execute cost-reduction plans efficiently | Real-time Yes/No buttons, instant templates |
| **3. Decision Making Improvement** | Use timely, accurate data for decisions | AI analysis, weekly rate forecasts, demand heatmaps |
| **4. Comprehensive Cost Information** | Provide full visibility of costs | Broadcast predicted rate + diesel impact + demand pressure |

### Cost Structure Breakdown
| Cost Area | % of Total | Reduction Strategy |
|-----------|------------|-------------------|
| **Transportation / Empty Runs** | 55-70% | Demand heatmap + AI predictive matching → 20-30% reduction |
| **Idle Vehicles / Waiting Time** | 15-25% | Auto-escalation + generic availability status |
| **Platform / Matching Overhead** | 3-6% | Fully automated n8n + PostgreSQL → keep ≤4% |
| **Information & Decision Delays** | Hidden but high | Real-time AI + rate forecasting → eliminate delays |

---

## Part 7: Freight Rate Forecasting System

### Weekly Forecast Workflow
```
┌─────────────────────────────────────────────────────────────────┐
│                 WEEKLY RATE FORECAST PROCESS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SUNDAY NIGHT AUTOMATION (n8n Trigger)                          │
│  ├── Query: Last 90 days matches by pincode-pair               │
│  ├── Fetch: Current diesel price via API                       │
│  ├── Calculate: Demand pressure (this week vs last week)       │
│  └── AI Analysis: GPT-4o rate prediction                         │
│                                                                 │
│  GPT-4o PROMPT:                                                 │
│  "You are a freight rate forecaster for South India road       │
│   transport. Current diesel: ₹XX/litre. Route: Chennai to      │
│   Bangalore (historical avg ₹18/km). Demand: High/Medium/Low.  │
│   Season: Normal/Festival/Harvest/Monsoon.                     │
│   Historical range: ₹15-22/km.                                 │
│   Predict fair market rate per km for next 7 days."            │
│                                                                 │
│  OUTPUT:                                                        │
│  {"predicted_rate": 19.5,                                       │
│   "low": 17.0,                                                 │
│   "high": 22.0,                                                │
│   "reason": "Diesel up 4%, festival demand surge"}             │
│                                                                 │
│  BROADCAST:                                                     │
│  "Chennai→Bangalore forecast: ₹17-22/km (diesel ↑4%, demand ↑)"│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Forecasting Drivers
| Driver | Impact | Data Source |
|--------|--------|-------------|
| **Diesel Price** | Very High | Weekly API fetch |
| **Demand (Pincode)** | High | Your heatmap queries |
| **Seasonality** | High | Calendar flags in DB |
| **Capacity (Owners Online)** | High | % of vehicles available |
| **Empty Return Runs** | Medium | One-way vs round-trip tracking |

---

## Part 8: KPIs & Performance Tracking

### Cost Management KPIs
| KPI | Formula | Target | Tracking |
|-----|---------|--------|----------|
| **Cost per Successful Match** | Total ops cost ÷ matched shipments | ≤4% | n8n cost tracking |
| **Platform Fee Efficiency** | Platform revenue ÷ shipment value | 3-5% | Monthly review |
| **Empty Mile Reduction** | Empty km ÷ Total km | Reduce 20-30% | GPS + AI matching |
| **Idle Vehicle Cost** | Daily cost × idle days | ≤₹800/day | DB monitoring |
| **User Savings Delivered** | (Broker cost - Your cost) ÷ Broker cost | 18-25% | Post-match survey |

### Pricing Accuracy Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Forecast Accuracy** | ≥80% | Predicted vs actual rate |
| **Price Acceptance Rate** | ≥90% | Customers accepting AI rate |
| **Dispute Rate** | <2% | Price-related complaints |
| **Margin Consistency** | ±1% | Platform fee stability |

---

## Part 9: Implementation Roadmap

### Week 1-2: Foundation
- [ ] Add cost-tracking fields to DB: `match_value`, `platform_fee`, `idle_days`
- [ ] Implement base cost calculator
- [ ] Set up diesel price API feed
- [ ] Create tier city mapping table

### Week 3-4: Scenario Engine
- [ ] Build surcharge matrix (festival, remote, hill)
- [ ] Implement RDS scoring integration
- [ ] Add congestion fee logic (Map API)
- [ ] Create customer segmentation rules

### Month 2: Forecasting
- [ ] Deploy weekly n8n forecast workflow
- [ ] Integrate GPT-4o rate prediction
- [ ] Build `rate_forecasts` table
- [ ] Set up group broadcast system

### Month 3: Optimization
- [ ] Implement demand-supply surge pricing
- [ ] Add return trip discount logic
- [ ] Create pricing dashboard
- [ ] A/B test pricing strategies

---

## Part 10: Integration with Other Systems

### OMS ↔ Pricing Engine
| OMS Phase | Pricing Input | Output |
|-----------|---------------|--------|
| Order Validation | Pincode-pair | Serviceability + base rate range |
| Order Processing | Vehicle type, distance | Estimated cost |
| Dispatch | Real-time demand | Final dynamic price |
| Delivery | Actual route, delays | Cost reconciliation |

### TMS ↔ Pricing Engine
| TMS Function | Pricing Role |
|--------------|--------------|
| Route Optimization | RDS score calculation |
| Carrier Selection | Cost per km comparison |
| Load Consolidation | Shared cost distribution |
| Freight Audit | Price verification |

### AI Agent ↔ Pricing Engine
```
AI Agent Flow:
1. Receive customer requirement
2. Query Pricing Engine for base cost
3. Check current demand/supply
4. Apply scenario surcharges
5. Generate rate forecast
6. Send to customer with Yes/No buttons
7. Track acceptance in DB
8. Learn from acceptance patterns
```

---

## Key Takeaways

1. **Base Cost Foundation** - Fuel + Driver + Depreciation + Insurance + Toll + Maintenance
2. **Tier City Multipliers** - Tier 1: 0.95x, Tier 2: 1.0x, Tier 3: 1.1-1.25x
3. **Scenario Surcharges** - Festival (+20-60%), Remote (+25-50%), Hill (+35-60%)
4. **Express Premium** - 1.5x multiplier for priority service
5. **Return Trip Discount** - 15-25% for round-trip efficiency
6. **Dynamic Surge** - Based on demand/supply ratio (capped at 2x)
7. **Strategic Cost Management** - 4 levers drive 18-25% user savings
8. **Weekly Forecasting** - AI-powered rate prediction via GPT-4o
9. **Platform Fee Target** - 3-5% (vs 8-12% traditional brokers)
10. **Cost Transparency** - Show full breakdown to build trust

---

## Quick Reference: Pricing Rules

### One-Line Rules for AI Agent

> **"Base cost is truth — fuel, driver, depreciation never lie."**

> **"Festival surge up to 60% — demand wins over cost."**

> **"Return trip discount 15-25% — empty miles kill profit."**

> **"Tier 3 cities 1.25x — infrastructure costs more."**

> **"Express service 1.5x — time is money."**

> **"Every unmatched vehicle after 48 hours triggers demand alert — idle time is the #1 cost killer."**

---

*Source: India Logistics Cost Benchmarks 2026 + Freight Rate Forecasting Guide + Strategic Cost Management Research + Production Pricing Engine*