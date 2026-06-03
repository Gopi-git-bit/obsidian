# Zippy Logistics SOP Operating System

## Operating System for Controlled Internal Pilot

## 1. Purpose

This SOP defines how Zippy Logistics should operate during the controlled internal MVP pilot. It acts as the company's operating system across customers, drivers, transport companies, operations, finance, supervisor review, settlement, compliance, technology, and exception handling.

The goal is simple:

**Every shipment must move through a controlled, auditable, and repeatable process from order creation to settlement closure.**

This SOP is not for public launch yet. It is for internal pilot operations using controlled users, controlled data, manual external processes, and verified backend workflows.

---

# 2. Current Operating Status

## 2.1 MVP Status

Zippy Logistics is ready for a **controlled internal pilot**, not public production.

Current strengths:

* Backend runtime is verified.
* Docker runtime is working.
* PostgreSQL migrations are verified.
* Health and readiness checks are working.
* Supervisor hold system is implemented.
* Finance console is implemented.
* Settlement release is policy-gated and auditable.
* Policy preflight is wired into high-risk actions.
* Event outbox exists.
* Six frontend harnesses pass smoke and E2E tests.
* Dev-login is blocked outside development mode.

Current limitations:

* No real payment gateway yet.
* No real WhatsApp/SMS/email provider yet.
* No real OCR/document storage yet.
* No live GST/NIC/e-way/ULIP/VAHAN integrations yet.
* No production secrets manager yet.
* No reverse proxy/TLS yet.
* No formal backup/restore drill yet.
* No production metrics exporter yet.

## 2.2 Pilot Rule

During pilot:

**No real money movement should happen automatically.**
**No public users should be onboarded.**
**No external production launch should happen until payment, security, backup, TLS, and communications are hardened.**

---

# 3. Operating Principles

## 3.1 Agents Propose, System Enforces

AI agents, staff, and frontend users may propose actions, but only backend services can execute state changes.

Examples:

* Driver may upload POD, but cannot verify POD.
* Finance may request settlement release, but backend checks POD, OTP, fraud hold, settlement hold, role, idempotency, and policy decision.
* Supervisor may clear holds, but all decisions must be logged.
* Policy checks can approve, hold, or reject actions, but hard backend validations remain the final authority.

## 3.2 No State Jumping

Orders must move through approved lifecycle states only. No user, agent, or admin should skip required states.

Core lifecycle:

1. Draft
2. Validated
3. Priced
4. Payment pending
5. Confirmed
6. Allocated
7. Driver assigned
8. Loading
9. In transit
10. Delivered
11. POD/OTP verified
12. Settlement ready
13. Settlement released
14. Closed

## 3.3 Every Critical Action Must Be Traceable

Every important action must have:

* Actor
* Role
* Timestamp
* Entity ID
* Trace ID
* Idempotency key
* Old state
* New state
* Decision reason
* Policy result where applicable

If it is not logged, it did not happen.

---

# 4. Roles and Responsibilities

## 4.1 Customer

Customer is responsible for:

* Creating order request.
* Providing pickup and drop details.
* Providing material details.
* Uploading or sharing invoice/shipment documents where required.
* Confirming payment terms.
* Coordinating loading at pickup point.
* Ensuring consignee is reachable for OTP/POD flow.

Customer cannot:

* Force wrong vehicle assignment.
* Change delivery destination without new approval.
* Bypass material compliance rules.
* Demand dispatch without required documents.

## 4.2 Driver / Vehicle Owner

Driver is responsible for:

* Staying online only when available.
* Accepting or rejecting orders within SLA.
* Moving toward pickup after acceptance.
* Uploading loading evidence.
* Uploading POD/evidence after delivery.
* Collecting consignee OTP.
* Reporting breakdown, delay, accident, police/RTO stop, damage, or consignee refusal.

Driver cannot:

