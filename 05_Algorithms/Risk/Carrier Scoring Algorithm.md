---
type: algorithm
domain: risk
decision_value: high
inputs:
  - carrier_id
  - performance_history
  - order_history
  - customer_feedback
outputs:
  - carrier_score
  - risk_indicators
status: verified
related_hubs:
  - Algorithms Hub
  - Business Models Hub
tags:
  - algorithm
  - risk
  - carrier
---

# Carrier Scoring Algorithm

## Purpose

Calculate comprehensive performance scores for carrier partners to inform assignment decisions.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| carrier_id | UUID | Unique carrier identifier |
| performance_history | Array | Historical delivery data |
| order_history | Array | Past order outcomes |
| customer_feedback | Array | Shipper reviews |

## Logic

```
1. CALCULATE delivery metrics:
   - On-time rate (deliveries on time / total)
   - POD submission rate
   - Exception rate
   - Cancellation rate

2. CALCULATE quality metrics:
   - Damage rate
   - Customer complaint rate
   - Communication quality score

3. CALCULATE reliability metrics:
   - Acceptance rate (offers accepted)
   - Completion rate
   - Response time average

4. COMPOSITE_SCORE = weighted_sum(all_metrics)
```

## Scoring Formula

```
Score = (OnTime × 0.30) + 
        (Quality × 0.25) + 
        (Reliability × 0.25) + 
        (Feedback × 0.20)
```

## Score Ranges

| Score | Tier | Action |
|-------|------|--------|
| 4.5-5.0 | Excellent | Preferred partner |
| 4.0-4.4 | Good | Standard partner |
| 3.5-3.9 | Average | Monitor closely |
| 3.0-3.4 | Below Average | Probation |
| <3.0 | Poor | Review/replace |

## Related Notes

- [[Carrier Selection Algorithm]]
- [[Load Matching Algorithm]]

## Related Hubs

- [[Algorithms Hub]]
- [[Business Models Hub]]
