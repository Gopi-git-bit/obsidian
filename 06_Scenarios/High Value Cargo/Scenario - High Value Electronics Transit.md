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
  - Fleet & Transport Hub
  - Operations Strategy Hub
source_notes:
  - claude
tags:
  - scenario
  - high-value
  - electronics
---

# Scenario - High Value Electronics Transit

## Situation

Customer needs to transport high-value electronics (laptops, phones, components) worth INR 50+ lakhs. Requires secure, closed-body transport with full visibility.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Cargo value | INR 50L+ | Insurance threshold |
| Cargo type | Electronics | Fragile + high value |
| Packaging | Boxes/pallets | Tamper-proof preferred |
| Route | Tier 1 to Tier 2 | Multiple state borders |
| Security needs | High | Theft prevention |

## Decision Questions

1. **Vehicle type?** Closed body mandatory
2. **Insurance coverage?** Customer vs platform responsibility
3. **Route selection?** Safer vs faster tradeoff
4. **Driver vetting?** Additional background checks?
5. **Tracking requirements?** Real-time + alerts?

## Recommended Response

### Vehicle Assignment

1. Assign [[Closed Body Vehicle]] ONLY
2. Verify vehicle has:
   - Tamper-proof container
   - GPS tracking
   - No rear opening option
3. Prefer known, reliable drivers

### Security Protocol

```
1. DRIVER_CHECK:
   - Minimum 3 years experience
   - No prior theft claims
   - Verified identity

2. ROUTE_SELECTION:
   - Prefer NH routes
   - Avoid night travel if possible
   - Minimize state borders

3. TRACKING:
   - 15-minute location updates
   - Geofence alerts
   - Driver check-in requirement

4. INSURANCE:
   - Confirm cargo insurance
   - Note declared value
   - Document condition at pickup
```

## Risks

| Risk | Mitigation |
|------|------------|
| Theft | Secure vehicle + tracking |
| Damage | Proper packaging + handling |
| Delay | Buffer time + backup plan |
| Insurance claim | Complete documentation |

## Related SOPs

- [[SOP - Assign Secure Vehicle]]
- [[SOP - Handle High Value Cargo]]
- [[SOP - Verify Shipment Documents]]

## Related Concepts

- [[Closed Body Vehicle]]
- [[Route Risk Scoring]]
- [[Proof of Delivery]]

## Related Algorithms

- [[Carrier Scoring Algorithm]]
- [[Load Matching Algorithm]]
