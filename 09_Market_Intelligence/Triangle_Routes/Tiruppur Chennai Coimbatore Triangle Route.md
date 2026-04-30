---
type: triangle_route
triangle_id: TRI-TUP-CHN-CBE
city_a: Tiruppur
city_b: Chennai
city_c: Coimbatore
primary_lane: Tiruppur -> Chennai
weak_return_lane: Chennai -> Tiruppur
substitute_leg_1: Chennai -> Coimbatore
substitute_leg_2: Coimbatore -> Tiruppur
vehicle_type: LCV/MCV/closed-body
target_industry: textiles
expected_empty_km_reduction: validate
expected_revenue_gain: validate
time_penalty: medium
payment_risk: medium
vehicle_fit_risk: medium
triangle_score: 82
data_confidence: medium
status: validate
tags:
  - triangle-route
  - backhaul
  - textiles
  - tamil-nadu
  - validate
---

# Triangle Route: Tiruppur -> Chennai -> Coimbatore -> Tiruppur

## Logic

Tiruppur to Chennai has frequent textile/export shipments.

Chennai to Tiruppur appears weaker as a direct return lane.

Instead of waiting only for Chennai -> Tiruppur cargo, redirect the truck to Coimbatore and then use the short Coimbatore -> Tiruppur textile cluster movement.

## Route Legs

| Leg | Direction | Cargo Hypothesis | Strength |
| --- | --- | --- | --- |
| 1 | Tiruppur -> Chennai | garments, textiles, export cargo | strong |
| 2 | Chennai -> Coimbatore | FMCG, retail, machinery, raw material | medium/high |
| 3 | Coimbatore -> Tiruppur | yarn, fabric, textile inputs | high/short |

## Triangle Decision

Use this triangle when:

- Chennai -> Tiruppur direct load is unavailable within 6-12 hours
- Chennai -> Coimbatore load is available
- Coimbatore -> Tiruppur has same-day or next-day feeder load
- added time is acceptable
- driver has enough working time
- vehicle type fits all cargo legs

## Risks

| Risk | Control |
| --- | --- |
| cargo mismatch | vehicle-fit check |
| waiting time in Chennai | slot booking and max wait rule |
| low Coimbatore-Tiruppur rate | bundle with return contract |
| payment delay | verified customer or advance |
| driver fatigue | time-window constraint |

## Validation Tasks

- [ ] Collect Chennai -> Coimbatore load postings for 14 days
- [ ] Collect Chennai -> Tiruppur direct load postings for 14 days
- [ ] Compare rate per km
- [ ] Interview 10 textile transporters
- [ ] Test with 5 vehicles manually
- [ ] Compare revenue per vehicle day

## Related Notes

- [[Triangle Route Engine for Return Trip Optimization]]
- [[South India City Pair Master]]
- [[Coimbatore <-> Tiruppur]]
- [[Tiruppur <-> Chennai Port]]
