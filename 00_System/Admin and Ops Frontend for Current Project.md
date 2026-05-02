---
type: memo
domain: frontend
scope: admin_ops_web
status: active
last_updated: 2026-05-01
related_hubs:
  - "[[Technology Stack Hub]]"
  - "[[Operations Strategy Hub]]"
  - "[[AI Agents Hub]]"
tags:
  - frontend
  - admin
  - ops
  - control-tower
  - source-of-truth
source_files:
  - "C:\\Users\\user\\Downloads\\forntend Admin.txt"
---

# Admin and Ops Frontend for Current Project

## Purpose

This note reshapes the older admin dashboard PRD for the current Zippy project state.

The admin frontend should not start as a broad platform-control fantasy dashboard.

It should start as an operational control tower for the MVP workflow:

```text
order
-> quote
-> payment gate
-> match
-> assignment
-> trip
-> POD
-> invoice
-> settlement
```

## Current Admin/Ops Mission

The admin and ops web app helps the team:

- see current operational truth
- identify stuck work
- intervene safely
- monitor SLA and trip risk
- handle finance blockers
- supervise AI recommendations
- protect compliance and audit integrity

## User Types

| Role | Main Need |
|---|---|
| Ops Executive | manage daily orders, trips, alerts, PODs |
| Ops Manager | monitor lanes, exceptions, service quality |
| Finance Ops | payment, invoice, settlement, dispute queues |
| Admin | verification, overrides, roles, audit |
| Founder / Strategy | corridor performance, customer health, route economics |

## Recommended Navigation

Sidebar navigation:

- Operating Cockpit
- Orders
- Matching
- Trips
- Alerts
- Finance
- Customers
- Providers
- Lanes
- AI Review
- Audit
- Settings

MVP can start with:

- Operating Cockpit
- Orders
- Trips
- Alerts
- Finance
- Customers
- Providers

## Operating Cockpit

Purpose:

- answer what needs action now

Core queues:

- new orders pending quote
- orders missing required data
- payment gate pending
- unmatched orders
- provider acceptance pending
- pickup at risk
- delivery at risk
- active incidents
- POD pending
- invoice/payment blockers
- settlement blockers

Each queue item should show:

- severity
- owner
- deadline
- next recommended action
- last update time

## Orders Workspace

Purpose:

- manage the order lifecycle without unsafe state mutation

Views:

- all active orders
- pending quote
- pending payment
- pending match
- active execution
- delivered / POD pending
- completed / closed
- cancelled / exception

Actions:

- view order details
- request missing customer data
- approve or reject manual override
- assign owner
- add internal note
- trigger customer update

Rule:

```text
admin actions must go through backend policy and event logging
```

## Matching Workspace

Purpose:

- supervise vehicle/provider recommendations

Show:

- recommended providers
- vehicle compatibility
- lane reliability
- return-load or triangle opportunity
- price and SLA implications
- risk flags
- AI explanation if available

Actions:

- approve match
- reject recommendation
- request alternative
- escalate to supervisor

The UI should separate:

- deterministic eligibility
- AI explanation
- human approval

## Trips Workspace

Purpose:

- monitor active movement

Show:

- map or list view of active trips
- trip status
- ETA vs promised window
- pickup/delivery milestone state
- long halt
- route deviation
- driver unreachable
- document pending

Actions:

- contact driver/provider
- contact customer
- create incident
- update next action
- request POD
- mark issue for review

## Alerts And Incidents

Purpose:

- convert noise into owned exceptions

Alert categories:

- SLA risk
- pickup delay
- delivery delay
- route deviation
- prolonged halt
- GPS loss
- document blocker
- payment blocker
- customer complaint
- provider cancellation

Each alert should have:

- severity
- source
- related order/trip
- responsible owner
- recommended action
- escalation status
- audit trail

## Finance Workspace

Purpose:

- connect logistics execution to financial closure

Queues:

- payment intent pending
- payment failed
- ToPay pending
- invoice pending
- POD missing for invoice
- settlement preprocessing
- settlement hold
- payout ready
- reconciliation pending
- billing dispute

Actions:

- view finance event timeline
- approve or reject hold release
- request payment follow-up
- view invoice/POD
- escalate discrepancy

Rule:

```text
finance UI must never imply payment or payout completion without backend finance event confirmation
```

## Customers Workspace

Purpose:

- connect CRM to operations

Show:

- customer profile
- active shipments
- health score
- complaint history
- payment behavior
- route history
- satisfaction metrics
- next follow-up date

Actions:

- create follow-up task
- send performance report
- mark retention risk
- view monthly value report

This connects to:

- [[CRM and Customer Retention Playbook for Zippy Logistics]]

## Providers Workspace

Purpose:

- manage driver, owner-driver, and transport-company reliability

Show:

- verification status
- active vehicles
- acceptance rate
- cancellation rate
- on-time pickup/delivery
- POD speed
- incident history
- settlement status

Actions:

- verify documents
- suspend or reactivate with approval
- mark preferred provider
- review repeated failures

## Lane Intelligence Workspace

Purpose:

- expose corridor learning for ops and strategy

Show:

- directed lane performance
- quote vs actual cost
- delay patterns
- loaded km ratio
- return-load opportunity
- triangle-route candidates
- partner performance by lane

This should come after basic operational workflow visibility.

## AI Review Workspace

Purpose:

- supervise bounded AI outputs

Review:

- shipment extraction confidence
- match explanations
- delay reason classification
- customer message drafts
- settlement blocker summaries
- churn-risk suggestions

Rules:

- AI output is advisory
- deterministic rules and backend state own truth
- human review required for high-risk workflow changes

## MVP Scope

Build first:

- operating cockpit queues
- order detail view
- matching review
- active trip monitor
- alert/incident queue
- finance blocker queue
- customer/provider profile basics
- audit notes for manual actions

Delay:

- full system infrastructure monitoring
- broad AI model retraining UI
- complex geospatial analytics
- advanced predictive dashboards
- public marketplace moderation

## Success Metrics

- time to detect exception
- time to assign owner
- exception resolution time
- unmatched order aging
- pickup and delivery risk caught before breach
- POD pending aging
- payment and settlement blocker aging
- manual override audit completeness
- customer complaint closure time

## Bottom Line

The current admin frontend should be treated as:

```text
an operations and finance control tower
that makes stuck workflows visible, owned, auditable, and recoverable
```