* Verify POD or OTP.
* Assign the order to another driver.
* Demand extra money without documented reason.
* Take direct customer deal outside the platform.
* Continue after serious misconduct, drink-and-drive, or fraud flag.

## 4.3 Transport Company

Transport company may act in two roles:

1. **Hirer** - needs vehicles from other providers.
2. **Service provider** - offers available fleet capacity.

Transport company is responsible for:

* Registering valid company details.
* Maintaining fleet/driver records.
* Accepting or rejecting orders honestly.
* Handling inter-company commercial terms where Zippy is only a platform facilitator.
* Paying Zippy platform fee where applicable.

Transport company cannot:

* Misrepresent vehicle availability.
* Use Zippy to deceive partner companies.
* Shift payment disputes to Zippy unless Zippy-controlled payment flow was used.
* Bypass verification or policy controls.

## 4.4 Operations Admin

Operations admin is responsible for:

* Monitoring order flow.
* Resolving assignment failures.
* Handling customer/driver operational complaints.
* Reviewing loading, transit, and delivery issues.
* Escalating suspicious or high-risk cases to Supervisor.
* Ensuring shipment lifecycle moves correctly.

Operations admin cannot:

* Release settlement.
* Bypass finance holds.
* Override policy rejects without supervisor route.
* Verify financial completion without evidence.

## 4.5 Supervisor

Supervisor is responsible for:

* Reviewing exception cases.
* Creating or clearing fraud holds.
* Creating or clearing settlement holds.
* Approving or rejecting disputed evidence.
* Reviewing policy holds/rejections.
* Maintaining audit trail of decisions.

Supervisor cannot:

* Release settlement directly unless also authorized as super admin.
* Delete audit history.
* Ignore policy-blocked actions without recorded decision.
* Allow driver-side POD/OTP self-verification.

## 4.6 Finance Admin

Finance admin is responsible for:

* Reviewing settlement queue.
* Checking POD and OTP verification status.
* Checking fraud and settlement holds.
* Releasing settlement only when eligible.
* Reviewing journal and GST invoice records.
* Monitoring blocked release reasons.
* Ensuring no duplicate settlement release happens.

Finance admin cannot:

* Release settlement when fraud hold is active.
* Release settlement when settlement hold is active.
* Release settlement without POD and OTP verification.
* Release settlement without audit trail.
* Override supervisor hold.

## 4.7 Super Admin

Super admin is responsible for:

* Emergency access.
* Role management.
* Final escalation decisions.
* Production environment governance.
* Security and compliance oversight.

Super admin should not be used for routine operations.

---

# 5. Daily Operating Rhythm

## 5.1 Morning Startup Checklist

Responsible: Operations Admin + Tech Admin

Before business operations begin:

1. Confirm backend is healthy.
2. Confirm database is connected.
3. Confirm readiness endpoint returns no missing tables.
4. Confirm Docker runtime is healthy if running pilot stack.
5. Confirm frontend harnesses are accessible.
6. Confirm pilot users can log in through approved non-dev route.
7. Confirm dev-login is disabled in pilot mode.
8. Check open exception cases.
9. Check pending settlement holds.
10. Check failed outbox events.
11. Check yesterday's unresolved orders.
12. Check backup status if pilot DB is active.

## 5.2 During-Day Operations

Responsible: Operations Admin

Monitor:

* New orders.
* Vehicle assignment delays.
* Driver accept/reject/no-response.
* Loading delays.
* In-transit delays.
* POD upload status.
* OTP verification status.
* Settlement readiness.
* Supervisor cases.
* Blocked releases.
* Outbox event failures.

## 5.3 End-of-Day Checklist

Responsible: Operations + Finance + Supervisor

Before closing the day:

1. List all open orders.
2. List all stuck orders.
3. List all orders awaiting POD.
4. List all orders awaiting OTP verification.
5. List all settlement-ready orders.
6. List all settlement-blocked orders.
7. List all fraud holds.
8. List all settlement holds.
9. List all unresolved customer/driver complaints.
10. Export or record daily pilot issue log.
11. Confirm DB backup if pilot data is important.
12. Prepare next-day action list.

