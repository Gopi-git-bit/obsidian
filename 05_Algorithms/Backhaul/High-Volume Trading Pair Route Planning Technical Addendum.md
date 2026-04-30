---
title: High-Volume Trading Pair Route Planning Technical Addendum
type: technical-implementation
category: corridor-intelligence
status: draft
region: South India
created: 2026-04-30
tags:
  - logistics
  - trading-pairs
  - directed-lanes
  - tier-scoring
  - postgis
  - corridor-priority
  - route-planning
related:
  - South India Trading Pair City Research System
  - Directed Lane Master
  - Triangle Backhaul Technical Implementation Addendum
  - Triangle Route Engine for Return Trip Optimization
  - South India City Pair Master
---

# High-Volume Trading Pair Route Planning Technical Addendum

## Purpose

This note extracts the valid technical points from the Qwen high-volume trading-pair framework and adapts them to the existing South India corridor intelligence system.

The useful addition is:

```text
Before searching for triangle backhauls,
rank directed lanes by tier-weighted commercial potential.
```

The route-planning stack should become:

```text
City nodes
-> directed lanes
-> tier-weighted corridor score
-> weak-return detection
-> triangle candidate search
-> 14-day validation
-> active route rule
```

---

# 1. Valid Qwen Takeaways To Keep

| Idea | Keep? | Optimized Use |
| --- | --- | --- |
| Directional demand beats bidirectional assumptions | Yes | Already core to Directed Lane Master |
| Tier 2/3 bonus in corridor scoring | Yes | Useful for startup wedge selection |
| Seasonality in lane schema | Yes | Important for textiles, agri, seafood, festivals |
| Last updated / idempotency key | Yes | Useful for data freshness and dedupe |
| Corridor priority thresholds | Yes | Launch, validate, watchlist, deprioritize |
| PostGIS ranking query | Yes, but corrected | Useful after city_nodes and directed_lanes exist |
| n8n recommendation flow | Yes | Good dispatcher workflow skeleton |
| Autoclaw/GSTN scraping | Delay | Access/legal/technical feasibility must be confirmed |
| WhatsApp/Telegram NLP parsing | Delay | Consent/privacy and data quality needed first |
| GLM/LLM decision node | Later | Use rule-based scoring first; LLM can summarize/extract later |

## Main Improvement To Add

The triangle engine starts with weak return lanes.

But we also need to find the best lanes to study first.

That requires a tier-weighted directed-lane score.

---

# 2. Directed Lane Schema Upgrade

Add these fields to directed lane notes and database rows.

```yaml
type: directed_lane
origin:
destination:
distance_km:
volume_score:
rate_score:
margin_score:
backhaul_score:
industry_fragmentation_score:
operational_ease_score:
tier_combination: T2->T1
seasonality:
  peak_months:
  factor:
cargo_types:
  -
lane_strength:
triangle_candidate:
data_confidence:
last_updated:
idempotency_key:
```

## Why These Fields Matter

| Field | CEO/Operator Use |
| --- | --- |
| volume_score | shows freight density |
| rate_score | shows willingness to pay |
| margin_score | avoids high-volume low-profit traps |
| backhaul_score | identifies return-trip opportunity |
| tier_combination | highlights Tier 2/3 wedge potential |
| seasonality | prevents mistaking peak demand for normal demand |
| idempotency_key | prevents duplicate observations during automated imports |

---

# 3. Tier-Weighted Corridor Score

Use this formula for high-volume trading-pair prioritization.

```text
Tier-Weighted Corridor Score =
0.30 x Volume Score
+ 0.25 x Margin Potential
+ 0.20 x Backhaul Opportunity
+ 0.15 x Tier 2/3 Presence
+ 0.10 x Industry Fragmentation
```

## Tier 2/3 Presence Score

| Tier Combination | Score |
| --- | ---: |
| T2 -> T1 or T1 -> T2 | 8 |
| T3 -> T1 or T1 -> T3 | 9 |
| T2 -> T2 | 10 |
| T2 -> T3 or T3 -> T2 | 10 |
| T1 -> T1 | 5 |

## Decision Thresholds

| Score | Decision |
| ---: | --- |
| >= 8.0 | launch/test now if operations are feasible |
| 6.5-7.9 | validate for 14 days |
| 5.0-6.4 | watchlist |
| below 5.0 | deprioritize |

## Important Rule

```text
A high corridor score does not automatically mean launch.
If payment risk, demurrage risk, or vehicle-fit risk is high, move to validation first.
```

---

# 4. Lane Strength Derivation

Use a simple formula first:

```text
Lane Strength Score =
0.60 x Volume Score
+ 0.40 x Rate Score
```

## Lane Strength Labels

