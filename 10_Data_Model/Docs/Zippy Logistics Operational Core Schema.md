---
type: data_model_doc
schema: zippy_logistics_operational_core
status: active
created_at: 2026-05-01
related_hubs:
  - "[[AI Agents Hub]]"
  - "[[Algorithms Hub]]"
  - "[[Business Models Hub]]"
linked_sql:
  - zippy_logistics_operational_core_schema.sql
  - zippy_logistics_operational_triggers.sql
---
# Zippy Logistics Operational Core Schema

## Purpose

This note refines the older `data base.txt` schema draft into an operational schema that fits the current Zippy vault.

It is meant to support:

- OMS order lifecycle
- IMS availability and partner capacity
- TMS assignment, trip legs, and shipment events
- finance traceability
- lane-aware intelligence handoff into the analytics star schema

## Why The Older Draft Needed Refinement

The previous draft was useful as a starting point, but it no longer fits the current project cleanly.

Main issues:

- incomplete and duplicated `orders` definitions
- polymorphic ownership via `owner_type` and `owner_id`
- minimal support for directed lanes and corridor intelligence
- weak separation between operational transactions and analytical reporting
- no strong event model for state changes
- limited finance lifecycle support
- weak support for partner transport companies, bids, and controlled matching

## Design Principles

### 1. Separate Operational Core From Analytics

Use transactional tables for live workflows.

Use the existing star schema for BI, scorecards, and historical analytics.

```text
Operational schema -> events and facts -> analytics schema
```

### 2. Model Directed Lanes Explicitly

Do not treat city pairs as symmetric.

```text
chennai -> tiruppur != tiruppur -> chennai
```

The operational schema should preserve canonical directed lane identifiers so OMS, IMS, pricing, matching, and reliability logic all speak the same lane language.

### 3. Prefer Explicit Relationships Over Polymorphic Owners

The older draft used:

```text
owner_type + owner_id
```

That is flexible but weak for integrity.

Refinement:

- a vehicle can belong to a driver-owner or to a transport company
- use nullable foreign keys plus check constraints instead of loose polymorphism

### 4. Keep Events First-Class

Zippy’s operating model is event-driven.

That means:

- order state transitions should be logged
- trip execution should be logged
- finance events should be logged
- events should be replay-safe and idempotent

### 5. Preserve Traceability For Trust And Finance

The operational core must make it possible to answer:

- who accepted the load
- who ran the trip
- what was promised
- what changed
- what was invoiced
- what was settled

## Recommended Operational Domains

| Domain | Tables |
|---|---|
| Identity | `app_users`, `driver_profiles`, `customer_accounts`, `transport_companies` |
| Fleet | `vehicle_models`, `vehicles`, `vehicle_availability_snapshots` |
| Network | `directed_lanes`, `lane_rate_bands`, `partner_relationships` |
| Pricing intelligence | `city_market_profiles`, `lane_pricing_signals`, `price_quotes` |
| OMS | `orders`, `order_stops`, `order_documents`, `order_state_events` |
| Matching | `order_bids`, `order_matches` |
| TMS | `trips`, `trip_legs`, `shipment_events` |
| SLA and service policy | `service_levels`, `sla_policies`, `order_sla_commitments` |
| Finance | `payment_records`, `payment_intents`, `invoice_records`, `finance_events` |
| Trust and ops | `notifications`, `push_tokens`, `driver_ratings`, `transport_company_ratings`, `admin_activities`, `incident_logs`, `driver_alerts` |

## Key Refinements Over The Old Draft

### Identity Layer

- keep `app_users` as the auth root
- add role-specific profile tables
- allow a transport company to act as both customer and provider through separate profiles if needed

### User Roles In Current Project Scope

The current project needs these operational roles clearly represented:

- `customer`: consignor or shipper placing an order
- `driver`: vehicle-running executor, including owner-driver cases
- `transport_company`: fleet or partner network operator that can supply vehicles and, in some cases, place orders
- `admin`: governance, support, override, and audit actor
- `ops`: dispatcher or control-tower operator managing matching, SLA, and exception workflows

Important scope decision:

- warehouse-specific roles are out of current scope
- pure inventory or SKU roles are out of current scope

Transport company dual-role behavior is relevant to the product, but it should be represented as:

- a durable business identity in `transport_companies`
- optional current operating mode for workflow context
- not as a replacement for order, match, and trip history

### Vehicle Layer

- keep `vehicle_models` as reference metadata
- add `vehicles` as real operating assets
- support company-owned and owner-driver vehicles
- store compliance and capacity attributes needed for matching

### OMS Layer

