"""
Vehicle API endpoints
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import SUPPORT_READ_ROLES, TRANSPORT_COMPANY_ROLES, require_roles
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole
from app.models.vehicle_model import VehicleModel
from app.schemas.vehicle import (
    VehicleResponse,
    VehicleListResponse,
    VehicleRecommendResponse,
    VehicleCreate,
    VehicleUpdate,
)

router = APIRouter(dependencies=[Depends(require_roles(SUPPORT_READ_ROLES | TRANSPORT_COMPANY_ROLES))])


def _is_transport_company(user: UserAccount) -> bool:
    return user.role == UserRole.TRANSPORT_COMPANY


def _assert_company_owns_vehicle(vehicle: VehicleModel, user: UserAccount) -> None:
    if _is_transport_company(user) and vehicle.transport_company_id != str(user.id):
        raise HTTPException(status_code=404, detail="Vehicle not found")


@router.post("/vehicles", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(TRANSPORT_COMPANY_ROLES)),
):
    vehicle = VehicleModel(**payload.model_dump(), transport_company_id=str(current_user.id))
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return VehicleResponse.model_validate(vehicle)


@router.get("/vehicles", response_model=VehicleListResponse)
async def list_vehicles(
    category: Optional[str] = Query(
        None, description="Filter by category (LCV, ICV, HCV, Tipper)"
    ),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer"),
    min_payload: Optional[float] = Query(
        None, ge=0, description="Minimum payload in kg"
    ),
    max_payload: Optional[float] = Query(
        None, ge=0, description="Maximum payload in kg"
    ),
    limit: int = Query(100, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(SUPPORT_READ_ROLES | TRANSPORT_COMPANY_ROLES)),
):
    """List all vehicles with optional filters"""
    query = db.query(VehicleModel).filter(VehicleModel.is_active == True)
    if _is_transport_company(current_user):
        query = query.filter(VehicleModel.transport_company_id == str(current_user.id))

    if category:
        query = query.filter(VehicleModel.category == category)
    if manufacturer:
        query = query.filter(VehicleModel.manufacturer == manufacturer)
    if min_payload:
        query = query.filter(VehicleModel.payload_kg >= min_payload)
    if max_payload:
        query = query.filter(VehicleModel.payload_kg <= max_payload)

    # Get total count
    total = query.count()

    # Get paginated results
    vehicles = query.order_by(VehicleModel.payload_kg).offset(offset).limit(limit).all()

    return VehicleListResponse(
        total=total,
        limit=limit,
        offset=offset,
        vehicles=[VehicleResponse.model_validate(v) for v in vehicles],
    )


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(SUPPORT_READ_ROLES | TRANSPORT_COMPANY_ROLES)),
):
    """Get a specific vehicle by ID"""
    vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    _assert_company_owns_vehicle(vehicle, current_user)

    return VehicleResponse.model_validate(vehicle)


@router.patch("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: UUID,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: UserAccount = Depends(require_roles(TRANSPORT_COMPANY_ROLES)),
):
    vehicle = db.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    _assert_company_owns_vehicle(vehicle, current_user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return VehicleResponse.model_validate(vehicle)


@router.get("/vehicles/category/{category}", response_model=VehicleListResponse)
async def get_vehicles_by_category(
    category: str,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Get vehicles by category"""
    valid_categories = ["LCV", "ICV", "HCV", "Tipper", "Tractor"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {valid_categories}",
        )

    query = db.query(VehicleModel).filter(
        VehicleModel.category == category, VehicleModel.is_active == True
    )

    total = query.count()
    vehicles = query.order_by(VehicleModel.payload_kg).offset(offset).limit(limit).all()

    return VehicleListResponse(
        total=total,
        limit=limit,
        offset=offset,
        vehicles=[VehicleResponse.model_validate(v) for v in vehicles],
    )


@router.get("/vehicles/manufacturer/{manufacturer}", response_model=VehicleListResponse)
async def get_vehicles_by_manufacturer(
    manufacturer: str,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Get vehicles by manufacturer"""
    query = db.query(VehicleModel).filter(
        VehicleModel.manufacturer.ilike(f"%{manufacturer}%"),
        VehicleModel.is_active == True,
    )

    total = query.count()
    vehicles = (
        query.order_by(VehicleModel.category, VehicleModel.payload_kg)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return VehicleListResponse(
        total=total,
        limit=limit,
        offset=offset,
        vehicles=[VehicleResponse.model_validate(v) for v in vehicles],
    )


@router.get("/vehicles/recommend", response_model=List[VehicleRecommendResponse])
async def recommend_vehicles(
    weight_kg: float = Query(..., gt=0, description="Cargo weight in kg"),
    volume_cbm: Optional[float] = Query(
        None, gt=0, description="Cargo volume in cubic meters"
    ),
    distance_km: Optional[float] = Query(
        None, gt=0, description="Transport distance in km"
    ),
    category_preference: Optional[str] = Query(None, description="Preferred category"),
    limit: int = Query(5, le=10, description="Number of recommendations"),
    db: Session = Depends(get_db),
):
    """
    Recommend suitable vehicles based on cargo requirements.
    Returns vehicles with payload capacity >= required weight (with 20% buffer).
    """
    # Calculate minimum required payload with buffer
    required_payload = weight_kg * 1.2

    # Query for suitable vehicles
    query = db.query(VehicleModel).filter(
        VehicleModel.is_active == True, VehicleModel.payload_kg >= required_payload
    )

    if category_preference:
        query = query.filter(VehicleModel.category == category_preference)

    candidates = query.order_by(VehicleModel.payload_kg).limit(limit * 2).all()

    recommendations = []
    for vehicle in candidates[:limit]:
        # Calculate utilization (higher is better, target ~85%)
        utilization = weight_kg / vehicle.payload_kg
        utilization_score = min(utilization / 0.85, 1.0)

        # Calculate efficiency score
        mileage_score = (vehicle.mileage_kmpl or 5) / 10.0  # Normalize to 10 kmpl
        price_score = 1 - ((vehicle.price_ex_showroom or 0) / 6000000)

        total_score = (
            (utilization_score * 0.5) + (mileage_score * 0.3) + (price_score * 0.2)
        )

        recommendations.append(
            VehicleRecommendResponse(
                vehicle=VehicleResponse.model_validate(vehicle),
                utilization_percent=round(utilization * 100, 1),
                efficiency_score=round(total_score * 100, 1),
                recommended=True,
            )
        )

    return recommendations


@router.get("/manufacturers")
async def list_manufacturers(db: Session = Depends(get_db)):
    """Get list of all manufacturers"""
    manufacturers = (
        db.query(VehicleModel.manufacturer)
        .distinct()
        .order_by(VehicleModel.manufacturer)
        .all()
    )
    return {"manufacturers": [m[0] for m in manufacturers]}


@router.get("/categories")
async def list_categories(db: Session = Depends(get_db)):
    """Get list of all vehicle categories"""
    categories = (
        db.query(VehicleModel.category).distinct().order_by(VehicleModel.category).all()
    )
    return {"categories": [c[0] for c in categories]}
