---
title: Quad Route Template
type: template
category: backhaul-optimization
status: active
---

# Quad Route Template

```yaml
type: quad_route
city_a:
city_b:
city_c:
city_d:
route_chain:
primary_lane:
weak_return_problem:
expected_empty_km_reduction_pct:
expected_revenue_lift_pct:
total_cycle_time_hours:
risk_score:
quad_score:
status:
```

# Quad Route: {{city_a}} -> {{city_b}} -> {{city_c}} -> {{city_d}} -> {{city_a}}

## Logic


## Route Legs

| Leg | Direction | Cargo Hypothesis | Strength |
| --- | --- | --- | --- |
| 1 | city_a -> city_b |  |  |
| 2 | city_b -> city_c |  |  |
| 3 | city_c -> city_d |  |  |
| 4 | city_d -> city_a |  |  |

## Score

```text
Quad Route Score =
0.25 x Total Revenue
+ 0.20 x Empty Km Reduction
+ 0.20 x Load Probability
+ 0.15 x Time Feasibility
+ 0.10 x Vehicle Compatibility
+ 0.10 x Payment Reliability
```

## Risks

| Risk | Control |
| --- | --- |
| added cycle time | max route time constraint |
| cargo mismatch | vehicle-fit check |
| weak leg | minimum load probability threshold |
| payment delay | payment reliability threshold |

## Validation Tasks

- [ ] Collect load data for each leg
- [ ] Estimate total cycle time
- [ ] Compare with direct return baseline
- [ ] Check driver acceptance
- [ ] Score and decide
```
