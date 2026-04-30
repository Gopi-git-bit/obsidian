---
type: concept
domain: operations
decision_value: high
status: draft
related_hubs:
  - Operations Strategy Hub
  - Customer Problems Hub
  - Business Models Hub
tags:
  - reverse-logistics
  - return-policy
  - operations
  - customer-trust
---

# Reverse Logistics and Return Policy Framework

## Purpose

Convert return logistics research from Tmall Mart into a practical reverse-logistics framework for Zippy's warehouse-first logistics startup.

Derived from [[Tmall Mart Reverse Logistics Source]].

## Core Principle

A return is not a failed order. It is a second logistics order with higher dispute risk.

```text
forward order = move goods according to promise
reverse order = recover goods, evidence, money, packaging, and trust
```

The platform should own the policy and information standard even when a 3PL, driver, warehouse, supplier, or consignee physically executes the reverse movement.

## Unified Return Policy Canvas

| Policy Area | Rule To Define |
|-------------|----------------|
| Eligibility | Which cases qualify for return, rejection, replacement, reattempt, cancellation, or claim |
| Time window | How long after pickup, delivery attempt, or delivery the reverse request is valid |
| Evidence | Required photos, POD, seal number, weight check, invoice/LR, temperature log, damage note, or recipient comment |
| Cost owner | Customer, consignee, warehouse, transporter, supplier, or platform |
| Reverse destination | origin warehouse, supplier, repair center, disposal point, alternate consignee, or consolidation desk |
| 3PL responsibility | pickup SLA, scan events, proof of handover, damage liability, and escalation rules |
| Refund/settlement logic | when payment is held, reversed, partially refunded, or released |
| Exception path | who approves disputed, high-value, hazardous, cold-chain, or damaged returns |

## Return Types For Zippy

| Return Type | Trigger | Operational Response |
|-------------|---------|----------------------|
| customer cancellation before pickup | customer changes plan before vehicle loading | cancel order, release vehicle, apply cancellation fee rules |
| rejected at pickup | cargo/document/packaging does not match booking | hold order, capture evidence, re-price or cancel |
| rejected at delivery | consignee refuses goods or payment | create reverse order, capture refusal reason, route cargo back or to alternate node |
| damaged cargo claim | damage found during loading, transit, or delivery | freeze settlement, capture evidence, start claim workflow |
| wrong vehicle/material fit | vehicle cannot legally or physically carry load | reassign vehicle and decide who bears delay cost |
| excess material return | warehouse receives or ships extra material | plan reverse pickup or consolidation with next lane |
| reusable packaging return | pallets, crates, dunnage, or totes need recovery | track packaging assets as returnable units |
| failed delivery reattempt | address/recipient/time-window failure | decide reattempt, storage, or return-to-origin |

## Information Flow

The OMS should create a reverse-order event that updates every stakeholder at the same time.

```text
Return request
-> eligibility check
-> evidence capture
-> cost owner decision
-> reverse route / drop-off node selection
-> 3PL assignment
-> pickup or drop-off scan
-> warehouse/supplier receipt
-> refund / claim / settlement closure
-> carrier and customer score update
```

Required data fields:

- original order ID
- reverse order ID
- return reason code
- cargo condition
- item/material category
- evidence checklist status
- reverse destination
- pickup/drop-off mode
- assigned 3PL or driver
- cost owner
- SLA deadline
- refund or settlement state

## 3PL Relationship Rules

The startup should not let each logistics partner define return behavior independently.

| Contract Area | Minimum Standard |
|---------------|------------------|
| scan events | return accepted, picked up, in transit, received, exception |
| pickup SLA | time to collect return after approval |
| evidence | photos, weight, seal, timestamp, GPS, recipient refusal note |
| liability | who pays when goods are damaged after return pickup |
| escalation | when partner must route to platform support |
| data integration | API, app event, or dashboard update required for every return |
| penalties/rewards | score impact, volume downgrade, or preferred access based on return handling quality |

## Automated Drop-Off And Dense Nodes

Tmall Mart's unmanned distribution idea connects directly to the Cainiao Post dense-node pattern.

For Zippy, possible return nodes are:

- warehouse-cluster transport desks
- industrial estate counters
- truck terminal counters
- partner warehouse drop-off points
- smart parcel lockers for small parts/documents
- local EV/e-loader shuttle points
- reusable packaging and pallet return zones

This links to [[Cainiao Post Campus Case Source]]: automation is useful only when the physical node has enough density, clear scan discipline, and a clean handover process.

## Return Policy Algorithm

```text
input:
  order_status
  return_reason
  material_type
  cargo_value
  evidence_status
  pickup_or_delivery_stage
  customer_score
  carrier_score
  warehouse_grade
  reverse_node_density

if evidence_status is incomplete:
  hold return approval and request evidence

if material_type is hazardous, cold-chain, high-value, or regulated:
  require manual operations approval

if return_reason is carrier_fault:
  assign cost to carrier or 3PL contract bucket

if return_reason is customer_change:
  apply cancellation/reverse movement fee policy

if reverse_node_density is high:
  prefer drop-off desk, locker, shuttle, or consolidation pickup
else:
  assign direct 3PL pickup

create reverse_order_id
notify customer, warehouse, supplier, carrier, and support dashboard
track SLA until receipt and settlement closure
update customer, carrier, and warehouse operational scores
```

## KPIs

| KPI | Meaning |
|-----|---------|
| return initiation time | how fast the system recognizes a reverse need |
| evidence completion rate | whether liability can be decided without dispute |
| reverse pickup SLA | partner discipline in collecting approved returns |
| return-to-receipt cycle time | total reverse logistics speed |
| dispute rate | policy clarity and evidence quality |
| refund/settlement closure time | financial trust |
| packaging recovery rate | reusable asset and sustainability performance |
| reverse logistics cost per order | management-level cost visibility |
| repeat return reason rate | root cause signal for product, warehouse, carrier, or booking errors |

## Startup Rule

Return policy should be visible before order confirmation, not discovered after failure.

The customer app, driver app, warehouse dashboard, and support dashboard should all use the same return reason codes and evidence checklist. That consistency is what prevents buck-passing between platform, warehouse, driver, and 3PL.

## Related Notes

- [[Tmall Mart Reverse Logistics Source]]
- [[Order Lifecycle]]
- [[Damage Claim Process]]
- [[Failed Delivery Handling]]
- [[Scenario - Customer Cancels Order]]
- [[SOP - Handle Customer Complaint]]
- [[Cainiao Strategy Patterns for Zippy]]
- [[Warehouse Customer Strategy Canvas]]
