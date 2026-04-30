---
type: warehouse_cluster
city: Coimbatore
cluster_name: SIPCOT Irugur / East Coimbatore
coordinates:
  lat:
  lng:
radius_km: 5
industries:
  - textiles
  - engineering
  - pumps
  - auto_components
warehouse_types:
  - industrial_warehouse
  - cross_dock
  - raw_material_storage
connectivity:
  highways:
    - NH544
  rail: Coimbatore rail connectivity
  port: Kochi Port / Chennai Port
  airport: Coimbatore Airport
cargo_profile:
  outbound:
    - yarn
    - machinery
    - pumps
    - engineering goods
  inbound:
    - FMCG
    - chemicals
    - packaging
    - raw materials
avg_daily_truck_movements:
peak_hours:
  - morning dispatch
  - evening receiving
tier: 2
backhaul_potential: 8
data_confidence: low
last_updated: 2026-04-30
idempotency_key: coimbatore:sipcot-irugur-east:2026-04-30
status: validate
tags:
  - warehouse-cluster
  - coimbatore
  - triangle-candidate
  - validate
---

# SIPCOT Irugur / East Coimbatore - Coimbatore

## Industrial Context

Central connector cluster for Western Tamil Nadu textile, engineering, pumps, and machinery movement.

This cluster is useful as a return-side node for Chennai-origin loads and a feeder back into Tiruppur/Erode.

## Cargo Flow Patterns

| Direction | Primary Cargo | Volume Score | Seasonality |
| --- | --- | ---: | --- |
| Outbound | yarn, machinery, pumps, engineering goods | 8 | industrial cycles |
| Inbound | FMCG, chemicals, packaging, raw materials | 8 | steady |

## Triangle Integration Rules

Use as cluster C in:

```text
Tiruppur cluster -> Chennai cluster -> Coimbatore cluster -> Tiruppur cluster
```

## Validation Tasks

- [ ] Verify exact cluster coordinates
- [ ] Interview 5 Coimbatore transporters
- [ ] Estimate Chennai -> Coimbatore load frequency
- [ ] Estimate Coimbatore -> Tiruppur feeder load frequency
- [ ] Track wait time at industrial warehouses

## Related Notes

- [[South India Warehouse and Industrial Cluster Intelligence Framework]]
- [[Chennai to Tiruppur]]
- [[Tiruppur Chennai Coimbatore Triangle Route]]
