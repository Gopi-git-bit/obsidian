---
type: template
category: route_chain_timing
status: active
created_at: 2026-04-30
---
# Route Chain Timing Evaluation Template

## Route Chain

```text
A -> B -> C -> A
```

| Field | Value |
|---|---|
| Triangle ID |  |
| Primary lane |  |
| Weak return lane |  |
| Substitute leg 1 |  |
| Substitute leg 2 |  |
| Vehicle type |  |
| Cargo type |  |
| Driver time constraint |  |

## Timing Metrics

| Metric | Leg 1 | Leg 2 | Leg 3 | Total |
|---|---:|---:|---:|---:|
| Scheduled travel time |  |  |  |  |
| Actual travel time |  |  |  |  |
| Arrival delay |  |  |  |  |
| Handoff wait |  |  |  |  |
| Loading/unloading delay |  |  |  |  |
| Documentation delay |  |  |  |  |
| Terminal/hub dwell |  |  |  |  |

## Reliability Checks

| Check | Pass/Fail | Notes |
|---|---|---|
| Next load window met |  |  |
| Driver hours feasible |  |  |
| P90 delay within SLA |  |  |
| Cargo compatibility confirmed |  |  |
| Hub capability confirmed |  |  |
| Payment reliability acceptable |  |  |

## Decision

```yaml
route_chain_decision:
  approve_triangle:
  reason:
  required_buffer_hours:
  backup_carrier_required:
  pricing_premium_pct:
  escalate_to_control_tower:
```
