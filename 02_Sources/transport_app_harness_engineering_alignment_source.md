---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-05-30
source_file: "D:\\Zippy_Transport_App_Harness_Engineering_Alignment.docx"
notes: Transport Company App verification and harness engineering alignment for dual-role hirer/service-provider architecture
---

# Transport App Harness Engineering Alignment Source

## Overview

This source captures the Transport Company App verification and harness engineering alignment report for Zippy Logistics. It focuses on the app's dual-role architecture: a registered transport company can act as a vehicle hirer when it needs capacity, and as a service provider when it has available fleet capacity.

The document cross-references the Transport App against the Agent Algorithm, participant/pricing logic, and Driver App harness alignment. Its main purpose is to ensure that the Transport App does not operate as an isolated B2B surface, but as a coherent part of the Zippy autonomous logistics platform.

## Source Scope

The report verifies:

- Transport Company App dual-role flows
- Agent Algo and autonomous orchestration responsibilities
- participant/pricing logic from the scenario context and pricing documents
- Driver App harness alignment standards
- cross-app event, state, pricing, payment, notification, and schema consistency

Method used:

1. Decompose the Transport App, Agent Algo, participant/pricing logic, and Driver App harness documents.
2. Map the 10 Transport App scenarios to agents, states, events, SLAs, and fallback paths.
3. Analyze dual-role conflicts where one company acts as hirer and service provider in overlapping workflows.
4. Reverse-trace agent actions back to transport-company UI and workflow surfaces.
5. Check consistency across commission, pricing, event naming, state vocabulary, and cross-app boundaries.

## Transport App Dual-Role Architecture

The Transport Company App serves registered transport companies that manage fleet capacity, typically in the 5-10 vehicle range. It is different from the Driver App because it supports company-level fleet coordination rather than individual driver operations.

| Role Context | UI Signal | Operational Meaning |
|---|---|---|
| Hirer | Orange toggle / orange dots | Company places orders to other transport companies when its own capacity is insufficient |
| Service Provider | Blue toggle / blue dots | Company receives and fulfills orders from other transport companies |

Important boundaries:

- The Transport App is for inter-transport-company coordination.
- End customers of transport companies should not receive B2B map, tracking, or payment visibility.
- Hirers can track the service-provider vehicle.
- Service providers can access route optimization.
- The platform should not over-intervene in private B2B settlement unless the order enters a platform-mediated path.

## Commission and Payment Model

The source preserves a simple adoption-friendly commission model:

| Case | Commission / Payment Rule |
|---|---|
| Short-distance LCV trip | INR 150 flat commission |
| Long-distance or CV/HCV trip | INR 350 flat commission |
| Optional GPay/Paytm payment gateway | Additional 2% commission on total shipment value |
| Driver App individual-driver fulfillment | Standard 10% commission applies |
| Platform-mediated individual-driver path | 40% advance and 60% settlement flow applies |

The Transport App's payment handling must keep B2B direct settlement separate from platform-mediated driver/customer settlement.

## Scenario Coverage Assessment

The Transport App document contains 10 documented operational scenarios.

| Result | Count |
|---|---:|
| Fully passed scenarios | 4 |
| Partial scenarios | 6 |
| Total assessed scenarios | 10 |

| ID | Scenario | Verdict |
|---|---|---|
| S-01 | Customer cannot access map/status in B2B orders | PASS |
| S-02 | Hirers do not pay advance to service providers | PARTIAL |
| S-03 | Consignee refuses ToPay; service-provider impact | PARTIAL |
| S-04 | Hirer doubts new transport company credibility | PARTIAL |
| S-05 | Customer needs multiple vehicles; individual-owner shortage | PARTIAL |
| S-06 | Service provider requests platform payment gateway | PASS |
| S-07 | Hirer cannot find appropriate vehicle from service providers | PASS |
| S-08 | Hirer cancels before vehicle leaves origin | PASS |
| S-09 | Hirer cancels after vehicle reaches consignor | PARTIAL |
| S-10 | Vehicle accident, theft, or material damage | PASS |

The partial scenarios are handled conceptually but need stronger event payloads, agent ownership, state transitions, or cross-app mappings.

## Identified Gaps

