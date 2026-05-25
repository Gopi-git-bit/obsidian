"""GAAP/ASC 606 revenue recognition endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.revenue import RevenueRecognitionRequest, RevenueRecognitionResponse
from app.services.revenue_service import recognize_revenue

router = APIRouter()


@router.post("/revenue/recognize", response_model=RevenueRecognitionResponse)
async def post_revenue_recognition(payload: RevenueRecognitionRequest):
    """Recognize revenue only after ASC 606 and SoD controls pass."""
    return recognize_revenue(payload)
