---
type: algorithm
domain: matching
decision_value: high
inputs:
  - order_requirements
  - carrier_profiles
  - partnership_terms
outputs:
  - carrier_selection
  - match_score
status: verified
related_hubs:
  - Algorithms Hub
  - Business Models Hub
tags:
  - algorithm
  - matching
  - carrier
---

# Carrier Selection Algorithm

## Purpose

Select the optimal carrier/partner for orders where own fleet is unavailable.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| order_requirements | Object | Vehicle, cargo, route needs |
| carrier_profiles | Array | Partner carrier data |
| partnership_terms | Object | Commission, SLAs, terms |

## Logic

```
1. PRE-QUALIFY carriers:
   - Vehicle type availability
   - Geographic coverage
   - Service track record

2. SCORE carriers by:
   - Reliability score (35%)
   - Price competitiveness (25%)
   - Quality rating (25%)
   - Response time (15%)

3. CHECK commercial terms:
   - Commission within limits
   - SLA compliance capability
   - Payment terms acceptable

4. SELECT optimal carrier
```

## Scoring Matrix

| Criterion | Weight | Max Score |
|----------|--------|-----------|
| Reliability | 35% | 5.0 |
| Price | 25% | 5.0 |
| Quality | 25% | 5.0 |
| Response | 15% | 5.0 |

## Carrier Tiers

| Tier | Score Range | Priority |
|------|-------------|----------|
| Gold | 4.5-5.0 | First choice |
| Silver | 3.5-4.4 | Standard |
| Bronze | 2.5-3.4 | Backup only |

## Related Notes

- [[Load Matching Algorithm]]
- [[Carrier Scoring Algorithm]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
