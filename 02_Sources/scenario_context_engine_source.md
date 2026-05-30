---
type: source
status: processed
domain: logistics
origin: user_provided
processed: true
created: 2026-05-30
source_file: D:\all partiipnts role.txt
notes: First scenario-context-engine draft for AI-agent decision clarity across pricing, city density, return-load risk, participant context, and scenario-based quote behavior
---

# Scenario Context Engine Source

## Overview

This source captures the first draft of a scenario context engine for Zippy Logistics. The core idea is that AI agents act better when they receive connected operational context, not isolated facts. Scenario management should tell the agent what situation it is in, which participants are involved, what pricing and routing variables matter, and which decision rules are allowed.

The strongest example in this draft is dynamic logistics pricing. Pricing cannot be a free-form AI answer. It must be a deterministic, auditable calculation that uses city tier, network density, demand, traffic, fixed vehicle costs, driver cost, and return-load risk.

## Core Takeaways

### 1. Scenario Management Gives Agents Context

AI agents need context about:

- participant role and responsibility
- city tier and surrounding logistics network
- vehicle demand and supply pressure
- traffic congestion and operating-time cost
- return-load or deadhead probability
- payment, audit, and state-machine constraints

Without those relationships, agents may retrieve correct facts but still fail to combine them into a useful decision.

### 2. Connected Data Beats Isolated Data

A large domain-specific database is valuable only when facts are connected. Low-conflict data improves reliability, but low-interrelation limits deep analysis. The recommended direction is a knowledge-graph layer that connects customers, cities, lanes, vehicles, drivers, transport companies, policies, risks, and outcomes.

This turns a pile of facts into a map of knowledge that agents can reason over.

### 3. Pricing Is a Scenario Decision, Not Only a Rate Table

Prices vary by location because demand, driver salary, traffic congestion, industrialization, vehicle availability, and return-load probability vary by location. Fuel, maintenance, insurance, and vehicle cost are broadly common fixed inputs, but local operating context changes the actual quote.

The source frames pricing as:

```text
P = (fixed cost + variable cost) * (1 + tier multiplier + density multiplier + risk adjustments)
```

The AI agent should orchestrate this calculation but should not invent the price.

## Pricing Context Variables

| Variable | Role in Scenario Context |
|---|---|
| City tier | Distinguishes Tier-1, Tier-2, and Tier-3 price behavior |
| Urbanization density | Measures nearby demand and operating complexity |
| Demand volume | Higher demand increases vehicle hiring pressure |
| Driver salary | Key local cost factor next to demand and traffic |
| Traffic congestion | Raises time cost and opportunity cost |
| Fixed vehicle costs | Fuel, maintenance, insurance, vehicle price, fitness, and depreciation baseline |
| Nearby city network | Shows whether a city belongs to a high-activity cluster |
| Return-load probability | Prevents underpricing isolated lanes with empty return risk |

## Radius-Based City Network Rules

| Radius / Condition | Scenario Meaning | Pricing Treatment |
|---|---|---|
| High density within 100 km | City is influenced by nearby hub demand | Raise demand and congestion context |
| Low density within 30 km | City has weak local demand | Check return-load risk before discounting |
| Many Tier-1/2/3 cities within 500 km | High-activity cluster | Use maximum or premium pricing slab |
| Tier-2 near 1-2 Tier-1 cities within 500 km and 5-7 Tier-2/3 cities within 200 km | Satellite Tier-2 market | Set around 20% below Tier-1 slab |
| Tier-3 within 500 km of only one Tier-1 and one or two Tier-2 cities | Lower-density Tier-3 market | Set around 20% below Tier-2 slab before risk correction |
| Tier-3 far from Tier-1 and weakly connected to Tier-2 trade | Rural/low-density market | Apply 10-15% below Tier-3 slab only if return load exists |
| Tier-3 between two Tier-1 cities, harbours, or high-growth Tier-2 cities | Hidden high-potential market | Treat closer to Tier-2 slab |

## Return-Load Correction Rule

The source adds an important correction: low demand does not always mean a lower price. If a vehicle goes to an isolated Tier-3 city and cannot find a return load, the quote must cover deadhead risk.

