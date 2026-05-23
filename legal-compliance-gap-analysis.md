# Legal Compliance And Finance-Control Architecture

Prepared: May 17, 2026

Primary source reviewed: `C:\Users\user\Downloads\compliance recorrection.txt`

Project reviewed: `C:\Users\user\Downloads\MiniMax Agent_ Minimize Effort, Maximize Intelligence_files`

Related internal references:

- `business-model-blueprint.md`
- `04_AI_Agents\Finance and Invoice Event Layer for Logistics Platform.md`
- `04_AI_Agents\Payment Settlement Agent.md`
- `04_Concepts\Compliance\Operational Compliance Framework for Indian Logistics Startup 2025-2026.md`

External anchors used for product interpretation:

- CBIC electronic way bill rules: https://cbic-gst.gov.in/ewaybill-rules.html
- NeGD/PIB DPDP Rules press release PDF: https://negd.gov.in/wp-content/uploads/2025/11/Press-Release_Press-Information-Bureau1-2.pdf

Note: This is product, engineering, and operating-control guidance, not legal advice. Final statutory interpretation, contract clauses, payment-flow design, insurance distribution posture, and go-live controls should be reviewed by Indian logistics, GST, privacy, insurance, and payments counsel.

## Executive Summary

The current project has a useful logistics transaction skeleton: order lifecycle states, vehicle model data, vehicle-fit recommendation, basic matching, pricing fields, and order transition audit events.

The next version needs a compliance and finance-control spine. Zippy should not be just a load board or a loose order tracker. The investment-grade direction is:

```text
ULIP and government systems = verified data gateway
Zippy backend = execution brain and compliance decision layer
Payment aggregator/bank partner = regulated money rail
Insurer API = risk-transfer and claim-evidence rail
```

The golden operating boundary is:

```text
Zippy verifies, records, transmits, and preserves evidence.
The insurer insures, decides, and pays claims.
```

This distinction must sit in contracts, backend design, admin SOPs, chatbot guardrails, and finance workflows. Zippy may freeze or release freight settlement under its order/payment rules, but it must not represent itself as the insurer, broker, claim advisor, or claim settlement authority unless a separately approved licensed model exists.

## Current Backend Baseline

| Area | Current implementation | Evidence |
|---|---|---|
| Order lifecycle | Basic statuses: `created`, `pending_match`, `matched`, `bidding`, `bid_accepted`, `in_transit`, `delivered`, `cancelled` | `backend/app/models/order_model.py`, `OrderStatus` |
| State machine enforcement | Blocks illegal order transitions and role-disallowed transitions | `backend/app/services/order_service.py`, `ORDER_STATUS_GRAPH`, `ROLE_STATUS_PERMISSIONS` |
| Order audit events | Stores lifecycle events with actor role, idempotency key, reason, and evidence reference | `backend/app/models/order_model.py`, `OrderStateEvent` |
| Vehicle model data | Stores GVW, payload, dimensions, body type, emission norm, etc. | `backend/app/models/vehicle_model.py`, `VehicleModel` |
| Vehicle fit recommendation | Recommends vehicle by payload with 20% buffer | `backend/app/api/vehicles.py`, `recommend_vehicles` |
| Basic GST amount field | Match has `gst_amount`, but not full invoicing/e-way bill compliance | `backend/app/models/order_model.py`, `Match` |
| E-way bill placeholders | E-way bill API credentials exist as config placeholders | `.env.example` |
| API tests | Tests order creation, transition, idempotency, and illegal transition blocking | `backend/tests/test_orders.py` |

Current gap: the project can move a digital order through operational states, but it cannot yet prove that the vehicle, driver, cargo, tax document, consent, payment, settlement, POD, and incident evidence were legally and financially controlled.

## Target Operating Architecture

### 1. ULIP Gateway Adapter

ULIP should be treated as a verified data gateway, not as the Zippy backend.

The adapter should handle:

