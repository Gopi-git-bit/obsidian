---
type: dashboard-seed
domain: market-intelligence
scope: strategic
status: active
last_updated: 2026-05-11
related_hubs:
  - Market Intelligence Hub
tags:
  - dashboard
  - corridor-scoring
  - seed-data
  - strategic
  - zippy-logistics
---

# Top 10 Corridor Seed Score Sheet

## Purpose

This note provides the first-pass scored corridor sheet for the strategic market-intelligence dashboard.

It converts existing lane research into usable seed data for:

- corridor ranking
- launch sequencing
- pricing-confidence review
- competitor white-space review

## Scoring Basis

These scores follow [[Corridor Opportunity Scoring Model]] and use current evidence from:

- lane notes
- corridor and cluster research
- return-load and triangle-route notes
- pricing and service benchmark logic
- competitor battlefield positioning

These are first-pass strategic scores, not final field-validated scores.

## Seed Scored Corridors

| Lane ID | Origin | Destination | Cargo Focus | Demand | Supply | Backhaul | Pricing | Payment | Complexity | Proof | Competition | Total | Confidence | Hard Gate | Recommendation | Next Action |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| tiruppur:chennai:garments | Tiruppur | Chennai | garments / export cargo | 18 | 10 | 11 | 7 | 6 | 6 | 9 | 7 | 74 | medium | no | validate manually | collect reverse-lane rates and transporter interviews |
| chennai:tiruppur:textiles | Chennai | Tiruppur | textile inputs / dry goods | 11 | 11 | 6 | 6 | 6 | 7 | 7 | 6 | 60 | medium | no | build later | verify reverse-demand depth and backhaul fit |
| coimbatore:chennai:engineering | Coimbatore | Chennai | engineering / warehouse freight | 17 | 11 | 10 | 7 | 7 | 7 | 8 | 6 | 73 | medium | no | validate manually | capture live rate bands and shipper proof angle |
| chennai:coimbatore:mixed | Chennai | Coimbatore | industrial inputs / mixed B2B | 14 | 11 | 9 | 7 | 7 | 7 | 7 | 7 | 69 | medium | no | validate manually | confirm repeat-lane mix and contractability |
| erode:chennai:textiles | Erode | Chennai | processed fabric / textile cargo | 16 | 9 | 10 | 7 | 6 | 6 | 8 | 8 | 70 | medium | no | validate manually | validate shipper frequency and rate benchmarks |
| karur:chennai:home_textiles | Karur | Chennai | home textiles / furnishing exports | 14 | 8 | 9 | 7 | 6 | 6 | 8 | 9 | 67 | medium | no | validate manually | confirm export-linked repeat demand and supply depth |
| namakkal:chennai:poultry_industrial | Namakkal | Chennai | poultry inputs / industrial freight | 13 | 13 | 8 | 6 | 6 | 5 | 6 | 7 | 64 | medium | no | build later | separate poultry and non-poultry vehicle patterns |
| hosur:chennai:auto_components | Hosur | Chennai | auto / EV / industrial parts | 17 | 11 | 10 | 8 | 7 | 8 | 8 | 8 | 77 | medium | no | validate manually | prioritize industrial shipper interviews and lane pilots |
| hosur:coimbatore:industrial | Hosur | Coimbatore | industrial parts / west TN supply | 15 | 10 | 11 | 7 | 7 | 7 | 7 | 8 | 72 | medium | no | validate manually | confirm return-load logic through Salem/Erode |
| coimbatore:tuticorin_via_madurai:export | Coimbatore | Tuticorin via Madurai | textile / engineering export cargo | 15 | 8 | 9 | 7 | 6 | 5 | 8 | 8 | 66 | low | yes | validate manually | validate port workflow, CFS dependency, and document burden |

## Immediate Strategic Read

### Best Near-Term Lanes

- `hosur:chennai:auto_components`
- `tiruppur:chennai:garments`
- `coimbatore:chennai:engineering`
- `hosur:coimbatore:industrial`

Why:

- strong recurring demand
- good proof potential
- workable competitive white-space
- strong connection to Zippy's corridor-first thesis

### Lanes Needing More Caution

- `chennai:tiruppur:textiles`
- `namakkal:chennai:poultry_industrial`
- `coimbatore:tuticorin_via_madurai:export`

Why:

- weaker or more specialized reverse-lane logic
- more complex vehicle-fit or compliance issues
- lower benchmark confidence

## Field Validation Priorities

Promote the first four corridors for:

1. shipper interviews
2. transporter interviews
3. live quote capture
4. reverse-lane signal collection
5. proof-asset opportunity mapping

## Data Confidence Notes

- `medium` means multiple notes support the lane, but live field data is still partial
- `low` means the lane is strategically interesting but still too dependent on desk research or document-heavy assumptions
- hard gates should block automatic promotion into `launch now`

## Related Seed Data

Dashboard-friendly CSV:

- `12_Dashboards/Tableau/sample_data/sample_corridor_opportunity_scores.csv`
