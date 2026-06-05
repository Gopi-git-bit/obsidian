# Zippy Logistics Standard Operating Procedures

> Source: `Zippy_Logistics_Standard_Operating_Procedures (1).docx`
> Document Version: 1.0 | Effective Date: June 2026 | Classification: Internal Use Only

## Document Control

| Field | Value |
| --- | --- |
| Document Title | Standard Operating Procedures |
| Organization | Zippy Logistics |
| Version | 1.0 |
| Effective Date | June 2026 |
| Classification | Internal Use Only |
| Approved By | Operations Director |
| Review Cycle | Quarterly |
| Next Review Date | September 2026 |

### Revision History

| Version | Date | Author | Description |
| --- | --- | --- | --- |
| 1.0 | June 2026 | Operations Team | Initial release covering 21 operational SOPs |

### Introduction

This Standard Operating Procedures document provides comprehensive guidelines for all employees and management at Zippy Logistics. It serves a dual purpose: as an operational reference for employees executing daily tasks, and as a management instruction guide for supervisors, managers, and directors overseeing operations and making decisions. Every procedure in this document has been designed to align with the platform's core engineering principle: Agents propose, Backend enforces, Audit records, Outbox announces. This principle ensures that operational flexibility coexists with system-level safety controls, preventing errors, fraud, and compliance violations while enabling efficient logistics operations.

The procedures cover the complete order lifecycle from initial booking through settlement and closure, as well as exception handling, compliance operations, partner management, and emergency response. Each SOP includes detailed steps, role assignments, exception handling protocols, and escalation paths. Employees should familiarize themselves with the SOPs relevant to their role and refer to this document whenever they encounter unfamiliar situations or need clarification on the correct procedure.

For management, this document serves as an instruction guide for overseeing operations, making escalation decisions, and ensuring that the team follows consistent and compliant procedures. The escalation protocols define when and how issues should be elevated, and the compliance notes highlight regulatory requirements that must never be compromised. Management should use this document during training, performance reviews, and incident investigations to ensure that operational standards are maintained.

## SOP-001: New Shipment Booking

### Purpose

This procedure standardizes the process of capturing, validating, and confirming new shipment booking requests from customers across all channels, including the web application, API integrations, and partner platforms. Every booking must pass through structured validation, pricing estimation, and policy preflight before it enters the order queue for vehicle assignment. The goal is to ensure that no invalid, non-compliant, or underpriced order enters the system, protecting both customer expectations and platform revenue integrity.

### Scope

This SOP applies to all customer-facing booking channels and covers the entire order creation lifecycle from initial request submission through the state transition from CREATED to CONFIRMED. It encompasses field validation, cargo restriction checks, route serviceability verification, pricing estimation, ToPay consent handling, and policy preflight execution. Out of scope are vehicle assignment and dispatch, which are covered in SOP-003.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| Customer | N/A | Initiates booking request with shipment details |
| OMS Agent | OMS | Validates order fields and runs policy preflight |
| Pricing Engine | N/A | Generates price estimate with surcharges and GST |
| IMS Agent | IMS | Pre-checks vehicle availability for the route |

### Pre-conditions

Customer account must be active with verified contact information. The requested route must fall within serviceable corridors (currently Tamil Nadu and Karnataka). The system must have at least one vehicle category available for the requested cargo type and weight. All mandatory fields must be provided: shipper name, shipper phone, origin city, destination city, cargo type, weight in kilograms, and payment mode.

### Procedure

1. Customer submits booking request via web or API with the following mandatory details: shipper name, shipper phone number, origin city and state, destination city and state, cargo type (general, fragile, perishable, hazardous, oversized), cargo description, weight in kilograms, and preferred payment mode (advance, full, or ToPay).
2. System validates all mandatory fields are present and correctly formatted. Weight must be greater than zero. Phone numbers must follow Indian format. Origin and destination must be in the serviceable route zone list.
3. OMS Agent validates cargo type against restricted categories. Hazardous cargo requires special permits and HazMat-certified vehicles. Perishable cargo requires closed body or refrigerated vehicles. Oversized cargo requires appropriate vehicle category (HCV or Tipper).
4. System determines route characteristics: interstate or intrastate based on origin and destination states. This classification affects GST application (IGST for interstate, CGST plus SGST for intrastate) and E-Way Bill requirements.
5. Pricing Engine generates a detailed estimate via the pricing estimate endpoint. The estimate includes base cost calculated by distance multiplied by the per-kilometre rate for the selected vehicle category, city tier multiplier, fuel index adjustment, route difficulty surcharge, applicable scenario surcharges (festival, remote, hill area, congestion), surge multiplier from the ML model, platform fee (four percent for distances over 200 kilometres, five percent for shorter routes), and GST breakdown at twelve percent for transport and eighteen percent for services.
6. For ToPay payment orders, the system checks the ToPay consent status. The consent must be explicitly accepted by the customer before the order can transition to CONFIRMED state. If consent is pending, rejected, or timed out, the order remains in CREATED state and the customer is prompted to provide consent.
7. Customer reviews the pricing estimate and confirms the booking. The customer may request a price adjustment, which will be evaluated against the route zone margin floor policy. If the offered price falls below the minimum gross margin percentage for the route zone, the adjustment will be rejected with a ROUTE_MARGIN_FLOOR_VIOLATION.
8. System creates the order record in the database with state set to CREATED. The order record includes all captured details, the pricing breakdown, and metadata including timestamps and channel information.
9. OMS Agent executes policy preflight using the order.transition action. The policy service runs its sequential validation chain: idempotency and trace verification, agent role authorization, state transition legality, route margin floor check, required document verification, and confidence threshold assessment.
10. Based on the payment mode and policy preflight result, the system transitions the order from CREATED to PAYMENT_PENDING (for advance payments) or directly to CONFIRMED (for full or ToPay with accepted consent). If policy preflight fails, the order remains in CREATED with the failure reason recorded in policy_decisions.
11. Customer receives a booking confirmation notification via their preferred channel, containing the order ID, estimated pickup window, pricing summary, and next steps. The COMMS Agent triggers this notification using the notification.trigger action, and the event is recorded in the outbox for audit purposes.

### Exceptions and Handling

If the address is not serviceable, the system notifies the customer with a clear message indicating which areas are currently covered and suggests the nearest serviceable origin or destination point. For restricted cargo that cannot be transported through the standard flow, the order is routed to the compliance team for manual evaluation. If the customer rejects the pricing estimate, the system offers counter pricing options that must remain above the route zone margin floor. If the requested timeline is not feasible due to vehicle availability or route constraints, the system suggests alternative pickup dates or times.

### Escalation Protocol

Failed bookings due to validation errors are routed to the Operations Manager for process improvement analysis. Compliance issues identified during policy preflight are escalated to the Supervisor Agent for review and potential hold placement. System failures during booking are handled by IT Support, with manual booking process as a fallback for critical orders. If the booking failure rate exceeds five percent in any hour, an automatic alert is sent to the Engineering team for investigation.

### Compliance Notes

All bookings must comply with GST regulations for transport services. E-Way Bill requirements must be flagged for interstate shipments exceeding fifty thousand INR in value. Customer personal data must be handled per DPDP Act requirements as detailed in SOP-019. All order state transitions must be recorded in the state_audit_logs table for traceability.

## SOP-002: Order Validation and Pricing

### Purpose

This procedure ensures that all orders meet business rules, compliance requirements, and pricing integrity standards before vehicle assignment begins. The validation process acts as the gatekeeper between order confirmation and the resource allocation phase, preventing underpriced shipments, compliance violations, and policy breaches from propagating through the system. Every order must pass through the policy kernel's sequential validation chain before it can transition to the RINGING state for vehicle matching.

### Scope

This SOP covers the validation phase between the CONFIRMED and RINGING states. It encompasses the policy preflight execution, route zone margin floor verification, compliance document requirement checking, confidence threshold validation, and business rule enforcement. This procedure applies to all orders regardless of cargo type, value, or route. Out of scope are vehicle matching and assignment, which are covered in SOP-003.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| OMS Agent | OMS | Initiates validation and manages order state transitions |
| Policy Service | N/A | Enforces the sequential validation chain |
| Pricing Engine | N/A | Calculates and verifies pricing integrity |
| SUP Agent | SUP | Reviews margin violations and low-confidence decisions |

### Pre-conditions

Order must be in CONFIRMED state with all mandatory fields populated. The policy service must be operational with current policy versions loaded in policy_registry, route_zone_policy, compliance_document_rules, and confidence_thresholds tables. The route zone for the order must be defined in the route_zone_policy table with margin floor and compliance settings.

### Procedure

1. Receive the validated order in CONFIRMED state. Verify that the order record contains all required fields including customer_id, origin, destination, cargo details, pricing, and payment information.
2. Policy Service executes the sequential validation chain. The chain runs six validations in strict order, and any failure stops the chain and creates a PolicyDecision record with the failure reason.
3. Validate idempotency and trace: the request must include a valid trace_id and idempotency_key. Duplicate requests with the same idempotency_key must not create duplicate decisions or actions.
4. Validate agent role: verify that the requesting agent code has the order.transition action in its AGENT_ALLOWED_ACTIONS whitelist. OMS, TMS, FIN, SUP, and ADMIN_OPS are authorized for state transitions.
5. Validate state transition: verify that the transition from CONFIRMED to RINGING is legal according to the ORDER_STATE_GRAPH. The target state RINGING must be in the allowed transitions from CONFIRMED.
6. Validate route margin floor: check the proposed gross margin percentage against the RouteZonePolicy.min_gross_margin_pct for the order's route zone. If the margin is below the floor, the validation fails with ROUTE_MARGIN_FLOOR_VIOLATION.
7. Apply crisis margin buffer: if the current vehicle supply percentage for the route zone is below the vehicle_supply_threshold_pct defined in the policy, the margin floor is relaxed by the crisis_margin_buffer_pct. This allows lower-margin bookings during supply shortages to maintain platform utilization.
8. If the margin floor is violated even after crisis buffer adjustment, reject the transition and create a PolicyDecision record with result equals reject and reason_code equals ROUTE_MARGIN_FLOOR_VIOLATION. Escalate to the SUP Agent for review.
9. Check compliance document rules: verify that all mandatory documents for the shipment_type and route_type combination are present or accounted for. For interstate shipments, an E-Way Bill is mandatory. For hazardous cargo, special permits are mandatory.
10. Validate confidence thresholds: check the decision confidence score against the ConfidenceThreshold table. Financial decisions require a minimum confidence of 0.85, compliance decisions require 0.95, operational decisions require 0.75, and communication decisions require 0.70.
11. If confidence is below the threshold for the decision category, create a PolicyDecision with requires_human_review set to true. The order is held until a human reviewer evaluates and approves the decision.
12. Validate business-specific rules: pharmaceutical material types require closed body vehicles before CONFIRMED transition. ToPay orders require topay_consent_status equal to accepted. These rules are enforced in the order service layer.
13. Generate a complete PolicyDecision record with all validation results, evidence references, confidence scores, and the applicable policy version. Record the trace_id and idempotency_key for audit purposes.
14. If all validations pass, transition the order from CONFIRMED to RINGING state. The RINGING state indicates that the order is ready for vehicle matching and assignment.
15. Emit an outbox event for order.validated with the full validation result, enabling downstream systems and monitoring dashboards to track validation outcomes.

### Exceptions and Handling

Margin floor violations trigger an immediate hold and escalation to the Supervisor Agent, who can approve an exception with documented justification or reject the order. Confidence threshold breaches route the order to a human reviewer queue, where a supervisor must evaluate the decision within four hours during business hours. Missing compliance documents block the transition until the documents are uploaded or a conditional override is granted by a supervisor with maker-checker approval.

### Escalation Protocol

Margin floor violations are escalated to the SUP Agent with the policy.check action. If the SUP Agent cannot resolve within two hours, the case is escalated to the Operations Manager. Compliance failures are escalated to the Compliance Officer, who has authority to grant conditional overrides for non-critical document gaps. Financial confidence threshold breaches are escalated to the Finance Manager, who must document the justification for any approval below the standard threshold.

### Compliance Notes

All policy decisions must be recorded in the policy_decisions table with full traceability. Route zone margin floors must not be bypassed without Supervisor approval and documented justification. Compliance document requirements must align with the latest GST and E-Way Bill regulations. The agent model revenue constraint must be enforced: Zippy revenue cannot exceed commission plus platform fee under Ind AS 115.

## SOP-003: Vehicle Assignment and Dispatch

### Purpose

This procedure governs the matching of confirmed orders with available vehicles and drivers, ensuring optimal capacity utilization, timely dispatch, and a smooth handoff from the order management phase to the transportation execution phase. The vehicle assignment process must balance multiple objectives: minimizing customer wait time, maximizing vehicle utilization, respecting transport company preferences, and maintaining compliance with cargo-specific vehicle requirements.

### Scope

This SOP covers the vehicle matching, driver notification, and order assignment process from the RINGING state through the ASSIGNED state. It includes the matching algorithm execution, transport company acceptance, vehicle reservation with TTL, driver acknowledgement, and fallback procedures when primary matching fails. Out of scope are trip execution and milestone tracking, covered in SOP-006.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| IMS Agent | IMS | Runs matching algorithm and ranks candidate vehicles |
| OMS Agent | OMS | Manages order state transitions during assignment |
| Transport Company | N/A | Reviews and accepts or rejects match proposals |
| Driver | N/A | Acknowledges trip assignment and confirms availability |

### Pre-conditions

Order must be in RINGING state with validated pricing and passed policy preflight. At least one vehicle must be available in the system for the required category and body type. The transport company must be an active partner with valid insurance and compliance status. Driver must have valid license and be within the service area.

### Procedure

