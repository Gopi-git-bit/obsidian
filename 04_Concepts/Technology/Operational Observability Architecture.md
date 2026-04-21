---
type: concept
domain: technology
decision_value: high
status: verified
related_hubs:
  - Technology Stack Hub
  - Operations Strategy Hub
tags:
  - concept
  - observability
  - reliability
  - prometheus
  - grafana
  - alerting
---

# Operational Observability Architecture

## Purpose

Define the minimum monitoring, dashboard, and alerting architecture required to operate an autonomous logistics platform safely.

## Why It Matters

- Reliability gaps become harder to detect when routing, matching, payments, telemetry, and AI decisions are distributed.
- State safety is not real unless illegal transitions, schema violations, and audit failures are visible immediately.
- Teams need deploy and rollback decisions tied to measurable service health, not intuition.

## Core Principle

If a critical metric is missing, that is a reliability gap rather than just a dashboard gap.

## Required Dashboard Domains

| Domain | What It Should Answer |
|--------|------------------------|
| Platform overview | Is the platform available and fast enough overall |
| Gateway and contract safety | Are requests and responses staying within API contracts |
| State-machine health | Are illegal transitions being blocked and legal ones flowing |
| Payments and settlement integrity | Is money processing safely without duplicates or mismatches |
| Realtime and GPS streams | Is live tracking fresh and trustworthy |
| Background jobs and DLQ | Are async workflows succeeding and recovering cleanly |
| Audit and data integrity | Can the platform still trust its audit trail |
| Error budget and canary health | Is the system healthy enough to keep deploying |

## Recommended Metric Families

| Metric Family | Example Concern |
|--------------|-----------------|
| HTTP availability and latency | API uptime, p95 and p99 latency, 5xx rate |
| Schema validation failures | Request or response shape drift at the gateway |
| State-transition metrics | Legal transitions, rejected illegal attempts, terminal-state violations |
| Payment safety metrics | Duplicate charges, settlement mismatch, refund lag |
| Realtime telemetry metrics | WebSocket success, stale GPS, location-update rate |
| Background execution metrics | Celery success, retry exhaustion, DLQ size |
| Audit integrity metrics | Hash-chain failure, forbidden DB mutation attempt |
| Model and rollout metrics | Canary degradation, confidence drift, error-budget burn |

## Governance Signals

| Signal | Operational Meaning |
|--------|---------------------|
| Schema violation above zero | Contract safety incident |
| Illegal transition success above zero | State-control failure |
| Audit hash violation above zero | Integrity emergency |
| Duplicate charge above zero | Financial-severity incident |
| Fast burn rate above threshold | Freeze deployment and investigate |
| Canary worse than baseline | Roll back or hold promotion |

## Design Rules

1. Separate control-plane health from business-outcome health.
2. Keep financial-integrity dashboards independent from generic API dashboards.
3. Treat state-machine monitoring as first-class, not just an application log query.
4. Make DLQ and retry exhaustion visible instead of burying them inside worker metrics.
5. Tie canary rollout and release decisions to explicit error-budget and regression signals.

## Implementation Pattern

- Use Prometheus for metrics collection and alert evaluation.
- Use Grafana for operator-facing dashboards grouped by domain.
- Emit metrics from gateway, backend, Celery workers, realtime services, and audit controls.
- Keep alert severity aligned with business risk, especially for money, state, and audit integrity.

## Related Notes

- [[TMS Execution Architecture]]
- [[Fallback & Resilience Architecture]]
- [[Authoritative Database Schema]]
- [[Hyperparameter Tuning System]]
- [[ETA Prediction Logic]]

## Related Hubs

- [[Technology Stack Hub]]
- [[Operations Strategy Hub]]
