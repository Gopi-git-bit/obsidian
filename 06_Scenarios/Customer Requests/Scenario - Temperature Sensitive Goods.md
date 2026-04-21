---
type: scenario
domain: transport
urgency: high
decision_value: high
actors:
  - customer
  - dispatcher
region: India
status: draft
related_hubs:
  - Scenario Playbooks Hub
  - Fleet & Transport Hub
tags:
  - scenario
  - customer-requests
  - temperature-sensitive
---

# Scenario - Temperature Sensitive Goods

## Situation

Customer needs to transport temperature-sensitive goods (pharma, vaccines, perishables, chemicals) that require temperature-controlled vehicles.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Temperature range | Specific | Cold chain required |
| Cargo type | Perishable/Pharma | Critical handling |
| Duration | Time-sensitive | Spoilage risk |
| Monitoring | Required | Temperature logs |

## Recommended Response

```
1. REQUIRE refrigerated/insulated vehicle
2. VERIFY temperature control system
3. CONFIRM temperature monitoring capability
4. ESTABLISH acceptable temperature ranges
5. DOCUMENT temperature logs throughout
6. COORDINATE quick loading/unloading
```

## Related SOPs

- [[SOP - Assign Vehicle to Order]]
- [[SOP - Verify Shipment Documents]]

## Related Concepts

- [[Cold Chain Requirements]]
- [[Pharma Logistics Needs]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Operations Strategy Hub]]
