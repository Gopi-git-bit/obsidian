---
type: hub
domain: master
scope: strategic
status: active
last_updated: 2026-04-30
---

# Logistics Brain - Master Index

Central navigation note for the Obsidian-style logistics vault in this workspace.

## Vault Purpose

This vault serves as:

- Operations knowledge base for Indian logistics
- Decision support system for scenario-based work
- Retrieval layer for AI and agent workflows
- Strategy reference for pricing, fleet, transport, finance, market analysis and analytics
- Build reference for dashboards, data models and route intelligence

## Current Vault Snapshot

- **Vault markdown note count:** 282 notes across `00_` to `12_` folders
- **SQL/data-model files:** 5 SQL files in `10_Data_Model/SQL`
- **Dashboard asset files:** 9 Tableau/Power BI sample/theme/README assets
- **Primary focus:** Indian logistics operations, platform design, route intelligence, finance lifecycle, data model and execution playbooks
- **Known issue:** some older/deeper notes still reference planned notes that do not yet exist

## Vault Architecture

```text
Raw sources
-> Concepts and market intelligence
-> Algorithms and agent rules
-> SOPs and business models
-> Data model and dashboards
-> Operating cockpit / execution index
```

## Linear Reading Path

Use this order when onboarding yourself, an agent, or a teammate.

| Order | Layer | Start Here |
|---:|---|---|
| 1 | System orientation | [[Logistics Brain - Linear Execution Index]] |
| 2 | Market thesis | [[South India Tier 2-3 City Pair Freight Atlas Framework]] |
| 3 | Directed demand | [[South India Trading Pair City Research System]] |
| 4 | Return-trip logic | [[Return Trip Analogy - From Empty Return to Earning Loop]] |
| 5 | Triangle engine | [[Triangle Route Engine for Return Trip Optimization]] |
| 6 | Deadhead intelligence | [[Deadhead Reduction Intelligence Layer for Tier 2-3 Freight]] |
| 7 | Hub/warehouse intelligence | [[South India Logistics Hub Intelligence Framework]] |
| 8 | Industry/cargo compatibility | [[Industry Hub Cargo Matrix for Triangle Backhaul Optimization]] |
| 9 | Delay and promise logic | [[Common Delay Metrics for South India Transportation Planning]] |
| 10 | Delay-to-action rules | [[Delay-to-Action Optimization Framework for Logistics Agents]] |
| 11 | Lane scorecards | [[Lane Reliability Scorecard for Return Trip Promise Engine]] |
| 12 | Finance/invoice lifecycle | [[Finance and Invoice Event Layer for Logistics Platform]] |
| 13 | Analytics schema | [[Zippy Logistics Analytics Star Schema]] |
| 14 | Calendar/seasonality | [[dim_time India Logistics Calendar]] |
| 15 | Control dashboard | [[Corridor Delay Trends and Performance Dashboard Template]] |
| 16 | Tableau implementation | [[Tableau Workbook Spec: ZippyLogitech Corridor Delay Analytics]] |

## Hub Navigation

| Hub | Purpose |
|---|---|
| [[Indian Logistics Ecosystem Hub]] | India-specific context |
| [[Operations Strategy Hub]] | Core operations logic |
| [[Algorithms Hub]] | Matching, pricing, routing and scoring logic |
| [[Scenario Playbooks Hub]] | Decision scenarios |
| [[Business Models Hub]] | Revenue and market strategy |
| [[AI Agents Hub]] | Multi-agent logic |
| [[Fleet & Transport Hub]] | Fleet operations |
| [[Compliance & Regulation Hub]] | Legal requirements |
| [[Customer Problems Hub]] | Customer pain points |
| [[Technology Stack Hub]] | Tech architecture |
| [[Skills Hub]] | Team capability building |
| [[Market Intelligence Hub]] | Ecosystem data |
| [[SOPs Hub]] | Operating procedures |

## Active Build Areas

| Area | Folder | Status |
|---|---|---|
| Return-trip intelligence | `05_Algorithms/Backhaul`, `09_Market_Intelligence` | active |
| Corridor intelligence | `09_Market_Intelligence`, `12_Dashboards` | active |
| Finance + invoice event layer | `04_AI_Agents` | active |
| Analytics/data model | `10_Data_Model` | active |
| Tableau/Power BI dashboards | `12_Dashboards` | active |
| Legacy concept agents | `10_AI_Agents` | legacy/reference |

## System Notes

- [[Tag Dictionary]] - tagging standards
- [[Linking Rules]] - internal linking conventions
- [[Note Templates]] - note creation patterns
- [[VAULT_AUDIT_REPORT]] - current audit and alignment status
- [[Logistics Brain - Linear Execution Index]] - clean linear product reading path

## Daily Workflow

1. Capture raw notes in `01_Inbox` or directly in the right domain folder.
2. Convert useful content into concepts, algorithms, data models, dashboards, SOPs, or market intelligence.
3. Link new notes upward to this master index or a relevant hub.
4. If the note belongs to the return-trip stack, add it to [[Logistics Brain - Linear Execution Index]].
5. Use dashboards and index notes to navigate, not folders alone.

## Contribution Rules

1. Start from [[Note Templates]] or a domain-specific template in `00_System/Templates`.
2. Add frontmatter that reflects note type, domain and status.
3. Link upward to a relevant hub or index.
4. Add at least two meaningful related links when possible.
5. If a referenced note does not exist yet, either create it soon or replace the link with an existing note.

---

*Treat this index as the front door to the vault, not as the final source of every metric.*

## Active Canvas Maps

- [[Return Trip Triangle Engine Operating Canvas]] - visual operating map for trading pairs, triangle engine, hub/warehouse data, delay data, decision rules and dashboards.
