---
type: algorithm_framework
domain: delay_metrics
status: active
created_at: 2026-04-30
linked_frameworks:
  - "Lane Reliability Scorecard for Return Trip Promise Engine"
  - "Triangle Route Engine for Return Trip Optimization"
---
# Common Delay Metrics for South India Transportation Planning

## Purpose

Delay metrics are the foundation of reliable delivery promises, lane reliability scoring, triangle route approval, risk pricing and control-tower escalation.

The goal is not only to know whether a shipment was late.

The goal is to know where delay happened, why it happened, whether it repeats, and what the agent should do next.

## Core Principle

```text
Measure delays where they happen, not only at delivery.
```

A shipment is usually late because of cumulative micro-delays:

```text
pickup delay
+ transit delay
+ terminal dwell
+ documentation delay
+ last-mile delay
= total delay
```

## Measurement Philosophy

```yaml
delay_measurement_philosophy:
  granularity: "per shipment leg, not only end-to-end"
  attribution: "assign delay to stage and root cause"
  actionability: "every metric must trigger an agent decision"
  scoring_unit: "directed lane + cargo type + vehicle type + rolling window"
```

## Tier 1: Raw Delay Metrics

| Metric | Definition | Data Source | Why It Matters |
|---|---|---|---|
| pickup_delay_min | Actual pickup time minus scheduled pickup time | Dispatcher logs, driver app, geofence entry/exit | Origin-side reliability and first cascade risk |
| transit_delay_min | Actual arrival minus expected arrival during linehaul | GPS trajectory, ETA engine, map API | Congestion, breakdown, weather and route risk |
| terminal_dwell_delay_min | Time waiting at hub, port, rail terminal or warehouse beyond SLA | Gate logs, terminal API, driver app | Multimodal handoff and hub congestion risk |
| documentation_delay_min | Time lost to e-way bill, customs, POD, invoice or document validation | Document workflow, admin logs, driver app | Preventable compliance friction |
| last_mile_delay_min | Final delivery window miss, usually final 50 km | Customer confirmation, GPS, POD timestamp | Customer experience and complaint risk |
| total_delay_min | Sum of all stage delays | Calculated field | Core OTIF and buffer signal |
| exception_count | Number of alerts triggered per shipment | Exception system | Complexity and instability proxy |
| resolution_time_min | Time from exception trigger to closure | Ops workflow logs | Operational responsiveness score |
| gps_coverage_pct | Percent of expected GPS pings received | Driver app, telematics | Tracking confidence and intervention ability |

## Tier 2: Analytical Metrics

### On-Time Performance

| Metric | Formula | Target | Agent Use |
|---|---|---:|---|
| on_time_pct | on-time shipments / total shipments | 92 percent or higher | Primary reliability signal |
| otif_pct | on-time and in-full shipments / total shipments | 90 percent or higher | Premium SLA eligibility |
| p50_delay_min | Median delay | <= 120 min | Normal buffer baseline |
| p90_delay_min | 90th percentile delay | <= 300 min | Worst-case planning |
| p99_delay_min | 99th percentile delay | <= 600 min | Risk escalation trigger |

### Variability and Predictability

| Metric | Formula | Target | Agent Use |
|---|---|---:|---|
| delay_stddev_min | Standard deviation of total_delay_min | <= 90 min | Lower variance means stronger promise quality |
| delay_cv | delay_stddev_min / avg_delay_min | <= 0.75 | Normalized unpredictability |
| on_time_trend_7d | 7-day rolling change in on_time_pct | >= 0 percent | Early lane degradation detection |

### Operational Health

| Metric | Formula | Target | Agent Use |
|---|---|---:|---|
| carrier_consistency_score | Score based on repeated reliable carriers | >= 80 | Fewer unknown carriers means more predictability |
| terminal_reliability_pct | Dwell performance against scheduled dwell | >= 85 percent | Hub and multimodal handoff quality |
| tracking_coverage_pct | Average GPS ping compliance | >= 95 percent | Visibility for proactive intervention |
| exception_resolution_speed | Normalized speed of resolving alerts | >= 80 | Ops responsiveness |

### Contextual Risk

| Metric | Formula | Target | Agent Use |
|---|---|---:|---|
| weather_impact_factor | avg delay in bad weather / avg delay overall | <= 1.5 | Seasonal buffer adjustment |
| peak_season_penalty | avg peak delay / avg off-peak delay | <= 1.3 | Dynamic pricing and capacity planning |
| border_crossing_delay_avg | Average e-way bill/state border delay | <= 30 min | Route and documentation optimization |

## Delay Root Cause Taxonomy

Use consistent root cause labels so analysis does not become free-text soup.

