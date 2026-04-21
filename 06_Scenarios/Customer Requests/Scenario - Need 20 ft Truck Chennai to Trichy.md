---
type: scenario
domain: transport
urgency: medium
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
  - regional
---

# Scenario - Need 20 ft Truck Chennai to Trichy

## Situation

A customer (MSME manufacturer) needs to transport industrial equipment from Chennai to Trichy. Equipment is 2.5 tons, standard dimensions.

## Variables

| Variable | Value | Notes |
|----------|-------|-------|
| Cargo weight | 2.5 tons | Within HCV capacity |
| Required vehicle | 20 ft truck | HCV or Container |
| Distance | ~320 km | NH+SH route |
| Timeline | Flexible | Normal delivery ok |
| Special handling | None | Standard equipment |

## Decision Questions

1. **Which vehicle type?** 20 ft truck vs container vs part load?
2. **Own fleet or partner?** Available capacity check
3. **Route selection?** NH-32 + NH-83 or alternative
4. **Pricing?** Distance-based vs negotiated?

## Recommended Response

### If Own Fleet Available

1. Assign 20 ft HCV or container vehicle
2. Optimize with return load opportunity
3. Apply standard [[Dynamic Pricing Logic]]
4. ETA: 6-8 hours

### If Partner Fleet Required

1. Use [[Load Matching Algorithm]] for partner
2. Verify partner vehicle certification
3. Apply [[Carrier Scoring Algorithm]] check
4. ETA: 8-10 hours (additional buffer)

## Risks

| Risk | Mitigation |
|------|------------|
| No 20 ft vehicle available | Offer container as alternative |
| Route congestion | Allow buffer time |
| Partner vehicle delay | Real-time tracking + alerts |

## Related SOPs

- [[SOP - New Shipment Booking]]
- [[SOP - Assign Vehicle to Order]]
- [[SOP - Handle Partner Transporter]]

## Related Concepts

- [[LCV vs MCV vs HCV]]
- [[Fleet Utilization]]
- [[Closed Body Vehicle]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Dynamic Pricing Logic]]
- [[Route Risk Scoring]]
