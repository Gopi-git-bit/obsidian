---
type: algorithm
domain: pricing
decision_value: high
inputs:
  - base_price
  - urgency_level
  - current_demand
  - vehicle_availability
outputs:
  - final_price
  - surcharge_applied
status: verified
related_hubs:
  - Algorithms Hub
  - Business Models Hub
tags:
  - algorithm
  - pricing
---

# Urgency Surcharge Logic

## Purpose

Apply dynamic surcharges based on delivery urgency and market conditions.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| base_price | Currency | Standard calculated price |
| urgency_level | Enum | Normal/Express/Urgent/Critical |
| current_demand | Float | Demand ratio (0.5-2.0) |
| vehicle_availability | Float | Supply ratio (0.5-2.0) |

## Logic

```
1. DETERMINE base urgency multiplier:
   - Normal: 1.0
   - Express (same day): 1.25
   - Urgent (4-6 hours): 1.5
   - Critical (immediate): 1.75-2.0

2. CALCULATE market factor:
   - market_factor = current_demand / vehicle_availability
   - If > 1.5: Apply market surge
   - If < 0.7: Apply market discount

3. FINAL_MULTIPLIER = urgency × market_factor

4. FINAL_PRICE = base_price × FINAL_MULTIPLIER
```

## Surcharge Tiers

| Urgency | Time Window | Base Surcharge |
|---------|-------------|----------------|
| Normal | 24+ hours | 0% |
| Express | Same day | 25% |
| Urgent | 4-6 hours | 50% |
| Critical | Immediate | 75-100% |

## Constraints

- Maximum surcharge: 100% of base price
- Minimum price: Cost + 10% margin
- Floor price: Never below operational cost

## Related Notes

- [[Dynamic Pricing Logic]]
- [[Distance Based Pricing]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
