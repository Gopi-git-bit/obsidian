---
title: Logistics Hub Template
type: template
category: logistics-hub-intelligence
status: active
---

# Logistics Hub Template

```yaml
type: logistics_hub
name:
city:
tier:
coordinates:
  lat:
  lng:
radius_km:
hub_type:
  -
connectivity:
  highways:
    -
  rail_links:
    -
  port_links:
    -
  airport_links:
    -
cargo_profile:
  inbound:
    -
  outbound:
    -
avg_daily_truck_movements:
peak_hours:
  -
backhaul_potential:
triangle_feasibility_score:
data_confidence:
last_updated:
idempotency_key:
status:
```

# {{name}} - {{city}}

## Hub Context


## Connectivity

| Mode | Link | Notes |
| --- | --- | --- |
| Highway |  |  |
| Rail |  |  |
| Port |  |  |
| Airport |  |  |

## Cargo Profile

| Direction | Cargo | Strength | Notes |
| --- | --- | --- | --- |
| Inbound |  |  |  |
| Outbound |  |  |  |

## Triangle Role


## Guardrails

| Risk | Control |
| --- | --- |
| low confidence | human validation |
| vehicle mismatch | vehicle-fit check |
| waiting time | DWIS/gate timing |
| payment risk | verified payer/advance |

## Validation Tasks

- [ ] Verify hub coordinates and radius
- [ ] Interview 5 transporters serving this hub
- [ ] Identify top inbound cargo
- [ ] Identify top outbound cargo
- [ ] Estimate truck movement and peak hours
- [ ] Map nearby weak return lanes
- [ ] Score triangle feasibility
```