- use one clean `orders` table only
- split multi-stop or pickup-delivery details into `order_stops`
- store documents separately
- store every state transition in `order_state_events`

### Matching Layer

- keep bids and matches separate
- a bid is a proposal
- a match is the accepted or system-scored assignment candidate

### TMS Layer

- treat a trip as an execution object, not just a match row
- support trip legs for direct and triangle routing
- capture shipment and trip events with timestamps and locations

### SLA And Service Layer

- represent service levels explicitly instead of relying only on free-text service tiers
- store lane-aware SLA policies that define promised windows and escalation requirements
- store order-level SLA commitments so the platform can measure promise vs actual execution

### Finance Layer

- separate payment, invoice, and finance event records
- keep enough granularity for order -> invoice -> settlement -> accounting trace

### Pricing Intelligence Layer

- support dynamic lane pricing without allowing free-form AI price invention
- preserve city-tier and urban-density context as explicit pricing inputs
- preserve return-load or deadhead risk as a structured pricing factor
- store quote breakdowns for audit, benchmarking, and later model tuning

### Trust And Operational Support Layer

- add notifications and push tokens for app workflows
- add ratings as a controlled trust signal for driver and partner quality
- add admin and incident logging for auditability and exception response
- add structured driver alerts for long halt, deviation, breakdown, and accident monitoring
- keep these as supporting operational tables, not as substitutes for the core event stream

## Context-Aware Extraction From DB 5

Only the parts that strictly match the current project were kept.

### What Matches The Current Project

#### 1. User-Role Clarity

This is relevant and should be explicit in both the product and schema:

- consignor or customer
- driver or owner-driver
- transport company
- admin
- operations or dispatcher

#### 2. SLA-As-Data, Not Just Documentation

This strongly matches the current vault because the project already uses:

- lane-specific promises
- buffer logic
- delivery products like economy, standard, guaranteed
- exception-based operations

This means the schema should store:

- service-level definitions
- SLA rules by lane or cargo context
- order-level promise commitments

#### 3. Logistics Operations As Structured Events

This is aligned with the current project.

The database should support operational visibility around:

- assignment
- pickup
- loading
- in-transit milestones
- proof of delivery
- delay and exception alerts

#### 4. Testing As A First-Class Validation Requirement

This is relevant, but it does not require a large permanent production schema by itself.

For the current project, testing should be defined as:

- lifecycle transition tests
- matching and pricing rule tests
- SLA promise vs delivery outcome tests
- exception and cancellation scenario tests
- event idempotency tests

### What Was Not Adopted

#### 1. Tech Stack Specificity

Any references to changing stack choices were ignored because they are unstable and not the source of truth for the data model.

#### 2. LLM or Model Assignment Advice

That was ignored because the schema should survive model changes.

#### 3. Warehouse-Oriented Expansion

Anything that pushes the product toward warehousing was excluded because the current platform scope is still vehicle owner to consignor shipment execution.

## Testing Guidance For The Current Schema

Testing belongs to the current project, but most of it should be implemented as:

- migration tests
- constraint tests
- trigger tests
- lifecycle scenario tests
- analytics reconciliation tests

The schema should support testability through:

- explicit enums
- check constraints
- state-event logs
- immutable timestamps where needed
- reproducible order and trip traces

Not every testing need requires a permanent table.

## Final Distillation From DB 6

`DB 6.txt` was mostly a refinement pass over concepts already captured.

The parts that strictly match the current project and are worth keeping are:

- optional active operating role for transport-company workflow context
- explicit provider-side fee and commission transparency, which is already covered by order pricing plus finance events
- structured driver alert records for control-tower operations
- admin-facing oversight views, which should usually be built from base tables rather than treated as the primary source of truth

The parts that were intentionally not adopted are:

- AI-agent activity and intervention tables as core schema requirements
- tech-specific or model-specific monitoring assumptions
- duplicate financial transaction patterns that overlap with `payment_records`, `payment_intents`, and `finance_events`

## Canonical Lane Shape

Recommended lane key:

```text
origin_city:destination_city:cargo_group:vehicle_class
```

Use a simpler city-to-city key only where a broader lane abstraction is acceptable.

## How This Connects To Existing Analytics Work

The operational schema should feed:

- `fact_shipment_delays`
- `fact_lane_performance_daily`
- `fact_asct_performance`
- `lane_delay_events`
- `lane_reliability_scores`

Operational-to-analytics mapping examples:

| Operational Source | Analytics Target |
|---|---|
| `shipment_events` | `lane_delay_events`, `fact_shipment_delays` |
| `trips` and `trip_legs` | `fact_asct_performance` |
| `vehicles` and `transport_companies` | `dim_vehicle`, `dim_carriers` |
| `directed_lanes` | `dim_lanes` |