| Gap ID | Description | Severity | Affected Agent | Priority |
|---|---|---|---|---|
| G-01 | GST Verification Automation | Critical | Verification Agent | P0 |
| G-02 | Reputation Scoring System (TCRS) | Critical | Notification/Risk Agent | P0 |
| G-03 | IMS-to-Transport Handoff Trigger | High | IMS/OMS Agent | P1 |
| G-04 | Dual-Role Conflict Resolution | High | IMS Agent | P1 |
| G-05 | Advance Payment and Escrow B2B paths | High | Payment Agent | P1 |
| G-06 | Cancellation After Vehicle Dispatch | Medium | OMS/TMS Agent | P1 |
| G-07 | Fake Order and Fraud Detection | Medium | Risk/Fraud Agent | P2 |
| G-08 | Vehicle Model AI Matching | Medium | RMA Agent | P2 |
| G-09 | Offline and Low-Connectivity Mode | Medium | TMS/Local Storage | P2 |
| G-10 | Shipment and POD Scanning Integration | Medium | Verification Agent | P2 |
| G-11 | Multi-Vehicle Order Support | Low | OMS/IMS Agent | P3 |
| G-12 | Notification Deduplication | Low | Notification Agent | P3 |

## Gap Resolution Rules

### GST Verification Automation

Registration should not rely only on manual review. The Transport App should validate GSTIN through the Indian Government GST API and verify the landline through IVR OTP within 5 minutes.

Required data:

- GST verification status
- landline verification status
- verification timestamp
- API response
- KYC status

Failed verification should restrict the company to view-only mode until corrected and re-verified.

### Reputation Scoring System

The source proposes a Transport Company Reliability Score (TCRS) from 0-100.

| Factor | Weight |
|---|---:|
| Order completion rate | 30% |
| Payment dispute frequency | 25% |
| Average delivery time adherence | 20% |
| Response time to order acceptance | 15% |
| Customer/peer feedback score | 10% |

Governance thresholds:

- TCRS below 40: automated warning.
- TCRS below 20: automatic suspension pending manual review.
- Suspended companies should have a formal appeal path within 7 business days.

### IMS-to-Transport Handoff Trigger

The handoff from individual vehicle-owner search to transport-company pool needs deterministic triggers.

Required behavior:

- Search individual vehicle owners within 10 km for 10 minutes.
- If no match, escalate to transport company pool.
- If no transport company accepts within 5 minutes, check ETA of arriving vehicles.
- If no suitable vehicles are expected, broadcast via WhatsApp RAG Agent.
- Log trigger reason, timestamp, and contacted candidates.
- Show current search phase in Transport App.

### Dual-Role Conflict Resolution

The same transport company may act as hirer and service provider at the same time. Inventory must be unified so the same vehicle is not double-booked across role contexts.

Required behavior:

- One inventory pool per transport company.
- Vehicles committed in hirer orders cannot appear as available in service-provider mode.
- Role toggle updates available vehicle count.
- Dashboard shows committed and available vehicles by role context.

### Payment Path Definition

The report defines three payment paths:

| Path | Situation | Payment Event |
|---|---|---|
| A | Transport-to-Transport B2B | `b2b_settled_directly` |
| B | Transport Hirer uses individual drivers from Driver App | `platform_mediates_advance` |
| C | Customer uses transport company pool | `customer_pays_platform` |

Path B should preserve the 40% advance and 60% settlement flow from the Driver App. Path A should avoid platform intervention in private B2B settlement.

### Cancellation After Dispatch

If a hirer cancels after the vehicle reaches or travels toward the consignor, the base price should be calculated from vehicle location to consignor destination using the same pricing engine. The Transport App should show the amount before cancellation and warn that unpaid cancellation charges block new orders.

### Fake Order and Fraud Detection

The Risk/Fraud Agent should monitor:

- cancellation rate above 30% after dispatch
- more than 2 payment disputes per month
- shared credentials across multiple accounts
- unusual off-peak order volume

Disputes should require timestamped order records, GPS coordinates, and communication logs. Blocking should use TCRS penalty workflow, not informal WhatsApp group expulsion.

### Vehicle Model AI Matching

The RMA Agent should support three input modes:

- model name exact match
- body length with +/- 5% tolerance
- loading capacity with same or next higher class, max +500 kg

The shared `vehicle_models` schema should be authoritative for Driver App and Transport App.

### Offline and Low-Connectivity Mode

The Transport App should use local-first behavior for:

- accept/reject order
- shipment document scan
- POD capture
- role toggle state
- queued notifications

On reconnect, conflicts must be resolved when an offline acceptance overlaps with a server-side assignment.

### Shipment Document and POD Scanning

The Transport App service-provider interface should reuse Driver App document verification patterns:

- shipment document OCR validation
- GPS-verified scan at consignor
- consignee OTP verification
- EXIF validation
- temporary driver session token that expires after POD completion

