"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    database: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Basic health check endpoint"""
    # Check database connection
    db_status = "connected"
    try:
        db.execute("SELECT 1")
    except Exception:
        db_status = "disconnected"

    return HealthResponse(status="healthy", database=db_status, version="1.0.0")


@router.get("/health/live")
async def liveness():
    """Liveness probe for container orchestration"""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(db: Session = Depends(get_db)):
    """Readiness probe - checks database connectivity"""
    try:
        db.execute("SELECT 1")
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return {"status": "not ready", "database": "disconnected", "error": str(e)}
