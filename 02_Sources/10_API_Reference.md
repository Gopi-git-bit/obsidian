# 🔌 API Reference

> [!INFO] Architecture
> RESTful API via Django REST Framework
> Documentation: drf-spectacular (OpenAPI 3.0)

## 🔐 Authentication
- **Method:** JWT Token / OTP-based
- **Header:** `Authorization: Bearer <token>`
- **Rate Limiting:** Via Kong Gateway

## 📦 Order Management

### Create Order
```
POST /api/orders/
```

**Request Body:**
```json
{
  "pickup_address": "123 Industrial Area, Delhi",
  "pickup_city": "Delhi",
  "pickup_pincode": "110001",
  "drop_address": "456 Tech Park, Bangalore",
  "drop_city": "Bangalore",
  "drop_pincode": "560001",
  "cargo_type": "Electronics",
  "weight_kg": 500,
  "vehicle_type": "CLOSED",
  "pickup_scheduled_at": "2026-04-05T10:00:00Z"
}
```

**Response:**
```json
{
  "order_id": "uuid",
  "state": "DRAFT",
  "trace_id": "uuid"
}
```

### Get Order Details
```
GET /api/orders/{id}/
```

**Response:**
```json
{
  "order_id": "uuid",
  "state": "ENROUTE",
  "customer_id": "uuid",
  "vehicle": {
    "id": "uuid",
    "registration_number": "KA01AB1234",
    "vehicle_type": "CLOSED"
  },
  "driver": {
    "id": "uuid",
    "name": "Raj Kumar",
    "phone": "+91-9876543210"
  },
  "pickup_address": "...",
  "drop_address": "...",
  "base_fare": 15000.00,
  "final_fare": 15000.00,
  "promised_pickup_at": "2026-04-05T10:00:00Z",
  "promised_delivery_at": "2026-04-06T18:00:00Z",
  "loop_group_id": null,
  "is_return_leg": false
}
```

### State Transition
```
POST /api/orders/{id}/transition/
```

**Request Body:**
```json
{
  "new_state": "DRIVER_ASSIGNED",
  "event": "driver_assigned",
  "idempotency_key": "unique-key-123"
}
```

**Response:**
```json
{
  "order_id": "uuid",
  "state": "DRIVER_ASSIGNED",
  "event": "driver_assigned",
  "actor": "IMS",
  "timestamp": "2026-04-04T15:30:00Z"
}
```

### Cancel Order
```
POST /api/orders/{id}/cancel/
```

**Request Body:**
```json
{
  "reason": "Customer request"
}
```

## 🚛 Vehicle & Driver

### List Available Vehicles
```
GET /api/vehicles/?vehicle_type=CLOSED&min_weight=500
```

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": "uuid",
      "registration_number": "KA01AB1234",
      "vehicle_type": "CLOSED",
      "vehicle_model": "Tata Prima",
      "max_weight_kg": 25000,
      "status": "AVAILABLE",
      "current_location": {
        "lat": 12.9716,
        "lng": 77.5946
      }
    }
  ]
}
```

### List Drivers
```
GET /api/drivers/?status=ONLINE
```

## 🔄 Return Trip

### Get Return Trip Matches
```
GET /api/return-trip/match/?completed_order_id={uuid}
```

**Response:**
```json
{
  "matched": true,
  "offer_id": "uuid",
  "return_order_id": "uuid",
  "confidence": 72.5,
  "loop_group_id": "uuid",
  "discount_pct": 20,
  "distance_km": 12.5,
  "expires_at": "2026-04-04T16:00:00Z"
}
```

### Accept Return Trip Offer
```
POST /api/return-trip/accept/
```

**Request Body:**
```json
{
  "offer_id": "uuid"
}
```

## 💰 Payments

### Initiate Payment
```
POST /api/payments/initiate/
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "amount": 15000.00,
  "payment_method": "UPI"
}
```

**Response:**
```json
{
  "payment_id": "uuid",
  "order_id": "uuid",
  "amount": 15000.00,
  "status": "PENDING",
  "payment_url": "https://payment-gateway/..."
}
```

### Payment Webhook
```
POST /api/payments/webhook/
```

**Request Body:**
```json
{
  "payment_id": "uuid",
  "status": "SUCCESS",
  "transaction_id": "TXN123456",
  "signature": "sha256-hash"
}
```

## 📍 Tracking & Telemetry

### Update GPS Location
```
POST /api/telemetry/
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "vehicle_id": "uuid",
  "driver_id": "uuid",
  "lat": 12.9716,
  "lng": 77.5946,
  "speed": 45.5,
  "accuracy": 10.0
}
```

### Get Order Tracking
```
GET /api/orders/{id}/tracking/
```

**Response:**
```json
{
  "order_id": "uuid",
  "state": "ENROUTE",
  "current_location": {
    "lat": 15.9129,
    "lng": 79.7400
  },
  "eta_minutes": 180,
  "distance_remaining_km": 350,
  "last_updated": "2026-04-04T15:30:00Z"
}
```

## 📊 Settlements

### Get Settlement Status
```
GET /api/settlements/{order_id}/
```

**Response:**
```json
{
  "order_id": "uuid",
  "settlement_id": "uuid",
  "status": "COMPLETED",
  "base_fare": 15000.00,
  "discount": 3000.00,
  "gst": 2160.00,
  "final_fare": 14160.00,
  "transporter_payout": 11000.00,
  "driver_payout": 2000.00,
  "platform_commission": 1160.00,
  "processed_at": "2026-04-07T10:00:00Z"
}
```

## 🚨 Disputes

### Create Dispute
```
POST /api/disputes/
```

**Request Body:**
```json
{
  "order_id": "uuid",
  "dispute_type": "DELIVERY_DELAY",
  "description": "Delivery was 2 hours late"
}
```

### Get Dispute Status
```
GET /api/disputes/{id}/
```

## 📋 Error Responses

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 400  | Bad Request - Invalid data              |
| 401  | Unauthorized - Invalid token            |
| 403  | Forbidden - Insufficient permissions    |
| 404  | Not Found - Resource doesn't exist      |
| 409  | Conflict - State transition invalid     |
| 422  | Unprocessable - Business rule violation |
| 429  | Too Many Requests - Rate limited        |
| 500  | Internal Error - Server issue           |

**Error Response Format:**
```json
{
  "error": {
    "code": "STATE_TRANSITION_INVALID",
    "message": "Cannot transition from ENROUTE to DRIVER_ASSIGNED",
    "details": {
      "current_state": "ENROUTE",
      "requested_state": "DRIVER_ASSIGNED",
      "allowed_transitions": ["ARRIVED_DELIVERY", "FAILED"]
    }
  },
  "trace_id": "uuid"
}
```

## 🔗 Related Notes
- [[07_State_Machine]] - State transition rules
- [[02_Agentic_AI_Application]] - Agent API calls
- [[06_Tech_Stack_Architecture]] - API Gateway (Kong)

---
*Status: 🟢 Production API*
*Implementation: MiniMax Agent Generated*
