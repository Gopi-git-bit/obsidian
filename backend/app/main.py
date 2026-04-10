"""
Zippy Logitech - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import (
    vehicles,
    health,
    pricing,
    orders,
    matches,
    bids,
    ml_pricing,
    routing,
)
from app.database import engine
from app.models import vehicle_model, order_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    vehicle_model.Base.metadata.create_all(bind=engine)
    order_model.Base.metadata.create_all(bind=engine)
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(vehicles.router, prefix="/api/v1", tags=["Vehicles"])
app.include_router(pricing.router, prefix="/api/v1", tags=["Pricing"])
app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(matches.router, prefix="/api/v1", tags=["Matching"])
app.include_router(bids.router, prefix="/api/v1", tags=["Bidding"])
app.include_router(ml_pricing.router, prefix="/api/v1", tags=["ML Pricing"])
app.include_router(routing.router, prefix="/api/v1", tags=["Route Optimization"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"name": "Zippy Logitech API", "version": "1.0.0", "status": "running"}
