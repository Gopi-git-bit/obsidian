---
type: memo
domain: governance
scope: archive_candidates
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[VAULT_AUDIT_REPORT]]"
  - "[[Note Status Policy for Current Project]]"
tags:
  - archive
  - cleanup
  - current-project
  - source-of-truth
---

# Archive Candidates - First Pass

This list does not move or delete anything.

It marks notes or note classes that should be reviewed later for archive treatment once source-of-truth governance is stable.

## Candidate Classes

### 1. Raw chat or extract notes that now have current-project replacements

Examples:

- raw PRD or workflow extracts under `01_Inbox`
- old chat-derived notes whose durable ideas are already distilled into `00_System`, `04_AI_Agents`, or `05_Algorithms`

### 2. Stack-locked legacy instructions that conflict with repo reality

Examples:

- Django/DRF-first implementation drafts not restated by current FastAPI-aligned notes

### 3. Older agent inventory notes that duplicate current governance

Examples:

- frozen role inventories or agent notes that look authoritative but are now superseded by [[Agent Governance and Operating Model for Current Project]]

### 4. Zero-value inbox residue

Examples:

- empty untitled notes
- transient chat scratch notes that do not contribute to the active graph

## Review Rule

A note should only move to archive when all three are true:

1. a canonical or supporting replacement already exists
2. the note is linked in this register or a later archive decision note
3. removing it from active navigation will not break the active project reading path

## First-Pass Recommendation

Keep broad research in place.

Focus archive review on low-value residue and clearly superseded builder-facing drafts first.