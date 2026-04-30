# Lane Reliability Scorecard Master

| Lane | Cargo | Vehicle | Score | Grade | P90 Delay | Agent Action | Status |
|---|---|---|---:|---|---:|---|---|
| Chennai -> Coimbatore | Textiles | 20ft | 78 | B | 546 | Standard SLA + backup carrier | validate |
| Tiruppur -> Chennai Port | Export garments | 20ft/32ft | 68 | C | 620 | Human approval for export cutoff | validate |
| Bengaluru -> Hosur | Auto/EV | 14ft/20ft | 90 | A | 120 | Tight SLA allowed | active |

## Dataview: Low Reliability Lanes

```dataview
TABLE origin, destination, cargo_type, reliability_score, reliability_grade, p90_delay_min, pricing_premium_pct
FROM "12_Dashboards/Lane_Scorecards"
WHERE type = "lane_reliability_scorecard" AND reliability_score < 70
SORT reliability_score ASC
```

## Dataview: Lanes Eligible for Tight SLA

```dataview
TABLE origin, destination, cargo_type, vehicle_type, reliability_score, tracking_coverage_pct
FROM "12_Dashboards/Lane_Scorecards"
WHERE type = "lane_reliability_scorecard" AND reliability_score >= 85 AND tracking_coverage_pct >= 95
SORT reliability_score DESC
```
