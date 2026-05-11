---
type: dashboard-spec
domain: market-intelligence
scope: strategic
status: active
last_updated: 2026-05-11
related_hubs:
  - Market Intelligence Hub
  - Business Models Hub
tags:
  - dashboard
  - market-intelligence
  - corridor-intelligence
  - competitor-analysis
  - pricing
  - strategic
  - zippy-logistics
---

# Market Intelligence Dashboard Specification

## Purpose

Define a dashboard layer that unifies:

- intelligence maturity
- competitor battlefield analysis
- corridor opportunity scoring
- pricing and service benchmarks
- GTM and proof-system learning

This dashboard is not for live dispatch.

It is for strategic decisions such as:

- which corridors to launch
- which lanes to pause
- where pricing confidence is weak
- where competition is beatable
- where proof assets are strong enough to support scale

## Core Questions

At any moment, this dashboard should answer:

- which corridors are strongest right now?
- why does each top corridor rank highly or poorly?
- where is Zippy winning white-space versus walking into a red ocean?
- which lanes have usable price confidence?
- which corridors deserve GTM spend, carrier onboarding, or pilot focus next?
- what evidence would change the current ranking?

## Dashboard Design Principle

Do not merge this into the live transport control tower.

Keep this as a strategic intelligence layer with slower refresh cadence and richer context.

Split the dashboard into:

1. executive overview
2. corridor opportunity board
3. competitor battlefield board
4. pricing and service benchmark board
5. proof and GTM learning board
6. intelligence health and confidence board

## Target Users

| User | Primary Use |
| --- | --- |
| Founder / strategy lead | decide focus corridors and sequencing |
| GTM lead | choose campaign lanes and proof priorities |
| Pricing analyst | assess lane quality and benchmark confidence |
| Supply lead | decide where to recruit carriers next |
| Ops strategy lead | connect execution pain to corridor attractiveness |

## Dashboard Views

### 1. Executive Overview

Purpose:

- show the current strategic state in one screen

Top cards:

- overall intelligence maturity score
- active scored corridors
- launch-now corridors
- validate-manually corridors
- average pricing confidence
- competitor pressure index
- proof-ready corridors

Recommended visual layout:

```text
KPI row
Top 10 corridor scoreboard
Competitor pressure heatmap | Pricing confidence chart
Proof-ready corridor table | Strategic alerts panel
```

### 2. Corridor Opportunity Board

Purpose:

- rank lanes by attractiveness and actionability

Core visuals:

- ranked corridor table
- corridor score breakdown stacked bars
- map by launch class
- corridor score trend over time

Required metrics:

- total corridor score
- demand score
- supply score
- backhaul score
- pricing score
- payment score
- complexity score
- proof score
- competition score
- hard-gate flag
- confidence level
- current recommendation

Action outputs:

- launch now
- validate manually
- build later
- avoid for now

### 3. Competitor Battlefield Board

Purpose:

- show where competition is strong, weak, or avoidable

Core visuals:

- competitor matrix by archetype
- corridor-by-competitor pressure heatmap
- partner-versus-fight quadrant
- segment threat map

Required metrics:

- competitor density by corridor
- marketplace pressure
- broker saturation
- regional 3PL strength
- white-space score
- WhatsApp-fit differential
- proof-strength differential

Action outputs:

- fight
- flank
- partner
- avoid

### 4. Pricing And Service Benchmark Board

Purpose:

- show whether lane pricing is grounded and whether price posture matches service promise

Core visuals:

- benchmark band versus actual quoted band
- spot versus contract comparison
- urgent premium distribution
- backhaul discount usage
- margin variance by corridor
- surcharge transparency tracker

Required metrics:

- base rate low, mid, high
- quote dispersion
- pricing confidence
- urgent multiplier usage
- backhaul discount frequency
- detention leakage
- quoted versus realized margin variance
- proof-adjusted premium capture

Action outputs:

- tighten benchmark
- gather more rate data
- protect margin
- reduce overpromising

### 5. Proof And GTM Learning Board

Purpose:

- connect corridor selection to actual market messaging and trust-building evidence

Core visuals:

- proof-ready corridor list
- proof asset performance by lane
- corridor-level lead-to-booking conversion
- repeat-booking trend by corridor
- message-theme performance table

Required metrics:

- proof asset count
- case-study readiness
- proof-assisted close rate
- qualified leads by corridor
- booking conversion rate by corridor
- repeat booking rate
- message win rate by pain theme

Action outputs:

- promote lane in GTM
- collect more proof
- pause generic campaigns
- localize message further

### 6. Intelligence Health And Confidence Board

Purpose:

- show whether the intelligence layer itself is trustworthy

Core visuals:

- maturity score breakdown
- data confidence by corridor
- stale-data alerts
- missing-input tracker
- field-validation status board

Required metrics:

- maturity score by dimension
- corridor benchmark confidence
- last field validation date
- missing reverse-lane data count
- missing transporter interview count
- missing shipper interview count
- stale competitor assumption count

Action outputs:

- refresh benchmark
- revalidate lane
- update competitor map
- collect field interviews

## KPI Definitions

### Strategic KPI Cards

| KPI | Meaning |
| --- | --- |
| intelligence maturity score | current maturity from the v1 model |
| launch-now corridors | count of lanes scoring 80+ without hard gates |
| pricing confidence avg | average benchmark confidence across active lanes |
| white-space score avg | how favorable the competitive position is |
| proof-ready corridors | lanes with enough trust assets for GTM scaling |
| corridor re-score alerts | lanes whose recommendation likely changed |

