"""
Basic tests for the FastAPI backend
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.observability import REQUEST_ID_HEADER, init_sentry_if_configured
from conftest import auth_headers

client = TestClient(app)
client.headers.update(auth_headers(client, "super_admin"))


@app.get("/__test/unhandled-error", include_in_schema=False)
async def _test_unhandled_error():
    raise RuntimeError("boom")


def test_health_check():
    """Test health endpoint returns 200"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data
    assert "timestamp" in data


def test_root_health_endpoint():
    """Root health endpoint supports deployment probes."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["version"]
    assert data["timestamp"]


def test_liveness_probe():
    """Test liveness endpoint"""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_readiness_probe():
    """Test readiness endpoint checks database connectivity"""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"


def test_root_readiness_endpoint_checks_tables():
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"
    assert "orders" in data["checked_tables"]
    assert "policy_decisions" in data["checked_tables"]
    assert data["missing_tables"] == []


def test_request_id_header_is_returned():
    request_id = "test-request-id-123"
    response = client.get("/health", headers={REQUEST_ID_HEADER: request_id})
    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == request_id


def test_request_id_header_is_generated_when_missing():
    response = client.get("/health", headers={REQUEST_ID_HEADER: ""})
    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER]


def test_unhandled_error_response_includes_request_id():
    error_client = TestClient(app, raise_server_exceptions=False)
    response = error_client.get("/__test/unhandled-error", headers={REQUEST_ID_HEADER: "error-request-id"})
    assert response.status_code == 500
    assert response.headers[REQUEST_ID_HEADER] == "error-request-id"
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["request_id"] == "error-request-id"


def test_missing_sentry_dsn_does_not_crash(monkeypatch):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    init_sentry_if_configured()


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
