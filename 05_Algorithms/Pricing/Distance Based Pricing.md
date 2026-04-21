---
type: algorithm
domain: pricing
decision_value: medium
inputs:
  - distance_km
  - vehicle_type
  - cargo_type
  - route_factor
  - chargeable_weight
outputs:
  - base_freight
  - cost_breakdown
status: verified
related_hubs:
  - Algorithms Hub
  - Business Models Hub
tags:
  - algorithm
  - pricing
---

# Distance Based Pricing

## Purpose

Calculate the deterministic trip-cost floor for a shipment based on distance, vehicle class, route conditions, and chargeable load.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| distance_km | Float | Total route distance |
| vehicle_type | Enum | LCV/MCV/HCV/Container |
| cargo_type | String | Category affecting handling and rate |
| route_factor | Float | Route difficulty multiplier |
| chargeable_weight | Float | Actual or volumetric weight used for pricing |

## Logic

```text
1. DETERMINE chargeable weight:
   - max(actual_weight, volumetric_weight)

2. GET base rate per km for vehicle type

3. CALCULATE line-haul cost:
   BASE = distance x base_rate

4. APPLY cargo and route adjustments:
   - cargo sensitivity
   - route difficulty
   - handling complexity

5. ADD deterministic trip costs:
   - loading/unloading
   - documentation
   - tolls
   - maintenance allocation
   - depreciation allocation
   - driver cost allocation adjusted for region when useful
   - insurance if applicable

6. RETURN a cost breakdown that can feed [[Dynamic Pricing Logic]]
```

## Vehicle Base Rates

| Vehicle | Per KM Rate | Pricing Note |
|---------|-------------|--------------|
| LCV | Lower | Best for lighter urban and regional loads |
| MCV | Medium | Balanced cost for mid-weight movements |
| HCV | Higher | Better for dense long-haul utilization |
| Container | Highest | Premium for specialized movement |

## Cost Layers

| Layer | Purpose |
|-------|---------|
| Line-haul | Core distance-based transport cost |
| Handling | Loading, unloading, and document effort |
| Corridor | Toll and route difficulty impact |
| Maintenance | Recover wear, tires, and service burden |
| Depreciation | Recover vehicle capital cost over time |
| Labor | Recover driver salary and field effort |
| Insurance | Risk-based protection when required |

## Decision Notes

- This note defines the quote floor, not the full customer-facing price.
- Deterministic costs should stay separate from discounts, platform fees, and taxes.
- Fuel cost should ideally be mileage-aware rather than treated as one flat assumption per vehicle class.
- The output should remain explainable enough for audit, settlement, and dispute review.

## Related Notes

- [[Dynamic Pricing Logic]]
- [[Urgency Surcharge Logic]]
- [[Vehicle Operating Cost Model]]
- [[Hybrid Logistics Data Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
