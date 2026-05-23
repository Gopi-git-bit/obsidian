# 🔄 State Machine (Locked)

> [!WARNING] Immutability
> State graph is **LOCKED**. No skipping states, no reverse transitions.
> All changes via `transition()` method only.

## 📊 Canonical State Graph

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> PAYMENT_PENDING
    DRAFT --> CANCELLED
    
    PAYMENT_PENDING --> CONFIRMED
    PAYMENT_PENDING --> FAILED
    PAYMENT_PENDING --> CANCELLED
    
    CONFIRMED --> VEHICLE_SEARCH
    CONFIRMED --> CANCELLED
    
    VEHICLE_SEARCH --> DRIVER_ASSIGNED
    VEHICLE_SEARCH --> FAILED
    
    DRIVER_ASSIGNED --> ARRIVED_PICKUP
    DRIVER_ASSIGNED --> CANCELLED
    
    ARRIVED_PICKUP --> LOADING
    ARRIVED_PICKUP --> CANCELLED
    
    LOADING --> ENROUTE
    LOADING --> CANCELLED
    
    ENROUTE --> ARRIVED_DELIVERY
    ENROUTE --> FAILED
    
    ARRIVED_DELIVERY --> POD_UPLOADED
    
    POD_UPLOADED --> DELIVERY_COMPLETED
    
    DELIVERY_COMPLETED --> SETTLEMENT_PREPROCESS
    
    SETTLEMENT_PREPROCESS --> SETTLEMENT_READY
    
    SETTLEMENT_READY --> SETTLEMENT_RELEASED
    
    SETTLEMENT_RELEASED --> CLOSED
    
    CANCELLED --> [*]
    FAILED --> [*]
    CLOSED --> [*]
```

## 🏷️ State Definitions

| State | Code | Actor | Description |
|-------|------|-------|-------------|
| **DRAFT** | `DRAFT` | OMS | Order created, awaiting payment |
| **PAYMENT_PENDING** | `PAYMENT_PENDING` | OMS | Payment initiated |
| **CONFIRMED** | `CONFIRMED` | OMS | Payment received, searching vehicle |
| **VEHICLE_SEARCH** | `VEHICLE_SEARCH` | IMS | Finding vehicle/driver |
| **DRIVER_ASSIGNED** | `DRIVER_ASSIGNED` | IMS | Vehicle and driver assigned |
| **ARRIVED_PICKUP** | `ARRIVED_PICKUP` | TMS | Driver at pickup location |
| **LOADING** | `LOADING` | TMS | Cargo being loaded |
| **ENROUTE** | `ENROUTE` | TMS | In transit to delivery |
| **ARRIVED_DELIVERY** | `ARRIVED_DELIVERY` | TMS | At delivery location |
| **POD_UPLOADED** | `POD_UPLOADED` | TMS | Proof of delivery submitted |
| **DELIVERY_COMPLETED** | `DELIVERY_COMPLETED` | TMS | Delivery confirmed complete |
| **SETTLEMENT_PREPROCESS** | `SETTLEMENT_PREPROCESS` | FIN | Calculating payouts |
| **SETTLEMENT_READY** | `SETTLEMENT_READY` | FIN | Ready for fund release |
| **SETTLEMENT_RELEASED** | `SETTLEMENT_RELEASED` | FIN | Funds transferred |
| **CLOSED** | `CLOSED` | FIN | Final state |

### Terminal States
- `CANCELLED` - Order cancelled by customer or system
- `FAILED` - Order failed (no vehicle, payment failure, etc.)
- `CLOSED` - Order completed and settled

## 🔒 Transition Rules

### Allowed Transitions (Python Dict)
```python
ORDER_STATE_GRAPH = {
    OrderState.DRAFT: {OrderState.PAYMENT_PENDING, OrderState.CANCELLED},
    OrderState.PAYMENT_PENDING: {OrderState.CONFIRMED, OrderState.FAILED, OrderState.CANCELLED},
    OrderState.CONFIRMED: {OrderState.VEHICLE_SEARCH, OrderState.CANCELLED},
    OrderState.VEHICLE_SEARCH: {OrderState.DRIVER_ASSIGNED, OrderState.FAILED},
    OrderState.DRIVER_ASSIGNED: {OrderState.ARRIVED_PICKUP, OrderState.CANCELLED},
    OrderState.ARRIVED_PICKUP: {OrderState.LOADING, OrderState.CANCELLED},
    OrderState.LOADING: {OrderState.ENROUTE, OrderState.CANCELLED},
    OrderState.ENROUTE: {OrderState.ARRIVED_DELIVERY, OrderState.FAILED},
    OrderState.ARRIVED_DELIVERY: {OrderState.POD_UPLOADED},
    OrderState.POD_UPLOADED: {OrderState.DELIVERY_COMPLETED},
    OrderState.DELIVERY_COMPLETED: {OrderState.SETTLEMENT_PREPROCESS},
    OrderState.SETTLEMENT_PREPROCESS: {OrderState.SETTLEMENT_READY},
    OrderState.SETTLEMENT_READY: {OrderState.SETTLEMENT_RELEASED},
    OrderState.SETTLEMENT_RELEASED: {OrderState.CLOSED},
}
```

### Forbidden Actions
- ❌ No skipping states (e.g., DRAFT → ENROUTE)
- ❌ No reverse transitions (e.g., ENROUTE → DRIVER_ASSIGNED)
- ❌ No jumping to terminal states (except via defined paths)
- ❌ No state change without `idempotency_key`

## 🔐 Transition Method

```python
def transition(self, new_state: OrderState, *, actor: str, event: str, idempotency_key: str):
    """THE ONLY WAY to change order state."""
    current = OrderState(self.state)
    
    # Idempotent retry protection
    if self.last_idempotency_key == idempotency_key:
        return self  # Already processed
    
    # Validate transition
    allowed = ORDER_STATE_GRAPH.get(current, set())
    if new_state not in allowed:
        raise ValidationError(
            f"Illegal state transition: {current} → {new_state}"
        )
    
    # Execute transition
    self.state = new_state
    self.last_event = event
    self.last_actor = actor
    self.last_idempotency_key = idempotency_key
    self.save()
    
    # Create audit event
    OrderEvent.objects.create(
        order=self,
        event_type=event,
        from_state=old_state,
        to_state=new_state,
        actor=actor,
        idempotency_key=idempotency_key
    )
```

## 📝 Audit Trail (Hash-Chained)

Every state change creates an immutable `OrderEvent` record:

| Field | Purpose |
|-------|---------|
| `event_type` | What happened (e.g., `driver_assigned`) |
| `from_state` | Previous state |
| `to_state` | New state |
| `actor` | Who/what made the change (OMS, IMS, TMS, FIN) |
| `idempotency_key` | Unique key for retry protection |
| `payload_hash` | SHA-256 of payload |
| `prev_hash` | Hash of previous event |
| `chain_hash` | Hash(prev_hash + payload_hash) |

> [!INFO] Tamper Detection
> Any modification to audit logs breaks the hash chain, making tampering detectable.

## 🔗 Related Notes
- [[02_Agentic_AI_Application]] - Agent responsibilities
- [[08_Database_Schema]] - Order, OrderEvent models
- [[03_ReturnTrip_Algorithm]] - DELIVERY_COMPLETED trigger

---
*Status: 🟢 Locked*
*Implementation: MiniMax Agent Generated*
