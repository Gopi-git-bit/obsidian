---
type: dashboard-validation
domain: partnerships
scope: contract-compatibility
status: active
last_updated: 2026-05-21
related_hubs:
  - Business Models Hub
  - Compliance & Regulation Hub
tags:
  - backtest
  - partnerships
  - contracts
  - settlement
  - compliance
  - zippy-logistics
---

# Partnership Terms Backtest v1

## Purpose

Backtest the uploaded partnership term sheet ideas against current Zippy business practice and system guardrails.

This is a deterministic compatibility backtest, not a legal approval workflow.

It validates whether term-sheet patterns preserve:

- OMS/TMS/FIN state boundaries
- driver and transport-company default economics
- payment custody controls
- insurance distribution controls
- AI dispute limits
- loop settlement and GST isolation
- partner data minimization
- wind-down and exit discipline

## Backtest Inputs

Script:

- `backend/scripts/partnership_terms_backtest.py`

Output:

- `12_Dashboards/Tableau/sample_data/sample_partnership_terms_backtest_results.csv`

Policy sources:

- `08_Business_Models/Partnership Term Sheet Compatibility Framework.md`
- `03_Hubs/Business Models Hub.md`
- `KNOWLEDGE.md`
- `04_AI_Agents/Payment Settlement Agent.md`
- `04_Concepts/Compliance/Operational Compliance Framework for Indian Logistics Startup 2025-2026.md`

## Scenarios Covered

| Scenario | Purpose |
|---|---|
| Anchor tenant SCaaS | Confirms bounded enterprise API partnership can pass |
| SFO default commission | Confirms 10% driver commission is compatible |
| SFO commission override | Confirms non-default commission requires review |
| Transport company flat fee | Confirms Rs 700/order service fee is compatible |
| Transport company revenue share | Confirms percentage share requires strategic approval |
| Strategic alliance | Confirms approved revenue share can pass |
| Payment partner escrow | Confirms regulated partner escrow can pass |
| Zippy-held funds | Confirms unapproved custody is blocked |
| Insurance partner-led model | Confirms approved insurer path can pass |
| Direct insurance sale | Confirms unapproved insurance distribution is blocked |
| AI-assisted dispute | Confirms AI scoring plus Finance approval can pass |
| AI refund execution | Confirms AI auto-refund is blocked |
| Loop settlement isolation | Confirms per-order invoice/refund is compatible |
| Loop cascade refund | Confirms auto-cascade across loop legs is blocked |
| Direct DB state write | Confirms state-machine bypass is blocked |
| Overbroad data access | Confirms full customer/driver data access is blocked |

## Interpretation Rules

The term-sheet framework is healthy if:

- safe partner patterns are approved
- business-model deviations are sent to review
- regulated/payment/insurance failures are blocked
- state-machine bypasses are blocked
- AI cannot execute monetary outcomes
- partner data access remains scoped to assigned orders
- loop discounts do not corrupt per-order invoice/refund records

## Backtest Verdict

Current verdict:

```text
Pass as partnership contract compatibility sanity check.
Not a substitute for legal, tax, RBI, IRDAI, or DPDP review.
```

Latest run summary:

| Metric | Result |
|---|---:|
| scenarios tested | 16 |
| approved | 8 |
| review required | 2 |
| blocked | 6 |
| expectation failures | 0 |
| average compatibility score | 83.12 |

Why:

- default driver and transport-company economics are preserved
- percentage revenue share is allowed only when treated as strategic collaboration
- unapproved payment custody is blocked
- unapproved insurance sale language is blocked
- AI recommendations do not mutate finance or settlement state
- loop-related discounts and disputes stay isolated per order for GST and audit purposes

## Run Command

From repo root:

```powershell
backend\.venv\Scripts\python.exe backend\scripts\partnership_terms_backtest.py
```

If the local virtual environment is not active, use the available Python runtime:

```powershell
python backend\scripts\partnership_terms_backtest.py
```

## Next Backtest Upgrade

Move from deterministic scenarios to evidence-backed partner simulation by collecting:

1. real partner term-sheet drafts
2. signed pilot economics
3. partner API events
4. settlement holds and disputes
5. SLA breach logs
6. refund and credit-note records
7. partner scorecard history

## Final Reading

The partnership framework is backtestable because each clause can be reduced to:

```text
partner type -> authority -> economics -> data scope -> custody/regulatory path -> dispute/settlement guardrail -> approve/review/block
```
