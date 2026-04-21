---
type: sop
domain: dispatch
owner: operations
decision_value: high
status: verified
related_hubs:
  - Operations Strategy Hub
  - Fleet & Transport Hub
tags:
  - sop
  - operations
  - dispatch
---

# SOP - Assign Vehicle to Order

## Trigger

Order confirmed and pending vehicle assignment in the dispatch queue.

## Preconditions

- Order ID created
- Vehicle requirements identified
- Pickup time window established

## Steps

### Step 1: Check Own Fleet

```
1.1 Query available vehicles by type
1.2 Filter by location proximity to pickup
1.3 Check vehicle capacity vs cargo
1.4 Verify driver availability
1.5 Calculate utilization impact
```

### Step 2: Run Matching Algorithm

```
2.1 Execute [[Load Matching Algorithm]]
2.2 Score candidates using fit, ETA, reliability, and return potential
2.3 Check [[Carrier Scoring Algorithm]] if partner
2.4 Verify route feasibility
2.5 Keep top alternates in case confirmation fails
```

### Step 3: Select Vehicle

```
3.1 Choose best-scored vehicle
3.2 If own fleet: Assign vehicle + driver
3.3 If partner: Confirm with partner transporter
3.4 Record assignment in system
```

### Step 4: Notify Driver

```
4.1 Send pickup details to driver app
4.2 Include:
    - Pickup address
    - Customer contact
    - Cargo details
    - Special instructions
4.3 Request pickup confirmation
```

### Step 5: Track Assignment

```
5.1 Monitor driver acknowledgment
5.2 Send reminder if no response
5.3 Escalate if unresponsive
5.4 Fall back to next candidate if timeout
5.5 Expand search radius or partner pool if confidence drops below dispatch threshold
```

## Exceptions

| Exception | Handling |
|-----------|----------|
| No own fleet available | Run partner search → [[Scenario - No Own Fleet Available]] |
| Partner vehicle unavailable | Try next partner or escalate |
| Driver unresponsive | Contact alternative driver |
| Time window at risk | Notify customer immediately |

## Escalation

- 30 minutes without driver confirmation → Dispatcher review
- Partner confirmation delayed → Operations Manager
- Multiple assignment failures → Escalation team

## Related Scenarios

- [[Scenario - No Own Fleet Available]]
- [[Scenario - Urgent Delivery Request]]

## Related Concepts

- [[Vehicle Assignment Logic]]
- [[Fleet Utilization]]
- [[Driver Assignment Logic]]