- VAHAN vehicle verification: RC, fitness, permit, insurance, tax, PUC where available, vehicle class.
- SARATHI driver verification: license validity, class/endorsement, suspension or mismatch indicators where available.
- FASTag/NETC toll movement ingestion for toll stamps, ETA support, exception detection, and backhaul intelligence.
- GST/e-way bill validation for shipment movement control.
- DigiLocker document pulls for consented document retrieval.
- ICEGATE, LDB/container, FOIS, port, and multimodal APIs when EXIM or multimodal expansion becomes active.

Implementation pattern:

```text
ULIP API Gateway
  -> FastAPI ULIP Adapter
  -> Pydantic validation and schema normalization
  -> Event queue: Redis Streams first, Kafka later if volume justifies it
  -> PostgreSQL/PostGIS + Redis live cache + operational DB
  -> Compliance, Pricing, Dispatch, Finance, Insurance API, and Admin agents
```

Frontend apps and autonomous agents should not call ULIP directly. All calls must pass through the backend, carry a purpose code, be logged, and be tied to an order/trip/vendor context where applicable.

### 2. Real-Time State Engine

ULIP can provide verified snapshots and transport signals, but Zippy still needs its own live execution layer.

Recommended MVP posture:

```text
FASTag / GPS / Driver App / IoT
  -> MQTT broker, such as EMQX
  -> Vehicle State Processor
  -> Redis live-state cache
  -> WebSocket Gateway
  -> Customer dashboard, dispatcher dashboard, admin console, WhatsApp bot
```

Use Redis Streams and PostGIS before introducing Kafka unless event volume or replay requirements make Kafka necessary. The live state engine should generate exception events for GPS loss, unauthorized stop, route deviation, detention, accident, theft suspicion, and rescue-vehicle dispatch.

### 3. Spatial Execution Engine

PostGIS is mandatory for operational intelligence. ULIP does not replace spatial decisioning.

Use PostGIS for:

- 5 km -> 10 km -> 15 km vehicle search expansion.
- Dead-zone and surplus-zone tagging.
- Pincode heatmaps and corridor demand intelligence.
- Route risk scoring and high-theft-zone alerts.
- Warehouse catchment zones.
- Replacement/rescue truck dispatch.
- City-pair return-load probability scoring.

Minimum spatial tables:

| Table | Purpose |
|---|---|
| `vehicle_live_state` | Current vehicle location, status, freshness, source, and confidence |
| `geofence_zones` | Pickup zones, delivery zones, restricted zones, theft-prone zones, warehouse catchments |
| `pincode_demand_heatmap` | Demand/supply intensity by pincode and corridor |
| `dead_zone_registry` | Regions with weak return-load or supply risk |
| `return_load_candidates` | Candidate backhaul matches and ranking signals |
| `incident_events` | Accident, theft, detention, damage, GPS-loss, route-deviation events |

## Hard-Block Compliance Engine

The compliance engine should be a named backend service invoked before assignment, dispatch, rescue movement, payout, and certain admin overrides.

### Dispatch Hard Blocks

An order cannot move to `in_transit` when any mandatory check fails:

- Vehicle RC is inactive, missing, or expired.
- Fitness certificate is expired or missing where required.
- Permit is invalid, expired, missing, or mismatched to route/use case.
- Vehicle insurance is inactive or expired.
- PUC is expired or missing where required by the workflow.
- Driver license is inactive, expired, suspended, or mismatched to vehicle class.
- Hazardous cargo requires an endorsement, permit, SDS, emergency instructions, or eligible vehicle/driver, and any required item is missing.
- Cargo weight or volume exceeds legal/declared vehicle capacity.
- Shipment requires an e-way bill and the e-way bill is missing, expired, not valid for the movement, or stale after vehicle reassignment.
- Restricted/prohibited goods declaration is missing or fails screening.

CBIC e-way bill rules state that movement information must be furnished before commencement where applicable, Part B transport details are required in the specified cases, and transfer from one conveyance to another in transit requires compliance before further movement. Zippy should encode those rules as configurable rule versions, not hardcoded prose.

### Soft Blocks And Warnings

Use warnings where the workflow can continue with visibility:

- Vehicle, permit, insurance, fitness, PUC, or license expires soon.
- FASTag/toll movement signal is stale but GPS is fresh.
- GSTIN/invoice metadata mismatch needs ops review but does not yet affect dispatch.
- E-way bill validity is near expiry but still valid with enough route buffer.
- Driver rest or welfare signal needs review but is not a statutory dispatch stop in the current configured rule set.

Soft blocks should create an ops task, notify the responsible owner, and be visible in admin dashboards.

### Rescue Vehicle And Transshipment Rule

If cargo is moved to a replacement vehicle after breakdown, accident, detention, or operational rescue, movement must be blocked until:

- Replacement vehicle passes RC, fitness, permit, insurance, PUC, class, and capacity checks.
- Replacement driver passes license and role checks.
- E-way bill vehicle/transport details are updated as required before further movement.
- Transshipment or rescue reason is logged.
- Incident evidence packet is attached.
- Original vehicle and driver are placed into the correct hold/review state.

The rescue flow may re-route freight settlement operationally, but it must not alter insurance claim responsibility or decide claim value.

## Finance, Settlement, And Payout Guardrails

Finance is not the order brain. OMS owns lifecycle truth. Finance, Invoice, Settlement, Accounting, Tally, and Payment agents attach money-control events to that truth.

### Boundary Model

```text
OMS owns: order state, holds, lifecycle closure
TMS owns: trip execution evidence
IMS/WMS owns: inventory, loading, unloading, storage evidence
Payment Agent owns: collection and payment-status events
Invoice Agent owns: compliant invoice generation
Settlement Agent owns: payout-readiness evaluation
Accounting Agent owns: ledger truth
Admin Agent owns: overrides, risk governance, audit, retention
Communication Agent owns: invoice, receipt, alert, and dispute messages
```

Every operational event should produce the right financial event. Every financial event should produce a controlled accounting record. No financial agent should casually change OMS state.

### Payment Compliance Guardrails

- Do not store raw card data.
- Treat customer fund custody as a regulated design decision, not a default shortcut.
- Use an authorised payment aggregator, bank, escrow, linked-account, or approved partner-led settlement path where required.
- Record who collected the funds, where the funds are held, and whether payout is partner-executed or platform-executed.
- Refund to the original payment method unless customer consent and the payment partner flow support an alternate method.
- Map every collection, refund, split transfer, chargeback, dispute freeze, and payout release to `order_id`, `trip_id`, `invoice_id`, `pod_id`, and `ledger_entry_id`.
- Failed, refunded, reversed, or disputed payment states block settlement until cleared.

### Payout Hard Blocks

Provider payout must remain blocked unless all are true:

- Required customer payment condition is satisfied.
- Payment custody path is legally approved for the transaction type.
- Beneficiary KYC and bank verification pass.
- POD or delivery evidence is verified.
- No active dispute, damage flag, amount mismatch, incident hold, or compliance hold exists.
- Required tax invoice, settlement statement, and ledger events exist.
- Admin override, if any, is maker-checker approved and still unexpired.

### Freight Settlement Is Not Insurance Claim Settlement

Freight settlement is controlled by Zippy's payment workflow and contract terms. It can consider POD, OTP, dispute window, damage report, detention, rescue movement, and settlement rules.

Insurance claim settlement is controlled only by the licensed insurer. Zippy may transmit evidence and status, but should not approve, reject, value, negotiate, or guarantee insurance claims.

## Insurance Boundary Engine

Zippy must maintain a strict insurance boundary unless a separately licensed and counsel-approved structure is created.

Zippy should not present itself as:

- Insurer.
- Insurance broker.
- Corporate agent.
- Web aggregator.
- Claim advisor.
- Claim settlement authority.

Allowed product posture:

- Verify policy status through insurer or partner API.
- Store policy reference and coverage metadata as evidence.
- Collect customer/driver consent for data sharing.
- Transmit claim evidence packets to insurer.
- Store insurer API responses and response hashes.
- Show claim status as received from insurer.

Disallowed product posture without licensing/legal sign-off:

- Recommend insurance as advice.
- Decide whether a claim is payable.
- Promise claim approval or payout.
- Handle premium custody unless the insurer/payment partner structure explicitly supports it.
- Modify policy terms or claim values.

## DPDP Privacy And Consent Layer

The DPDP posture should be implemented now as product readiness, not postponed. The design should support notice, consent, purpose limitation, access control, retention, breach response, and third-party data sharing controls.

### Consent Ledger

Create consent records for:

- Customer operational data processing.
- Driver/SFO operational data processing.
- Location and trip telemetry.
- Document verification and DigiLocker/ULIP access where applicable.
- Insurer API evidence sharing.
- Marketing communications, kept separate from operational consent.

Insurance API consent should be explicit:

- Customer consents to sharing invoice, e-way bill, trip, cargo, POD, incident, and route data with insurer.
- Driver/SFO consents to sharing vehicle, license, location, incident, and compliance data with insurer only for claim/compliance purposes.
- `consent_id` must be attached to every insurer API call.

### Purpose Codes

Every sensitive API call or personal-data access should carry a purpose code:

- `ULIP_VAHAN_PRE_DISPATCH_CHECK`
- `ULIP_SARATHI_DRIVER_CHECK`
- `INSURER_POLICY_STATUS_LOOKUP`
- `INSURER_CLAIM_EVIDENCE_SUBMISSION`
- `PAYMENT_SETTLEMENT_RELEASE`
- `PAYMENT_DISPUTE_FREEZE`
- `EWAYBILL_PARTB_UPDATE`
- `HAZMAT_PERMIT_VALIDATION`
- `POD_VERIFICATION`
- `INCIDENT_EVIDENCE_REVIEW`

Minimum log fields:

- `actor_id`
- `agent_id`
- `purpose_code`
- `legal_basis`
- `consent_id`, where applicable
- `order_id`
- `trip_id`
- `data_fields_accessed`
- `timestamp`
- `result`
- `request_hash`
- `response_hash`

This makes the audit posture concrete: not "we probably checked it," but "this exact actor or agent accessed these fields for this declared purpose at this time."

## Forensic Evidence Vault

Evidence must be first-class data, not random chat attachments.

Required evidence categories:

- Vehicle document snapshots.
- Driver document snapshots.
- GST invoice and e-way bill snapshots.
- Loading photos and loading checklist.
- Seal photo and seal number for high-value cargo.
- Packaging acknowledgement and defect notes.
- GPS trail and toll stamps.
- POD photo, consignee OTP/signature, timestamp, and GPS point.
- POD OCR output where used.
- Accident photos, FIR reference, emergency response notes.
- Theft alert packet, GPS-loss event, unauthorized-stop evidence, police complaint pack.
- Damage photos, delivery damage declaration, hidden damage claim packet.
- Dispute evidence, reviewer decision, settlement impact.

Evidence storage requirements:

- Store content-addressed file reference or object-storage key.
- Store cryptographic hash.
- Store uploader, source device, timestamp, and evidence category.
- Link to order, trip, vehicle, driver, party, dispute, incident, or claim as applicable.
- Support hash chaining for legal audit events.
- Preserve legal hold when dispute, claim, police case, or counsel instruction is active.

## Human Override Governance

Hard-block systems need override controls, because APIs fail and field operations can face genuine exceptional conditions.

### No-Override Cases

Do not allow human override for:

- Expired or inactive RC.
- Expired fitness certificate where required.
- Invalid, expired, suspended, or mismatched driver license.
- Missing hazardous-goods endorsement or safety documentation where required.
- Missing required e-way bill for a legally required movement.
- Final payout release without POD/OTP/equivalent delivery evidence.
- Bank account mismatch against onboarded vendor/KYC identity.

### Conditional Override Cases

Temporary override may be allowed only when:

- API downtime prevents fresh verification.
- Cached verification is fresh within configured SLA.
- No critical document is known to be expired.
- Maker-checker approval is completed.
- Override reason, approver, expiry, evidence, and risk acceptance are logged.
- Override cannot release final payout unless payout gates pass.

Every override should expire automatically and be visible in admin risk reports.

## Data Model Additions

