---
type: audit_report
domain: governance
scope: topic_collisions
status: active
last_updated: 2026-05-17
related_hubs:
  - "[[Current Project Navigation Hub]]"
  - "[[Current Architecture Source of Truth]]"
  - "[[Note Status Policy for Current Project]]"
tags:
  - source-of-truth
  - collisions
  - cleanup
  - current-project
---

# Topic Collision Register for Current Project

| Topic | Canonical owner | Supporting notes | Conflict pattern | First-pass decision |
|---|---|---|---|---|
| backend stack | [[Current Architecture Source of Truth]], [[Backend Structure for Current Project]] | [[Codex Context Bundle for Current Project]], [[Backend Gap Analysis Against Current Target]], backend README | old Django/DRF instructions survive in source drafts while repo reality is FastAPI | FastAPI is authoritative; Django-first drafts are reference only unless restated in current-project notes |
| lifecycle and transition gateway | [[API and Event Contract for Current Project]] | [[07_State_Machine]], [[Backend Structure for Current Project]], backend order transition code | multiple notes describe lifecycle, but not all are framed as the builder contract | API and Event Contract owns the canonical gateway; state-machine notes remain supporting/domain logic |
| agent governance | [[Agent Governance and Operating Model for Current Project]] | [[02_Agentic_AI_Application]], [[Role and Permission Matrix for Current Project]], communication and escalation notes | summary notes and older agent inventories can look equally authoritative | governance note owns forbidden actions and boundaries; other notes must summarize or specialize |
| frontend contracts | [[Frontend UI Blueprint for Current Project]], [[Frontend Architecture for Current Project]] | role-specific frontend notes, [[Frontend-to-Backend Flow Map for Current Project]] | raw frontend specs and role-specific notes overlap on screens and actions | UI blueprint owns state-driven rules; role notes own per-surface details |
| return-trip operations | [[Return Trip Streamlined Operations v1]] | [[03_ReturnTrip_Algorithm]], [[08_Database_Schema]], [[10_API_Reference]], [[02_Agentic_AI_Application]] | algorithm, schema, API, and ops notes all restate pieces of the same flow | streamlined operations note owns v1 operational flow; algorithm note owns scoring details |
| database authority | [[Current Architecture Source of Truth]], [[Zippy Logistics Operational Core Schema]] | [[08_Database_Schema]], SQL docs in `10_Data_Model/SQL`, [[Authoritative Database Schema]] | high-level schema summaries and legacy schema drafts overlap | operational core schema is builder-facing database truth; summaries remain supporting/reference |
| async orchestration | [[Async Event and Worker Orchestration for Current Project]] | [[Backend Structure for Current Project]], [[API and Event Contract for Current Project]] | older Celery examples can look like workers own workflow truth or mutate state directly | async note owns worker discipline; backend and API notes remain supporting |
| testing strategy | [[Testing and Verification Strategy for Current Project]] | [[Current Architecture Source of Truth]], [[Backend Structure for Current Project]], [[MVP Build Contract for Current Project]] | happy-path or code-presence testing can be mistaken for workflow verification | testing note owns verification depth and required failure-path coverage |

## Priority

Resolve these collisions in this order:

1. backend stack
2. lifecycle and transition gateway
3. agent governance
4. frontend contracts
5. return-trip operations
6. database authority
7. async orchestration
8. testing strategy
