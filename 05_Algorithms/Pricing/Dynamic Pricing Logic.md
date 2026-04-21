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
| segment_fee_rule | Object | Segment-specific discount and platform fee logic |
| backhaul_signal | Object | Return-route discount eligibility or deadhead reduction signal |

## Logic

```text
1. START with deterministic cost floor from [[Distance Based Pricing]]
2. APPLY vehicle, urgency, demand, and route-risk adjustments
3. APPLY segment discounts and platform-fee logic separately for transparency
4. ADD value-added services and insurance where needed
5. APPLY backhaul discount only when return-economics justify it
6. CALCULATE GST on the final taxable subtotal
7. STORE a full quote breakdown for audit and later acceptance analysis
```

## Architecture Notes

- Precision math should use decimal arithmetic, not binary floating point.
- Quote engines should keep base cost, fee layers, discount layers, and tax layers separately explainable.
- Backhaul discounting is strongest when sourced from [[Return Load Optimization]] or graph-based route intelligence.
- Configuration such as GST, volumetric divisor, and pricing weights should be hot-reloadable.

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
