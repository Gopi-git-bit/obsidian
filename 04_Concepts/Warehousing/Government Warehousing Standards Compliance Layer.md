---
type: concept
domain: warehousing
decision_value: high
status: evergreen
region: India
related_hubs:
  - Compliance & Regulation Hub
  - Indian Logistics Ecosystem Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - concept
  - warehousing
  - standards
  - dpiit
  - wai
  - bis
  - wdra
  - compliance
---

# Government Warehousing Standards Compliance Layer

## Definition

This note converts the DPIIT-WAI `e-Handbook on Warehousing Standards (2025 Edition)` into a platform design layer for warehouse onboarding, warehouse grading, vehicle assignment, dock compatibility, safety checks, and transport network planning.

Use it as the official-standard overlay on top of the more general warehouse strategy notes.

## Strategic Correction

Our warehouse A/B/C segmentation remains useful for customer targeting, but it must be treated as a commercial and operational segmentation, not a formal legal classification.

The source says Grade A and Grade B are industry nomenclature. They are not formal BIS or WDRA classifications, and no formal Indian standard defines Grade A/B/C warehouse grades.

Platform implication:

```text
commercial_grade = A | B | C
official_standard_fit = infrastructure + fire + floor + dock + pallet + racking + MHE + product + transport + sustainability + technology
```

The startup should therefore say:

- "Grade A/B/C operating profile" for sales, risk, and routing.
- "BIS/WDRA/CMVR/NBC/MoRTH compliance status" for regulatory and standards readiness.

## Where This Fits In The Product

| Product Layer | Government Standard Impact |
|---------------|----------------------------|
| Warehouse onboarding | Capture infrastructure, dock, yard, MHE, racking, fire safety, pallet, product, and technology readiness |
| Customer segmentation | Keep A/B/C as practical market labels, but validate each site with standard-based scorecards |
| Vehicle assignment | Check truck body, dock height, apron depth, turning radius, pallet fit, forklift access, and CMVR/MoRTH readiness |
| TMS planning | Use warehouse location, demand pattern, lead-time target, and transport infrastructure quality |
| Compliance | Link to BIS, WDRA, CMVR, MoRTH, NBC, FSSAI/FCI/cold-chain references where relevant |
| Risk scoring | Penalize weak fire safety, poor dock fit, no weighment proof, inadequate MHE, weak vehicle checklist, poor documentation |
| Sustainability | Track fuel, route optimization, energy efficiency, water/resource use, waste, and green-building readiness |

## Official Standard Dimensions To Capture

| Dimension | Fields To Capture | Dispatch Impact |
|-----------|-------------------|-----------------|
| Infrastructure | clear height, floor load, column spacing, PEB/RCC, drainage, fire access, parking | Determines vehicle access, storage density, safety risk |
| Dock and apron | dock height, dock width, apron depth, dock leveler capacity, dock seals, wheel chocks | Determines LCV/MCV/HCV/container/reefer compatibility |
| Truck body fit | internal width, rear/side loading, flooring robustness, pallet loading fit | Determines palletized cargo compatibility and loading speed |
| Palletization | pallet size, pallet type, overhang, BOPT/forklift support | Determines cube utilization, truck fit, rack safety |
| Racking | load capacity, inspection, aisle fit, installation quality | Determines SKU storage safety and MHE path |
| MHE | forklift, reach truck, pallet jack, BOPT, stacker, VNA, operator skill | Determines loading turnaround and cargo handling eligibility |
| Product standards | agri/non-agri, grading, sampling, testing, weighment, cold/hazmat needs | Determines compliance checks before dispatch |
| Transport safety | vehicle checklist, cargo security, driver training, GPS, tamper evidence | Determines dispatch gate pass and carrier eligibility |
| Technology | WMS, TMS, FMS, telematics, AIS-140 GPS, digital docs, AI/ML readiness | Determines integration depth and visibility SLA |
| Sustainability | route optimization, fuel use, waste, energy, water, green building | Determines ESG reporting and cost reduction plan |

## Dock And Vehicle Compatibility Table

Use these source-derived dock planning bands as operational checks.