1. Order enters RINGING state after successful validation and policy preflight. The system flags the order as ready for vehicle matching in the dispatch queue.
2. IMS Agent executes the vehicle matching algorithm via the matching endpoint, considering the following criteria: vehicle category must match or exceed the order's vehicle_category_preference, body type must satisfy cargo requirements (closed body for pharma and electronics, refrigerated for perishables), payload capacity must exceed the order's weight in kilograms, vehicle location proximity to the pickup point, and vehicle current availability status.
3. System ranks matched vehicles by a composite score comprising match_score (algorithmic fit), utilization_percent (how efficiently the vehicle is being used), and efficiency_score (historical performance of the vehicle and driver on similar routes). The ranking is presented to the transport company for selection.
4. Transport company reviews the match proposal through the transport company web console. The proposal includes the order details, estimated distance and duration, offered price breakdown, and vehicle-driver pair suggested by the algorithm.
5. Transport company accepts the match via the accept endpoint, or rejects it with a reason. If accepted, the system proceeds to vehicle reservation. If rejected, the next ranked vehicle is proposed automatically.
6. Upon match acceptance, the system creates a vehicle reservation in the vehicle_reservations table with a five-minute time-to-live. The reservation prevents double-booking by setting is_active to True and establishing an expires_at timestamp. A partial unique index on vehicle_id where is_active equals True ensures database-level protection against concurrent reservations.
7. Driver receives the assignment notification through the driver web application or SMS, containing the pickup location, cargo details, pickup time window, and route overview.
8. Driver acknowledges the trip via the acknowledge endpoint within the reservation TTL period. If the driver fails to acknowledge before the reservation expires, the reservation is automatically released and the next ranked vehicle is engaged.
9. OMS Agent transitions the order from RINGING to ASSIGNED state upon successful driver acknowledgement. This transition is recorded in the state_audit_logs with the actor_role, trace_id, and idempotency_key.
10. System creates a trip record in the trips table linking the order_id, vehicle_id, driver_id, and transport_company_id. The trip becomes the central tracking entity for all subsequent milestones and events.
11. If no vehicles from the own fleet are available, the system automatically extends the search to partner transporters following the partner management procedures in SOP-016. Partner vehicles are included based on their tier priority: Gold partners first, then Silver, then Bronze.
12. If the time window for pickup is at risk due to matching delays, the system immediately notifies the customer with a revised estimated pickup time and offers the option to cancel without penalty if the revised timeline is unacceptable.

### Exceptions and Handling

If no vehicles are available in the system for the required category, the dispatch team escalates to the partner network per SOP-016. If a driver is unresponsive after the five-minute reservation TTL expires, the system automatically releases the reservation and engages the next ranked vehicle from the matching results. When multiple orders compete for the same vehicle, the system applies first-come-first-served logic with the reservation TTL as the tiebreaker. If a vehicle breaks down before pickup, the reassignment process follows SOP-010 for vehicle breakdown response.

### Escalation Protocol

If no suitable match is found within thirty minutes of the order entering RINGING state, the case is escalated to the Dispatch Manager who may authorize expanded search radius, partner fleet activation, or customer communication with alternative options. If all drivers in the area are rejecting assignments, the Operations Lead investigates potential systemic issues such as rate disputes, route problems, or driver app issues. Vehicle shortage in a specific zone triggers a Fleet Manager review of capacity planning and potential rebalancing.

### Compliance Notes

Vehicle reservations must use the TTL mechanism to prevent indefinite locks on vehicle capacity. All state transitions during assignment must be recorded with trace_id and idempotency_key for audit purposes. The matching algorithm must respect cargo-specific vehicle requirements as defined in the compliance_document_rules table.

## SOP-004: Secure Vehicle Assignment (High-Value Cargo)

### Purpose

This procedure ensures that high-value, sensitive, or regulated cargo is assigned exclusively to vehicles meeting enhanced security and compliance requirements beyond the standard matching criteria. Secure assignments involve additional verification steps, enhanced monitoring configurations, and specific documentation requirements that protect both the cargo and the platform from loss, theft, or regulatory violations.

### Scope

This SOP applies to all orders involving electronics with declared value above fifty thousand INR, pharmaceuticals requiring temperature control, fragile goods with high replacement cost, confidential documents, and hazardous materials requiring specialized vehicles and certified drivers. Standard cargo assignments follow SOP-003 instead.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| IMS Agent | IMS | Filters vehicle pool for security-qualified vehicles only |
| TMS Agent | TMS | Configures enhanced tracking and geo-fence alerts |
| Dispatch Team | N/A | Assigns secure vehicles and briefs drivers |
| Compliance Officer | N/A | Verifies insurance, permits, and driver certifications |

### Pre-conditions

Order must be classified as requiring secure transportation based on cargo type or declared value. At least one security-qualified vehicle must be available in the fleet or partner network. Driver must hold appropriate license endorsements for the cargo type. Vehicle insurance must cover the declared cargo value.

### Procedure

1. Identify the order as requiring secure transportation based on the cargo_type field and the declared or estimated cargo value. Orders with electronics valued over fifty thousand INR, all pharmaceuticals, all hazardous materials, and goods specifically marked as high-value by the customer trigger this SOP.
2. Apply the security requirements matrix: for Electronics, require closed body vehicle plus mandatory GPS tracking plus active insurance covering the cargo value. For Pharmaceuticals, require refrigerated or temperature-controlled vehicle plus mandatory GPS tracking plus cold chain compliance certification. For Documents, require any secure body type with recommended GPS tracking. For Fragile goods, require closed body with mandatory GPS tracking and padding certification. For Hazardous materials, require HazMat-certified vehicle plus special permits plus mandatory GPS tracking plus driver HazMat endorsement.
3. IMS Agent filters the vehicle pool to only those meeting the security criteria for the specific cargo type. This overrides the standard matching algorithm's broader selection criteria.
4. Verify vehicle insurance is active and covers the declared cargo value. The insurance policy document must be verified through the compliance_document_rules validation endpoint.
5. Verify driver holds the appropriate license endorsements: HazMat endorsement for hazardous cargo, refrigerated vehicle certification for pharma, and standard commercial license for other secure cargo types.
6. Assign the security-qualified vehicle with all documentation requirements loaded into the trip record. The vehicle_reservations table entry includes a security_flag field indicating enhanced verification requirements.
7. Enable enhanced GPS tracking with a two-minute update interval instead of the standard fifteen-minute interval. Configure this through the TMS Agent's route.plan action with the tracking_frequency parameter.
8. Configure geo-fence alerts for the planned route. Any deviation beyond ten kilometres from the planned route triggers an automatic alert to the TMS Agent and Dispatch Team. The geo-fence is set via the route optimization endpoint with a deviation_threshold parameter.
9. Brief the assigned driver on security protocols specific to the cargo type, emergency contact numbers for the security team, and incident reporting procedures. Document the briefing in trip_documents with document_type equal to security_briefing.
10. Record the secure assignment in trip_documents with verification_status tracking each security requirement as verified, pending, or waived with supervisor approval.

### Exceptions and Handling

If no secure vehicle is available in the zone, escalate to the Operations Director with a proposed alternative and a risk assessment document. The risk assessment must quantify the potential loss exposure and recommend whether to proceed with a less-secure option or delay the shipment. If vehicle insurance is lapsed or insufficient for the cargo value, the assignment is blocked until the insurance is renewed or supplemented. If the assigned driver lacks the required certification, a certified backup driver must be assigned from the available pool.

### Escalation Protocol

No secure vehicle available within the zone triggers escalation to the Operations Director within two hours. Insurance coverage disputes are escalated to Legal and Finance for resolution. HazMat compliance gaps trigger immediate escalation to the Compliance Officer and a mandatory hold on the shipment until resolved.

### Compliance Notes

Secure vehicle assignments must comply with the insurance boundary policy: Zippy transmits evidence and verification only, and does not act as insurer, broker, or claim advisor. All enhanced tracking data must be retained for a minimum of ninety days after delivery for potential investigation purposes.

## SOP-005: Shipment Document Verification

### Purpose

This procedure ensures that all required shipping documents are complete, consistent, and compliant before dispatching the shipment. Document verification is a critical compliance gate that prevents non-compliant shipments from entering the transportation network, reducing the risk of regulatory penalties, shipment seizures at check-posts, and customer disputes. Every shipment must pass document verification before the loading phase begins.

### Scope

This SOP applies to document validation for all shipments, with particular emphasis on interstate shipments requiring E-Way Bills and special permits for regulated cargo. It covers the identification of required documents, completeness and consistency checks, E-Way Bill validation, and GST rate verification. This procedure applies to all orders regardless of cargo type or route.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| OMS Agent | OMS | Initiates document verification and validates completeness |
| ADMIN_OPS Agent | ADMIN_OPS | Runs compliance checks on submitted documents |
| Dispatch Team | N/A | Collects and submits physical and digital documents |
| Transport Company | N/A | Provides vehicle and driver documentation |

### Pre-conditions

Order must be in ASSIGNED state with a vehicle and driver confirmed. The compliance_document_rules table must contain the applicable rules for the shipment_type and route_type combination. The E-Way Bill generation system must be accessible for interstate shipments.

### Procedure

1. Identify the complete set of required documents based on the shipment_type and route_type from the compliance_document_rules table. The rules specify which documents are mandatory versus optional for each combination.
2. Compile the standard document checklist: Invoice showing cargo description, value, and GSTIN of consignor and consignee. E-Way Bill required for all interstate shipments exceeding fifty thousand INR in value. Lorry Receipt or Goods Receipt documenting the handover of cargo to the transporter. POD prerequisites including consignee signature format and delivery confirmation requirements. Special permits for hazardous materials, oversized cargo, or agricultural products as applicable.
3. Validate document completeness: verify that all mandatory documents are present, all required fields within each document are populated, signatures are present where required, and document dates are current and valid.
4. Validate document consistency across all submitted documents: shipper name and address match across invoice, E-Way Bill, and order record. Origin and destination addresses match the order details and the E-Way Bill. Weight and value figures match across the invoice, E-Way Bill, and order declared amounts. Vehicle registration number matches the assigned vehicle in the trip record.
5. Verify E-Way Bill validity: the bill must not be expired based on its validity period which is one day per two hundred kilometres for over-dimensional cargo and one day per one hundred kilometres for normal cargo. The GSTIN numbers must be valid and active. The E-Way Bill must specify the correct transport mode as road and the correct vehicle number.
6. Cross-reference GST rate application: transport of goods by road attracts twelve percent GST, while platform services attract eighteen percent GST. Verify that the GST breakdown on the invoice matches the rates calculated by the Pricing Engine.
7. Record the document verification result in the compliance_document_rules table with the validation_endpoint status updated to verified, failed, or pending for each document.
8. Clear the shipment for dispatch if all documents pass verification. The order can proceed to the loading phase with full compliance clearance.
9. If documents fail validation, flag the specific deficiencies in the order notes and notify the responsible party. For shipper document issues, notify the customer. For transport document issues, notify the transport company. Set a resolution deadline based on the pickup time window.
10. Do not dispatch non-compliant shipments without written supervisor approval. Any override of the document verification gate must be recorded in the supervisor_decisions table with the justification, the approving supervisor, and the conditional requirements for post-dispatch document submission.

### Exceptions and Handling

If the E-Way Bill is pending generation, allow a two-hour window for the shipper or transporter to generate it through the NIC portal. If the E-Way Bill generation fails due to NIC system downtime, a conditional override may be granted with maker-checker approval, and the E-Way Bill must be generated within twenty-four hours of dispatch. Minor discrepancies in weight within a five percent tolerance band are accepted with a note in the order record. If a non-mandatory document is missing, document the gap and proceed with a caution flag that triggers enhanced milestone monitoring.

### Escalation Protocol

E-Way Bill generation failure is escalated to the Compliance Team and NIC support for resolution. Document mismatches that cannot be resolved within the pickup window are escalated to the OMS Agent for investigation and potential order hold. Persistent non-compliance from a specific shipper or transporter triggers an Operations Director review of the business relationship.

### Compliance Notes

All document verification results must be recorded in the compliance_document_rules and policy_decisions tables for audit purposes. E-Way Bill requirements must comply with the latest Central Goods and Services Tax Rules. Document retention must follow GST record-keeping requirements of six years from the date of filing.

## SOP-006: Trip Execution and Milestone Tracking

### Purpose

This procedure governs the real-time monitoring and recording of shipment progress through defined milestones from pickup to delivery. Milestone tracking provides the operational visibility that customers, transport companies, and the platform need to manage expectations, detect exceptions early, and maintain an auditable record of every trip. The milestone data feeds directly into customer communications, exception detection algorithms, and settlement verification processes.

### Scope

This SOP covers all milestones from the EN_ROUTE_TO_PICKUP state through the DELIVERED_PENDING_SETTLEMENT state. It includes driver check-ins, location updates, ETA revisions, telemetry-based incident detection, loading verification, and delivery confirmation. Out of scope are POD collection and OTP verification, covered in SOP-007, and settlement release, covered in SOP-008.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| TMS Agent | TMS | Tracks milestones, monitors telemetry, and detects incidents |
| Driver | N/A | Reports milestones and uploads trip evidence |
| COMMS Agent | COMMS | Sends milestone notifications to customers |
| OMS Agent | OMS | Records state transitions in audit log |

### Pre-conditions

Order must be in ASSIGNED state with a confirmed vehicle, driver, and trip record. The driver must have acknowledged the trip assignment. The vehicle's GPS tracking must be active and transmitting location data.

### Procedure

