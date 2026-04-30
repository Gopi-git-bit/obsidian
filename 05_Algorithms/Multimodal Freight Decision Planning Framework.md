---
title: Multimodal Freight Decision Planning Framework
type: strategy-framework
category: logistics
status: draft
region: South India
source_type: academic-model-adapted
created: 2026-04-30
tags:
  - freight
  - multimodal
  - decision-engine
  - generalized-cost
  - route-optimization
  - south-india
  - zippy-logistics
related:
  - South India Multimodal Freight Strategy
  - South India Logistics and Transportation Market Research
  - Multimodal Freight Transportation - Operational Takeaways Data Strategy
---

# Multimodal Freight Decision Planning Framework

## Purpose

This note extracts the useful decision-planning logic from an integrated multimodal freight network planning source and adapts it for a South India freight startup context.

The key idea:

> Do not plan road, rail, ports, air cargo, warehouses, and terminals separately. Treat them as one connected freight network and choose the route that gives the best reliable total cost under real constraints.

This note should support the future product logic for a South India freight decision engine.

---

## 1. Core Planning Principle

Multimodal freight planning should not start with:

```text
Which truck is available?
```

It should start with:

```text
Which combination of road, rail, port, air, warehouse, and terminal gives the lowest reliable cost for this shipment?
```

A better freight system compares multiple route and mode options before goods move.

Planning logic:

```text
Origin -> First-mile road -> Terminal / hub -> Rail / sea / air / long-haul road -> Destination terminal -> Last-mile road -> Customer
```

The goal is to reduce:

- total transport cost
- delay risk
- delivery failure
- empty return trips
- handling inefficiency
- terminal waiting time
- unnecessary road dependence

---

## 2. Main Idea From The Source

The source describes multimodal freight planning as an integrated network design problem.

Instead of planning each transport mode separately:

```text
Road plan separately
Rail plan separately
Port plan separately
Air plan separately
Warehouse plan separately
```

Use:

```text
One integrated multimodal network
```

This means road, rail, sea, air, terminals, ports, dry ports, and warehouses are treated as one connected system.

Each route option should be evaluated by:

| Factor | Meaning |
| --- | --- |
| Transport cost | Direct freight cost per tonne-km |
| Time cost | Value lost because of longer transit time |
| Delay/reliability cost | Cost caused by uncertainty, late delivery, or failure |
| Handling cost | Loading, unloading, terminal, and warehouse cost |
| Transshipment time | Time spent changing from one mode to another |
| Capacity | Maximum cargo the route or node can handle |
| Budget | Investment, operation, and maintenance limit |
| Scenario | Minimum, moderate, or high improvement option |

---

## 3. Planning Levels

## 3.1 Strategic Planning

Strategic planning decides the structure of the freight network.

| Question | Example |
| --- | --- |
| Which corridors should be prioritized? | Chennai-Bengaluru, Hyderabad-Chennai |
| Which hubs should be used? | Chennai Port, Kochi Port, Hyderabad warehouse |
| Which modes should be combined? | Road + Rail + Road |
| Which terminals need improvement? | Rail terminal, ICD, CFS, port gate |
| Which lanes deserve investment first? | High-volume, high-failure, high-cost lanes |

Use strategic planning for:

- lane selection
- terminal selection
- warehouse placement
- port connectivity
- rail feasibility
- investment planning

---

## 3.2 Tactical Planning

Tactical planning decides how the network should operate monthly or quarterly.

| Question | Example |
| --- | --- |
| Which carriers should be assigned? | Cold-chain carrier for pharma |
| How often should service run? | Daily Chennai-Bengaluru movement |
| How many trucks are required? | 20 trucks per day |
| Should shipments be consolidated? | Combine Tiruppur textile loads |
| Which mode should be default? | Road for short-haul, rail for long-haul |

Use tactical planning for:

- fleet allocation
- carrier contracts
- service frequency
- consolidation planning
- lane pricing
- customer SLA planning

---