| Score | Label |
| ---: | --- |
| 8.0-10 | strong |
| 6.0-7.9 | medium |
| below 6.0 | weak |

## Backhaul Flag

```text
If reverse lane strength < 6
OR reverse backhaul_score < 5,
mark triangle_candidate = true.
```

---

# 5. Corrected PostGIS Query: Top Tier 2/3 Directed Lanes

The Qwen query had the right idea, but the score expression should use real score columns and avoid referencing an alias inside the same SELECT.

```sql
WITH lane_base AS (
    SELECT
        dl.lane_id,
        origin.name AS origin,
        destination.name AS destination,
        origin.tier AS origin_tier,
        destination.tier AS destination_tier,
        dl.volume_score,
        dl.margin_score,
        dl.backhaul_score,
        dl.industry_fragmentation_score,
        dl.operational_ease_score,
        CASE
            WHEN origin.tier = 1 AND destination.tier = 1 THEN 5
            WHEN origin.tier IN (2, 3) OR destination.tier IN (2, 3) THEN 8
            WHEN origin.tier IN (2, 3) AND destination.tier IN (2, 3) THEN 10
            ELSE 5
        END AS tier_presence_score,
        dl.data_confidence
    FROM directed_lanes dl
    JOIN city_nodes origin ON origin.city_id = dl.origin_city_id
    JOIN city_nodes destination ON destination.city_id = dl.destination_city_id
    WHERE origin.region = 'South India'
      AND destination.region = 'South India'
      AND dl.data_confidence IN ('medium', 'high')
),
scored AS (
    SELECT
        *,
        ROUND(
            (volume_score * 0.30)
            + (margin_score * 0.25)
            + (backhaul_score * 0.20)
            + (tier_presence_score * 0.15)
            + (industry_fragmentation_score * 0.10),
            2
        ) AS corridor_score
    FROM lane_base
)
SELECT
    origin,
    destination,
    origin_tier,
    destination_tier,
    volume_score,
    margin_score,
    backhaul_score,
    tier_presence_score,
    industry_fragmentation_score,
    corridor_score,
    CASE
        WHEN corridor_score >= 8.0 AND backhaul_score >= 6 THEN 'LAUNCH_NOW'
        WHEN corridor_score >= 6.5 THEN 'VALIDATE_14D'
        WHEN corridor_score >= 5.0 THEN 'WATCHLIST'
        ELSE 'DEPRIORITIZE'
    END AS priority_flag
FROM scored
WHERE volume_score >= 5
ORDER BY corridor_score DESC
LIMIT 25;
```

## Note

If you want to prioritize triangle opportunities instead of stable launch corridors, invert the backhaul logic:

```text
High volume + weak reverse/backhaul = triangle opportunity.
High volume + strong backhaul = normal lane launch opportunity.
```

---

# 6. Query: Find Triangle Opportunities From Top Lanes

```sql
WITH top_outbound AS (
    SELECT
        dl.lane_id,
        dl.origin_city_id AS city_a_id,
        dl.destination_city_id AS city_b_id,
        origin.name AS city_a,
        destination.name AS city_b,
        dl.volume_score AS outbound_volume_score,
        dl.rate_score AS outbound_rate_score
    FROM directed_lanes dl
    JOIN city_nodes origin ON origin.city_id = dl.origin_city_id
    JOIN city_nodes destination ON destination.city_id = dl.destination_city_id
    WHERE dl.volume_score >= 7
      AND dl.rate_score >= 6
),
reverse_lane AS (
    SELECT
        t.*,
        rev.lane_id AS weak_return_lane_id,
        rev.backhaul_score AS reverse_backhaul_score,
        rev.volume_score AS reverse_volume_score
    FROM top_outbound t
    LEFT JOIN directed_lanes rev
        ON rev.origin_city_id = t.city_b_id
       AND rev.destination_city_id = t.city_a_id
    WHERE COALESCE(rev.backhaul_score, 0) < 5
),
candidate_cities AS (
    SELECT
        r.*,
        c.city_id AS city_c_id,
        c.name AS city_c
    FROM reverse_lane r
    JOIN city_nodes a ON a.city_id = r.city_a_id
    JOIN city_nodes b ON b.city_id = r.city_b_id
    JOIN city_nodes c ON c.city_id NOT IN (r.city_a_id, r.city_b_id)
    WHERE c.tier IN (2, 3)
      AND (
          ST_DWithin(c.geom, a.geom, 150000)
          OR ST_DWithin(c.geom, b.geom, 150000)
      )
)
SELECT
    city_a,
    city_b,
    city_c,
    outbound_volume_score,
    reverse_backhaul_score,
    bc.volume_score AS b_to_c_volume,
    ca.volume_score AS c_to_a_volume,
    (bc.volume_score + ca.volume_score) AS substitute_strength
FROM candidate_cities cc
JOIN directed_lanes bc
    ON bc.origin_city_id = cc.city_b_id
   AND bc.destination_city_id = cc.city_c_id
JOIN directed_lanes ca
    ON ca.origin_city_id = cc.city_c_id
   AND ca.destination_city_id = cc.city_a_id
WHERE bc.volume_score >= 6
  AND ca.volume_score >= 5
ORDER BY substitute_strength DESC
LIMIT 25;
```