```yaml
delay_root_causes:
  pickup:
    - shipper_not_ready
    - loading_labour_delay
    - vehicle_late_to_origin
    - wrong_vehicle_type
    - packaging_not_ready
  transit:
    - congestion
    - breakdown
    - accident
    - weather
    - route_diversion
    - driver_rest_constraint
  terminal:
    - port_gate_wait
    - warehouse_slot_delay
    - rail_yard_dwell
    - weighbridge_queue
    - loading_bay_unavailable
  documentation:
    - eway_bill_missing
    - invoice_mismatch
    - gst_validation_issue
    - pod_upload_issue
    - permit_missing
  last_mile:
    - consignee_unavailable
    - unloading_labour_delay
    - city_entry_restriction
    - address_resolution_issue
    - payment_pending
```

## Composite Reliability Score

This score feeds the lane reliability scorecard.

```text
Lane Reliability Score =
0.30 x On-Time Score
+ 0.20 x Delay Variability Score
+ 0.15 x Carrier Consistency Score
+ 0.15 x Terminal Reliability Score
+ 0.10 x Tracking Coverage Score
+ 0.10 x Exception Resolution Score
```

## Score to Agent Decision

| Score | Grade | SLA Promise | Backup Required | Pricing Premium | Agent Rule |
|---:|---|---|---|---:|---|
| 85-100 | A | +/- 2 hours | No | 0 percent | Allow tight SLA and premium cargo |
| 70-84 | B | +/- 4-6 hours | 1 backup | 8 percent | Standard SLA with carrier validation |
| 55-69 | C | +/- 8-12 hours | 2 backups | 18 percent | Human approval for time-sensitive cargo |
| below 55 | D | Manual promise only | Escalate | 35 percent | Block auto-matching |

## Triangle Route Integration

A triangle is not approved only because load exists.

```text
Triangle can be approved if:
1. Triangle score >= 70
2. Each leg has reliability score >= 55
3. Premium/time-sensitive cargo has all legs >= 70
4. p90 delay does not break SLA
5. documentation_delay trend is not worsening
6. GPS coverage is acceptable
```

## Matching Agent Rules

```yaml
matching_rules:
  - if: "lane_reliability_score >= 85 and cargo in ['pharma', 'export_garments', 'auto_ev']"
    action: "allow_tight_sla_with_priority_tracking"

  - if: "lane_reliability_score >= 70 and lane_reliability_score < 85"
    action: "standard_sla_plus_backup_carrier"

  - if: "lane_reliability_score >= 55 and lane_reliability_score < 70"
    action: "add_buffer_and_require_human_approval_for_time_sensitive_cargo"

  - if: "lane_reliability_score < 55"
    action: "block_auto_matching_and_escalate_to_ops"

  - if: "p90_delay_min > 300 and cargo = 'perishables'"
    action: "reject_lane_or_require_reefer_control_tower_review"
```

## Pricing Agent Rule

```python
def calculate_risk_premium(lane_score: float, base_rate: float) -> float:
    if lane_score >= 85:
        return base_rate * 1.00
    if lane_score >= 70:
        return base_rate * 1.08
    if lane_score >= 55:
        return base_rate * 1.18
    return base_rate * 1.35
```

## Risk Agent Escalations

```yaml
escalation_triggers:
  - trigger: "p90_delay_min > 480 and cargo = export_garments"
    action: "require_port_cutoff_buffer_and_ops_review"

  - trigger: "on_time_trend_7d < -5"
    action: "pause_premium_sla_and_start_root_cause_analysis"

  - trigger: "tracking_coverage_pct < 80"
    action: "require_gps_compliance_audit_before_next_booking"

  - trigger: "exception_resolution_speed < 50"
    action: "assign_lane_controller_and_review_exception_workflow"

  - trigger: "documentation_delay_min trending_up"
    action: "send_pre_trip_document_checklist_and_escalate_missing_docs"
```

## MVP Implementation Order

| Step | Build | Why |
|---:|---|---|
| 1 | lane_delay_events table | Capture atomic delay truth |
| 2 | root cause taxonomy | Prevent messy delay classification |
| 3 | lane_reliability_scores table | Create agent-readable score |
| 4 | Obsidian lane scorecards | Make operational decisions visible |
| 5 | n8n daily refresh | Keep matching/pricing/risk agents updated |

## Start with Road-Only Lanes

Start with road-only lanes first because they have fewer handoff points and cleaner delay attribution.

Recommended MVP lanes:

```text
Chennai -> Coimbatore
Tiruppur -> Chennai Port
Bengaluru -> Hosur
```

## Takeaway

Delay metrics are not dashboard decoration.

They are control signals that tell Zippy when to promise, when to buffer, when to price risk, and when to escalate before a customer gets disappointed.