| Return-Load Probability | Interpretation | Pricing Action |
|---|---|---|
| 0.8-1.0 | Strong backhaul market, common in Tier-1 clusters | Keep normal slab; no deadhead surcharge |
| 0.4-0.8 | Moderate uncertainty | Price with caution and monitor lane data |
| <0.4 | Low backhaul probability | Apply deadhead surcharge, source example uses 40% |
| <0.3 | Very weak return-load market | Require manual review or strong surcharge logic |

This prevents the AI agent from giving a low Tier-3 quote that causes the platform or driver to lose money on the empty return journey.

## Agent Decision Flow

1. Identify the order scenario: city pair, vehicle type, weight, distance, service urgency, customer segment, and payment mode.
2. Classify origin and destination city tiers.
3. Scan city-network density at 30 km, 100 km, 200 km, and 500 km radii.
4. Calculate fixed and variable cost baseline.
5. Apply tier and density rules.
6. Estimate return-load probability.
7. Apply deadhead surcharge when return-load probability is low.
8. Apply customer segment, VAS, GST, and approved policy adjustments.
9. Return an explainable quote with reason codes.
10. Log the decision in audit history; the frontend should receive only the approved quote output, not raw pricing logic.

## Participant and Context Signals to Preserve

Future drafts should continue capturing participant roles because different actors change the scenario meaning:

| Context Signal | Why It Matters |
|---|---|
| Customer / consignor | Owns demand, shipment details, payment intent, and quote acceptance |
| Consignee | Affects delivery confirmation, ToPay consent, and destination communication |
| Driver | Affects availability, route execution, document capture, and POD evidence |
| Vehicle owner | Affects asset responsibility, vehicle condition, and operating cost |
| Transport company | Provides emergency capacity, partner pool, and possible dual-role behavior |
| OMS Agent | Owns order validation, quote orchestration, and state-safe decisions |
| Pricing / Payment Agent | Calculates quote, commission, GST, invoice, and settlement implications |
| Communication Agent | Delivers explanation, retry, and escalation messages |
| Admin / Ops | Approves overrides, reviews high-risk pricing, and handles exception policy |

## Source Handling Notes

- Treat this as the first source in a larger scenario-management drafting sequence.
- Do not merge it directly into the canonical [[Scenario Management Framework]] until the remaining drafts are collected.
- Use it to enrich future scenario-management, pricing, agent-orchestration, and knowledge-graph notes.
- Keep the code snippets below as reference material; they are not implemented by this source note.

## Derived Notes

- [[Scenario Management Framework]]
- [[Dynamic Pricing Logic]]
- [[Pricing Engine Backtest v1]]
- [[Autonomous Logistics Execution Architecture]]
- [[02_Agentic_AI_Application]]

## Related Notes

- [[pricing_engine_architecture_source]]
- [[Distance Based Pricing]]
- [[Return Load Optimization]]
- [[Hub-Aware Return Trip Matching]]
- [[Fallback & Resilience Architecture]]

## Appendix - Preserved Implementation Snippets

### A. Urbanization-Based Pricing Simulation

