# Zippy Logitech - Knowledge Base

## India Logistics Context

### Market Statistics
- **Logistics Cost:** 8-9% of GDP (target: 5-6%)
- **Road Modal Share:** 68%
- **Rail Modal Share:** 30-32%
- **Empty Running:** 28-43% (target: 20%)

### Cost Benchmarks
- **FTL Rate:** ₹15-25/km
- **Diesel Cost:** 55-70% of operating cost
- **Last-Mile:** 53% of total shipping cost
- **Platform Fee:** 3-5% (vs 8-12% brokers)

### Key Regulations
- **GST:** 12% on transport, 18% on services
- **E-Way Bill:** Required for inter-state >₹50,000
- **BS-VI Emission:** Mandatory for all vehicles

## Technical Standards

### API Design
- RESTful endpoints with OpenAPI 3.0
- JWT authentication
- Rate limiting: 100 req/min
- Response timeout: 30s

### Database
- PostgreSQL 15+
- Connection pool: 20 max
- Index on: vehicle_models, bookings, users

### Code Standards
- Python: PEP 8, Black formatter
- TypeScript: Strict mode enabled
- React: Functional components, hooks only
- Testing: 80% coverage minimum

## Architecture Decisions

### Why FastAPI?
- Native async support
- OpenAPI auto-generation
- Pydantic validation
- Fast performance

### Why React Native?
- Cross-platform (iOS + Android)
- Expo for rapid development
- Large component library
- Good for logistics apps

### Why LightGBM?
- Fast training
- Handles categorical features
- Good for pricing prediction
- Lower memory than XGBoost

## Known Challenges

1. **Diesel Price Volatility:** Update weekly
2. **Festival Surges:** Oct-Nov (Diwali), Dec-Jan (Christmas)
3. **Monsoon Disruptions:** Jun-Sep
4. **Driver Availability:** Peak during harvest season
5. **E-Way Bill API:** Rate limit 100/day on NIC

## Database Schema

```sql
-- Core tables
bi_insights (245 records)
bi_metrics (93 records)
vehicle_models (26 records)
raw_web_data (31 records)
raw_pdf_data (10 records)
insights (3,633 records)
```

## Key Endpoints

```
POST /api/v1/bookings          - Create booking
GET  /api/v1/bookings/:id      - Get booking details
POST /api/v1/pricing/estimate   - Get price estimate
GET  /api/v1/vehicles          - List vehicle models
POST /api/v1/tracking/:id       - Update tracking
```