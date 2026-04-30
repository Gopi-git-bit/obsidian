---
type: logistics_hub
name: Madhavaram Logistics Hub
city: Chennai
tier: 1
coordinates:
  lat:
  lng:
radius_km: 12
hub_type:
  - cross_dock
  - grade_a_warehousing
  - fmcg_distribution
  - port_gateway
connectivity:
  highways:
    - NH16
  rail_links:
    - validate
  port_links:
    - Chennai Port
    - Ennore/Kattupalli proximity
  airport_links:
    - Chennai Airport
cargo_profile:
  inbound:
    - textile cartons
    - containers
    - consumer goods
  outbound:
    - FMCG
    - retail goods
    - packaging
    - machinery spares
avg_daily_truck_movements:
peak_hours:
  - early morning receiving
  - evening dispatch
backhaul_potential: 8
triangle_feasibility_score: 80
data_confidence: low
last_updated: 2026-04-30
idempotency_key: chennai:madhavaram-logistics-hub:2026-04-30
status: validate
tags:
  - logistics-hub
  - chennai
  - triangle-candidate
  - validate
---

# Madhavaram Logistics Hub - Chennai

## Hub Context

Metro-edge logistics hub hypothesis for FMCG, retail, e-commerce, and port-linked cargo.

Use as a major Chennai-side hub for textile inbound and Coimbatore/Tiruppur/Erode return routing.

## Triangle Role

Potential Hub B in:

```text
Tiruppur Export ICD -> Madhavaram Logistics Hub -> SIPCOT Irugur -> Tiruppur Export ICD
```

## Validation Tasks

- [ ] Verify hub boundary and coordinates
- [ ] Interview 5 Chennai transporters
- [ ] Estimate Chennai -> Coimbatore outbound load strength
- [ ] Estimate Chennai -> Tiruppur direct return weakness
- [ ] Measure wait-time patterns

## Related Notes

- [[South India Logistics Hub Intelligence Framework]]
- [[Madhavaram Logistics Hub]]
- [[Tiruppur Chennai Coimbatore Triangle Route]]
