---
type: concept
domain: india-logistics
decision_value: high
status: draft
region: India
related_hubs:
  - Indian Logistics Ecosystem Hub
  - Market Intelligence Hub
  - Operations Strategy Hub
  - Technology Stack Hub
tags:
  - concept
  - india-logistics
  - national-logistics-policy
  - ulip
  - multimodal
  - mmlp
  - gati-shakti
---

# National Logistics Master Plan

## Purpose

Use this note as the national-level strategy layer above the state logistics policy notes. It connects the National Logistics Policy direction with Zippy's warehouse-first, TMS, multimodal, fleet, EV, and control-tower product strategy.

Derived from [[National Logistics Policy RSM 2024 Source]].

## Core Thesis

India's logistics modernization is not one policy or one infrastructure project. It is a national operating-system shift:

```text
lower logistics cost
+ national infrastructure buildout
+ multimodal nodes
+ digital integration through ULIP/IDS
+ standardization
+ EV and green logistics
+ state policy execution
= logistics as a coordinated national network
```

For Zippy, this means the product should not remain a spot truck-booking app. It should become a node-aware logistics operating layer that understands warehouses, ports, ICDs, CFSs, MMLPs, railway terminals, inland waterways, EV routes, and state-specific incentives.

## NLP Targets To Encode

| Target | Platform Meaning |
|--------|------------------|
| Reduce logistics cost to global-benchmark levels by 2030 | Build cost visibility, mode comparison, vehicle utilization, detention control, and return-load optimization |
| Top-25 Logistics Performance Index ambition by 2030 | Improve reliability, timeliness, visibility, customs/document readiness, and service quality |
| Data-driven decision support | Build lane intelligence, customer/warehouse scorecards, carrier scoring, ETA confidence, and exception analytics |

## National Infrastructure Layers

| Layer | Role In Logistics Network | Zippy Product Implication |
|-------|---------------------------|---------------------------|
| Roads and Bharatmala | First-mile, last-mile, expressway freight, flexible domestic movement | Truck routing, toll/fuel/time costing, detention and rest-stop intelligence |
| Ports | International gateway and coastal shipping nodes | Gate-slot, demurrage, DPE, document readiness, port-linked carrier workflows |
| ICD/CFS/AFS | Inland customs, container handling, air freight handoff | Customs-aware workflow, container tracking, bonded movement, EXIM document control |
| MMLP | Multimodal transfer, storage, consolidation, value-added services | Handoff SLA, dwell tracking, mode-chain planning, consolidation engine |
| Rail terminals and DFCs | Long-haul bulk/container freight and road-to-rail shift | Intermodal recommendation, rail feasibility, terminal pickup/delivery execution |
| Inland waterways | Bulk, ODC, lower-cost alternative lanes where available | Waterway candidate detection and terminal-linked planning |
| Commercial EVs | Urban/regional low-emission freight with TCO advantage on right routes | EV route-fit scoring, charging-aware dispatch, battery/vehicle-as-a-service hooks |
| ULIP/IDS | Digital integration across logistics systems | Unified status, data enrichment, document checks, visibility APIs |

## Product Architecture Implication

```text
OMS demand
-> warehouse readiness
-> vehicle/body/MHE fit
-> mode selection
-> road/rail/port/ICD/CFS/MMLP/waterway node choice
-> carrier and driver assignment
-> document and compliance readiness
-> ETA and cost prediction
-> execution tracking
-> POD and settlement
-> exception learning
```

This connects directly to [[Warehouse Transport Correlation Algorithm]], [[Intermodal Transport Framework]], and [[Transport Control Tower KPI Framework]].

## Master Plan To State Policy Flow

```text
National Logistics Policy / PM GatiShakti / ULIP
-> state logistics policies
-> logistics parks, MMLPs, ICDs, CFSs, truck terminals, cold chains
-> warehouse and industrial cluster demand
-> vehicle supply and carrier networks
-> Zippy operating wedge
```

Use [[Indian State Logistics Policy Comparison]] to translate national intent into state-specific GTM sequencing.

## Decision Model For Mode And Node Selection

```text
recommend_mode_chain(order):
  evaluate direct_road
  evaluate road_to_rail
  evaluate road_to_port_or_coastal
  evaluate road_to_icd_cfs
  evaluate road_to_mmlp
  evaluate road_to_waterway
  evaluate air_for_high_value_urgent

  reject mode chains where:
    node access is weak
    documents are not ready
    tracking continuity is poor
    terminal dwell risk exceeds savings
    shipment volume/distance does not justify handoff

  choose mode chain that minimizes:
    total landed cost
    service failure risk
    detention/demurrage risk
    empty running
    carbon where commercially relevant
```

## Zippy Product Modules From National Plan

| Module | Why It Exists |
|--------|---------------|
| Lane intelligence engine | National infrastructure changes lane economics over time |
| Node registry | Ports, ICDs, CFSs, MMLPs, rail terminals, waterways, truck terminals must be first-class entities |
| Mode comparison engine | Road-only matching misses rail, waterway, port, and ICD/CFS savings |
| ULIP/IDS integration layer | National digital systems can reduce manual document/status chasing |
| Warehouse standard readiness | Standardized physical assets and processes start at warehouse/dock level |
| EXIM workflow module | Ports, ICDs, CFSs, AFSs, FTWZs require document-aware execution |
| EV route-fit engine | EV works where TCO, charging, route length, payload, and duty cycle fit |
| MMLP/cross-dock planner | MMLPs become consolidation and handoff nodes |
| Detention/demurrage control | Unplanned costs are a major savings lever |
| State policy intelligence | Incentives and infrastructure differ sharply by state |

## Startup GTM Implication

The national plan favors customers who feel the pain of coordination across nodes:

- Grade A/B warehouses near industrial corridors
- 3PLs operating in logistics parks
- exporters/importers using ports, ICDs, CFSs, or AFSs
- pharma, electronics, textile, agri, seafood, and high-value manufacturers
- transporters that need digital compliance and visibility
- cold-chain and reefer operators
- city freight operators affected by congestion and restrictions

## Related Notes

- [[National Logistics Policy RSM 2024 Source]]
- [[Indian State Logistics Policy Comparison]]
- [[India Freight 2050 Strategic Roadmap]]
- [[Intermodal Transport Framework]]
- [[Transport Mode Selection Framework]]
- [[Lane Intelligence Model]]
- [[Warehouse Customer Strategy Canvas]]
- [[Government Warehousing Standards Compliance Layer]]
- [[Warehouse Transport Correlation Algorithm]]
- [[Transport Control Tower KPI Framework]]
- [[Digital Freight Marketplace]]