## 3.3 Operational Planning

Operational planning decides shipment-level execution.

| Question | Example |
| --- | --- |
| Which route should this shipment take today? | Road only or road + rail |
| Is there congestion? | NH44 delay |
| Is the rail terminal available? | Yes/no |
| Is cold chain required? | 2-8 C pharma |
| Is delivery urgent? | 24 hours |
| Is backup needed? | Yes, high-value electronics |

Use operational planning for:

- daily dispatch
- route choice
- real-time tracking
- failure prevention
- delay response
- proof of delivery

---

## 4. Multimodal Network Components

A multimodal freight network has two main parts: nodes and links.

## 4.1 Nodes

Nodes are places where freight starts, stops, transfers, or is stored.

| Node Type | Example | Role |
| --- | --- | --- |
| Origin | Factory, supplier | Cargo starts |
| Destination | Customer, warehouse | Cargo ends |
| Warehouse | Chennai DC, Bengaluru DC | Storage and consolidation |
| Rail terminal | ICD, freight terminal | Road-rail transfer |
| Port | Chennai, Kochi, Vizag | Sea export/import |
| Airport | Chennai, Hyderabad, Bengaluru | Air cargo |
| Dry port / ICD | Inland container depot | Container handling |
| CFS | Container freight station | Export/import processing |

---

## 4.2 Links

Links are transport movements between nodes.

| Link Type | Example |
| --- | --- |
| Road link | Factory to terminal |
| Rail link | Chennai to Hyderabad |
| Sea link | Kochi to international port |
| Air link | Hyderabad airport to destination |
| Transfer link | Truck unloading to rail loading |
| Terminal link | Port gate to container yard |

Each link should have data attributes.

| Attribute | Meaning |
| --- | --- |
| Distance | km |
| Speed | km/hour |
| Unit cost | Rs/tonne-km |
| Handling cost | Rs/tonne |
| Transit time | hours |
| Delay percentage | % late |
| Capacity | tonnes/day |
| Reliability score | 0-100 |
| Mode | road, rail, sea, air |

---

## 5. Generalized Transport Cost

The most useful idea from the source is to calculate generalized cost, not just freight price.

```text
Generalized Cost = Transport Cost + Time Cost + Delay/Reliability Cost
```

This matters because the cheapest quoted route can still fail if it has:

- too much terminal waiting
- too many handoffs
- poor tracking
- weak carrier reliability
- high congestion
- high damage risk
- no backup route

---

## 6. Practical Cost Formula

## 6.1 Total Route Cost

```text
Total Route Cost =
Transport Cost
+ Handling Cost
+ Terminal Cost
+ Storage Cost
+ Documentation Cost
+ Delay Cost
+ Risk Buffer
```

---

## 6.2 Transport Cost

```text
Transport Cost = Distance x Weight x Mode Cost per Tonne-Km
```

Example:

```text
Distance = 600 km
Weight = 10 tonnes
Road cost = Rs 8 per tonne-km

Transport Cost = 600 x 10 x 8
Transport Cost = Rs 48,000
```

---

## 6.3 Handling Cost

```text
Handling Cost = Weight x Handling Cost per Tonne x Number of Transfers
```

Example:

```text
Weight = 10 tonnes
Handling cost = Rs 250 per tonne
Transfers = 2

Handling Cost = 10 x 250 x 2
Handling Cost = Rs 5,000
```

---

## 6.4 Time Cost

```text
Time Cost = Transit Time x Value of Time
```

Example:

```text
Transit time = 40 hours
Value of time = Rs 500/hour

Time Cost = 40 x 500
Time Cost = Rs 20,000
```

---

## 6.5 Delay/Reliability Cost

```text
Delay Cost = Expected Delay Hours x Value of Reliability
```

Example:

```text
Expected delay = 8 hours
Value of reliability = Rs 700/hour

Delay Cost = 8 x 700
Delay Cost = Rs 5,600
```

---

## 6.6 Final Generalized Cost