1. Driver confirms trip start and proceeds to the pickup location. The driver marks departure through the driver web application, triggering the system to transition the order from ASSIGNED to EN_ROUTE_TO_PICKUP.
2. System captures the driver's departure timestamp and starting GPS coordinates. The TMS Agent begins real-time tracking with location updates at the configured interval (fifteen minutes for standard shipments, two minutes for secure cargo).
3. Driver arrives at the pickup location and marks arrival. The system transitions the order to AT_PICKUP_WAITING and records the arrival time and GPS coordinates. The COMMS Agent notifies the customer that the driver has arrived.
4. Loading begins with cargo verification against the order details and document exchange between shipper and driver. The system transitions the order to LOADING state. The driver verifies the cargo type, weight, and packaging match the order record.
5. Driver uploads a loading photo through the loading photo endpoint as evidence of cargo condition at pickup. The photo must include the cargo in the vehicle, clearly showing the loading state and any existing damage or packaging conditions.
6. System scans and verifies shipment document data including document type, document URL, and scan EXIF metadata. The EXIF data must contain a valid timestamp and GPS coordinates confirming the document was scanned at the pickup location.
7. Driver confirms departure from the pickup location after loading is complete and all documents are verified. The system transitions the order from LOADING to DEPARTED_FOR_DELIVERY. The TMS Agent calculates the estimated delivery time based on route conditions.
8. TMS Agent monitors telemetry data throughout the trip for anomaly detection: speed anomaly when vehicle speed exceeds ninety-five kilometres per hour, prolonged stop when the vehicle is idle for more than forty-five minutes, and route deviation when the vehicle strays more than ten kilometres from the planned route.
9. System updates milestones through the milestones endpoint with each recorded event. Each milestone update includes a unique idempotency_key to prevent duplicate records, the milestone_type, current status, and a payload with relevant metadata such as GPS coordinates, timestamp, and any anomaly flags.
10. ETA is dynamically recalculated at each milestone based on real-time traffic conditions, weather alerts, road closures, and the driver's average speed on the current route. If the revised ETA deviates by more than twenty percent from the original estimate, the COMMS Agent sends a proactive update to the customer.
11. Driver arrives at the delivery location and marks arrival. The system transitions the order to AT_DELIVERY_WAITING. The COMMS Agent sends a delivery approaching notification to the consignee with the driver's contact details (masked per DPDP requirements) and the OTP for delivery confirmation.
12. At delivery, the process continues to POD collection and OTP verification per SOP-007. The trip milestones are complete when the order transitions to DELIVERED_PENDING_SETTLEMENT.

### Exceptions and Handling

Speed anomaly detected by the TMS Agent triggers an incident log entry and a notification to the driver to reduce speed. If the anomaly persists, the Dispatch Team contacts the driver directly. Prolonged stop detected by telemetry triggers a check with the driver via phone within fifteen minutes. If the driver is unreachable after thirty minutes, the case is escalated to the Dispatch Manager. Route deviation triggers an automatic alert to the driver and a log entry in the incident tracking system. If the deviation is not corrected within thirty minutes, the Dispatch Team investigates. If loading photo quality is insufficient, the driver is requested to re-upload before departure is confirmed.

### Escalation Protocol

Driver unreachable for more than thirty minutes triggers escalation to the Dispatch Manager and the Transport Company for alternative contact methods. Telemetry system failure triggers a manual check-in protocol where the driver must call in milestones every hour. Multi-milestone delay affecting the delivery SLA triggers a Supervisor review of the order status and potential customer compensation.

### Compliance Notes

All milestone updates must include idempotency_key and trace_id for audit trail. Telemetry data must be retained for a minimum of ninety days after trip completion. Customer notifications must not include exact vehicle GPS coordinates unless the customer is the consignee and delivery is imminent.

## SOP-007: POD Collection and OTP Verification

### Purpose

This procedure ensures proper proof of delivery collection and OTP-based consignee verification, which are mandatory prerequisites for authorizing shipment completion and triggering the settlement process. The POD and OTP serve as the dual-factor evidence that the shipment was delivered to the correct recipient at the correct location, protecting the platform from fraudulent delivery claims and ensuring that transport companies are paid only for confirmed deliveries.

### Scope

This SOP covers the POD upload process, OTP generation and verification, and the state transition from AT_DELIVERY_WAITING to DELIVERED_PENDING_SETTLEMENT. It applies to all shipments regardless of cargo type or value. Out of scope are settlement release, covered in SOP-008, and POD disputes, covered in SOP-011.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| Driver | N/A | Collects POD from consignee and uploads evidence |
| Authorized Verifier | N/A | Verifies POD and OTP as separate controls |
| FIN Agent | FIN | Prepares settlement after verification is complete |
| COMMS Agent | COMMS | Sends delivery confirmation to customer |

### Pre-conditions

Order must be in AT_DELIVERY_WAITING state. Driver must be at the delivery location with the cargo. Consignee contact information must be on record for OTP delivery.

### Procedure

1. Driver arrives at the delivery location and the order is in AT_DELIVERY_WAITING state. The driver visually confirms the delivery address matches the order record.
2. Driver collects Proof of Delivery from the consignee through one of the accepted methods: physical signature on the delivery receipt, digital signature captured through the driver application, or photo evidence of the cargo at the delivery location with the consignee present.
3. Driver uploads the POD through the POD upload endpoint, providing the POD URL where the evidence file is stored, the consignee OTP that will be used for verification, and the POD EXIF metadata containing the timestamp and GPS coordinates of the upload.
4. System captures the GPS coordinates and timestamp from the POD upload metadata. These are compared against the expected delivery location and the current time to detect potential fraud indicators such as location mismatch or timestamp manipulation.
5. Customer or consignee receives a one-time password on their registered phone number. The OTP is generated by the system and delivered via the configured communication channel, typically SMS or WhatsApp.
6. Consignee provides the OTP to the driver for verification. The driver enters the OTP into the system through the driver application.
7. An authorized verifier role confirms the OTP through the OTP verification endpoint. This must be a separate verification step from the POD verification to maintain dual-factor control.
8. An authorized verifier role confirms the POD through the POD verification endpoint. The verifier checks that the POD evidence meets the quality checklist: signature is present and legible, photo evidence is clear and well-lit, timestamp is within a reasonable window of the delivery time, and GPS location matches the delivery address within an acceptable radius.
9. System validates the complete POD evidence checklist: signature present, photo clear and identifiable, timestamp valid and within expected delivery window, GPS location matches the delivery address or is within the acceptable geofence radius.
10. System transitions the order from AT_DELIVERY_WAITING to DELIVERED_PENDING_SETTLEMENT upon successful dual verification. This transition is recorded in the state_audit_logs with both the POD and OTP verification references.
11. FIN Agent is notified that the order has reached DELIVERED_PENDING_SETTLEMENT and settlement can be prepared according to SOP-008.
12. COMMS Agent sends a delivery confirmation to the customer with a summary of the POD evidence, the delivery timestamp, and information about the settlement timeline.

### Exceptions and Handling

If the OTP is not received by the consignee, the system resends the OTP with a maximum of three attempts. After three failed attempts, the case is escalated to customer support for manual verification. If the consignee refuses to sign the POD, the driver documents the refusal with a photo of the cargo at the delivery location and GPS evidence. If the POD photo quality is poor, the driver is requested to re-upload before the state transition. If OTP verification fails after three consecutive incorrect entries, the system locks the OTP and escalates to customer support for manual identity verification.

### Escalation Protocol

Consignee unavailable for OTP verification triggers escalation to Customer Support, who attempts to contact the consignee through alternative channels. Persistent OTP failure after three resend attempts escalates to the Supervisor for manual override, which requires documented evidence of delivery such as GPS trail, loading photo, and witness statements. POD disputes are handled through the dedicated SOP-011 for POD Dispute Resolution.

### Compliance Notes

Both POD and OTP verification must be completed before settlement can be released. This is a hard requirement enforced at the database level and cannot be bypassed without dual-supervisor approval. All verification records must be retained for a minimum of six years for GST audit compliance.

## SOP-008: Settlement Release

### Purpose

This is the most financially critical standard operating procedure in the Zippy Logistics platform. Settlement release authorizes payment to transport companies and drivers, creates financial records including journal entries and GST invoices, and transitions the order to its terminal COMPLETED state. Because this procedure involves the movement of money, it has the strictest verification requirements and the most comprehensive audit trail. No settlement may be released without all prerequisite verifications being confirmed and all holds being cleared.

### Scope

This SOP covers the settlement release process from the DELIVERED_PENDING_SETTLEMENT state through the COMPLETED state. It includes all verification checks, hold clearance, financial record creation, outbox event emission, and state transition. This procedure applies to every settlement without exception.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| FIN Agent | FIN | Initiates settlement and creates financial records |
| Policy Service | N/A | Runs final policy preflight before release |
| SUP Agent | SUP | Clears any active holds blocking settlement |
| Finance Admin | N/A | Authorizes settlement release as the human approver |

### Pre-conditions

Order must be in DELIVERED_PENDING_SETTLEMENT state. POD must be verified by an authorized role. OTP must be verified by an authorized role. No active fraud_holds may exist for the order. No active settlement_holds may exist for the order. The actor must have finance_admin or super_admin role.

### Procedure

1. Verify the order exists and is currently in DELIVERED_PENDING_SETTLEMENT state. Query the orders table to confirm the current_state field matches the expected state.
2. Verify the trip record exists and is correctly linked to the order through the trip_id field in the trips table. Confirm that the trip status reflects completed delivery.
3. Confirm that the Proof of Delivery has been verified by an authorized role. Check the trip_documents table for a POD record with verification_status equal to verified.
4. Confirm that the OTP has been verified by an authorized role. Check the trips table for the otp_verified field set to true.
5. Check for active fraud holds on the order. Query the fraud_holds table where order_id matches and is_active equals True. If any active fraud hold exists, the settlement cannot proceed.
6. Check for active settlement holds on the settlement. Query the settlement_holds table where order_id matches and is_active equals True. If any active settlement hold exists, the settlement cannot proceed.
7. Verify that the actor initiating the settlement has the finance_admin or super_admin role. This is enforced by the RBAC system at the API layer and verified again in the policy preflight.
8. Execute policy preflight with the FIN agent code and the settlement.release action. The policy service runs the full sequential validation chain: idempotency and trace verification, agent role authorization for settlement.release, state transition legality, route margin floor re-verification, compliance document completeness, and confidence threshold assessment for the financial decision category at 0.85 minimum.
9. If any policy preflight check fails, emit an outbox event with event type settlement.release_blocked including the reason details, the policy decision record, and the blocking check identifier. Stop the settlement process and notify the Finance Admin of the blockage.
10. If all checks pass, create a SettlementRecord in the settlement_records table. The record must include a unique idempotency_key, the order_id, trip_id, settlement amount, currency set to INR, and the current timestamp. Duplicate idempotency_key values must not create duplicate settlement records.
11. Create a JournalEntry in the journal_entries table with the debit_ledger and credit_ledger accounts, the settlement amount, currency, and a unique idempotency_key linked to the settlement. The journal entry must reflect the agent model revenue constraint where Zippy recognizes only commission plus platform fee as revenue, not gross freight.
12. Create a GSTInvoiceRecord in the gst_invoice_records table with a unique invoice_number, the taxable_amount, gst_amount split between twelve percent transport GST and eighteen percent services GST, total_amount, and the current status. The invoice_number must be unique across the entire table, enforced by a unique constraint.
13. Emit three outbox events: settlement.released confirming the settlement amount and payee details, finance.journal_created referencing the journal entry, and finance.gst_invoice_created referencing the GST invoice. Each event includes its own idempotency_key and is processed through the outbox service.
14. Transition the order from DELIVERED_PENDING_SETTLEMENT to COMPLETED state. The COMPLETED state is a terminal state with no further transitions possible. This transition is recorded in the state_audit_logs with full trace information.
15. Verify that no duplicate financial records were created. If the idempotency_key was already processed, the system returns the existing records without creating new ones. This prevents double-settlement in case of network retries or duplicate API calls.

### Exceptions and Handling

An active fraud hold blocks settlement unconditionally. The FIN Agent cannot override a fraud hold; it must be released by the SUP Agent through the fraud investigation process described in SOP-015. An active settlement hold also blocks settlement and must be cleared by a Supervisor through the supervisor console. If policy preflight fails, the reason code identifies the specific check that failed, and the Finance Admin can address the root cause or escalate to the appropriate team. Missing POD or OTP verification must be resolved by routing the order back to the verification team before settlement can be attempted again.

### Escalation Protocol

Repeated settlement blocks on the same order escalate to the Finance Director and Compliance Officer for joint review. An active fraud hold triggers mandatory investigation by the SUP Agent as described in SOP-015. Settlement amount discrepancies greater than five percent from the expected value trigger a Finance Manager review before release. System errors during the settlement process trigger IT Support involvement with a full transaction audit to ensure no partial records were created.

### Compliance Notes

Settlement release is a non-negotiable control point. The six prerequisite checks (POD verified, OTP verified, no fraud hold, no settlement hold, authorized role, policy preflight pass) must all be satisfied without exception. The agent model revenue constraint must be enforced through the accounting controls: Zippy revenue cannot exceed commission plus platform fee. Segregation of duties must be maintained: the person generating the GST invoice cannot be the same person approving the settlement release.

## SOP-009: Delayed Shipment Handling

### Purpose

This procedure provides a structured approach to detecting, assessing, communicating, and resolving shipment delays to minimize customer impact and maintain SLA compliance. Delays are inevitable in logistics due to traffic, weather, mechanical issues, and operational disruptions, but the response to delays must be systematic, transparent, and well-documented to maintain customer trust and protect the platform from SLA penalties.

### Scope

This SOP covers all shipments experiencing delays exceeding acceptable thresholds at any point from pickup through delivery. It encompasses delay detection, classification, impact assessment, route optimization, customer communication, and escalation procedures. Both single-order delays and systemic delays affecting multiple orders are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| TMS Agent | TMS | Detects delays through milestone tracking and telemetry |
| COMMS Agent | COMMS | Communicates delay information to customers |
| OMS Agent | OMS | Re-plans orders and adjusts timelines |
| SUP Agent | SUP | Handles escalated delay cases |

### Pre-conditions

Delay thresholds must be configured in the system for each service tier. Standard, Premium, and VIP orders have different acceptable delay windows. The route optimization service must be available for traffic-related delay mitigation.

