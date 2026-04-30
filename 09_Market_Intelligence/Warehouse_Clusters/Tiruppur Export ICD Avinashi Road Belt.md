---
type: warehouse_cluster
city: Tiruppur
cluster_name: Tiruppur Export ICD / Avinashi Road Belt
coordinates:
  lat:
  lng:
radius_km: 5
industries:
  - textiles
  - garments
  - export cargo
warehouse_types:
  - export_compliance
  - carton_storage
  - hanging_storage
connectivity:
  highways:
    - Avinashi Road
  rail:
  port: Chennai Port / Tuticorin Port
  airport: Coimbatore Airport
cargo_profile:
  outbound:
    - knitwear
    - garments
    - textile cartons
    - export cargo
  inbound:
    - packaging
    - trims
    - labels
    - chemicals
avg_daily_truck_movements:
peak_hours:
  - morning loading
  - evening dispatch
 tier: 2
backhaul_potential: 7
data_confidence: low
last_updated: 2026-04-30
idempotency_key: tiruppur:export-icd-avinashi-road:2026-04-30
status: validate
tags:
  - warehouse-cluster
  - textiles
  - export
  - triangle-candidate
  - validate
---

# Tiruppur Export ICD / Avinashi Road Belt - Tiruppur

## Industrial Context

Primary garment and knitwear export-origin cluster for Tiruppur.

This cluster should be treated as a major origin node for Chennai port-linked textile movement.

## Cargo Flow Patterns

| Direction | Primary Cargo | Volume Score | Seasonality |
| --- | --- | ---: | --- |
| Outbound | garments, knitwear, textile cartons | 9 | export/fashion peaks |
| Inbound | packaging, trims, labels, chemicals | 6 | production-linked |

## Triangle Integration Rules

If direct Chennai -> Tiruppur return is weak, test:

```text
Madhavaram / Chennai cluster -> SIPCOT Irugur / Coimbatore cluster -> Tiruppur Export ICD
```

## Validation Tasks

- [ ] Verify exact cluster coordinates
- [ ] Interview 5 Tiruppur textile transporters
- [ ] Estimate daily truck movement
- [ ] Collect Chennai-bound rate benchmarks
- [ ] Estimate average loading wait time
- [ ] Validate inbound packaging/chemical cargo demand

## Related Notes

- [[South India Warehouse and Industrial Cluster Intelligence Framework]]
- [[Tiruppur to Chennai]]
- [[Tiruppur Chennai Coimbatore Triangle Route]]
