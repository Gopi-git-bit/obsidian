---
type: market-intelligence
domain: market_intelligence
decision_value: high
status: raw-scrape
region: Tamil Nadu
source_date: 2026-04-26
source_batches: 4+
related_hubs:
  - Market Intelligence Hub
  - Indian Logistics Ecosystem Hub
tags:
  - market-intelligence
  - tamil-nadu
  - chennai
  - warehousing
  - logistics-parks
  - transport-companies
  - autoclaw
---

# Tamil Nadu Warehouse and Logistics Market Scan

## Research Context

This note captures the Tamil Nadu warehouse and logistics database generated on 2026-04-26 across multiple scrape/research/import batches. Sources include Tavily Search, TNAU, D&B, company websites, and local listing sources. Treat this as a raw market-intelligence layer until field verification, phone validation, and current availability checks are completed.

## Database Snapshot

| Table | Records | Coverage |
|-------|---------|----------|
| companies | 76 | Logistics parks, 3PL/4PL/4.5PL providers, cold chain, e-commerce fulfillment, express/courier, government, industry associations, textile logistics, port logistics, on-demand warehousing |
| facilities | 36 | Specific warehouse locations with sqft, corridor, grade, including 18 cold storage units from the TNAU government directory |
| corridors | 15 | Chennai Metro, Chennai-Oragadam-Sriperumbudur, Hosur-SIPCOT, Coimbatore-Tiruppur, Madurai, Trichy, Salem, Thoothukudi Port, Tiruppur Textile Belt, Erode Textile Cluster, Namakkal Transport Hub, Vellore Industrial, Cuddalore-Nagapattinam, Southern TN, Thanjavur Delta |
| warehouse_pricing | 19 | Chennai warehouse rental records from MagicBricks, Stockarea, and RealEstateIndia |
| fulfillment_centers | 2 | Amazon FBA MAA4 at Puduvoyal/Thiruvallur and CJB1 at Coimbatore |
| district_stats | 31 | Warehousing company density across 31 of 38 Tamil Nadu districts |
| local_transport | New table | Association members, local transporters, fleet owners, online truck booking platforms, and industry bodies |
| godown_listings | New table | Private godown/warehouse rental listings from MagicBricks for Chennai and Trichy |
| district_deep_dive | New/expanded table | District-level logistics profiles, hubs, routes, industries, fleet estimates, and insights |
| tn_policy_corridors | New table | TN Logistics Policy corridor priorities and truck lay-bye phase signals |

### Database Fields Captured

| Table | Important Fields |
|-------|------------------|
| companies | name, type, parent_company, founded_year, CIN, hq_address, tn_locations, industries_served, services, total_warehouses, total_sqft, employees, website, phone, email, key_contacts, key_clients, notes, data_source |
| facilities | name, location, district, address, corridor, facility_type, total_sqft, available_sqft, specialization, certification |
| corridors | corridor name, region, dominant industry/traffic pattern, logistics relevance |
| warehouse_pricing | location, source, grade, sqft, rent per sqft/month, notes |
| fulfillment_centers | operator, code, location, district, fulfillment role |
| district_stats | district, company density/count, relative opportunity signal |
| local_transport | name, owner_name, city, district, address, phone, WhatsApp, email, vehicle_types, services, association, role_in_association, fleet_size, turnover, routes, specialization, notes, data_source |
| godown_listings | owner_name, location, district, size_sqft, rent_per_month, road_width_ft, property_age, furnishing, floor, features, notes, listed_date, source |
| district_deep_dive | district, city, state, logistics_profile, key_hubs, major_industries, transport_routes, warehouse_clusters, fleet_size_estimate, local_transport_companies, truck_body_building, key_insights, data_source |
| tn_policy_corridors | corridor_name, phase, priority, districts_covered, notes, source |

## Initial Thesis

Tamil Nadu's logistics opportunity is concentrated around Chennai consumption zones, the Sriperumbudur-Oragadam industrial corridor, Redhills/Thiruvallur warehousing clusters, Poonamallee-Irungattukottai gateway routes, Coimbatore/Tiruppur textile and manufacturing belts, and selected underserved districts with low warehousing density. The strongest near-term wedge for Zippy is not only large Grade A parks, but the operating gap between large logistics infrastructure and fragmented local transport supply.

## Strategic Signals

| Signal | Why It Matters |
|--------|----------------|
| Grade A supply is expanding around Chennai | Large park operators are creating dense warehouse nodes that need transport connectivity |
| Redhills is emerging as a fast-growth distribution hub | FMCG, e-commerce, 3PL, and D2C demand can create repeat local and regional lanes |
| Sriperumbudur remains auto/electronics-heavy | Strong B2B freight density and supplier ecosystems support recurring loads |
| Poonamallee links city freight with industrial corridors | Useful gateway for Chennai-Oragadam-Sriperumbudur movements |
| Local warehousing data is fragmented | Justdial/Sulekha-style leads need direct validation before sales outreach |
| Database covers 31 of 38 Tamil Nadu districts | The scrape is broad enough to compare mature hubs against underserved districts |
| Chennai pricing varies sharply by warehouse grade | Grade A+ can reach around Rs.63/sqft/month while standard facilities appear around Rs.13-16/sqft/month |
| Low-density districts may be expansion whitespaces | Perambalur, Tiruvarur, Ramanathapuram, and Nagapattinam show lower warehousing company density |
| Thoothukudi is a port-led logistics node | VOC Port adjacency creates export/import, coastal shipping, customs, and port-warehouse use cases |
| Western TN has textile-led freight density | Coimbatore, Tiruppur, Erode, and Karur create repeat textile, garment, processing, and export logistics demand |
| Namakkal is a trucking capability cluster | Truck body building, driver training, and transport operator density make it important for supply-side onboarding |
| Local transporter associations expose supply nodes | CGTA Coimbatore, Chennai Goods Transport Association, and Madurai lorry associations provide structured entry points into fragmented supply |
| Koyambedu remains a dense Chennai transport hub | Multiple Justdial/IndiaMART transporter leads cluster around Koyambedu and can support first-mile/line-haul onboarding |
| Private godown listings reveal small-market leasing signals | MagicBricks godown leads in Chennai and Trichy help benchmark informal/private warehouse availability |
| Cold chain is a distinct Chennai/Coimbatore/Salem opportunity | Pharma, dairy, seafood, vaccines, frozen food, and agri perishables need tighter SLA and temperature-control workflows |
| Amazon FCs anchor e-commerce demand | MAA4 in Puduvoyal/Thiruvallur and CJB1 in Coimbatore are useful demand signals for fulfillment and middle-mile mapping |
| Southern TN has multiple specialized freight pockets | Trichy engineering, Madurai distribution, Tirunelveli cement/wind, Sivakasi fireworks, Thoothukudi port, Theni spices, and Kanyakumari marine/wind all create different operating requirements |
| TN policy corridors validate lane priority | Hosur-Chennai, Coimbatore-Tuticorin, Hosur-Coimbatore, Coimbatore-Chennai, and Chennai-Kanyakumari provide government-backed corridor signals |

