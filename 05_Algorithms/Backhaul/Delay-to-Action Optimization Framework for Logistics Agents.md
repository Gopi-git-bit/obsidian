---
type: operating_framework
domain: delay_to_action_optimization
status: active
created_at: 2026-04-30
linked_notes:
  - "Traffic Signal Delay Metrics Analogy for Logistics Reliability"
  - "Common Delay Metrics for South India Transportation Planning"
  - "Lane Reliability Scorecard for Return Trip Promise Engine"
---
# Delay-to-Action Optimization Framework for Logistics Agents

## Purpose

Traffic signal engineers improve intersections by translating delay components into timing adjustments.

Zippy should improve freight execution by translating delay components into operational adjustments.

```text
Traffic signal: delay component -> cycle, split, offset, phase, actuation
Zippy freight: delay component -> SLA, dispatch slot, route, hub, carrier, price, escalation
```

## Core Principle

```text
Delay is a diagnostic signal, not just a KPI.
```

Every recurring delay should answer two questions:

```text
1. What exactly caused the delay?
2. Which operational lever should change?
```

## Traffic-to-Logistics Translation

| Signal Optimization Lever | Freight Equivalent |
|---|---|
| Cycle length | Trip cycle time and route buffer |
| Green split | Capacity allocation by lane/customer/cargo |
| Offset | Handoff timing between legs/hubs |
| Phasing | Shipment sequence and loading priority |
| Actuation | Real-time dispatch adjustment based on live data |
| Adaptive signal control | Dynamic routing/pricing/control tower intervention |

## Delay Metric to Freight Action Mapping

| Delay Pattern | What It Reveals | Primary Zippy Lever | Expected Impact |
|---|---|---|---|
| High pickup delay | Origin loading process is unreliable | Slot booking, shipper readiness checklist, loading SLA | Reduces first-leg cascade delay |
| High transit delay | Route has congestion, weather, breakdown or driver-hour risk | Route buffer, alternate route, backup carrier | Improves ETA reliability |
| High terminal dwell | Hub/port/warehouse handoff bottleneck | Pre-clearance, alternate hub, appointment scheduling | Reduces idle time and missed next load |
| High documentation delay | E-way bill, invoice, POD or compliance friction | Pre-trip document checklist, admin verification | Prevents avoidable dispatch holds |
| High last-mile delay | Consignee/unloading/address issue | Consignee notification, unloading slot, geofence validation | Reduces customer-facing late delivery |
| High P90/P95 delay | Bad-day risk is too high | Wider SLA, risk premium, human approval | Avoids overpromising |
| High delay variance | Lane is unpredictable | Block premium SLA, use only flexible cargo | Protects trust and margin |
| High handoff wait | Triangle timing is poorly coordinated | Adjust B -> C load window or choose different C-node | Improves revenue per vehicle day |
| High carryover backlog | Previous slot affects next cycle | Check hub backlog before dispatch | Prevents cascading failures |

## Component Diagnosis Rules

Borrowing from signal delay decomposition:

```text
If normal delay dominates -> tune baseline operating plan.
If overflow delay dominates -> add capacity or suppress demand.
If carryover delay dominates -> fix coordination and backlog.
```

Translated for freight:

| Delay Component | Freight Meaning | Agent Diagnosis | Agent Action |
|---|---|---|---|
| Normal recurring delay | Lane always needs more buffer | Baseline SLA too tight | Increase standard buffer |
| Overflow delay | Demand exceeds vehicle/hub capacity | Capacity constrained | Add partner carrier or surge price |
| Carryover delay | Previous shipment/hub delay affects next load | Poor chain coordination | Re-time handoff or break chain |
| Stopped/idle delay | Driver waits too long at a node | Node bottleneck | Slot booking, demurrage, alternate node |
| Queue delay | Too many vehicles at same hub/window | Hub congestion | Stagger appointments |

## Closed-Loop Optimization Workflow

