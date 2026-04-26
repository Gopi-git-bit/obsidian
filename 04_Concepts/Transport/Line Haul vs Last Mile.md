---
type: concept
domain: transport
decision_value: medium
status: evergreen
related_hubs:
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - concept
  - transport
---

# Line Haul vs Last Mile

## Line Haul

### Definition
Long-distance transportation between major hubs/cities, typically over 200 km.

### Characteristics

| Aspect | Line Haul |
|--------|-----------|
| Distance | 200-1500+ km |
| Vehicle | HCV, trailers |
| Route | Highway-focused |
| Time | 4-24+ hours |
| Complexity | Moderate |
| Customer | B2B primarily |

### Key Metrics
- Per-km cost efficiency
- Fuel optimization
- Route straightness
- Load consolidation

## Last Mile

### Definition
Final leg of delivery from local hub to end recipient, typically under 50 km.

### Characteristics

| Aspect | Last Mile |
|--------|-----------|
| Distance | 5-50 km |
| Vehicle | LCV, bikes |
| Route | Urban/rural |
| Time | 1-4 hours |
| Complexity | High |
| Customer | B2C, retail |

### Key Metrics
- Delivery success rate
- First-attempt success
- Time windows honored
- Cost per delivery
- Failed delivery rate
- Cost per successful delivery
- Stop density per route
- ETA accuracy and notification response rate

## Comparison

| Factor | Line Haul | Last Mile |
|--------|-----------|-----------|
| Cost per km | Low | High |
| Cost per delivery | N/A | High |
| Volume efficiency | High | Low |
| Customer proximity | Indirect | Direct |
| Failure impact | Moderate | High |
| Tech needs | GPS, tracking | Real-time, routing |

## Hybrid Operations

### Hub-and-Spoke Model

```
Shipper → [Line Haul] → Regional Hub → [Last Mile] → Recipient
```

### Why It Matters

- Different skill sets required
- Different vehicle types
- Different pricing models
- Different SLA expectations
- Different failure economics: one bad address or absent consignee can erase the margin of a route
- Different customer impact: last-mile experience shapes trust more directly than upstream movement

## Decision Impact

- [[Load Matching Algorithm]] must consider leg type
- [[Fleet Utilization]] calculation differs
- [[Dynamic Pricing Logic]] varies by leg
- [[Route Optimization Logic]] must use delivery windows, stop density, consignee availability, and failed-attempt risk for last-mile routes
- [[Delivery Attempt Management]] should be treated as a control layer, not only a driver task

## Related Notes

- [[LCV vs MCV vs HCV]]
- [[Fleet Utilization]]
- [[Return Load Economics]]
- [[Last-Mile Delivery Execution]]
- [[Delivery Attempt Management]]
- [[Failed Delivery Handling]]