```python
class LogisticsPricingEngine:
    def __init__(self, cities_data):
        self.cities = cities_data # List of city dictionaries
        self.base_tier1_price = 1000  # Baseline price for a Tier-1 Hub


    def get_distance(self, city_a, city_b):
        # In a real app, this would use GPS coordinates or a distance matrix
        return city_a['distances'].get(city_b['name'], 9999)


    def calculate_price(self, target_city_name):
        target = next(c for c in self.cities if c['name'] == target_city_name)
        
        # 1. Scan the Radius for nearby cities (Your Density Logic)
        tier1_nearby_500km = [c for c in self.cities if self.get_distance(target, c) <= 500 and c['tier'] == 1]
        tier2_3_nearby_200km = [c for c in self.cities if self.get_distance(target, c) <= 200 and c['tier'] in [2, 3]]


        # 2. Apply your Logic Tree Rules
        
        # RULE 1: High Density Cluster (Tier-1 or surrounded by many cities)
        if target['tier'] == 1 or len(tier1_nearby_500km) >= 3:
            final_price = self.base_tier1_price
            slab = "Maximum Slab (Tier-1 / High Cluster)"


        # RULE 2: Tier-2 Satellite (Nearby 1-2 Tier-1 cities + several Tier-2/3)
        elif target['tier'] == 2 and 1 <= len(tier1_nearby_500km) <= 2:
            # Set price 20% below Tier-1
            final_price = self.base_tier1_price * 0.80
            slab = "Mid-Slab (Tier-2 Satellite - 20% off Tier-1)"


        # RULE 3: Isolated Tier-3 (Only 1 Tier-1 nearby)
        elif target['tier'] == 3:
            # Set price 20% below Tier-2 (which is 0.8 * 0.8 = 0.64 of Tier-1)
            tier2_price = self.base_tier1_price * 0.80
            final_price = tier2_price * 0.80
            slab = "Economy Slab (Tier-3 Isolated - 20% off Tier-2)"
            
        else:
            final_price = self.base_tier1_price * 0.50 # Default baseline
            slab = "Rural/Remote Slab"


        return {"city": target_city_name, "price": final_price, "slab": slab}


# --- Sample Data Set ---
city_network = [
    {"name": "Metro-City-A", "tier": 1, "distances": {"Town-B": 150, "Village-C": 450}},
    {"name": "Town-B", "tier": 2, "distances": {"Metro-City-A": 150, "Village-C": 250}},
    {"name": "Village-C", "tier": 3, "distances": {"Metro-City-A": 450, "Town-B": 250}}
]


# --- Running the AI Agent ---
engine = LogisticsPricingEngine(city_network)
for city in ["Metro-City-A", "Town-B", "Village-C"]:
    result = engine.calculate_price(city)
    print(f"City: {result['city']} | Price: {result['price']} | {result['slab']}")
```

### B. Urbanization Pricing with Deadhead Adjustment

```python
class LogisticsPricingEngine:
    def __init__(self, cities_data):
        self.cities = cities_data
        self.base_tier1_price = 1000 


    def get_distance(self, city_a, city_b):
        return city_a['distances'].get(city_b['name'], 9999)


    def calculate_price(self, target_city_name):
        target = next(c for c in self.cities if c['name'] == target_city_name)
        
        # 1. Scan Density & Return Load availability
        tier1_nearby = [c for c in self.cities if self.get_distance(target, c) <= 500 and c['tier'] == 1]
        backhaul_avail = target.get('return_load_prob', 0.5) # Default 50% if unknown


        # 2. Base Tier Logic (from your previous rules)
        if target['tier'] == 1:
            price = self.base_tier1_price
            slab = "Max Slab (Tier-1)"
        elif target['tier'] == 2:
            price = self.base_tier1_price * 0.80
            slab = "Mid-Slab (Tier-2)"
        else: # Tier 3
            price = (self.base_tier1_price * 0.80) * 0.80
            slab = "Economy Slab (Tier-3)"


        # 3. Apply the "Deadhead" Adjustment
        # If return load probability is low, we add a surcharge to cover fuel for the empty return
        deadhead_surcharge = 0
        if backhaul_avail < 0.4:
            deadhead_surcharge = price * 0.40 # Add 40% to cover the empty trip back
            slab += " + [DEADHEAD SURCHARGE]"
        
        final_price = price + deadhead_surcharge


        return {
            "city": target_city_name, 
            "base": price, 
            "surcharge": deadhead_surcharge, 
            "total": final_price, 
            "slab": slab
        }


# --- Sample Data Set with Backhaul Probability ---
city_network = [
    {"name": "Metro-Hub", "tier": 1, "return_load_prob": 0.95, "distances": {"Remote-Village": 600}},
    {"name": "Remote-Village", "tier": 3, "return_load_prob": 0.10, "distances": {"Metro-Hub": 600}}
]


# --- Running the Simulation ---
engine = LogisticsPricingEngine(city_network)
for city in ["Metro-Hub", "Remote-Village"]:
    res = engine.calculate_price(city)
    print(f"City: {res['city']} | Base: {res['base']} | Surcharge: {res['surcharge']} | Total: {res['total']} | ({res['slab']})")
```

### C. Pricing Agent Orchestration Function

