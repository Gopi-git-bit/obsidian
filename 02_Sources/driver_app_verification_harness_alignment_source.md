---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-05-30
source_file: "D:\\Zippy_Driver_App_Verification_Harness_Alignment.docx"
notes: Driver app scenario verification and harness engineering alignment across Agent Algo, participant role/pricing logic, and driver app operational scenarios
---

# Driver App Verification Harness Alignment Source

## Overview

This source captures the driver-app verification and harness alignment report for Zippy Logistics. It cross-references the Driver App scenarios against the autonomous agent algorithm and the participant role/pricing logic to confirm whether driver-facing operations are fully covered by agent orchestration, state transitions, events, SLAs, pricing, and fallback behavior.

The document treats the Driver App as an operational surface that must remain synchronized with agent decisions. Every driver action should map to an agent and every agent output that affects the driver should have a clear driver-facing screen, event, timer, or escalation path.

## Source Scope

The report verifies alignment across:

- Agent Algo and autonomous agent responsibilities
- All Participants Role and pricing/dynamic context logic
- Driver App scenarios, states, events, and user stories
- Harness engineering requirements for events, state machine, pricing, SLA, and data schema consistency

Method used:

1. Decompose source documents into agents, states, events, scenarios, pricing rules, and SLA parameters.
2. Map every Driver App scenario to agent coverage, state transition, emitted events, SLA, and fallback path.
3. Reverse-trace agent actions back to driver-facing scenarios.
4. Check consistency between documents and identify gaps.

## Scenario Coverage Assessment

The Driver App contains 18 documented operational scenarios. The verification found:

| Result | Count |
|---|---:|
| Fully passed scenarios | 13 |
| Partial scenarios | 5 |
| Total assessed scenarios | 18 |

Partial scenarios:

| # | Scenario | Gap Type |
|---:|---|---|
| 4 | Refuse to load because of material type | Needs stronger agent definitions and payload/state clarity |
| 6 | Driver demands extra charges | Needs clearer payment/dispute event model |
| 11 | Payment not credited after POD | Needs complete settlement hold and dispute flow |
| 16 | Address or company not found | Needs stronger address-verification fallback |
| 17 | Phone switched off during trip | Needs stronger telemetry integrity and incident model |

## Key Driver-App Gaps

The report identifies 15 gap scenarios that should be converted into driver-app requirements, tests, and harness cases.

| Gap ID | Gap Description | Severity | Affected Agents | Priority |
|---|---|---|---|---|
| G-01 | Express delivery driver-side UI/SLA flow | Critical | OMS + TMS + Payment | P0 |
| G-02 | ToPay consent rejection at delivery point | Critical | OMA + Payment + Comm | P0 |
| G-03 | Structured loading/unloading late fees | High | Payment + OMS + DriverOps | P1 |
| G-04 | VTU mandate and GPS spoof detection | Critical | TMS + Risk/Fraud | P0 |
| G-05 | Transit damage reporting and insurance | High | Verification + Insurance | P1 |
| G-06 | Owner vs salaried driver ACL | High | DriverOps + Auth | P1 |
| G-07 | Offline mode and network resilience | Critical | All Agents | P0 |
| G-08 | Night driving and fatigue management | High | TMS + DriverOps | P1 |
| G-09 | RTO/checkpost stop handling | Medium | TMS + OMS | P2 |
| G-10 | Route disruption/weather driver side | Medium | TMS + Communication Agent | P2 |
| G-11 | Hazardous material structured compliance | High | OMA + Risk + Admin | P1 |
| G-12 | Loop order return trip discount flow | Medium | IMS + Payment | P2 |
| G-13 | Toll payment handling and reimbursement | Medium | Payment + TMS | P2 |
| G-14 | KYC document encryption and retention | Medium | Verification + Compliance | P2 |
| G-15 | Driver scoring and appeal workflow | Medium | DriverOps + Risk | P2 |

## Gap Resolution Rules

### Express Delivery Driver Flow

Express delivery must be visible to the driver as a distinct commitment, not just another order. The order assignment payload should include an express badge, stricter SLA timer, and commission display. The source preserves the express logic of vehicle age less than 3 years, driver score greater than or equal to 85, 30-70% surge pricing, and 15% commission versus 10% standard.

Driver app requirements:

- Show express badge with distinct color/icon.
- Show express SLA countdown.
- Require an explicit express acceptance confirmation.
- Display elevated commission rate on the order confirmation screen.

### ToPay Consent Flow

