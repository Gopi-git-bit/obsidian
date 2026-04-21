---
type: source
status: raw
domain: logistics
origin: internal
processed: false
created: 2026-04-16
source_file: claude.md
notes: Primary source document containing full logistics platform documentation for Zippy Logistics
---

# Logistics Brain - Source Index

This document serves as an index for the primary source document `claude.md`.

## Source Document

<filepath>02_Sources\claude.md</filepath>

## Additional Processed Sources

- [[grok_algo_source_reference]] - AI-generated logistics algorithms for matching, routing, and return trips
- [[pricing_engine_architecture_source]] - Hybrid pricing-engine architecture covering SQLite, Neo4j, GraphQL, and quote precision
- [[unified_routing_optimization_source]] - State-safe routing orchestration across Valhalla, OR-Tools, RDS, and return-trip workflows
- [[fallback_resilience_architecture_source]] - Fallback execution, simulation replay, chaos testing, and supervisor-led resilience controls
- [[customer_app_gap_analysis_source]] - Customer-app frontend alignment for transitions, consent, offline sync, and audit-safe UX
- [[driver_app_gap_analysis_source]] - Driver-app alignment for assignments, POD controls, offline sync, and fraud-resistant field operations
- [[ims_logic_architecture_source]] - IMS matching boundaries, atomic reservations, loop-aware scoring, and exhaustion handling
- [[enhanced_eta_algorithm_source]] - Layered ETA architecture with historical baseline, live corrections, ML residuals, and confidence bounds
- [[lgbm_eta_pipeline_source]] - LightGBM ETA training and inference pipeline with logistics-specific features and deployment guidance
- [[hyperparameter_tuning_system_source]] - MAPE-triggered Optuna and Ray Tune workflows for safe model tuning, promotion, and rollback
- [[authoritative_database_schema_source]] - Supabase and PostgreSQL schema for event-safe orders, PostGIS operations, finance, and AI audit controls
- [[tms_execution_spec_source]] - Refined TMS execution rules for routing hierarchy, telemetry validation, SLA monitoring, and canonical event contracts
- [[market_scope_source]] - South India Tier-2 and Tier-3 market growth thesis covering deadhead, warehousing, MSMEs, and expansion intelligence
- [[scenario_management_source]] - Policy-registry and simulation framework for strategic adaptation, human approval, and gradual rollout
- [[legal_guidance_source]] - General legal and compliance guidance for contracts, documentation, company setup, and hazardous-goods controls
- [[vehicle_model_cost_source]] - Vehicle-model and operating-cost inputs for mileage, dimensions, depreciation, tolls, insurance, and regional labor assumptions
- [[business_scope_2_source]] - Selective market and pricing signals for South India truck-rate bands, outsourced transport dependence, and dynamic-pricing inputs
- [[chatgpt_prd_observability_source]] - Selective observability and reliability-governance extraction for dashboards, alerts, and canary safety

## Document Contents

This source contains comprehensive documentation for:

- **Zippy Logistics Platform Architecture**
- **Driver Mobile App Specifications**
- **Customer Mobile App PRD**
- **Transport Company Mobile App PRD**
- **Admin Dashboard PRD**
- **Backend Architecture (7-Agent System)**
- **Database Schema Refinements**
- **AI Agent PRDs**
- **Workflow Automation Specifications**

## Derived Notes

The following notes have been extracted and structured from this source:

### Hubs
- [[AI Agents Hub]] - Multi-agent system design
- [[Operations Strategy Hub]] - Core operations logic

### Concepts
- [[Order Lifecycle]] - End-to-end order process
- [[Fleet Utilization]] - Fleet management metrics
- [[Closed Body Vehicle]] - Vehicle type specifications
- [[Proof of Delivery]] - POD requirements
- [[E-way Bill]] - Compliance documentation
- [[MSME Shipper Pain Points]] - Customer needs
- [[Line Haul vs Last Mile]] - Transport segmentation
- [[LCV vs MCV vs HCV]] - Vehicle classification

### Algorithms
- [[Load Matching Algorithm]] - Order-vehicle matching
- [[Dynamic Pricing Logic]] - Pricing models
- [[Route Risk Scoring]] - Risk assessment

### Scenarios
- [[Scenario - Need 20 ft Truck Chennai to Trichy]]
- [[Scenario - No Own Fleet Available]]
- [[Scenario - High Value Electronics Transit]]

### SOPs
- [[SOP - New Shipment Booking]]
- [[SOP - Assign Vehicle to Order]]

### Business Models
- [[Truck Aggregator Model]]
- [[3PL vs 4PL]]
- [[Commission vs Flat Fee]]

### AI Agents
- [[Customer Service Agent]]
- [[Order Management Agent]]

### Personas
- [[MSME Owner Persona]]
- [[Transport Company Manager Persona]]

## Vault Navigation

Start with: [[Logistics Brain - Master Index]]

---
*This is a source document. It feeds the atomic notes but is not itself the brain.*
