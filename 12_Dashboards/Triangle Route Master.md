---
title: Triangle Route Master
type: dashboard
category: backhaul-optimization
status: active
region: South India
created: 2026-04-30
tags:
  - dashboard
  - triangle-route
  - backhaul
  - return-trip
  - empty-km
related:
  - Triangle Route Engine for Return Trip Optimization
  - South India City Pair Master
---

# Triangle Route Master

## Purpose

Track candidate triangle routes where direct return freight is weak but an alternate city C can create a better continuous-load loop.

The operating question:

```text
Should this vehicle return directly, wait, or move through a better demand node?
```

---

# Starter Triangle Table

| Triangle | Primary Lane | Weak Return | Substitute Return | Score | Status |
| --- | --- | --- | --- | ---: | --- |
| Tiruppur -> Chennai -> Coimbatore -> Tiruppur | TUP->CHN | CHN->TUP | CHN->CBE->TUP | 82 | validate |
| Erode -> Chennai -> Coimbatore -> Erode | ERD->CHN | CHN->ERD | CHN->CBE->ERD | 76 | validate |
| Salem -> Chennai -> Coimbatore -> Salem | SLM->CHN | CHN->SLM | CHN->CBE->SLM | 72 | validate |
| Bengaluru -> Sri City -> Chennai -> Bengaluru | BLR->SRI | SRI->BLR | SRI->CHN->BLR | 78 | validate |
| Chennai -> Madurai -> Coimbatore -> Chennai | CHN->MDU | MDU->CHN | MDU->CBE->CHN | 65 | watchlist |

---

# Triangle Score Formula

```text
Triangle Score =
0.25 x Revenue Gain
+ 0.25 x Empty Km Reduction
+ 0.20 x Load Availability
+ 0.15 x Time Feasibility
+ 0.10 x Operational Simplicity
+ 0.05 x Payment Reliability
```

---

# Decision Rule

| Score | Decision |
| ---: | --- |
| 85-100 | launch immediately |
| 70-84 | validate with transporters |
| 55-69 | occasional use |
| below 55 | avoid |

---

# Dataview: Triangle Routes

```dataview
TABLE city_a, city_b, city_c, primary_lane, weak_return_lane, triangle_score, status
FROM "09_Market_Intelligence/Triangle_Routes"
WHERE type = "triangle_route"
SORT triangle_score DESC
```

# Dataview: Validate Next

```dataview
TABLE city_a, city_b, city_c, triangle_score, data_confidence, status
FROM "09_Market_Intelligence/Triangle_Routes"
WHERE status = "validate"
SORT triangle_score DESC
```

---

# Manual Validation Rhythm

```text
For 14 days:
1. Track direct return load availability.
2. Track substitute leg load availability.
3. Track rate/km.
4. Track wait hours.
5. Estimate empty km saved.
6. Compare revenue per vehicle day.
```

Promote only if:

```text
Revenue per vehicle day improves by 15-20 percent
AND driver accepts the loop
AND payment risk is manageable
AND cargo/vehicle fit is clean
```
