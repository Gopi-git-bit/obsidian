---
type: algorithm
domain: pricing
decision_value: high
inputs:
  - base_rate
  - distance
  - vehicle_type
  - urgency
  - market_demand
  - fuel_cost
  - route_risk
  - route_difficulty_score
  - urbanization_density_factor
  - lane_viability
  - segment_fee_rule
  - backhaul_signal
outputs:
  - quoted_price
  - confidence_score
status: verified
related_hubs:
  - Algorithms Hub
  - Business Models Hub
tags:
  - algorithm
  - pricing
---

# Dynamic Pricing Logic

## Purpose

Generate competitive yet profitable quotes by layering commercial adjustments on top of a deterministic trip-cost floor.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| base_rate | Currency/km | Market base rate |
| distance | km | Total route distance |
| vehicle_type | Enum | LCV/MCV/HCV multiplier |
| urgency | Enum | Normal/Express/Urgent multiplier |
| market_demand | Float | 0.8-1.5 demand factor |
| fuel_cost | Currency/L | Current fuel price |
| route_risk | Float | 1.0-1.3 risk factor |
| route_difficulty_score | Float | 0-100 composite score for terrain, road quality, congestion, weather, toll density, accident history, and checkpoint friction |
| urbanization_density_factor | Float | Origin/destination density multiplier based on Metro, Tier-1, Tier-2, Tier-3, semi-urban, or rural operating complexity |
| lane_viability | Enum | Return-load viability class used to price deadhead risk |
| segment_fee_rule | Object | Segment-specific discount and platform fee logic |
| backhaul_signal | Object | Return-route discount eligibility or deadhead reduction signal |

## Logic

```text
1. START with deterministic cost floor from [[Distance Based Pricing]]
2. APPLY Route Difficulty Score surcharge to reflect terrain, poor roads, congestion, weather, toll density, accident history, and checkpoint friction
3. APPLY urbanization density factor using both origin and destination operating complexity
4. APPLY service-tier, urgency, demand, and surge adjustments
5. APPLY lane-viability / deadhead multiplier when return-load probability is weak
6. APPLY segment discounts and platform-fee logic separately for transparency
7. ADD value-added services and insurance where needed
8. APPLY backhaul discount only when return-economics justify it and it does not break the quote floor
9. CLASSIFY GST through the finance/tax engine instead of hard-coding one transport rate
10. STORE a full quote breakdown for audit and later acceptance analysis
```

## Enhanced Pricing Dimensions

### Route Difficulty Score

Route difficulty should be a composite score from 0 to 100.

Inputs:

- terrain grade
- road surface quality
- traffic congestion
- weather risk
- toll-gate density
- historical accident rate
- border or checkpoint frequency

Recommended tier mapping:

| RDS Band | Meaning | Pricing Action |
| --- | --- | --- |
| 0-20 | easy corridor | no or minimal surcharge |
| 20-40 | normal operating friction | low surcharge |
| 40-60 | moderate difficulty | medium surcharge |
| 60-80 | hard corridor | high surcharge |
| 80-100 | extreme operating risk | manual review or maximum bounded surcharge |

### Urbanization Density Factor

Both origin and destination should influence cost.

Use city tier plus operational signals:

- congestion index
- access restrictions
- average urban speed
- truck entry windows
- last-mile difficulty

Dense metros can increase costs because of congestion and entry restrictions.

Rural or remote locations can also increase costs because of poor road quality and weak return-load availability.

### Lane Viability And Deadhead Risk

Lane viability should price the probability of finding a return load.

Recommended classes:

| Class | Meaning |
| --- | --- |
| highly_balanced | strong two-way freight flow |
| moderately_balanced | reasonable return-load probability |
| unbalanced_origin_heavy | loaded one way, weak return flow |
| seasonal | return economics vary by harvest, festival, or industry cycle |
| remote_low_demand | high deadhead risk |

Important:

```text
Backhaul intelligence can reduce price only when it is backed by an auditable return-load signal.
Deadhead risk can increase price when the lane is structurally one-way or remote.
```

## Pricing Data Provider Rule

Pricing logic should not hard-code production reference data.

Use a provider abstraction for:

- vehicle cost parameters
- diesel/fuel prices
- city tiers and congestion data
- route difficulty factors
- lane viability and return-load probability
- insurance rates
- value-added service catalog
- segment discount and fee rules

Development can use in-memory sample data.

Production should source this from PostgreSQL/Supabase, graph route intelligence, or approved external APIs.

## Architecture Notes

- Precision math should use decimal arithmetic, not binary floating point.
- Quote engines should keep base cost, fee layers, discount layers, and tax layers separately explainable.
- Backhaul discounting is strongest when sourced from [[Return Load Optimization]] or graph-based route intelligence.
- Configuration such as GST, volumetric divisor, and pricing weights should be hot-reloadable.
- GST display belongs to the finance event layer; pricing can estimate tax placeholders but final tax treatment must come from supplier role, payer, invoice ownership, and effective-dated GST rules.
- AI or ML surge output should be treated as a bounded multiplier, not as the quote authority.

## Pricing Factors

### Market Factors

- Demand-supply balance
- Seasonality
- Route popularity
- Competition rates
- Congestion or delay-sensitive corridor pressure

### Cost Factors

- Fuel cost
- Driver cost
- Vehicle depreciation
- Overhead allocation
- Tolls and maintenance allocation
- Insurance, fitness, and other compliance-linked vehicle costs
- Platform fee logic by customer segment

### Value Factors

- Urgency premium
- Cargo value
- Special handling
- Customer relationship
- Return-route economics

## Commission vs Flat Fee

See: [[Commission vs Flat Fee]]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Price below cost | Reject or minimum floor |
| Extreme demand | Apply surge pricing |
| New customer | Standard rate initially |
| Long-term contract | Negotiated rates |
| Backhaul discount misfires | Require auditable eligibility signal before discounting |
| RDS very high | Add bounded surcharge or send for manual review |
| Rural destination with weak return flow | Apply lane-viability/deadhead multiplier |
| Metro-to-metro route with severe access restrictions | Apply density factor and show the reason in quote detail |
| GST ownership unresolved | Return quote estimate but block final invoice/tax finalization |

## Market Benchmark Notes

- External market-rate bands can help detect obviously weak or unrealistic quotes, but they should not override deterministic floor protection.
- Congestion-based delay fees should remain explicit and bounded rather than becoming a hidden multiplier.
- Regional rate intelligence is most useful as a calibration input for South India and Tier-2 or Tier-3 corridors.

## Related Notes

- [[Distance Based Pricing]]
- [[Urgency Surcharge Logic]]
- [[Indian MSME Logistics Model]]
- [[Return Load Optimization]]
- [[South India Local Truck Rate Bands]]
- [[Vehicle Operating Cost Model]]
- [[Hybrid Logistics Data Architecture]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[GST for Logistics]]
