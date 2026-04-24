---
type: concept
domain: dashboard
scope: operations
status: active
last_updated: 2026-04-24
related_hubs:
  - Operations Strategy Hub
  - Fleet & Transport Hub
  - Technology Stack Hub
tags:
  - dashboard
  - kpi
  - control-tower
  - transport
  - operations
---

# Transport Control Tower KPI Framework

## Purpose

Define the KPI structure for a transport control tower so operations teams can detect risk early, intervene fast, and improve service, cost, and reliability over time.

## What A Control Tower Must Answer

At any moment, the control tower should answer:

- which shipments are at risk right now?
- where is service degrading?
- which lanes, vehicles, or partners are causing exceptions?
- how much margin is leaking through delay, empty km, or poor assignment?
- what needs dispatcher action now versus management review later?

## KPI Design Principle

Do not mix everything into one dashboard.

Split metrics into:

1. live execution metrics for dispatch action
2. daily operational KPIs for supervisor review
3. strategic trend KPIs for management decisions

## KPI Layers

| Layer | Purpose | Typical User |
|------|---------|--------------|
| live control | act on active shipment risk | dispatcher, control tower operator |
| daily review | identify recurring operational failure | ops lead, fleet manager |
| weekly/monthly strategy | improve network design and policy | founder, operations head |

## Core KPI Domains

### 1. Service Reliability

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| on-time pickup rate | percent of pickups started within committed window | <95% |
| on-time delivery rate | percent of deliveries completed within SLA | <92% |
| order cycle time | booking to delivery duration | rising trend |
| ETA accuracy | gap between promised and actual arrival | p90 drift above threshold |
| first-attempt delivery success | percent delivered without reattempt | <97% |

### 2. Dispatch And Assignment

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| assignment response time | time from confirmed order to vehicle assignment | >15 min for urgent loads |
| driver acknowledgment time | time from assignment to driver acceptance | >10 min |
| assignment failure rate | percent of orders requiring reassignment | >5% |
| own-fleet assignment ratio | percent assigned to internal fleet | trend depends on strategy |
| partner fallback rate | how often control tower must use partner network | spike above baseline |

### 3. Fleet Productivity

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| vehicle utilization | share of available fleet actively used | <75% |
| empty km percentage | unproductive kilometers | >25% |
| trips per vehicle per day | asset throughput | falling trend |
| idle vehicle count | available but unused vehicles | rising trend |
| breakdown rate | percent of trips disrupted by vehicle failure | >2% |

### 4. Tracking And Execution Control

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| GPS freshness | time since last valid location ping | >10 min on active trip |
| route deviation rate | percent of trips deviating materially from route | >3% |
| stalled-trip count | active trips with no movement beyond threshold | any spike |
| milestone update latency | delay in pickup, in-transit, delivered events | rising trend |
| exception detection time | time from event to operator visibility | >5 min for critical loads |

### 5. Cost And Margin

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| realized cost per km | actual operating cost per km | above lane benchmark |
| realized margin per trip | revenue minus actual trip cost | below target floor |
| quoted vs realized margin variance | pricing accuracy gap | persistent negative variance |
| detention cost per trip | waiting-related margin leakage | spike by customer or lane |
| toll share of trip cost | corridor burden | unusual increase |

### 6. Partner Network Quality

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| partner acceptance rate | percent of partner offers accepted | falling trend |
| partner on-time delivery | reliability of outsourced trips | <90% |
| partner cancellation rate | percent of accepted trips later cancelled | >5% |
| partner dispute rate | claims, document issues, billing disputes | rising trend |
| verified partner coverage | availability of trusted partner capacity | below demand baseline |

### 7. Customer Experience

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| complaint rate per 100 orders | customer pain signal | rising trend |
| status update timeliness | speed of proactive updates on active issues | below SLA |
| POD submission time | delay from delivery to POD completion | >2 hours on standard loads |
| repeat booking rate | retained customer confidence | falling trend |
| escalation count | orders needing manager intervention | spike above normal |