## Key Quantitative Insights

### Chennai Warehouse Pricing

| Grade | Indicative Rent |
|-------|-----------------|
| Grade A+ | Around Rs.63/sqft/month |
| Grade A | Around Rs.25/sqft/month |
| Standard | Around Rs.13-16/sqft/month |

Pricing sources in the scrape include MagicBricks, Stockarea, and RealEstateIndia. These numbers are directionally useful for market sizing but should be refreshed before pricing decisions because warehouse rents can change quickly by road access, clear height, power, dock quality, and leasing term.

### Top Company-Type Signals

| Company Type | Count / Signal |
|--------------|----------------|
| Cold chain | 13 companies |
| 3PL | 9+ companies |
| Logistics parks | 6 companies |
| Industry associations | 6 entries |
| Express/courier | 3 companies |

### District Density Signals

| District | Warehousing Company Density |
|----------|-----------------------------|
| Chennai | 350 |
| Kanchipuram | 200 |
| Coimbatore | 180 |
| Madurai | 150 |
| Tiruppur | 137 |
| Vellore | 132 |
| Namakkal | 130 |
| Cuddalore | 128 |
| Erode | 120 |
| Tiruvannamalai | 120 |
| Virudhunagar | 114 |
| Salem | 110 |
| Thanjavur | 100 |
| Trichy | 100 |
| Krishnagiri | 95 |
| Kanyakumari | 92 |
| Dharmapuri | 91 |
| Thoothukudi | 90 |
| Tirunelveli | 85 |
| Sivaganga | 83 |
| Dindigul | 80 |
| Chengalpattu | 75 |
| Pudukkottai | 74 |
| Viluppuram | 73 |
| Karur | 60 |
| Sivakasi | 58 |
| Theni | 58 |

### Underserved District Signals

| District | Density | Why It Matters |
|----------|---------|----------------|
| Perambalur | 28 | Low-density market that may need aggregation and discovery |
| Ramanathapuram | 39 | Southern TN coverage gap with potential regional logistics need |
| Tiruvarur | 42 | Delta-adjacent district where agri/logistics demand may be underserved |
| Nagapattinam | 50 | Coastal/delta logistics opportunity with comparatively low density |

## Database Operations Note

- PostgreSQL host recorded from Railway public endpoint: `metro.proxy.rlwy.net:19786`
- Database name: `railway`
- No credentials are stored in this note.
- Pasted import scripts included a full PostgreSQL connection URL with password. Rotate the Railway credential before sharing scripts or committing anything anywhere.

### Latest Import Batch Captured

| Import Area | Rows In Script | Destination Table | Notes |
|-------------|----------------|-------------------|-------|
| Chennai-region facilities | 12 | `facilities` | Uses `ON CONFLICT DO NOTHING RETURNING id`; source label `Tavily 2026-04-26` |
| Warehouse clusters | 5 | `warehouse_clusters` | Inserts Sriperumbudur, Redhills, Poonamallee-Irungattukottai, Koyambedu-Madhavaram, and Guindy-Siruseri |
| Facility district count | Query output | `facilities` | Groups facilities by district after insert |
| Total facilities count | Query output | `facilities` | Prints final table count after insert |
| Regional expansion companies | 15 | `companies` | Adds Thoothukudi port, western TN textile/3PL, pan-TN express, D&B, Erode, and Namakkal leads |
| Regional corridors | 8 | `corridors` | Adds Thoothukudi Port, Tiruppur Textile Belt, Erode Textile Cluster, Namakkal Transport Hub, Vellore Industrial, Cuddalore-Nagapattinam, Southern TN, and Thanjavur Delta |
| Regional facilities | 7 | `facilities` | Adds Thoothukudi, Erode, Salem, and Trichy warehouse/logistics leads |
| District warehousing density | 31 | `district_stats` | Creates/upserts district-level company density and specialization from D&B/Tavily |
| Local transport table | DDL | `local_transport` | Creates table for association members, transport companies, fleet owners, online platforms, and industry bodies |
| CGTA Coimbatore members | 25 | `local_transport` | Captures association leadership and member transport companies from CGTA Coimbatore |
| Chennai/Madurai associations | 3 | `local_transport` | Adds Chennai Goods Transport Association and Madurai Lorry Owners Association entries |
| Local transport companies | 32 | `local_transport` | Adds Koyambedu, Chennai, Cuddalore, Trichy, Salem, Erode, Tiruppur, digital platform, and AIMTC leads |
| Godown listings table | DDL | `godown_listings` | Creates table for private warehouse/godown rental listings |
| Private godown listings | 6 | `godown_listings` | Adds MagicBricks listings from Chennai and Trichy |
| Warehouse cluster reset/rebuild | Destructive DDL + 5 rows | `warehouse_clusters` | Drops `warehouse_clusters`, recreates schema, reinserts 5 Chennai-region cluster rows, then prints facility counts by district |
| Cold-chain/company batch | 15 | `companies` | Adds cold chain, government warehousing, e-commerce fulfillment, express, agri, association, on-demand warehousing, and 3PL leads |
| TNAU cold storage facilities | 18 | `facilities` | Adds cold storage capacity records across Chennai, Coimbatore, Salem, Madurai, Trichy, Virudhunagar, Thiruvallur, and Perumballur/Perambalur spelling variant |
| Warehouse pricing records | 19 | `warehouse_pricing` | Adds MagicBricks, RealEstateIndia, Stockarea, and ChennaiProperties records with computed rent/sqft when possible |
| Amazon fulfillment centers | 2 | `fulfillment_centers` | Adds Amazon MAA4 at Puduvoyal/Thiruvallur and CJB1 at Coimbatore |
| Southern/central TN local transport leads | 29 | `local_transport` | Adds Trichy, Madurai, Tirunelveli, Sivakasi/Virudhunagar, Thoothukudi, Theni, Kanyakumari, Namakkal, and pan-India platform entries |
| District deep dives | 9 | `district_deep_dive` | Adds Trichy, Madurai, Tirunelveli, Sivakasi, Virudhunagar, Dindigul, Thoothukudi, Theni, and Kanyakumari profiles |
| TN policy corridors | 5 | `tn_policy_corridors` | Adds Phase 1 and Phase 2 Logistics Policy corridor priorities from TIDCO/TN Logistics Policy 2023 |
| Warehouse cluster enrichment | 5 | `warehouse_clusters` | Re-inserts/enriches Chennai-region clusters with fuller notes, player/tenant details, and final coverage summary |
| Warehouse cluster insert test | 1 temporary row | `warehouse_clusters` | Test script attempts insert/delete cleanup, but SQL has 17 target columns and only 16 placeholders; add `$17` for `data_source` |

The latest batch is an executable database seed/import script, but the Obsidian record should store only sanitized metadata, table shapes, and market insights. Keep passwords, full connection strings, and raw secrets out of the vault.

### Warehouse Cluster Rebuild Note

The latest cluster script uses `DROP TABLE IF EXISTS warehouse_clusters` before recreating the table. This is useful for resetting a malformed schema, but it will delete any previously added cluster rows beyond the 5 hardcoded Chennai-region clusters.

