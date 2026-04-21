---
type: concept
domain: fleet
decision_value: high
status: evergreen
related_hubs:
  - Fleet & Transport Hub
  - Operations Strategy Hub
tags:
  - concept
  - fleet
  - vehicle-types
---

# LCV vs MCV vs HCV

## Vehicle Classification in India

### LCV (Light Commercial Vehicle)

| Attribute | Value |
|-----------|-------|
| GVW | 3.5 - 7.5 tons |
| Capacity | 500 - 2000 kg |
| Typical Use | Urban delivery, small packages |
| Fuel | Diesel/Petrol/CNG |
| License | Light Motor Vehicle |

### MCV (Medium Commercial Vehicle)

| Attribute | Value |
|-----------|-------|
| GVW | 7.5 - 16 tons |
| Capacity | 2 - 7 tons |
| Typical Use | Regional distribution |
| Fuel | Diesel |
| License | Medium Goods Vehicle |

### HCV (Heavy Commercial Vehicle)

| Attribute | Value |
|-----------|-------|
| GVW | 16 - 49 tons |
| Capacity | 10 - 25 tons |
| Typical Use | Long-haul, heavy cargo |
| Fuel | Diesel |
| License | Heavy Goods Vehicle |

## Cost Comparison (Per km)

| Vehicle | Fixed Cost | Variable Cost | Total |
|---------|------------|---------------|-------|
| LCV | Low | Low | Rs 8-12 |
| MCV | Medium | Medium | Rs 15-22 |
| HCV | High | Low | Rs 22-35 |

## Operating-Cost Pattern

| Vehicle | Mileage Tendency | Toll Burden | Depreciation Burden | Labor Sensitivity |
|---------|------------------|-------------|---------------------|-------------------|
| LCV | Best | Lower | Lower | Moderate |
| MCV | Medium | Medium | Medium | Moderate |
| HCV | Lowest | Higher | Highest | High when utilization slips |

## When to Use

### LCV
- City deliveries
- Small shipments
- Tight timelines
- Urban areas with restrictions

### MCV
- Regional routes (100-400 km)
- Medium loads
- Mix of urban/rural
- Flexibility needs

### HCV
- Long distance (>400 km)
- Heavy/bulk cargo
- Cost optimization
- FTL (Full Truck Load)

## Decision Tree

```text
Required Capacity?
|- <2 tons -> LCV
|- 2-7 tons -> MCV
`- >7 tons -> HCV

Distance?
|- <100 km -> LCV/MCV
|- 100-400 km -> MCV/HCV
`- >400 km -> HCV

Special Requirements?
|- Fragile -> Closed Body
|- Liquid -> Tanker
`- Oversized -> Special Permit
```

## Related Notes

- [[Closed Body Vehicle]]
- [[Line Haul vs Last Mile]]
- [[Load Matching Algorithm]]
- [[Vehicle Operating Cost Model]]
