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
  - vehicle
---

# SOP - Handle Vehicle Breakdown

## Trigger

Driver reports vehicle breakdown during transit.

## Preconditions

- Active order assigned to vehicle
- Driver is on route
- Vehicle breakdown reported

## Steps

### Step 1: Receive Breakdown Report

```
1.1 Receive notification from driver
1.2 Record breakdown details (location, nature, urgency)
1.3 Confirm driver and cargo safety
1.4 Document timestamp
```

### Step 2: Assess Situation

```
2.1 Evaluate if quick repair is possible
2.2 Assess cargo transfer requirement
2.3 Determine estimated repair time
2.4 Calculate delivery impact
```

### Step 3: Coordinate Response

```
3.1 IF quick fix: Dispatch repair support
3.2 IF transfer needed:
    a. Identify nearest available replacement vehicle
    b. Coordinate cargo transfer
    c. Update driver with revised plan
3.3 Monitor response in real-time
```

### Step 4: Customer Communication

```
4.1 Notify customer of situation
4.2 Provide revised ETA
4.3 Reassure cargo safety
4.4 Update with resolution progress
```

### Step 5: Resolution

```
5.1 Verify delivery completion
5.2 Document incident details
5.3 Record cost impact
5.4 Update vehicle status
```

## Exceptions

| Exception | Handling |
|-----------|----------|
| No replacement available | Escalate to management |
| Cargo at risk | Coordinate immediate safety |
| Driver injured | Emergency services + backup |

## Escalation

- >2 hour delay → Operations Manager
- Cargo security risk → Security team
- Customer threat → Senior management

## Related Scenarios

- [[Scenario - Vehicle Breakdown Mid-Route]]
- [[Scenario - Partner Transporter Failure]]

## Related Concepts

- [[Fleet Maintenance Scheduling]]
- [[Vehicle Availability]]

## Related Hubs

- [[Fleet & Transport Hub]]
