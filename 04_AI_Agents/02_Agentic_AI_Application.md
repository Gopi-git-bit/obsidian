# 🤖 Agentic AI Application

> [!WARNING] Governance
> Agents **NEVER** mutate DB state directly.
> Agents **NEVER** move money without approval.
> All actions flow through [[07_State_Machine]] via `transition()` method.

## 🏗 Agent Inventory

| Agent          | Code      | Role                               | Forbidden Actions                |
| :------------- | :-------- | :--------------------------------- | :------------------------------- |
| **Supervisor** | `SUP`     | Arbitration, Safety, Overrides     | Changing state, Issuing refunds  |
| **OMS**        | `OMS`     | Order Lifecycle, Return Offers     | Assign vehicles, Settle payments |
| **IMS**        | `IMS`     | Vehicle Matching, Return Discovery | Accept trips, Apply discounts    |
| **TMS**        | `TMS`     | Routing, ETA, SLA Monitoring       | Reassign drivers, Change pricing |
| **Finance**    | `FIN`     | Settlement, Refund Execution       | Approve disputes, Change state   |
| **Dispute AI** | `DISPUTE` | Scoring, Refund Recommendations    | Issue refunds, Close disputes    |

## 🧠 Agent Implementation Details

### OMS Agent (Order Management)
**File:** `backend/agents/oms_agent.py`

| Method               | Purpose                            | State Transition            |
| -------------------- | ---------------------------------- | --------------------------- |
| `create_order()`     | Create order in DRAFT state        | → DRAFT                     |
| `initiate_payment()` | Start payment flow                 | DRAFT → PAYMENT_PENDING     |
| `confirm_order()`    | Confirm after payment, trigger IMS | PAYMENT_PENDING → CONFIRMED |
| `cancel_order()`     | Cancel from valid states           | → CANCELLED                 |
| `get_order_status()` | Get order history                  | Read-only                   |

### IMS Agent (Inventory & Matching)
**File:** `backend/agents/ims_agent.py`

| Method                     | Purpose                         | Output                                 |
| -------------------------- | ------------------------------- | -------------------------------------- |
| `search_vehicle()`         | Find available vehicle/driver   | `{matched, vehicle_id, driver_id}`     |
| `find_return_trip()`       | Discover return trip candidates | `{matched, offer_id, score, discount}` |
| `check_vehicle_capacity()` | Validate cargo capacity         | `{can_accept, max_weight, max_volume}` |

**Key Algorithm:** Haversine distance calculation for geo-matching:
```python
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    # Returns distance between two coordinates
```

### TMS Agent (Transportation)
**File:** `backend/agents/tms_agent.py`

| Method                 | Purpose                  | State Transition                  |
| ---------------------- | ------------------------ | --------------------------------- |
| `start_shipment()`     | Driver arrives at pickup | DRIVER_ASSIGNED → ARRIVED_PICKUP  |
| `start_loading()`      | Begin loading cargo      | ARRIVED_PICKUP → LOADING          |
| `start_transit()`      | Depart for delivery      | LOADING → ENROUTE                 |
| `arrive_delivery()`    | Arrive at drop location  | ENROUTE → ARRIVED_DELIVERY        |
| `upload_pod()`         | Upload proof of delivery | ARRIVED_DELIVERY → POD_UPLOADED   |
| `complete_delivery()`  | Mark delivery complete   | POD_UPLOADED → DELIVERY_COMPLETED |
| `check_sla_breaches()` | Monitor SLA violations   | Read-only, creates breach records |

**SLA Rules (Locked):**
| Breach Type | Threshold | Grace Period |
|-------------|-----------|--------------|
| PICKUP_DELAY | 30 min | 15 min |
| DELIVERY_DELAY | 60 min | 30 min |
| POD_DELAY | 120 min | None |
| ROUTE_DEVIATION | 15% extra km | None |

### Finance Agent
**File:** `backend/agents/finance_agent.py`

| Method                      | Purpose                 | State Transition                           |
| --------------------------- | ----------------------- | ------------------------------------------ |
| `preprocess_settlement()`   | Calculate payouts       | DELIVERY_COMPLETED → SETTLEMENT_PREPROCESS |
| `ready_settlement()`        | Mark ready for release  | SETTLEMENT_PREPROCESS → SETTLEMENT_READY   |
| `release_settlement()`      | Transfer funds          | SETTLEMENT_READY → SETTLEMENT_RELEASED     |
| `close_order()`             | Final state             | SETTLEMENT_RELEASED → CLOSED               |
| `calculate_loop_discount()` | 20% return leg discount | Read-only calculation                      |
| `process_refund()`          | Execute approved refund | Creates Refund record                      |

**Loop Discount Logic:**
- Return leg orders (`is_return_leg=True`) get **20% discount**
- Linked via `loop_group_id` to outbound order

## 🕸 Orchestration Flow (LangGraph + n8n)
1. **Event Trigger** (Webhook/DB Trigger)
2. **Agent Reasoning** (Deep Agent / LLM)
3. **n8n Workflow** (Validation, Retry, DLQ)
4. **State Machine** (Django Backend - `transition()` method)
5. **Audit Log** (Immutable Hash Chain - `OrderEvent` model)

## 🛡 Safety Guards
- **Idempotency:** Every agent output requires `idempotency_key`.
- **DLQ:** Permanent failures go to Dead Letter Queue (Supabase).
- **Shadow Mode:** New models run in parallel before activation.
- **Human-in-the-Loop:** Refunds > Cap or SEV-1 incidents require Admin.

## 🧠 Memory & Context
- **Storage:** `pgvector` (Supabase)
- **Namespace:** Segregated per agent (e.g., `oms_rules`, `dispute_history`)
- **Retention:** 90 Days Hot, 1 Year Cold Archive.

## 🔗 Related Notes
- [[03_ReturnTrip_Algorithm]] - IMS scoring formula
- [[07_State_Machine]] - Full state graph
- [[08_Database_Schema]] - Order, OrderEvent models
- [[01_Business_Model]] - Revenue logic

---
*Status: 🟢 Governance Locked*
*Implementation: MiniMax Agent Generated*