```text
1. Capture stage-level delay event
2. Attribute root cause
3. Aggregate by directed lane + cargo + vehicle
4. Detect recurring delay pattern
5. Map pattern to operational lever
6. Apply agent action
7. Validate over 2-4 week window
8. Keep, adjust, or rollback rule
```

## Agent Rules

```yaml
delay_to_action_rules:
  - trigger: "pickup_delay_min_p90 > 90"
    diagnosis: "origin readiness problem"
    actions:
      - "require shipper readiness checklist"
      - "add pickup buffer"
      - "warn customer about loading SLA"

  - trigger: "terminal_dwell_delay_min_p90 > 120"
    diagnosis: "hub or port bottleneck"
    actions:
      - "require appointment slot"
      - "pre-clear documents"
      - "evaluate alternate hub"

  - trigger: "documentation_delay_min_avg > 30"
    diagnosis: "document workflow friction"
    actions:
      - "send e-way bill checklist before dispatch"
      - "hold trip start until mandatory docs verified"
      - "notify admin agent"

  - trigger: "p90_delay_min > customer_sla_buffer"
    diagnosis: "promise risk"
    actions:
      - "block tight SLA"
      - "apply risk premium"
      - "escalate to control tower"

  - trigger: "handoff_wait_min > 360 on triangle route"
    diagnosis: "poor cargo-wave coordination"
    actions:
      - "choose different C-node"
      - "search later B_to_C load"
      - "compare against direct return"

  - trigger: "delay_variance_high and cargo_time_sensitive = true"
    diagnosis: "unpredictable lane unsuitable for premium cargo"
    actions:
      - "reject lane for premium SLA"
      - "recommend alternate mode or route"
```

## Triangle Route Timing Optimization

A triangle route works like a coordinated signal corridor. Each leg must arrive in time for the next green window.

```text
Leg 1: A -> B must arrive before B -> C load window closes
Leg 2: B -> C must arrive before C -> A feeder load window closes
Leg 3: C -> A must finish before driver, vehicle, payment or customer constraints break
```

If one leg repeatedly misses its window, do not only add buffer. First diagnose whether the issue is:

| Issue | Better Fix |
|---|---|
| B-node waiting | Change B pickup slot or C-node candidate |
| C-node feeder unavailable | Use return-to-cluster instead of exact return |
| Documentation delay | Pre-clear docs before Leg 1 completion |
| Transit variance | Choose more reliable lane even if distance is longer |
| Driver hour risk | Split route or assign different vehicle |

## Zippy Operating Levers

| Lever | When to Use |
|---|---|
| Increase SLA buffer | Delay is predictable and acceptable |
| Add backup carrier | Lane has moderate reliability risk |
| Change C-node | Triangle handoff wait is too high |
| Apply pricing premium | Delay risk consumes capacity/margin |
| Add demurrage clause | Node waiting is recurring and controllable by customer/hub |
| Block auto-match | Delay risk is too high or data confidence is low |
| Escalate to control tower | Cargo is time-sensitive, high-value or compliance-sensitive |
| Change mode | Road delay is structurally unreliable for promised SLA |

## Validation Window

For any new rule, validate over 2-4 weeks.

| Metric | Success Signal |
|---|---|
| avg delay | Down 10 percent or more |
| P90 delay | Down 15 percent or more |
| missed handoff windows | Down 20 percent or more |
| revenue per vehicle day | Up 10-15 percent or more |
| customer complaints | Not increased |
| driver idle time | Down 15 percent or more |

## MVP Application

Apply this framework to the first three triangle experiments:

| Triangle | Primary Delay Lever to Watch |
|---|---|
| Tiruppur -> Chennai -> Coimbatore -> Tiruppur | Port/warehouse dwell and B -> C handoff wait |
| Erode -> Chennai -> Coimbatore -> Erode | Chennai pickup queue and Coimbatore feeder timing |
| Bengaluru -> Sri City -> Chennai -> Bengaluru | JIT slot miss, border/documentation delay and offset timing |

## Takeaway

The mature version of Zippy will not simply record that a shipment was late.

It will know which lever to pull next.

That is the difference between a dashboard and an operating system.
