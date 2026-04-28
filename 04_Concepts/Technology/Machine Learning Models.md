---
type: concept
domain: technology
decision_value: medium
status: verified
related_hubs:
  - Technology Stack Hub
  - Algorithms Hub
tags:
  - concept
  - machine-learning
  - models
  - analytics
---

# Machine Learning Models

## Purpose

Describe where machine-learning models fit in the Zippy stack, what they are allowed to influence, and how they should be trained, deployed, and monitored.

## Operating Principle

- ML augments deterministic logistics logic; it does not replace hard feasibility, compliance, or state-machine rules.
- Models should provide scores, forecasts, or residual corrections that remain explainable and observable.

## Good Fit Use Cases

| Use Case | Role |
|----------|------|
| ETA residual correction | Improve arrival-time accuracy on noisy lanes |
| Route difficulty estimation | Summarize terrain, road quality, and traffic burden |
| Candidate ranking | Refine order-to-vehicle prioritization after hard filters |
| Risk detection | Flag anomalies, fraud, or delayed-execution patterns |
| Demand forecasting | Support staffing, capacity, and pricing preparation |
| Route optimization support | Score route alternatives and predict delay exposure before TMS selects a plan |
| Predictive maintenance | Flag vehicles likely to fail or miss readiness windows based on usage and history |

## AI Application Layer

AI applications should be treated as decision support for logistics execution:

- route optimization helps compare route options, but final routing must still respect truck feasibility, safety, and compliance.
- predictive maintenance reduces breakdown risk by using vehicle history, utilization, and inspection signals.
- demand forecasting prepares capacity, pricing, staffing, and partner outreach before confirmed orders arrive.
- AI outputs should feed deterministic OMS, IMS, and TMS rules instead of silently replacing them.

## Deployment Guardrails

- Keep training-time and inference-time feature engineering aligned.
- Ship models behind feature flags or shadow mode before production rollout.
- Monitor MAE, calibration, drift, and latency, not just accuracy snapshots.
- Degrade safely to deterministic logic when models or features are unavailable.
- Preserve traceability for model version, input freshness, and confidence output.
- Trigger hyperparameter tuning from explicit quality signals such as MAPE drift, not schedule alone.
- Promote new models only after holdout validation and controlled canary checks.

## ETA Model Pattern

- Use a layered ETA architecture where ML acts as residual correction over deterministic and live-adjusted ETA.
- LightGBM is a strong default for tabular logistics signals such as time, corridor, vehicle, driver, and load context.
- Native categorical support is useful for zone, cargo, customer tier, and vehicle-type dimensions.
- Feature engineering packages such as `tsfresh`, `Featuretools`, `feature-engine`, and `statsmodels` fit better than broad AutoML when pipelines must stay explainable and auditable.

## Common Failure Modes

| Failure Mode | Risk |
|-------------|------|
| Feature drift | Online predictions stop matching training behavior |
| Data staleness | Predictions look precise but reflect old traffic or route state |
| Overfitting | Strong offline metrics fail on new lanes or seasons |
| Silent confidence misuse | Teams trust low-quality predictions too much |
| Unbounded influence | ML overrides rules it should only advise |

## Related Notes

- [[ETA Prediction Logic]]
- [[Hyperparameter Tuning System]]
- [[Hybrid Logistics Data Architecture]]
- [[Fallback & Resilience Architecture]]
- [[Python Package Fit for Final Architecture]]
- [[Transportation Agent]]
- [[Unified Routing & Optimization Algorithm]]
- [[Order Processing and Transportation Management Knowledge Map]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Algorithms Hub]]
