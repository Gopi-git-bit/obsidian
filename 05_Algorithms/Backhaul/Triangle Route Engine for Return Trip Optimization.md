---
title: Triangle Route Engine for Return Trip Optimization
type: algorithm-framework
category: backhaul-optimization
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - backhaul
  - return-trip
  - triangle-route
  - empty-km
  - vehicle-routing
  - south-india
related:
  - South India Tier 2-3 City Pair Freight Atlas Framework
  - South India City Pair Master
  - Return Load Optimization
  - Hub-Aware Return Trip Matching
  - AI Intermodal Freight Optimizer Framework
---

# Triangle Route Engine for Return Trip Optimization

## Core Idea

Return-trip optimization should not mean only:

```text
Find load from B back to A.
```

The stronger strategy is:

```text
Find the most profitable route chain from B through C back toward A.
```

This is a triangular backhaul strategy.

It belongs to the practical family of:

- vehicle routing with backhauls
- pickup and delivery problems
- minimum empty-mile routing
- trip chaining
- continuous move optimization
- backhaul profit maximization

## Main Insight

If:

```text
A -> B is strong
B -> A is weak
```

Then do not force a direct return.

Search for a nearby demand node C:

```text
A -> B -> C -> A
```

The goal is not just lower empty kilometers.

The real goal is:

```text
higher revenue per vehicle per day
```

Tiny triangle. Big margin claw.

---

# 1. Example: Tiruppur, Chennai, Coimbatore

## Direct Return Model

```text
Tiruppur -> Chennai = strong loaded lane
Chennai -> Tiruppur = weak return lane
```

## Triangle Model

```text
Tiruppur -> Chennai -> Coimbatore -> Tiruppur
```

## Why It May Work

| Leg | Cargo Hypothesis | Strength |
| --- | --- | --- |
| Tiruppur -> Chennai | garments, textiles, export cargo | strong |
| Chennai -> Coimbatore | FMCG, retail, machinery, raw materials | medium/high |
| Coimbatore -> Tiruppur | yarn, fabric, textile inputs | high/short |

Instead of waiting for a weak Chennai -> Tiruppur direct load, the vehicle moves through Coimbatore, where Coimbatore -> Tiruppur is a short cluster lane.

---

# 2. Directed Lane Principle

Do not store only bidirectional city pairs.

Store directional lanes.

```text
Tiruppur -> Chennai
Chennai -> Tiruppur
```

Because freight demand is asymmetric.

A lane can be strong in one direction and weak in the opposite direction.

## Directed Lane Example

```yaml
type: directed_lane
origin: Tiruppur
destination: Chennai
distance_km: 450
volume_score: 9
rate_score: 8
backhaul_score: 4
cargo_types:
  - garments
  - textiles
lane_strength: strong
seasonality: export_peak
data_confidence: medium
```

Opposite direction:

```yaml
type: directed_lane
origin: Chennai
destination: Tiruppur
distance_km: 450
volume_score: 4
rate_score: 5
backhaul_score: 3
cargo_types:
  - retail_goods
  - raw_materials
lane_strength: weak
data_confidence: low
```

## Rule

```text
If the database stores only Chennai <-> Tiruppur, it will hide directional imbalance.
```

That is how a clean table lies politely.

---

# 3. Triangle Definition

```text
A -> B = primary paid shipment
B -> C = substitute return-side paid shipment
C -> A = feeder return into origin cluster
```

## South India Meaning

| Route Type | Meaning | Example |
| --- | --- | --- |
| Primary linehaul | high-volume outward lane | Tiruppur -> Chennai |
| Weak direct return | low cargo back to origin | Chennai -> Tiruppur |
| Nearby demand node | stronger return-side market | Coimbatore |
| Feeder return | short movement back to origin cluster | Coimbatore -> Tiruppur |

## Search Rule

```text
If B -> A is weak,
find C near A or near B
where B -> C has stronger demand
and C -> A is short or high-frequency.
```

---

# 4. Triangle Candidate Formula

For each weak return lane:

```text
B -> A is weak
```

Test:

```text
B -> C + C -> A
```

against:

```text
B -> A
```

## Triangle Profit

```text
Triangle Profit =
Revenue_AB + Revenue_BC + Revenue_CA
- Cost_AB - Cost_BC - Cost_CA
- Waiting_Cost
- Detour_Cost
```

## Direct Round Trip Profit

```text
Direct Round Trip Profit =
Revenue_AB + Revenue_BA
- Cost_AB - Cost_BA
```

## Choose Triangle If

```text
Triangle Profit > Direct Round Trip Profit
```

and

```text
Triangle Empty Km < Direct Empty Km
```

and

```text
Revenue per Vehicle Day improves
```

---

# 5. Triangle Score