---

# 7. Practical Data Source Policy

The Qwen source table is directionally useful, but it should be staged carefully.

## Source Maturity Levels

| Level | Source | MVP Use |
| --- | --- | --- |
| Level 1 | manual interviews, field notes, transporter calls | use immediately |
| Level 2 | public reports, port/rail/industry pages | use immediately |
| Level 3 | paid/public marketplace research | use after terms review |
| Level 4 | ULIP/GSTN/API data | use only after access and compliance review |
| Level 5 | WhatsApp/Telegram parsing | use only with consent/privacy controls |

## Rule

```text
Do not build an MVP that depends on data you do not legally and reliably control.
```

Start with manual lane observation and partner interviews.

Then automate.

---

# 8. n8n Corridor Scoring Workflow

## Workflow Name

```text
WF_CORRIDOR_01_score_directed_lanes
```

## Trigger

```text
daily schedule
or
new lane_observation inserted
```

## Steps

```text
1. Fetch lane observations from the last 14/30/90 days.
2. Aggregate load count, rate/km, wait time, and payment reliability.
3. Update directed_lanes score fields.
4. Calculate tier-weighted corridor score.
5. Flag lanes:
   - launch_now
   - validate_14d
   - watchlist
   - deprioritize
6. If reverse lane is weak, mark triangle_candidate = true.
7. Trigger WF_BACKHAUL_01_triangle_recommendation for triangle candidates.
8. Write decision summary to dashboard/event log.
```

## Output Payload

```json
{
  "lane_id": "UUID",
  "origin": "Tiruppur",
  "destination": "Chennai",
  "corridor_score": 8.3,
  "lane_strength_score": 8.6,
  "priority_flag": "LAUNCH_NOW",
  "reverse_backhaul_score": 3.0,
  "triangle_candidate": true,
  "recommended_next_workflow": "WF_BACKHAUL_01_triangle_recommendation",
  "reason_codes": [
    "high_volume",
    "tier2_to_tier1",
    "weak_reverse_lane",
    "textile_cluster"
  ]
}
```

---

# 9. Obsidian Dashboard Additions

Add this Dataview query to Directed Lane Master or Corridor Priority Dashboard.

## Top Launch Lanes

```dataview
TABLE origin, destination, tier_combination, volume_score, margin_score, backhaul_score, corridor_score, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane" AND corridor_score >= 8
SORT corridor_score DESC
```

## Triangle Candidate Lanes

```dataview
TABLE origin, destination, volume_score, backhaul_score, nearby_substitute_city, data_confidence, status
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane" AND triangle_candidate = true
SORT volume_score DESC
```

## Recently Updated Lanes

```dataview
TABLE origin, destination, lane_strength, data_confidence, last_updated
FROM "09_Market_Intelligence/Directed_Lanes"
WHERE type = "directed_lane"
SORT last_updated DESC
```

---

# 10. Quick-Start Implementation Plan

## This Week

1. Seed 25 city nodes with coordinates and tier classification.
2. Seed 30 directed lanes using existing city-pair and triangle notes.
3. Add seasonality and tier_combination to each high-priority directed lane.
4. Calculate tier-weighted corridor score manually first.
5. Mark weak reverse lanes as triangle candidates.
6. Select 3 triangles for 14-day validation.

## First 3 Route Systems

```text
1. Tiruppur -> Chennai -> Coimbatore -> Tiruppur
2. Erode -> Chennai -> Coimbatore -> Erode
3. Bengaluru -> Sri City -> Chennai -> Bengaluru
```

## Minimum MVP Output

```text
Top 25 directed lanes
Top 10 launch/validate corridors
Top 5 triangle candidates
3 active validation experiments
```

---

# Final Takeaway

This Qwen note adds a useful pre-triangle step:

```text
rank high-volume trading pairs first,
then detect weak reverse lanes,
then search triangle substitutes.
```

That makes the system more CEO-useful.

Instead of asking:

```text
Where can we find return loads?
```

The platform asks:

```text
Which directed lanes deserve investment,
which reverse lanes are weak,
and which triangle loops can improve revenue per vehicle day?
```

That is the real route-planning intelligence layer.