### Procedure

1. TMS Agent detects a delay through milestone tracking when actual progress falls behind the planned timeline by more than the configured threshold for the order's service tier. The detection can be triggered by a missed milestone checkpoint, an ETA revision exceeding the threshold, or a manual report from the driver or customer.
2. Classify the delay into one of five categories: Traffic delay caused by congestion or road closures, which may be resolved through route optimization. Weather delay caused by rain, fog, or other conditions making travel unsafe, which typically requires waiting and resuming. Mechanical delay caused by vehicle breakdown, which is handled through SOP-010. Documentation delay caused by missing or incorrect paperwork, which requires document correction or re-generation. Operational delay caused by resource shortages or scheduling conflicts, which may require reassignment.
3. Assess the delay impact by estimating the additional time required, determining whether the customer SLA will be breached, identifying any downstream effects on other orders or return trips, and calculating the potential financial impact including SLA penalties and customer compensation.
4. For traffic delays, TMS Agent attempts route optimization through the optimize route endpoint. The OR-Tools solver considers alternative routes, current traffic conditions, and toll costs to find the fastest alternative path.
5. For mechanical delays, initiate the vehicle breakdown response procedure in SOP-010. The TMS Agent transitions the order to the INCIDENT state and coordinates the repair or vehicle swap process.
6. COMMS Agent notifies the customer with an accurate revised ETA and a clear, honest explanation of the delay reason. The notification must be proactive, sent before the customer inquires about the delay. For delays under two hours, an SMS notification is sufficient. For delays over two hours, a phone call or WhatsApp message is required.
7. If the delay exceeds four hours for standard orders, escalate to the Team Lead who reviews the situation and authorizes additional resources or customer compensation if needed.
8. If the delay exceeds eight hours for standard orders, escalate to the Operations Manager who may authorize order cancellation with full refund, partial delivery, or alternative transportation arrangements.
9. If the delay exceeds four hours for premium orders, escalate directly to the Manager level, as premium customers have higher SLA expectations and lower tolerance for delays.
10. If the delay exceeds two hours for VIP orders, escalate to the VP of Operations for personal attention and resolution. VIP orders represent the highest-value customers and require the most responsive delay handling.
11. If any legal threat arises from the delay, escalate immediately to the Legal Department regardless of the delay duration. Legal threats include customer claims of breach of contract, threats of regulatory complaints, or indications of potential litigation.
12. Document all delay events, actions taken, and customer communications in the order notes and outbox events. Every communication must have a trace_id for audit purposes, and every decision must have a documented rationale.
13. Post-resolution: conduct a root cause analysis to determine whether the delay was preventable. Update route buffers if the delay was caused by consistently underestimated transit times. Update SLA metrics and customer satisfaction scores to reflect the delay impact.

### Exceptions and Handling

Force majeure events such as natural disasters, strikes, or government-mandated road closures trigger the force majeure clause in the customer agreement, which suspends SLA penalties for the duration of the event. Multi-order cascade delays where a single disruption affects multiple shipments are prioritized by customer tier and order value, with VIP and high-value orders receiving priority for re-routing and resource allocation. Driver-caused delays due to negligence or unauthorized stops are assessed for penalties per the partnership agreement with the transport company.

### Escalation Protocol

Standard delay exceeding four hours escalates to the Team Lead. Standard delay exceeding eight hours escalates to the Manager. Premium delay exceeding four hours escalates to the Manager. VIP delay exceeding two hours escalates to the VP Operations. Any legal threat from a delay escalates to the Legal Department immediately, regardless of delay duration or order tier.

### Compliance Notes

All delay communications must be truthful and must not promise outcomes that cannot be verified. Customer compensation for SLA breaches must be calculated per the published SLA terms and approved by the Finance Admin before commitment. Delay patterns indicating systemic issues such as recurring congestion on specific routes or recurring driver availability problems must be reported to the Operations Director for strategic resolution.

## SOP-010: Vehicle Breakdown Response

### Purpose

This procedure provides a structured response when a vehicle breaks down during an active trip, ensuring driver safety, cargo protection, customer communication, and timely recovery through either repair or vehicle replacement. Vehicle breakdowns are high-stress events that require rapid decision-making and clear coordination between multiple teams to minimize the impact on the shipment and maintain customer confidence.

### Scope

This SOP covers all vehicle breakdowns during active trips, from initial detection through either successful cargo delivery via replacement vehicle or order cancellation. It includes safety assessment, repair evaluation, cargo transfer coordination, and post-breakdown documentation. Both mechanical failures and accident-related immobilizations are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| TMS Agent | TMS | Detects breakdown through telemetry and manages incident state |
| Driver | N/A | Reports breakdown and cooperates with recovery efforts |
| Dispatch Team | N/A | Coordinates repair or vehicle replacement |
| COMMS Agent | COMMS | Notifies customer of breakdown and recovery plan |
| IMS Agent | IMS | Finds replacement vehicle from fleet or partner network |

### Pre-conditions

Trip must be active with the order in a transportation state between DEPARTED_FOR_DELIVERY and AT_DELIVERY_WAITING. Vehicle GPS must be active to provide location data for recovery coordination. The breakdown must be confirmed either by driver report or telemetry analysis.

### Procedure

1. Receive the breakdown report through either a driver-initiated call or message to the dispatch team, or a TMS Agent telemetry detection where the vehicle has been stationary for more than forty-five minutes in a location not consistent with a scheduled stop such as a pickup or delivery point.
2. Assess the immediate situation starting with driver safety: is the driver injured or in danger? Is the vehicle in a safe location away from traffic? Is the cargo secure and protected from weather or theft? If the driver is in an unsafe location on a highway shoulder or in a high-crime area, advise them to move to a safer position if possible.
3. If the driver is injured, call emergency services at 112 immediately before taking any other action. Driver safety is the absolute first priority. Document the injury report and notify HR and the transport company.
4. TMS Agent logs the incident event by transitioning the order to the INCIDENT state. This state allows the order to be tracked separately from normal flow orders and triggers enhanced monitoring and reporting.
5. Dispatch Team evaluates repair options by contacting the driver to understand the nature of the breakdown: engine failure, tire blowout, electrical failure, or other mechanical issues. Estimate the repair time based on the breakdown type and the distance to the nearest authorized service center. Check if the vehicle has roadside assistance coverage through the transport company's insurance.
6. Make the repair versus transfer decision: if the estimated repair time is less than two hours and the repair can be performed safely at the roadside, proceed with the quick fix option. If the repair will take more than two hours or raises safety concerns about continuing the trip with a repaired vehicle, proceed with the cargo transfer option.
7. If cargo transfer is required, IMS Agent searches for a replacement vehicle from the own fleet first, then the partner network. The replacement vehicle must meet all the original order requirements including vehicle category, body type, and any security specifications for high-value cargo.
8. Coordinate the cargo transfer: verify the new vehicle meets all requirements for the cargo type, confirm the replacement driver has the necessary certifications, arrange for the physical transfer of cargo from the broken-down vehicle to the replacement, and update the trip record with the new vehicle and driver information.
9. COMMS Agent notifies the customer of the breakdown, the expected delay, and the recovery plan. The communication must be honest about the situation while reassuring the customer that active measures are being taken. Include a revised ETA if available.
10. Update the order milestones with the breakdown event, the transfer details if applicable, and the revised ETA for delivery. All updates must include idempotency_key and trace_id for the audit trail.
11. If no replacement vehicle is available within an acceptable window, typically four hours for standard orders and two hours for premium orders, escalate to the Operations Manager who may authorize alternative arrangements such as partial delivery, temporary storage, or order cancellation with full refund.
12. Post-resolution: document the complete breakdown cause, repair records or transfer details, and update the vehicle maintenance schedule in the fleet management system. If the breakdown was caused by a maintenance issue that should have been caught during pre-trip inspection, flag the transport company for a compliance review.

### Exceptions and Handling

If a quick fix is available and the repair takes less than two hours, the trip continues with the same vehicle and driver under close monitoring. The TMS Agent increases the tracking frequency for the remainder of the trip. If no replacement vehicle is available in a high-demand zone, the Dispatch Team considers partial delivery options where feasible, such as offloading a portion of the cargo to a smaller available vehicle. High-value cargo breakdowns require mandatory supervisor notification and a security assessment before any cargo transfer is authorized.

### Escalation Protocol

No replacement vehicle available within four hours escalates to the Operations Manager. Driver injury escalates to Emergency Services and HR simultaneously. High-value cargo breakdowns escalate to the Security Team and Operations Director for security assessment and authorization of the transfer process.

### Compliance Notes

All breakdown events must be recorded in the exception_cases table with the breakdown cause, recovery method, and total delay impact. Vehicle maintenance records must be updated after every breakdown to support fleet reliability analysis. Insurance claims for breakdown-related cargo damage must follow the insurance boundary policy where Zippy transmits evidence only.

## SOP-011: POD Dispute Resolution

### Purpose

This procedure handles disputes arising from proof of delivery, including signature discrepancies, missing or forged signatures, damaged cargo claims, delivery location disputes, and consignee denial of receipt. POD disputes are sensitive because they involve conflicting claims between the customer and the driver or transport company, and resolution must be based on objective evidence while maintaining fairness to all parties.

### Scope

This SOP covers all POD-related disputes from customers, consignees, or transport companies. It includes dispute intake, evidence review, investigation, classification, resolution, and post-dispute analysis. Both single-order disputes and patterns of disputes indicating systemic issues are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| DISPUTE Agent | DISPUTE | Scores disputes and recommends resolution paths |
| Customer Support | N/A | Investigates dispute details and gathers evidence |
| SUP Agent | SUP | Approves resolutions involving compensation above threshold |
| FIN Agent | FIN | Processes refunds and credits after approval |

### Pre-conditions

Dispute must be filed within seven days of delivery. Order must have a POD on record. Delivery GPS trail must be available for investigation.

### Procedure

1. Receive the POD dispute from the customer or consignee via any channel including the web application, phone call, email, or WhatsApp message. Create a unique case ID in the exception_cases table with case_type set to pod_dispute.
2. DISPUTE Agent scores the dispute using the dispute.score action based on the following factors: quality and completeness of the submitted POD evidence, customer complaint history and credibility, declared cargo value and potential financial exposure, SLA impact and delivery timeline deviation, and whether similar disputes have been filed for the same driver or route in the past.
3. Review the POD evidence checklist in detail: is the signature present and does it match the consignee's known signature? Is the photo evidence clear, well-lit, and timestamped? Does the GPS location recorded at delivery match the delivery address within an acceptable radius? Is the delivery timestamp within the expected delivery window?
4. Investigate the discrepancy by comparing POD data with order data: does the cargo description in the POD match the order record? Are the weight and package count consistent? Compare the delivery GPS trail with the planned route and any deviations recorded during the trip. Review the state audit log for any unusual state transitions or timing anomalies.
5. Contact the driver for their statement on the delivery circumstances. Document the driver's account of what happened at the delivery point, including any unusual conditions or consignee behaviour.
6. Contact the consignee for their version of events. Record their specific complaint: did they not receive the cargo at all? Was the cargo damaged? Was it delivered to the wrong address? Was the signature forged?
7. Classify the dispute resolution path: Valid dispute where evidence clearly supports non-delivery or damage, proceed to resolution with compensation. Invalid dispute where evidence supports successful delivery, provide the evidence to the customer with an explanation. Partial dispute where some elements are unclear or contradictory, negotiate a resolution that balances the interests of all parties.
8. For valid disputes, determine the appropriate resolution: re-delivery at no extra cost when the cargo is available and the customer still needs it, full refund when the cargo is lost or damaged beyond use, partial refund based on damage assessment when the cargo is partially usable, or replacement shipment when a new shipment can be arranged quickly.
9. For compensation exceeding five thousand INR, SUP Agent must approve the resolution through the case.approve action. The approval must include documented justification and the evidence supporting the decision.
10. FIN Agent processes the refund or credit after SUP Agent approval. The refund is recorded in the payment_records table with a unique idempotency_key, and a journal entry is created to reverse the original revenue recognition if applicable.
11. COMMS Agent communicates the resolution to all parties: the customer receives confirmation of the refund or re-delivery, and the driver and transport company are notified of the dispute outcome and any performance impact.
12. Document the complete dispute in the exception_cases table with the full evidence chain, the dispute score, the resolution decision, and the supervisor approval if applicable. This record supports pattern analysis and regulatory compliance.
13. Analyze dispute patterns on a weekly basis: if a specific driver, route, or transport company shows a dispute rate exceeding five percent, flag for performance review. If a specific cargo type consistently generates disputes, review the loading and handling procedures. Update the fraud detection model with new patterns identified during investigations.

### Exceptions and Handling

Compensation exceeding five thousand INR requires mandatory Supervisor approval regardless of the evidence strength. Legal threats from either party trigger immediate escalation to the Legal Department. Repeated disputes from the same driver trigger a performance review and potential suspension from the platform. Disputes involving suspected forgery or fraud are routed directly to the SUP Agent for fraud investigation under SOP-015.

### Escalation Protocol

Compensation above five thousand INR escalates to the Supervisor for approval. Any legal threat escalates to the Legal Department. Media risk from a high-profile dispute escalates to the Communications Director. Repeated disputes from the same source escalate to the Operations Director for relationship review.

### Compliance Notes

All dispute resolutions must be documented in the exception_cases and supervisor_decisions tables. Refunds must follow the standard financial controls including idempotency_key and journal entries. Dispute patterns indicating potential fraud must be reported to the SUP Agent for investigation under the fraud hold procedure.

## SOP-012: Customer Complaint Handling

### Purpose

This procedure provides a consistent, fair, and timely process for receiving, investigating, and resolving customer complaints across all channels. Effective complaint handling is critical for customer retention, brand reputation, and regulatory compliance. Every complaint must be treated as an opportunity to identify and fix systemic issues while providing the individual customer with a satisfactory resolution.

