"""
Zippy Logitech - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import (
    auth,
    vehicles,
    health,
    pricing,
    orders,
    matches,
    bids,
    ml_pricing,
    policy,
    routing,
    shipments,
    revenue,
    flow,
    finance,
    outbox,
    supervisor,
)
from app.middleware.privacy import DPDPPrivacyMaskingMiddleware
from app.config import cors_allowed_origins
from app.observability import (
    RequestIdLoggingMiddleware,
    configure_logging,
    init_sentry_if_configured,
    unhandled_exception_handler,
)

configure_logging()
init_sentry_if_configured()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Initialize FastAPI app
app = FastAPI(
    title="Zippy Logitech API",
    description="Logistics Business Intelligence Platform API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DPDPPrivacyMaskingMiddleware)
app.add_middleware(RequestIdLoggingMiddleware)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(health.router, tags=["Health"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(vehicles.router, prefix="/api/v1", tags=["Vehicles"])
app.include_router(pricing.router, prefix="/api/v1", tags=["Pricing"])
app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(orders.transition_alias_router, prefix="/api", tags=["Orders"])
app.include_router(matches.router, prefix="/api/v1", tags=["Matching"])
app.include_router(bids.router, prefix="/api/v1", tags=["Bidding"])
app.include_router(ml_pricing.router, prefix="/api/v1", tags=["ML Pricing"])
app.include_router(policy.router, prefix="/api/v1", tags=["Policy"])
app.include_router(routing.router, prefix="/api/v1", tags=["Route Optimization"])
app.include_router(shipments.router, prefix="/api/v1", tags=["Shipments"])
app.include_router(revenue.router, prefix="/api/v1", tags=["Revenue Controls"])
app.include_router(flow.router, prefix="/api/v1", tags=["Order Flow"])
app.include_router(finance.router, prefix="/api/v1", tags=["Finance"])
app.include_router(outbox.router, prefix="/api/v1", tags=["Outbox"])
app.include_router(supervisor.router, prefix="/api/v1", tags=["Supervisor"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"name": "Zippy Logitech API", "version": "1.0.0", "status": "running"}
