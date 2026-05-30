---
type: dashboard-validation
domain: accounting
scope: broker-model
status: active
last_updated: 2026-05-20
related_hubs:
  - Business Models Hub
  - Compliance & Regulation Hub
tags:
  - backtest
  - accounting
  - broker-model
  - ind-as-115
  - zippy-logistics
---

# Accounting Policy Backtest v1

## Purpose

Backtest Zippy's agent/broker accounting policy against deterministic accounting scenarios.

This validates whether the accounting policy engine behaves correctly when:

- customer money is collected before delivery
- POD or OTP is missing
- POD and OTP fall across month-end
- driver settlement is disputed
- someone tries to post gross freight as revenue
- contract wording or vehicle ownership creates principal-agent risk

## Backtest Inputs

Script:

- `backend/scripts/accounting_policy_backtest.py`

Output:

- `12_Dashboards/Tableau/sample_data/sample_accounting_policy_backtest_results.csv`

Policy source:

- `04_AI_Agents/Accounting Policy Engine for Broker Model.md`
- `04_AI_Agents/Payment Invoice and Accounting Agent Architecture for Logistics Platform.md`
- `04_AI_Agents/Finance and Invoice Event Layer for Logistics Platform.md`
- `09_Market_Intelligence/Indian Ecosystem/GST for Logistics.md`

## Scenarios Covered

| Scenario | Purpose |
| --- | --- |
| Clean prepaid broker transaction | Confirms net commission after POD + OTP |
| Payment received, no POD/OTP | Confirms liability-only treatment |
| POD verified, OTP missing | Confirms revenue hold |
| Driver dispute open | Confirms driver payable hold |
| Gross freight posted as revenue | Confirms blocker catches wrong journal |
| Contract wording not broker-safe | Confirms principal-agent review |
| POD before month-end, OTP after month-end | Confirms cut-off defers revenue |
| Zippy owns vehicle / primary obligor | Confirms principal review |

## Expected Accounting Behavior

For standard marketplace transactions:

```text
Dr Bank / Payment Gateway Control
    Cr Customer Advance / Freight Collection Liability
```

After verified POD + OTP and no hold:

```text
Dr Customer Advance / Freight Collection Liability
    Cr Commission / Platform Service Income
    Cr Output GST - Commission / Platform Fee
```

Driver payable:

```text
Dr Customer Advance / Freight Collection Liability
    Cr Driver / Vehicle Owner Payable
```

Blocked journal:

```text
Dr Bank / Payment Gateway Control
    Cr Freight Revenue
```

## Backtest Verdict

Current verdict:

```text
Pass as broker-model accounting sanity check.
Not yet a statutory audit evidence test.
```

Why:

- revenue is never recognized on gross freight in broker scenarios
- commission revenue waits for POD + OTP
- GST taxable value follows commission, not gross freight
- gross collection reconciles to driver payable + commission + GST on commission
- driver payable is held when dispute evidence exists
- contract-risk scenarios go to review instead of being auto-posted
- month-end cut-off defers commission when OTP falls after period end

Latest run summary:

| Metric | Result |
|---|---:|
| scenarios tested | 8 |
| pass count | 8 |
| fail count | 0 |
| blocked count | 1 |
| review count | 2 |
| average recognized revenue | 625.00 |

Actual-result distribution:

| Actual Result | Count |
|---|---:|
| pass | 5 |
| blocked | 1 |
| review | 2 |

## Run Command

From repo root:

```powershell
backend\.venv\Scripts\python.exe backend\scripts\accounting_policy_backtest.py
```

## Next Backtest Upgrade

Replace deterministic scenarios with real pilot transaction exports:

1. payment gateway collection records
2. POD timestamps
3. OTP timestamps
4. driver payout files
5. settlement holds
6. GST invoice exports
7. Tally voucher exports

## Final Reading

The accounting policy is now backtestable because each transaction can be reduced to:

```text
classification -> collection liability -> POD/OTP evidence -> commission revenue -> driver payable -> GST validation -> close blocker
```

That is the right spine for avoiding inflated revenue and messy GST treatment.