### Multi-Vehicle Orders

The order form should support multi-vehicle requests up to a configurable maximum of 10. OMS splits the master order into sub-orders; IMS reserves each sub-order independently; the hirer sees a consolidated status view.

### Notification Deduplication

Transport companies need one notification feed across both roles.

Required behavior:

- unified chronological feed
- `role_context` on every notification
- orange/blue role color coding
- priority sorting for cancellations and payment disputes
- one combined notification badge count

## Agent-to-Transport Company Interaction Mapping

| Agent | Hirer Interactions | Service Provider Interactions | Shared Events |
|---|---|---|---|
| OMS Agent | Order placement, cancellation, tracking, payment status | Order receipt, acceptance/rejection, fulfillment tracking | `order_assigned`, `order_confirmed`, `order_cancelled` |
| IMS Agent | Vehicle search request, fleet availability check | Vehicle inventory registration, availability toggle | `vehicle_search_initiated`, `inventory_updated` |
| RMA Agent | Vehicle model search, body length/capacity matching | Fleet exposure to hirers, vehicle matching | `vehicle_matched`, `vehicle_reserved` |
| TMS Agent | Real-time tracking, ETA monitoring, route viewing | Route optimization, delivery navigation, fuel/repair assist | `tracking_update`, `eta_calculated`, `route_optimized` |
| Payment Agent | Payment history viewing with orange dots, invoice download | Commission payment, gateway transaction | `payment_recorded`, `commission_deducted`, `invoice_generated` |
| Notification Agent | Order status alerts, cancellation notices, dispute alerts | New order alerts, acceptance reminders, payment alerts | `notification_sent`, `alert_triggered` |
| Verification Agent | GST/landline verification, profile editing OTP | Vehicle registration, driver assignment | `kyc_verified`, `vehicle_registered` |
| Risk/Fraud Agent | Fraud detection, credibility scoring, blocking | Complaint filing, peer review reporting | `fraud_detected`, `complaint_filed`, `company_blocked` |

## Dual-Role State Machine

The Transport App needs parallel state tracking for hirer and service-provider contexts.

| State | Hirer Context | Service Provider Context | Trigger |
|---|---|---|---|
| REGISTERED | Company verified and onboarding complete | Same | GST/landline verified |
| ACTIVE | Available to place orders | Available to receive and fulfill orders | Role toggle |
| HIRER_ORDER_PLACED | Order submitted to service providers | N/A | order booking submitted |
| HIRER_MATCHING | Searching service providers | N/A | IMS searching transport pool |
| HIRER_ASSIGNED | Service provider accepted order | N/A | `accept_order` |
| HIRER_TRACKING | Vehicle en route, tracking active | N/A | `tracking_update` |
| HIRER_DELIVERED | Goods delivered, awaiting payment | N/A | `delivery_confirmed` |
| SP_ORDER_RECEIVED | N/A | New order from hirer received | `order_assigned` |
| SP_ACCEPTED | N/A | Order accepted, driver assigned | `accept_order` |
| SP_IN_TRANSIT | N/A | Driver en route to consignor | `driver_started_trip` |
| SP_LOADING | N/A | At consignor, loading goods | `shipment_doc_scanned` |
| SP_DELIVERING | N/A | En route to consignee | `driver_departed_for_delivery` |
| SP_DELIVERED | N/A | POD scanned, OTP verified | `pod_scanned` + `otp_verified` |
| SP_SETTLED | N/A | Payment received, commission deducted | `payment_settled` |
| CANCELLED | Order cancelled by hirer or platform | Order cancelled by service provider | `cancel_order` |
| SUSPENDED | Company suspended due to fraud/penalty | Same | `company_blocked` |

A company can occupy different states for different orders at the same time. The role toggle changes the default view, not the existence of active orders in the other role.

## Harness Engineering Alignment

### Event Canonicalization

The Transport App should adopt the canonical event registry from the Driver App harness and extend it with transport-specific events:

- `transport_company_registered`
- `dual_role_toggled`
- `b2b_order_placed`
- `b2b_order_accepted`
- `commission_deducted`
- `transport_company_scored`

### State Machine Unification

Shared states such as REGISTERED, ACTIVE, CANCELLED, and SUSPENDED should use the same canonical names across apps. Transport-specific states should use `HIRER_` and `SP_` prefixes to keep role context explicit.

### Pricing Integration

The Transport App supports custom negotiated pricing and system-generated pricing. System-generated pricing should use the same multi-factor pricing engine from the scenario context source and then add the flat transport commission.

