---
type: algorithm
domain: allocation
decision_value: high
inputs:
  - warehouse_profile
  - material_profile
  - shipment_profile
  - lane_profile
  - vehicle_pool
  - carrier_pool
  - historical_exceptions
outputs:
  - distribution_strategy
  - vehicle_recommendation
  - carrier_shortlist
  - dispatch_constraints
  - correlation_explanation
status: draft
related_hubs:
  - Algorithms Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - algorithm
  - allocation
  - warehousing
  - transport-management
  - correlation
---

# Warehouse Transport Correlation Algorithm

## Purpose

Select the best transport and distribution plan for a warehouse customer by correlating warehouse grade, material type, handling capability, lane behavior, vehicle fit, carrier reliability, and historical exceptions.

This extends [[Load Matching Algorithm]] and [[Multi-Objective Vehicle Scoring]] with warehouse-specific intelligence.

## Inputs

| Input | Description |
|-------|-------------|
| `warehouse_profile` | Grade, dock readiness, yard access, MHE, loading method, detention history, document quality |
| `material_profile` | Cargo class, temperature need, hazard class, fragility, density, value, expiry, contamination risk |
| `shipment_profile` | Weight, volume, dimensions, pallet/carton count, pickup window, delivery window, urgency |
| `lane_profile` | Distance, road quality, toll, congestion, delivery density, return-load probability, route risk |
| `vehicle_pool` | Available vehicle type, body type, capacity, location, compliance, fitness, GPS, reefer/special equipment |
| `carrier_pool` | Carrier price, reliability, lane familiarity, claim history, cancellation history, document discipline |
| `historical_exceptions` | Detention, damage, delay, overload, route deviation, temperature excursion, POD delay, payment dispute |

## Hard Filters

Reject any plan where:

- Cargo exceeds legal or rated payload.
- Vehicle body type is incompatible with cargo condition.
- Warehouse yard/dock cannot support the vehicle.
- Dock height, dock width, apron depth, or turning radius is incompatible with the vehicle class.
- Palletized cargo cannot fit the selected truck body or loading method.
- Required MHE is absent or unconfirmed for heavy/palletized cargo.
- Cold-chain cargo lacks cold staging, reefer vehicle, or temperature proof.
- Hazardous cargo lacks required carrier, driver, route, and safety readiness.
- High-value cargo lacks verified carrier, GPS, insurance, and trust threshold.
- Documentation is insufficient for e-way bill, invoice, customs, bonded, or regulated movement.

Use [[Government Warehousing Standards Compliance Layer]] for the official-standard checks behind dock fit, truck body fit, pallet fit, CMVR/MoRTH readiness, weighment, vehicle gate checklist, and product-specific compliance.

## Strategy Selection Logic

```text
if shipment_volume_high and destination_single:
  candidate_strategy = direct_ftl

if shipment_volume_low and delivery_density_high:
  candidate_strategy = ltl_consolidation or milk_run

if many_small_shipments and repeat_city_to_city_flow:
  candidate_strategy = hub_and_spoke

if inbound_outbound_timing_synchronized and dwell_time_low:
  candidate_strategy = cross_docking

if storage_adds_no_value and receiver_ready:
  candidate_strategy = warehouse_bypass

if long_distance_high_volume and terminal_access_good:
  candidate_strategy = intermodal

if temperature_control_required:
  restrict strategy to controlled_direct, controlled_hub, or cold_chain_network
```

## Vehicle Recommendation Logic

```text
vehicle_feasibility_score =
  payload_fit
+ cube_fit
+ body_type_fit
+ warehouse_access_fit
+ loading_method_fit
+ route_access_fit
+ compliance_fit
+ special_equipment_fit

vehicle_utility_score =
  cost_efficiency
+ ETA_confidence
+ carrier_reliability
+ lane_familiarity
+ capacity_utilization
+ return_load_probability
- detention_risk
- damage_risk
- overload_risk
- temperature_risk
- documentation_risk
```

## Correlation Features

| Feature | Positive Signal | Negative Signal |
|---------|-----------------|-----------------|
| `grade_material_fit` | Grade A cold warehouse with pharma; Grade B regional warehouse with FMCG | Grade C manual godown with fragile/high-value/cold cargo |
| `warehouse_vehicle_fit` | Yard, dock, MHE, and body type all compatible | HCV assigned to tight yard; pallet cargo without forklift |
| `material_body_fit` | Closed body for electronics/textiles; reefer for perishables; tanker for liquid | Open body for moisture-sensitive cargo |
| `network_density_fit` | Repeated drops allow milk run or hub consolidation | Isolated urgent load forced into costly direct route |
| `lane_return_fit` | Destination has backhaul demand | Long-haul vehicle likely returns empty |
| `exception_history_fit` | Warehouse and carrier have low detention/damage/POD issues | Repeated delay, overload, or claim pattern |
| `service_cost_fit` | SLA value justifies higher-cost carrier/vehicle | Low-value nonurgent cargo over-served with premium model |

