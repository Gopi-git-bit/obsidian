---
type: concept
domain: fleet
decision_value: high
status: evergreen
related_hubs:
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - concept
  - fleet
  - pricing
  - vehicle-costs
---

# Vehicle Operating Cost Model

## Purpose

Describe the recurring vehicle-cost inputs that should feed deterministic pricing, fleet selection, and route-level profitability checks.

## Core Cost Components

| Component | Why It Matters |
|-----------|----------------|
| Fuel or mileage efficiency | Directly drives per-kilometer economics and corridor profitability |
| Depreciation | Recovers vehicle capital cost over time and utilization |
| Insurance | Adds recurring compliance and risk cost |
| Tolls | Changes materially by corridor and vehicle class |
| Driver salary or labor allocation | Varies by route length, region, and operating pattern |
| Maintenance and tires | Captures wear from utilization, road quality, and load pattern |
| Fitness, permits, and health-linked compliance | Adds recurring legal-operating burden beyond fuel alone |

## Vehicle-Class Pattern

| Vehicle Class | Cost Shape | Commercial Reading |
|---------------|------------|--------------------|
| LCV | Lower fixed burden, better mileage, lower toll exposure | Strong for urban and short-regional moves where agility matters |
| MCV | Balanced fixed and variable costs | Useful when route mix and load profile are variable |
| HCV | Higher depreciation, higher toll burden, weaker mileage when underutilized | Best when load density and corridor utilization are strong |

## Pricing Implications

- Quote floors should reflect more than fuel and distance.
- Mileage-aware cost assumptions are more accurate than a single flat rate per vehicle class.
- Long-haul pricing should be sensitive to toll burden and depreciation recovery.
- Return-load logic should consider whether a model's operating cost stays viable on the empty leg.

## Assignment Implications

- IMS and fleet allocation logic should prefer vehicles whose operating-cost profile matches the route, not just the gross capacity.
- Premium or time-sensitive lanes can justify lower-mileage models only when SLA and revenue support the extra burden.
- Low-utilization routes can silently destroy HCV economics if pricing does not recover fixed costs.

## Data Quality Warnings

- Regional driver salary assumptions should be versioned, not hard-coded as universal truth.
- Insurance and compliance costs should be refreshed periodically.
- Model-level mileage should be treated as an operating estimate, not a brochure claim.

## Related Notes

- [[LCV vs MCV vs HCV]]
- [[Distance Based Pricing]]
- [[Dynamic Pricing Logic]]
- [[Return Load Economics]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
