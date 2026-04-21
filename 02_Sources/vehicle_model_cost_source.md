---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-04-21
source_file: vehicle model.txt
notes: Vehicle-model and operating-cost inputs for mileage, dimensions, depreciation, tolls, insurance, and regional labor assumptions
---

# Vehicle Model Cost Source

This source captures operational pricing inputs that sit between high-level vehicle classes and live quote generation.

## Key Extracts

- Vehicle selection should not stop at LCV, MCV, and HCV labels; model-level operating behavior matters.
- Mileage differences materially affect per-kilometer cost, especially on long-haul routes and lower-utilization loops.
- Insurance, depreciation, toll burden, and routine fitness or health costs should be treated as recurring operating-cost inputs.
- Driver salary assumptions can vary by region and route difficulty, so labor allocation should not always be treated as flat.
- Vehicle dimensions and carrying form factor influence suitability, but also affect commercial efficiency and deadhead economics.

## Why It Matters

The existing vault already describes vehicle classes and dynamic pricing. This source adds the missing bridge between them: a reusable operating-cost model that can inform deterministic pricing, floor-rate protection, and fleet selection.

## Derived Notes

- [[Vehicle Operating Cost Model]]
- [[LCV vs MCV vs HCV]]
- [[Distance Based Pricing]]
- [[Dynamic Pricing Logic]]

---
*Processed from user-provided vehicle model notes and normalized for fleet and pricing architecture.*
