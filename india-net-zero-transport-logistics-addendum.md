# India Net-Zero Transport & Logistics Addendum

Source file: `C:\Users\user\Downloads\Scenarios-Towards-Viksit-Bharat-and-Net-Zero-Sectoral-Insights-Transport.txt`

Validation sources:

- NITI Aayog official publication page: https://www.niti.gov.in/node/2140
- NITI Aayog report PDF: https://www.niti.gov.in/sites/default/files/2026-02/Scenarios-Towards-Viksit-Bharat-and-Net-Zero-Sectoral-Insights-Transport.pdf
- National Logistics Policy PIB release: https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1861133
- PM GatiShakti 2026 PIB update: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2225805&lang=1&reg=3
- Dedicated Freight Corridor PIB update: https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2112843
- National Green Hydrogen Mission PIB update: https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2039091

## 1. Validation Status

- The document is a real NITI Aayog publication. The official page lists `Scenarios towards Viksit Bharat and Net Zero - Sectoral Insights: Transport (Vol. 3)` with publication date February 9, 2026.
- Treat it as a scenario and planning report, not binding policy. The report itself says it is not a policy statement and that readers should independently verify data before commercial decisions.
- Use the report for long-range logistics strategy, energy transition assumptions, freight modal shift thinking, and clean-fuel architecture.
- Do not use it as the only source for current project counts, incentives, or legal compliance because those numbers can change quickly.

## 2. Where This Information Belongs

- Put freight modal shift, clean freight, DFC, MMLP, waterways, pipelines, hydrogen, LNG, CBG, and SAF points into the logistics strategy/playbook.
- Put EV charging, hydrogen pilots, clean-fuel corridors, and fleet transition into transport technology architecture.
- Put multimodal logistics parks, rail-water-road integration, and PM GatiShakti into intermodal transport strategy.
- Put logistics-cost benchmarks into `KNOWLEDGE.md` because they affect pricing, routing, and platform positioning.
- Put port, ICD/CFS, inland waterway, railway terminal, MMLP, and cold-chain infrastructure mapping into `india-logistics-infrastructure-ports-intermodal.md`.
- Do not put passenger mobility details into warehouse operations except where they affect urban delivery access, EV charging, or city freight restrictions.

## 3. Validated Logistics Context

- India transport is road-heavy. The report estimates 2025 freight transport at about 4,661 BTKM, with road carrying about 66%, rail 22%, waterways 8%, pipelines about 3.6-4%, and air freight near zero.
- Passenger transport is also road-heavy. The report estimates 2025 passenger travel at about 6,410 BPKM, with road at 78%, rail 17%, air 4%, and metro about 1%.
- Transport accounted for about 20% of final energy demand and about 10% of India GHG emissions in 2020, according to the report.
- A separate DPIIT/NCAER logistics-cost assessment reported India logistics cost at about 7.97% of GDP in 2023-24. This updates the older commonly quoted 13-14% figure, which should now be treated carefully as legacy or externally estimated.
- National Logistics Policy targets a technologically enabled, integrated, cost-efficient, resilient, and sustainable logistics ecosystem, including cost reduction toward global benchmarks, LPI improvement, and data-driven decision support.

## 4. Current Policy/Infrastructure Updates

- PM GatiShakti: the report mentions 434 projects worth INR 11.17 lakh crore. A newer PIB update from February 10, 2026 says the Network Planning Group had evaluated 352 projects worth INR 16.10 lakh crore. Use the newer number when discussing current status.
- Dedicated Freight Corridors: PIB reported on March 19, 2025 that 2,741 route km out of 2,843 km, or 96.4%, had been commissioned and operational across the Eastern and Western DFCs.
- Gati Shakti Multi-Modal Cargo Terminals: PIB reported 97 commissioned GCTs and 277 in-principle approvals.
- National Green Hydrogen Mission: PIB confirms an outlay of INR 19,744 crore and a target of 5 MMT/year green hydrogen production by 2030.

## 5. Strategic Implications for the Startup

### 5.1 Build for Multimodal Freight, Not Only Truck Brokerage

The startup should not position itself only as a truck-matching layer. India’s long-term direction is multimodal:

- Road for first-mile, last-mile, urgent loads, fragmented lanes, and flexible service.
- Rail for long-haul bulk, containers, lower-cost freight, and decarbonized trunk movement.
- Waterways/coastal shipping for low-cost bulk and port-linked corridors.
- Pipelines for fuel, gas, CBG/hydrogen-compatible future networks, and selected slurry/bulk flows.
- Air only for high-value, time-critical cargo.

Product requirement:

- Add `mode_chain` to shipment planning: `truck -> rail -> truck`, `truck -> port -> ship -> truck`, `truck -> pipeline-compatible terminal`, etc.
- Add lane-level modal alternatives instead of only road quotation.

