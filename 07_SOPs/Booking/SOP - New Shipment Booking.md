---
type: sop
domain: booking
owner: operations
decision_value: high
status: verified
related_hubs:
  - Operations Strategy Hub
  - Scenario Playbooks Hub
tags:
  - sop
  - operations
  - booking
---

# SOP - New Shipment Booking

## Trigger

Customer submits booking request via any channel (web, app, phone, WhatsApp).

## Preconditions

- Customer account verified
- Pickup and delivery addresses valid
- Cargo details provided

## Steps

### Step 1: Capture Requirements

```
1.1 Customer name and contact
1.2 Pickup location and time window
1.3 Delivery location and time window
1.4 Cargo details:
    - Type of goods
    - Weight (kg)
    - Volume (if applicable)
    - Special handling needs
1.5 Required vehicle type
1.6 Any special instructions
```

### Step 2: Validate Request

```
2.1 Verify addresses are serviceable
2.2 Check for restricted items
2.3 Validate cargo type compatibility
2.4 Confirm pickup timeline is feasible
```

### Step 3: Generate Quote

```
3.1 Run [[Dynamic Pricing Logic]]
3.2 Apply customer tier discount if applicable
3.3 Calculate estimated delivery time
3.4 Present quote to customer
```

### Step 4: Customer Confirmation

```
4.1 Share quote with validity period
4.2 Customer accepts or negotiates
4.3 On acceptance: Create order record
4.4 Assign order ID
4.5 Send confirmation to customer
```

### Step 5: Order Queue

```
5.1 Add to pending vehicle assignment queue
5.2 Trigger [[Load Matching Algorithm]]
5.3 Notify customer of booking confirmation
```

## Exceptions

| Exception | Handling |
|-----------|----------|
| Address not serviceable | Suggest alternative or decline |
| Restricted cargo | Decline with explanation |
| Timeline not feasible | Propose alternative timing |
| Price rejected | Offer slight discount or decline |

## Escalation

- Multiple failed booking attempts → Operations Manager
- Customer complaint during booking → [[Customer Service Agent]]
- System failure → Manual booking process

## Related Scenarios

- [[Scenario - First-time Shipper Onboarding]]
- [[Scenario - Price Negotiation]]

## Related Concepts

- [[Order Lifecycle]]
- [[MSME Shipper Pain Points]]
