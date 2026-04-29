---
type: concept
domain: warehousing
decision_value: high
status: evergreen
related_hubs:
  - Operations Strategy Hub
  - Fleet & Transport Hub
  - Technology Stack Hub
tags:
  - concept
  - warehouse
  - material-handling
  - vehicle-types
  - mhe
---

# Warehouse Vehicle and MHE Model Taxonomy

## Purpose

Define the warehouse-side vehicle and material-handling equipment models that should be captured when profiling a warehouse, assigning vehicles, estimating dock turnaround, or deciding whether a site can support a specific cargo flow.

## Core Distinction

Warehouse vehicles are not the same as road freight vehicles.

| Category | Operating Zone | Platform Meaning |
|----------|----------------|------------------|
| Internal warehouse vehicles / MHE | Inside warehouse, yard, rack aisles, staging area | Determines handling speed, aisle fit, dock productivity, storage density, and cargo restrictions |
| External transport vehicles | Public roads, port/CFS routes, intermodal legs | Determines pickup/drop capacity, body type, permits, freight cost, compliance, and ETA |
| Intermodal/container equipment | Ports, CFS, rail/road interfaces, container yards | Determines whether cargo can move across road, rail, ship, and air without repacking |

## Aisle-Based Lift Truck Models

| Model / Class | Typical Aisle Fit | Use Case | System Signal |
|---------------|-------------------|----------|---------------|
| Wide aisle truck / counter-balanced forklift | Wider than 11 ft | General pallet movement, loading/unloading, standard warehouse handling | Faster general handling but lower storage density |
| Narrow aisle truck | 8-10 ft | Double-deep storage, stand-up reach movement, tighter storage layouts | Requires aisle-width and reach capability fields |
| Very narrow aisle truck | Less than 6 ft | High-density racking with guided travel | Requires guidance type, rack compatibility, and trained operator signal |
| Stand-up reach truck | Narrow aisle | Pallet putaway/retrieval in racking | Useful for medium/high-density warehouse scoring |
| Double-deep reach truck | Narrow aisle | Deep pallet storage where selectivity is lower | Raises handling complexity and retrieval sequencing needs |
| Turret truck | Very narrow aisle | In-aisle picking and pallet handling in dense storage | Strong signal for high-density warehouse capability |
| Order picker | Narrow/VNA picking aisles | Person-up picking for piece/case operations | Indicates e-commerce, spare-parts, or high-SKU workflows |

## Walkie And Manual Equipment

| Equipment | Use Case | Platform Signal |
|-----------|----------|-----------------|
| Pallet jack | Short-distance pallet movement and basic dock work | Minimum viable MHE for small warehouses and godowns |
| Hand truck | Carton, parcel, and small-load movement | Manual handling, low automation, lower throughput |
| Walkie reach stacker | Affordable narrow-aisle pallet handling | Good for small storage areas that need more than manual flow |
| Walkie straddle stacker | Pallet stacking where straddle support is needed | Useful for small warehouses with racking but limited capital equipment |
| Walkie counter-balanced stacker | Flexible stacking without full forklift footprint | Useful where aisle width or cost limits standard forklifts |
| Stand-up straddle truck | Bridge between narrow and wide aisle handling | Mid-capability signal for regional warehouses |

## Automated Warehouse Vehicles

| Equipment | Use Case | Platform Signal |
|-----------|----------|-----------------|
| Automated guided vehicle (AGV) | Floor automation coordinated by WCS/WMS | High automation maturity; needs traffic zones and system integration |
| Rack entry vehicle | Deep-lane AS/RS and shuttle-style storage | High-density storage; retrieval timing depends on automation availability |
| Man-on-board AS/RS / order-picking truck | In-aisle picking and storage/retrieval | Strong signal for controlled, system-driven warehouse execution |

## External Transport Vehicles To Capture