| Rebuilt Cluster | District | Approx. Sq Ft | Notes |
|-----------------|----------|---------------|-------|
| Sriperumbudur Industrial Corridor | Kanchipuram | 5,000,000 | Auto/electronics/logistics cluster; NH-48; SIPCOT/auto anchor signal |
| Redhills Warehouse Hub | Thiruvallur | 4,300,000 | FMCG/e-commerce/3PL hub; SH-114, NH-16, ORR |
| Poonamallee-Irungattukottai | Thiruvallur/Kanchipuram | 1,500,000 | Gateway to Oragadam and Irungattukottai/SIPCOT |
| Koyambedu-Madhavaram | Chennai | 800,000 | Transport/urban warehouse cluster; fragmented local supply |
| Guindy-Siruseri-Okkiyam | Chennai/Kanchipuram | 600,000 | IT/industrial/3PL cluster along OMR/GST Road |

Before running this script again, either export existing `warehouse_clusters` rows or replace the destructive reset with upserts keyed by `cluster_name`.

## Companies And Park Operators

| Company | Type | Tamil Nadu Locations | Scale | Services | Notes | Source |
|---------|------|----------------------|-------|----------|-------|--------|
| Hiranandani Industrial Parks | Logistics Park | Redhills, Mannur-Sriperumbudur, Sethupakkam | 2.0 Mn sq ft at Redhills plus 60 acres | Grade A warehousing, built-to-suit, industrial space, AI/IoT smart warehousing | House of Hiranandani legacy, 3 Chennai-area parks, IGBC Gold certified at Redhills | hiranandaniindustrialparks.com; Tavily 2026-04-26 |
| Pragati Warehousing | Logistics Park | Sriperumbudur | 1,617,644 sq ft | Grade A industrial and logistics, ready-to-move, built-to-suit | Backed by large Asia PE fund; 12m clear height; 7t/sqm load capacity; NFPA fire safety | pragatiwarehousing.com; Tavily 2026-04-26 |
| Ramanujar Industrial and Logistics Parks | Logistics Park | Pillaipakkam/Sriperumbudur, Thally | 6.8 lakh sq ft at Pillaipakkam; 4.8 lakh sq ft at Thally | Grade A warehousing, built-to-suit, logistics park | TVS Infra Trust/Jagannath Industrial Parks; EDGE certified; near NH-4; solar capable | tvsinfratrust.com; Tavily 2026-04-26 |
| Siruvapuri Murugan Industrial and Logistics | Logistics Park | Thamaraipakkam/Redhills | 11.2 lakh sq ft | Grade A warehousing, logistics park | TVS Infra Trust asset; 33.18 acres; 36km from Chennai Port; 14km from NH-16 | tvsinfratrust.com; Tavily 2026-04-26 |
| ACME Warehousing | Warehousing | Chennai | 55,000 sq ft | Warehouse space, supply chain solutions | Since 2010; small team | goodfirms.co; Tavily 2026-04-26 |
| Sanjay Forwarders Pvt Ltd | Freight Forwarding/Warehousing | Chennai | Unknown | Freight forwarding, warehousing | Needs verification | goodfirms.co; Tavily 2026-04-26 |
| Aakarsh Air and Sea Freight Forwarders | Freight Forwarding | Chennai | Unknown | Air freight, ocean freight, customs clearance, marine insurance, distribution | Since 2018; 50-249 employees | goodfirms.co; Tavily 2026-04-26 |

## Regional Expansion Company Leads

| Company | Type | Tamil Nadu Locations | Services / Industry | Notes | Source |
|---------|------|----------------------|---------------------|-------|--------|
| Tuticorin Logistics | Port Logistics | Thoothukudi | Port logistics, warehousing, coastal shipping, freight forwarding | Near V.O. Chidambaranar Port; phone/email captured in database | tutlog.in; Tavily 2026-04-26 |
| Cargocare Logistics | Freight Forwarding/3PL | Thoothukudi, Chennai | Freight forwarding, customs, warehousing, port logistics | Tuticorin branch contact captured in database | cargocarelogistics.in; Tavily 2026-04-26 |
| Surmount Logistics Solutions | 3PL | Thoothukudi | Logistics, warehousing, freight, supply chain | Regional Manager South India based in Thoothukudi | LinkedIn; Tavily 2026-04-26 |
| Navata SCS | 3PL | Coimbatore | 3PL, warehousing, transportation, distribution, reverse logistics | 40+ years; 400+ GPS vehicles; 670+ South India branches | navatascs.com; Tavily 2026-04-26 |
| SRD Logistics | 3PL | Pan-TN | Warehousing, distribution, surface transport | 50+ years; strong in textile logistics | srdlogistics.com; Tavily 2026-04-26 |
| Velocity Express | Express/Courier/3PL | Pan-TN | B2B courier, B2C delivery, freight, same-day, hyperlocal | All 38 Tamil Nadu districts covered | velexp.com; Tavily 2026-04-26 |
| Fit 3PL Warehousing Pvt Ltd | 3PL | Tamil Nadu | Warehousing | D&B listed warehousing company | dnb.com; Tavily 2026-04-26 |
| Isuzu Logistics India Pvt Ltd | 3PL | Chennai | Freight forwarding, contract logistics | D&B listed | dnb.com; Tavily 2026-04-26 |
| SICAL Multimodal and Rail Transport | Port Logistics/Multimodal | Chennai | Multimodal transport, rail freight, port logistics, warehousing, CFS | Major port logistics player | dnb.com; Tavily 2026-04-26 |
| SANCO Trans Limited | 3PL/Transport | Chennai | Transport, logistics, warehousing | D&B listed transport/logistics player | dnb.com; Tavily 2026-04-26 |
| Asia Crystal Commodity LLP | Warehousing/Trading | Erode | Commodities, trading | D&B listed | dnb.com; Tavily 2026-04-26 |
| Krishna Textile Process | Textile Logistics | Erode | Textile processing, warehousing | SIPCOT Industrial Estate, Erode | Scribd Erode Directory; Tavily 2026-04-26 |
| Ezhil Exports | Textile/Export | Erode | Export logistics, warehousing | Sathiyamangalam textile/garment lead | Scribd Erode Directory; Tavily 2026-04-26 |
| Make Easy Logistics | 3PL | Erode | Logistics, warehousing, transport | Erode local logistics lead | Scribd Erode Directory; Tavily 2026-04-26 |
| Ashok Leyland Driver Training Institute | Training/Logistics | Namakkal | Driver training, logistics education | Trains 20,000 drivers annually per source note | KPMG White Paper; Tavily 2026-04-26 |

## Cold Chain, Fulfillment, And Institutional Leads

