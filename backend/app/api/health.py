"""
Health check endpoints
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.observability import APP_VERSION

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
    timestamp: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    version: str
    timestamp: str
    checked_tables: list[str]
    missing_tables: list[str] = []


REQUIRED_READY_TABLES = ("alembic_version", "orders", "policy_decisions", "event_outbox")


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Basic health check endpoint"""
    # Check database connection
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return HealthResponse(status="healthy", database=db_status, version=APP_VERSION, timestamp=_utc_timestamp())


@router.get("/health/live")
async def liveness():
    """Liveness probe for container orchestration"""
    return {"status": "alive"}


@router.get("/health/ready")
@router.get("/ready", response_model=ReadinessResponse)
async def readiness(response: Response, db: Session = Depends(get_db)):
    """Readiness probe - checks database connectivity and migration-backed tables."""
    try:
        db.execute(text("SELECT 1"))
        table_names = set(inspect(db.bind).get_table_names())
        missing = [table for table in REQUIRED_READY_TABLES if table not in table_names]
        if missing:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return ReadinessResponse(
                status="not ready",
                database="connected",
                version=APP_VERSION,
                timestamp=_utc_timestamp(),
                checked_tables=list(REQUIRED_READY_TABLES),
                missing_tables=missing,
            )
        return ReadinessResponse(
            status="ready",
            database="connected",
            version=APP_VERSION,
            timestamp=_utc_timestamp(),
            checked_tables=list(REQUIRED_READY_TABLES),
            missing_tables=[],
        )
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not ready",
            "database": "disconnected",
            "version": APP_VERSION,
            "timestamp": _utc_timestamp(),
            "checked_tables": list(REQUIRED_READY_TABLES),
            "missing_tables": [],
            "error": str(e),
        }
