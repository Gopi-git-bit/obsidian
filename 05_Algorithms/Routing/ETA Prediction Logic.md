---
type: algorithm
domain: routing
decision_value: high
inputs:
  - route_segments
  - historical_speed_profile
  - gps_ping
  - traffic_feed
  - weather_feed
  - driver_telematics
  - load_context
  - model_features
outputs:
  - eta_datetime
  - eta_seconds
  - confidence_interval
  - factor_summary
  - eta_events
status: verified
related_hubs:
  - Algorithms Hub
  - Fleet & Transport Hub
  - Technology Stack Hub
  - Operations Strategy Hub
tags:
  - algorithm
  - eta
  - routing
  - prediction
  - observability
---

# ETA Prediction Logic

## Purpose

Produce explainable, confidence-scored ETA updates by combining deterministic route timing, real-time adjustments, and optional ML residual correction.

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| route_segments | Array | Planned path with distance, road class, tolls, and baseline speed |
| historical_speed_profile | Object | Corridor and time-bucket speed history |
| gps_ping | Object | Latest verified location and motion state |
| traffic_feed | Object | Live congestion or delay signals |
| weather_feed | Object | Route-level weather conditions |
| driver_telematics | Object | Recent speed discipline and route behavior |
| load_context | Object | Vehicle type, load ratio, and route complexity |
| model_features | Object | Features for optional residual prediction layer |

## Hard Guardrails

- ETA prediction must not mutate order state directly.
- Every recalculation should remain traceable to `trace_id`, `idempotency_key`, and data freshness context.
- ML may refine ETA but must not override hard feasibility or lifecycle rules.
- Low-confidence ETA should trigger escalation or conservative communication, not silent optimism.
- External feed failure must degrade gracefully to historical or cached estimates.
- Final ETA should remain clamped to an approved bounded range around the deterministic baseline.

## Three-Layer Logic

```text
1. CALCULATE deterministic base ETA from route segments, historical speeds, toll delay, and fixed checkpoint friction
2. APPLY real-time multipliers for traffic, weather, incidents, driver behavior, and weight context
3. ADD optional ML residual correction when model confidence is acceptable
4. FUSE results into final ETA, confidence score, and confidence interval
5. EMIT recalculation event for TMS, OMS, and supervisor consumption
```

## Layer 1: Base ETA

- Use segment-level route data from Valhalla, OSRM, or cached routing.
- Pull historical speed by road class, hour, weekday, and vehicle type.
- Add fixed delay blocks for tolls, urban-entry friction, loading-zone dwell, or known choke points.
- Treat this layer as the fallback floor when live services degrade.

## Layer 2: Real-Time Adjustments

| Factor | Typical Effect | Notes |
|--------|----------------|-------|
| Traffic | Slows or speeds route progression | Highest-confidence live signal when fresh |
| Weather | Penalizes safe speed | Important during rain, fog, heat |
| Incidents | Adds fixed delay | Prefer explicit minute-level penalty |
| Driver behavior | Personalizes speed profile | Use only from recent verified telematics |
| Load ratio | Slight speed adjustment | Keep effect bounded and explainable |

## Telemetry Validation Pattern

- Reject GPS points with poor accuracy, impossible speed, or invalid movement state before ETA updates.
- Deduplicate near-identical pings so replay noise does not distort ETA or breach detection.
- Treat GPS silence as a transport signal that may require fallback communication or supervisor review.

## Layer 3: Predictive Correction

- Predict residual error between observed outcomes and the deterministic-plus-live ETA.
- Use LightGBM or similar tabular model on route, time, driver, vehicle, and season features.
- Apply ML correction only when model confidence is above a deployment threshold.
- Run shadow mode before production rollout and monitor calibration, not just MAE.

## Training Pipeline Pattern

- Build features from pickup time, weekday, peak-hour signals, vehicle age, body type, route difficulty, service level, and customer tier.
- Use native categorical handling for vehicle, cargo, zone, and payment dimensions where possible.
- Keep training and inference feature engineering in one shared contract or mirrored implementation.
- Favor modular feature packages such as `tsfresh`, `Featuretools`, `feature-engine`, and `statsmodels` when they improve feature quality without obscuring reasoning.
- Save models with explicit versioning and validate them in shadow mode before traffic expansion.
- Tune hyperparameters only after baseline feature quality and data hygiene are stable.
- Use MAPE or comparable live-quality thresholds to decide when tuning should run.
- Promote tuned models only after holdout wins and controlled canary checks.

## Confidence and Explainability

- Return a confidence interval rather than a single hard promise.
- Include factor summaries such as base ETA, live adjustment percentage, and ML correction minutes.
- Surface stale-input warnings when traffic, weather, or GPS data exceed freshness limits.
- Use low-confidence thresholds to trigger supervisor review or conservative ETA messaging.

## Operational Triggers

| Trigger | Action |
|---------|--------|
| Significant GPS movement | Recalculate ETA asynchronously |
| Traffic or weather shift | Refresh live factors and recompute |
| Confidence drops below threshold | Raise operator or supervisor alert |
| API outage | Fall back to historical or cached ETA path |
| Large ETA slip with high confidence | Notify OMS or customer-communication flow |

## Metrics

| Metric | Target Use |
|--------|------------|
| ETA MAE | Accuracy benchmark |
| Confidence interval coverage | Calibration quality |
| Recalculation latency p95 | Runtime health |
| Low-confidence alert rate | Operational risk indicator |
| Delay-notification precision | Customer trust signal |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| ML model unavailable | Use realtime-adjusted ETA only |
| Traffic API unavailable | Use historical speed profile and cached corridor factor |
| GPS stale | Freeze ETA confidence downward and alert if prolonged |
| Severe route disruption | Re-route first, then recalculate ETA from new path |

## Related Notes

- [[Route Optimization Logic]]
- [[Unified Routing & Optimization Algorithm]]
- [[Machine Learning Models]]
- [[Hyperparameter Tuning System]]
- [[Python Package Fit for Final Architecture]]
- [[TMS Execution Architecture]]
- [[Transportation Agent]]
- [[Order Management Agent]]
- [[Logistics SLA]]
- [[Fallback & Resilience Architecture]]

## Related Hubs

- [[Algorithms Hub]]
- [[Fleet & Transport Hub]]
- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
