---
type: lane_reliability_scorecard
lane_id:
origin:
destination:
cargo_type:
vehicle_type:
calculation_window_days: 90
reliability_score:
reliability_grade:
on_time_pct:
otif_pct:
p90_delay_min:
tracking_coverage_pct:
requires_backup_carrier:
pricing_premium_pct:
data_confidence:
last_calculated:
idempotency_key:
---
# Lane Reliability Scorecard: {{origin}} -> {{destination}} ({{cargo_type}})

## Current Score

| Metric | Value | Target | Status |
|---|---:|---:|---|
| Reliability Score | {{reliability_score}} | 85+ |  |
| Grade | {{reliability_grade}} | A |  |
| On-Time % | {{on_time_pct}} | 92 percent |  |
| OTIF % | {{otif_pct}} | 90 percent |  |
| P90 Delay | {{p90_delay_min}} min | <= 300 min |  |
| GPS Coverage | {{tracking_coverage_pct}} | 95 percent |  |

## Delay Breakdown

| Cause | Average Delay | Notes |
|---|---:|---|
| Pickup delay |  |  |
| Transit delay |  |  |
| Terminal dwell |  |  |
| Documentation delay |  |  |
| Last-mile delay |  |  |

## Agent Guidance

```yaml
sla_window_hours:
requires_backup_carrier:
pricing_premium_pct:
can_promise_tight_sla:
requires_human_approval:
block_auto_matching:
```

## Improvement Actions

- [ ] Identify top delay source
- [ ] Validate carrier consistency
- [ ] Check GPS coverage compliance
- [ ] Update route buffer
- [ ] Review pricing premium

## Trend

```dataview
TABLE last_calculated, reliability_score, reliability_grade, on_time_pct, p90_delay_min
FROM "12_Dashboards/Lane_Scorecards"
WHERE lane_id = this.lane_id
SORT last_calculated DESC
```

## Evidence Log

| Claim | Source | Confidence |
|---|---|---|
|  |  |  |