| Company | Type | Tamil Nadu Locations | Services / Industry | Notes | Source |
|---------|------|----------------------|---------------------|-------|--------|
| Chennai Cold Logistics | Cold Chain | Chennai | Temperature-controlled transport, cold-chain logistics, refrigerated trucking, vaccine transport | Pharma, dairy, frozen foods, seafood, vaccines, perishables; contact captured in database | chennaicoldlogistics.in; Tavily 2026-04-26 |
| TMT Cold Storage | Cold Chain | Chennai/Manali | Automated cold storage, temperature-controlled storage, food management, HACCP support | Founded 2016; 51-200 employees; Manali cold-storage signal | LinkedIn; Tavily 2026-04-26 |
| Snowman Logistics | Cold Chain | Chennai | Temperature-controlled warehousing, cold-chain distribution | Gateway Distriparks group; pharma/food/perishables | Tavily 2026-04-26 |
| SFC Cold Chain Logistics | Cold Chain | Chennai | Cold-chain transportation, temperature-controlled delivery | Pharma, food, perishable goods | sfccoldchainlogistics.in; Tavily 2026-04-26 |
| Tamilnadu Warehousing Corporation | Government | Chennai/Guindy | Government warehousing, storage | Government-owned warehousing entity | Justdial; Tavily 2026-04-26 |
| NimbusPost Fulfillment | E-commerce Fulfillment | Chennai | Fulfillment, pick and pack, same-day/next-day delivery, multi-channel fulfillment | 3 lakh+ sq ft across 14+ FCs; contact captured in database | nimbuspost.com; Tavily 2026-04-26 |
| Warehousing Express Logistics | E-commerce Fulfillment/3PL | Chennai/Mevalurkuppam | Seller Flex-ready warehousing, Amazon/Flipkart optimized fulfillment, WMS | 25+ years; optimized for marketplace SLAs | warehousingexpress.com; Tavily 2026-04-26 |
| Blue Dart Express | Express/Courier | Chennai/Nungambakkam | Express logistics, air freight, courier, warehousing | National express/courier benchmark | bluedart.com; Tavily 2026-04-26 |
| Godrej Agrovet | Agri/Warehousing | Chennai/Ambattur | Agri warehousing, food-processing storage | Agri/food-processing storage signal | Justdial; Tavily 2026-04-26 |
| CII Institute of Logistics | Industry Association | Chennai/Taramani | Training, events, skill development, advisory | Key institutional logistics knowledge and training node; contacts captured in database | ciilogistics.com; Tavily 2026-04-26 |
| Warehousing Association of India | Industry Association | National | Advocacy, standardization, warehouse rating, geo-tagging, networking | Useful policy/standards body for warehouse quality frameworks | warehousingindia.org; Tavily 2026-04-26 |
| Stockarea | On-Demand Warehousing | Chennai/Keelameni, Periyapalayam, Sriperumbudur | Verified warehouse listings, on-demand warehousing | Useful benchmark for marketplace-style warehouse discovery | stockarea.io; Tavily 2026-04-26 |
| Emiza | 3PL/E-commerce Fulfillment | Chennai | Middle-mile logistics, warehousing, e-commerce fulfillment | Technology-driven fulfillment player | emizainc.com; Tavily 2026-04-26 |
| CCI Logistics Industrial Park | Logistics Park | Not TN-specific in script | Warehouse development, logistics park | Included as national logistics park benchmark; TN relevance needs validation | IWLS Catalog 2019; Tavily 2026-04-26 |
| Om Logistics | 3PL/Express | Ambur, Coimbatore, Puducherry | Transportation, warehousing, freight forwarding | Regional network signal; contact captured in database | omlogisticssupplychain.com; Tavily 2026-04-26 |

## Facilities And Warehouse Leads

| Facility | Company | Location | District | Corridor | Approx. Scale | Specialization | Notes |
|----------|---------|----------|----------|----------|---------------|----------------|-------|
| Pragati Industrial and Logistics Park | Pragati Warehousing | Sriperumbudur | Kanchipuram | Chennai-Oragadam-Sriperumbudur | 1,617,644 sq ft | Auto, EMS, logistics, manufacturing | 32,292 to 1,617,644 sq ft available; 12m height; 7t/sqm load; 10 free units |
| Ramanujar Industrial and Logistics Park | Ramanujar/TVS Infra | Pillaipakkam | Kanchipuram | Chennai-Oragadam-Sriperumbudur | 680,000 sq ft | Industrial, warehousing, logistics | 17 acres; 2km from NH-4; dock levelers; 5t/sqm floor load |
| Hiranandani Industrial Park Mannur | Hiranandani Industrial Parks | Mannur-Sriperumbudur | Kanchipuram | Chennai-Oragadam-Sriperumbudur | Unknown | Smart warehousing, manufacturing | AI and IoT-enabled operations |
| Hiranandani Industrial Park Redhills | Hiranandani Industrial Parks | Redhills | Thiruvallur | Chennai Metro | 2,000,000 sq ft | FMCG, e-commerce, 3PL, warehousing | 82 acres; NH-16 and ORR connectivity; IGBC Gold |
| Hiranandani Industrial Park Sethupakkam | Hiranandani Industrial Parks | Sethupakkam | Thiruvallur | Chennai Metro | Unknown | Industrial, warehousing | Part of Hiranandani Chennai network |
| Siruvapuri Murugan Industrial and Logistics Park | TVS Infra Trust | Thamaraipakkam | Thiruvallur | Chennai Metro | 1,120,000 sq ft | FMCG, e-commerce, 3PL | 33.18 acres; 46km airport; 36km port; 14km NH-16 |
| IndoSpace Vishnuvakkam | IndoSpace | Vishnuvakkam | Thiruvallur | Chennai Metro | 1,045,760 sq ft | Automobile, electronics, FMCG, 3PL | 48 acres on SH-114 Redhills-Tiruvallur Highway |
| IndoSpace Mevalurkuppam Industrial Park | IndoSpace | Mevalurkuppam | Thiruvallur | Chennai-Oragadam-Sriperumbudur | 428,838 sq ft | Industrial, warehousing, logistics | Off NH-48; near Irungattukottai SIPCOT and Hyundai; hazardous and non-hazardous land use |
| Sri Ramajayam Road Lines Warehouse | Sri Ramajayam Road Lines | Poonamallee | Thiruvallur | Chennai Metro | Unknown | Warehousing, transport | 24-hour operation; Sulekha lead |
| Pooja Freight Carrier Warehouse | Pooja Freight Carrier | Poonamallee | Thiruvallur | Chennai Metro | Unknown | Warehousing, freight | 24-hour operation; Sulekha lead |
| Narendra Enterprises Warehouse | Narendra Enterprises | Poonamallee | Thiruvallur | Chennai Metro | Unknown | Warehousing, distribution | 121 Justdial ratings |
| SSK Smart Move Logistics Warehouse | SSK Smart Move Logistics Pvt Ltd | Poonamallee area | Thiruvallur | Chennai Metro | Unknown | Logistics, warehousing | 17 Justdial ratings |
| Tuticorin Logistics Warehouse | Tuticorin Logistics | Thoothukudi | Thoothukudi | Thoothukudi Port | Unknown | Port logistics, export/import, warehousing | Port-adjacent lead |
| Cargocare Logistics Tuticorin | Cargocare Logistics | Thoothukudi | Thoothukudi | Thoothukudi Port | Unknown | Freight forwarding, customs, warehousing | Script spelling used `Toothukudi`; normalize to Thoothukudi during cleanup |
| Sarvam Logistics Thoothukudi | Sarvam Logistics | Thoothukudi | Thoothukudi | Thoothukudi Port | Unknown | Warehousing, project cargo, distribution | Registered MTO, multimodal transport |
| Krishna Textile Process SIPCOT | Krishna Textile Process | Erode | Erode | Erode Textile Cluster | Unknown | Textile processing, warehousing | SIPCOT Industrial Estate |
| Make Easy Logistics Warehouse | Make Easy Logistics | Erode | Erode | Erode Textile Cluster | Unknown | General warehousing, transport | Erode local lead |
| Stockarea Salem Warehouse | Stockarea | Salem | Salem | Salem | Unknown | On-demand warehousing, 3PL | Needs current availability validation |
| Stockarea Trichy Warehouse | Stockarea | Trichy | Trichy | Trichy | Unknown | On-demand warehousing, 3PL | Needs current availability validation |