## Useful Additions From The Second Legacy Draft

The second draft included a few tables that are still relevant and were folded into the refined schema:

- `payment_intents` for gateway-facing payment orchestration and idempotency
- `incident_logs` for exception and service-issue traceability
- `notifications` and `push_tokens` for mobile and app messaging workflows
- `driver_ratings` and `transport_company_ratings` for trust and service quality signals
- `admin_activities` for controlled override and audit trails

These are worth keeping because they support operational trust, not just transactional storage.

## Distilled Additions From The Third Legacy Draft

The third draft was mostly repetitive at the table level, but it added useful operational database patterns.

The important parts were not new core entities. They were:

- explicit order lifecycle enforcement
- realtime `NOTIFY` patterns for order and inventory changes
- expiry-job thinking for stale pending orders
- payment webhook locking patterns
- bounded-context separation between fleet, inventory, and orders

### What Was Kept Conceptually

#### 1. Database-Enforced Order Lifecycle

This is relevant to Zippy.

The database should reject illegal order-status jumps such as:

```text
payment_pending -> delivered
```

That belongs in trigger or service-guard logic, not just frontend logic.

#### 2. Realtime Event Emission

The draft's `LISTEN/NOTIFY` idea is useful for:

- order updates
- payment updates
- shipment status changes
- incident alerts

This fits the event-driven operating model already used by the vault.

#### 3. Timeout And Expiry Handling

Pending orders should not wait forever.

That logic belongs in:

- a scheduled job
- a status transition policy
- an event trail when expiry happens

#### 4. Payment Webhook Safety

The row-locking pattern is valid:

```text
SELECT ... FOR UPDATE
```

This matters when payment confirmation and expiry jobs can race.

### What Was Not Carried Into The Core Schema

#### 1. Duplicate Core Tables

The repeated `orders`, `users`, `vehicles`, and enum definitions were not reused because the refined operational schema already supersedes them.

#### 2. Generic Warehouse SKU Inventory

The draft added `stock_levels` and `stock_movements`.

That is a valid pattern, but it does **not** belong in the current operational core unless Zippy is explicitly expanding into warehouse inventory management.

For the current project, the better equivalent is:

```text
vehicle availability inventory
```

not:

```text
SKU stock inventory
```

#### 3. Direct Framework-Specific ORM Guidance

The Prisma/module-layout advice is useful implementation guidance, but it does not change the schema itself.

## Strictly Relevant Extracts From DB 4

Only a narrow subset of `DB 4.txt` matches the current project.

### What Matches Strongly

#### 1. City-Tier And Density-Aware Pricing

This fits the current vault because pricing already depends on:

- tiered city behavior
- corridor-specific rate bands
- nearby cluster and hub spillover effects
- local congestion and demand intensity

#### 2. Deadhead / Return-Load Adjustment

This is strongly aligned with the current project because the vault already emphasizes:

- return-trip optimization
- triangle routing
- empty-km reduction
- backhaul probability

#### 3. Quote Transparency

This is worth preserving because your pricing logic should remain:

- deterministic
- auditable
- explainable
- benchmarkable against real lane conditions

### What Was Intentionally Not Adopted

#### 1. Hardcoded Tier Slab Math As Permanent Database Truth

The `20% below Tier-1` style logic is useful as a pricing-rule idea, but too rigid as schema truth.

It belongs in pricing logic and configuration, not in permanent table design.

#### 2. Generic Knowledge-Graph Commentary

Interesting, but not a direct schema requirement.

#### 3. Python Simulation Snippets

Useful for prototyping logic, but not part of the schema itself.

## Recommended SQL File

The corresponding SQL scaffold lives here:

```text
10_Data_Model/SQL/zippy_logistics_operational_core_schema.sql
```

Behavioral trigger patterns live here:

```text
10_Data_Model/SQL/zippy_logistics_operational_triggers.sql
```

## What This Schema Optimizes For

- strong data integrity for live execution
- explicit support for partner-network operations
- deterministic and auditable pricing inputs
- explicit SLA policy and order-promise tracking
- lane-aware matching and reliability workflows
- finance traceability
- clean downstream analytics integration

## What It Does Not Try To Do Yet

- full accounting double-entry design
- every compliance workflow for every cargo type
- every future AI-agent artifact as a table

Those can be layered later once the first corridor workflows are proven.

## Immediate Recommendation

Treat this operational schema as the transactional source of truth, and keep the existing star schema as the reporting and scoring layer.
