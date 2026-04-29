# India Logistics Infrastructure: Ports, ICD/CFS, Waterways, Rail, and MMLPs

Source file: `C:\Users\user\Downloads\RSM India Publication - The Logistics Navigator 2025.txt`

Validation sources:

- RSM India publication page: https://www.rsm.global/india/insights/logistics-navigator-2025
- RSM India PDF: https://www.rsm.global/india/sites/default/files/media/publications/2025/RSM%20India%20Publication%20-%20The%20Logistics%20Navigator%202025.pdf
- PIB major ports FY 2024-25 update: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2128329&lang=1&reg=3
- PIB PM GatiShakti update: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2225805&lang=1&reg=3
- PIB DFC/Gati Shakti Cargo Terminal update: https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2112843

## 1. How to Use This Document

Use this file as an infrastructure intelligence layer for the logistics startup. It should support:

- Port-aware shipment planning
- Import/export routing
- Coastal shipping decisions
- ICD/CFS selection
- Rail-road intermodal routing
- MMLP node selection
- Inland waterway opportunities
- Cold-chain and warehouse placement
- Customs and documentation workflow planning

Do not use this file as a legal compliance source. Exact port statistics, customs rules, and government project status should be refreshed from official sources before financial or operational commitments.

## 2. Validation Notes

- The RSM document is a real 2025 publication and is useful as a compiled logistics infrastructure navigator.
- RSM states that the navigator is compiled from public and subscribed sources. Treat it as a secondary research document.
- One caution: the RSM text states major ports handled about 843 MT in 2023-24, while official/PIB updates use about 819 MT for FY 2023-24 and about 855 MT for FY 2024-25. For exact headline statistics, use official government releases.
- Use RSM mainly for infrastructure categories, state/port patterns, operational interpretation, and node-mapping ideas.

## 3. Core Infrastructure Map

The Indian logistics network should be modelled as a multi-layer graph:

- Seaports: major ports, non-major ports, deep-water ports, transshipment ports.
- ICD/CFS/AFS nodes: inland container depots, container freight stations, air freight stations.
- Inland waterways: National Waterways, floating terminals, jetties, Ro-Ro/Ro-Pax services.
- Rail corridors: HDN, HUN, Dedicated Freight Corridors, Gati Shakti Cargo Terminals.
- MMLPs: multi-modal logistics parks connecting road, rail, ports, warehousing, and value-added services.
- Airports and air cargo terminals.
- Warehouses, cold stores, logistics parks, FTWZs, and customs-bonded infrastructure.

Product implication:

```text
Shipment request
-> origin/destination geography
-> cargo type and containerization
-> port/ICD/CFS candidates
-> road/rail/water alternatives
-> cost/time/reliability comparison
-> documentation and customs workflow
-> selected mode chain
```

## 4. Ports: Operational Insights

India’s port system is not one market. It is a set of specialized regional gateways.

Key categories:

- Major ports: central-government ports handling large national and international traffic.
- Non-major ports: state/private ports with strong regional and industrial linkages.
- Coastal cargo ports: useful for domestic movement where road/rail alternatives are congested or costly.
- Overseas cargo ports: useful for EXIM traffic and global supply chains.
- Container ports: essential for manufactured goods, electronics, retail, ecommerce imports, and export cargo.
- Bulk ports: coal, iron ore, petroleum, fertilizers, agri commodities, cement, minerals.
- Transshipment ports: strategic for hub-and-spoke container movement and reducing dependence on foreign transshipment hubs.

Startup use cases:

- Recommend ports based on cargo type, origin/destination, port congestion, customs handling, hinterland connectivity, and container availability.
- Build port scorecards with capacity, utilization, commodity fit, container capability, coastal capability, transshipment capability, and rail connectivity.
- Track port-specific commodity shocks, such as export bans, coal surges, iron ore demand, petroleum movement, or container route changes.

## 5. Port Selection Score

For each shipment, score possible ports:

```text
port_score =
  hinterland_distance_score
+ rail_connectivity_score
+ road_connectivity_score
+ container_availability_score
+ cargo_specialization_score
+ capacity_utilization_score
+ customs_speed_score
+ coastal_shipping_option_score
+ transshipment_access_score
+ reliability_score
- congestion_penalty
- documentation_risk_penalty
- weather_or_disruption_penalty
```

Minimum fields:

