---
type: concept
domain: compliance
decision_value: high
status: evergreen
related_hubs:
  - Compliance & Regulation Hub
  - Operations Strategy Hub
tags:
  - concept
  - compliance
  - india-logistics
---

# E-way Bill

## Definition

Electronic way bill required for movement of goods worth more than INR 50,000 across India under GST regulations.

## When Required

| Condition | Requirement |
|-----------|-------------|
| Goods value > INR 50,000 | E-way bill mandatory |
| Interstate movement | Always required |
| Intrastate movement | Required per state rules |
| Transport change | Part B update needed |

## Generation Requirements

- Supplier/Recipient GSTIN
- Invoice/Bill details
- Vehicle number (Part B)
- Transport document

## Key Fields

- **E-way Bill Number (EBN)** - 12-digit unique ID
- **Validity** - Based on distance
- **Part A** - Invoice details
- **Part B** - Vehicle details

## Validity Period

| Distance | Validity |
|----------|----------|
| Up to 100 km | 1 day |
| 100-300 km | 3 days |
| 300-500 km | 7 days |
| 500-1000 km | 15 days |
| >1000 km | 30 days |

## Exceptions

- Null/Zero-rated goods
- Defense cargo
- Railway receipts
- Specific exemption list

## Decision Impact

- [[Scenario - E-way Bill Expiry During Transit]]
- Triggers [[Communication Agent]] alerts
- Required for compliance verification

## Risks

- Expiry during transit
- Wrong vehicle assignment
- Missing/invalid EBN
- Document mismatch

## Related Notes

- [[GST for Logistics]]
- [[SOP - E-way Bill Generation]]
- [[Scenario - E-way Bill Expiry During Transit]]