### Scope

This SOP covers all customer complaints including but not limited to shipment delays, cargo damage, billing errors, service quality issues, and lost cargo. It applies to complaints received through any channel and covers the entire lifecycle from initial acknowledgment through resolution and post-resolution follow-up.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| COMMS Agent | COMMS | Acknowledges complaint and manages communication |
| Customer Support | N/A | Investigates complaint and proposes resolution |
| DISPUTE Agent | DISPUTE | Scores complaint severity and recommends action |
| SUP Agent | SUP | Approves high-value resolutions |
| FIN Agent | FIN | Processes refunds and credits |

### Pre-conditions

Complaint must be from a verified customer with an active or recent order. Customer contact information must be current for follow-up communication.

### Procedure

1. Acknowledge the complaint within one hour of receipt via the customer's preferred communication channel. The acknowledgment must include a unique case reference number, confirmation that the complaint has been received and logged, and a commitment to provide an update within twenty-four hours.
2. Log the complaint in the CRM system with a unique case ID, the customer's details including account ID and contact information, the order reference number, the complaint category selected from the standardized list, and the customer's initial statement of the issue.
3. Gather comprehensive information about the complaint: review the order details including all state transitions and timestamps, examine the timeline of events from booking through delivery, understand the customer's specific grievance and their desired resolution, and collect any supporting evidence the customer can provide such as photos of damaged cargo, delivery screenshots, or correspondence.
4. Classify the complaint into one of five categories: Delay complaint where the shipment arrived later than the promised delivery time, which may warrant partial refund or service credit. Damage complaint where the cargo was damaged during transit, which may warrant full refund or replacement. Service quality complaint covering driver behaviour, communication failures, or process issues, which may warrant apology and service credit. Billing error complaint involving incorrect charges, duplicate billing, or pricing discrepancies, which requires correction and refund of the overcharged amount. Lost cargo complaint where the cargo was not delivered and cannot be located, which requires full compensation and investigation.
5. Investigate the complaint by reviewing the order events in the state audit logs, the driver communications and milestone reports, the POD records and GPS trail, the pricing calculation and margin verification, and any previous complaints from the same customer or involving the same driver or route.
6. Determine the appropriate resolution and calculate any compensation amount. The resolution must be proportional to the severity of the issue, consistent with previous similar cases, within the authorized compensation limits for the support agent's level, and compliant with the customer agreement and SLA terms.
7. Propose the resolution to the customer. If the customer accepts, proceed to execution. If the customer rejects the proposed resolution, escalate to the next level of authority with the customer's counter-proposal and the investigation findings.
8. Execute the resolution: process the refund through the FIN Agent, issue a service credit to the customer's account, arrange a replacement shipment through the OMS Agent, or implement service recovery measures such as priority handling for the customer's next booking.
9. Follow up with the customer within forty-eight hours of resolution to confirm satisfaction. The follow-up must ask whether the resolution was implemented as promised, whether the customer is satisfied with the outcome, and whether there is anything else the customer needs.
10. Close the case in the CRM with a resolution summary, the lessons learned, and any recommended process improvements to prevent similar complaints in the future.
11. Monitor for escalation triggers: compensation requests exceeding five thousand INR, any legal threat from the customer, potential media exposure risk, repeated complaints from the same customer within a thirty-day period, and systemic patterns suggesting a broader operational issue.

### Exceptions and Handling

High-value customer complaints receive priority handling with a dedicated account manager assigned to coordinate the resolution. Regulatory complaints such as those involving GST issues, privacy violations, or consumer protection claims are routed to the Compliance Officer immediately without going through the standard complaint process. Complaints involving suspected fraud are routed to the SUP Agent for fraud investigation under SOP-015.

### Escalation Protocol

Compensation exceeding five thousand INR escalates to the Customer Service Manager for approval. Legal threats escalate to the Legal Department. Media risk escalates to the Communications Director. Repeated systemic complaints about the same issue escalate to the Operations Director for root cause analysis and process improvement.

### Compliance Notes

All complaints must be documented in the CRM and linked to the order record. Compensation must follow financial controls with proper authorization. Privacy requirements under the DPDP Act must be maintained during all complaint communications. Customer complaint data must be analyzed monthly for trend identification and process improvement.

## SOP-013: Customer Communication Standards

### Purpose

This procedure defines the standards, timing, channels, and content requirements for all customer-facing communications throughout the shipment lifecycle. Consistent, accurate, and timely communication is a key differentiator for Zippy Logistics, directly impacting customer satisfaction, trust, and retention. Every communication must reinforce the platform's commitment to transparency and reliability.

### Scope

This SOP applies to all customer communications from booking confirmation through delivery and post-delivery follow-up. It covers proactive notifications triggered by order state changes, reactive communications in response to customer inquiries, and marketing or relationship management communications. All channels including SMS, email, WhatsApp, and in-app notifications are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| COMMS Agent | COMMS | Drafts and triggers all customer notifications |
| Customer Support | N/A | Handles customer responses and inquiries |
| OMS/TMS/FIN Agents | Various | Provide context data for accurate communications |

### Pre-conditions

Customer contact information must be verified and current. Communication templates must be approved and loaded in the system. The DPDP privacy masking middleware must be active for all API responses.

### Procedure

1. Identify the communication trigger point in the order lifecycle: booking confirmation when the order is created, price estimate when pricing is generated, vehicle assigned when a match is accepted, pickup started when the driver departs, loading complete when cargo is loaded, in-transit milestones at major checkpoints, approaching delivery when the driver is near the destination, delivered when POD and OTP are verified, POD available when the customer can download delivery evidence, and settlement complete when payment is processed.
2. Confirm the current context by pulling the latest order state, milestone data, and any active exceptions from the system. Never communicate based on stale data, as this can create confusion and erode trust.
3. Prepare the message content following five core principles: accuracy with no speculation or unverified claims, proactivity by notifying the customer before they need to ask, specificity with exact times, amounts, and locations rather than vague statements, documentation by logging all communications in the CRM and outbox, and channel awareness by matching the communication urgency to the appropriate channel.
4. COMMS Agent drafts the notification using the notification.draft action. The draft must include the communication content, the target channel, the recipient role, and any data references needed for personalization.
5. Apply DPDP privacy masking to all communications. The DPDPPrivacyMaskingMiddleware automatically masks phone numbers to the asterisk-prefixed last four digits format in all API responses. Direct customer communications must respect the same masking standards when referencing other parties' contact information.
6. COMMS Agent triggers the notification using the notification.trigger action. The trigger records the dispatch event in the outbox for audit trail purposes.
7. Handle customer responses by routing replies to the appropriate agent or support queue. If the customer responds with a question, the COMMS Agent can handle routine inquiries directly. If the response involves a complaint or escalation, route to Customer Support. If the response involves a change to the order, route to the OMS Agent.
8. Log all communications in the event outbox with the communication type, channel, recipient, content summary, and delivery status. This creates a complete audit trail of all customer touchpoints.
9. For delay notifications specifically, always include the reason for the delay in clear and honest terms, the revised ETA calculated from current conditions, alternative options if available such as re-routing or schedule changes, and a genuine apology for the inconvenience caused.
10. For price-related communications, always include the base cost calculation, each applicable surcharge itemized with a brief explanation, the platform fee percentage and amount, and the GST breakdown showing both transport and services components separately.
11. Never promise specific outcomes that are not system-verified. For example, do not guarantee a specific delivery time if the order has not yet been assigned to a driver. Do not confirm a refund amount that has not been calculated by the FIN Agent. Do not state that a vehicle has been dispatched if the order is still in the RINGING state.
12. All communications must be traceable via trace_id and idempotency_key for audit and compliance purposes. If a communication fails to deliver, retry up to three times through alternative channels before logging a delivery failure.

### Exceptions and Handling

If the customer is unreachable after three communication attempts across different channels, document the attempts and continue the shipment process. The customer will be notified upon their return to the platform. If the communication system experiences a failure, use backup channels such as phone calls for critical notifications. If a customer requests a callback, schedule it within two hours during business hours or at the next business hour start for after-hours requests.

### Escalation Protocol

Customer expressions of significant frustration or anger during communication should be escalated to a senior support agent with training in de-escalation techniques. Any communication breach such as sending information to the wrong recipient must be reported immediately to the SUP Agent as a DPDP incident requiring investigation and remediation.

### Compliance Notes

All customer communications must comply with the DPDP Act regarding personal data handling. Phone numbers and other PII must be masked in all shared communications. Communications about pricing must accurately reflect the system-calculated amounts and must not misrepresent the fee structure.

## SOP-014: Supervisor Exception Handling

### Purpose

This procedure defines how supervisor agents identify, hold, investigate, and resolve exception cases that require human oversight in the order-to-settlement flow. Supervisor exceptions are the safety net that catches issues that automated policy enforcement cannot resolve on its own, including fraud indicators, policy violations, confidence threshold breaches, and complex operational situations that require human judgment.

### Scope

This SOP covers all exception cases including fraud detection, policy violations, compliance failures, confidence threshold breaches, and manual escalation requests from other agents or human operators. It encompasses the full lifecycle of an exception from initial trigger through resolution and post-resolution analysis.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| SUP Agent | SUP | Identifies exceptions, places holds, and manages resolution |
| Supervisor | N/A | Makes human judgment decisions on exception cases |
| OMS/TMS/FIN Agents | Various | Provide context and execute post-resolution actions |
| Compliance Officer | N/A | Advises on compliance-related exceptions |

### Pre-conditions

The exception must have a valid trigger from the policy service, a fraud detection alert, or a manual escalation. The exception_cases table must be accessible for case creation. The supervisor must have the appropriate role authorization for the case type.

### Procedure

1. SUP Agent receives an exception trigger from one of the following sources: a policy preflight failure creating a PolicyDecision with result equal to reject or hold, a confidence score below the threshold for the decision category, a fraud_score greater than or equal to 0.75 from the fraud detection model, a payment amount greater than or equal to 500,000 INR triggering automatic review, or a manual escalation from another agent or human operator identifying an unusual situation.
2. Create an exception case in the exception_cases table with the following details: case_type set to fraud, policy, compliance, or operational depending on the trigger, severity rated as low, medium, high, or critical based on the financial exposure and risk level, a descriptive title summarizing the exception, a detailed description of the triggering condition and initial evidence, and the created_by field set to the SUP Agent or the triggering source.
3. If a fraud indicator is detected with a fraud_score at or above 0.75, immediately place a fraud hold on the order. Create a record in the fraud_holds table with the order_id, the reason for the hold, is_active set to True, and the placed_by field set to the SUP Agent. This blocks all downstream actions including settlement release.
4. If a settlement is at risk due to the exception, place a settlement hold. Create a record in the settlement_holds table with the settlement_id, order_id, and trip_id if available, the reason for the hold, is_active set to True, and the placed_by field. This specifically blocks the settlement release process.
5. Notify relevant stakeholders via outbox events. The event must include the exception case details, the type and severity of the hold placed, the order and trip references, and the expected response timeline for investigation and resolution.
6. Investigate the exception by reviewing the state_audit_logs for the order to understand the complete lifecycle and identify anomalies, the policy_decisions for any previous policy evaluations on the order, the order timeline comparing expected versus actual state transitions, and the agent action history for any unusual patterns or unauthorized access attempts.
7. Gather additional evidence as needed: request documents from the transport company such as vehicle inspection reports or driver logs, verify information with the customer through a confirmation call or message, check the vehicle GPS trail for route anomalies or unauthorized stops, and cross-reference with external systems such as VAHAN for vehicle verification or SARATHI for driver license verification.
8. Make a decision based on the investigation findings: Approve the exception, release all holds, and allow the order to continue its normal flow. Reject the exception, cancel the order if appropriate, and initiate refund or corrective processes. Escalate the exception to a higher authority if the case exceeds the supervisor's authorization level or involves complex legal or compliance issues.
9. Record the supervisor decision in the supervisor_decisions table with the decision field set to approve, reject, or escalate, detailed notes explaining the rationale, the decided_by field with the supervisor's identity, and any payload data supporting the decision such as evidence references or policy interpretations.
10. If the decision is to approve, release all holds: update fraud_holds and settlement_holds records to set is_active to False, record the released_by and released_at timestamps, and emit outbox events confirming the hold release. The order can then continue through its normal lifecycle.
11. If the decision is to reject, ensure all financial records are corrected: reverse any revenue recognition entries through journal entries, process any required customer refunds through the FIN Agent, and notify all affected parties through the COMMS Agent.
12. Emit an outbox event for exception.resolved with the full decision trail including the case ID, the decision, the justification, and the evidence chain. This event enables monitoring dashboards to track exception resolution metrics.

### Exceptions and Handling

Critical severity cases involving a fraud_score above 0.9 or a payment amount exceeding 1,000,000 INR require mandatory dual-supervisor approval before any hold can be released. System-generated holds cannot be overridden without documented evidence justifying the release. No-override cases include expired vehicle registration, suspended driver license, missing E-Way Bill for mandatory shipments, and bank account mismatch for settlement payments.

### Escalation Protocol

Critical fraud cases escalate to the Chief Risk Officer. High-value payment disputes escalate to the Finance Director. Compliance violations escalate to the Compliance Officer. Repeated exceptions from the same source such as a specific transport company or route trigger an Operations Director review of the underlying cause.

### Compliance Notes

All exception cases must be documented in the exception_cases, supervisor_decisions, and relevant hold tables with complete traceability. Hold release must include documented justification and the identity of the approving supervisor. No-override cases must be respected without exception as they represent regulatory hard blocks.

## SOP-015: Fraud Hold and Investigation

### Purpose

