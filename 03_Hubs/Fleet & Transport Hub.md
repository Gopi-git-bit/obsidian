---
type: hub
domain: fleet_management
status: active
tags:
  - hub
  - fleet
  - transport
region:
  - India
created: 2025-01-15
updated: 2026-04-28
---

# Fleet & Transport Hub

Central hub for all vehicle types, transport modes, fleet management, and driver operations.

## Vehicle Categories

| Category | Types | Capacity | Use Cases |
|----------|-------|----------|-----------|
| LCV | Tata Ace, Pickup | 0.5-2 ton | Last mile, small shipments |
| MCV | 2-4 axle trucks | 5-15 ton | Regional routes |
| HCV | 6+ axle trailers | 20-40 ton | Long haul, bulk |
| Specialized | Refrigerated, Hazmat | Varies | Perishable, dangerous goods |

## Warehouse Interface

External vehicle assignment should be checked against warehouse-side equipment and site constraints: dock fit, yard turning radius, forklift/reach-truck/crane availability, container/CFS readiness, and whether loading is manual, semi-automated, or WMS/WCS-driven.

## Related Child Notes

### Core Concepts (04_Concepts/)
- [[LCV vs MCV vs HCV]] - Vehicle class selection and operating profile
- [[Warehouse Vehicle and MHE Model Taxonomy]] - Warehouse-side vehicle, forklift, aisle-truck, AGV, container, and CFS handling taxonomy
- [[Warehouse Customer Strategy Canvas]] - Connects warehouse grade, material category, distribution strategy, and vehicle model
- [[Government Warehousing Standards Compliance Layer]] - Official-standard overlay for dock fit, truck body fit, palletization, CMVR/MoRTH, and warehouse readiness
- [[Closed Body Vehicle]] - Enclosed-cargo fit and protection logic
- [[Vehicle Operating Cost Model]] - Mileage, depreciation, toll, insurance, and labor cost inputs
- [[Transport Mode Selection Framework]] - Decision framework for road, rail, air, and multimodal movement
- [[Intermodal Transport Framework]] - Node, transshipment, standardization, ICT/EDI, customs, and sustainability logic for multimodal flows
- [[Transport Cost Breakdown Model]] - Full trip cost decomposition beyond only fuel and distance
- [[Transport Operations Implementation Framework]] - Practical transport operating model and system implementation guide
- [[Last-Mile Delivery Execution]] - Final-leg operating model for density, delivery-window precision, failed-attempt control, and customer-visible delivery execution
- [[Fleet vs Partner Allocation Strategy]] - Decision framework for choosing own fleet versus partner capacity
- [[Transport Fraud & Cybersecurity Framework]] - Operational fraud prevention and cyber controls for transport workflows
- [[Lane Intelligence Model]] - Corridor-level intelligence for pricing, routing, allocation, and expansion

### Scenarios (06_Scenarios/)
- [[Scenario - Vehicle Breakdown Mid-Route]] - Breakdown handling
- [[Scenario - Driver Unavailable]] - Driver availability issues
- [[Scenario - Electronics Need Closed Body Vehicle]] - Vehicle type selection
- [[Scenario - Fragile Cargo Handling Required]] - Special handling
- [[Scenario - Hazardous Material Transport]] - Hazmat compliance

### SOPs (07_SOPs/)
- [[SOP - Handle Vehicle Breakdown]] - Vehicle failure protocol
- [[SOP - Assign Secure Vehicle]] - Vehicle type matching
- [[SOP - Handle Partner Transporter]] - Partner fleet management

### Algorithms (05_Algorithms/)
- [[Fleet Allocation Algorithm]] - Vehicle-to-order matching
- [[Driver Assignment Logic]] - Driver-to-vehicle matching
- [[Route Optimization Logic]] - Route planning
- [[Warehouse Transport Correlation Algorithm]] - Correlate warehouse grade, material, lane, network strategy, and vehicle choice
- [[Delivery Attempt Management]] - Doorstep attempt readiness, recipient communication, and proof capture control
- [[IMS Matching Engine]] - Inventory-side candidate generation and reservation

### AI Agents (04_AI_Agents/)
- [[Transportation Agent]] - Route and transport coordination
- [[Resource Management Agent]] - Fleet allocation and management

### Frontend & Execution
- [[Driver App Frontend Architecture]] - Driver-side operational UI constraints

## Fleet Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Vehicle Utilization | >75% | <60% |
| Breakdown Rate | <2% | >5% |
| Driver Availability | >90% | <80% |
| On-time Departure | >95% | <90% |
| Assignment Response Time | Fast | Rising timeout rate |

## Related Hubs
- [[Operations Strategy Hub]] - Operational context
- [[AI Agents Hub]] - Fleet automation
- [[Indian Logistics Ecosystem Hub]] - Market context

---

*Maps to: [[Operations Strategy Hub]] | Part of: [[Logistics Brain - Master Index]]*
