# Graph Report - backend  (2026-04-28)

## Corpus Check
- 27 files · ~10,995 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 251 nodes · 498 edges · 17 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 200 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]

## God Nodes (most connected - your core abstractions)
1. `VehicleModel` - 21 edges
2. `Order` - 20 edges
3. `OrderStatus` - 18 edges
4. `VehicleListResponse` - 15 edges
5. `Bid` - 14 edges
6. `VehicleRecommendResponse` - 13 edges
7. `VehicleResponse` - 12 edges
8. `DynamicPricingEngine` - 12 edges
9. `Match API endpoints — vehicle-load matching engine` - 11 edges
10. `Find best vehicles for an order using weighted scoring algorithm` - 11 edges

## Surprising Connections (you probably didn't know these)
- `create_bid()` --calls--> `Bid`  [INFERRED]
  app\api\bids.py → app\models\order_model.py
- `Bid API endpoints — driver bidding system for orders` --uses--> `Order`  [INFERRED]
  app\api\bids.py → app\models\order_model.py
- `Bid API endpoints — driver bidding system for orders` --uses--> `OrderStatus`  [INFERRED]
  app\api\bids.py → app\models\order_model.py
- `Bid API endpoints — driver bidding system for orders` --uses--> `Bid`  [INFERRED]
  app\api\bids.py → app\models\order_model.py
- `Bid API endpoints — driver bidding system for orders` --uses--> `VehicleModel`  [INFERRED]
  app\api\bids.py → app\models\vehicle_model.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (26): get_vehicle(), get_vehicles_by_category(), get_vehicles_by_manufacturer(), list_categories(), list_manufacturers(), list_vehicles(), Vehicle API endpoints, Get vehicles by manufacturer (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (15): predict_surge(), Predict demand-supply surge multiplier.      Returns surge multiplier (1.0-3.0), generate_synthetic_data(), main(), LightGBM Surge Pricing Model Training Pipeline  Generates synthetic Indian logis, train_model(), Services package — business logic layer for Zippy Logitech  - pricing_service: L, _calc_savings() (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (15): calculate_distance(), Calculate distance and estimated travel time between two points.      Returns st, DRL4RouteAgent, estimate_road_distance_km(), estimate_travel_time_min(), get_gst_zone(), haversine_km(), ORToolsSolver (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (23): compare_pricing(), get_detailed_rate_card(), ml_price_estimate(), MLPricingRequest, MLPricingResponse, ML-Enhanced Pricing API endpoints  Extends the base pricing engine with LightGBM, Get current dynamic rate card with all multipliers and surcharges.      Includes, Compare Zippy pricing vs traditional broker pricing.      Shows side-by-side cos (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (22): accept_match(), calculate_match_score(), find_matches(), get_match_stats(), list_matches(), Match API endpoints — vehicle-load matching engine, Accept a proposed match, Reject a proposed match (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (20): create_order(), get_order(), get_order_stats(), list_orders(), Order API endpoints — freight transport order lifecycle management, Update an order's status or price, Get order summary statistics, Create a new freight transport order (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (17): Basic tests for the FastAPI backend, Test health endpoint returns 200, Test liveness endpoint, Test manufacturers endpoint, Test categories endpoint, Test vehicles list endpoint, Test vehicles filtering by category, Test pricing estimation endpoint (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.26
Nodes (13): counter_bid(), create_bid(), list_bids(), Bid API endpoints — driver bidding system for orders, Counter-offer on a bid, Place a bid on an order, List all bids for an order, BidStatus (+5 more)

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (6): create_order(), Tests for Order, Match, and Bid API endpoints, test_cancel_order(), test_create_order(), test_get_order(), test_update_order_status()

### Community 9 - "Community 9"
Cohesion: 0.25
Nodes (8): health_check(), HealthResponse, liveness(), Health check endpoints, Basic health check endpoint, Liveness probe for container orchestration, Readiness probe - checks database connectivity, readiness()

### Community 10 - "Community 10"
Cohesion: 0.33
Nodes (6): estimate_price(), get_current_rates(), PriceEstimateResponse, Pricing API endpoints, Get current base rates for pricing, Calculate price estimate for freight transport.      Formula:     - Base Cost =

### Community 11 - "Community 11"
Cohesion: 0.4
Nodes (4): init_database(), lifespan(), Zippy Logitech - FastAPI Backend Main application entry point, Create the local schema for development and tests.

### Community 12 - "Community 12"
Cohesion: 0.5
Nodes (1): Alembic environment configuration for Zippy Logitech

### Community 13 - "Community 13"
Cohesion: 0.5
Nodes (1): Initial schema - vehicle_models, orders, bids, matches  Revision ID: 001_initial

### Community 14 - "Community 14"
Cohesion: 0.5
Nodes (3): get_db(), Database configuration and session management, Dependency for getting database session

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (1): API package initialization

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): App package initialization

## Knowledge Gaps
- **45 isolated node(s):** `Alembic environment configuration for Zippy Logitech`, `Initial schema - vehicle_models, orders, bids, matches  Revision ID: 001_initial`, `Zippy Logitech - FastAPI Backend Main application entry point`, `Create the local schema for development and tests.`, `Health check endpoints` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (4 nodes): `env.py`, `Alembic environment configuration for Zippy Logitech`, `run_migrations_offline()`, `run_migrations_online()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (4 nodes): `001_initial_schema.py`, `downgrade()`, `Initial schema - vehicle_models, orders, bids, matches  Revision ID: 001_initial`, `upgrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `API package initialization`, `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (2 nodes): `__init__.py`, `App package initialization`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DynamicPricingEngine` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `VehicleModel` connect `Community 0` to `Community 4`, `Community 7`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `Services package — business logic layer for Zippy Logitech  - pricing_service: L` connect `Community 1` to `Community 2`, `Community 3`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `VehicleModel` (e.g. with `Bid API endpoints — driver bidding system for orders` and `Place a bid on an order`) actually correct?**
  _`VehicleModel` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Order` (e.g. with `Bid API endpoints — driver bidding system for orders` and `Place a bid on an order`) actually correct?**
  _`Order` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `OrderStatus` (e.g. with `Bid API endpoints — driver bidding system for orders` and `Place a bid on an order`) actually correct?**
  _`OrderStatus` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VehicleListResponse` (e.g. with `Vehicle API endpoints` and `List all vehicles with optional filters`) actually correct?**
  _`VehicleListResponse` has 12 INFERRED edges - model-reasoned connections that need verification._