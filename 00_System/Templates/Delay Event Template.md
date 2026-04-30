---
type: delay_event_template
lane_id:
shipment_id:
order_id:
leg_id:
origin:
destination:
cargo_type:
vehicle_type:
carrier_id:
driver_id:
primary_delay_stage:
root_cause_code:
pickup_delay_min: 0
transit_delay_min: 0
terminal_dwell_delay_min: 0
documentation_delay_min: 0
last_mile_delay_min: 0
exception_count: 0
resolution_time_min:
gps_coverage_pct:
delivered_on_time:
delivered_in_full:
damaged: false
data_confidence: medium
event_date:
idempotency_key:
---
# Delay Event: {{lane_id}} / {{shipment_id}}

## Delay Summary

| Stage | Delay Minutes | Root Cause | Notes |
|---|---:|---|---|
| Pickup | {{pickup_delay_min}} |  |  |
| Transit | {{transit_delay_min}} |  |  |
| Terminal dwell | {{terminal_dwell_delay_min}} |  |  |
| Documentation | {{documentation_delay_min}} |  |  |
| Last mile | {{last_mile_delay_min}} |  |  |

## Operational Impact

| Metric | Value |
|---|---|
| Delivered on time | {{delivered_on_time}} |
| Delivered in full | {{delivered_in_full}} |
| Damaged | {{damaged}} |
| Exception count | {{exception_count}} |
| Resolution time | {{resolution_time_min}} |
| GPS coverage | {{gps_coverage_pct}} |

## Corrective Action

- [ ] Identify preventable cause
- [ ] Update lane scorecard if recurring
- [ ] Notify matching/pricing/risk agent if needed
- [ ] Add ops note if manual intervention was required