| Vehicle Class | Bed Height | Dock Height | Dock Width Per Bay | Apron Depth | Platform Rule |
|---------------|------------|-------------|--------------------|-------------|---------------|
| LCV | 750-900 mm | 750-900 mm | 2.5-3.0 m | 10-12 m | Good for small warehouses, city dispatch, low yard depth |
| MCV | 1000-1200 mm | 1000-1200 mm | 3.0-3.5 m | 12-15 m | Good for regional movement and mixed loads |
| HCV | 1200-1400 mm | 1200-1400 mm | 3.5-4.0 m | 15-18 m | Needs larger yard, dock discipline, MHE readiness |
| Container trailer | 1200-1400 mm | 1200-1400 mm | 3.5-4.0 m | 18-20 m | Needs large apron, turning radius, container/CFS readiness |
| Reefer | 1300-1500 mm | 1300-1500 mm | 3.5-4.0 m | 15-18 m | Needs cold dock discipline and temperature proof |

## Truck Body Standard Checks

Add these checks to vehicle onboarding and order assignment:

```text
truck_body_check
- clear_internal_width_mm >= 2286 where palletized standard movement is expected
- supports_standard_pallets: 1200x1200, 1200x1000, 1200x800, 1140x1140
- side_loading_ready if warehouse lacks ramp/dock-leveler support
- rear_forklift_entry_ready if rear loading is needed
- floor_supports_bopt_or_forklift_movement
- CMVR_compliance_confirmed
- MoRTH_body_code_practice_confirmed
```

## Warehouse Onboarding Scorecard

```text
official_warehouse_standard_score =
  infrastructure_score
+ dock_vehicle_compatibility_score
+ pallet_racking_mhe_score
+ fire_safety_score
+ product_specific_compliance_score
+ transport_gate_check_score
+ technology_visibility_score
+ sustainability_score
- exception_penalty
```

Where:

```text
exception_penalty =
  repeated_detention
+ damage_claims
+ failed_vehicle_checks
+ weighment_mismatch
+ missing_documents
+ unsafe_loading_events
+ temperature_excursions
```

## Transport Network Planning Rule

The government standard source connects warehouse planning and transportation planning. The TMS should therefore treat warehouse design as part of transport feasibility.

```text
if warehouse_dock_fit fails:
  reject vehicle assignment or require alternate loading plan

if apron_depth insufficient:
  reject HCV/container/reefer assignment or require offsite staging

if palletized cargo and truck body width/side/rear loading not compatible:
  reject or recommend alternate vehicle body

if lead_time_target <= 24h:
  prioritize direct or controlled hub route

if lead_time_target between 24h and 72h:
  compare direct, hub, milk-run, and consolidation models by service-cost curve

if repeated demand exists in both directions:
  prefer consolidated route with committed return-load planning
```

## A/B/C Customer Strategy With Official Overlay

| Commercial Segment | Official-Standard Interpretation | Sales Motion |
|--------------------|----------------------------------|--------------|
| A-grade operating profile | Likely stronger infrastructure, dock, fire, WMS, palletization, MHE, and vehicle access | Sell API/TMS integration, dock scheduling, control tower, SLA analytics |
| B-grade operating profile | Partial standards readiness, mixed manual/system flow, variable MHE/dock maturity | Sell vehicle recommendation, dock checklist, partner fleet pool, document/POD discipline |
| C-grade operating profile | Often informal/manual, weak records, limited dock/MHE, higher risk of detention or loading mismatch | Sell assisted dispatch, simple checklists, verified vehicle network, weight/document gate |

## Product Modules To Build From This Source

- Government-standard warehouse onboarding checklist
- Dock/vehicle compatibility validator
- Truck body and pallet fit validator
- MHE and racking readiness profile
- Vehicle entry/exit safety checklist
- Weighbridge and weighment proof capture
- AIS-140/GPS visibility readiness field
- Official standards reference library inside admin dashboard
- Sustainability and fuel/utilization reporting
- Warehouse standard maturity score for sales prioritization

## Related Notes

- [[DPIIT-WAI e-Handbook on Warehousing Standards 2025 Source]]
- [[Warehouse Customer Strategy Canvas]]
- [[Warehouse Execution & Intelligence Framework]]
- [[Warehouse Vehicle and MHE Model Taxonomy]]
- [[Warehouse Transport Correlation Algorithm]]
- [[LCV vs MCV vs HCV]]
- [[Transport Mode Selection Framework]]
- [[Transport Control Tower KPI Framework]]
- [[Legal Compliance Framework]]
- [[E-way Bill System]]

