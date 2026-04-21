---
type: sop
domain: dispatch
owner: operations
decision_value: high
status: verified
related_hubs:
  - Operations Strategy Hub
  - Operations Strategy Hub
tags:
  - sop
  - operations
  - urgent
---

# SOP - Handle Urgent Request

## Trigger

Customer requests expedited/same-day delivery or urgent pickup.

## Preconditions

- Customer request received
- Delivery location verified
- Vehicle requirement identified

## Steps

### Step 1: Assess Urgency

```
1.1 Confirm deadline/timeline
1.2 Calculate feasibility
1.3 Identify gap between request and standard
1.4 Determine premium pricing applicable
```

### Step 2: Resource Check

```
2.1 Query immediate vehicle availability
2.2 Filter by vehicle type requirement
2.3 Check driver location and status
2.4 Assess pickup-to-delivery time
```

### Step 3: Quote with Urgency Premium

```
3.1 Apply urgency surcharge
3.2 Confirm pickup timeline
3.3 Present quote to customer
3.4 Get explicit confirmation
```

### Step 4: Prioritize Assignment

```
4.1 Bump standard queue if needed
4.2 Assign best available vehicle
4.3 Notify driver with priority status
4.4 Set enhanced monitoring
```

### Step 5: Real-Time Tracking

```
5.1 Monitor pickup in real-time
5.2 Track transit progress
5.3 Alert customer of any delays
5.4 Prepare for immediate POD on arrival
```

## Urgency Tiers

| Tier | Timeline | Surcharge | Escalation |
|------|----------|-----------|------------|
| Express | 2-4 hours | 25% | Standard |
| Same Day | Same business day | 50% | Priority |
| Critical | Immediate | 75-100% | VIP handling |

## Related Scenarios

- [[Scenario - Same Day Delivery]]
- [[Scenario - Urgent Delivery Request]]

## Related Concepts

- [[Urgency Surcharge Logic]]
- [[Fleet Utilization]]

## Related Algorithms

- [[Load Matching Algorithm]]
- [[Route Optimization Logic]]

## Related Hubs

- [[Operations Strategy Hub]]
