---
type: algorithm
domain: routing
decision_value: high
inputs:
  - origin
  - destination
  - waypoints
  - vehicle_type
  - traffic_conditions
outputs:
  - optimal_route
  - estimated_time
  - fuel_cost
  - routing_strategy
  - route_trace
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
tags:
  - algorithm
  - routing
---

# Route Optimization Logic

## Purpose

Calculate optimal routes considering distance, time, traffic, road conditions, vehicle characteristics, and return-load opportunity.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| origin | Location | Start point (lat/long) |
| destination | Location | End point (lat/long) |
| waypoints | Array | Intermediate stops |
| vehicle_type | Enum | LCV/MCV/HCV |
| traffic_conditions | Enum | Light/Medium/Heavy |

## Logic

```text
1. CLASSIFY routing problem:
   - single-stop or single-vehicle loop -> TSP-style search
   - multi-stop or multi-vehicle -> VRP / VRPTW
   - dynamic rerouting under disruption -> ACO / tabu-style repair

2. GENERATE candidate routes:
   - Shortest distance
   - Fastest time
   - Highway preference
   - Avoid tolls option
   - Open-route or backhaul-aware option for return economics

3. CALCULATE route metrics:
   - Total distance (km)
   - Estimated time (hours)
   - Fuel consumption estimate
   - Toll costs (if applicable)
   - Road quality / route difficulty score
   - Return-load potential

4. WEIGHT routes by priority:
   - Time-sensitive: Prioritize fastest and ETA confidence
   - Cost-sensitive: Prioritize fuel efficiency and toll control
   - Cargo-sensitive: Prioritize road quality and handling safety
   - Utilization-sensitive: Prioritize backhaul and open-route fit

5. SELECT optimal route and label the routing strategy used
```

## Production Guardrails

- Treat routing output as recommendation data, not a state transition.
- Include `trace_id`, `idempotency_key`, and routing agent identity in responses.
- Use truck-aware runtime routing before falling back to static route engines.
- Keep route-difficulty penalties bounded so they tune, but do not replace, hard feasibility logic.
- Keep ETA prediction layered: deterministic baseline first, then live penalties, then optional ML correction.

## Recommended Algorithm Stack

| Routing Need | Best-Fit Family | Why |
|--------------|-----------------|-----|
| Simple intra-city loop | TSP heuristic | Fast for low-complexity routing |
| Multi-vehicle dispatch | VRP / VRPTW | Handles capacity and time windows |
| Dynamic disruption recovery | ACO or Tabu Search | Useful for rerouting after traffic or breakdowns |
| Complex optimization with many tradeoffs | Genetic Algorithm hybrid | Flexible with capacity, packing, and return legs |
| Predictive ETA and adaptive routing | ML-assisted routing | Improves confidence on noisy corridors |
| Truck-aware production routing | Valhalla + optimizer | Handles truck profiles and runtime costing |
| Confidence-scored ETA | [[ETA Prediction Logic]] | Adds explainability and uncertainty bounds |

## Decision Rules

| Vehicle Type | Highway Preference | Speed Limit |
|-------------|-------------------|-------------|
| LCV | Medium | 80 km/h |
| MCV | High | 70 km/h |
| HCV | Very High | 60 km/h |

## India-Specific Considerations

- Add buffers for congestion, variable road quality, and checkpoint friction.
- Penalize corridors with weak reload density when deadhead risk is high.
- Feed route difficulty into pricing and assignment decisions, not just navigation.
- Preserve OMS control over lifecycle transitions even when routing confidence is high.
- Use confidence intervals for customer promises on volatile corridors rather than single-point ETA only.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No route found | Return nearest alternative |
| Waypoint unreachable | Skip and warn |
| Heavy traffic | Add 50% time buffer |
| Low-confidence ETA | Switch to conservative route and escalate |
| Return leg likely empty | Check [[Return Load Optimization]] before final route commit |

## Related Notes

- [[Multi-stop Route Planning]]
- [[Route Risk Scoring]]
- [[Unified Routing & Optimization Algorithm]]
- [[ETA Prediction Logic]]
- [[Return Load Optimization]]
- [[Return Load Economics]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
