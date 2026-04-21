---
type: sop
domain: dispatch
owner: operations
decision_value: high
status: verified
related_hubs:
  - Compliance & Regulation Hub
  - Operations Strategy Hub
  - SOPs Hub
tags:
  - sop
  - dispatch
  - compliance
  - documentation
---

# SOP - Verify Shipment Documents

## Trigger

Shipment is being booked, assigned, picked up, handed over to a partner, or delivered, and the document set must be checked for compliance and operational completeness.

## Preconditions

- Order record exists
- Shipment details are available
- Document set has been collected in digital or physical form

## Steps

### Step 1: Identify Required Documents

```text
1.1 Check cargo type, route type, and customer segment
1.2 Determine whether shipment is intra-state or inter-state
1.3 Confirm whether E-way Bill, invoice, LR/GR, and permits are required
1.4 Mark any special cargo compliance requirements
```

### Step 2: Validate Document Completeness

```text
2.1 Verify consignee and consignor details
2.2 Verify goods description, quantity, and declared value
2.3 Check vehicle and driver identifiers where applicable
2.4 Confirm signatures, timestamps, and attachments are present
```

### Step 3: Validate Consistency

```text
3.1 Match documents against the order record
3.2 Check route, origin, and destination consistency
3.3 Confirm cargo type matches vehicle and handling requirements
3.4 Flag mismatches before dispatch or handoff
```

### Step 4: Clear Or Escalate

```text
4.1 Approve shipment for next operational step if documents are valid
4.2 Escalate missing or inconsistent documents immediately
4.3 Do not dispatch non-compliant shipments without approval
4.4 Record verification status in the order trail
```

## Verification Checklist

| Item | What To Check |
|------|----------------|
| Invoice | Goods, value, party details |
| E-way Bill | Validity, route, taxable shipment fit |
| LR/GR | Carrier, shipment, and consignee details |
| POD prerequisites | Delivery proof expectations and receiver details |
| Special permits | Hazardous, temperature-sensitive, or regulated cargo needs |

## Escalation Triggers

- Missing mandatory compliance document
- E-way Bill mismatch or expiry risk
- Cargo description mismatch
- Value discrepancy or suspicious edit
- Customer or partner refuses correction

## Related Scenarios

- [[Scenario - E-way Bill Expiry During Transit]]
- [[Scenario - High Value Electronics Transit]]
- [[Scenario - Hazardous Material Transport]]

## Related Concepts

- [[Proof of Delivery]]
- [[E-way Bill]]
- [[GST for Logistics]]

## Related Hubs

- [[Compliance & Regulation Hub]]
- [[Operations Strategy Hub]]
- [[SOPs Hub]]
