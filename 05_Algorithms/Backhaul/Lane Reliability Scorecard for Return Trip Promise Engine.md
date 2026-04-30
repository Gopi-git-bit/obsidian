---
type: algorithm_framework
domain: lane_reliability
status: active
source_file: "C:\\Users\\user\\Downloads\\return trip -3.txt"
created_at: 2026-04-30
---
# Lane Reliability Scorecard for Return Trip Promise Engine

## Purpose

The return-trip engine should not recommend a triangle only because cargo exists.

It should recommend a triangle only when the route can be promised, executed, tracked and paid safely.

A lane reliability scorecard converts historical delay data into a control signal for matching, pricing and risk agents.

## Core Principle

```text
A metric is useful only if it changes agent behaviour.
```

The scorecard should answer:

```text
Can we promise tight SLA?
Should we add buffer?
Should we require backup carrier?
Should we apply risk premium?
Should we block auto-matching and escalate?
```

## Granularity

Score lanes directionally.

```text
Chennai -> Coimbatore != Coimbatore -> Chennai
```

Recommended scoring unit:

```text
directed lane + cargo type + vehicle class + rolling time window
```

Example:

```text
chennai:coimbatore:textiles:20ft:rolling_90d
```

## Raw Delay Event Metrics

| Metric | Definition | Agent Use |
|---|---|---|
| pickup_delay_min | Actual pickup minus scheduled pickup | Origin reliability |
| transit_delay_min | Actual arrival minus expected arrival | Route and congestion risk |
| terminal_dwell_delay_min | Hub/port/rail waiting beyond SLA | Handoff risk |
| documentation_delay_min | E-way bill/customs/POD delay | Compliance friction |
| last_mile_delay_min | Final delivery window miss | Customer experience risk |
| exception_count | Number of exceptions per shipment | Complexity signal |
| resolution_time_min | Alert to resolution duration | Ops responsiveness |
| gps_coverage_pct | GPS ping compliance | Tracking confidence |

## Analytical Metrics

| Metric | Formula / Logic | Target |
|---|---|---|
| on_time_pct | On-time shipments / total shipments | >= 92 percent |
| otif_pct | On-time and in-full shipments / total shipments | >= 90 percent |
| p50_delay_min | Median delay | Low and stable |
| p90_delay_min | 90th percentile delay | <= 300 min for normal lanes |
| p99_delay_min | 99th percentile delay | Escalation signal |
| delay_cv | stddev delay / average delay | <= 0.75 |
| tracking_coverage_pct | Average GPS compliance | >= 95 percent |
| terminal_reliability_pct | Dwell performance against SLA | >= 85 percent |
| exception_resolution_speed | Normalized resolution speed | >= 80 |

## Composite Score

```text
Lane Reliability Score =
0.30 x On-Time Score
+ 0.20 x Delay Variability Score
+ 0.15 x Carrier Consistency Score
+ 0.15 x Terminal Reliability Score
+ 0.10 x Tracking Coverage Score
+ 0.10 x Exception Resolution Score
```

## Grade to Agent Action

| Score | Grade | SLA Promise | Backup | Pricing | Agent Action |
|---:|---|---|---|---|---|
| 85-100 | A | +/- 2 hours | No | 0 percent premium | Allow tight SLA and premium cargo |
| 70-84 | B | +/- 4-6 hours | 1 backup | +8 percent | Standard SLA with validation |
| 55-69 | C | +/- 8-12 hours | 2 backups | +18 percent | Human approval for time-sensitive cargo |
| below 55 | D | Manual promise only | Escalate | +35 percent/manual fee | Block auto-matching |

## Return-Trip Integration

A triangle route can be selected only if each leg passes the lane reliability gate.

```text
Triangle Approved if:
triangle_score >= 70
AND min(lane_reliability_score for each leg) >= 55
AND no leg has blocked cargo compliance
AND p90_delay does not break customer SLA
```

For premium cargo:

```text
Require all legs >= 70
Require GPS coverage >= 95 percent
Require backup carrier for any B-grade leg
```

## Matching Agent Rules

```yaml
matching_rules:
  - if: "lane_reliability_score >= 85 and cargo in ['pharma', 'auto_ev', 'export_garments']"
    action: "allow_tight_sla"

  - if: "lane_reliability_score >= 70 and lane_reliability_score < 85"
    action: "standard_sla_with_backup_carrier"

  - if: "lane_reliability_score >= 55 and lane_reliability_score < 70"
    action: "require_human_approval_for_time_sensitive_cargo"

  - if: "lane_reliability_score < 55"
    action: "block_auto_matching_and_escalate"

  - if: "p90_delay_min > 300 and cargo in ['perishables', 'export_garments']"
    action: "reject_or_add_control_tower_buffer"
```

## Pricing Agent Formula

```python
def lane_risk_multiplier(lane_score: float) -> float:
    if lane_score >= 85:
        return 1.00
    if lane_score >= 70:
        return 1.08
    if lane_score >= 55:
        return 1.18
    return 1.35
```

## Risk Agent Escalation

```yaml
risk_escalations:
  - trigger: "p90_delay_min > 480 and cargo = export_garments"
    action: "require_port_cutoff_buffer_and_ops_review"

  - trigger: "on_time_trend_7d < -5"
    action: "pause_premium_sla_and_start_root_cause_analysis"

  - trigger: "tracking_coverage_pct < 80"
    action: "require_gps_compliance_audit"

  - trigger: "sample_size < 30"
    action: "mark_data_confidence_low_and_require_human_validation"
```

## n8n Workflow

```text
WF_LANE_01_daily_reliability_scorecard_refresh

Schedule: Daily 02:00 IST
-> Query lane_delay_events for rolling 90-day window
-> Aggregate per directed lane, cargo type and vehicle class
-> Calculate component scores
-> Upsert lane_reliability_scores
-> Generate improvement actions for scores below 80
-> Update Obsidian lane scorecard notes
-> Notify matching, pricing and risk agents
-> Alert ops if any lane drops more than 10 points week-over-week
```

## MVP Lanes

| Lane | Reason |
|---|---|
| Chennai -> Coimbatore | High-volume mixed cargo and triangle connector role |
| Tiruppur -> Chennai Port | Export-critical and cutoff-sensitive |
| Bengaluru -> Hosur | Short JIT lane with cleaner delay attribution |

## Takeaway

A lane reliability scorecard is not a report. It is a promise engine.

It tells Zippy when to sell confidence, when to price risk, and when to slow down before the system makes a bad promise.
