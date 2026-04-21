---
type: sop
domain: exception_handling
owner: operations
decision_value: high
status: verified
related_hubs:
  - Operations Strategy Hub
  - Customer Problems Hub
tags:
  - sop
  - exception
  - delay
---

# SOP - Handle Delayed Shipment

## Trigger

Shipment is behind schedule - ETA will exceed promised delivery time.

## Preconditions

- Active order in transit
- Delay detected via tracking or ETA update
- Original SLA at risk

## Steps

### Step 1: Identify Delay

```
1.1 Receive delay alert (system or manual)
1.2 Determine delay cause
1.3 Calculate new ETA
1.4 Assess SLA breach severity
```

### Step 2: Assess Options

```
2.1 Can delay be recovered? (expedite route)
2.2 Is driver intervention possible?
2.3 Can partner assist?
2.4 What is minimum unavoidable delay?
```

### Step 3: Customer Communication

```
3.1 Proactively notify customer
3.2 Explain delay reason (brief, factual)
3.3 Provide revised ETA
3.4 Offer compensation options if applicable
3.5 Confirm communication preferences
```

### Step 4: Implement Recovery

```
4.1 IF recoverable: Expedite delivery
4.2 IF unavoidable: Document reason
4.3 Monitor for further updates
4.4 Keep customer informed
```

### Step 5: Resolution

```
5.1 Confirm delivery completion
5.2 Send delivery confirmation
5.3 Apply SLA credit if applicable
5.4 Document delay for analysis
```

## Delay Categories

| Category | Cause | Typical Action |
|----------|-------|----------------|
| Traffic | Congestion | Route optimization |
| Weather | Rain/flood | Wait + resume |
| Mechanical | Breakdown | Vehicle swap |
| Documentation | E-way/expiry | Update docs |
| Operational | Scheduling | Reassign |

## Escalation

- >4 hour delay → Manager notification
- >8 hour delay → Customer manager call
- SLA breach imminent → Executive notice

## Related Scenarios

- [[Scenario - Route Blocked Due to Protests]]
- [[Scenario - Natural Disaster Impact]]

## Related Concepts

- [[Logistics SLA]]
- [[Route Deviation Risk]]

## Related Hubs

- [[Operations Strategy Hub]]
- [[Customer Problems Hub]]
