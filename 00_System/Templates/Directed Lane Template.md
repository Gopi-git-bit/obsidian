---
title: Directed Lane Template
type: template
category: corridor-intelligence
status: active
---

# Directed Lane Template

```yaml
type: directed_lane
origin:
destination:
distance_km:
state_pair:
primary_industries:
  -
primary_cargo:
  -
lane_strength: strong / medium / weak
load_frequency_score:
rate_score:
backhaul_score:
payment_risk:
demurrage_risk:
vehicle_types:
  - lcv
  - 14ft
  - 20ft
  - 32ft
best_mode:
triangle_candidate:
nearby_substitute_city:
data_confidence:
source_type: official / association / field / whatsapp / estimate
status:
```

# {{origin}} -> {{destination}}

## Lane Summary


## Cargo Flow

| Cargo | Frequency | Vehicle | Notes |
| --- | --- | --- | --- |
|  |  |  |  |

## Why This Direction Matters


## Return-Trip Problem


## Triangle Opportunity


## Rate And Cost Notes


## Risk

| Risk | Level | Control |
| --- | --- | --- |
| payment delay |  |  |
| demurrage/waiting |  |  |
| vehicle mismatch |  |  |
| cargo damage |  |  |

## Validation Tasks

- [ ] Collect WhatsApp/load-board posts for 14 days
- [ ] Interview 5 transporters
- [ ] Interview 5 MSMEs
- [ ] Collect rate benchmarks
- [ ] Estimate wait time
- [ ] Score lane

## Evidence Log

| Claim | Source | Confidence |
| --- | --- | --- |
|  |  |  |

## Related Notes

- [[{{origin}}]]
- [[{{destination}}]]