---

# 6. Order Lifecycle SOP

## 6.1 Order Creation

Trigger:

Customer creates order.

Required data:

* Customer ID
* Pickup address
* Drop address
* Contact person
* Material type
* Vehicle type or body requirement
* Weight/dimensions if available
* Invoice/shipment document if available
* Payment mode
* Expected pickup time

System action:

* Create order in draft state.
* Validate required fields.
* Assign trace ID.
* Assign idempotency key for state-changing request.
* Log order creation.

Manual check:

Operations admin should verify whether order is realistic for pilot scope.

## 6.2 Order Validation

Validation includes:

* Address completeness.
* Material type.
* Vehicle/body compatibility.
* Hazardous material flag.
* Customer status.
* Payment mode.
* Document requirement.
* Route feasibility.

If validation passes:

Move to validated/priced flow.

If validation fails:

Hold order and notify customer/admin.

## 6.3 Pricing

During MVP pilot:

Pricing may be semi-manual or system-assisted.

Pricing should consider:

* Distance
* Vehicle type
* Material type
* City/tier route
* Loading/unloading complexity
* Return-trip possibility
* Driver/provider cost
* Platform commission
* Pilot discount or manual adjustment

Hard rule:

No pricing should violate configured margin floor once margin rules are active.

## 6.4 Payment Mode

Allowed pilot modes:

* Manual payment confirmation
* Simulated payment
* Internal test payment record

Not allowed yet:

* Uncontrolled real payment automation
* Public payment gateway use without reconciliation
* Automatic external settlement

## 6.5 Order Confirmation

Order can be confirmed only when:

* Customer data is valid.
* Pricing is approved.
* Payment terms are accepted.
* Required documents are present or marked pending with approval.
* Policy preflight allows transition.

---

# 7. Vehicle Assignment SOP

## 7.1 Assignment Rules

Vehicle assignment must consider:

* Vehicle availability
* Vehicle body type
* Vehicle capacity
* Material compatibility
* Driver/vehicle verification
* Driver location
* Driver score
* Active trip status
* Reservation conflict

## 7.2 Assignment Cascade

Use this order:

1. Search within 5 km.
2. Search within 10 km.
3. Search transport company availability.
4. Check arriving/return-trip vehicles.
5. Escalate to operations.
6. Notify customer if no vehicle available.

## 7.3 Reservation Rule

Once a vehicle is selected:

* Create reservation.
* Prevent double booking.
* Apply reservation TTL.
* Release reservation if driver rejects, times out, or order is cancelled.

## 7.4 Driver Response

Driver can choose:

* Accept
* Cancel/Reject
* Later

Rules:

* Accept moves order toward driver assigned.
* Cancel moves to next candidate.
* Later excludes driver temporarily from same offer cycle.
* No response within SLA triggers reassignment.

---

# 8. Loading SOP

## 8.1 Driver Arrival at Pickup

Driver must:

* Reach pickup location.
* Confirm arrival.
* Upload loading evidence if required.
* Scan shipment document if available.
* Report mismatch, overload, wrong material, hazardous issue, or customer delay.

## 8.2 Loading Evidence

Required evidence may include:

* Loading photo
* Material photo
* Invoice/shipment document scan
* Timestamp
* Location metadata if available

## 8.3 Loading Delay

If loading delay exceeds threshold:

* Driver reports reason.
* Operations contacts customer.
* Supervisor case is created if dispute or policy risk exists.
* Delay is logged.

---

# 9. Transit SOP

## 9.1 Trip Start

Driver starts trip after loading completion.

System should log:

* Trip start time
* Vehicle location
* Route
* ETA
* Driver status

## 9.2 Monitoring

Operations should monitor:

