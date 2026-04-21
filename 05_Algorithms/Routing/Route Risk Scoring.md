---
type: algorithm
domain: routing
decision_value: medium
inputs:
  - route
  - time_of_day
  - cargo_type
  - vehicle_type
outputs:
  - risk_score
  - risk_factors
  - recommended_actions
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
tags:
  - algorithm
  - routing
  - risk
---

# Route Risk Scoring

## Purpose

Assess and score potential risks for a given route to enable informed assignment decisions.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| route | Object | Origin, destination, waypoints |
| time_of_day | Enum | Morning/Afternoon/Night |
| cargo_type | String | Category of goods |
| vehicle_type | Enum | Vehicle classification |

## Logic

```
1. INFRASTRUCTURE_RISK:
   - Road type (NH/SH/Others)
   - Construction zones
   - Known bottlenecks

2. SECURITY_RISK:
   - Region crime data
   - Time-of-day factor
   - Cargo value sensitivity

3. WEATHER_RISK:
   - Seasonal patterns
   - Recent weather events
   - Flood-prone areas

4. REGULATORY_RISK:
   - Check post frequency
   - State border delays
   - Time restrictions

5. TRAFFIC_RISK:
   - City vs highway
   - Peak hour impact
   - Known congestion

6. FINAL_SCORE = weighted_sum / max_possible × 100
```

### Default Weights

- Infrastructure: 0.25
- Security: 0.20
- Weather: 0.15
- Regulatory: 0.15
- Traffic: 0.25

## Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-30 | Low | Standard monitoring |
| 31-60 | Medium | Enhanced tracking |
| 61-80 | High | Additional precautions |
| 81-100 | Critical | Reroute or decline |

## Risk Factors Detail

### Infrastructure Risks
- Single-lane roads
- Unpaved sections
- Bridge weight limits
- Toll booth delays

### Security Risks
- Night travel in rural areas
- High-value cargo routes
- Known theft-prone areas

### Weather Risks
- Monsoon flooding
- Fog in North India
- Heat impact on vehicles

## Related Notes

- [[Route Optimization Logic]]
- [[Return Load Optimization]]
- [[Scenario - Route Blocked Due to Protests]]
