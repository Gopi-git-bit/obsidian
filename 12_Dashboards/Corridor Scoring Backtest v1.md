---
type: dashboard-validation
domain: market-intelligence
scope: strategic
status: active
last_updated: 2026-05-11
related_hubs:
  - Market Intelligence Hub
tags:
  - backtest
  - corridor-scoring
  - dashboard-validation
  - strategic
  - zippy-logistics
---

# Corridor Scoring Backtest v1

## Purpose

Backtest the corridor scoring model against the best operational proxy data currently available in the workspace.

This is not a full commercial backtest using real bookings, real quotes, and real field interviews.

It is a `proxy backtest` that compares:

- strategic lane scores
- reliability sample data
- lane-master strength signals
- triangle-route priority
- current strategic priorities

## Backtest Inputs

Used:

- `12_Dashboards/Top 10 Corridor Seed Score Sheet v2.md`
- `12_Dashboards/Tableau/sample_data/sample_lane_reliability_scores.csv`
- `12_Dashboards/Directed Lane Master.md`
- `12_Dashboards/Lane Reliability Scorecard Master.md`
- `12_Dashboards/Current Strategic Priorities.md`

Not yet used because missing:

- live shipper interview outcomes
- live transporter interview outcomes
- actual quote win/loss data
- actual margin-by-lane history
- actual wait-time and dispute logs for these 10 lanes

## Backtest Method

The model is treated as directionally correct if:

- high-ranked lanes align with known priority corridors
- high-ranked lanes do not conflict with poor reliability evidence unless the recommendation remains `validate manually`
- weak-return lanes are downgraded appropriately
- hard-gated lanes do not get promoted too early

## Comparable Lanes With Proxy Operational Data

Only some of the top 10 lanes have usable operational proxies right now.

| Lane ID | Strategic Score v2 | Strategic Recommendation | Proxy Operational Evidence | Operational Read | Backtest Result |
| --- | ---: | --- | --- | --- | --- |
| tiruppur:chennai:garments | 76 | validate manually | sample reliability `62.8`, grade `C`, backhaul `0.52` | strategically strong but operationally noisy | pass |
| chennai:coimbatore:mixed | 74 | validate manually | sample reliability `76.4`, grade `B`, backhaul `0.68` | solid operating lane, not yet proven enough for blind launch | pass |
| hosur:chennai:auto_components | 80 | launch now | proxy support from policy priority and industrial corridor logic; no direct sample row | strategically strongest lane, but still lacks direct lane telemetry in vault | conditional pass |
| chennai:tiruppur:textiles | 56 | build later | weak-return note, backhaul score `3`, triangle dependence | lane is weaker as standalone lane than as loop support | pass |
| coimbatore:tuticorin_via_madurai:export | 68 | validate manually | policy support but hard-gated by port workflow complexity | not safe to promote early without document controls | pass |

## Backtest Summary Metrics

### Recommendation Quality

| Check | Result |
| --- | --- |
| weak-return lane downgraded correctly | yes |
| port-complexity lane gated correctly | yes |
| noisy but strategically strong lane kept in validate state | yes |
| strongest industrial lane promoted to top priority | yes, but still needs direct telemetry |

### Backtest Confidence

| Area | Confidence |
| --- | --- |
| directional ranking quality | medium |
| final launch-readiness quality | low-medium |
| commercial truth quality | low |

## What The Backtest Says

The scoring model is doing the right *kind* of work.

It is:

- filtering weak standalone return lanes downward
- rewarding corridor strength plus route logic
- keeping noisy lanes in `validate manually` instead of falsely promoting them
- respecting complexity gates on export and port-linked lanes

The model is **not yet fully proven** because the vault still lacks:

- lane-level commercial win-rate data
- live pricing capture
- real shipper willingness-to-pay data
- actual per-lane settlement and dispute history

## Backtest Verdict

### Model Verdict

`Pass with caution`

Why:

- the model aligns well with the operational hints we do have
- it avoids the most dangerous false-positive behaviors
- it still depends too much on desk-research and proxy signals for final lane promotion

### Best-Proven Strategic Behaviors

- weak-return recognition
- triangle-route support logic
- policy and industrial corridor prioritization
- port-lane gating discipline

### Least-Proven Strategic Behaviors

- true pricing-quality scoring by lane
- real payment-reliability scoring by lane
- proof-readiness scoring from actual customer assets
- competition score calibration from field reality

## Next Validation Upgrade

To move from `proxy backtest` to `evidence backtest`, collect for the top 5 lanes:

1. 10-14 day quote capture
2. 3-5 shipper interviews
3. 3-5 transporter interviews
4. reverse-load post counts
5. wait-time and detention observations
6. one real proof asset per lane if possible

## Final Reading

This backtest does not prove the model is production-ready.

It does prove that the model is already useful for:

- narrowing focus
- rejecting weak lanes
- sequencing validation work
- structuring the next research sprint

That is enough to treat it as a decision aid, not yet as an autonomous lane selector.