| Vehicle / Mode | Warehouse Interface | Use Case |
|----------------|--------------------|----------|
| LCV | Small docks, city routes, tight access | Parcel, small shipment, local distribution |
| MCV | Regional docks and mixed-load distribution | Regional replenishment and medium-load movement |
| HCV | Large yard/dock, higher turning radius, highway access | Long-haul FTL, bulk, heavy cargo |
| Truck and trailer | Large-scale inbound/outbound and intermodal handoff | Consolidated loads, door-to-door delivery, port/CFS movement |
| Refrigerated truck / reefer | Cold storage dock and temperature-controlled staging | Pharma, dairy, seafood, frozen food, perishable cargo |
| Tanker | Liquid cargo handling and safety controls | Chemicals, edible oils, liquid products |
| Customs bonded truck | CFS/port/customs-sealed movement | Sealed cargo transfer between freight stations, ports, and bonded nodes |
| Rail, ship, air | Intermodal network | Long-distance movement where warehouse connects to terminal, CFS, port, or airport |

## Containerization And CFS Implications

Containerized freight changes warehouse and vehicle requirements:

- Cargo can move across road, rail, ship, and air without opening the container.
- Standard ISO containers need compatible handling equipment, yard space, and terminal/CFS workflows.
- Containers reduce pilferage and manual handling, but require capital-intensive infrastructure, cranes or container handlers, and enough land for stacking/repositioning.
- Empty or half-empty repositioning is a cost and planning problem that should feed return-load and intermodal optimization.
- Container Freight Stations handle customs, container deconsolidation, temporary storage, and port decongestion; they need road/rail connectivity and enough layout space for vehicle/container movement.

## Data Fields To Add To Warehouse Profiles

| Field | Why It Matters |
|-------|----------------|
| `aisle_width_class` | Determines whether WA, NA, or VNA trucks can operate |
| `mhe_types_available` | Captures forklifts, reach trucks, pallet jacks, AGVs, cranes, stackers, and order pickers |
| `forklift_capacity_kg` | Prevents assigning loads that cannot be safely handled |
| `dock_mhe_ready` | Signals whether loading/unloading can start immediately |
| `automation_level` | Distinguishes manual, semi-automated, WMS/WCS-driven, AGV/ASRS-enabled sites |
| `container_handling_ready` | Indicates whether the site can handle containerized freight or CFS-like operations |
| `yard_turning_radius_ok` | Prevents HCV/trailer assignment to physically constrained sites |
| `customs_bonded_flow` | Triggers bonded documentation and sealed vehicle handling |
| `operator_skill_required` | Captures need for forklift, VNA, hazmat, reefer, or AS/RS-trained operators |

## Government Standard Overlay

Use [[Government Warehousing Standards Compliance Layer]] to validate MHE and vehicle-interface assumptions against the DPIIT-WAI warehousing standards source.

Important source-derived transport checks:

- Palletized truck body movement should consider clear internal width around `2286 mm`.
- LCV, MCV, HCV, container trailer, and reefer assignments should be checked against dock height, dock width, and apron depth.
- Truck bodies should support suitable rear or side loading where forklift/BOPT loading is expected.
- Truck/trailer flooring should be robust enough for palletized movement where BOPT or forklift entry is part of the operating model.

## Assignment Logic

```text
If warehouse has only manual handling,
  avoid heavy palletized cargo unless shipper provides loading support.

If aisle_width_class = VNA,
  require compatible VNA/turret/reach capability for internal handling assumptions.

If cargo is containerized or bonded,
  require container/CFS readiness, customs documents, and suitable external vehicle.

If cargo is cold-chain,
  require cold dock readiness, reefer vehicle fit, and temperature-control proof.
```

## Related Notes

- [[Warehouse Execution & Intelligence Framework]]
- [[Inventory-Driven Resource Allocation Framework]]
- [[LCV vs MCV vs HCV]]
- [[Closed Body Vehicle]]
- [[Transport Mode Selection Framework]]
- [[Transport Logistics and Warehousing Knowledge Map]]

## Source Seed

Derived from `C:\Users\user\Downloads\warehouse an logistic.txt`, summarized into vault-ready operating concepts.
