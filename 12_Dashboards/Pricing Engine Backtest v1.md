---
type: dashboard-validation
domain: pricing
scope: strategic
status: active
last_updated: 2026-05-20
related_hubs:
  - Algorithms Hub
  - Market Intelligence Hub
tags:
  - backtest
  - pricing
  - corridor-scoring
  - zippy-logistics
---

# Pricing Engine Backtest v1

## Purpose

Backtest the enhanced dynamic pricing mechanism against the corridor seed lanes currently available in the vault.

This is a proxy backtest, not a production revenue backtest.

It validates whether the pricing engine now behaves sensibly when exposed to:

- route difficulty
- urban density
- deadhead / return-load risk
- demand-supply imbalance
- hard-gated corridor complexity
- service-tier differences

## Backtest Inputs

Used:

- `12_Dashboards/Tableau/sample_data/sample_corridor_opportunity_scores.csv`
- `backend/app/services/pricing_service.py`
- `backend/scripts/pricing_backtest.py`

Output:

- `12_Dashboards/Tableau/sample_data/sample_pricing_backtest_results.csv`

Still missing:

- actual quote win/loss data
- real transporter bid data
- real customer willingness-to-pay by lane
- actual margin and payout history
- actual detention, dispute, and settlement hold events

## Backtest Method

Each corridor seed lane is converted into a deterministic pricing scenario.

The script infers:

- distance from known South India lane approximations
- vehicle category from cargo profile
- weight from cargo profile
- route difficulty from complexity, competition, route shape, and hard-gate flags
- lane viability from backhaul score
- demand/supply imbalance from corridor score inputs

The pricing engine then returns:

- final price
- rate per km
- route difficulty tier
- density multiplier
- deadhead surcharge
- surge multiplier
- platform fee
- GST estimate

## Interpretation Rules

The pricing engine is treated as directionally healthy if:

- hard-gated lanes remain visibly expensive or review-oriented
- weak-return lanes are not underpriced
- balanced lanes avoid unnecessary deadhead surcharge
- higher-complexity lanes receive route difficulty pricing
- pricing output remains explainable by component

## Backtest Verdict

Current verdict:

```text
Pass as proxy pricing sanity check.
Not yet a commercial proof backtest.
```

Why:

- the enhanced model now prices corridor friction explicitly instead of hiding it inside a vague route-risk multiplier
- deadhead risk is visible and auditable
- urban density is separated from general surge
- high-risk lanes produce visible pricing reasons
- the output CSV can be inspected in Tableau or spreadsheet workflows

## Operational Use

Use this backtest for:

- checking pricing-engine regressions
- comparing lane quote reasonableness
- showing why a quote changed
- prioritizing lanes that need field quote capture
- preparing the next evidence-backed pricing sprint

Do not use it for:

- final customer rate cards
- autonomous quote approval
- GST finalization
- provider payout calculation
- credit or settlement decisions

## Next Backtest Upgrade

Move from proxy backtest to evidence backtest by collecting, for each priority lane:

1. 10-14 day quote capture from transporters
2. shipper accepted/rejected quote samples
3. actual trip cost and margin
4. return-load availability observations
5. detention or waiting-time evidence
6. payment delay and settlement hold outcomes

## Run Command

From repo root:

```powershell
backend\.venv\Scripts\python.exe backend\scripts\pricing_backtest.py
```

## Final Reading

The pricing mechanism is now backtestable because the core quote output exposes its reasons.

That is the important shift:

```text
from black-box quote
to auditable corridor price memory
```