## Default Weights

| Objective | Weight |
|-----------|--------|
| Feasibility and compliance | 0.25 |
| Service reliability and ETA confidence | 0.20 |
| Vehicle/body/handling fit | 0.20 |
| Total landed transport cost | 0.15 |
| Risk reduction | 0.10 |
| Return-load and utilization | 0.10 |

Weights should shift by material:

- Pharma, food, and hazardous cargo: increase risk and compliance.
- FMCG and ecommerce: increase delivery density and time-window reliability.
- Steel, cement, and dense cargo: increase payload, axle risk, and loading method.
- High-value electronics: increase trust, insurance, GPS, and secure vehicle fit.

## Output

```text
transport_decision
- chosen_distribution_strategy
- chosen_vehicle_model
- required_body_type
- required_handling_support
- carrier_shortlist
- driver_or_carrier_constraints
- route_constraints
- document_requirements
- price_risk_adjustments
- confidence_score
- explanation
- fallback_plan
```

## Pseudocode

```text
function plan_transport(warehouse, material, shipment, lane, vehicles, carriers, history):
  warehouse_score = score_warehouse_capability(warehouse, material, shipment)
  material_risk = classify_material_risk(material)
  candidate_strategies = generate_distribution_strategies(warehouse, material, shipment, lane)

  feasible_vehicles = []
  for vehicle in vehicles:
    if passes_hard_filters(warehouse, material, shipment, lane, vehicle):
      feasible_vehicles.append(vehicle)

  if feasible_vehicles is empty:
    return fallback("expand radius, split load, change vehicle class, require loading support, or escalate")

  scored_options = []
  for strategy in candidate_strategies:
    for vehicle in feasible_vehicles:
      for carrier in carriers_that_can_operate(vehicle, lane):
        score = weighted_score(
          feasibility=strategy_vehicle_fit(strategy, vehicle, warehouse, shipment),
          service=eta_and_reliability(carrier, lane, history),
          handling=warehouse_vehicle_material_fit(warehouse, vehicle, material),
          cost=total_landed_transport_cost(strategy, vehicle, carrier, lane),
          risk=risk_penalty(material, lane, carrier, warehouse, history),
          utilization=capacity_and_return_load(vehicle, shipment, lane)
        )
        scored_options.append((strategy, vehicle, carrier, score))

  best = highest_score_above_threshold(scored_options)
  if best is missing:
    return fallback("manual dispatcher review with top constraint failures")

  return decision_with_explanation(best)
```

## Learning Loop

Every completed shipment updates the model:

| Event | Score Updated |
|-------|---------------|
| Late vehicle arrival | Carrier punctuality, lane ETA confidence |
| Long loading wait | Warehouse detention score, loading-method assumption |
| Damage or shortage | Warehouse handling score, carrier claim score, material risk |
| Overload event | Warehouse/loading-point accuracy score, customer weight trust |
| Temperature excursion | Cold-chain carrier score, cold dock readiness |
| POD delay | Driver/carrier document discipline |
| Empty return | Lane return-load probability |
| Payment dispute | Customer and carrier commercial risk |

## Startup Decision Use

Use this algorithm to decide:

- Which warehouses are best first customers.
- Which warehouse grade needs assisted operations versus API-grade integration.
- Which vehicle models should be recruited in each city or lane.
- Which lanes justify partner carriers, hubs, or cross-dock nodes.
- Which customers need pricing buffers for detention, overload, damage, or documentation risk.
- Which material categories deserve specialized product modules.

## Related Notes

- [[Warehouse Customer Strategy Canvas]]
- [[Warehouse Vehicle and MHE Model Taxonomy]]
- [[LCV vs MCV vs HCV]]
- [[Load Matching Algorithm]]
- [[Multi-Objective Vehicle Scoring]]
- [[Vehicle Assignment Logic]]
- [[Route Risk Scoring]]
- [[Lane Intelligence Model]]
- [[Transport Mode Selection Framework]]
- [[Carrier Scoring Algorithm]]
