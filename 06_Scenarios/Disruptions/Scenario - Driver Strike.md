---
type: scenario
domain: operations
urgency: critical
decision_value: high
actors:
  - dispatcher
  - transport_company
  - admin
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
tags:
  - scenario
  - disruptions
  - strike
---

# Scenario - Driver Strike

## Situation

Drivers across the industry or in a specific region go on strike, affecting pickup and delivery capabilities.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Strike scope | Local/Regional | Industry-wide? |
| Duration | Unknown | May be extended |
| Active orders | At risk | Pickups/deliveries pending |
| Customer impact | High | Delayed shipments |

## Decision Questions

1. **Strike scope?** Limited or widespread?
2. **Alternative drivers?** Partner fleet?
3. **Order prioritization?** Which to fulfill?
4. **Customer communication?** Transparent updates?

## Recommended Response

```
1. ASSESS strike impact on operations
2. IDENTIFY all affected orders
3. COORDINATE with partner transporters
4. PRIORITIZE critical deliveries
5. COMMUNICATE proactively with all customers
6. NEGOTIATE if possible with striking drivers
7. INVOKE force majeure clauses if needed
```

## Risks

- Deliveries delayed → SLA breach
- Customer churn → Trust erosion
- Driver relations → Long-term impact

## Related SOPs

- [[SOP - Handle Partner Transporter]]
- [[SOP - Customer Communication]]
- [[SOP - Escalate Delayed Shipment]]

## Related Concepts

- [[Logistics SLA]]
- [[Partner Network]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Fleet & Transport Hub]]
- [[Customer Problems Hub]]
