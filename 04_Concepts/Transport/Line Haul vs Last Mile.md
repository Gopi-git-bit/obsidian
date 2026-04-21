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

## Decision Impact

- [[Load Matching Algorithm]] must consider leg type
- [[Fleet Utilization]] calculation differs
- [[Dynamic Pricing Logic]] varies by leg

## Related Notes

- [[LCV vs MCV vs HCV]]
- [[Fleet Utilization]]
- [[Return Load Economics]]
