---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: python packages.txt
notes: Selective extraction of Python ML and forecasting packages that best fit Zippy's deterministic, audit-heavy logistics architecture
---

# Python Packages Architecture Fit Source

This source was processed selectively. It contained broad logistics and ML tooling discussion, but only a few Python packages closely matched the current architecture.

## Best-Fit Packages Extracted

- `tsfresh` for time-series feature extraction on order, ETA, and telemetry histories
- `Featuretools` for relational feature synthesis across orders, vehicles, drivers, and city tiers
- `feature-engine` for sklearn-friendly, auditable, rule-based feature transformations
- `statsmodels` for decomposition and baseline seasonality analysis before heavier ML

## Why These Fit

- They support explainable preprocessing and forecasting workflows.
- They align well with LightGBM-style tabular modeling already present in the vault.
- They can be combined with deterministic features rather than replacing business logic.
- They fit the current architecture better than heavy end-to-end AutoML tools.

## De-emphasized Packages

- Broad AutoML packages such as PyCaret, AutoTS, and TPOT were not prioritized because they are less aligned with the current deterministic, audit-friendly production posture.
- End-to-end black-box tooling is less suitable than modular feature engineering for the current final-stage architecture.

## Derived Notes

- [[Python Package Fit for Final Architecture]]
- [[Machine Learning Models]]
- [[ETA Prediction Logic]]

---
*Processed selectively to keep only the Python packages that best reinforce the current ML and forecasting architecture.*