* Vehicle movement
* Route deviation
* GPS loss
* Long halt
* Driver phone off
* Breakdown
* Accident
* Customer complaint
* RTO/police stop

## 9.3 Incident Handling

If incident occurs:

1. Driver reports through app or WhatsApp/manual channel.
2. Operations logs incident.
3. TMS/admin verifies severity.
4. Supervisor case is created if needed.
5. Customer is informed if ETA impact is serious.
6. Replacement vehicle is arranged if shipment is at risk.

---

# 10. Delivery, POD, and OTP SOP

## 10.1 Delivery Arrival

Driver reaches consignee location.

Driver must:

* Confirm arrival.
* Coordinate unloading.
* Upload delivery evidence.
* Upload POD.
* Collect consignee OTP.

## 10.2 POD Upload

Driver can upload POD/evidence.

Driver cannot verify POD.

POD verification can be done only by:

* Ops admin
* Supervisor
* Super admin

## 10.3 OTP Verification

OTP must come from consignee or authorized receiver.

Driver cannot self-verify OTP.

If OTP fails:

* Resend OTP if allowed.
* Contact consignee.
* Create exception case if consignee refuses.
* Do not mark delivery complete until resolved.

## 10.4 Delivery Completion

Delivery can move to settlement-ready only when:

* POD uploaded.
* POD verified.
* OTP verified.
* No unresolved delivery exception blocks completion.

---

# 11. Settlement SOP

## 11.1 Settlement Readiness

Settlement can be considered only when:

* Order exists.
* Trip exists.
* POD is verified.
* OTP is verified.
* No active fraud hold exists.
* No active settlement hold exists.
* Actor is finance admin or super admin.
* Policy preflight approves.
* Existing hard backend validation passes.

## 11.2 Settlement Release

Finance admin reviews settlement queue.

Before release, finance checks:

* Order ID
* Trip ID
* Provider/driver ID
* Amount
* POD status
* OTP status
* Fraud hold status
* Settlement hold status
* Journal status
* GST invoice record status
* Audit trail

If all pass:

* Release settlement.
* Create audit milestone.
* Create journal/GST visibility records if configured.
* Emit outbox event.

If blocked:

* Do not release.
* Record blocked reason.
* Show blocker code.
* Notify supervisor/finance queue.

Common blocker codes:

* FRAUD_HOLD_ACTIVE
* SETTLEMENT_HOLD_ACTIVE
* POD_NOT_VERIFIED
* OTP_NOT_VERIFIED
* WRONG_ROLE
* POLICY_CHECK_HOLD
* POLICY_CHECK_REJECTED

## 11.3 Duplicate Release Protection

If settlement release is requested twice:

* Do not double-release.
* Do not duplicate journal record.
* Do not duplicate GST invoice record.
* Return existing released status.
* Log idempotent replay if configured.

---

# 12. Supervisor Exception SOP

## 12.1 When to Create Supervisor Case

Create supervisor case for:

* Fraud suspicion
* POD mismatch
* OTP failure
* Driver misconduct
* Customer dispute
* Settlement block
* Policy check rejection
* Material compliance concern
* Vehicle/driver mismatch
* Payment complaint
* Repeated delay or no-show
* Transport company credibility issue

## 12.2 Supervisor Actions

Supervisor can:

* Hold case
* Approve case
* Reject case
* Create fraud hold
* Clear fraud hold
* Create settlement hold
* Clear settlement hold
* Record decision reason

Supervisor must not make silent changes.

Every decision must be auditable.

---

# 13. Policy Engine SOP

## 13.1 Policy Preflight

Policy preflight must run before high-risk actions:

* Settlement release
* Order state transition
* Future: vehicle assignment
* Future: payment confirmation
* Future: document verification
* Future: refund

Policy check result:

* Approved
* Hold
* Rejected

## 13.2 Policy Check Required Fields

Each policy check should include:

