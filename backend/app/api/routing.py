"""
Route Optimization API — OR-Tools VRPTW + DRL4Route dynamic adaptation

Based on BI_Tech_Stack_ML_Systems.md:
- Phase 1: OR-Tools deterministic routing (VRPTW)
- Phase 2: DRL4Route confidence gating
- Phase 3-5: Progressive rollout (Shadow → Canary → Production)
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.route_optimizer import route_service

router = APIRouter()


class RouteNodeInput(BaseModel):
    id: str = Field(..., description="Unique node identifier")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
    demand_kg: float = Field(default=0, ge=0, description="Demand at this node in kg")
    time_window_start: int = Field(
        default=0, ge=0, description="Window start (minutes from midnight)"
    )
    time_window_end: int = Field(
        default=1440, ge=0, description="Window end (minutes from midnight)"
    )
    service_time_min: int = Field(
        default=15, ge=0, description="Service/dwell time in minutes"
    )
    is_depot: bool = Field(
        default=False, description="Whether this is the depot/start node"
    )


class RouteVehicleInput(BaseModel):
    id: str = Field(..., description="Vehicle identifier")
    capacity_kg: float = Field(
        default=10000, ge=0, description="Vehicle capacity in kg"
    )
    cost_per_km: float = Field(default=18.0, ge=0, description="Cost per km in INR")
    max_distance_km: float = Field(
        default=500, ge=0, description="Max route distance in km"
    )
    max_stops: int = Field(default=8, ge=1, description="Max stops per route")


class OptimizeRouteRequest(BaseModel):
    nodes: list[RouteNodeInput] = Field(
        ..., min_length=2, description="Route nodes (first is depot)"
    )
    vehicles: list[RouteVehicleInput] = Field(
        ..., min_length=1, description="Available vehicles"
    )
    optimize_for: str = Field(
        default="cost", description="Optimize for: cost, distance, time"
    )
    time_limit_seconds: int = Field(
        default=10, ge=1, le=60, description="Solver time limit"
    )
    use_drl: bool = Field(default=False, description="Use DRL4Route confidence gating")


class OptimizeRouteResponse(BaseModel):
    order_id: str
    routes: list
    total_distance_km: float
    total_duration_min: float
    total_cost: float
    model_used: str
    confidence: float
    fallback_reason: Optional[str] = None
    solve_time_ms: int


@router.post("/optimize/route", response_model=OptimizeRouteResponse)
async def optimize_route(
    request: OptimizeRouteRequest,
    db: Session = Depends(get_db),
):
    """
    Optimize vehicle routing using OR-Tools VRPTW solver.

    Supports:
    - Multiple vehicles with different capacities and costs
    - Time windows for deliveries
    - Capacity constraints
    - DRL4Route confidence gating (optional)
    - Indian logistics specifics (GST zones, road types)
    """
    nodes = [n.model_dump() for n in request.nodes]
    vehicles = [v.model_dump() for v in request.vehicles]

    if not any(n.get("is_depot") for n in nodes):
        nodes[0]["is_depot"] = True

    result = route_service.solve(
        nodes=nodes,
        vehicles=vehicles,
        optimize_for=request.optimize_for,
        time_limit_seconds=request.time_limit_seconds,
        use_drl=request.use_drl,
    )

    return result


@router.get("/optimize/distance")
async def calculate_distance(
    lat1: float = Query(..., description="Origin latitude"),
    lng1: float = Query(..., description="Origin longitude"),
    lat2: float = Query(..., description="Destination latitude"),
    lng2: float = Query(..., description="Destination longitude"),
    road_type: str = Query(
        default="default",
        description="highway, national_highway, state_highway, urban, rural, hill",
    ),
):
    """
    Calculate distance and estimated travel time between two points.

    Returns straight-line distance, estimated road distance (1.2-1.35x),
    and estimated travel time based on Indian road speed averages.
    """
    from app.services.route_optimizer import (
        haversine_km,
        estimate_road_distance_km,
        estimate_travel_time_min,
        INDIAN_AVERAGE_SPEED_KMH,
    )

    straight_line = haversine_km(lat1, lng1, lat2, lng2)
    road_factor = 1.2 if straight_line < 100 else 1.35
    road_distance = estimate_road_distance_km(straight_line, road_factor)
    travel_time = estimate_travel_time_min(road_distance, road_type)
    speed_kmh = INDIAN_AVERAGE_SPEED_KMH.get(
        road_type, INDIAN_AVERAGE_SPEED_KMH["default"]
    )

    return {
        "origin": {"lat": lat1, "lng": lng1},
        "destination": {"lat": lat2, "lng": lng2},
        "straight_line_km": round(straight_line, 2),
        "road_distance_km": round(road_distance, 2),
        "road_factor": road_factor,
        "estimated_time_min": round(travel_time, 1),
        "estimated_time_hours": round(travel_time / 60, 2),
        "road_type": road_type,
        "average_speed_kmh": speed_kmh,
    }


@router.get("/optimize/gst-zone")
async def get_gst_zone(city: str = Query(..., description="City name")):
    """
    Get GST zone classification for an Indian city.

    Used for interstate vs intrastate GST calculation:
    - Intrastate: CGST + SGST (each 50% of total GST)
    - Interstate: IGST (full rate)
    """
    return route_service.get_gst_zone_info(city)


@router.post("/optimize/multi-stop")
async def optimize_multi_stop(
    origin: RouteNodeInput,
    destinations: list[RouteNodeInput],
    vehicle: RouteVehicleInput,
    time_limit_seconds: int = Query(default=10, ge=1, le=60),
):
    """
    Optimize a single-vehicle multi-stop route.

    Finds the optimal order of stops to minimize total distance/time.
    First node is treated as depot (start/end).
    """
    all_nodes = [origin.model_dump()] + [d.model_dump() for d in destinations]
    all_nodes[0]["is_depot"] = True

    result = route_service.solve(
        nodes=all_nodes,
        vehicles=[vehicle.model_dump()],
        time_limit_seconds=time_limit_seconds,
        use_drl=False,
    )

    return result
