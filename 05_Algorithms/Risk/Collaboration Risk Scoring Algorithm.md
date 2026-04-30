---
type: algorithm
domain: risk
decision_value: high
status: draft
related_hubs:
  - Algorithms Hub
  - Business Models Hub
  - Operations Strategy Hub
tags:
  - collaboration
  - risk
  - partner-scoring
  - governance
---

# Collaboration Risk Scoring Algorithm

## Purpose

Score collaboration risk, opportunity, and balance so Zippy can decide whether to expand, pilot, maintain, reduce exposure, or exit a partnership.

Derived from [[Collaboration Risk Opportunity Balance Source]] and used by [[Collaboration Risk Opportunity Balance Framework]].

## Inputs

| Input | Description |
|-------|-------------|
| strategic alignment | capability complementarity, cultural fit, long-term vision |
| operational readiness | technology compatibility, process maturity, data sharing |
| financial health | payment reliability, credit rating, insurance adequacy |
| compliance posture | regulatory compliance, audit readiness, data privacy alignment |
| opportunity potential | capacity gain, demand growth, margin improvement, network effect |
| live metrics | dispute rate, settlement errors, response time, data quality, order growth |

## Risk Score

```text
alignment_score =
  capability_complementarity * 0.40
+ cultural_fit * 0.25
+ vision_alignment * 0.35

operational_score =
  technology_compatibility * 0.35
+ process_maturity * 0.30
+ data_sharing_willingness * 0.35

financial_score =
  payment_reliability * 0.45
+ credit_strength * 0.30
+ insurance_adequacy * 0.25

compliance_score =
  regulatory_compliance * 0.40
+ audit_readiness * 0.35
+ data_privacy_alignment * 0.25

overall_strength =
  alignment_score * 0.30
+ operational_score * 0.25
+ financial_score * 0.25
+ compliance_score * 0.20

risk_score = 100 - overall_strength
```

Risk category:

| Risk Score | Category |
|------------|----------|
| 0-25 | low |
| 26-50 | medium |
| 51-75 | high |
| 76-100 | critical |

## Opportunity Score

```text
opportunity_score =
  capacity_gain * 0.25
+ demand_generation * 0.25
+ margin_or_cost_improvement * 0.20
+ service_tier_expansion * 0.15
+ network_effect_potential * 0.15
```

## Balance Score

```text
balance_score = min((opportunity_score / max(risk_score, 1)) * 100, 100)
```

Interpretation:

| Balance Score | Action |
|---------------|--------|
| 75-100 | expand scope |
| 40-74 | maintain current level and optimize |
| 20-39 | reduce exposure and add controls |
| below 20 | exit, pause, or renegotiate |

## Decision Matrix

```text
if opportunity_score >= 70 and risk_score <= 30:
  expand_aggressively
elif opportunity_score >= 70 and risk_score > 30:
  pilot_with_guards
elif opportunity_score < 70 and risk_score <= 30:
  automate_limited_scope
else:
  avoid_or_exit
```

## Pilot Guardrails

| Guardrail | Default |
|-----------|---------|
| corridor scope | one corridor |
| daily order cap | 50 or lower until stable |
| financial exposure cap | configured per partner |
| data sharing | anonymized or minimum necessary |
| system access | read-only or event-only |
| settlement review | weekly |
| exit triggers | severe incident, margin erosion, trust breach, compliance failure |

## Live Monitoring Inputs

| Metric | Risk Signal |
|--------|-------------|
| dispute rate | quality and trust risk |
| settlement error rate | financial-control risk |
| partner response time | coordination risk |
| data quality score | technology and transparency risk |
| order volume growth | opportunity signal |
| margin improvement | economics signal |
| CAC reduction | demand partnership value |
| network effect score | long-term moat signal |

## Related Notes

- [[Collaboration Risk Opportunity Balance Framework]]
- [[Collaborative Logistics Network Framework]]
- [[Partnership-Led Market Entry Framework]]
- [[Carrier Scoring Algorithm]]
- [[Payment Risk Logic]]
