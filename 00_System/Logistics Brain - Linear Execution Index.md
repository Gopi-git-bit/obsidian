---
type: linear_index
domain: vault_navigation
status: active
created_at: 2026-04-30
---
# Logistics Brain - Linear Execution Index

## Purpose

This note is the straight-line path through the Zippy logistics knowledge base.

Use it when the vault feels too wide and you need to understand the system in the order it should be built.

## Product Logic in One Line

```text
Market lanes -> Directed demand -> Return loops -> Reliability gates -> Finance lifecycle -> Data model -> Dashboards -> Operating system
```

## Phase 1: Market and Corridor Brain

| Step | Note | Why It Comes Here |
|---:|---|---|
| 1 | [[South India Tier 2-3 City Pair Freight Atlas Framework]] | Defines the freight atlas structure |
| 2 | [[South India City Pair Master]] | Gives the master corridor list |
| 3 | [[South India Trading Pair City Research System]] | Converts city pairs into research system |
| 4 | [[Directed Lane Master]] | Forces directional lane thinking |
| 5 | [[Tiruppur to Chennai]] | Example strong outbound lane |
| 6 | [[Chennai to Tiruppur]] | Example weak return lane |

## Phase 2: Return-Trip and Deadhead Engine

| Step | Note | Why It Comes Here |
|---:|---|---|
| 7 | [[Return Trip Analogy - From Empty Return to Earning Loop]] | Explains the business intuition |
| 8 | [[Triangle Route Engine for Return Trip Optimization]] | Core A -> B -> C -> A logic |
| 9 | [[Triangle Route Master]] | Master dashboard for triangle candidates |
| 10 | [[Tiruppur Chennai Coimbatore Triangle Route]] | First detailed triangle example |
| 11 | [[Triangle Backhaul Technical Implementation Addendum]] | Technical implementation details |
| 12 | [[High-Volume Trading Pair Route Planning Technical Addendum]] | Trading-pair scoring and route planning |
| 13 | [[Deadhead Reduction Intelligence Layer for Tier 2-3 Freight]] | Expands from triangle to deadhead KPIs |

## Phase 3: Hub, Warehouse and Industry Intelligence

| Step | Note | Why It Comes Here |
|---:|---|---|
| 14 | [[South India Warehouse and Industrial Cluster Intelligence Framework]] | Cluster-aware routing layer |
| 15 | [[Warehouse Placement Strategy for Triangle Backhaul Optimization]] | Warehouse placement logic |
| 16 | [[South India Logistics Hub Intelligence Framework]] | Hub-aware route closure layer |
| 17 | [[Logistics Hub Master]] | Hub dashboard |
| 18 | [[Madhavaram Logistics Hub]] | Example hub note |
| 19 | [[Industry Hub Cargo Matrix for Triangle Backhaul Optimization]] | Cargo compatibility rules |
| 20 | [[Industry Cargo Compatibility Dashboard]] | Industry/cargo dashboard |
| 21 | [[Manufacturing Hub Support Matrix for Return Trip Optimization]] | Manufacturing support matrix |

## Phase 4: Delay, Reliability and Promise Engine

| Step | Note | Why It Comes Here |
|---:|---|---|
| 22 | [[Common Delay Metrics for South India Transportation Planning]] | Defines atomic delay metrics |
| 23 | [[Traffic Signal Delay Metrics Analogy for Logistics Reliability]] | Explains delay as operating signal |
| 24 | [[Delay-to-Action Optimization Framework for Logistics Agents]] | Maps delay patterns to agent levers |
| 25 | [[Lane Reliability Scorecard for Return Trip Promise Engine]] | Converts delays into lane grades |
| 26 | [[Lane Reliability Scorecard Master]] | Scorecard dashboard |
| 27 | [[Route Chain Timing Evaluation Template]] | Template for evaluating handoff timing |
| 28 | [[Delay Event Template]] | Template for raw delay events |

