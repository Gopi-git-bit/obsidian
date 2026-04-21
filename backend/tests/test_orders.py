"""
Tests for Order, Match, and Bid API endpoints
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_ORDER = {
    "shipper_name": "Rajesh Kumar",
    "shipper_phone": "9876543210",
    "shipper_email": "rajesh@example.com",
    "origin_city": "Mumbai",
    "origin_state": "Maharashtra",
    "destination_city": "Delhi",
    "destination_state": "Delhi",
    "cargo_type": "general",
    "weight_kg": 5000.0,
    "volume_cbm": 25.0,
    "num_packages": 10,
    "vehicle_category_preference": "HCV",
    "is_interstate": True,
    "estimated_distance_km": 1400.0,
    "offered_price": 25000.0,
}


def create_order():
    response = client.post("/api/v1/orders", json=SAMPLE_ORDER)
    assert response.status_code == 201
    data = response.json()
    assert data["shipper_name"] == "Rajesh Kumar"
    assert data["status"] == "created"
    assert data["origin_city"] == "Mumbai"
    assert data["destination_city"] == "Delhi"
    assert data["weight_kg"] == 5000.0
    return data["id"]


def test_create_order():
    create_order()


def test_list_orders():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "orders" in data
    assert isinstance(data["orders"], list)


def test_list_orders_with_filters():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders?status=created&origin_city=Mumbai")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_get_order():
    order_id = create_order()
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


def test_get_order_not_found():
    response = client.get("/api/v1/orders/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_order_status():
    order_id = create_order()
    response = client.patch(
        f"/api/v1/orders/{order_id}", json={"status": "pending_match"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending_match"


def test_cancel_order():
    order_id = create_order()
    response = client.post(f"/api/v1/orders/{order_id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"


def test_order_stats():
    client.post("/api/v1/orders", json=SAMPLE_ORDER)
    response = client.get("/api/v1/orders/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_orders" in data
    assert "by_status" in data


def test_create_order_invalid_cargo():
    invalid_order = SAMPLE_ORDER.copy()
    invalid_order["cargo_type"] = "invalid_type"
    response = client.post("/api/v1/orders", json=invalid_order)
    assert response.status_code == 400


def test_list_matches():
    response = client.get("/api/v1/matches")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "matches" in data


def test_match_stats():
    response = client.get("/api/v1/matches/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_matches" in data
    assert "by_status" in data
