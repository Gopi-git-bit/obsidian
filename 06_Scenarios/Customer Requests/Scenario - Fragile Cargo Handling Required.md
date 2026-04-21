---
type: scenario
domain: transport
urgency: high
decision_value: high
actors:
  - customer
  - dispatcher
  - driver
region: India
status: verified
related_hubs:
  - Scenario Playbooks Hub
  - Operations Strategy Hub
  - Fleet & Transport Hub
source_notes:
  - claude
tags:
  - scenario
  - customer-requests
  - fragile-cargo
---

# Scenario - Fragile Cargo Handling Required

## Situation

Customer needs to transport fragile goods (glassware, machinery parts, artwork) that require special handling during loading, transit, and unloading.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Cargo fragility | High | Requires careful handling |
| Packaging | Must be adequate | May need strapping/packing |
| Loading time | Extended | May need pallet jack/forklift |
| Transit speed | Moderate | Avoid sudden braking |

## Decision Questions

1. **Vehicle type?** Open vs closed body considerations
2. **Special equipment?** Forklift, packing materials
3. **Handler experience?** Trained driver/loader required
4. **Insurance?** Cargo insurance coverage needed

## Recommended Response

```
1. ASSIGN closed body vehicle with proper securing
2. COORDINATE with customer on loading method
3. INSTRUCT driver on fragile handling protocols
4. VERIFY insurance coverage before acceptance
5. DOCUMENT cargo condition at pickup with photos
```

## Related SOPs

- [[SOP - Handle High Value Cargo]]
- [[SOP - Verify Shipment Documents]]

## Related Concepts

- [[Proof of Delivery]]
- [[Damage Claim Process]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Route Risk Scoring]]

## Related Hubs

- [[Fleet & Transport Hub]]
- [[Compliance & Regulation Hub]]