### 8. Compliance And Risk

| KPI | Meaning | Suggested Alert |
|-----|---------|-----------------|
| document completeness rate | shipments with all required docs validated | <99% |
| e-way bill exception count | expiry, mismatch, or missing documentation | any upward trend |
| suspicious tracking anomalies | spoofing, impossible jumps, repeated silence | investigate immediately |
| payment mismatch count | revenue or settlement integrity gap | above zero |
| fraud or claim incident rate | security and process-control weakness | rising trend |

## Leading Indicators vs Lagging Indicators

### Leading Indicators

These help prevent failure before delivery misses happen:

- assignment response time
- driver acknowledgment time
- GPS freshness
- stalled-trip count
- route deviation alerts
- document completeness
- detention buildup

### Lagging Indicators

These tell you what already went wrong:

- on-time delivery rate
- complaint rate
- claim rate
- margin variance
- partner cancellation rate
- repeat booking rate

## Daily Control Tower View

The live dashboard should highlight:

- total active trips
- trips at SLA risk
- trips with stale GPS
- trips with route deviation
- orders unassigned beyond threshold
- pickups delayed today
- deliveries delayed today
- detention-heavy trips
- POD pending after delivery

## Supervisor Review View

The daily review should focus on:

- top failing lanes
- top failing customers by wait time
- top failing partners by cancellation or delay
- fleet utilization by vehicle class
- exception root-cause split
- realized margin leakage
- unresolved escalations

## Executive Review View

Weekly or monthly management review should focus on:

- service reliability trend
- lane profitability trend
- own fleet vs partner mix
- network coverage gaps
- repeat booking trend
- claims and fraud trend
- corridor expansion readiness

## Root-Cause Framework

Every major KPI miss should be classified into one of these buckets:

- planning failure
- assignment failure
- vehicle failure
- driver failure
- customer delay
- documentation/compliance failure
- route disruption
- partner failure
- payment/closure failure

Without root-cause tagging, dashboards become decorative instead of operational.

## Example KPI Scorecard

| KPI | Target | Amber | Red | Owner |
|-----|--------|-------|-----|-------|
| on-time pickup | >=95% | 92-94% | <92% | dispatch lead |
| on-time delivery | >=92% | 89-91% | <89% | ops manager |
| assignment response time | <=15 min | 16-25 min | >25 min | control tower |
| GPS freshness | <=10 min | 11-20 min | >20 min | tracking team |
| vehicle utilization | >=75% | 65-74% | <65% | fleet manager |
| empty km | <=25% | 26-32% | >32% | network planning |
| POD submission time | <=2 hr | 2-6 hr | >6 hr | delivery ops |
| realized margin variance | within 5% | 5-10% | >10% | pricing + ops |

## Data Sources

A strong control tower KPI layer should combine:

- order lifecycle data
- assignment and dispatch logs
- driver app events
- GPS telemetry
- document workflow status
- settlement and payment data
- customer support tickets
- partner performance records

## Implementation Notes

This KPI framework should sit on top of:

- [[Transport Operations Implementation Framework]]
- [[Transport Cost Breakdown Model]]
- [[Order Lifecycle]]
- [[TMS Execution Architecture]]
- [[Operational Observability Architecture]]

Use separate views for:

- real-time action
- daily performance review
- strategic analysis

## Recommended First Dashboard Build

If starting small, begin with these 10 KPIs:

1. active trips at risk
2. on-time pickup rate
3. on-time delivery rate
4. assignment response time
5. GPS freshness breach count
6. route deviation count
7. vehicle utilization
8. empty km percentage
9. POD pending after delivery
10. realized margin per trip

## Related Notes

- [[Transport Operations Implementation Framework]]
- [[Transport Cost Breakdown Model]]
- [[Operational Observability Architecture]]
- [[Fleet Utilization]]
- [[Logistics SLA]]
- [[Notification Taxonomy & Escalation Matrix]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Fleet & Transport Hub]]
- [[Technology Stack Hub]]