```text
Triangle Score =
0.25 x Revenue Gain
+ 0.25 x Empty Km Reduction
+ 0.20 x Load Availability
+ 0.15 x Time Feasibility
+ 0.10 x Operational Simplicity
+ 0.05 x Payment Reliability
```

## Score Meaning

| Score | Decision |
| ---: | --- |
| 85-100 | launch triangle immediately |
| 70-84 | validate with transporters |
| 55-69 | use occasionally |
| below 55 | avoid |

---

# 6. Revenue Per Vehicle Day

Do not optimize only distance.

Optimize:

```text
Revenue per Vehicle Day =
Total Revenue in Route Cycle / Total Cycle Time in Days
```

## Example: Direct Return

```text
Tiruppur -> Chennai loaded = INR 30,000
Chennai -> Tiruppur weak return = INR 5,000
Cycle time = 2 days

Revenue per vehicle day = 35,000 / 2 = INR 17,500
```

## Example: Triangle

```text
Tiruppur -> Chennai loaded = INR 30,000
Chennai -> Coimbatore loaded = INR 24,000
Coimbatore -> Tiruppur short loaded = INR 4,000
Cycle time = 2.5 days

Revenue per vehicle day = 58,000 / 2.5 = INR 23,200
```

Triangle wins.

But if the triangle takes 4 days:

```text
58,000 / 4 = INR 14,500
```

Direct wins.

## Rule

```text
A longer triangle is useful only if extra revenue beats extra time, waiting, and driver fatigue.
```

---

# 7. Backhaul Search Windows

After delivery at B, search for the best next paid leg within a time window.

| Waiting Window | Use |
| --- | --- |
| 0-3 hours | premium/urgent truck |
| 3-6 hours | normal return |
| 6-12 hours | acceptable if strong load |
| 12-24 hours | only if high revenue |
| 24+ hours | usually avoid unless contract load |

## Rule

```text
Do not wait 18 hours for a return load unless the load pays more than waiting cost plus missed opportunity cost.
```

---

# 8. Algorithm 1: Simple Triangle Search

## Inputs

```text
Origin city A
Destination city B
Weak return lane B -> A
Candidate nearby cities C
Distance matrix
Lane volume scores
Lane rate scores
Vehicle type
Time limit
```

## Pseudocode

```text
For every completed trip A -> B:

    Check direct return lane B -> A

    If direct return load exists with good rate:
        choose B -> A

    Else:
        Find candidate cities C within radius of A or B

        For each C:
            calculate:
                revenue_BC
                revenue_CA
                cost_BC
                cost_CA
                extra_distance
                expected_wait_time
                load_probability_BC
                load_probability_CA

            triangle_score =
                revenue_gain
                + empty_km_reduction
                + load_probability
                - detour_penalty
                - waiting_penalty

        Select best C

    Recommend:
        B -> C -> A
```

## Candidate City Filter

Only test C if:

```text
C is within 50-150 km of A
OR B -> C is a known high-volume lane
OR C -> A is short/high-frequency
AND vehicle can carry cargo on all legs
AND time window is feasible
```

---

# 9. Algorithm 2: Directed Lane Strength Matrix

Example matrix:

| From / To | Chennai | Tiruppur | Coimbatore | Erode | Salem |
| --- | ---: | ---: | ---: | ---: | ---: |
| Chennai | - | 8 | 8 | 4 | 4 |
| Tiruppur | 9 | - | 8 | 7 | 6 |
| Coimbatore | 7 | 9 | - | 7 | 6 |
| Erode | 6 | 7 | 6 | - | 6 |
| Salem | 7 | 6 | 6 | 6 | - |

If:

```text
Chennai -> Erode = 4
Chennai -> Coimbatore = 8
Coimbatore -> Erode = 7
```

Then:

```text
Chennai -> Coimbatore -> Erode
```

may beat:

```text
Chennai -> Erode
```

## Matrix Rule

```text
If direct return lane score < 5,
search two-leg return paths with combined score > 12.
```

---

# 10. Algorithm 3: Minimum Empty Km With Revenue Constraint

Goal:

```text
Minimize EmptyKm
```

But not blindly.

Because a low-rate long detour can look good on empty-km but bad on profit.

Better goal:

```text
Maximize Revenue per Vehicle Day
```

## Decision Formula

```text
If Revenue_per_vehicle_day_triangle > Revenue_per_vehicle_day_direct
AND Empty_km_triangle < Empty_km_direct
AND Wait_hours < max_wait_limit
THEN choose triangle
ELSE choose direct return
```

---

# 11. Algorithm 4: Time-Window Backhaul Matching

For each vehicle after delivery:

```text
current_city = B
home_cluster = A
search_window = 6/12/24 hours
```

Find loads that satisfy:

```text
pickup_time <= search_window
vehicle_fit = true
payment_risk acceptable
cargo_compatibility = true
driver_time feasible
```