```text
Generalized Cost = Transport Cost + Handling Cost + Time Cost + Delay Cost
```

Example:

```text
Transport Cost = Rs 48,000
Handling Cost = Rs 5,000
Time Cost = Rs 20,000
Delay Cost = Rs 5,600

Generalized Cost = Rs 78,600
```

This is the real cost. Not just the carrier quote.

---

## 7. Timeline Planning

Every route option should be judged by total delivery timeline.

## 7.1 Road-Only Timeline

```text
Pickup time
+ loading time
+ road travel time
+ driver rest / toll / checkpost delay
+ unloading time
= total delivery time
```

Example:

| Stage | Time |
| --- | ---: |
| Pickup and loading | 3 hrs |
| Road transit | 18 hrs |
| Toll/congestion buffer | 3 hrs |
| Unloading | 2 hrs |
| Total | 26 hrs |

---

## 7.2 Road + Rail + Road Timeline

```text
Pickup time
+ first-mile road
+ terminal waiting
+ loading to rail
+ rail transit
+ destination terminal waiting
+ last-mile road
+ unloading
= total delivery time
```

Example:

| Stage | Time |
| --- | ---: |
| Pickup and loading | 3 hrs |
| First-mile road | 4 hrs |
| Origin terminal waiting | 6 hrs |
| Rail loading | 3 hrs |
| Rail transit | 14 hrs |
| Destination terminal waiting | 5 hrs |
| Last-mile road | 4 hrs |
| Final unloading | 2 hrs |
| Total | 41 hrs |

Rail may be cheaper, but terminal time can make it slower. The decision must compare cost saving against timeline risk.

---

## 7.3 Road + Port + Sea Timeline

```text
Pickup
+ road to port
+ port gate entry
+ container handling
+ vessel waiting
+ sea transit
+ destination port handling
+ last-mile delivery
= total delivery time
```

Best for:

- non-urgent heavy cargo
- export/import containers
- coastal shipping
- bulk commodities

---

## 7.4 Road + Air Timeline

```text
Pickup
+ airport feeder movement
+ security/check-in
+ flight time
+ destination airport handling
+ local delivery
= total delivery time
```

Best for:

- pharma samples
- biologics
- electronics
- urgent spare parts
- high-value lightweight cargo

---

## 8. Minimum Viable Transport Options

Do not start with every possible mode. Start with minimum viable options.

## 8.1 MVO 1: Road-Only

Use when:

| Condition | Rule |
| --- | --- |
| Distance | Less than 300 km |
| Cargo | Urgent, fragile, direct delivery |
| Terminal access | Poor |
| Shipment size | Small or irregular |
| Delivery window | Very tight |

Best for:

- Chennai-Hosur
- Hosur-Bengaluru
- Chennai-Sri City
- Coimbatore-Tiruppur
- Palakkad-Coimbatore

---

## 8.2 MVO 2: Road + Rail + Road

Use when:

| Condition | Rule |
| --- | --- |
| Distance | Above 500 km |
| Cargo | Bulk or container-compatible |
| Deadline | Flexible |
| Terminal access | Good |
| Cost saving | More than 15% |
| Transfer risk | Low or manageable |

Best for:

- Hyderabad-Chennai
- Hyderabad-Vizag
- Chennai-Vizag
- Tiruppur-Chennai Port
- Bengaluru-Chennai
- Bengaluru-Mangaluru

---

## 8.3 MVO 3: Road + Port / Coastal Shipping

Use when:

| Condition | Rule |
| --- | --- |
| Cargo | Heavy, bulk, containerized |
| Urgency | Low to medium |
| Origin/destination | Port-linked |
| Cost priority | High |
| Delivery flexibility | Available |

Best for:

- Kochi-Chennai
- Kochi-Mumbai
- Mangaluru-Chennai
- Tuticorin-Kochi
- Vizag-Chennai

---

## 8.4 MVO 4: Road + Air

Use when:

| Condition | Rule |
| --- | --- |
| Cargo value | High |
| Weight | Low/medium |
| Deadline | Strict |
| Delay cost | Very high |
| Customer priority | Premium |

Best for:

- Hyderabad pharma samples
- Chennai electronics
- Bengaluru aerospace parts
- Kochi seafood/perishables
- Tiruppur fashion samples

---

## 9. Decision Tree For Picking The Right Mode

```text
Step 1: Is shipment distance below 300 km?
    Yes -> Road-only
    No -> Go to Step 2

Step 2: Is cargo urgent or high-value?
    Yes -> Road express or Road + Air
    No -> Go to Step 3

Step 3: Is cargo bulk or container-compatible?
    Yes -> Compare Road vs Road + Rail + Road
    No -> Road or specialized carrier

Step 4: Is there good rail terminal / port access?
    Yes -> Multimodal option possible
    No -> Road-only may be better

Step 5: Is multimodal cost saving above 15%?
    Yes -> Choose multimodal if reliability is acceptable
    No -> Choose road

Step 6: Is delivery failure risk high?
    Yes -> Choose reliable route, not cheapest route
    No -> Choose lowest generalized cost
```

---

## 10. Route Option Scoring Model

Every shipment should generate at least 3 route options.

```text
Option A: Road-only
Option B: Road + Rail + Road
Option C: Road + Air or Road + Port
```

Score each option.

| Factor | Weight |
| --- | ---: |
| Cost | 30% |
| Reliability | 25% |
| Time | 20% |
| Failure risk | 15% |
| Mode fit | 10% |

Formula:

```text
Final Route Score =
(0.30 x Cost Score)
+ (0.25 x Reliability Score)
+ (0.20 x Time Score)
+ (0.15 x Failure Risk Score)
+ (0.10 x Mode Fit Score)
```

The highest score wins.

---

## 11. Cost Score

```text
Cost Score = 100 - ((Route Cost - Lowest Route Cost) / Lowest Route Cost x 100)
```

Example:

| Option | Cost |
| --- | ---: |
| Road-only | Rs 80,000 |
| Road + Rail | Rs 65,000 |
| Road + Air | Rs 140,000 |

Lowest cost = Rs 65,000.

Road + Rail gets the best cost score.

---

## 12. Reliability Score

Reliability should include:

| Reliability Variable | Weight |
| --- | ---: |
| Carrier on-time rate | 35% |
| Route delay history | 25% |
| Terminal reliability | 20% |
| Tracking visibility | 10% |
| Backup availability | 10% |

Formula:

```text
Reliability Score =
(0.35 x Carrier On-Time Score)
+ (0.25 x Route Delay Score)
+ (0.20 x Terminal Score)
+ (0.10 x Tracking Score)
+ (0.10 x Backup Score)
```

---

## 13. Failure Risk Score

Failure risk should include:

| Risk Variable | Weight |
| --- | ---: |
| Congestion risk | 20% |
| Terminal delay risk | 20% |
| Carrier cancellation risk | 15% |
| Cargo sensitivity risk | 15% |
| Documentation risk | 10% |
| Weather/disruption risk | 10% |
| Transfer complexity risk | 10% |

Formula:

```text
Failure Risk =
(0.20 x Congestion Risk)
+ (0.20 x Terminal Delay Risk)
+ (0.15 x Carrier Cancellation Risk)
+ (0.15 x Cargo Sensitivity Risk)
+ (0.10 x Documentation Risk)
+ (0.10 x Weather Risk)
+ (0.10 x Transfer Complexity Risk)
```

Lower failure risk is better.

---

## 14. Budget-Based Scenario Planning

The source uses scenarios under budget limitation. For the business, use 3 development scenarios.

| Scenario | Meaning | Investment Level |
| --- | --- | --- |
| Pessimistic | Small improvement | Low budget |
| Moderate | Practical improvement | Medium budget |
| Optimistic | Maximum improvement | High budget |

Example:

| Development Action | Pessimistic | Moderate | Optimistic |
| --- | ---: | ---: | ---: |
| Reduce road travel time | 10% | 30% | 50% |
| Reduce terminal waiting time | 10% | 30% | 50% |
| Improve tracking coverage | 30% lanes | 60% lanes | 90% lanes |
| Reduce empty miles | 5% | 15% | 30% |
| Improve on-time delivery | 5% | 15% | 25% |

---

## 15. Benefit-Efficiency Logic

Do not choose a plan only because it reduces cost. Choose the plan that gives the best benefit per rupee invested.

```text
Benefit Efficiency = Cost Saving / Investment Cost
```

Example:

| Plan | Cost Saving | Investment Cost | Benefit Efficiency |
| --- | ---: | ---: | ---: |
| Improve road route | Rs 1,00,000 | Rs 10,00,000 | 0.10 |
| Improve rail terminal | Rs 3,00,000 | Rs 15,00,000 | 0.20 |
| Add tracking system | Rs 2,00,000 | Rs 5,00,000 | 0.40 |

Best option = Add tracking system, because it gives the highest saving per rupee.

Tiny formula, giant hammer.

---

## 16. Better Decision Framework

Use this framework before choosing a freight route.

## Step 1: Define Shipment Requirement

| Field | Example |
| --- | --- |
| Origin | Hyderabad |
| Destination | Chennai Port |
| Cargo | Pharma formulations |
| Weight | 10 tonnes |
| Deadline | 48 hours |
| Temperature | 15-25 C |
| Cargo value | Rs 50 lakh |
| Export/domestic | Export |
| Failure penalty | High |

---

## Step 2: Generate Route Options

| Option | Mode Mix |
| --- | --- |
| A | Road-only |
| B | Road + Rail + Road |
| C | Road + Air |
| D | Road + Warehouse + Port |

---

## Step 3: Calculate Generalized Cost

| Option | Freight Cost | Time Cost | Delay Cost | Handling Cost | Generalized Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| A Road-only | Rs 70,000 | Rs 18,000 | Rs 8,000 | Rs 2,000 | Rs 98,000 |
| B Road + Rail | Rs 52,000 | Rs 25,000 | Rs 10,000 | Rs 8,000 | Rs 95,000 |
| C Road + Air | Rs 1,40,000 | Rs 8,000 | Rs 3,000 | Rs 4,000 | Rs 1,55,000 |
| D Road + Warehouse + Port | Rs 60,000 | Rs 30,000 | Rs 12,000 | Rs 12,000 | Rs 1,14,000 |

Lowest generalized cost = Road + Rail.

But if the delivery deadline is strict, road-only may be safer.

---

## Step 4: Score Reliability

| Option | Reliability Score |
| --- | ---: |
| Road-only | 82 |
| Road + Rail | 78 |
| Road + Air | 92 |
| Road + Warehouse + Port | 70 |

---

## Step 5: Score Failure Risk

| Option | Failure Risk |
| --- | ---: |
| Road-only | 35 |
| Road + Rail | 42 |
| Road + Air | 20 |
| Road + Warehouse + Port | 55 |

---

## Step 6: Pick Route Based On Context

| Context | Best Choice |
| --- | --- |
| Cheapest acceptable route | Road + Rail |
| Fastest route | Road + Air |
| Most reliable route | Road + Air |
| Balanced route | Road-only or Road + Rail |
| Low urgency bulk route | Road + Rail / Port |
| High-value urgent route | Road + Air |
| High failure penalty | Most reliable, not cheapest |

---

## 17. South India Application

## 17.1 Chennai-Bengaluru

| Factor | Decision |
| --- | --- |
| Distance | ~350 km |
| Cargo | Auto, electronics, FMCG, pharma |
| Current best mode | Road |
| Multimodal potential | Medium |
| Reason | Short/medium distance and high road density |
| Better service | Scheduled road, milk-run, GPS, backhaul matching |

Recommended strategy:

```text
Road-first lane with digital reliability layer
```

