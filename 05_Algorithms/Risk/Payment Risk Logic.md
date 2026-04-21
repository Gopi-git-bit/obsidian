---
type: algorithm
domain: risk
decision_value: medium
inputs:
  - customer_id
  - order_amount
  - payment_terms
  - customer_history
outputs:
  - risk_score
  - credit_decision
  - payment_terms
status: draft
related_hubs:
  - Algorithms Hub
tags:
  - algorithm
  - risk
  - payment
---

# Payment Risk Logic

## Purpose

Assess credit risk and determine appropriate payment terms for customers.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| customer_id | UUID | Customer identifier |
| order_amount | Currency | Order value |
| payment_terms | Enum | Prepaid/Postpaid |
| customer_history | Object | Payment history data |

## Logic

```
1. CALCULATE risk score (0-100):
   - Payment history (40%): On-time payments ratio
   - Order history (30%): Volume and frequency
   - Credit history (20%): External data if available
   - Business age (10%): Years operating

2. DETERMINE risk level:
   - Low (0-30): Full credit available
   - Medium (31-60): Partial credit, monitoring
   - High (61-80): Limited credit, prepayment
   - Very High (81-100): Full prepayment required

3. SET payment terms based on risk:
   - Low: Net 30 terms
   - Medium: Net 15 terms
   - High: 50% advance, 50% on delivery
   - Very High: Full prepayment
```

## Risk Factors

| Factor | Weight | Data Source |
|--------|--------|-------------|
| Payment history | 40% | Platform records |
| Order frequency | 20% | Platform records |
| Order value | 10% | Platform records |
| Business tenure | 15% | Registration data |
| External credit | 15% | Credit bureaus |

## Related Notes

- [[Customer Credit Scoring]]
- [[Payment Settlement Agent]]

## Related Hubs

- [[Algorithms Hub]]