This procedure addresses the detection, hold, investigation, and resolution of suspected fraudulent activities including fake bookings, ghost deliveries, price manipulation, identity fraud, and collusion between customers and drivers. Fraud prevention is essential for protecting the platform's financial integrity, maintaining trust with legitimate users, and complying with regulatory requirements. Every suspected fraud case must be handled with urgency, thoroughness, and strict confidentiality.

### Scope

This SOP covers all fraud detection triggers, investigation procedures, hold management, and resolution processes. It applies to suspected fraud involving any participant in the logistics chain: customers, drivers, transport companies, and internal staff. Both individual fraud cases and organized fraud patterns are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| SUP Agent | SUP | Detects fraud indicators and places immediate holds |
| Fraud Investigation Team | N/A | Conducts detailed investigation and evidence analysis |
| Finance Admin | N/A | Releases holds after clearance and processes refunds |
| COMMS Agent | COMMS | Communicates hold status without revealing investigation details |

### Pre-conditions

Fraud trigger must be validated from at least one source: policy service alert, fraud detection model score, pattern detection algorithm, or external tip. The fraud_holds table must be accessible for immediate hold placement.

### Procedure

1. Receive the fraud trigger from one of the following sources: a fraud_score of 0.75 or higher from the policy evaluation, an automatic hold triggered by a payment of 500,000 INR or more, pattern detection flags such as the same IP address creating multiple bookings, unusual route combinations that suggest testing or exploitation, repeated cancellations that suggest booking manipulation, discrepancies between declared and actual cargo, or an external tip from a partner, customer, or regulatory body.
2. Immediately place a fraud hold on the order by creating a record in the fraud_holds table with the order_id, a detailed reason for the hold, is_active set to True, and the placed_by field. This hold blocks ALL downstream actions including vehicle assignment, state transitions, and settlement release. Time is critical: the hold must be placed within five minutes of the trigger to prevent further potentially fraudulent activity.
3. Notify the Fraud Investigation Team via an outbox event with the case details including the triggering source, the fraud score if applicable, the order and customer details, and the initial evidence summary. The notification must be sent within fifteen minutes of the hold placement.
4. Collect evidence systematically: review the booking pattern including frequency, timing, and IP addresses associated with the customer account. Examine the payment history for unusual amounts, rapid refunds, or payment method changes. Analyze the delivery GPS trail for route anomalies, stops at unusual locations, or GPS spoofing indicators. Check the POD verification records for signature discrepancies, photo manipulation, or timestamp anomalies. Review the vehicle and driver history for previous fraud flags, complaints, or suspicious activity.
5. Analyze the collected evidence by cross-referencing with known fraud patterns from historical case data, verifying identities through VAHAN and SARATHI databases, checking for collusive behaviour such as the same customer repeatedly booking with the same driver, and evaluating the consistency of all evidence points. Genuine orders should have consistent data across all dimensions: booking, payment, routing, delivery, and documentation.
6. If the evidence confirms fraud: reject the order and cancel any pending shipments. Process a refund if payment was collected but the shipment was not genuine. Blacklist the entities involved including customer accounts, driver profiles, and transport company registrations. File a regulatory report if the fraud amount exceeds the reporting threshold or involves identity theft. Record the complete case in the exception_cases table with the fraud classification and evidence chain.
7. If the evidence clears the suspicion and the activity is determined to be legitimate: release the fraud hold by setting is_active to False in the fraud_holds table, record the released_by and reason in the hold record, and allow the order to continue its normal lifecycle. Notify the customer that the verification is complete using neutral language that does not disclose the fraud investigation details.
8. If the investigation is inconclusive after the initial evidence review: maintain the fraud hold and request additional evidence such as further identity verification from the customer, additional documentation from the transport company, or enhanced monitoring of the current trip. Set a review deadline of seventy-two hours maximum for the additional evidence collection. If the deadline passes without resolution, escalate to the Fraud Investigation Team lead for decision.
9. SUP Agent records all decisions in the supervisor_decisions table with the complete evidence chain, the decision rationale, and the identity of the decision-maker. This creates an audit trail for regulatory compliance and pattern analysis.
10. FIN Agent ensures no settlement is released while the fraud hold is active. This is enforced at the database level in the settlement release process as documented in SOP-008.
11. COMMS Agent communicates the hold status to the customer using language such as verification in progress or order under review without revealing the specific fraud investigation details. The communication must not accuse the customer of fraud or create unnecessary alarm while maintaining the hold.
12. Post-resolution: update the fraud detection model with the new patterns identified during the investigation. Update blacklists with confirmed fraudulent entities. Review and adjust fraud_score thresholds if the false positive rate exceeds ten percent in any week. Share anonymized fraud patterns with the industry if permitted by data protection regulations.

### Exceptions and Handling

If the false positive rate exceeds ten percent in any week, the fraud detection thresholds should be reviewed and adjusted in consultation with the Fraud Investigation Team and the Product Manager. For time-sensitive orders with a low fraud_score between 0.75 and 0.85, a Supervisor can approve the order to proceed with enhanced monitoring, including more frequent GPS tracking and milestone verification. For regulatory investigations, cooperate fully with the authorities and do not release any holds until explicitly cleared by the investigating agency.

### Escalation Protocol

Confirmed fraud exceeding 500,000 INR escalates to the Chief Risk Officer and Legal Department for potential criminal proceedings. Identity theft suspicion escalates to Cyber Crime reporting authorities. Internal fraud involving employees escalates to HR and Legal with immediate access revocation for the implicated staff member.

### Compliance Notes

All fraud investigations must be documented with full evidence chains in the exception_cases and supervisor_decisions tables. Fraud hold placement and release must be logged with timestamps and identities. Blacklisted entities must be maintained in a secure, access-controlled registry. Fraud patterns must be reported to the product and engineering teams for model improvement.

## SOP-016: Partner Transporter Management

### Purpose

This procedure manages the onboarding, assignment, monitoring, and evaluation of partner transport companies and their fleets. Partner transporters are essential for extending Zippy's capacity beyond the own fleet, especially during peak demand periods and in regions where direct fleet operations are not economically viable. Effective partner management ensures consistent service quality, regulatory compliance, and fair commercial terms across the entire network.

### Scope

This SOP covers partner transporter verification, order assignment, performance monitoring, tier management, and relationship governance. It applies to all partner transport companies from initial onboarding through ongoing operations and annual contract review. Out of scope are own-fleet vehicle assignments, covered in SOP-003.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| IMS Agent | IMS | Includes partner vehicles in matching algorithm |
| ADMIN_OPS Agent | ADMIN_OPS | Verifies partner documents and compliance status |
| Dispatch Team | N/A | Assigns orders to partner vehicles and coordinates operations |
| Operations Manager | N/A | Evaluates partner performance and manages tier progression |

### Pre-conditions

Partner must have valid business registration and GST registration. Fleet documents including vehicle registrations, insurance certificates, and fitness certificates must be current. Driver licenses must be verified through SARATHI.

### Procedure

1. Partner transporter onboarding begins with verification of business registration documents, GST registration certificate confirming the GSTIN is active and valid, fleet documentation including vehicle registration certificates, insurance certificates, and fitness certificates for each vehicle offered to the platform, and driver license verification through SARATHI for every driver who will operate on the platform.
2. ADMIN_OPS Agent runs compliance checks on all submitted documents using the compliance.check action. Each document is validated against regulatory requirements and flagged if any items are expired, incomplete, or inconsistent.
3. Classify the partner into one of three tiers based on their verification status and track record: Bronze tier for newly onboarded partners with basic verification completed, standard commission rates, and normal priority in vehicle matching. Silver tier for partners with a proven performance track record over at least three months, a two percent commission reduction as a performance incentive, and priority matching over Bronze partners. Gold tier for partners with volume commitments and consistently excellent performance, a five percent commission reduction, VIP matching priority, and access to premium order flows.
4. When an order requires partner fleet capacity, IMS Agent includes partner vehicles in the matching algorithm with priority adjusted by tier: Gold partners are offered orders before Silver, who are offered before Bronze. The matching considers the same vehicle criteria as own-fleet matching: category, body type, payload, and location proximity.
5. Assign the order to the partner transporter following the standard vehicle assignment process in SOP-003. The partner receives the assignment through the transport company web console with the same order details and pickup requirements.
6. Coordinate pickup and delivery with the partner's dispatch team. The partner is responsible for ensuring their driver reports milestones through the driver application, complies with document requirements, and follows the standard POD and OTP procedures.
7. Monitor partner performance continuously using the following metrics: on-time delivery rate measured as the percentage of shipments delivered within the promised SLA window, POD quality measured as the percentage of deliveries with clean, verified POD evidence, damage rate measured as the percentage of shipments with cargo damage complaints, and customer complaint rate measured as the number of complaints per hundred shipments.
8. Handle partner-specific issues: driver behaviour complaints are investigated and may result in the specific driver being suspended from the platform. Documentation failures such as missing E-Way Bills or expired vehicle fitness certificates result in a warning and a compliance deadline. Payment disputes are resolved per the Partnership Agreement's dispute resolution clause. Capacity shortfalls where the partner commits vehicles but fails to provide them are tracked and affect the partner's health score.
9. Conduct monthly performance reviews by calculating the partner health score using weighted metrics: on-time delivery rate weighted at thirty percent, POD quality at twenty-five percent, damage rate at twenty percent, customer complaint rate at fifteen percent, and capacity reliability at ten percent.
10. Adjust partner tiers based on performance: promote partners who consistently exceed target metrics for three consecutive months, downgrade partners whose performance declines below the threshold for their current tier for two consecutive months, and suspend partners with critical failures such as safety violations, fraud involvement, or persistent non-compliance.
11. Settlement with partners follows the standard SOP-008 procedure with additional verification of the partner's bank account details to prevent misdirected payments. The partner's commission rate is applied according to their tier at the time of order completion.
12. Conduct annual contract reviews with each partner covering performance data, tier status, commission rate adjustments, capacity commitments for the upcoming period, and any regulatory or compliance changes that affect the partnership terms.

### Exceptions and Handling

If a partner transporter fails mid-trip, activate a backup transporter from the partner pool immediately. The replacement must meet all the original order requirements and the original partner bears the cost differential if the replacement is more expensive. If a partner's insurance lapses, suspend the partner from the platform immediately until the insurance is renewed and verified. Partner disputes that cannot be resolved through standard negotiation are escalated to the Partnership Agreement's formal dispute resolution process.

### Escalation Protocol

Partner non-performance affecting customer SLA escalates to the Operations Manager for intervention. Contract breaches such as unauthorized sub-contracting or data misuse escalate to the Legal Department. Safety violations including unroadworthy vehicles or unlicensed drivers trigger immediate suspension and escalation to the Compliance Officer.

### Compliance Notes

Partner onboarding must include DPDP Act compliance regarding customer data handling. Partner commission rates must be documented in the partnership agreement and applied consistently. All partner settlements must follow the standard financial controls including segregation of duties and idempotency requirements.

## SOP-017: Urgent and Express Shipment Handling

### Purpose

This procedure handles time-critical shipments requiring expedited processing, priority vehicle assignment, and enhanced monitoring throughout the delivery lifecycle. Urgent shipments command premium pricing and carry higher customer expectations for speed and reliability. The platform must deliver on its urgency promises while maintaining safety, compliance, and financial integrity.

### Scope

This SOP covers Express shipments with two to four hour pickup windows, Same Day shipments requiring pickup within six hours, and Critical shipments requiring immediate pickup for emergency situations. All urgency tiers involve premium pricing and priority resource allocation. Standard shipments follow SOP-001 and SOP-003 instead.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| OMS Agent | OMS | Prioritizes order processing and fast-tracks validation |
| IMS Agent | IMS | Fast-tracks vehicle matching with expanded search |
| TMS Agent | TMS | Enables enhanced real-time tracking and monitoring |
| COMMS Agent | COMMS | Provides real-time updates at every milestone |

### Pre-conditions

Customer must explicitly request and confirm an urgency tier. Urgency premium pricing must be accepted before order creation. The system must have vehicle availability in the expanded search radius for the pickup area.

### Procedure

1. Customer requests an urgent shipment through any channel and specifies the required urgency level. The system assesses the appropriate urgency tier: Express tier with a two to four hour pickup window and a twenty-five percent surcharge on the base price, Same Day tier with pickup within six hours and a fifty percent surcharge, or Critical tier with immediate pickup and a seventy-five to one hundred percent surcharge with VIP handling throughout the lifecycle.
2. OMS Agent validates the order with priority processing, completing all validations within fifteen minutes instead of the standard processing window. The validation includes all standard checks from SOP-001 plus an assessment of whether the requested timeline is feasible given current vehicle availability and route conditions.
3. Pricing Engine applies the urgency premium to the base price. The premium is calculated on top of all other applicable charges including base cost, surcharges, and platform fee. The total price including the urgency premium and GST is presented to the customer for confirmation.
4. Customer confirms the urgency premium pricing and accepts the total amount. The confirmation is recorded in the order metadata with the urgency tier, the premium percentage, and the customer's acceptance timestamp.
5. IMS Agent fast-tracks vehicle matching by bypassing the standard queue, searching an expanded radius around the pickup location, and including the partner fleet immediately rather than as a fallback. The matching algorithm prioritizes speed of assignment over utilization optimization for urgent orders.
6. Dispatch Team assigns the best available vehicle regardless of utilization optimization considerations. The closest available vehicle that meets the cargo requirements is selected, even if this means a less efficient deployment of the vehicle fleet.
7. Driver receives a priority assignment notification with an urgency flag through the driver application. The notification highlights the time-critical nature of the assignment and the pickup deadline that must be met.
8. TMS Agent enables real-time tracking with a two-minute update interval instead of the standard fifteen-minute interval. This provides the operations team and the customer with near-real-time visibility into the shipment progress.
9. COMMS Agent provides real-time updates to the customer at every milestone, including driver assignment, driver departure, pickup arrival, loading, transit checkpoints, and approach to delivery. Each update includes the current status and the expected time for the next milestone.
10. If the timeline is at risk at any point during the process, immediately escalate to the next authority level without waiting for the standard delay thresholds. For urgent shipments, even a thirty-minute delay warrants proactive escalation and customer communication.
11. Post-delivery verification confirms whether the SLA was met, calculates any penalty if the promised timeline was missed despite the premium paid, and documents lessons learned for improving the urgent shipment handling process.
12. If the urgency SLA is breached, process a partial refund of the urgency premium proportional to the delay. For Critical tier breaches, offer a full refund of the urgency premium plus a service credit as compensation.