---

## 17.2 Hyderabad-Chennai

| Factor | Decision |
| --- | --- |
| Distance | ~630 km |
| Cargo | Pharma, FMCG, IT hardware |
| Current mode | Road + Rail possible |
| Multimodal potential | High |
| Reason | Long enough for rail comparison |
| Better service | Road + rail + cold-chain option |

Recommended strategy:

```text
Compare road-only vs road + rail for every shipment
```

---

## 17.3 Tiruppur-Chennai Port

| Factor | Decision |
| --- | --- |
| Distance | ~500 km |
| Cargo | Garments, knitwear, textiles |
| Current mode | Road + rail possible |
| Multimodal potential | High |
| Reason | Export cargo + port gateway |
| Better service | Container consolidation + port drayage |

Recommended strategy:

```text
Textile export corridor optimizer
```

---

## 17.4 Hyderabad-Vizag Port

| Factor | Decision |
| --- | --- |
| Distance | ~620 km |
| Cargo | Pharma exports, bulk chemicals |
| Current mode | Road + rail |
| Multimodal potential | High |
| Reason | Port-linked export cargo |
| Better service | Rail/road comparison + export documentation tracking |

Recommended strategy:

```text
Pharma export multimodal lane
```

---

## 17.5 Bengaluru-Mangaluru

| Factor | Decision |
| --- | --- |
| Distance | ~370 km |
| Cargo | Coffee, petroleum, containers |
| Current mode | Road + rail |
| Multimodal potential | Medium |
| Reason | Port access and commodity cargo |
| Better service | Road + rail + port planning |

Recommended strategy:

```text
Western port feeder corridor
```

---

## 18. Data To Collect For Better Decisions

## 18.1 Route Data

| Field | Why It Matters |
| --- | --- |
| Distance | Base cost and time |
| Average speed | Transit time |
| Toll cost | Road cost |
| Congestion points | Delay risk |
| Accident history | Safety risk |
| Weather disruption | Reliability |
| Road condition | Damage risk |

---

## 18.2 Terminal Data

| Field | Why It Matters |
| --- | --- |
| Loading time | Timeline |
| Unloading time | Timeline |
| Waiting time | Delay cost |
| Handling cost | Total cost |
| Damage rate | Failure risk |
| Capacity | Congestion |
| Operating hours | Scheduling |
| Documentation time | Export/import delay |

---

## 18.3 Carrier Data

| Field | Why It Matters |
| --- | --- |
| On-time delivery rate | Reliability |
| Cancellation rate | Failure risk |
| Damage rate | Cargo safety |
| Tracking availability | Visibility |
| Fleet type | Cargo fit |
| Temperature control | Pharma/seafood |
| Insurance | Risk protection |
| Backhaul availability | Cost saving |

---

## 18.4 Cargo Data

| Field | Why It Matters |
| --- | --- |
| Weight | Cost |
| Volume | Vehicle/container fit |
| Value | Risk priority |
| Fragility | Handling decision |
| Temperature need | Cold chain |
| Deadline | Mode selection |
| Export/domestic | Documentation |
| Container-compatible | Rail/sea suitability |

---

## 19. Minimum Viable Product For The Startup

## MVP Name

```text
Multimodal Freight Decision Engine
```

## MVP Scope

Start with South India only.

Initial corridors:

| Corridor | Reason |
| --- | --- |
| Chennai-Bengaluru | Highest density |
| Hosur-Bengaluru | Auto/EV frequency |
| Tiruppur-Chennai Port | Textile export |
| Hyderabad-Chennai | Pharma/FMCG |
| Hyderabad-Vizag | Pharma export |
| Bengaluru-Mangaluru | Port feeder |
| Chennai-Vizag | Bulk/container corridor |

---

## MVP Inputs

```yaml
shipment:
  origin:
  destination:
  cargo_type:
  weight_tonnes:
  volume_cbm:
  cargo_value:
  deadline_hours:
  temperature_required:
  export_or_domestic:
  container_compatible:
  priority:
    - cheapest
    - fastest
    - safest
    - balanced
```