Then rank by:

```text
expected_profit
revenue_per_vehicle_day
empty_km_saved
load_probability
payment_reliability
```

---

# 12. First South India Triangle Candidates

| Triangle | Primary Lane | Weak Return | Substitute Return | Score | Status |
| --- | --- | --- | --- | ---: | --- |
| Tiruppur -> Chennai -> Coimbatore -> Tiruppur | TUP->CHN | CHN->TUP | CHN->CBE->TUP | 82 | validate |
| Erode -> Chennai -> Coimbatore -> Erode | ERD->CHN | CHN->ERD | CHN->CBE->ERD | 76 | validate |
| Salem -> Chennai -> Coimbatore -> Salem | SLM->CHN | CHN->SLM | CHN->CBE->SLM | 72 | validate |
| Bengaluru -> Sri City -> Chennai -> Bengaluru | BLR->SRI | SRI->BLR | SRI->CHN->BLR | 78 | validate |
| Chennai -> Madurai -> Coimbatore -> Chennai | CHN->MDU | MDU->CHN | MDU->CBE->CHN | 65 | watchlist |

---

# 13. Data To Collect For Every Directional Lane

| Field | Why Needed |
| --- | --- |
| daily load posts | volume signal |
| rate per km | revenue |
| average waiting time | time cost |
| cargo type | vehicle fit |
| vehicle type needed | matching |
| loading point density | pickup ease |
| unloading delay | demurrage risk |
| payment reliability | cash flow |
| backhaul availability | return planning |
| seasonality | forecasting |

---

# 14. 14-Day Manual Validation Experiment

Choose 3 triangles first:

```text
1. Tiruppur -> Chennai -> Coimbatore -> Tiruppur
2. Erode -> Chennai -> Coimbatore -> Erode
3. Bengaluru -> Sri City -> Chennai -> Bengaluru
```

For 14 days, record:

| Metric | Target |
| --- | ---: |
| direct return load availability | count/day |
| triangle leg load availability | count/day |
| rate/km for each leg | collect |
| average wait time | collect |
| empty km saved | estimate |
| revenue per vehicle day | compare |
| driver acceptance | interview |
| payment speed | track |

## Improvement Formula

```text
Triangle Improvement =
Triangle Revenue per Vehicle Day
- Direct Return Revenue per Vehicle Day
```

If improvement is above 15-20 percent, the triangle is worth operationalizing.

---

# 15. MVP Spreadsheet Columns

```text
Truck ID
Current city
Home cluster
Last delivery city
Direct return city
Direct return load score
Candidate city C
B->C load score
C->A load score
Extra km
Expected wait hours
Revenue direct
Revenue triangle
Empty km direct
Empty km triangle
Revenue per vehicle day direct
Revenue per vehicle day triangle
Recommendation
```

## Spreadsheet Decision Rule

```text
If Revenue_per_vehicle_day_triangle > Revenue_per_vehicle_day_direct
AND Empty_km_triangle < Empty_km_direct
AND Wait_hours < max_wait_limit
THEN choose triangle
ELSE choose direct return
```

This spreadsheet is the first AI.

No glitter, but it may actually make money.

---

# 16. Advanced Model Roadmap

| Stage | Model | Use |
| --- | --- | --- |
| MVP | rule-based scoring | fast manual decisions |
| Stage 2 | greedy heuristic | pick best nearby return city |
| Stage 3 | mixed integer programming | optimize fleet-wide routing |
| Stage 4 | machine learning | predict best future backhaul |
| Stage 5 | real-time marketplace | automatically chain trips |

Do not start with advanced optimization.

Start with lane matrix plus greedy triangle search.

---

# 17. Final Strategic Positioning

The product is not only backhaul matching.

It is:

```text
Continuous-load routing for regional freight clusters.
```

The wedge can be:

```text
Triangle Route Engine for MSME freight.
```

Start with:

```text
Tiruppur
Coimbatore
Erode
Salem
Chennai
Bengaluru
Sri City
Madurai
Tuticorin
```

Score every triangle by:

```text
empty km saved
extra revenue
load probability
waiting time
vehicle fit
payment reliability
```

If even one triangle improves revenue per vehicle day by 15-20 percent, it is not just a clever map scribble.

It is an operating advantage.

---

# Source Links

- [Vehicle routing with backhauls: Review and research perspectives - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0305054817302794)
- [Practical and Effective Heuristics for the Backhaul Profit Maximization Problem - Springer Nature](https://link.springer.com/article/10.1007/s11067-025-09684-0)
- [[South India Tier 2-3 City Pair Freight Atlas Framework]]
- [[South India City Pair Master]]
- [[Return Load Optimization]]
- [[Hub-Aware Return Trip Matching]]
