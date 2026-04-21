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
  - security
---

# SOP - Assign Secure Vehicle

## Trigger

Order requires secure transportation - high-value cargo, sensitive goods, or customer request for enhanced security.

## Preconditions

- Order identified for secure handling
- Cargo value or type documented
- Security requirements confirmed

## Steps

### Step 1: Identify Requirements

```
1.1 Review cargo details for security needs
1.2 Confirm vehicle type required
1.3 Check for GPS tracking requirement
1.4 Verify insurance coverage
```

### Step 2: Select Vehicle

```
2.1 Filter vehicles by security features:
    - GPS tracking enabled
    - Tamper-proof containers
    - Locking mechanisms
2.2 Verify vehicle maintenance status
2.3 Confirm driver track record
```

### Step 3: Driver Assignment

```
3.1 Check driver reliability score
3.2 Verify driving experience
3.3 Confirm driver background check
3.4 Brief driver on security protocols
```

### Step 4: Document Assignment

```
4.1 Record vehicle and driver for order
4.2 Note security measures taken
4.3 Set enhanced monitoring
4.4 Document departure time
```

## Requirements Matrix

| Cargo Type | Vehicle Type | Tracking | Insurance |
|-----------|--------------|----------|----------|
| High-value electronics | Closed body + GPS | Mandatory | Required |
| Pharma | Refrigerated + GPS | Mandatory | Required |
| Documents | Any secure | Recommended | Optional |
| Fragile | Closed body | Mandatory | Optional |

## Related Scenarios

- [[Scenario - High Value Electronics Transit]]
- [[Scenario - Electronics Need Closed Body Vehicle]]

## Related Concepts

- [[Closed Body Vehicle]]
- [[Fleet Utilization]]

## Related Hubs

- [[Fleet & Transport Hub]]
