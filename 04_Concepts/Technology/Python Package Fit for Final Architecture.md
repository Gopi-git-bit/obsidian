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
  - python
  - packages
  - ml
  - forecasting
---

# Python Package Fit for Final Architecture

## Purpose

Capture the Python packages that most closely match Zippy's final-stage architecture for explainable forecasting, feature engineering, and production-safe ML workflows.

## Best-Fit Packages

| Package | Best Use in Zippy | Why It Fits |
|---------|-------------------|-------------|
| `tsfresh` | Time-series feature extraction for ETA, demand, and telemetry histories | Strong for lag, rolling, frequency, and statistical features without forcing end-to-end black-box modeling |
| `Featuretools` | Relational feature synthesis across orders, vehicles, drivers, routes, and customer entities | Fits multi-table logistics data and supports auditable feature generation |
| `feature-engine` | Deterministic sklearn-compatible preprocessing and feature transforms | Strong fit for compliance-friendly, explainable pipelines |
| `statsmodels` | Seasonal decomposition, trend analysis, and baseline forecasting | Useful for validation, decomposition, and simpler benchmark models before ML residuals |

## Architecture Match

- These packages complement the existing LightGBM-centered tabular ML pattern.
- They support deterministic-first design by making feature generation explicit.
- They are better aligned with audited production pipelines than broad AutoML suites.
- They help preserve the boundary where business rules remain primary and ML handles structured prediction problems.

## Where They Fit

| Layer | Package Fit |
|------|-------------|
| ETA feature engineering | `tsfresh`, `feature-engine`, `statsmodels` |
| Demand forecasting | `tsfresh`, `statsmodels`, `feature-engine` |
| Relational operations data | `Featuretools` |
| Model-ready preprocessing | `feature-engine` |

## De-prioritized Tools

- Large AutoML tools such as PyCaret, AutoTS, and TPOT are less aligned with the current deterministic and audit-heavy posture.
- Black-box automation is less desirable than modular, explainable preprocessing in a platform with state, finance, and compliance constraints.

## Related Notes

- [[Machine Learning Models]]
- [[ETA Prediction Logic]]
- [[Hyperparameter Tuning System]]
- [[Operational Observability Architecture]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Algorithms Hub]]