## TNAU Cold Storage Facilities

| Facility | Location | District | Capacity / Size Field | Items | Notes |
|----------|----------|----------|-----------------------|-------|-------|
| Raja Cold Storage | Ariyalur | Perumballur | 3,500 | Multipurpose | District spelling should be normalized against Perambalur |
| Tamil Nadu Coop Marketing Fed Ltd | Chennai | Chennai | 2,000 | Multipurpose | Government/cooperative cold-storage signal |
| Adi Sakthi Cold Storage Pvt Ltd | Mettupalayam | Coimbatore | 5,000 | Multipurpose | Coimbatore cold-chain node |
| Kolar Cold Storage | Jedayampalayam | Coimbatore | 4,500 | Multipurpose | Coimbatore cold-chain node |
| Palamudir Cold Storage | Chinnayampalayam | Coimbatore | 500 | Multipurpose | Coimbatore cold-chain node |
| Ranga Lalitha Cold Storage | Shevapet | Salem | 2,000 | Multipurpose | Salem cold-chain node |
| Vidya Bharathi Cold Storage | Madhavaram | Thiruvallur | 5,500 | Multipurpose | Chennai-north/Thiruvallur cold-chain node |
| Garden Fresh Cold Storage | Allampatti | Madurai | 2,500 | Multipurpose | Madurai cold-chain node |
| Sri Ayyappa Hitech Cold Storage Ltd | Jadayampalayam | Coimbatore | 5,000 | Multipurpose | Coimbatore cold-chain node |
| EmpeeBee Exports & Imports | Ambattur | Thiruvallur | 3,000 | Multipurpose | Ambattur/Thiruvallur spelling normalized from script |
| Fazil Cold Storage | Trichy | Trichy | 4,400 | Multipurpose | Trichy cold-chain node |
| Elumalai Cold Storage Pvt Ltd | Rajapalayam | Virudhunagar | 2,320 | Multipurpose | Southern TN cold-chain node |
| Sree Bishnu Potato Cold Storage Ltd | Bellathi Village | Coimbatore | 7,000 | Multipurpose | Largest capacity record in this TNAU batch |
| Tamil Nadu Cold Storage SF No. 10/2-5 | Paranattamangalam | Salem | 5,300 | Multipurpose | Salem cold-chain node |
| Maruthi Ice and Cold Storage | Saidapet | Chennai | 40 | Fish, meat | Small urban cold-storage signal |
| Inter Sea Exports Corporation | T Nagar | Chennai | 250 | Marine products | Seafood/export-adjacent signal |
| Pukharaj Mohanlal | Chennai | Chennai | 25 | Dry fruits | Small specialty storage signal |
| Department of Racing | Guindy | Chennai | 12 | Multipurpose | Public-sector record in source |

## Warehouse Clusters

| Cluster | Area | District | Type | Parks | Approx. Sq Ft | Grade | Rent Range | Growth |
|---------|------|----------|------|-------|---------------|-------|------------|--------|
| Sriperumbudur Industrial Corridor | Sriperumbudur-Oragadam | Kanchipuram | Auto, electronics, logistics | 6 | 5,000,000 | Grade A | Rs.25-30/sqft/month | Rapidly growing |
| Redhills Warehouse Hub | Redhills-Thamaraipakkam | Thiruvallur | FMCG, e-commerce, 3PL | 4 | 4,300,000 | Grade A | Rs.13-25/sqft/month | Rapidly growing |
| Poonamallee-Irungattukottai | Poonamallee-Mevalurkuppam-Irungattukottai | Thiruvallur/Kanchipuram | Industrial, warehousing | 3 | 1,500,000 | Grade A | Rs.22-42/sqft/month | Growing |
| Koyambedu-Madhavaram | Koyambedu-Madhavaram-Perambur | Chennai | Transport, urban warehouse | 2 | 800,000 | Standard to Grade B | Rs.13-20/sqft/month | Stable |
| Guindy-Siruseri-Okkiyam | Guindy-Siruseri-Okkiyam Thoraipakkam | Chennai/Kanchipuram | IT, industrial, 3PL | 2 | 600,000 | Grade A-B | Rs.25-40/sqft/month | Stable to growing |

## Regional Corridors Added

| Corridor | Key Areas | Specialization | Strategic Meaning |
|----------|-----------|----------------|-------------------|
| Thoothukudi Port | Thoothukudi, Tuticorin, VOC Port | Port logistics, export/import, coastal shipping, container traffic | Gateway for international trade on Tamil Nadu's southeast coast |
| Tiruppur Textile Belt | Tiruppur, Erode, Karur | Textiles, garments, knitwear, home textiles | Dense repeat freight from India's knitwear export hub |
| Erode Textile Cluster | Erode, Sathiyamangalam, Bhavani, Perundurai | Textile processing, dyeing, yarn, garment manufacturing | Processing and export support hub with SIPCOT relevance |
| Namakkal Transport Hub | Namakkal, Tiruchengode, Paramathi-Velur | Truck body building, transport, driver training | Supply-side onboarding and fleet ecosystem node |
| Vellore Industrial | Vellore, Ranipet, Gudiyatham, Katpadi | Automotive components, leather, manufacturing | Northern industrial corridor with D&B density signal |
| Cuddalore-Nagapattinam Corridor | Cuddalore, Nagapattinam, Chidambaram, Neyveli | Industrial, power, agriculture, port | Coastal agriculture/industry corridor with underserved pockets |
| Southern TN Corridor | Tirunelveli, Kanyakumari, Tenkasi, Nagercoil | Agro-processing, marine products, wind energy, manufacturing | Southern coverage expansion and marine/agri logistics |
| Thanjavur Delta | Thanjavur, Tiruvarur, Nagapattinam, Kumbakonam | Agriculture, agro-processing, food storage, cold chain | Cauvery delta cold-chain and food logistics opportunity |

## Local Transport Supply Layer

This batch adds the unorganized and semi-organized carrier ecosystem that sits underneath the larger logistics park and warehouse market. Individual phone numbers and personal contacts are kept in the database/source layer, not repeated in this Obsidian note.