```sql
ports(
  port_id,
  port_name,
  state,
  port_type,
  major_or_non_major,
  cargo_specialization,
  container_teu_capacity,
  bulk_capacity_mt,
  coastal_cargo_support,
  overseas_cargo_support,
  transshipment_support,
  rail_connectivity,
  road_connectivity,
  nearby_icd_cfs,
  capacity_utilization,
  average_dwell_time,
  customs_capability,
  reliability_score
)
```

## 6. Important Port Patterns from the RSM Document

- Port cargo has grown over recent years across both major and non-major ports.
- Non-major ports are especially important for coastal cargo and state-led industrial logistics.
- Gujarat dominates non-major port cargo, especially overseas cargo, because of its industrial base and port infrastructure.
- Andhra Pradesh, Maharashtra, Odisha, Tamil Nadu, and Gujarat should be treated as strategic maritime logistics states.
- Paradip, Deendayal, JNPT/JNPA, Visakhapatnam, Chennai, Mumbai, Kamarajar, V.O. Chidambaranar, Cochin, New Mangalore, Mormugao, and Syama Prasad Mookerjee/Kolkata-Haldia are important major-port nodes.
- JNPT/JNPA remains critical for containerized cargo and western India EXIM.
- Paradip is important for coal, iron ore, and bulk cargo.
- Deendayal/Kandla is strategically important for western bulk and liquid cargo.
- Visakhapatnam and Chennai are important eastern/southern gateways.
- Kamarajar and V.O. Chidambaranar are important for southern industrial and coastal flows.

## 7. Upcoming and Strategic Port Nodes

Track these as strategic future nodes:

- Vadhvan Port, Maharashtra: mega deep-draft/container port; important for western India, large vessels, and JNPT decongestion.
- Vizhinjam, Kerala: deep-water international container transshipment port; important for reducing dependence on Colombo/Singapore/Salalah-type foreign transshipment.
- Tajpur, West Bengal: potential eastern deep-water/transshipment capability.
- Machilipatnam, Andhra Pradesh: regional coastal and agricultural export support.
- Dighi Port, Maharashtra: multipurpose port upgrade potential.
- Kattupalli expansion, Tamil Nadu: container/transshipment and southern logistics relevance.
- Great Nicobar/Galathea Bay-type strategic transshipment concepts should be watched separately with official status checks.

Product implication:

- Build `future_node_status`: planned, approved, under construction, trial operations, commercial operations, delayed, regulatory pending.
- Do not price live routes through future ports until commercial service, customs, road/rail connectivity, and liner calls are confirmed.

## 8. ICD and CFS Layer

ICDs and CFSs are inland extensions of port logistics.

Use cases:

- Customs clearance away from congested seaports.
- Container stuffing and de-stuffing.
- Consolidation and deconsolidation.
- Rail-road container transfer.
- Export staging near production clusters.
- Import distribution closer to consumption centers.

Architecture:

```sql
icd_cfs_nodes(
  node_id,
  node_name,
  node_type,
  state,
  operator_type,
  nearest_port,
  rail_connected,
  road_connected,
  customs_available,
  bonded_storage_available,
  container_yard_capacity,
  reefer_plug_capacity,
  export_import_focus,
  average_clearance_time,
  congestion_score
)
```

Decision rule:

- Use CFS near ports when port-adjacent consolidation or deconsolidation is needed.
- Use ICD inland when cargo originates far from the port, rail movement is viable, and customs clearance should happen closer to factory/warehouse clusters.
- Use AFS for air cargo where airport congestion or inland cargo preparation is important.

## 9. Inland Waterways and Coastal Shipping

The RSM navigator emphasizes 111 notified National Waterways and the development of key corridors.

Use waterways/coastal shipping for:

- Bulk cargo
- Non-urgent cargo
- Heavy/oversized cargo where feasible
- Coal, minerals, cement, fertilizer, agri cargo, and selected container flows
- Corridors with terminal and draught reliability

Important design variables:

- Navigability seasonality
- Draught availability
- Terminal/jetties
- Road/rail access to water terminal
- Cargo handling equipment
- Transit time reliability
- First-mile and last-mile cost
- Barge/container availability
- Weather and river condition risk

RORO/Ro-Pax implication:

- Ro-Ro and ferry links can reduce road distance, driver time, fuel cost, and congestion.
- Add ferry/Ro-Ro legs into the routing graph where operating service exists.

## 10. Railway Terminals, HDN, HUN, and DFCs

Rail is central to lower-cost long-haul logistics.

Key concepts:

