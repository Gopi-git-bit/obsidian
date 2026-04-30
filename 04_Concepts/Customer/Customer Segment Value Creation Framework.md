---
type: concept
domain: customer
decision_value: high
status: draft
related_hubs:
  - Market Intelligence Hub
  - Customer Problems Hub
  - Business Models Hub
  - Operations Strategy Hub
tags:
  - customer-segmentation
  - value-creation
  - service-design
  - logistics-strategy
---

# Customer Segment Value Creation Framework

## Purpose

Translate customer-first logistics strategy into Zippy's segmentation, service design, warehouse targeting, and operating rules.

Derived from [[Customer-First Logistics Segmentation Source]].

## Core Rule

Do not segment customers only by who they are. Segment them by what logistics outcome they value and what operational promise they can profitably support.

```text
customer identity
+ warehouse grade
+ material type
+ buying behavior
+ service expectation
+ cost-to-serve
= segment-specific logistics product
```

## Segment Axes

| Axis | Values | Why It Matters |
|------|--------|----------------|
| customer type | warehouse, MSME, enterprise, transport company, trader, manufacturer | defines buying role and workflow |
| warehouse grade | A, B, C | defines process maturity, dock readiness, and integration depth |
| service tier | Standard, Express, Premium, Dedicated | defines SLA, matching speed, support priority, and pricing |
| value driver | price, speed, reliability, visibility, flexibility, support | defines the actual reason for purchase |
| order behavior | low, medium, high frequency; ad hoc or repeat lane | defines retention potential and lane planning |
| material complexity | general, fragile, cold, hazardous, high-value, bulk | defines vehicle, evidence, and risk controls |
| tech readiness | API/WMS/TMS, app, WhatsApp, phone-only | defines onboarding and product interface |
| cost-to-serve | low, medium, high | protects margin while serving different promises |

## Segment-To-Value Map

| Segment | Primary Value | Service Design |
|---------|---------------|----------------|
| Grade A enterprise warehouse | reliability, visibility, integration, SLA control | API/WMS/TMS integration, dock scheduling, control tower, dedicated account workflow |
| Grade B regional warehouse | vehicle fit, predictable dispatch, documentation, regional lane reliability | dispatch calendar, vehicle recommendation, carrier pool, ETA and POD discipline |
| Grade C godown / MSME stock point | simplicity, trust, price clarity, assisted execution | assisted booking, WhatsApp/app flow, loading checklist, verified vehicle network |
| SME Express shipper | speed, frequent communication, fast matching | priority matching, tighter ETA confidence, multi-channel alerts |
| transport company / fleet owner | utilization, return loads, faster payment, trusted demand | return-load matching, route intelligence, settlement proof, partner score |
| specialized shipper | risk control, compliance, evidence | cold-chain, hazmat, high-value, port/container, or fragile cargo workflow |

## Value Discipline Choice

| Discipline | Meaning | Best Fit |
|------------|---------|----------|
| Operational excellence | low friction, low cost, predictable standard service | high-volume Standard lanes, Grade B/C repeat dispatch |
| Customer intimacy | customized support and workflow adaptation | enterprise warehouses, key accounts, complex material flows |
| Product leadership | superior digital intelligence and automation | Grade A, integrated 3PLs, predictive planning, API customers |

Zippy should not use one discipline for every customer. A Grade C godown may need operational excellence and trust first; a Grade A warehouse may pay for integration and control-tower intelligence.

## Segment Service Config

Each segment should become a configuration object that the OMS, IMS, TMS, pricing, support, and notification systems can read.

```text
segment_service_config
- segment_id
- customer_type
- warehouse_grade
- service_tier
- max_matching_time_minutes
- eta_accuracy_p90_target_minutes
- vehicle_quality_threshold
- communication_channels
- support_priority_level
- evidence_requirement
- return_policy_level
- pricing_model
- escalation_path
- cost_to_serve_target
```

## Buying Behavior Signals

| Signal | Interpretation | Product Response |
|--------|----------------|------------------|
| repeatedly checks price | price-sensitive | show transparent cost breakdown, backhaul discount, Standard tier |
| selects Express frequently | speed-sensitive | priority queue, tighter ETA, proactive alerts |
| opens tracking often | visibility-sensitive | richer tracking, more milestone notifications |
| starts support chat during transit | anxiety or poor visibility | proactive communication and exception prediction |
| repeats same lane | lane loyalty potential | prebuilt lane rate, carrier shortlist, return-load plan |
| frequent disputes/refunds | trust or execution mismatch | evidence checklist, risk scoring, manual review |
| asks for documents/POD quickly | compliance-sensitive | document automation and guaranteed POD SLA |

## Segment KPI Dashboard

| KPI | Why It Matters |
|-----|----------------|
| on-time delivery by segment | proves promise quality |
| ETA accuracy p90 | reveals whether tier promise is honest |
| matching time p95 | measures supply response for each segment |
| damage/dispute/refund rate | captures hidden trust cost |
| support response time | measures customer experience, not just movement |
| cost-to-serve | protects unit economics |
| retention and reorder rate | validates value creation |
| NPS or satisfaction score | checks whether the segment experiences value |

## Warehouse-First Application

For Zippy's current strategy, the warehouse is the target customer. Segment design should therefore connect directly to [[Warehouse Customer Strategy Canvas]].

```text
warehouse grade
-> customer value driver
-> service tier
-> vehicle model
-> distribution strategy
-> SLA and KPI
-> product module
```

Examples:

| Warehouse Segment | Value Promise | Product Module |
|-------------------|---------------|----------------|
| Grade A ecommerce / pharma / 3PL | dock-slot discipline, visibility, integration | control tower, API integration, dock scheduler |
| Grade B distributor | right vehicle, fewer dispatch delays, POD discipline | vehicle recommendation, dispatch calendar, carrier score |
| Grade C godown | trust, assisted booking, no wrong vehicle | assisted dispatch, loading checklist, verified vehicle |
| cold-chain warehouse | temperature-safe movement | reefer matching, temperature evidence, cold dwell alerts |
| port/CFS warehouse | detention risk control | document checklist, gate timing, container workflow |

## A/B Test Pattern

Use segment-specific experiments before changing the whole platform.

| Test | Target Segment | Primary Metric | Guardrails |
|------|----------------|----------------|------------|
| SME Express priority matching | SME Express orders | p95 matching time | dispute rate, refund rate, driver rejection, cost/order |
| Grade B dispatch calendar | regional warehouses | pickup readiness and detention | missed pickup, support tickets |
| Grade C assisted booking | small godowns | wrong-vehicle reduction | booking time, cancellation rate |
| enterprise proactive alerts | premium warehouses | support chat reduction | notification fatigue, cost-to-serve |

## Startup Rule

The segment is only real when operations behave differently.

If pricing, matching, ETA, notifications, support, evidence, and return policy are identical for every customer, then segmentation exists only in marketing. Zippy should make segmentation executable through service configs, KPI dashboards, and controlled experiments.

## Related Notes

- [[Customer-First Logistics Segmentation Source]]
- [[Warehouse Customer Strategy Canvas]]
- [[Tamil Nadu Customer Segmentation and GTM Plan]]
- [[Warehouse Transport Correlation Algorithm]]
- [[Reverse Logistics and Return Policy Framework]]
- [[Cainiao Strategy Patterns for Zippy]]
