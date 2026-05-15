---
type: memo
domain: product
scope: roles_and_permissions
status: active
last_updated: 2026-05-15
related_hubs:
  - "[[Operations Strategy Hub]]"
  - "[[Current Project Navigation Hub]]"
  - "[[Frontend Architecture for Current Project]]"
tags:
  - roles
  - permissions
  - auth
  - product-rules
  - source-of-truth
---

# Role and Permission Matrix for Current Project

## Purpose

This note defines the minimum canonical role model and permission boundaries for the first real Zippy build.

Use it as the builder-facing source of truth for:

- backend auth and authorization
- frontend visibility rules
- role-aware API responses
- contact-sharing and workflow boundaries

## Canonical Roles

- `customer`
- `driver`
- `transport_company`
- `admin`
- `ops`

Important interpretation:

- `transport_company` is a business identity and may appear in customer-side or provider-side workflows
- `owner-driver` behavior belongs under `driver` plus owned vehicle context
- warehouse-only roles are out of scope

## Role Summary

| Role | Main Goal |
| --- | --- |
| customer | place orders, pay, track, receive POD and invoice visibility |
| driver | accept work, execute trip, upload POD, receive alerts |
| transport_company | provide capacity and later support dual-role workflows |
| admin | governance, override, audit, approval |
| ops | dispatch supervision, matching oversight, exception handling |

## Permission Matrix

| Capability | Customer | Driver | Transport Company | Admin | Ops |
| --- | --- | --- | --- | --- | --- |
| Login | Yes | Yes | Yes | Yes | Yes |
| Create order | Yes | No | Later customer-side | Yes | Yes |
| View own orders | Yes | No | Scoped | Yes | Yes |
| View assigned offers | No | Yes | Scoped provider-side | Yes | Yes |
| Accept or reject offer | No | Yes | Later provider-side | Yes | Yes |
| View active trip | Scoped | Yes | Scoped | Yes | Yes |
| Post trip milestones | No | Yes | No | No | Yes |
| Upload POD | No | Yes | No | Yes | Yes |
| View POD for related order | Yes | Scoped | Scoped | Yes | Yes |
| View payment status | Yes | Limited | Scoped | Yes | Yes |
| View invoice status | Yes | Limited | Scoped | Yes | Yes |
| View all exception queues | No | No | No | Yes | Yes |
| Override blocked workflow | No | No | No | Yes | Limited approved actions |
| View audit history | No | No | No | Yes | Limited |

## Role Rules By Surface

### Customer

May:

- authenticate
- create booking
- view quote and payment mode
- track own shipment
- view own document, invoice, and payment status

May not:

- assign vehicles
- mutate lifecycle state directly
- post trip milestones
- view unrelated drivers, vehicles, or customers

### Driver

May:

- authenticate
- view own offers and assigned trip
- accept or reject offers
- post execution milestones
- upload POD and required documents
- view only contact details required for the live trip stage

May not:

- create customer orders
- change payment terms
- override SLA or route policy
- browse unrelated orders

### Transport Company

MVP-safe rule:

```text
preserve the role in backend and schema
defer broad UI behavior until after core MVP proof
```

Near-term permissions:

- authenticate
- maintain company profile and documents later
- participate in provider-side capacity workflows later

Must keep separate in future:

- company as provider
- company as customer

### Ops

May:

- view pending orders
- view unmatched and exception queues
- monitor active trips and alerts
- trigger approved workflow actions through backend services
- log incidents

May not:

- bypass audit trails
- directly mutate state outside approved transition path
- silently alter finance truth

### Admin

May:

- view all entities
- apply approved overrides
- review incidents, audits, blocked flows, and finance blockers
- unlock or close exceptional states through audited actions

May not:

- bypass event logging
- rewrite workflow history without traceability

## Contact Visibility Rules

Contact visibility must be minimal and stage-aware.

### Customer Can See

- support contact
- assigned driver contact only when shipment is in the appropriate execution stage

### Driver Can See

- customer or pickup/delivery contact only when required for assigned live trip execution

### Ops And Admin Can See

- operationally necessary contact details for supervision and intervention

Core rule:

```text
contact access is governed by workflow stage and role, not by static UI convenience
```

## Finance Visibility Rules

### Customer

Can see:

- quote amount
- payment mode
- payment status
- invoice status

### Driver

Can see:

- payout-relevant visibility only
- not full customer finance internals

### Ops

Can see:

- payment blockers
- invoice blockers
- settlement blockers

### Admin

Can see:

- full finance visibility required for governance and override

## Transition Authority Rules

Suggested ownership:

| Workflow Area | Primary Role |
| --- | --- |
| order intake and booking | customer |
| matching review and assignment oversight | ops |
| trip execution milestones | driver |
| incident and alert review | ops |
| override and exceptional closure | admin |

No role may mutate lifecycle state outside the canonical transition gateway.

## Authentication And Session Assumptions

Required minimum auth behavior:

- one `app_users` root identity
- one primary operational role per active session
- backend-issued session or token identity
- role carried in `/auth/me`

Future-safe note:

transport companies may need role-context switching later, but that should not complicate the MVP auth path.

## Bottom Line

Builders should treat this as the safe MVP rule:

```text
customer books
driver executes
ops supervises
admin governs
transport-company role is preserved in architecture but not allowed to destabilize the first shipping workflow
```