### Exceptions and Handling

If no vehicle is available for a critical urgency request, the Operations Director can authorize external procurement from non-partner sources at a higher cost, with the cost differential covered by the platform. If the customer rejects the urgency premium pricing, offer the standard timeline with a clear explanation of the difference in service levels. Critical shipments involving hazardous cargo must still complete compliance verification before expedited dispatch, as safety cannot be compromised for speed.

### Escalation Protocol

Express tier delays exceeding thirty minutes escalate to the Team Lead. Same Day tier delays exceeding one hour escalate to the Manager. Critical tier delays at any point escalate directly to the VP Operations. All delays on urgent shipments trigger customer notification within fifteen minutes of the delay being identified.

### Compliance Notes

Urgency premiums must be calculated by the Pricing Engine and cannot be manually overridden without Finance Director approval. All urgent shipment SLAs must be tracked separately from standard shipment metrics. The urgency premium refund policy must be clearly communicated to customers before they confirm the booking.

## SOP-018: GST and E-Way Bill Compliance

### Purpose

This procedure ensures that all shipments comply with Indian GST regulations and E-Way Bill requirements, and that accurate GST invoices are generated for every settlement. GST compliance is a legal requirement with significant penalties for non-compliance, and the platform must maintain impeccable records to support both operational needs and regulatory audits. The procedure aligns with the Ind AS 115 broker model where Zippy recognizes only commission and platform fee as revenue.

### Scope

This SOP covers GST calculation, E-Way Bill management, GST invoice generation, revenue recognition validation, and regulatory reporting preparation. It applies to all shipments regardless of cargo type or route, with particular emphasis on interstate shipments where both GST and E-Way Bill requirements are more complex.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| FIN Agent | FIN | Calculates GST, generates invoices, and records journal entries |
| ADMIN_OPS Agent | ADMIN_OPS | Runs compliance checks and validates E-Way Bills |
| Policy Service | N/A | Enforces margin floors and compliance document rules |
| SUP Agent | SUP | Handles compliance exceptions and escalation cases |

### Pre-conditions

All orders must have the applicable GST rates configured in the system. The E-Way Bill generation system must be accessible for interstate shipments. The gst_invoice_records table must be available for invoice creation with unique invoice_number constraint.

### Procedure

1. At order creation, determine the GST applicability: transport of goods by road attracts twelve percent GST, while platform services including brokerage and orchestration fees attract eighteen percent GST. For interstate shipments, Integrated GST (IGST) applies at the full rate. For intrastate shipments within the same state, Central GST (CGST) and State GST (SGST) each apply at half the applicable rate.
2. Pricing Engine includes GST in the price estimate from the earliest customer-facing calculation. The estimate must clearly separate the base cost, platform fee, and GST components so that the customer understands the tax breakdown.
3. For interstate shipments with a consignment value exceeding fifty thousand INR, flag the E-Way Bill as a mandatory requirement in the compliance document rules. The system must prevent dispatch without a valid E-Way Bill for these shipments.
4. Generate the E-Way Bill through the NIC portal with the correct consignor GSTIN, consignee GSTIN, HSN codes for the goods being transported, vehicle registration number, transporter details, and the applicable GST rates. In the current MVP, this integration is simulated, but the data structure and validation logic must mirror the real integration requirements.
5. Validate the E-Way Bill details: the consignor and consignee GSTINs must be valid and active. The HSN codes must correctly classify the goods. The vehicle number must match the assigned vehicle. The E-Way Bill must be within its validity period, which is one day per one hundred kilometres for normal cargo and one day per two hundred kilometres for over-dimensional cargo.
6. At settlement, FIN Agent creates a GSTInvoiceRecord in the gst_invoice_records table with a unique invoice_number generated by the system, the taxable_amount separated into transport and services components, the gst_amount calculated as twelve percent of the transport component plus eighteen percent of the services component, the total_amount as the sum of taxable and GST amounts, and the current status of the invoice.
7. Verify that the GST invoice aligns with the Ind AS 115 broker model: Zippy's recognized revenue under the agent model must equal commission plus platform fee only. The gross freight amount is not Zippy's revenue. The validate_no_gross_revenue_under_agent_model function in the accounting controls enforces this constraint programmatically.
8. Validate segregation of duties: the user who generates the GST invoice must be different from the user who approves the settlement release. The SegregationOfDutiesValidator in the accounting controls module enforces this requirement.
9. Emit the GST invoice outbox event with event type finance.gst_invoice_created. The event includes the invoice details, the linked settlement and journal entry references, and the applicable tax period for reporting purposes.
10. Conduct monthly GST reconciliation by comparing gst_invoice_records with payment_records and settlement_records. Identify and resolve any discrepancies in GST amounts, invoice numbers, or tax periods before filing monthly returns.
11. Prepare for GST return filing by aggregating invoice data for the tax period, reconciling input tax credits where applicable, and generating the return preparation reports. In the current MVP, actual filing with the NIC portal is a post-pilot integration task.
12. Maintain all GST records for a minimum of six years from the date of filing as required by the Central Goods and Services Tax Act. Records include invoices, E-Way Bills, payment receipts, and reconciliation statements.

### Exceptions and Handling

If E-Way Bill generation fails due to NIC portal downtime, a conditional override may be granted with maker-checker approval from a Supervisor. The E-Way Bill must be generated within twenty-four hours of dispatch, and the shipment is flagged for compliance tracking until the bill is produced. GST rate disputes with customers are routed to the Tax Consultant for resolution. Customer GSTIN verification failures may be processed under the reverse charge mechanism if applicable, where the liability to pay GST shifts to the recipient.

### Escalation Protocol

E-Way Bill expiry during transit escalates to the Compliance Officer for extension or re-generation. GST audit queries from tax authorities escalate to the Finance Director and Tax Consultant for joint response. Revenue recognition errors discovered during reconciliation trigger immediate CFO notification and correction.

### Compliance Notes

All GST invoices must be recorded in the gst_invoice_records table with unique invoice numbers. Revenue recognition must follow the Ind AS 115 agent model constraint enforced by the accounting controls. Segregation of duties between invoice generation and settlement approval must be maintained without exception.

## SOP-019: Privacy and DPDP Compliance

### Purpose

This procedure ensures that all operations comply with the Digital Personal Data Protection Act, protecting customer, driver, and partner personal information throughout the data lifecycle. Privacy compliance is both a legal obligation and a trust-building measure that differentiates Zippy from competitors who may treat personal data as a commodity rather than a responsibility.

### Scope

This SOP covers all personal data collection, storage, processing, sharing, and masking across the platform. It applies to all categories of personal data including customer identity and contact information, driver personal and license data, transport company business details, and shipment addresses and cargo descriptions that may reveal personal information. All agents and human operators who handle personal data are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| ADMIN_OPS Agent | ADMIN_OPS | Executes privacy masking and access logging |
| All Agents | Various | Handle personal data in accordance with this SOP |
| DPDP Officer | N/A | Oversees compliance, handles incidents, and conducts audits |
| COMMS Agent | COMMS | Manages consent collection and communication preferences |

### Pre-conditions

The DPDPPrivacyMaskingMiddleware must be active in the API layer. The consent ledger must be accessible for recording and verifying consent status. All data access must be logged through the observability module.

### Procedure

1. At order intake through the consented intake endpoint, collect explicit consent for data processing with clearly defined purpose codes: order fulfilment for processing and delivering the shipment, compliance for meeting regulatory requirements such as GST and E-Way Bill, communication for sending shipment updates and notifications, and analytics for platform improvement and service optimization.
2. Record consent in the consent ledger with the timestamp of consent collection, the specific purpose codes consented to, the consent status as granted, denied, or withdrawn, and the method of consent collection such as web form checkbox, API parameter, or verbal confirmation with recording.
3. Apply DPDPPrivacyMaskingMiddleware to all API responses automatically. The middleware masks phone number fields including phone, mobile, contact_number, shipper_phone, driver_phone, and consignee_phone by replacing all but the last four digits with asterisks. For example, a phone number 9876543210 becomes asterisk-6789-0 format in the response.
4. Bypass masking only when the x-zippy-pii-access: full header is present in the API request. This header is granted only to authorized operations that require full personal information access, such as driver assignment coordination, emergency response, and compliance verification. Every bypass event is logged with the requesting identity, the data accessed, and the purpose.
5. Log all personal data access events in the audit trail: who accessed the data including agent code or user ID, what data was accessed including the specific fields and record identifiers, when the access occurred with precise timestamps, and for what purpose the access was made linking to the applicable purpose code from the consent ledger.
6. For data sharing with partner transporters: share only the minimum necessary information required for the partner to fulfil their role in the shipment. Standard information shared includes pickup and delivery addresses, cargo description, and pickup time window. Personal contact information such as customer phone numbers must be masked unless essential for delivery coordination. Ensure that each partner has equivalent data protection measures in place as required by the partnership agreement. Record all data sharing events in the audit trail.
7. For customer data deletion requests: verify the identity of the requesting party through multi-factor authentication. Check for active orders that legally require data retention such as pending settlements or GST audit periods. Delete or anonymize the personal data within thirty days of the verified request. Retain only the data required by law, specifically GST records for six years and E-Way Bill records for the statutory retention period.
8. For data portability requests: provide a structured export of the customer's personal data in a machine-readable format within fifteen days of the verified request. The export includes all data the customer has provided, all consent records, and all transaction records linked to the customer's identity.
9. Conduct regular privacy impact assessments for new features and data processing activities. Each assessment must identify the personal data involved, evaluate the necessity and proportionality of the processing, assess the risks to data subjects, and recommend mitigation measures for identified risks.
10. Require all employees and contractors who handle personal data to complete DPDP awareness training annually. The training covers the key provisions of the DPDP Act, the platform's data handling procedures, the consequences of non-compliance, and the incident reporting process.
11. In the event of a data breach: notify the DPDP Officer within four hours of detection. Assess the scope and impact of the breach within twenty-four hours including the number of affected individuals, the type of data exposed, and the potential harm. Notify affected individuals within seventy-two hours as required by the DPDP Act, providing clear information about what data was compromised, what steps they should take, and what the platform is doing to address the breach.
12. Conduct an annual privacy audit covering all data processing activities, consent records and their validity, access logs and their compliance with purpose limitations, masking effectiveness testing, and third-party data sharing compliance. The audit results must be reported to the DPDP Officer and the Management team with a corrective action plan for any identified gaps.

### Exceptions and Handling

Law enforcement data requests must be complied with as required by law, but each request must be documented including the requesting authority, the legal basis, the data provided, and the date of compliance. Emergency PII access without the required header is permitted only with Supervisor approval obtained within one hour of the access, and retrospective logging of the access event is mandatory. Data retention overrides beyond the standard policy require written approval from the DPDP Officer.

### Escalation Protocol

Data breaches must be reported to the DPDP Officer and Legal and Management within four hours of detection. Unauthorized PII access incidents must be reported to IT Security and HR for potential disciplinary action. Customer complaints about privacy practices must be investigated by the DPDP Officer and resolved within thirty days.

### Compliance Notes

All privacy controls must be tested quarterly for effectiveness. Consent records must be maintained for the duration of the customer relationship plus three years. Data breach notification timelines must comply with the DPDP Act requirements. The DPDP Officer must have direct access to the Management team for escalation of privacy incidents.

## SOP-020: Algorithm Rollout and Experimentation

### Purpose

This procedure ensures that all algorithm changes affecting pricing, vehicle matching, route optimization, and surge prediction are rolled out safely with controlled experimentation, continuous monitoring, and immediate rollback capability. Algorithm changes can have significant financial and operational impacts, and even small changes can produce unintended consequences at scale. This SOP implements the principle of observe, shadow, canary, controlled rollout, full launch, monitor, and rollback if necessary.

### Scope

This SOP covers all algorithm updates including pricing model changes, matching score weight adjustments, route optimization parameter tuning, surge prediction model updates, and any other algorithmic component that affects order processing, pricing, or resource allocation. Both machine learning model updates and rule-based algorithm changes are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| Engineering Team | N/A | Develops algorithm changes and implements feature flags |
| Operations Manager | N/A | Approves rollout stages and monitors operational impact |
| SUP Agent | SUP | Monitors for rollback triggers and system health |
| Product Manager | N/A | Validates business impact and customer experience |

### Pre-conditions

Algorithm change must have a clearly defined hypothesis and success metrics. Feature flag infrastructure must be in place for controlled traffic routing. Monitoring dashboards must be configured to track all rollback trigger metrics.

### Procedure