## Phase 5: Finance, Invoice and Settlement Trust Layer

| Step | Note | Why It Comes Here |
|---:|---|---|
| 29 | [[Payment Invoice and Accounting Agent Architecture for Logistics Platform]] | Payment/invoice/accounting agent view |
| 30 | [[Finance and Invoice Event Layer for Logistics Platform]] | Unified money lifecycle |
| 31 | [[Payment Settlement Agent]] | Settlement ownership and agent role |

## Phase 6: Data Model and Analytics Layer

| Step | Note | Why It Comes Here |
|---:|---|---|
| 32 | [[Zippy Logistics Analytics Star Schema]] | Data model overview |
| 33 | [[dim_time India Logistics Calendar]] | Calendar/seasonality decision signal |
| 34 | `10_Data_Model/SQL/zippy_logistics_analytics_star_schema.sql` | Production BI schema |
| 35 | `10_Data_Model/SQL/populate_dim_time_india_logistics.sql` | India calendar population script |
| 36 | `10_Data_Model/SQL/corridor_delay_dashboard_materialized_views.sql` | BI performance views |

## Phase 7: Dashboards and Control Tower

| Step | Note | Why It Comes Here |
|---:|---|---|
| 37 | [[Corridor Delay Trends Essential Metrics Framework]] | Dashboard metric hierarchy |
| 38 | [[Corridor Delay Trends and Performance Dashboard Template]] | Main dashboard specification |
| 39 | [[Transport Control Tower KPI Framework]] | Control tower KPI layer |
| 40 | [[Tableau Workbook Spec: ZippyLogitech Corridor Delay Analytics]] | Tableau implementation guide |
| 41 | [[Tableau Packaged Workbook Data Source Guide]] | TWBX packaging guide |
| 42 | [[README: ZippyLogitech Corridor Delay Analytics TWBX]] | Workbook documentation |
| 43 | [[Obsidian Embed - Tableau Corridor Delay Dashboard]] | Dashboard embed note |

## Phase 8: Operations and SOPs

| Step | Note | Why It Comes Here |
|---:|---|---|
| 44 | [[On-Time Delivery Control Tower Strategy for Multimodal Freight]] | Operating control tower strategy |
| 45 | [[SOP - Assign Vehicle to Order]] | Dispatch execution |
| 46 | [[SOP - Escalate Delayed Shipment]] | Delay escalation |
| 47 | [[SOP - Verify Shipment Documents]] | Document control |
| 48 | [[How to Keep Logistics Operational Cost Low]] | Cost discipline |

## Build Priority

If you are implementing, follow this order:

```text
1. Directed lanes
2. Triangle candidates
3. Delay event capture
4. Lane reliability scorecards
5. Finance/invoice event layer
6. Analytics star schema
7. Tableau/Power BI dashboards
8. n8n/agent automation
```

## Placement Rule

| New Content Type | Put It In |
|---|---|
| Business intuition or analogy | `04_Concepts` |
| Algorithm, scoring, agent logic | `05_Algorithms` |
| Operational process | `07_SOPs` |
| Revenue/partnership/warehouse strategy | `08_Business_Models` |
| Corridor/city/hub/industry data | `09_Market_Intelligence` |
| SQL/schema/data documentation | `10_Data_Model` |
| BI/dashboard/readme/theme/sample data | `12_Dashboards` |
| Event-driven agent architecture | `04_AI_Agents` |

## Current Structural Note

Legacy `10_AI_Agents` notes have been moved out of the active numbered vault and archived under `99_Archive/Legacy_AI_Agents_2026-04-30`. New agent architecture notes should go in `04_AI_Agents`.

## Canvas Companion

Use [[Return Trip Triangle Engine Operating Canvas]] as the visual companion to this linear index. The canvas is organized left-to-right as demand data -> route engine -> network constraints -> reliability gates -> decision -> dashboard.