### 5.2 Add Modal Shift Intelligence

For every lane, calculate:

- Road-only cost
- Road-only ETA
- Rail/intermodal cost
- Rail/intermodal ETA
- Water/coastal option where available
- Emission estimate
- Handling risk
- Reliability score
- First-mile and last-mile friction
- Minimum viable shipment size

Decision rule:

- Road wins when speed, flexibility, small loads, or direct delivery matter.
- Rail/intermodal wins when volume, distance, cost, and emissions matter.
- Water wins when cargo is non-urgent, bulky, and corridor access exists.

### 5.3 Freight Energy Transition Roadmap

Segment freight vehicles by transition path:

- Light commercial vehicles: electrification first.
- Urban delivery and high-utilization fleets: EV charging/swapping priority.
- Medium trucks: CNG/CBG bridge, electric where routes are predictable.
- Heavy long-haul trucks: LNG as bridge fuel, hydrogen/fuel-cell pilots, battery-electric on fixed corridors as charging improves.
- Cold chain: electrified reefer monitoring, energy-efficient routing, charging at warehouses and distribution centers.

System fields to add:

- `fuel_type`
- `emission_class`
- `ev_range_km`
- `charging_compatibility`
- `cng_lng_cbg_compatibility`
- `hydrogen_ready`
- `route_charging_available`
- `clean_fuel_score`

### 5.4 Clean-Fuel Corridor Planning

Create a `corridor_energy_profile` table:

```sql
corridor_energy_profile(
  corridor_id,
  origin,
  destination,
  distance_km,
  ev_charging_nodes,
  battery_swapping_nodes,
  cng_stations,
  lng_stations,
  cbg_nodes,
  hydrogen_refueling_nodes,
  rail_terminal_access,
  port_or_waterway_access,
  clean_fuel_readiness_score
)
```

Use this to decide whether a shipment can be assigned to EV, CNG/CBG, LNG, hydrogen, rail, or conventional diesel.

### 5.5 Multimodal Logistics Park Strategy

MMLPs should be treated as strategic nodes in the network graph.

For each MMLP/logistics hub track:

- Road access
- Rail terminal access
- Port/waterway access
- Warehouse/cross-dock capacity
- Container handling
- Cold-chain support
- Customs/bonded capability
- EV charging
- Clean-fuel availability
- Average dwell time
- Handling cost
- Reliability score

Use MMLPs for:

- Consolidation
- Cross-docking
- Rail-road transfer
- Long-haul modal shift
- Backhaul creation
- Empty return reduction

### 5.6 Pricing Implication

The startup pricing engine should not assume road is always the default cheapest option.

Quote engine should compare:

- Road direct
- Road + rail + road
- Road + coastal/water + road
- Road + MMLP consolidation
- Delayed delivery using lower-cost mode
- Premium clean-freight option

Add customer-facing quote categories:

- Fastest
- Cheapest
- Lowest emission
- Most reliable
- Best balanced

## 6. Scenario Data Useful for Planning

Use these as assumptions, not certainties:

- Freight rail share may rise from 22% in 2025 to 25% under Current Policy Scenario and 30% under Net Zero Scenario by 2070.
- Road freight share may decline from 66% in 2025 to about 60% under Net Zero Scenario by 2070.
- Transport energy demand under Net Zero Scenario is projected around 192-200 Mtoe by 2070, materially lower than the Current Policy Scenario.
- Petroleum share in transport energy may fall sharply under the Net Zero Scenario, with electricity, biofuels, hydrogen, green ammonia, and e-methanol gaining importance.
- Hydrogen is most relevant for heavy-duty freight, shipping, and other hard-to-electrify movement.

## 7. Product Features to Add Later

- Carbon-aware quoting
- Green freight score per shipment
- EV route feasibility check
- Rail/intermodal recommendation engine
- MMLP node selection engine
- Clean-fuel corridor map
- Backhaul and modal shift optimizer
- Customer option to choose lower-emission delivery
- Fleet transition advisory for transporters
- Government-infrastructure watchlist for DFCs, MMLPs, GCTs, ports, and hydrogen corridors

## 8. Caution Notes

- Do not treat 2070 scenario outputs as forecasts. They are modelled pathways.
- Do not rely on the report’s PM GatiShakti project count as current. Use the newer PIB update.
- Biofuel scale-up has supply-chain uncertainty because feedstock availability and land-use competition were outside the report scope.
- Infrastructure investment costs in the report exclude several major categories such as road/rail expansion, aviation, metro, LNG facilities, and hydrogen filling stations, so total transition capital needs are understated for startup infrastructure planning.
