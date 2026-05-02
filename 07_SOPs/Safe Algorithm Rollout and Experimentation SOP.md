---
type: sop
domain: algorithm_governance
scope: rollout_experimentation
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[SOPs Hub]]"
  - "[[Algorithms Hub]]"
  - "[[Technology Stack Hub]]"
tags:
  - algorithm-rollout
  - shadow-mode
  - canary
  - ab-testing
  - ims
  - safety
  - zippy-logistics
source_files:
  - "C:\\Users\\user\\Downloads\\new -chatgpt .txt"
---

# Safe Algorithm Rollout and Experimentation SOP

## Purpose

This SOP extracts the safe rollout discipline from `new -chatgpt .txt`.

It applies to:

- IMS return-trip matching
- geohash/spatial filtering upgrades
- pricing algorithm changes
- SLA risk scoring
- dispute scoring
- driver/provider scorecards
- future VRP or optimization engines

The goal is to improve operations without corrupting workflow truth.

## Core Principle

Algorithms should be launched gradually.

```text
observe
-> shadow
-> canary
-> controlled rollout
-> full rollout
-> monitor
-> rollback if needed
```

No algorithm should receive full operational authority on day one.

## Algorithm Safety Rules

1. New algorithms must not bypass backend policy.
2. New algorithms must emit explainable output.
3. New algorithms must log input references, version, and output.
4. New algorithms must support rollback.
5. New algorithms must have success and failure metrics before launch.
6. New algorithms must run in shadow mode before affecting users.
7. High-risk decisions require human or policy approval.

## Launch Phases

## Phase 1: Shadow Mode

Purpose:

- test algorithm recommendations without affecting users or workflow

Behavior:

- run algorithm on real events
- log suggested result
- do not create operational offers
- do not mutate state
- do not notify users

Use for:

- return-trip suggestions
- geohash candidate filtering
- dispute scoring
- SLA breach detection

Exit criteria:

- outputs reference valid records
- no major data integrity errors
- recommendation rate is plausible
- latency is within threshold
- ops/product review agrees with output quality

## Phase 2: Canary Mode

Purpose:

- expose algorithm to a small controlled slice

Behavior:

- enable for 5% to 10% of eligible traffic
- select by deterministic hash or explicit allowlist
- monitor closely
- keep instant rollback available

Example return-trip canary:

```text
5% of eligible drivers receive actual return-trip offers
95% remain in shadow/log-only mode
```

Exit criteria:

- no workflow corruption
- no duplicate offers
- no bad state transitions
- acceptance/conversion is not dangerously low
- support tickets do not spike

## Phase 3: Ramp-Up

Purpose:

- increase traffic gradually after canary success

Recommended ramp:

```text
5% -> 10% -> 25% -> 50% -> 100%
```

Each step should have:

- observation period
- metric review
- rollback decision
- owner approval

## Phase 4: Full Launch

Purpose:

- make algorithm normal operating path

Requirements:

- dashboard active
- alert thresholds active
- rollback switch active
- docs updated
- support and ops trained

## Rollback Triggers

Rollback if:

- system creates duplicate offers
- transition rejection rate spikes
- latency exceeds threshold
- acceptance rate collapses below agreed floor
- customer complaints spike
- driver/provider complaints spike
- finance blockers increase unexpectedly
- ops cannot explain recommendations
- audit data is missing or corrupted

For return-trip v1:

| Metric | Suggested Watch |
|---|---|
| p99 match latency | under 500 ms for deterministic v1 |
| acceptance rate | investigate if below 10% |
| duplicate pending offer count | must be zero |
| discount reversal rate | investigate if rising |
| support complaint spike | immediate review |

## Configuration Discipline

Algorithm parameters should be centralized and versioned.

For return-trip v1:

| Parameter | Default |
|---|---:|
| max search radius | 30 km |
| max wait window | 180 minutes |
| min score threshold | 40 |
| offer TTL | 15-30 minutes |

Do not change live parameters casually.

Parameter changes should record:

- previous value
- new value
- reason
- owner
- timestamp
- expected impact

## Observability Requirements

Every algorithm launch should emit:

- algorithm version
- input count
- candidate count
- selected candidate
- score/confidence
- reason codes
- latency
- accepted/rejected outcome
- downstream failure or success

Core metrics:

- p50/p95/p99 latency
- recommendation rate
- conversion rate
- rejection rate
- error rate
- rollback count
- business KPI impact

## Geohash And Spatial Filtering Policy

The source contains a large geohash optimization plan.

Current interpretation:

- geohash/spatial indexes are performance tools, not decision logic
- exact distance checks should remain after coarse filtering
- fallback to direct distance calculation must exist
- geohash rollout should be A/B tested

Use geohash when:

- candidate order volume makes naive distance calculation slow
- p95/p99 latency is above threshold
- order density supports spatial indexing

Do not use geohash to:

- skip vehicle compatibility
- skip time window validation
- bypass exact final distance check

## A/B Testing Policy

Use A/B testing for performance or recommendation changes only after shadow safety.

Test examples:

- original candidate filter vs geohash filter
- old score weights vs new score weights
- old ETA display vs new ETA model

Minimum A/B fields:

- experiment ID
- algorithm variant
- actor/order ID
- assignment method
- outcome
- latency
- business metric

Decision options after test:

- adopt
- reject
- extend test
- roll back
- keep for specific lanes only

## Advanced Optimization Policy

Future VRP or OR-Tools style optimization should be treated as v2, not MVP.

Use only when:

- there are enough simultaneous vehicles and orders
- deterministic v1 is measurably suboptimal
- ops can supervise and explain decisions
- runtime is bounded
- fallback to v1 exists

Recommended v2 pattern:

```text
real-time v1 handles immediate opportunities
batch v2 runs every 10-15 minutes for high-volume clusters
v1 wins if it already created a valid accepted offer
v2 creates offers, not state mutations
```

## Human Review Rules

Human approval is required for:

- high-value settlement impact
- refund recommendation
- dispute closure
- service-level exception
- override of deterministic policy
- new algorithm full rollout

AI and optimization output should be shown as:

- recommendation
- evidence
- confidence
- reason codes
- risk flags

not as hidden automation.

## Launch Checklist

Before canary:

- policy owner assigned
- config locked
- metrics dashboard exists
- rollback method tested
- duplicate protection exists
- idempotency keys implemented
- audit event emitted
- support playbook ready

Before full launch:

- canary passed
- no critical incidents
- ops trained
- docs updated
- dashboard monitored for at least one full operating cycle
- leadership/product owner signs off

## Bottom Line

Zippy should launch operational intelligence like this:

```text
deterministic first
shadow before canary
canary before scale
measure before optimize
rollback before damage
```

This keeps the platform stable while it becomes smarter.

