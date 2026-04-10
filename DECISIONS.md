# Architectural Decisions

## 2024 - Project Inception

### AD-001: Technology Stack Selection

**Decision:** Use FastAPI + PostgreSQL + Redis + Kafka for backend

**Rationale:**
- FastAPI: Best Python async framework, native OpenAPI support
- PostgreSQL: Strong ACID compliance, excellent JSON support
- Redis: Sub-millisecond caching, pub/sub for real-time
- Kafka: Event sourcing, order management, high throughput

**Status:** Approved

---

### AD-002: Frontend Framework

**Decision:** Use React 18 + TypeScript + Tailwind CSS

**Rationale:**
- React 18: Concurrent features, automatic batching
- TypeScript: Type safety, better IDE support
- Tailwind: Rapid development, consistent styling
- Component library: Headless UI for accessibility

**Status:** Approved

---

### AD-003: Mobile Strategy

**Decision:** Use React Native (Expo) for both Driver and Customer apps

**Rationale:**
- Single codebase for iOS + Android
- Expo: Faster build times, easy updates
- Large ecosystem for logistics features
- Push notifications via FCM

**Status:** Approved

---

### AD-004: AI/ML Approach

**Decision:** Hybrid approach - LightGBM for pricing, OR-Tools for routing

**Rationale:**
- LightGBM: Fast, handles mixed data types, good for demand prediction
- OR-Tools: Industry-standard constraint programming
- DRL4Route: Research phase for long-term optimization

**Status:** Approved - Implementation in progress

---

### AD-005: Payment Gateway

**Decision:** Razorpay as primary, Cashfree as backup

**Rationale:**
- Razorpay: Best India coverage, UPI support, easy integration
- Cashfree: Good alternative for specific use cases
- Both support GST-compliant invoicing

**Status:** Approved

---

### AD-006: Vehicle Database Approach

**Decision:** Pre-populate database with 26 popular Indian commercial vehicles

**Rationale:**
- Instant vehicle recommendations
- Accurate payload/capacity matching
- Price benchmarking for pricing engine

**Status:** Implemented - 26 vehicles loaded

---

### AD-007: Pricing Strategy

**Decision:** Base cost + scenario surcharges + platform fee + GST

**Components:**
- Base cost: Distance × rate per km
- Scenario surcharge: Festival, remote, hill, congestion
- Platform fee: 3-5% of base
- GST: 12% transport + 18% services

**Status:** Approved - Documented in knowledge base