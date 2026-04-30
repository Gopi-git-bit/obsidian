---
type: algorithm
domain: risk
status: draft
related_hubs:
  - Algorithms Hub
  - Technology Stack Hub
  - Operations Strategy Hub
tags:
  - partnership-health
  - governance
  - collaboration
  - supervisor-agent
  - audit
---

# Partnership Health Score Calculator

## Purpose

Convert live partnership metrics into a deterministic action category for Zippy's governance layer.

This calculator is the implementation companion to [[PartnershipAgreement.yaml]] and the operational health layer inside [[Collaboration Risk Opportunity Balance Framework]].

Implementation artifact: [[health_score_calculator]]

## Inputs

| Metric | Meaning | Default Minimum |
|--------|---------|-----------------|
| operational | SLA compliance, fulfillment rate, dispute frequency | 70 |
| financial | settlement accuracy, margin health, payout timeliness | 75 |
| compliance | KYC status, data-sharing scope, audit pass rate | 80 |
| relationship | communication responsiveness, satisfaction, escalation rate | 65 |

All metric inputs are clamped to `0-100`. Non-finite values are treated as `0` so a bad integration cannot silently inflate health.

## Weights

| Dimension | Weight |
|-----------|--------|
| operational | 0.35 |
| financial | 0.30 |
| compliance | 0.20 |
| relationship | 0.15 |

These weights match the governance section of [[PartnershipAgreement.yaml]].

## Threshold Actions

| Score Range | Category | Action |
|-------------|----------|--------|
| 75-100 | expand | consider increasing corridor, volume, or integration depth |
| 40-74 | maintain | keep current scope and monitor |
| 20-39 | reduce_exposure | lower financial cap, tighten SLA checks, schedule emergency ops sync |
| below 20 | exit | initiate wind-down procedure |

## Output Contract

The calculator returns:

| Field | Purpose |
|-------|---------|
| score | rounded weighted score from `0-100` |
| category | `expand`, `maintain`, `reduce_exposure`, or `exit` |
| recommendations | human-readable governance next steps |
| alerts | category and metric-specific warnings |
| metric_breakdown | raw and weighted contribution per metric |
| calculated_at | ISO timestamp for audit |
| trace_id | unique trace for Supervisor Agent and n8n logs |
| version | calculator version |

## Integration Pattern

| Consumer | Use |
|----------|-----|
| Supervisor Agent | decide whether to expand, maintain, reduce, or exit |
| n8n | route health outcomes into Slack, Supabase, Finance Agent, or partner workflows |
| Grafana | display current score and category by partner |
| FIN Agent | react to reduce or exit decisions by freezing, capping, or reviewing payouts |

## Governance Note

Expansion is approval-gated even when the score is high. Reduction can auto-execute because it limits risk. Exit remains approval-gated unless a separate hard-stop condition from [[PartnershipAgreement.yaml]] is triggered.

## Related Notes

- [[Collaboration Risk Opportunity Balance Framework]]
- [[Collaboration Risk Scoring Algorithm]]
- [[PartnershipAgreement.yaml]]
- [[Partnership-Led Market Entry Framework]]
- [[Collaborative Logistics Network Framework]]
