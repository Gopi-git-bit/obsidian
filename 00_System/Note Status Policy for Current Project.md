---
type: memo
domain: governance
scope: note_status_policy
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Logistics Brain - Master Index]]"
tags:
  - source-of-truth
  - governance
  - note-policy
  - current-project
---

# Note Status Policy for Current Project

## Purpose

This note defines how the active Zippy vault should classify note authority during the first source-of-truth cleanup pass.

The goal is not to shrink the research vault.

The goal is to make builder-facing truth explicit while preserving wider research and reference material.

## Status Classes

### Canonical

Use for notes that act as builder-facing truth.

Rules:

- may override older drafts when they conflict
- should be linked from [[Current Project Navigation Hub]] when relevant to the active build
- should not duplicate large chunks of older PRDs or raw chat extracts
- should state current repo reality when implementation exists

### Current-Project Supporting

Use for notes that expand canonical notes without replacing them.

Rules:

- may add detail, examples, or subsystem-specific guidance
- must not redefine core lifecycle, stack, role, or API truth against the canonical notes
- should link upward to at least one canonical note

### Research / Reference

Use for broad ecosystem research, source extracts, exploratory frameworks, or old drafts with useful context.

Rules:

- may remain deep and wide
- should not be used directly as build authority
- should be cited or distilled by canonical notes when their ideas remain valid

### Archive Candidate

Use for notes that are outdated, superseded, duplicated, or legacy enough that they may later move to archive after review.

Rules:

- do not delete in this first pass
- do not use directly for implementation
- log them in an archive candidate register before any move

## Current Canonical Set

For active build work, the primary canonical set is:

1. [[Current Project Navigation Hub]]
2. [[Current Architecture Source of Truth]]
3. [[Master PRD Distillation for Current Project]]
4. [[Backend Structure for Current Project]]
5. [[Frontend Architecture for Current Project]]
6. [[Frontend UI Blueprint for Current Project]]
7. [[API and Event Contract for Current Project]]
8. [[Role and Permission Matrix for Current Project]]
9. [[Codex Context Bundle for Current Project]]
10. [[MVP Build Contract for Current Project]]
11. [[Async Event and Worker Orchestration for Current Project]]
12. [[Testing and Verification Strategy for Current Project]]

## Topic Ownership Rules

- Backend stack truth belongs to [[Current Architecture Source of Truth]] and [[Backend Structure for Current Project]].
- Frontend state-driven UI truth belongs to [[Frontend UI Blueprint for Current Project]].
- API, event envelope, and transition gateway truth belongs to [[API and Event Contract for Current Project]].
- Role and permission truth belongs to [[Role and Permission Matrix for Current Project]].
- Agent boundary and forbidden-action truth belongs to [[Agent Governance and Operating Model for Current Project]].
- Return-trip v1 operating flow truth belongs to [[Return Trip Streamlined Operations v1]].
- Async worker and Celery orchestration truth belongs to [[Async Event and Worker Orchestration for Current Project]].
- Testing and verification truth belongs to [[Testing and Verification Strategy for Current Project]].

## First-Pass Enforcement

Apply this policy first in:

- `00_System`
- `04_AI_Agents`
- `05_Algorithms`
- `02_Sources`

These are the highest-conflict zones for current project work.

## Implementation Rule

When a raw source file or older draft overlaps with a current-project note:

```text
preserve the source
-> distill the durable idea
-> mark the current-project note as canonical or supporting
-> downgrade the source to reference unless it is still the only place the idea exists
```
