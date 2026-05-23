---
type: algorithm
domain: pricing
decision_value: medium
inputs:
  - distance_km
  - vehicle_type
  - cargo_type
  - route_factor
  - route_difficulty_factors
  - origin_city_tier
  - destination_city_tier
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
| route_difficulty_factors | Object | Terrain, road quality, congestion, weather, toll density, accident, and checkpoint inputs |
| origin_city_tier | Enum | Metro/Tier-1/Tier-2/Tier-3/Semi-Urban/Rural |
| destination_city_tier | Enum | Metro/Tier-1/Tier-2/Tier-3/Semi-Urban/Rural |
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
   - route difficulty score
   - urbanization density impact
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

## Chargeable Weight Rule

Use:

```text
chargeable_weight = max(actual_weight, volumetric_weight)
```

The volumetric divisor must be configurable by vehicle class, cargo profile, and commercial policy.

The improved calculator uses a sample conversion:

```text
volumetric_weight_tons = cargo_volume_cbm / 1.6667
```

Treat that as a starting assumption, not a permanent rule.

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

## Route Cost Floor Enhancements

The deterministic floor should expose the raw operating cost before commercial multipliers.

Recommended breakdown:

- fuel cost from route distance, vehicle mileage, and origin or corridor diesel price
- toll cost from vehicle toll rate and route distance
- driver cost allocated from monthly/annual driver cost and expected monthly kilometres
- depreciation allocated from annual capital cost and expected annual kilometres
- vehicle insurance allocated by trip distance
- permit and compliance cost allocation
- maintenance and tyre cost per kilometre
- loading/unloading cost
- document or e-way bill handling cost where applicable

This floor feeds dynamic pricing.

It should not include customer discounts, platform fee, final GST, or provider payout deductions.

## Decision Notes

- This note defines the quote floor, not the full customer-facing price.
- Deterministic costs should stay separate from discounts, platform fees, and taxes.
- Fuel cost should ideally be mileage-aware rather than treated as one flat assumption per vehicle class.
- The output should remain explainable enough for audit, settlement, and dispute review.
- RDS and density factors should be visible as separate quote lines when they materially affect price.
- Deadhead or backhaul logic belongs in dynamic pricing, but the distance floor should provide lane data required to calculate it.
- Do not bake final GST rates into the distance floor; tax classification belongs to the finance/GST layer.

## Related Notes

- [[Dynamic Pricing Logic]]
- [[Urgency Surcharge Logic]]
- [[Vehicle Operating Cost Model]]
- [[Hybrid Logistics Data Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
