---
type: scenario
domain: operations
urgency: high
decision_value: high
actors:
  - customer
  - payment_agent
  - admin
region: India
status: draft
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
tags:
  - scenario
  - admin-escalations
  - payment
---

# Scenario - Payment Dispute

## Situation

Customer disputes payment amount - claims incorrect charges, unauthorized deductions, or disagreement with invoice.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Dispute type | Various | Amount/Unauthorized |
| Amount at stake | Variable | Full or partial |
| Customer history | Verified | Repeat customer? |
| Documentation | Needed | Proof of charges |

## Recommended Response

```
1. RECEIVE dispute with specific details
2. COLLECT all relevant documentation
3. VERIFY charges against agreed quote
4. CHECK for any legitimate adjustments
5. EXPLAIN charges clearly to customer
6. IF error found: Process refund
7. IF valid: Maintain position with evidence
8. ESCALATE to management if unresolved
```

## Related SOPs

- [[SOP - Customer Communication]]
- [[SOP - Handle POD Disputes]]

## Related Concepts

- [[Payment Terms]]
- [[Invoice Disputes]]

## Related Hubs

- [[Operations Strategy Hub]]
