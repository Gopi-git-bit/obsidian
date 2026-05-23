# 🚛 Return Trip Algorithm (IMS v1)

> [!INFO] Overview
> Deterministic return-trip matching logic to reduce empty-leg kilometers.
> **Authority:** [[02_Agentic_AI_Application]] (IMS Agent)
> **Constraint:** No state mutation, Metadata only (`loop_group_id`)

## 🧮 Scoring Formula
The IMS Agent scores candidates based on weighted determinants:

$Score = (Dist_{score} \times 0.4) + (Time_{score} \times 0.3) + (Fit_{bonus}) + (Corridor_{bonus})$

| Component       | Logic                            | Weight  |
| :-------------- | :------------------------------- | :------ |
| **Distance**    | `max(0, (max_radius - dist_km))` | 40%     |
| **Time Window** | `max(0, (max_wait - wait_min))`  | 30%     |
| **Vehicle Fit** | Exact model match                | +20 pts |
| **Corridor**    | Drop zone == Next Pickup zone    | +15 pts |

## ⚙️ Operational Rules
1. **Trigger:** `DELIVERY_COMPLETED` event on Outbound Order.
2. **Search Radius:** Default 30km from Drop Location.
3. **Wait Window:** Max 180 minutes after outbound completion.
4. **Threshold:** Minimum score of **40** to generate offer.
5. **Safety:**
   - ❌ No auto-acceptance.
   - ❌ No state change until Offer Accepted.
   - ✅ Idempotent offer creation.

## 🔧 Implementation (IMS Agent)

### Haversine Distance Calculation
```python
def haversine_km(self, lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth radius
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c
```

### Return Trip Discovery Algorithm
```python
def find_return_trip(self, completed_order_id: str) -> dict:
    # Get drop location from completed order
    drop_lat = completed_order.drop_location.y
    drop_lng = completed_order.drop_location.x
    
    # Search parameters
    max_radius_km = 30
    max_wait_minutes = 180
    
    # Find candidates in DRAFT or PAYMENT_PENDING state
    candidates = Order.objects.filter(
        state__in=[OrderState.DRAFT, OrderState.PAYMENT_PENDING],
        pickup_scheduled_at__gte=earliest,
        pickup_scheduled_at__lte=latest,
        vehicle_type=completed_order.vehicle_type,
        loop_group_id__isnull=True,
    ).exclude(id=completed_order_id)[:10]
    
    # Score each candidate
    for cand in candidates:
        dist = self.haversine_km(drop_lat, drop_lng, pickup_lat, pickup_lng)
        if dist > max_radius_km:
            continue
        
        score = 0.0
        score += max(0, (max_radius_km - dist)) * 0.4  # Distance
        score += max(0, (max_wait_minutes - wait_min)) * 0.3  # Time
        
        if cand.vehicle_model == completed_order.vehicle_model:
            score += 20  # Vehicle fit bonus
        
        if cand.pickup_city == completed_order.drop_city:
            score += 15  # Corridor bonus
        
        if score >= 40:
            scored.append((cand, score, dist, wait_min))
    
    # Create offer for best match
    if scored:
        best = sorted(scored, key=lambda x: x[1], reverse=True)[0]
        offer = ReturnTripOffer.objects.create(
            outbound_order=completed_order,
            return_order=best[0],
            loop_group_id=uuid.uuid4(),
            discount_pct=20,
            expires_at=timezone.now() + timedelta(minutes=20),
            total_score=best[1]
        )
```

## 🔁 Loop Metadata Structure
When matched, orders are linked via `loop_group_id`:
```json
{
  "loop_group_id": "uuid",
  "outbound_order_id": "uuid",
  "return_order_id": "uuid",
  "discount_pct": 20,
  "is_return_leg": true
}
```

## 📊 v1 vs v2 Comparison

| Feature            | v1 (Deterministic)     | v2 (VRP Optimizer)           |
| :----------------- | :--------------------- | :--------------------------- |
| **Scope**          | 1 Order at a time      | Entire Fleet (100+ orders)   |
| **Efficiency**     | Local Max              | Global Max                   |
| **Empty Miles**    | Reduces by ~15%        | Reduces by ~30-40%           |
| **Latency**        | < 100ms                | 5-30 seconds                 |
| **Explainability** | High (visible formula) | Low (black-box)              |
| **Debuggability**  | Easy (log score: 45.2) | Hard (constraint violations) |

> [!TIP] Launch Strategy
> Launch with v1 (Deterministic) for stability. Upgrade to v2 (VRP) after scale.

## 🔗 Related Notes
- [[02_Agentic_AI_Application]] - IMS Agent implementation
- [[07_State_Machine]] - DELIVERY_COMPLETED trigger
- [[01_Business_Model]] - Loop economics

---
*Status: 🟢 Locked*
*Implementation: MiniMax Agent Generated*