* Agent code
* Entity type
* Entity ID
* Requested action
* Trace ID
* Idempotency key
* Confidence score
* Decision reason
* Evidence references
* Payload

## 13.3 Policy Does Not Replace Backend Enforcement

Policy preflight asks:

**Should this action even be attempted?**

Backend validation asks:

**Can this action legally mutate the system?**

Both are required for high-risk operations.

---

# 14. Event Outbox SOP

## 14.1 Purpose

The event outbox records important system events durably so future notification workers can safely deliver messages.

## 14.2 Events to Track

Track events such as:

* Settlement released
* Settlement release blocked
* Fraud hold created
* Fraud hold resolved
* Settlement hold created
* Settlement hold cleared
* Policy check hold
* Policy check rejected
* Journal created
* GST invoice record created

## 14.3 Pilot Rule

During pilot, outbox events may be viewed internally.

Do not send real WhatsApp/SMS/email until provider integration is ready.

---

# 15. Finance and GST SOP

## 15.1 Pilot Finance Rule

During pilot:

* GST records may be system-generated or simulated.
* No live GST filing should happen.
* No live e-invoice/NIC/e-way automation should happen.
* Manual finance review is mandatory.

## 15.2 Broker/Agent Revenue Rule

Zippy acts as a platform/broker/agent where applicable.

Revenue should be treated carefully:

* Gross freight may be pass-through liability depending on principal-agent classification.
* Zippy revenue should generally be recognized as net commission where Zippy only arranges transport.
* Revenue recognition should happen only after delivery evidence is complete, especially POD and OTP.

## 15.3 Settlement Ledger Rule

For each completed trip, maintain:

* Customer amount
* Driver/provider payable
* Zippy commission
* Deductions/penalties if any
* GST invoice record
* Journal record
* Settlement status
* Audit trail

---

# 16. Security SOP

## 16.1 Environment Modes

Allowed environments:

* Development
* Pilot
* Production

Rules:

* Dev-login allowed only in development.
* Dev-login must return not found or blocked in pilot/production.
* Pilot must use controlled users.
* Production must use real auth and secure secrets.

## 16.2 Secrets

Never commit real secrets.

Secrets include:

* JWT secret
* Database URL
* Sentry DSN
* Payment keys
* WhatsApp/SMS keys
* GST/ULIP/VAHAN/NIC API keys
* Cloud storage credentials

## 16.3 Access Control

Roles must be enforced:

* Customer
* Driver
* Transport company
* Ops admin
* Finance admin
* Supervisor
* Super admin

Wrong-role actions must be blocked.

## 16.4 External Access

Before external access:

* Use HTTPS/TLS.
* Use reverse proxy or managed platform.
* Restrict CORS origins.
* Disable dev-login.
* Protect API docs if required.
* Use strong JWT secret.
* Enable backup.

---

# 17. Deployment SOP

## 17.1 Local Pilot Runtime

Use Docker runtime profile:

* Backend container
* Postgres container
* Alembic migration on startup
* Healthcheck against readiness endpoint

## 17.2 Health Checks

Use:

* `/health` for liveness
* `/ready` for readiness

Healthy means app is running.

Ready means app can connect to DB and required tables exist.

## 17.3 Migration Rule

On startup:

1. Run Alembic upgrade head.
2. If migration fails, container must exit.
3. Never serve app with schema drift.

## 17.4 Port Isolation

Do not run Docker backend on the same port used by Playwright E2E harnesses.

If Docker uses `8000`, stop Docker before E2E.

Alternative:

* Docker backend: `8001`
* E2E backend: `8000`

---

# 18. Backup and Restore SOP

## 18.1 Backup Rule

For pilot, backup at least daily if real operational data is entered.

Minimum backup:

* PostgreSQL dump
* Timestamped file name
* Stored outside container volume
* Restore tested weekly during pilot

## 18.2 Backup Command Example

Use environment-specific values.

```bash
pg_dump "$DATABASE_URL" > backups/zippy_pilot_YYYYMMDD.sql
```

