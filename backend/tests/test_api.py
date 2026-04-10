"""
Basic tests for the FastAPI backend
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint returns 200"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_liveness_probe():
    """Test liveness endpoint"""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Zippy Logitech API"
    assert data["status"] == "running"


def test_list_manufacturers():
    """Test manufacturers endpoint"""
    response = client.get("/api/v1/manufacturers")
    assert response.status_code == 200
    data = response.json()
    assert "manufacturers" in data
    assert isinstance(data["manufacturers"], list)


def test_list_categories():
    """Test categories endpoint"""
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert isinstance(data["categories"], list)


def test_list_vehicles():
    """Test vehicles list endpoint"""
    response = client.get("/api/v1/vehicles")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "vehicles" in data
    assert isinstance(data["vehicles"], list)


def test_list_vehicles_with_category_filter():
    """Test vehicles filtering by category"""
    response = client.get("/api/v1/vehicles?category=LCV")
    assert response.status_code == 200
    data = response.json()
    for vehicle in data["vehicles"]:
        assert vehicle["category"] == "LCV"


def test_pricing_estimate():
    """Test pricing estimation endpoint"""
    payload = {"weight_kg": 5000, "distance_km": 300, "is_interstate": False}
    response = client.post("/api/v1/pricing/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "base_cost" in data
    assert "total_amount" in data
    assert "gst_amount" in data
    assert data["total_amount"] > data["base_cost"]


def test_get_pricing_rates():
    """Test pricing rates endpoint"""
    response = client.get("/api/v1/pricing/rates")
    assert response.status_code == 200
    data = response.json()
    assert "rates_per_km" in data
    assert "surcharges" in data
    assert "gst_rates" in data