```python
def calculate_quote(order):
    # Step 1: Statistical lookup
    base_cost = compute_fixed_variable_cost(order.distance_km, order.vehicle_type)


    # Step 2: Apply rule-based tier multiplier
    if is_high_density_cluster(order.destination):
        price = base_cost * 1.25  # Premium slab
    elif is_satellite_tier2(order.destination):
        price = (tier1_price * 0.80)
    else:
        price = (tier1_price * 0.80) * 0.80


    # Step 3: Apply deadhead surcharge (risk model)
    if get_return_load_probability(order.destination) < 0.4:
        price += price * 0.40


    # Step 4: Apply customer segment discount (SME/Enterprise)
    price = apply_customer_discount(price, order.customer_segment)


    # Step 5: Add VAS & GST
    price = add_vas_and_gst(price, order.vas)


    return price  # Deterministic, explainable
```

### D. PostgreSQL Schema - `city_tiers`

```sql
-- Stores static city metadata for pricing logic
CREATE TABLE city_tiers (
  city_name TEXT PRIMARY KEY,
  tier INT NOT NULL CHECK (tier IN (1, 2, 3)),
  return_load_probability FLOAT NOT NULL DEFAULT 0.5 CHECK (return_load_probability BETWEEN 0.0 AND 1.0),
  lat NUMERIC NOT NULL,
  lng NUMERIC NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);


-- Index for radius scans (PostGIS required)
CREATE EXTENSION IF NOT EXISTS postgis;
ALTER TABLE city_tiers ADD COLUMN IF NOT EXISTS geom GEOMETRY(POINT, 4326);
UPDATE city_tiers SET geom = ST_SetSRID(ST_MakePoint(lng, lat), 4326);
CREATE INDEX idx_city_tiers_geom ON city_tiers USING GIST (geom);
```

### E. PostgreSQL Schema - `pricing_rules`

```sql
-- Allows runtime tuning without code changes
CREATE TABLE pricing_rules (
  id SERIAL PRIMARY KEY,
  rule_name TEXT UNIQUE NOT NULL,
  tier INT CHECK (tier IN (1, 2, 3)),
  base_multiplier NUMERIC(4,2) NOT NULL, -- e.g., 1.00
  deadhead_surcharge_pct NUMERIC(4,2) NOT NULL DEFAULT 0.40, -- 40%
  created_at TIMESTAMPTZ DEFAULT NOW()
);


-- Seed default rules
INSERT INTO pricing_rules (rule_name, tier, base_multiplier) VALUES
('TIER_1_BASE', 1, 1.00),
('TIER_2_BASE', 2, 0.80),
('TIER_3_BASE', 3, 0.64);
```

### F. Python Pricing Function - OMS Agent

```python
# File: oms/agents/pricing_agent.py
import math
from django.db import connection
from django.conf import settings


def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)
    return 2 * R * math.asin(math.sqrt(a))


def calculate_dynamic_quote(
    origin_city: str,
    dest_city: str,
    base_cost: float  # Precomputed: fuel + tolls + driver wage
) -> dict:
    """
    Returns: {
        "base_cost": float,
        "tier_multiplier": float,
        "deadhead_surcharge": float,
        "total": float,
        "slab_description": str
    }
    """
    # 1. Get destination city tier & return_load_probability
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tier, return_load_probability, lat, lng
            FROM city_tiers
            WHERE city_name = %s
        """, [dest_city])
        dest_row = cursor.fetchone()
        if not dest_row:
            raise ValueError(f"Unknown destination city: {dest_city}")
        dest_tier, return_load_prob, dest_lat, dest_lng = dest_row


    # 2. Count nearby Tier-1 cities within 500km (PostGIS)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*)
            FROM city_tiers
            WHERE tier = 1
              AND ST_DWithin(
                  geom,
                  ST_SetSRID(ST_MakePoint(%s, %s), 4326)::GEOGRAPHY,
                  500000  -- 500 km in meters
              )
        """, [dest_lng, dest_lat])
        tier1_count = cursor.fetchone()[0]


    # 3. Apply slab logic
    if dest_tier == 1 or tier1_count >= 3:
        # Premium Slab (Tier-1 or High Cluster)
        multiplier = 1.25
        slab = "Premium Slab (Tier-1/High Cluster)"
    elif dest_tier == 2:
        # Tier-2 Satellite: 20% below Tier-1
        multiplier = 1.00  # Base cost is already Tier-1 equivalent
        base_cost = base_cost * 0.80
        slab = "Mid-Slab (Tier-2 Satellite)"
    else:  # Tier-3
        # Tier-3 Isolated: 20% below Tier-2 (64% of Tier-1)
        multiplier = 1.00
        base_cost = base_cost * 0.64
        slab = "Economy Slab (Tier-3 Isolated)"


    # 4. Apply deadhead surcharge if return load probability is low
    deadhead_surcharge = 0.0
    if return_load_prob < 0.4:
        deadhead_surcharge = base_cost * 0.40
        slab += " + [DEADHEAD SURCHARGE]"


    total = base_cost + deadhead_surcharge


    return {
        "base_cost": round(base_cost, 2),
        "tier_multiplier": multiplier,
        "deadhead_surcharge": round(deadhead_surcharge, 2),
        "total": round(total, 2),
        "slab_description": slab
    }
```