### Associations Captured

| Association | City | Signal | Notes |
|-------------|------|--------|-------|
| Coimbatore Goods Transport Association | Coimbatore | 25 member/office-bearer records | Includes chairman, advisors, trustees, officers, executive committee members, and transport company representatives |
| Chennai Goods Transport Association | Chennai | Association HQ record | Poonamallee High Road location; useful for Chennai transporter network discovery |
| Madurai Lorry Owners Association | Madurai | 2 association/branch records | Keerathurai and Chitrakkara Street leads from local directories |
| All India Motor Transport Congress | National / South India relevance | Industry body | Apex transport body; useful for policy, association mapping, and trucker network context |

### Chennai And Koyambedu Transport Leads

| Segment | Example Leads | Strategic Use |
|---------|---------------|---------------|
| Koyambedu transporters | Drop Truck, Sree Siddhi Vinayaka Logistics, VBN Logistics, Good Wheel Transport, PaceRoute Logistics, Om Sai Transport, Periya Transport | Local carrier discovery around Chennai's transport nerve center |
| Chennai fleet/FTL operators | Sree Jayam Trans, Power Logistics, AK Cargo Solution, Wehaul Logistics, Rapiditors Logistics, Shaik Transport, Rajasthan Roadlines, Ahluwalia Trans Logistics, Federal Transport | FTL/PTL onboarding, rate discovery, vehicle-type mapping |
| Digital truck booking platforms | FR8 India, Truckwaale | Competitive/partner benchmark for online booking, GPS tracking, and platform-led supply |

### Regional Transport Leads

| Region | Example Leads | Notes |
|--------|---------------|-------|
| Cuddalore | Veera Transports | 10-12 wheel truck signal, per-ton rate signal, GPS tracking claim |
| Trichy | SS Transport Carrier Co | Goods transport/FTL, long operating history |
| Salem | SPN Road Transport Service | Road transport, FTL/PTL, full and part loads |
| Erode/Tiruppur | Moving Goods Escort Transportation, Sky Land Xpress Cargo, Shakthy Transolutions, Texcity Cargo Carriers, Kavi Logistics, Agaram Transport Service, Sri Senthil Raja Road Lines, Surya Traders | Textile/agri/industrial goods carrier discovery; several rate and years-in-business signals |
| Pan-India platforms | Vahak, Trukky | Competitive benchmark for marketplace liquidity, online load booking, and rate transparency |

### Southern And Central TN Transport Leads

| District / City | Example Leads | Strategic Signal |
|-----------------|---------------|------------------|
| Trichy | HurryUp Cabs and Transport, SKVR Logistics, Blessing Cargo, Flywing Balaji Logistics, Shree Enterprises, Thunaivan Transport, YSH Logistics, Team Trans Logistics, Sarvam Logistics | Central TN distribution, BHEL/engineering cargo, containers, chemicals, hospital goods, app-based booking |
| Madurai | Vegin Global Express, TNTA, DTDC, Blue Dart, Delhivery, ST Courier | Southern TN hub with courier/express/logistics concentration and association presence |
| Tirunelveli | AKR Express | Next-day parcel/delivery signal; Justdial volume suggests deeper transporter market |
| Sivakasi/Virudhunagar | Jairanga Transport, Pandivel Transport | Fireworks corridor signal; hazardous-goods compliance is the core filter |
| Thoothukudi | Sarvam Logistics, Tuticorin Logistics Pvt Ltd | Port, customs, FCL/LCL, project cargo, RORO, door-to-door and container/bulk demand |
| Theni/Kanyakumari | MJ Packers Movers, Jairanga Transport Nagercoil | Kerala gateway, agri/spice/marine cross-border and southern-tip routes |
| Cross-district | AKR Express, Trukky Southern TN | Parcel/online booking benchmark and Kanyakumari base-rate signal |

## District Deep Dives

| District | Profile | Fleet Estimate | Important Hubs / Industries | Key Insight |
|----------|---------|----------------|-----------------------------|-------------|
| Trichy | Engineering and central TN distribution hub | 2,000+ trucks | BHEL Industrial Area, Thuvakudi, Tiruverumbur; engineering, fabrication, cement | Central connector for Chennai-Coimbatore-Madurai with heavy industrial cargo demand |
| Madurai | Southern TN distribution and retail/manufacturing hub | 2,500+ trucks | K.K. Nagar, Simmakkal, Kochadai, Mattuthavani; retail, IT, manufacturing, agro-processing | TNTA and major courier branches make it a strong regional control point |
| Tirunelveli | Cement, wind energy, manufacturing, agriculture | 1,500+ trucks | Tirunelveli Town, Palayamkottai, Thoothukudi Road industrial area | India Cements/wind corridor and gateway to Kanyakumari/southern tip |
| Sivakasi | Fireworks, printing, safety matches | 1,000+ trucks | Sivakasi industrial area, Sattur | Hazardous fireworks movement creates high-compliance, seasonal freight demand |
| Virudhunagar | Fireworks, match industries, trading | 1,200+ trucks | Virudhunagar, Rajapalayam, Sattur, Aruppukottai | Combined Sivakasi/Virudhunagar corridor is a specialized fireworks logistics zone |
| Dindigul | Locks, textiles, floriculture, agriculture | 800+ trucks | Dindigul, Natham, Oddanchatram | Oddanchatram flower market suggests cold-chain and time-sensitive agri movement |
| Thoothukudi | Port city, marine, salt, power | 1,000+ trucks | VOC Port, New Harbour Estate, SPIC area | Container/bulk cargo and port logistics make this a high-value corridor node |
| Theni | Agriculture, spices, dairy, cardamom | 500+ trucks | Theni, Bodinayakanur, Cumbum, Periyakulam | Kerala gateway and spice/mango flows create seasonal high-value cargo |
| Kanyakumari | Marine, wind energy, rubber/cashew, manufacturing | 600+ trucks | Nagercoil, Vadasery, Marthandam, Colachel | Southernmost point with Kerala proximity and future Colachel Port upside |

## TN Policy Corridors

| Corridor | Phase | Districts Covered | Strategic Meaning |
|----------|-------|-------------------|-------------------|
| Hosur to Chennai | Phase 1 | Krishnagiri, Vellore, Kanchipuram, Chennai | Highest-priority NH-48/Bangalore-Chennai freight corridor |
| Coimbatore to Tuticorin via Madurai | Phase 1 | Coimbatore, Dindigul, Madurai, Virudhunagar, Tirunelveli, Thoothukudi | Textile/apparel-to-port route; overlaps many target southern districts |
| Hosur to Coimbatore | Phase 1 | Krishnagiri, Dharmapuri, Salem, Erode, Coimbatore | Western industrial corridor and supply-side link through trucking/manufacturing areas |
| Coimbatore to Chennai | Phase 2 | Coimbatore, Erode, Karur, Namakkal, Salem, Vellore, Chennai | Textile/truck-body-building corridor into Chennai demand zones |
| Chennai to Kanyakumari | Phase 2 | Chennai, Madurai, Virudhunagar, Tirunelveli, Kanyakumari | Full north-south state spine and long-haul expansion lane |

