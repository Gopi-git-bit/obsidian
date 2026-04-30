---
title: Triangle Route Template
type: template
category: backhaul-optimization
status: active
---

# Triangle Route Template

```yaml
type: triangle_route
triangle_id:
city_a:
city_b:
city_c:
primary_lane:
weak_return_lane:
substitute_leg_1:
substitute_leg_2:
vehicle_type:
target_industry:
expected_empty_km_reduction:
expected_revenue_gain:
time_penalty:
payment_risk:
vehicle_fit_risk:
triangle_score:
data_confidence:
status:
```

# Triangle Route: {{city_a}} -> {{city_b}} -> {{city_c}} -> {{city_a}}

## Logic


## Route Legs

| Leg | Direction | Cargo Hypothesis | Strength |
| --- | --- | --- | --- |
| 1 | city_a -> city_b |  |  |
| 2 | city_b -> city_c |  |  |
| 3 | city_c -> city_a |  |  |

## Direct Return Comparison

| Option | Revenue | Cost | Empty Km | Cycle Time | Revenue / Vehicle Day |
| --- | ---: | ---: | ---: | ---: | ---: |
| Direct return |  |  |  |  |  |
| Triangle |  |  |  |  |  |

## Triangle Decision

Use this triangle when:

- direct return load is unavailable within allowed wait window
- substitute leg load is available
- feeder leg back to origin cluster is short or high-frequency
- added time is acceptable
- driver has enough working time
- vehicle type fits all cargo legs

## Risks

| Risk | Control |
| --- | --- |
| cargo mismatch | vehicle-fit check |
| waiting time | slot/waiting window rule |
| low feeder rate | bundle with return contract |
| payment delay | verified customer/advance |
| driver fatigue | time-window constraint |

## Evidence Log

| Claim | Type | Source | Confidence |
| --- | --- | --- | --- |
|  |  |  |  |

## Validation Tasks

- [ ] Collect direct return load postings for 14 days
- [ ] Collect substitute leg load postings for 14 days
- [ ] Compare rate per km
- [ ] Interview 10 transporters
- [ ] Test with 5 vehicles manually
- [ ] Compare revenue per vehicle day

## Related Lanes

- [[{{primary_lane}}]]
- [[{{weak_return_lane}}]]
- [[{{substitute_leg_1}}]]
- [[{{substitute_leg_2}}]]
