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

For formal collaboration pools, use [[Collaborative Logistics Network Framework]] before carrier scoring. A partner may be operationally strong but still unsuitable for collaboration if data sharing, economic alignment, compliance, or exit rules are weak.

For new corridor entry, use [[Partnership-Led Market Entry Framework]] to decide whether the partner is solving capacity, demand, compliance, technology, or trust before applying normal carrier ranking.

For collaboration pools or strategic partners, use [[Collaboration Risk Scoring Algorithm]] before expanding volume allocation.

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
   - Collaboration agreement scope if `collaboration_pool_id` exists

2. SCORE carriers by:
   - Reliability score (35%)
   - Price competitiveness (25%)
   - Quality rating (25%)
   - Response time (15%)

3. CHECK commercial terms:
   - Commission within limits
   - SLA compliance capability
   - Payment terms acceptable
   - Data sharing and dispute terms acceptable for collaborative orders

4. SELECT optimal carrier
```

## Collaboration Partner Gate

| Gate | Pass Condition |
|------|----------------|
| capability alignment | partner fills a corridor, vehicle, warehouse, or special-handling gap |
| technology readiness | partner can share required order, capacity, tracking, and POD events |
| commercial fit | revenue share, cost allocation, and customer ownership are clear |
| compliance fit | insurance, permits, audit trail, and privacy requirements pass |
| governance fit | dispute path, review cadence, and exit clause are explicit |
| risk-opportunity balance | opportunity justifies exposure under [[Collaboration Risk Scoring Algorithm]] |

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
- [[Collaborative Logistics Network Framework]]
- [[Partnership-Led Market Entry Framework]]
- [[Collaboration Risk Scoring Algorithm]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
