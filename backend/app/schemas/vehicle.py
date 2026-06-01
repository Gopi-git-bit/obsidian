"""
Pydantic schemas for vehicle API responses
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class VehicleResponse(BaseModel):
    """Vehicle model response schema"""

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: UUID
    transport_company_id: Optional[str]
    manufacturer: str
    model_name: str
    variant: Optional[str]
    category: str
    body_type: str
    gvw_kg: Optional[float]
    payload_kg: Optional[float]
    tonnage_class: Optional[str]
    length_mm: Optional[float]
    width_mm: Optional[float]
    height_mm: Optional[float]
    wheelbase_mm: Optional[float]
    loading_length_mm: Optional[float]
    loading_width_mm: Optional[float]
    loading_height_mm: Optional[float]
    engine_cc: Optional[float]
    engine_cylinders: Optional[int]
    power_hp: Optional[float]
    torque_nm: Optional[float]
    fuel_tank_ltr: Optional[float]
    mileage_kmpl: Optional[float]
    emission_norm: Optional[str]
    axle_config: Optional[str]
    tyres: Optional[int]
    price_ex_showroom: Optional[float]


class VehicleCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    manufacturer: str = Field(..., min_length=1, max_length=50)
    model_name: str = Field(..., min_length=1, max_length=100)
    category: str
    body_type: str = "open"
    gvw_kg: Optional[float] = None
    payload_kg: Optional[float] = None
    mileage_kmpl: Optional[float] = None
    price_ex_showroom: Optional[float] = None
    is_active: bool = True


class VehicleUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    manufacturer: Optional[str] = None
    model_name: Optional[str] = None
    category: Optional[str] = None
    body_type: Optional[str] = None
    gvw_kg: Optional[float] = None
    payload_kg: Optional[float] = None
    mileage_kmpl: Optional[float] = None
    price_ex_showroom: Optional[float] = None
    is_active: Optional[bool] = None

class VehicleListResponse(BaseModel):
    """Paginated list of vehicles"""

    total: int
    limit: int
    offset: int
    vehicles: list[VehicleResponse]


class VehicleRecommendResponse(BaseModel):
    """Vehicle recommendation with scoring"""

    vehicle: VehicleResponse
    utilization_percent: float = Field(
        ..., description="Cargo weight as % of vehicle capacity"
    )
    efficiency_score: float = Field(..., description="Overall efficiency score (0-100)")
    recommended: bool = Field(
        default=True, description="Whether vehicle is recommended"
    )