## Private Godown Listings

| Location | District | Size | Rent Signal | Source | Notes |
|----------|----------|------|-------------|--------|-------|
| Karanodai, GNT Road | Chennai | 15,000 sq ft | Rs.2,40,000/month plus maintenance signal | MagicBricks | Strategic road access and large-vehicle access noted |
| Tiruvallur High Road, Poonganagar | Chennai | 1,800 sq ft | Rs.24,000/month plus deposit signal | MagicBricks | Small private warehouse/godown lead |
| Madhavaram, Chennai North | Chennai | 2,100 sq ft | Rs.58,000/month | MagicBricks | Immediate availability, near high road |
| George Town | Chennai | 1,350 sq ft | Call for price | MagicBricks | Urban storage/godown signal |
| Ponmalaipatti | Trichy | 4,800 sq ft | Not captured | MagicBricks | Trichy private godown lead |
| Muthaliyar Chatram | Trichy | 5,000 sq ft | Not captured | MagicBricks | Trichy private godown lead |

## Warehouse Pricing Records

| Source | Records | Locations / Corridor Signal | Notes |
|--------|---------|-----------------------------|-------|
| MagicBricks | 6 | Greams Road, Sriperumbudur, Thiruninravur, Tiruvallur High Road, Karanodai, Katrambakkam | Standard warehouse/godown pricing; computed per-sqft where rent and size are numeric |
| RealEstateIndia | 6 | Oragadam, Sriperumbudur, Poonamallee Highway, Kundrathur, Madhavaram | Mix of Grade A and standard records; several call-for-price entries |
| Stockarea | 3 | Keelameni, NH-16 Periyapalayam, Sriperumbudur | Grade A/A+ records; useful benchmark for premium warehouse pricing |
| ChennaiProperties | 4 | Mambakkam, Padappai, Ponneri, Perambur | Standard/private listing signal; some negotiable or call-for-price entries |

## Fulfillment Centers

| Company | Code | Location | District | Strategic Signal |
|---------|------|----------|----------|------------------|
| Amazon | MAA4 | Puduvoyal | Thiruvallur | North Chennai/Thiruvallur e-commerce fulfillment anchor near IndoSpace AS Industrial Park |
| Amazon | CJB1 | Coimbatore | Coimbatore | Western TN e-commerce fulfillment anchor serving Coimbatore/Tiruppur regional demand |

## Cluster Notes

### Sriperumbudur Industrial Corridor

- Major players: IndoSpace, ESR, HiParks, SAN Logistik, Pragati Warehousing, Ramanujar/TVS Infra, Hiranandani Mannur.
- Key tenants and industrial anchors: Hyundai, Renault-Nissan, Samsung, Dell, Foxconn, Nokia, Motorola, Mitsubishi, BMW.
- Strategic relevance: recurring B2B freight, auto ancillary movement, electronics manufacturing, and supplier-to-plant coordination.
- Latest enrichment: 22+ Fortune 500 company signal, 4,500-acre SIPCOT context, and new Grade A supply from Pragati, Ramanujar, and Hiranandani Mannur.

### Redhills Warehouse Hub

- Major players: Hiranandani, TVS Infra, IndoSpace, Warehousing Express.
- Asset signals: Hiranandani 82 acres/2.0 Mn sq ft, TVS Infra 33 acres/11.2 lakh sq ft, IndoSpace 48 acres/10.4 lakh sq ft.
- Demand anchors: Amazon, Flipkart, DMart, Reliance Retail, BigBasket, FMCG companies.
- Strategic relevance: e-commerce and FMCG distribution, short-haul fleet demand, milk-run potential, local delivery concentration.
- Latest enrichment: fastest-growing Chennai warehouse cluster signal, Hiranandani IGBC Gold, e-commerce demand driver, and historical Chennai distribution role.

### Poonamallee-Irungattukottai

- Major players/leads: IndoSpace Mevalurkuppam, Stockarea, private godowns.
- Asset signal: IndoSpace Mevalurkuppam 15 acres/4.3 lakh sq ft.
- Tenant signal: Hyundai suppliers, Renault-Nissan suppliers, local 3PLs.
- Strategic relevance: gateway between Chennai city freight and the Oragadam-Sriperumbudur industrial belt.
- Validation need: local warehouse operators and transport companies here may be a strong first sales list.
- Latest enrichment: connects Redhills-side distribution and Sriperumbudur/Oragadam industrial demand via Poonamallee High Road/NH-48.

### Koyambedu-Madhavaram

- Strategic role: transport nerve center and urban distribution zone.
- Likely supply character: more fragmented and informal than Grade A parks.
- Strategic relevance: local trucker aggregation, last-mile/first-mile demand, fast dispatch use cases.
- Latest enrichment: Madhavaram functions as a warehouse district while Koyambedu remains the broker/transporter nerve center.

### Guindy-Siruseri-Okkiyam

- Strategic role: south Chennai 3PL/e-commerce and industrial support zone.
- Strategic relevance: useful for serving OMR, GST Road, and south Chennai consumption/industrial pockets.
- Latest enrichment: H&S Supply Chain HQ at Siruseri, IT parks/industrial estates as local demand anchors, and Amazon/Flipkart/ITC/Marico via H&S as tenant/client signals.

## Zippy Opportunity Map

| Opportunity | Target Segment | Why It Is Attractive | First Action |
|-------------|----------------|----------------------|--------------|
| Warehouse-to-local-transport matching | Redhills, Poonamallee, Madhavaram warehouses | Fragmented supply creates coordination pain | Build contact list and validate daily vehicle demand |
| Industrial corridor B2B lanes | Sriperumbudur-Oragadam manufacturers and 3PLs | Recurring freight and return-load economics | Map top 20 shipper lanes and vehicle types |
| Local transporter digitization | Poonamallee, Koyambedu, Madhavaram transport operators | Small operators need order visibility and faster settlement | Interview 15-20 transporters |
| E-commerce/FMCG support lanes | Redhills and Thamaraipakkam parks | High-frequency distribution and predictable demand windows | Validate route density and peak-hour constraints |
| Warehouse discovery/sales CRM | All scraped facilities | Scrape data can become lead pipeline | Convert facilities into CRM stages |
| Port logistics wedge | Thoothukudi, Chennai port-linked operators | Export/import workflows need freight, warehousing, documentation, and carrier coordination | Validate top customs/forwarding pain points |
| Textile corridor matching | Tiruppur, Erode, Karur, Coimbatore | Repeat textile movements can support lane density and return-load planning | Map textile shipper lanes and seasonal peaks |
| Transport supply onboarding | Namakkal and Koyambedu/Madhavaram | Dense trucking ecosystem can help build initial carrier supply | Interview fleet owners and driver trainers |
| Agro/cold-chain expansion | Thanjavur Delta, Nagapattinam, Tiruvarur | Low density plus food/agri specialization suggests service gaps | Validate cold storage and reefer demand |
| Association-led supply acquisition | Coimbatore, Chennai, Madurai | Associations provide warm network nodes for transporter trust-building | Build association outreach script and member validation checklist |
| Private godown marketplace wedge | Chennai North, George Town, Trichy | Small private godowns can become flexible storage inventory | Validate availability, lease terms, truck access, and loading constraints |
| Cold-chain operating wedge | Chennai, Coimbatore, Salem, Madurai, Trichy | Cold storage and reefer movement require higher trust, SLA tracking, and proof workflows | Validate temperature bands, vehicle availability, and pharma/food compliance needs |
| Fulfillment middle-mile wedge | Thiruvallur, Coimbatore, Chennai | Amazon and e-commerce fulfillment nodes create repeat middle-mile and carrier coordination demand | Map FC-to-city and FC-to-warehouse lanes |
| Southern TN compliance wedge | Sivakasi, Virudhunagar, Thoothukudi | Fireworks/DG cargo, port cargo, and project cargo require compliance-aware matching | Identify licensed hazardous/project-cargo operators |
| Policy-corridor launch sequencing | Phase 1 TN policy corridors | Government truck lay-bye priorities indicate where freight infrastructure will improve first | Prioritize Hosur-Chennai, Coimbatore-Tuticorin, and Hosur-Coimbatore validation |
| District playbooks | 9 deep-dive districts | Each district has different cargo, seasonality, and vehicle needs | Convert deep dives into district-specific sales/interview scripts |