- HDN: High-Density Network, the busiest railway routes, including Golden Quadrilateral-style corridors and diagonals.
- HUN: High-Utilization Network, important revenue and freight routes connected to industrial, port, and commercial hubs.
- DFC: Dedicated Freight Corridors, designed to separate freight from passenger congestion and improve freight speed, reliability, and capacity.
- Gati Shakti Cargo Terminals: rail cargo terminals intended to improve terminal access and mechanized loading/unloading.

Validated update:

- PIB reported that 2,741 route km out of 2,843 km of EDFC/WDFC, or 96.4%, had been commissioned and operational by March 19, 2025.
- PIB also reported 97 Gati Shakti Cargo Terminals commissioned and 277 in-principle approvals.

Startup use cases:

- Recommend rail for long-haul containers and bulk where terminal access is practical.
- Use DFC proximity as a lane advantage.
- Score rail terminals by distance, rake availability, container support, cargo specialization, turnaround, and last-mile road access.

## 11. MMLP Layer

MMLPs should be treated as high-value network nodes, not just warehouses.

Functions:

- Road-rail-port integration
- Container handling
- Warehousing
- Cross-docking
- Cold-chain integration
- Value-added services
- Customs/bonded support where available
- Consolidation and deconsolidation
- Long-haul mode shift

Benefits:

- Lower logistics cost
- Lower urban congestion
- Better route consolidation
- Lower inventory holding cost
- Industrial cluster support
- Regional development
- Better freight visibility

MMLP table:

```sql
mmlp_nodes(
  mmlp_id,
  location,
  state,
  development_status,
  road_access,
  rail_access,
  port_access,
  airport_access,
  warehouse_capacity,
  container_yard_capacity,
  cold_chain_available,
  customs_or_bonded_support,
  value_added_services,
  target_industries,
  nearest_industrial_corridor,
  clean_fuel_infrastructure,
  reliability_score
)
```

## 12. Cold Chain and Perishable Logistics

RSM notes cold-chain inefficiencies, regional imbalance, underutilization, and insufficient refrigerated vehicles.

Operational implications:

- Cold storage alone is not enough; the weak link is often transport, pre-cooling, handling discipline, and route timing.
- Build cold-chain lanes by commodity, not only by geography.
- Track reefer vehicle availability, cold-room temperature class, loading dock temperature control, and dwell time.
- Prioritize farm-gate aggregation, packhouses, reefer transport, urban cold stores, and pharma-compliant traceability.

Fields:

```sql
cold_chain_assets(
  asset_id,
  asset_type,
  location,
  temperature_range,
  capacity,
  utilization,
  backup_power,
  reefer_dock,
  pharma_grade,
  food_grade,
  monitoring_available,
  owner_operator
)
```

## 13. Digital Infrastructure and ULIP

RSM highlights ULIP as a logistics digital integration layer under the National Logistics Policy.

Platform implication:

- Design the startup architecture for API-based logistics data exchange.
- Build adapters for vehicle, shipment, port, rail, customs, e-way bill, FASTag/toll, and tracking data as they become available.
- Keep a data-governance layer because infrastructure data from public/private sources will vary in quality.

Suggested modules:

- Infrastructure node registry
- Lane registry
- Multimodal routing engine
- Customs/document workflow
- Port/terminal status tracker
- Clean-fuel corridor layer
- Cost and ETA engine
- Exception and delay monitor

## 14. Strategic Product Features

- Port recommendation engine
- ICD/CFS recommendation engine
- Rail vs road vs coastal shipping quote comparison
- Port congestion and dwell-time dashboard
- Container availability tracker
- MMLP selection engine
- DFC proximity score
- Cold-chain lane planner
- Customs-document checklist by shipment type
- Coastal shipping feasibility check
- Transshipment route advisor
- Infrastructure watchlist for upcoming ports, MMLPs, ICDs, GCTs, and waterways

## 15. Where This Fits With Existing Files

- `startup-logistics-playbook.md`: high-level strategy and logistics intelligence.
- `india-net-zero-transport-logistics-addendum.md`: net-zero, modal shift, clean fuels, freight energy transition.
- `warehouse-distribution-advanced-architecture.md`: WMS/TMS/warehouse execution.
- This file: physical infrastructure layer for ports, ICD/CFS, waterways, rail terminals, and MMLPs.

## 16. Main Takeaway

The logistics platform should become an infrastructure-aware operating system.

Not:

`customer asks for truck -> find truck`

But:

`customer asks for movement -> choose best node chain, mode chain, clearance path, cost path, and service path`

That is the difference between a freight broker and a logistics intelligence platform.

