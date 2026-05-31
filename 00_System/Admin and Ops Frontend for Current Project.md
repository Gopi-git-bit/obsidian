---
type: memo
domain: frontend
scope: admin_ops_web
status: active
last_updated: 2026-05-31
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

It must also act as the cross-app harness control surface for the customer, driver, and transport-company apps. The admin web app must show whether each frontend action maps to the canonical backend event, state transition, SLA timer, verification checkpoint, and finance gate.

## Current Admin/Ops Mission

The admin and ops web app helps the team:

- see current operational truth
- identify stuck work
- intervene safely
- monitor SLA and trip risk
- handle finance blockers
- supervise AI recommendations
- protect compliance and audit integrity
- verify cross-app event/state/schema consistency
- expose harness test failures before they become live operational gaps

## User Types

| Role | Main Need |
|---|---|
| Ops Executive | manage daily orders, trips, alerts, PODs |
| Ops Manager | monitor lanes, exceptions, service quality |
| Finance Ops | payment, invoice, settlement, dispute queues |
| Admin | verification, overrides, roles, audit |
| Founder / Strategy | corridor performance, customer health, route economics |

## Harness Engineering Responsibilities

The admin web app owns the operational view of harness alignment across apps.

It must show:

- customer app registration segment: `organized_company` or `individual_unorganized`
- OTP checkpoints for organized-company email, individual/unorganized phone, booking submission, and consignee POD verification
- ToPay consent status, denial reason, hold/resume state, and collection status
- driver offer, acceptance, movement, POD, damage report, telemetry, and settlement blocker events
- transport-company role context: hirer/customer mode or service-provider mode
- transport-company dual-role conflicts, inventory double-booking risk, and role-switch audit history
- canonical state and event names from [[API and Event Contract for Current Project]]
- SLA timers from centralized runtime configuration, not hardcoded frontend assumptions
- payment, invoice, and settlement states from backend finance events

Admin Web must not create a second source of truth. It observes, commands through approved APIs, and records every intervention.

## Cross-App Harness Monitor

Purpose:

- prove that Customer, Driver, and Transport Company apps are behaving like one coordinated system

Core panels:

- Event Registry Health: missing, duplicate, delayed, or unknown event names
- State Transition Health: illegal transition attempts, stale states, skipped gates
- SLA Timer Health: acceptance TTL, movement timeout, loading grace period, transport-company timeout, OTP expiry
- Verification Health: GST, landline IVR, phone OTP, email OTP, KYC, POD OCR, EXIF/GPS, consignee OTP
- Finance Gate Health: payment capture, ToPay collection, mismatch review, invoice readiness, settlement hold
- Offline Sync Health: queued driver/TC actions, conflict resolution, duplicate idempotency keys
- Notification Health: WhatsApp/SMS/email/push delivery, deduplication, role-scoped feed correctness

Required filters:

- app: Customer, Driver, Transport Company, Admin
- role context: consignor, consignee, driver, owner-driver, salaried driver, transport hirer, transport service provider
- severity
- event type
- state
- SLA breach
- unresolved blocker

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
- ToPay consent denied or expired
- order on hold for payment or ToPay resolution
- OTP checkpoint failed or expired
- offline action awaiting sync
- transport-company dual-role conflict
- driver VTU/phone GPS mismatch
- payment captured but order not confirmed

Each queue item should show:

- severity
- owner
- deadline
- next recommended action
- last update time
- related canonical event
- expected next event
- blocked gate

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
- apply controlled hold
- resume held order through backend policy
- resend ToPay consent request
- request OTP retry where policy allows

Rule:

```text
admin actions must go through backend policy and event logging
```

Admin cannot directly mark payment, delivery, POD, invoice, or settlement complete from the frontend. It can only request a backend command that validates evidence, permissions, and transition legality.

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
- trigger individual-driver to transport-company handoff review
- approve similar vehicle only after price/SLA delta is visible
- flag double-booked vehicle or dual-role transport-company conflict

The UI should separate:

- deterministic eligibility
- AI explanation
- human approval

Harness checks:

- 5 km individual-driver search phase
- 10 km individual-driver search phase
- transport-company pool handoff
- arriving-vehicle ETA fallback
- WhatsApp RAG broadcast
- assignment exhausted state
- contacted candidates and timeout evidence

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
- VTU versus phone GPS mismatch
- offline trip update waiting for sync
- fatigue or night-driving risk where configured
- transit damage report

Actions:

- contact driver/provider
- contact customer
- create incident
- update next action
- request POD
- mark issue for review
- request damage evidence
- request telemetry review
- request consignee OTP retry
- freeze payout pending incident review

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
- ToPay denial or consent timeout
- GPS spoof suspicion
- phone switched off during active trip
- POD uploaded but consignee OTP failed
- transit damage evidence submitted
- hazardous material concern
- transport-company TCRS threshold breach
- role-switch conflict
- offline sync conflict

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
- ToPay consent denied
- ToPay collection pending
- on-hold payment resolution
- invoice pending
- POD missing for invoice
- settlement preprocessing
- settlement hold
- payout ready
- reconciliation pending
- billing dispute
- payment mismatch under review
- refund initiated or completed
- debit note or credit note generated

Actions:

- view finance event timeline
- approve or reject hold release
- request payment follow-up
- view invoice/POD
- escalate discrepancy
- hold or release finance blocker with evidence
- route high-risk payout to second approval

Rule:

```text
finance UI must never imply payment or payout completion without backend finance event confirmation
```

Customer-facing payment states to support:

```text
payment_not_started
payment_link_created
booking_payment_pending
advance_paid
partially_paid
fully_paid
topay_consent_pending
topay_consent_accepted
topay_consent_denied
topay_collection_pending
topay_collection_received
on_hold_topay_consent
on_hold_payment_resolution
resumed_topay_consent_requested
credit_approved_due_later
payment_failed
payment_mismatch_under_review
refund_initiated
refund_completed
```

Driver/provider payout states to support:

```text
earning_estimated
payment_gate_pending
pod_uploaded
pod_under_review
settlement_preprocessing
settlement_on_hold
settlement_ready_for_disbursement
payout_initiated
payout_successful
payout_failed
settlement_reconciled
settlement_closed
```

## Customers Workspace

Purpose:

- connect CRM to operations

Show:

- customer profile
- customer segment: organized company or individual/unorganized
- registration OTP and KYC status
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
- disable ToPay for high-risk customers
- require full prepayment by policy
- resolve ToPay denial with pay/cancel/hold options

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
- driver role: owner-driver, fleet owner, or salaried driver
- VTU/telemetry health
- offline sync status
- transport-company TCRS score
- dual-role availability conflict

Actions:

- verify documents
- suspend or reactivate with approval
- mark preferred provider
- review repeated failures
- freeze payout pending dispute
- review driver score appeal
- restrict transport company to prepaid or view-only mode
- approve GST/landline re-verification

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
- event/state anomaly detection
- hallucination or policy-conflict alerts
- deterministic fallback activation

Rules:

- AI output is advisory
- deterministic rules and backend state own truth
- human review required for high-risk workflow changes

AI agent control must support pause, resume, fallback mode, confidence-threshold review, version registry, dead-letter queue inspection, and rejection of unsafe recommendations.

## MVP Scope

## Admin Harness Test Matrix

The admin web app should expose these verification scenarios as test runs or QA dashboards:

| Test ID | Scenario | Required Admin Evidence |
|---|---|---|
| T-ADM-01 | Organized-company registration email OTP succeeds/fails/expires | customer profile, OTP event, blocked/unblocked state |
| T-ADM-02 | Individual/unorganized phone OTP succeeds/fails/expires | customer profile, OTP event, hidden GST/PAN fields |
| T-ADM-03 | ToPay consignee accepts, pays, and order proceeds | consent event, payment event, order state |
| T-ADM-04 | ToPay consignee denies, consignor pays/cancels/holds/resumes | denial event, hold event, resume event, final resolution |
| T-ADM-05 | Driver accepts but does not move within movement timeout | driver event, SLA timer, alert, reassignment action |
| T-ADM-06 | VTU and phone GPS differ by policy threshold | telemetry evidence, incident, risk review |
| T-ADM-07 | POD uploaded but consignee OTP fails | POD event, OTP failure, settlement hold |
| T-ADM-08 | Transit damage report blocks settlement | evidence packet, damage case, finance hold |
| T-ADM-09 | Transport-company role toggle while active orders exist | role-switch log, inventory conflict check |
| T-ADM-10 | Same vehicle appears available in hirer and provider context | conflict alert, inventory event, admin resolution |
| T-ADM-11 | IMS handoff from individual owners to transport-company pool | search phase events, contacted candidates, timeout evidence |
| T-ADM-12 | Payment gateway outage and retry/fallback flow | failed attempt, retry event, blocker status |

These tests should be linked to [[Testing and Verification Strategy for Current Project]] and treated as launch-blocking for the control tower.

Build first:

- operating cockpit queues
- order detail view
- matching review
- active trip monitor
- alert/incident queue
- finance blocker queue
- ToPay, hold/resume, and OTP checkpoint monitor
- cross-app event/state harness monitor
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

## Related Project Notes

- [[Current Project Navigation Hub]]
- [[Frontend Architecture for Current Project]]
- [[Current Architecture Source of Truth]]
- [[Backend Structure for Current Project]]
- [[Operational Compliance Framework for Indian Logistics Startup 2025-2026]]