| Table | Purpose |
|---|---|
| `vehicle_compliance_documents` | RC, permit, fitness, insurance, PUC, expiry alerts, verification source |
| `driver_compliance_documents` | License, license class, endorsements, training, ID, expiry alerts |
| `vehicle_compliance_snapshot` | Point-in-time compliance state used for assignment/dispatch decision |
| `driver_compliance_snapshot` | Point-in-time driver compliance state used for assignment/dispatch decision |
| `compliance_checks` | Pre-assignment, pre-dispatch, rescue, and payout pass/fail checks |
| `legal_audit_logs` | Tamper-evident action and compliance log with hash chaining |
| `document_evidence` | Uploaded documents/photos with hashes and categories |
| `pod_evidence` | POD, OTP, signature, photos, OCR, delivery GPS, damage notes |
| `eway_bills` | E-way bill number, validity, Part A/B metadata, vehicle update status |
| `gst_invoices` | Invoice data linked to orders, settlements, and accounting |
| `consent_ledger` | DPDP consent/notice records, versions, withdrawal status, channel |
| `purpose_code_access_log` | Sensitive API and data-access log with declared purpose |
| `insurer_api_call_log` | Insurer API calls, data shared, consent ID, response hash |
| `vendor_kyc` | PAN, GSTIN, bank penny-drop, beneficial owner declaration, screening |
| `payment_settlement_events` | Collection, refund, chargeback, split transfer, payout, hold, release |
| `human_override_approvals` | Maker-checker approvals, scope, reason, expiry, evidence |
| `incident_cases` | Accident, theft, damage, delay, overload, detention, route deviation |
| `disputes` | Customer/carrier/payment disputes, evidence, decision, settlement impact |
| `insurance_policies` | Policy references and status metadata from insurer/partner |
| `insurance_claims` | Claim evidence transmission and insurer-provided status tracking |
| `contracts` | Service agreements, addendums, acceptance records, versioning |
| `state_regulations` | Route/state-specific permit, night movement, load, commodity rules |

## API And Event Additions

### API Groups

| Endpoint group | Example endpoints |
|---|---|
| Compliance checks | `POST /orders/{id}/compliance-check`, `GET /orders/{id}/compliance-status` |
| Vehicle documents | `POST /vehicles/{id}/documents`, `GET /vehicles/{id}/documents`, `GET /vehicles/expiring-documents` |
| Driver documents | `POST /drivers/{id}/documents`, `GET /drivers/{id}/compliance-status` |
| E-way bill | `POST /orders/{id}/eway-bill`, `POST /orders/{id}/eway-bill/validate`, `POST /orders/{id}/eway-bill/update-vehicle` |
| POD | `POST /orders/{id}/pod`, `GET /orders/{id}/pod` |
| Incidents | `POST /orders/{id}/incidents`, `GET /incidents`, `PATCH /incidents/{id}` |
| Disputes | `POST /orders/{id}/disputes`, `GET /disputes`, `PATCH /disputes/{id}/resolution` |
| Consent/privacy | `POST /consents`, `GET /users/{id}/consents`, `POST /privacy/data-access-log` |
| Insurance API | `POST /orders/{id}/insurance/policy-status`, `POST /claims/{id}/evidence-packet` |
| Settlement | `POST /orders/{id}/settlement/evaluate`, `POST /settlements/{id}/hold`, `POST /settlements/{id}/release` |
| Contracts | `POST /contracts/acceptance`, `GET /contracts/{id}` |

### Critical Events

| Event | Owner | Purpose |
|---|---|---|
| `compliance_check_requested` | Compliance Agent | Start vehicle/driver/order validation |
| `compliance_check_failed` | Compliance Agent | Block assignment, dispatch, rescue, or payout |
| `dispatch_blocked` | OMS | Prevent movement and create remediation task |
| `ewaybill_vehicle_update_required` | Compliance Agent | Block rescue or reassignment until Part B/transport details are current |
| `pod_submitted` | TMS | Attach delivery evidence to trip/order |
| `pod_verified` | Settlement Agent | Make payout eligible if other gates pass |
| `payment_received` | Payment Agent | Record collection status without directly closing OMS |
| `settlement_hold_created` | Settlement Agent | Freeze payout due to dispute, evidence, payment, compliance, or custody issue |
| `settlement_release_approved` | Settlement Agent/Admin Agent | Allow payout only after gates and approvals |
| `insurer_evidence_submitted` | Insurance API Agent | Transmit claim packet without deciding claim |
| `human_override_requested` | Admin Agent | Start maker-checker flow |
| `human_override_expired` | Admin Agent | Remove temporary exception automatically |