ToPay must be visible to the driver before departure, not discovered at delivery. The driver should see `consent_status` as pending, accepted, rejected, or timeout.

If consent is rejected or times out:

- OMS should notify the driver before departure.
- Driver App should allow wait-for-consignor, return-to-consignor, or support escalation.
- Payment and Communication agents should coordinate the resolution path.

### Loading and Unloading Late Fees

The source proposes a structured waiting policy:

| Waiting Time | Policy |
|---|---|
| First 15 minutes | Free |
| 15-60 minutes | 2% of order value per 15-minute block |
| Beyond 60 minutes | 5% per 15-minute block |

Driver app requirements:

- Show wait-time timer.
- Log elapsed waiting time automatically.
- Trigger alerts at 15, 30, and 60 minutes.
- Send late-fee calculation to Payment Agent for final invoice handling.

### Vehicle Telematics and GPS Integrity

Phone GPS alone is not sufficient for autonomous operations. The source recommends mandating Vehicle Telematics Units (VTU) for registered vehicles.

Driver app and TMS requirements:

- Compare phone GPS with VTU GPS.
- Flag discrepancy greater than 200 meters.
- Use VTU as authoritative source when phone and VTU differ.
- Treat phone-off or missing telemetry as an incident signal, not just a UI problem.

### Transit Damage Reporting

The Driver App needs a dedicated damage reporting flow for damage after pickup and before delivery.

Required behavior:

- Driver captures timestamped and geotagged photos.
- Driver records short damage description and suspected cause.
- OMS triggers incident workflow.
- Verification Agent checks EXIF and VLM evidence.
- Settlement is held pending damage assessment.
- Insurance workflow starts for declared shipment value orders.

### Owner vs Salaried Driver Authorization

The Driver App needs formal role-based access control.

| Role | Allowed Scope |
|---|---|
| Fleet Owner | Full vehicle, financial, and driver-management access |
| Salaried Driver | Accept/reject assigned vehicle orders; view current order and relevant payment history |
| Admin | Platform escalation and override access |

Every action must log `actor_id` and `actor_role`.

### Offline Mode and Network Resilience

Driver operations must survive weak network coverage.

Required behavior:

- Local-first storage using SQLite or similar embedded database.
- Cache state transitions, document scans, POD capture, and critical evidence locally.
- Sync when connectivity returns.
- Show clear offline indicator.
- Resolve conflicts if server state changed while the driver was offline.

### Night Driving and Fatigue Management

The source recommends explicit fatigue controls:

| Rule | Requirement |
|---|---|
| Warning threshold | Alert after 8 hours continuous driving |
| Mandatory rest threshold | Enforce after 10 hours continuous driving |
| Rest duration | Minimum 30-minute rest break |
| Cross-check | VTU engine-on time should verify driver-device records |

Route optimization should include rest stops in ETA calculations.

## Agent-to-Driver Interaction Mapping

| Agent | Driver-Facing Actions | Key Events | SLA / Timer |
|---|---|---|---|
| OMS Agent | Order offer, accept/cancel/later, reassignment, cancellation enforcement | `order_assigned`, `driver_response`, `driver_no_show_detected` | Accept: 10m; Movement: 15m |
| IMS Agent | Vehicle search, reservation, return trip matching | `vehicle_reservation_confirmed`, `return_trip_found` | Reservation TTL: 5m |
| TMS Agent | Route optimization, ETA updates, breakdown recovery, rerouting | `driver_started_trip`, `driver_arrived_pickup`, `vehicle_breakdown` | Breakdown: 30m recovery |
| Payment Agent | Advance release, final settlement, escrow, reconciliation | `advance_released`, `payment_settled`, `payment_dispute` | Settlement: 24h |
| Verification Agent | OCR, EXIF GPS validation, OTP, KYC validation | `shipment_doc_scanned`, `consignee_otp_verified`, `doc_validation_failed` | OTP expiry: 5m |
| Risk/Fraud Agent | POD fraud, misconduct, blacklisting | `fraud_detected`, `profile_blocked`, `rating_alert` | Strike threshold: 3 |
| Communication Agent | WhatsApp, chat support, translation | `notification_sent`, `whatsapp_message`, `translation_request` | 4 supported languages |
| DriverOps Agent | Penalty scoring, reliability, suspension, appeals | `penalty_applied`, `score_updated`, `appeal_submitted` | Appeal review: 48h |

## Harness Engineering Alignment

Harness engineering means creating a shared integration framework so Agent Algo, Participant Role/Pricing, and Driver App documents behave like one coherent system.