```text
system_price = pricing_engine.calculate(origin, destination, vehicle_type, weight) + commission_slab(distance, vehicle_type)
```

The app should display base fee, route difficulty surcharge, deadhead adjustment, and platform commission separately.

### SLA Harmonization

Shared SLA values:

- offer TTL / acceptance window: 10 minutes
- search cascade: 5 km, then 10 km, then transport company pool
- transport company acceptance timeout: 5 minutes
- loading grace period: first 15 minutes free

All SLA values should come from centralized runtime configuration.

### Data Schema Consistency

Shared schemas should include:

- `vehicle_models`
- `city_tiers`
- `pricing_rules`
- `transport_companies`
- `transport_fleets`
- `transport_orders`
- `transport_payments`

The `transport_companies` table should include `company_id`, `gst_number`, `landline_number`, `authorized_person_phone`, `address`, `fleet_composition`, `tcrs_score`, `kyc_status`, and `role_status`.

## Cross-App Ecosystem Integration

| Fulfillment Path | Commission Structure | Payment Mediation | Tracking Access |
|---|---|---|---|
| Customer -> Individual Driver | 10% of shipment value | Platform mediates 40% advance and 60% settlement | Full customer tracking |
| Customer -> Transport Co | INR 150/350 flat commission | Direct B2B, no platform mediation | Hirer tracks; customer cannot |
| Transport Co -> Individual Driver | Transport Co pays 10% + INR 150/350 to platform | Platform mediates driver payment | Transport Co tracks |
| Transport Co -> Transport Co | INR 150/350 from service provider | Direct B2B, no platform mediation | Hirer tracks; end customer excluded |
| Transport Co -> Customer's Own Fleet | No commission | No platform involvement | Full tracking via Driver App |

Notification boundaries:

- Customer App receives vehicle-assigned updates when a customer order is fulfilled by transport-company fleet.
- Driver App receives no notification unless an assigned driver is actually registered on Driver App.
- Admin/OMS receives all events for audit and monitoring.
- Transport App receives role-scoped notifications without leaking private B2B payment information to end customers.

## Recommended Action Plan

### Phase 1 - Critical, Weeks 1-3

- GST API verification and IVR landline validation
- TCRS scoring and appeal workflow
- transport-specific event registry
- dual-role state machine as shared artifact

### Phase 2 - High Priority, Weeks 4-8

- IMS-to-Transport handoff triggers
- unified inventory view and double-booking prevention
- three payment paths with distinct settlement events
- system-generated pricing integration

### Phase 3 - Medium Priority, Weeks 9-14

- cancellation base-price calculation
- fraud/anomaly monitoring
- vehicle model matching by length/capacity
- offline mode
- shipment and POD scanning
- multi-vehicle order support
- notification deduplication
- shared schema completion

## Testing Strategy

| Test ID | Scenario |
|---|---|
| T-TC-01 | GST verification with valid/invalid GST numbers and API timeout |
| T-TC-02 | Dual-role toggle while active orders exist in both roles |
| T-TC-03 | IMS-to-Transport handoff when individual owners are unavailable |
| T-TC-04 | Same vehicle appears in hirer and service-provider contexts |
| T-TC-05 | Three payment paths with commission accuracy |
| T-TC-06 | Cancellation after dispatch with base-price calculation and account blocking |
| T-TC-07 | Fraud pattern detection with simulated suspicious behavior |
| T-TC-08 | Vehicle model matching by body length and loading capacity |
| T-TC-09 | Offline mode with order queuing and reconnect synchronization |
| T-TC-10 | Multi-vehicle order splitting across service providers |

## Derived Notes

- [[Transport Company Frontend for Current Project]]
- [[Transport Company Network Model]]
- [[driver_app_verification_harness_alignment_source]]
- [[scenario_context_engine_source]]
- [[02_Agentic_AI_Application]]
- [[API and Event Contract for Current Project]]
- [[Role and Permission Matrix for Current Project]]
- [[Finance and Invoice Event Layer for Logistics Platform]]
- [[Pricing Engine Backtest v1]]

## Related Notes

- [[Resource Management Agent]]
- [[Transportation Agent]]
- [[Payment Settlement Agent]]
- [[Scenario Management Framework]]
- [[Compliance Compatibility Plan for Current Logistics Environment]]
- [[Transport Fraud & Cybersecurity Framework]]

## Source Handling Note

This source should be used for later updates to transport-company frontend requirements, event contracts, role/permission design, pricing/payment rules, and verification harness tests. It should not directly override canonical transport-company architecture notes until the full app documentation sequence is complete.