## 18.3 Restore Command Example

```bash
psql "$DATABASE_URL" < backups/zippy_pilot_YYYYMMDD.sql
```

## 18.4 Restore Drill

Once per week:

1. Create temporary database.
2. Restore latest backup.
3. Run readiness check.
4. Confirm order, policy, outbox, settlement tables exist.
5. Record result.

---

# 19. Pilot Execution Plan

## Phase 1: Internal Demo

Users:

* 1 ops admin
* 1 finance admin
* 1 supervisor
* 1 test customer
* 1 test driver
* 1 test transport company

Goal:

Run one shipment lifecycle from order to settlement using controlled data.

## Phase 2: Staff Pilot

Users:

* Internal team only
* No public customer
* No uncontrolled money movement

Goal:

Run 5 to 10 simulated or manually controlled shipments.

## Phase 3: Friendly Business Pilot

Users:

* 1 to 3 trusted businesses
* Known drivers or transport partners
* Manual payment confirmation
* Manual document review

Goal:

Validate operational behavior, not scale.

## Phase 4: External Pre-Production

Only after:

* Real auth
* Real payment gateway
* Real communication provider
* Real document storage
* TLS
* Backup/restore
* Secrets management
* Production deployment
* Support process

---

# 20. KPIs for Pilot

Track daily:

| KPI | Target |
| --- | --- |
| Order creation success | 95%+ |
| Vehicle assignment success | 80%+ in pilot pool |
| Driver response time | Under 10 minutes |
| POD upload success | 95%+ |
| OTP verification success | 95%+ |
| Settlement release correctness | 100% |
| Duplicate settlement incidents | 0 |
| Wrong-role action success | 0 |
| Policy blocked mutation bypass | 0 |
| Open exception cases older than 24h | 0 |
| Backend health uptime during pilot | 99% internal target |

---

# 21. Escalation Matrix

| Issue | Owner | Escalate To | SLA |
| --- | --- | --- | --- |
| Order stuck before assignment | Ops Admin | Supervisor | 30 min |
| Driver no response | Ops Admin | TMS/Ops Lead | 10 min |
| Loading delay | Ops Admin | Supervisor | 60 min |
| POD mismatch | Supervisor | Super Admin | Same day |
| OTP failure | Supervisor | Ops Admin | 30 min |
| Settlement blocked | Finance Admin | Supervisor | Same day |
| Fraud hold | Supervisor | Super Admin | Same day |
| Backend unhealthy | Tech Admin | Founder/DevOps | Immediate |
| DB readiness failed | Tech Admin | Founder/DevOps | Immediate |
| Payment complaint | Finance Admin | Supervisor | Same day |
| Driver misconduct | Supervisor | Super Admin | Immediate |

---

# 22. What Not To Do During Pilot

Do not:

* Launch publicly.
* Use real customer money without payment reconciliation.
* Enable dev-login in pilot/production.
* Allow drivers to verify POD/OTP.
* Allow settlement without POD/OTP.
* Ignore fraud or settlement holds.
* Add new features before stabilizing pilot.
* Use real GST filing automation.
* Use real ULIP/VAHAN/NIC calls without test mode and legal review.
* Store unmasked sensitive IDs in agent-accessible logs.
* Run production without backup.

---

# 23. Final Operating Rule

The MVP is successful when one shipment can move through this flow repeatedly without manual database fixes:

**Order created -> validated -> priced -> confirmed -> vehicle assigned -> driver accepts -> loading evidence uploaded -> trip starts -> delivery reached -> POD uploaded -> OTP verified -> supervisor clears exceptions -> finance releases settlement -> audit/outbox records created -> order closed.**

Until this flow works reliably for multiple controlled pilot shipments, Zippy should remain in pilot mode.

The company operating philosophy:

**Move fast only where reversible. Move slowly where money, law, safety, or trust is involved.**
