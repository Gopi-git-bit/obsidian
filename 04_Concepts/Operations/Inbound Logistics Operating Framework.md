---
type: concept
domain: operations
decision_value: high
status: draft
related_hubs:
  - Operations Strategy Hub
  - Fleet & Transport Hub
  - Technology Stack Hub
tags:
  - concept
  - inbound-logistics
  - supplier-collaboration
  - warehouse
  - tms
---

# Inbound Logistics Operating Framework

## Purpose

Define how Zippy should handle inbound logistics: supplier pickup, raw-material movement, vendor collaboration, receiving readiness, warehouse dock planning, and quality-controlled handoff into inventory.

Derived from [[Inbound Logistics Effectiveness Source]].

## Core Thesis

Inbound logistics is the first half of customer service.

If supplier pickup is late, packaging is weak, documents are missing, or the receiving dock is unready, outbound delivery and customer promises fail later.

```text
supplier readiness
-> pickup planning
-> vehicle fit
-> route execution
-> receiving dock slot
-> quality check
-> putaway / quarantine / cross-dock
-> inventory truth
```

## Inbound Flow

| Stage | Owner | Platform Control |
|-------|-------|------------------|
| Supplier shipment-ready signal | Supplier / customer | ASN, pickup request, expected quantity, packaging state |
| Pickup planning | OMS + TMS | pickup window, vehicle class, contract vs spot sourcing |
| Vehicle allocation | IMS / allocation | capacity, body type, MHE fit, supplier loading constraints |
| Supplier pickup | Driver / transporter | pickup photos, supplier signature, document capture |
| In-transit monitoring | TMS | ETA, route deviation, delay alerts, cargo condition if needed |
| Warehouse gate-in | Warehouse / guard / TMS | vehicle arrival, queue, dock assignment |
| Receiving inspection | Warehouse | count, damage, discrepancy, quality status |
| Inventory decision | WMS / IMS | accept, quarantine, cross-dock, return, shortage claim |
| Settlement | Billing | contract rate, spot rate, credit terms, OTIF bonus/penalty |

## Hybrid Fleet Sourcing

Inbound logistics should support multiple sourcing modes.

| Fleet Mode | Best Use | Risk |
|------------|----------|------|
| Contract | repeat supplier lanes, predictable volume, quality-sensitive cargo | inflexible if volume changes |
| Spot | urgent, volatile, one-off inbound movement | price volatility and trust risk |
| Hybrid | regular lanes with surge buffer | requires clear allocation rules |
| Owned / dedicated | high-SLA, high-value, cold-chain, plant-critical movement | fixed cost and utilization pressure |
| 3PL / transport company | scalable regional or long-haul inbound | SLA governance needed |
| gig / local pickup | small urban inbound or document/sample movement | lower control and capacity limits |

## Supplier Collaboration Layer

Supplier collaboration should not be a chat thread only. It should be a structured workflow.

```text
supplier_collaboration
- supplier_id
- pickup_contact
- shipment_ready_time
- loading_method
- packaging_status
- document_status
- agreed_pickup_window
- supplier_feedback_score
- recurring_lane_flag
- co_planning_permission
```

Permissions can include:

- view tracking
- view documents
- provide pickup feedback
- co-plan pickup windows
- confirm loading readiness

## Inbound Quality Controls

| Check | Why It Matters |
|-------|----------------|
| supplier pickup photo | proves cargo condition before transport |
| packaging verification | reduces damage disputes |
| supplier signature | confirms handoff and quantity |
| document capture | prevents receiving and compliance delay |
| vehicle body fit | protects cargo condition |
| loading method fit | avoids detention and unsafe loading |
| receiving dock slot | prevents gate congestion |
| discrepancy reason code | improves supplier and carrier scoring |

## KPI Framework

| KPI | Decision Use |
|-----|--------------|
| supplier pickup on-time rate | supplier and carrier reliability |
| supplier loading turnaround time | detention pricing and dock planning |
| inbound damage rate | packaging, carrier, and handling risk |
| receiving discrepancy rate | supplier quality and documentation risk |
| ASN accuracy | planning confidence |
| dock-to-stock time | warehouse productivity |
| inbound transport cost per unit | lane pricing and sourcing decision |
| contract vs spot cost variance | procurement and allocation strategy |
| OTIF inbound | supplier/carrier payment and bonus/penalty rules |

## Decision Rules

```text
if recurring_supplier_lane and stable_volume:
  prefer contract or dedicated partner capacity

if urgent_pickup and contract_capacity_unavailable:
  use spot search with price tolerance

if supplier_loading_method requires forklift:
  require compatible vehicle and warehouse/supplier MHE readiness

if cargo arrives damaged:
  compare supplier pickup photo, transit events, and receiving photo

if ASN quantity differs from received quantity:
  create discrepancy event and block automatic settlement

if inbound stock matches active outbound demand:
  evaluate cross-dock instead of standard putaway
```

## System Fields

```text
inbound_shipment
- inbound_id
- supplier_id
- purchase_order_id
- warehouse_id
- asn_id
- shipment_ready_time
- pickup_window_start
- pickup_window_end
- fleet_mode: contract | spot | hybrid | dedicated
- preferred_fleet_types
- contract_rate_id
- spot_pricing_tolerance_pct
- cargo_type
- expected_quantity
- expected_weight
- expected_volume
- packaging_status
- document_status
- loading_method
- vehicle_requirement
- pickup_photo_required
- supplier_signature_required
- receiving_status
- discrepancy_status
- quality_status
- settlement_rule
```

## Product Modules

| Module | Value |
|--------|-------|
| Supplier portal | shared pickup planning and visibility |
| Inbound pickup workflow | driver app evidence and handoff proof |
| Contract + spot sourcing | lower cost with surge resilience |
| Receiving discrepancy module | protects inventory truth and payment fairness |
| Dock appointment scheduling | reduces gate congestion and detention |
| Inbound KPI dashboard | turns supplier and carrier behavior into data |
| Cross-dock recommendation | converts inbound timing into outbound speed |

## Related Notes

- [[Inbound Logistics Effectiveness Source]]
- [[Warehouse Execution & Intelligence Framework]]
- [[Inventory-Driven Resource Allocation Framework]]
- [[Order Processing and Transportation Management Knowledge Map]]
- [[Fleet vs Partner Allocation Strategy]]
- [[Load Matching Algorithm]]
- [[Vehicle Assignment Logic]]
- [[Transport Control Tower KPI Framework]]
- [[Proof of Delivery]]