---

## MVP Outputs

```yaml
recommendation:
  best_mode_mix:
  estimated_cost:
  estimated_time:
  generalized_cost:
  reliability_score:
  failure_risk:
  backup_route:
  nearest_terminal:
  nearest_port:
  nearest_airport:
  reason_for_choice:
```

---

## 20. Decision Output Example

```yaml
shipment_id: SI-2026-001
origin: Hyderabad
destination: Chennai Port
cargo_type: Pharma formulations
weight_tonnes: 10
deadline_hours: 48
temperature_required: 15-25C
export_or_domestic: Export
container_compatible: true
priority: Balanced

options:
  - option: A
    mode_mix: Road only
    estimated_cost: 70000
    estimated_time_hours: 30
    generalized_cost: 98000
    reliability_score: 82
    failure_risk: 35
    decision: Good if deadline is strict

  - option: B
    mode_mix: Road + Rail + Road
    estimated_cost: 52000
    estimated_time_hours: 42
    generalized_cost: 95000
    reliability_score: 78
    failure_risk: 42
    decision: Best if cost saving is priority

  - option: C
    mode_mix: Road + Air
    estimated_cost: 140000
    estimated_time_hours: 12
    generalized_cost: 155000
    reliability_score: 92
    failure_risk: 20
    decision: Best for urgent high-value cargo

final_recommendation:
  selected_option: B
  reason: Lowest generalized cost, acceptable timeline, container-compatible cargo, export-linked route.
  backup_option: A
  warning: Use Road-only if rail terminal delay exceeds 8 hours.
```

---

## 21. Practical Rulebook

| Situation | Pick |
| --- | --- |
| Short distance under 300 km | Road-only |
| Medium distance 300-500 km | Road, compare rail only if cargo is bulk/containerized |
| Long distance 500+ km | Road + Rail comparison required |
| Export cargo near port | Road + Port / Rail + Port |
| Heavy non-urgent cargo | Rail or sea |
| High-value urgent cargo | Air |
| Pharma/seafood | Cold-chain road/air |
| Auto components | Road JIT / milk-run |
| Textiles export | Road + rail + port |
| FMCG | Hub-and-spoke road network |
| High failure penalty | Reliability beats low cost |

---

## 22. Best 7-Question Framework

For every shipment, ask:

```text
1. What is the cargo?
2. How urgent is it?
3. What is the shipment value?
4. Is it container-compatible?
5. Is there a reliable rail/port/air node nearby?
6. What is the total generalized cost, not just freight quote?
7. What is the probability of delivery failure?
```

Then choose the route that gives:

```text
Lowest acceptable generalized cost
+ acceptable delivery time
+ lowest failure risk
+ backup option
```

---

## 23. Final Takeaway

The right multimodal decision is not always the cheapest route.

The right decision is:

```text
The route that delivers at the best total cost without breaking the delivery promise.
```

Road-only is simple.

Multimodal is smarter.

But multimodal only wins when the transfer points, timelines, costs, and reliability are properly planned.

The startup should become the system that makes that decision before the cargo moves.

---

## Practical Recommendation

Build the first version as a manual spreadsheet decision engine for 5 to 7 South India corridors.

Do not code the dragon yet. First prove that route scoring can beat random transporter quotes.

Recommended first corridors:

- Chennai-Bengaluru
- Hosur-Bengaluru
- Tiruppur-Chennai Port
- Hyderabad-Chennai
- Hyderabad-Vizag
- Bengaluru-Mangaluru
- Chennai-Vizag

---

## Source

- [IIETA: The Integrated Strategic Planning of Multimodal Freight Transport Network Under Infrastructure Budget Limitation](https://iieta.org/journals/ijtdi/paper/10.18280/ijtdi.070101)
- [[South India Multimodal Freight Strategy]]
- [[South India Logistics and Transportation Market Research]]
