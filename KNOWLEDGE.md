# Zippy Logitech - Knowledge Base

## India Logistics Context

### Market Statistics
- **Logistics Cost:** 7.97% of GDP in 2023-24 per DPIIT/NCAER assessment; older 13-14% figures should be treated as legacy/external estimates
- **Freight Modal Share (2025 est.):** Road 66%, rail 22%, waterways 8%, pipelines ~3.6-4%, air ~0.06%
- **Passenger Modal Share (2025 est.):** Road 78%, rail 17%, air 4%, metro ~1%
- **Policy Direction:** PM GatiShakti, National Logistics Policy, DFCs, MMLPs, Gati Shakti Cargo Terminals, rail/water modal shift, and clean-fuel corridors
- **Port Infrastructure:** Use official figures for exact cargo volumes; PIB reported major ports grew from ~819 MT in FY 2023-24 to ~855 MT in FY 2024-25
- **Infrastructure Intelligence File:** `india-logistics-infrastructure-ports-intermodal.md`
- **Truck Operations File:** `india-truck-operations-playbook.md`
- **Agriculture Harvest Logistics File:** `agriculture-seasonality-harvest-logistics.md`
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