### G. DRF API Specification - `serializers.py`

```python
# File: oms/api/serializers.py
from rest_framework import serializers


class QuoteRequestSerializer(serializers.Serializer):
    origin_city = serializers.CharField(max_length=100)
    dest_city = serializers.CharField(max_length=100)
    vehicle_type = serializers.ChoiceField(choices=["LCV", "MCV", "HCV"])
    weight_kg = serializers.FloatField(min_value=1)
    distance_km = serializers.FloatField(min_value=1)


class QuoteResponseSerializer(serializers.Serializer):
    base_cost = serializers.FloatField()
    tier_multiplier = serializers.FloatField()
    deadhead_surcharge = serializers.FloatField()
    total = serializers.FloatField()
    slab_description = serializers.CharField()
```

### H. DRF API Specification - `views.py`

```python
# File: oms/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuoteRequestSerializer, QuoteResponseSerializer
from oms.agents.pricing_agent import calculate_dynamic_quote
from oms.utils.cost_calculator import compute_base_cost  # Precomputed cost logic


class QuoteAPIView(APIView):
    """
    POST /api/quotes
    Generates a dynamic quote based on urbanization density and deadhead risk.
    """
    def post(self, request):
        serializer = QuoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Step 1: Compute base cost (fuel + tolls + driver wage per km)
        base_cost = compute_base_cost(
            distance_km=data["distance_km"],
            vehicle_type=data["vehicle_type"],
            weight_kg=data["weight_kg"]
        )
        
        # Step 2: Apply dynamic pricing logic
        try:
            quote = calculate_dynamic_quote(
                origin_city=data["origin_city"],
                dest_city=data["dest_city"],
                base_cost=base_cost
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_serializer = QuoteResponseSerializer(quote)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
```

### I. DRF API Specification - `urls.py`

```python
# File: oms/api/urls.py
from django.urls import path
from .views import QuoteAPIView


urlpatterns = [
    path('quotes', QuoteAPIView.as_view(), name='quote'),
]
```

### J. Quote API Request Example

```http
POST /api/quotes
Content-Type: application/json


{
  "origin_city": "Chennai",
  "dest_city": "Remote-Village",
  "vehicle_type": "HCV",
  "weight_kg": 10000,
  "distance_km": 600
}
```

### K. Quote API Response Example

```json
{
  "base_cost": 24525.00,
  "tier_multiplier": 1.00,
  "deadhead_surcharge": 9810.00,
  "total": 34335.00,
  "slab_description": "Economy Slab (Tier-3 Isolated) + [DEADHEAD SURCHARGE]"
}
```

### L. Integration Notes from Source

1. **Precomputed Base Cost**:  
   `compute_base_cost()` should use your `vehicle model.txt` cost breakdown (fuel @ ₹95/l, driver salary, depreciation, etc.).


2. **City Data Seeding**:  
   Populate `city_tiers` via a one-time script using Indian city databases + elevation APIs for hill stations.


3. **Audit Trail**:  
   Log every quote in `decision_audit` with `reason_code="DYNAMIC_PRICING"`.


4. **Fallback**:  
   If PostGIS fails, fall back to Haversine distance (Python function above).


5. **Agent Role**:  
   Only the **OMS Agent** may call this function. Never expose raw pricing logic to frontend.