### Event Canonicalization

All driver-facing and agent-facing events should come from one canonical event registry. The registry should include:

- existing 20+ Agent Algo events
- Driver App event payload fields
- pricing events implied by participant role logic, such as `quote_generated` and `surcharge_applied`

### State Machine Unification

The Driver App and Agent Algo both reference 15-state models, but some names diverge. A single canonical state machine should own state names and transition rules. Driver App, OMS, TMS, IMS, and Payment Agent should reference the same artifact.

### Pricing Integration

Driver order assignment should include transparent pricing context:

- base transportation fee
- route difficulty surcharge, if applicable
- weather surcharge, if applicable
- deadhead adjustment, if applicable
- commission deduction
- final driver-visible amount

Pricing should be calculated by the OMS/Pricing service, not by the Driver App.

### SLA Harmonization

SLA values should move into centralized runtime configuration:

- 10-minute accept window
- 15-minute start movement timeout
- loading grace period
- retry counts and escalation thresholds

Driver App timers must read the same source of truth as OMS/TMS agents.

### Data Schema Consistency

Vehicle models, city tiers, pricing rules, and driver profiles should be defined once and shared through APIs. The Driver App should not maintain separate copies of vehicle models or pricing rules.

## Recommended Action Plan

### Phase 1 - Critical, Weeks 1-2

Resolve P0 gaps before production pilot:

- Express delivery driver flow
- ToPay consent rejection flow
- VTU mandate and GPS spoof detection
- Offline mode and conflict resolution
- Canonical event registry
- Unified state machine

### Phase 2 - High Priority, Weeks 3-6

Resolve P1 gaps before scaling beyond the initial pilot city:

- Loading late fee policy
- Transit damage reporting and VLM validation
- Owner vs salaried driver ACL
- Night driving/fatigue management
- Hazardous material compliance
- Pricing integration and transparent driver price breakdown
- Centralized SLA configuration

### Phase 3 - Medium Priority, Weeks 7-12

Resolve P2 gaps for broader operational robustness:

- RTO/checkpost handling
- Weather disruption driver flow
- Loop order return-trip discount display
- Toll reimbursement handling
- KYC encryption and retention
- Driver scoring and appeal workflow
- Unified schema completion for vehicles, city tiers, and driver profiles

## Testing Strategy

The source references 8 existing acceptance tests and recommends extending them to cover all 15 gaps.

Existing test coverage themes:

- Accept/Cancel/Later
- No-movement reassignment
- Advance release rollback
- Atomic reservation
- POD fraud
- Breakdown recovery
- Owner vs salaried driver ACL
- Payment gateway outage

Recommended additions:

| Test ID | Scenario |
|---|---|
| T9 | Express delivery SLA enforcement |
| T10 | ToPay consent rejection at delivery |
| T11 | GPS spoof detection and VTU cross-reference |
| T12 | Offline mode data synchronization |
| T13 | Transit damage reporting with VLM validation |
| T14 | Loading late fee calculation accuracy |
| T15 | Fatigue management enforcement |

Testing should include chaos scenarios for network outage, GPS spoofing, and payment gateway failure.

## Pilot Execution

Pilot recommendation:

- Single city pilot
- 50-200 orders
- 7-14 days
- Feature flags around ToPay, express pricing, auto-reassign, and fatigue management

Pilot SLIs:

- driver accept rate
- average accept latency
- POD fraud rate
- payments pending over 24 hours
- reassign rate
- express SLA compliance

Pilot results should feed SLA tuning, penalty calibration, and pricing parameter adjustment.

## Derived Notes

- [[Driver Frontend for Current Project]]
- [[Driver App Frontend Architecture]]
- [[02_Agentic_AI_Application]]
- [[scenario_context_engine_source]]
- [[Scenario Management Framework]]
- [[API and Event Contract for Current Project]]
- [[Role and Permission Matrix for Current Project]]
- [[Pricing Engine Backtest v1]]

## Related Notes

- [[Transportation Agent]]
- [[Resource Management Agent]]
- [[Payment Settlement Agent]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[SOP - Verify Shipment Documents]]
- [[SOP - Handle Vehicle Breakdown]]
- [[SOP - Handle Delayed Shipment]]

## Source Handling Note

This source should be used to update driver-app requirements, event contracts, scenario tests, and harness alignment after the remaining driver-app drafts are collected. It should not directly override existing driver architecture notes until the full driver-app documentation set is complete.