## Data Quality And Validation

| Item | Current Confidence | Validation Needed |
|------|--------------------|-------------------|
| Large Grade A park names and locations | Medium-high | Confirm via official sites and latest leasing pages |
| Facility sizes | Medium | Cross-check against official brochures and park pages |
| Rent ranges | Low-medium | Validate with brokers/operators; likely changes quickly |
| Local warehouse leads from Sulekha/Justdial | Low | Phone call, address confirmation, service availability |
| Tenant names | Low-medium | Confirm current occupancy before using in outreach |
| Growth trend labels | Directional | Support with market reports or interviews |
| Railway database imports | Medium | Confirm deduplication rules and add unique constraints where needed |
| Place-name normalization | Medium | Normalize Tuticorin/Thoothukudi, Trichy/Tiruchirappalli, and district spelling variants |
| Personal contact handling | High | Keep phone/WhatsApp fields in controlled database or CRM, not broad notes or commits |
| Local transporter lead quality | Low-medium | Verify whether listings are active, reachable, and relevant to target vehicle types |
| Private godown listing freshness | Low-medium | MagicBricks listings may expire quickly; confirm current availability before using |
| Destructive cluster rebuild | High | Replace `DROP TABLE` rebuild with migration/upsert flow before adding more regional clusters |
| Manual SQL value construction | Medium | Avoid manual SQL string assembly for arrays; prefer parameterized inserts to reduce syntax and injection risk |
| Cold storage capacity units | Medium | Confirm whether TNAU `capacity` values are metric tonnes, sqft proxy, or another unit before modeling capacity |
| Summary SQL bug | High | Final facility-type query selects `grade` but references `facility_type`; fix query before using script output |
| Non-TN company relevance | Medium | CCI Logistics Industrial Park locations in script are Panvel/NCR; validate Tamil Nadu relevance before treating as TN supply |
| Fleet estimate comparability | Medium | Values like `2500+ trucks` are directional and should not be sorted as strings for analytics |
| Hazardous goods compliance | High | Sivakasi/Virudhunagar fireworks logistics needs ADR/explosives licensing validation before outreach or matching |
| Policy corridor assumptions | Medium | Confirm TN Logistics Policy corridor details against official TIDCO/government documents before investor/sales use |
| Cluster duplicate imports | Medium | Repeated `warehouse_clusters` inserts without conflict handling can duplicate the same 5 cluster records |
| Warehouse cluster placeholder bug | High | Insert SQL lists 17 columns and passes 17 params, but only uses `$1`-`$16`; add `$17` for `data_source` before running |

## Follow-Up Research Queue

- [ ] Verify each company website and capture official contact details.
- [ ] Rotate Railway database credentials because a full connection URL was pasted into chat.
- [ ] Move import scripts to a sanitized local file using environment variables for secrets.
- [ ] Confirm `facilities` and `warehouse_clusters` have useful unique constraints before repeated imports.
- [ ] Replace destructive `warehouse_clusters` reset with idempotent upserts.
- [ ] Back up or export `warehouse_clusters` before any future schema reset.
- [ ] Add unique/dedupe strategy for `local_transport` and `godown_listings`.
- [ ] Normalize district and city spellings before using the database for analytics.
- [ ] Create a privacy-safe CRM workflow for phone/WhatsApp outreach data.
- [ ] Add phone/email/location fields for local transport and warehouse leads.
- [ ] Split leads into `Grade A parks`, `local warehouses`, `freight forwarders`, and `transport companies`.
- [ ] Build a Chennai-area map by cluster: Redhills, Sriperumbudur, Poonamallee, Madhavaram, Guindy/Siruseri.
- [ ] Build local transporter interview scripts for Coimbatore CGTA, Chennai CGTA, Madurai lorry association, Koyambedu, Erode, and Salem.
- [ ] Validate MagicBricks godown listings for current availability, access road, loading/unloading, deposit, and lease duration.
- [ ] Fix final summary query for facility types: select `facility_type`, not `grade`.
- [ ] Validate TNAU cold-storage capacity units and normalize Ambattoor/Ambattur and Perumballur/Perambalur spellings.
- [ ] Segment cold-chain leads by pharma, food, seafood, dairy, vaccine, and agri-perishable use cases.
- [ ] Map Amazon MAA4 and CJB1 to likely middle-mile corridors and local carrier needs.
- [ ] Convert district deep dives into one-page launch playbooks for Trichy, Madurai, Thoothukudi, Tirunelveli, Sivakasi/Virudhunagar, Dindigul, Theni, and Kanyakumari.
- [ ] Validate TN Logistics Policy corridors from official TIDCO/government source before external use.
- [ ] Replace text fleet estimates with numeric min/max fields for analytics.
- [ ] Create hazardous-goods compliance checklist for Sivakasi/Virudhunagar fireworks transport.
- [ ] Add `tn_policy_corridors` and `district_deep_dive` dedupe keys before repeated imports.
- [ ] Interview local transporters about vehicle types, daily load availability, payment cycles, and return-load pain.
- [ ] Deepen Coimbatore, Tiruppur, Madurai, Trichy, Salem, Hosur, Erode, Namakkal, Thoothukudi, and Thanjavur Delta research waves.

## Related Notes

- [[Tamil Nadu Industrial Corridors]]
- [[Chennai Logistics Hub]]
- [[Tamil Nadu Customer Segmentation and GTM Plan]]
- [[South India Tier 2-3 Logistics Opportunity]]
- [[South India Local Truck Rate Bands]]
- [[Indian Road Logistics Pain Point Map]]
- [[Digital Freight Marketplace]]
- [[Indian MSME Logistics Model]]

## Related Hubs

- [[Market Intelligence Hub]]
- [[Indian Logistics Ecosystem Hub]]