## Implementation Roadmap

### P0: Production-Blocking Controls

- Add compliance data models for vehicle documents, driver documents, compliance checks, e-way bill metadata, POD evidence, legal audit logs, consent ledger, and settlement events.
- Add pre-dispatch compliance service and wire it into order transition before `in_transit`.
- Add payout gate service and block provider payout unless POD, payment, KYC, custody, dispute, and compliance gates pass.
- Add e-way bill validation and vehicle-update workflow for normal dispatch and rescue movement.
- Add purpose-code access logging for ULIP, insurer, payment, e-way bill, POD, and incident actions.
- Add legal audit hashing for compliance checks, overrides, POD, disputes, and settlement decisions.

### P1: Risk And Evidence Workflows

- Add incident case workflows for accident, theft, damage, delay, overload, detention, and GPS loss.
- Add dispute workflow with evidence upload, reviewer decision, settlement impact, and escalation path.
- Add insurer API call log and evidence-packet submission flow.
- Add vendor KYC gate: PAN, GSTIN, bank penny-drop, beneficial owner declaration, and bank-name mismatch payout block.
- Add privacy controls for consent withdrawal, data access logging, retention, and breach response tasks.
- Add expiry reminders for vehicle/driver compliance documents.

### P2: Advanced Compliance Intelligence

- Add PostGIS geofence/risk zone model for high-theft routes, restricted areas, and warehouse catchments.
- Add state-specific route regulation rules.
- Add cold-chain, food, pharma, and hazardous-goods specialized compliance modules.
- Add dashboard views for compliance risk, pending overrides, payout holds, document expiry, insurer evidence status, and DPDP audit posture.
- Add Kafka only if replay, throughput, or long-term event-stream requirements exceed Redis Streams.

## Operational SOP Implications

Admin and ops teams need SOPs for:

- Failed dispatch compliance check.
- E-way bill expiry during transit.
- Rescue vehicle and transshipment.
- Accident response and evidence packet creation.
- Theft or GPS-loss escalation.
- Cargo damage at pickup or delivery.
- POD dispute and hidden damage claim window.
- Payment dispute, refund, chargeback, and settlement freeze.
- Human override maker-checker approval.
- DPDP breach response and legal hold.
- Insurer evidence transmission without insurance advice.

## Acceptance Review Checklist

The refined architecture is ready for implementation when the product and backend design answer these questions:

- What blocks dispatch?
- What blocks payout?
- What is only a warning?
- Who can override, when, and with what audit trail?
- What evidence is needed for POD, accident, theft, damage, dispute, and insurance support?
- Which agent owns each lifecycle: OMS, TMS, IMS/WMS, Finance, Settlement, Admin, Insurance API, Compliance?
- Which sensitive data access requires a consent ID, purpose code, legal basis, and response hash?
- Which money movements are partner-executed, platform-executed, escrowed, refunded, disputed, or held?

## Final Product Decision

Proceed with the compliance layer, but implement the insurance side as API evidence infrastructure, not as an insurance product.

Minimum production-ready compliance spine:

- Verified vehicle and driver documents.
- E-way bill/GST metadata and dispatch enforcement.
- Digital POD and delivery evidence.
- Payment, custody, settlement, and payout states.
- Legal audit log with evidence hashes.
- Incident and dispute workflows.
- DPDP consent, purpose-code access logs, and retention controls.
- Insurance API evidence log without claim-decision authority.

Zippy's strategic advantage should be trust, utilization, settlement speed, and compliance proof. The backend should make those claims operationally true.