1. Define the hypothesis for the algorithm change: what specific improvement is expected, such as a five percent increase in matching efficiency or a ten percent reduction in pricing estimation error. Define the metrics that will measure success, including the primary metric directly affected and secondary metrics that should not be negatively impacted. Establish the acceptable risk threshold, which is the maximum deviation allowed in secondary metrics before a rollback is triggered.
2. Implement the algorithm change with a feature flag that allows controlled traffic routing. The feature flag must support percentage-based traffic allocation to enable gradual rollout. The implementation must include comprehensive logging of algorithm decisions for comparison with the current algorithm.
3. Deploy the algorithm in Shadow Mode where it runs in observation-only mode. The algorithm processes the same inputs as the current production algorithm and generates predictions, but its outputs are logged without being used for actual decisions. Compare shadow results with current algorithm results for a minimum of seven days to identify any systematic differences or anomalies.
4. After Shadow Mode validation, activate Canary Mode by routing five to ten percent of traffic to the new algorithm. This is the first time the algorithm affects real decisions, so close monitoring is essential. Track the following rollback triggers: duplicate offers where the same vehicle is offered to multiple orders simultaneously, transition rejection spikes where the rate of state transition failures increases, latency increase greater than fifty milliseconds compared to the current algorithm, acceptance rate collapse where the rate of match or bid acceptance drops by more than ten percent, complaint spike where customer complaints increase by more than two times the baseline, finance blocker increase where the rate of settlement blocks rises, and audit data corruption where any inconsistency is detected in the audit trail.
5. If Canary Mode is stable for seventy-two hours with no rollback triggers activated, begin the Ramp-Up phase. Increase traffic gradually: five percent to ten percent to twenty-five percent to fifty percent to one hundred percent, with a minimum of forty-eight hours at each stage before proceeding to the next.
6. At each Ramp-Up stage, verify that the settlement release success rate is unchanged from the baseline, the policy preflight pass rate is stable, customer experience metrics such as CSAT and NPS are not declining, and no audit trail corruption is detected.
7. After reaching one hundred percent traffic with stable metrics for seven consecutive days, declare Full Launch. Update the feature flag to make the new algorithm the default, and remove the old algorithm from the active code path while retaining it for emergency rollback.
8. Monitor for thirty days post-launch with weekly metric reviews. Pay particular attention to edge cases that may not have appeared during the controlled rollout, such as seasonal patterns, unusual route combinations, or peak demand scenarios.
9. If any rollback trigger is detected at any stage, immediately revert to the previous algorithm. The rollback must be executable within fifteen minutes through the feature flag. Document the root cause of the rollback trigger, implement the fix, and restart the rollout process from Shadow Mode.
10. For A/B Testing experiments, ensure statistical significance with a minimum of one thousand samples per variant. Limit the maximum test duration to fourteen days to prevent prolonged exposure to a potentially inferior variant. Test only one variable per experiment to maintain clear attribution of results.
11. Document all experiment results in the decision log with the hypothesis, the metrics measured, the statistical analysis, and the conclusion. This documentation supports future algorithm development decisions and provides an audit trail for compliance purposes.
12. Never run experiments on financial calculations, including pricing and settlement algorithms, without explicit Finance Director approval. Financial algorithms have regulatory implications under GST and Ind AS 115 that require additional scrutiny before any experimentation.

### Exceptions and Handling

Critical bugs discovered in the production algorithm bypass this rollout procedure. Deploy the hotfix immediately with retrospective review and documentation within twenty-four hours. Regulatory-mandated algorithm changes, such as GST rate updates, follow an accelerated rollout with Supervisor oversight at each stage. Emergency pricing corrections, such as correcting a misconfigured surge multiplier, are deployed immediately with canary-only monitoring for the first two hours.

### Escalation Protocol

Rollback trigger detection at any stage escalates immediately to the Engineering Lead and Product Manager for joint assessment. Finance metric impacts from algorithm changes escalate to the Finance Director for evaluation and approval. Customer complaint spikes attributed to algorithm changes escalate to the Customer Support Director and Product Manager for coordinated response.

### Compliance Notes

All algorithm changes must be documented in the decision log with full traceability. Financial algorithm changes require Finance Director approval. Rollback capability must be maintained for thirty days after full launch. Experiment results must be archived for three years for regulatory and audit purposes.

## SOP-021: Emergency and Incident Response

### Purpose

This procedure provides a structured response to critical incidents including road accidents, cargo theft, natural disasters, system outages, and security breaches. Emergency response prioritizes life safety above all other considerations, followed by scene security, evidence preservation, stakeholder communication, and operational recovery. The procedure establishes clear command structures, communication protocols, and documentation requirements for managing incidents of varying severity.

### Scope

This SOP covers all critical incidents requiring immediate response and coordination across multiple teams. Incident types include road accidents involving Zippy-assigned vehicles, cargo theft or hijacking, natural disasters affecting operations, system-wide outages, cyber security incidents, and labour disruptions. Both single-incident responses and multi-incident crisis management are within scope.

### Roles and Responsibilities

| Role | Agent Code | Responsibility |
| --- | --- | --- |
| All Agents | Various | Detect and report incidents through established channels |
| SUP Agent | SUP | Coordinates response actions and manages incident state |
| Operations Director | N/A | Takes command for Critical severity incidents |
| COMMS Agent | COMMS | Manages all stakeholder communications |
| Legal Department | N/A | Advises on legal exposure and regulatory reporting |

### Pre-conditions

Emergency contact lists must be current and accessible. Incident response team members must be identified and reachable. Business continuity plan must be documented and accessible.

### Procedure

1. Incident is detected through one of several channels: a driver emergency call or panic button activation, a TMS Agent telemetry alert indicating an accident or severe route deviation, a customer emergency report, a system monitoring alert indicating service degradation or outage, or an external notification from law enforcement, media, or regulatory authorities.
2. Classify the incident severity: Critical level includes life safety situations, major accidents, cargo theft, and system-wide outages. High level includes significant delays, partial system failures, and compliance breaches. Medium level includes isolated operational issues affecting single orders. Low level includes minor inconveniences and cosmetic issues that do not affect service delivery.
3. For Critical severity incidents: activate the emergency response team within fifteen minutes of detection. The Operations Director takes command and coordinates all response activities. The SUP Agent places immediate holds on all affected orders to prevent further downstream actions until the situation is assessed.
4. Ensure life safety as the absolute first priority: if anyone is injured in an accident, call emergency services at 112 immediately before taking any other action. Provide first aid guidance to the driver if possible and safe to do so. Do not attempt to move injured persons unless they are in immediate danger from fire, traffic, or other hazards.
5. Secure the scene after ensuring life safety: for accidents, ensure the vehicle is in a safe position with hazard lights activated and warning triangles deployed. Secure the cargo to prevent further damage or theft. Preserve all evidence including vehicle positions, road conditions, and witness information.
6. SUP Agent transitions affected orders to the INCIDENT state for tracking purposes. The INCIDENT state allows orders to be monitored separately from normal flow and enables enhanced reporting on the incident's operational impact.
7. COMMS Agent notifies all affected customers with appropriate detail about the incident without speculating on causes or assigning blame. Provide factual information about the current status, the expected impact on their shipment, and the steps being taken to resolve the situation.
8. For system outages: the IT team activates disaster recovery procedures including switching to backup systems, activating manual processes for critical operations that cannot wait for system restoration, and the SUP Agent monitors all in-flight orders for potential issues arising from the outage.
9. Document all response actions with timestamps in the exception_cases and supervisor_decisions tables. Every decision must be recorded with who made it, when, what information it was based on, and what the expected outcome was. This documentation supports post-incident analysis and any regulatory or legal proceedings.
10. Conduct a post-incident root cause analysis within seventy-two hours of the incident resolution. The analysis must identify the root cause, contributing factors, and systemic issues. Implement corrective actions to prevent recurrence, update relevant SOPs if the incident revealed procedural gaps, and file any required regulatory reports within the mandated timeframes.
11. For legal incidents: notify the Legal Department immediately. Preserve all evidence including GPS trails, communications, documents, and photographs. Do not admit liability or make commitments about compensation without Legal approval. Follow the insurance claim process, noting that Zippy's role is limited to evidence transmission and does not extend to acting as insurer, broker, or claim advisor.
12. Respect the insurance boundary: Zippy transmits evidence only, including GPS trails, POD records, and incident documentation. Zippy does NOT act as insurer, insurance broker, insurance agent, or claim advisor. Claim decisions are made by the insurance provider, and Zippy's role is limited to providing the factual evidence that supports the claim process.

### Exceptions and Handling

Natural disasters affecting multiple corridors trigger the business continuity plan, which includes suspending standard SLA metrics for the duration of the disaster, activating alternative supply networks in unaffected areas, and providing customers with honest assessments of when normal service can resume. Cyber security incidents require immediate isolation of affected systems, engagement of the cybersecurity response team, and regulatory notification if a data breach is confirmed. Labour strikes require activating alternative supply networks, notifying customers of expected delays, and engaging with the Labour Relations team for resolution.

### Escalation Protocol

Life safety situations escalate to Emergency Services at 112 immediately. Critical incidents escalate to the Operations Director within fifteen minutes. Legal exposure from incidents escalates to the Legal Department within one hour. Regulatory notifications escalate to the Compliance Officer within twenty-four hours. Media inquiries about incidents are handled exclusively by the Communications Director.

### Compliance Notes

All incidents must be documented with full evidence chains and decision trails. The insurance boundary must be respected: Zippy transmits evidence only and does not make claim decisions. Post-incident reviews must produce actionable corrective measures. Regulatory reporting timelines must be met without exception.

## Appendix A: Escalation Matrix

The following escalation matrix defines the response paths for all categories of issues encountered during operations. Each row specifies the issue category, severity level, escalation contacts at each level, and the maximum response time expected at the first escalation level. All escalation contacts must be available during their designated hours, and backup contacts must be identified for coverage during absences.

| Issue Category | Severity | First Escalation | Second Escalation | Third Escalation | Response Time |
| --- | --- | --- | --- | --- | --- |
| Order Validation | Medium | Team Lead | Operations Manager | Operations Director | 2 hours |
| Settlement Block | High | Finance Manager | Finance Director | CFO | 1 hour |
| Fraud Detection | Critical | Fraud Team | Chief Risk Officer | CEO | 30 minutes |
| Shipment Delay (Standard) | Medium | Team Lead | Operations Manager | VP Operations | 4 hours |
| Shipment Delay (Premium) | High | Manager | Operations Director | VP Operations | 2 hours |
| Shipment Delay (VIP) | Critical | VP Operations | CEO | Board | 1 hour |
| Vehicle Breakdown | High | Dispatch Manager | Operations Manager | Operations Director | 2 hours |
| POD Dispute | Medium | Customer Support Lead | Supervisor | Operations Director | 4 hours |
| Customer Complaint | Medium | Senior Support Agent | Support Manager | Customer Director | 24 hours |
| Compliance Violation | Critical | Compliance Officer | Legal Department | CEO | 1 hour |
| System Outage | Critical | IT Lead | CTO | CEO | 15 minutes |
| Data Breach | Critical | DPDP Officer | Legal + Management | Regulator | 4 hours |
| Legal Threat | Critical | Legal Department | CEO | Board | 1 hour |
| Media Risk | High | Communications Director | CEO | Board | 2 hours |

## Appendix B: Role Definitions and Agent Codes

The following table provides a comprehensive mapping of agent codes to their operational roles, functional domains, key authorized actions, and the corresponding RBAC actor roles used in the authentication system. Understanding the distinction between agent codes used for policy enforcement and actor roles used for authentication is critical for correct system operation.

| Agent Code | Role Name | Domain | Key Actions | RBAC Actor Role |
| --- | --- | --- | --- | --- |
| OMS | Order Management Agent | Order lifecycle and validation | order.transition, order.submit, order.cancel, document.validate, workflow.trigger | OMS |
| TMS | Transport Management Agent | Route planning and milestones | state.transition, route.plan, route.reroute, eta.update, shipment.milestone | TMS |
| IMS | Inventory/Matching Agent | Vehicle matching and capacity | vehicle.match, vehicle.rank, capacity.recommend | N/A |
| FIN | Finance Agent | Settlements, payments, GST | settlement.release, payment.record, invoice.generate, journal.create, gst.invoice.create | FIN |
| SUP | Supervisor Agent | Exceptions, fraud, holds | policy.check, case.hold, case.approve, case.reject, fraud.hold, settlement.hold, settlement.hold.clear | SUP |
| DISPUTE | Dispute Resolution Agent | SLA scoring and refunds | dispute.score, refund.recommend, exception.raise | N/A |
| COMMS | Communication Agent | Notifications and alerts | notification.draft, notification.trigger | N/A |
| ADMIN_OPS | Admin Operations Agent | Verification and compliance | driver.verify, audit.query, privacy.mask, compliance.check | ADMIN |

## Appendix C: Compliance Checklists

The following compliance checklists define the recurring verification activities required to maintain regulatory compliance across the platform. Each check item specifies the applicable area, the frequency of verification, the responsible agent or role, and the method used to verify compliance. These checklists should be used during monthly compliance reviews and annual audits.

| Check Item | Applicable To | Frequency | Responsible Agent | Verification Method |
| --- | --- | --- | --- | --- |
| GST invoice accuracy | All settlements | Per settlement | FIN Agent | Compare gst_invoice_records with pricing breakdown |
| E-Way Bill validity | Interstate shipments >50K INR | Per shipment | ADMIN_OPS Agent | Validate against NIC portal (simulated in MVP) |
| Revenue recognition compliance | All financial records | Monthly | Finance Admin | Validate against Ind AS 115 agent model constraint |
| Segregation of duties | Invoice generation and approval | Per transaction | Accounting Controls | SegregationOfDutiesValidator enforcement |
| DPDP consent records | All customer data | Monthly | DPDP Officer | Audit consent ledger completeness and validity |
| PII masking effectiveness | All API responses | Weekly | ADMIN_OPS Agent | Automated test suite against API endpoints |
| Fraud detection model accuracy | Fraud scoring system | Weekly | SUP Agent | Compare fraud_score outcomes with investigation results |
| Partner compliance status | All partner transporters | Monthly | ADMIN_OPS Agent | Verify insurance, fitness certificates, and licenses |
| Vehicle reservation TTL | All vehicle assignments | Per assignment | IMS Agent | Verify reservations expire correctly and release vehicles |
| State audit log completeness | All order transitions | Daily | SUP Agent | Verify all transitions logged with trace_id and idempotency_key |
| Settlement hold clearance | All settlements on hold | Daily | SUP Agent | Review active holds for timely resolution |
| Outbox event delivery | All critical events | Daily | Operations Manager | Verify events dispatched within SLA |
