---
type: memo
domain: documentation
scope: coding_context
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
tags:
  - codex
  - context
  - documentation
  - source-of-truth
---

# Codex Context Bundle for Current Project

## Purpose

This note distills the useful idea from `markdown file.txt`:

```text
future coding work should read a small, authoritative context bundle instead of relying on old scattered drafts
```

That idea is still strong.

What is not carried forward:

- old Django-specific assumptions
- old file names as mandatory truth
- stack-locked coding instructions

## Why This Matters

The project now has multiple refined notes that replaced older drafts.

Without a compact context bundle, future coding work may accidentally read:

- outdated PRDs
- outdated backend assumptions
- duplicated schema drafts
- old agent inventories

## Current Recommended Context Bundle

For future coding sessions, the minimum source-of-truth bundle should be:

1. [[Current Architecture Source of Truth]]
2. [[Backend Structure for Current Project]]
3. [[Zippy Logistics Operational Core Schema]]
4. [[Agent Governance and Operating Model for Current Project]]
5. [[On-Time Delivery Control Tower Strategy for Multimodal Freight]]
6. [[Frontend Architecture for Current Project]]
7. [[Frontend UI Blueprint for Current Project]]
8. [[Return Trip Streamlined Operations v1]]
9. [[Safe Algorithm Rollout and Experimentation SOP]]

## Optional Supporting Notes

Use these when the task specifically touches them:

- [[Corridor Matching Agent with PydanticAI]]
- [[Founder SWOT + Moat + Investor Score Memo]]
- pricing and lane-reliability notes under `05_Algorithms`
- data-model SQL files under `10_Data_Model/SQL`

## Suggested Folder-Oriented Context Pack

If you want a future Codex or agent coding bundle, the clean current version is:

```text
/codex-context/
  00_CURRENT_ARCHITECTURE_SOURCE_OF_TRUTH.md
  01_BACKEND_STRUCTURE.md
  02_DATABASE_SCHEMA.md
  03_AGENT_GOVERNANCE.md
  04_SLA_AND_CONTROL_TOWER.md
  05_FRONTEND_CONTRACTS_AND_UI_BLUEPRINT.md
  06_RETURN_TRIP_AND_MATCHING_RULES.md
  07_SAFE_ALGORITHM_ROLLOUT.md
  08_NON_NEGOTIABLES.md
```

## What Each File Should Mean

### 00 Current Architecture Source Of Truth

Defines:

- what the project is
- what is in scope
- what is out of scope
- which notes override older drafts

### 01 Backend Structure

Defines:

- backend layers
- service boundaries
- workflow ownership
- module structure expectations

### 02 Database Schema

Defines:

- accepted operational domains
- core tables
- event and audit structures
- SLA, pricing, finance, and alert data

### 03 Agent Governance

Defines:

- bounded autonomy
- agent roles
- forbidden actions
- escalation rules

### 04 SLA And Control Tower

Defines:

- promise windows
- breach logic
- alert rules
- backup and buffer expectations

### 05 Optional Matching And Pricing

Defines:

- lane-aware pricing context
- return-load and triangle logic
- compatibility and matching rules

### 05 Frontend Contracts And UI Blueprint

Defines:

- frontend is request/render only
- buttons request transitions; backend decides
- realtime mirrors backend events and does not mutate truth
- driver telemetry is passive and never changes order state

### 06 Return Trip And Matching Rules

Defines:

- deterministic return-trip v1
- IMS suggestion boundaries
- OMS metadata-only offer flow
- loop-aware but per-order finance rules

### 07 Safe Algorithm Rollout

Defines:

- shadow mode
- canary
- ramp-up
- rollback triggers
- A/B testing and geohash/spatial filtering discipline

### 08 Non-Negotiables

Defines:

- do not invent states
- do not bypass transition gateway
- do not mutate state from frontend, agents, workers, or realtime streams
- do not treat AI output as authority
- do not implement old framework assumptions when current repo reality differs

## Practical Coding Rule

When future implementation work starts, the coding context should prefer:

1. current architecture notes
2. refined schema notes
3. current backend structure
4. current agent governance

It should not prefer:

- raw historical drafts
- stack-specific old instructions
- duplicated schema variants

## Extracted Additions From `new -chatgpt  (1).txt`

This source adds a useful implementation-governance idea:

```text
Codex should read a frozen context bundle before writing code
and all generated code should obey a single transition gateway
```

Keep these durable rules:

1. Use a small context bundle as implementation law.
2. Do not rely on conversational memory.
3. The frontend must not add states.
4. Workers and agents request transitions; they do not mutate state directly.
5. Realtime is event broadcast, not command channel.
6. Driver location is telemetry, not control.
7. Tests should attempt illegal transitions, skipped transitions, terminal-state mutation, and duplicate idempotency.

Do not carry forward blindly:

- Django/DRF as mandatory, because the current repo is FastAPI.
- claims that backend/frontend are complete.
- generated code snippets that conflict with the current SQLAlchemy/FastAPI structure.

## Best Current Interpretation Of The Old File

The strongest idea in `markdown file.txt` is not its old generated code direction.

It is this:

```text
freeze a small set of authoritative notes and treat them as the law of the system during implementation
```

That idea fits the current project extremely well.

## Bottom Line

`markdown file.txt` does help fill a gap:

- not by adding new business logic
- not by adding new schema truth
- but by clarifying how future coding work should consume the refined architecture safely

That makes it a documentation-governance contribution, not a product-architecture change.