### Core Corridor Metrics

| KPI | Meaning |
| --- | --- |
| corridor opportunity score | total 0-100 score |
| opportunity grade | A/B/C/D style rollup if needed |
| benchmark confidence | low/medium/high |
| white-space score | competitive beatability |
| proof-readiness score | ability to create trust assets |
| expansion readiness | whether the lane should move into GTM or pilot phase |

## Filters

Use filters for:

- time range
- corridor
- origin city
- destination city
- cargo type
- vehicle class
- launch class
- confidence level
- competitor archetype
- segment

## Strategic Alerts

The dashboard should raise alerts when:

- corridor score drops by more than 10 points
- pricing confidence falls below threshold
- a launch-now corridor loses proof-readiness
- competitor pressure rises sharply in a target lane
- detention leakage breaks benchmark tolerance
- repeat booking weakens in a lane still receiving GTM spend
- field data is stale for a corridor being actively pushed

## Data Model Inputs

The dashboard should pull from or be fed by:

- corridor opportunity scoring records
- competitor battlefield records
- lane pricing benchmark records
- corridor GTM metrics
- proof-system tracking
- lane reliability and delay scorecards
- route optimization performance
- interview and field-validation logs

### Suggested Core Tables Or Views

| Source | Role |
| --- | --- |
| corridor_scores | lane-level strategic score output |
| competitor_battlefield | competitor records and corridor pressure |
| lane_pricing_benchmarks | rate and service benchmark inputs |
| lane_reliability_scores | operational reliability context |
| gtm_corridor_metrics | leads, bookings, repeat-booking, proof performance |
| intelligence_maturity_scores | periodic maturity snapshots |

### Seed Dataset

Use the first-pass corridor seed file for dashboard prototyping:

- `12_Dashboards/Tableau/sample_data/sample_corridor_opportunity_scores.csv`

Use the re-scored seed file when v2 strategic comparisons are needed:

- `12_Dashboards/Tableau/sample_data/sample_corridor_opportunity_scores_v2.csv`

Use this proxy backtest file to compare score recommendations versus available operational hints:

- `12_Dashboards/Tableau/sample_data/sample_corridor_backtest_results.csv`

## Refresh Cadence

| Layer | Refresh |
| --- | --- |
| corridor scores | weekly or on material change |
| pricing benchmarks | weekly review, monthly hard refresh |
| competitor assumptions | monthly or on major market signal |
| GTM metrics | daily to weekly depending on source |
| maturity score | monthly or quarterly |

## Recommended Dashboard Pages

### Page 1: Strategy Command View

Audience:

- founder
- strategy lead

Shows:

- top KPI cards
- top corridors
- top strategic alerts
- maturity status

### Page 2: Corridor Ranking Lab

Audience:

- network planning
- GTM lead
- supply lead

Shows:

- lane table with all score components
- trend comparison
- map and launch class

### Page 3: Pricing Confidence Lab

Audience:

- pricing analyst
- founder

Shows:

- band comparison
- quote variance
- premium versus service fit
- detention and surcharge patterns

### Page 4: Competitor And White-Space View

Audience:

- strategy
- GTM

Shows:

- competitor archetype matrix
- corridor-level pressure
- white-space quadrants

### Page 5: GTM Proof Readiness View

Audience:

- GTM
- founder

Shows:

- proof-ready lanes
- conversion and repeat-booking by corridor
- message-theme performance

## Example Decision Rules

| Scenario | Dashboard Recommendation |
| --- | --- |
| lane scores high but pricing confidence is low | validate rates before scaling GTM |
| lane scores high and proof-readiness is high | push lane into campaign and pilot priority |
| lane scores high but competitor pressure spikes | narrow message and avoid generic price fight |
| lane has good GTM response but weak repeat booking | inspect service and pricing mismatch |
| lane is profitable but proof-poor | collect testimonials and POD evidence before scaling |

## Visualization Suggestions

Use:

- scorecards for top-line KPIs
- heatmaps for corridor and competitor pressure
- stacked bars for score composition
- scatter plots for opportunity score versus pricing confidence
- maps for geographic launch class
- alert tables for actionability

Avoid:

- dashboards that only report vanity lead counts
- price charts without service context
- corridor rankings without confidence flags

## Success Criteria

This dashboard is useful only if it helps someone:

- pick the next corridor
- stop spending on a weak lane
- tighten a pricing benchmark
- identify a beatable competitor zone
- decide where field interviews or proof capture should happen next

If a chart does not support one of those decisions, remove it.

## Implementation Phases

### Phase 1: Spec And Sample Layer

- define fields and calculations
- use sample corridor and lane score data
- mock competitor and pricing benchmark tables if needed

### Phase 2: Strategic Dashboard Prototype

- build the first dashboard pages
- connect corridor scoring, pricing benchmark, and GTM signals

### Phase 3: Intelligence Ops Layer

- add competitor refresh cadence
- add confidence and stale-data warnings
- support monthly re-scoring workflow

## Final Rule

This dashboard should act like a strategic operating console, not a decorative report.

It should tell Zippy:

- where to go
- why to go there
- what to charge
- what to prove
- and what to ignore for now
