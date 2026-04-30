---
type: hub
domain: algorithms
status: active
tags:
  - hub
  - algorithm
  - optimization
region:
  - India
created: 2025-01-15
updated: 2025-01-15
---

# Algorithms Hub

Central hub for all algorithmic logic, decision-making frameworks, and optimization strategies.

## Algorithm Child Notes (05_Algorithms/)

### Routing & Navigation
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Route Optimization Logic]] | Calculate optimal routes | Distance, time, traffic, cost |
| [[Unified Routing & Optimization Algorithm]] | Coordinate routing, ETA, and backhaul safely | Idempotency, traceability, VRP, loop metadata |
| [[ETA Prediction Logic]] | Generate explainable ETA windows with confidence | Historical speed, traffic, weather, telematics, residual error |
| [[Return Load Optimization]] | Reduce empty return miles | Corridor demand, wait time, backhaul fit |

### Matching
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Load Matching Algorithm]] | Match shipments to feasible vehicles | Capacity, compatibility, ETA, return probability |
| [[IMS Matching Engine]] | Generate candidate vehicles without mutating state | Hard filters, reservations, fallback path |
| [[Hub-Aware Return Trip Matching]] | Match completed hub-corridor deliveries to return loads | Hub context, spoke adjacency, capacity, saved km |

### Pricing & Commercial
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Distance Based Pricing]] | Calculate shipment costs | Distance, vehicle type, cargo |
| [[Urgency Surcharge Logic]] | Apply time premiums | Urgency level, deadline proximity |
| [[Strategic Profit Sharing Framework]] | Calculate contribution-based partner share and Zippy retained margin | Capacity, revenue, risk, strategic value, margin cap |

### Resource Allocation
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Fleet Allocation Algorithm]] | Assign vehicles to orders | Capacity, location, availability |
| [[Hub-and-Spoke Network Design Algorithm]] | Select hubs, spokes, corridors, and routing topology | Demand clusters, facility candidates, carrier density, SLA, cost |
| [[Vehicle Assignment Logic]] | Select best-fit vehicle for an order | Cargo fit, confidence, fallback path |
| [[Driver Assignment Logic]] | Match drivers to vehicles | Skills, hours, performance |
| [[Multi-Objective Vehicle Scoring]] | Rank candidates across cost and service dimensions | Cost, familiarity, reliability, utilization |
| [[Warehouse Transport Correlation Algorithm]] | Select warehouse-aware distribution and vehicle plan | Warehouse grade, material type, handling fit, lane risk |

### Partner Selection
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Carrier Selection Algorithm]] | Choose transport partners | Price, reliability, coverage |
| [[Carrier Scoring Algorithm]] | Rate partner performance | On-time %, ratings, capacity |

### Financial
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Payment Risk Logic]] | Assess payment risk | Customer history, order value |
| [[Strategic Profit Sharing Framework]] | Automate fair settlement for partnership economics | Rule model, contribution metrics, margin protection, audit hash |

### Risk & Governance
| Algorithm | Purpose | Key Variables |
|-----------|---------|---------------|
| [[Collaboration Risk Scoring Algorithm]] | Decide expand, pilot, maintain, reduce, or exit collaboration | Risk score, opportunity score, balance score |
| [[Partnership Health Score Calculator]] | Convert live partner metrics into expand, maintain, reduce, or exit actions | Operational, financial, compliance, relationship metrics |

## Algorithm Decision Tree

```
                    ┌─────────────────┐
                    │  New Order      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Validate Order │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────────┐    │    ┌─────────▼────────┐
     │ Price Calculation│    │    │ Resource Check   │
     │ - Distance       │    │    │ - Fleet Available│
     │ - Urgency        │    │    │ - Driver Ready   │
     └────────┬────────┘    │    └─────────┬────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │ Carrier Select  │
                    │ - Score Ranking │
                    │ - Risk Check    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Confirm Order  │
                    │ - Assign Fleet  │
                    │ - Assign Driver│
                    └─────────────────┘
```

## Related Hubs
- [[Fleet & Transport Hub]] - Resource algorithms
- [[Business Models Hub]] - Pricing algorithms
- [[Operations Strategy Hub]] - Strategic alignment

---

*Maps to: [[Operations Strategy Hub]] | Part of: [[Logistics Brain - Master Index]]*
