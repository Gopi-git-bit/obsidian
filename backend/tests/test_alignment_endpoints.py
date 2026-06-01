"""Tests for Phase 2 logistics and accounting alignment endpoints."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from conftest import auth_headers

client = TestClient(app)
client.headers.update(auth_headers(client, "super_admin"))


def _intake_payload():
    return {
        "shipper_name": "Meena Logistics",
        "shipper_phone": "9876543210",
        "shipper_email": "meena@example.com",
        "origin_city": "Tiruppur",
        "origin_state": "Tamil Nadu",
        "destination_city": "Chennai",
        "destination_state": "Tamil Nadu",
        "cargo_type": "general",
        "weight_kg": 1200,
        "num_packages": 12,
        "vehicle_category_preference": "LCV",
        "is_interstate": False,
        "estimated_distance_km": 460,
        "offered_price": 18000,
        "consent_id": f"consent-{uuid4()}",
        "privacy_notice_version": "DPDP-2026-05",
        "idempotency_key": f"intake-{uuid4()}",
    }


def test_order_intake_masks_phone_by_default():
    response = client.post("/api/v1/orders/intake", json=_intake_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["shipper_phone"] == "******3210"
    assert data["status"] == "CREATED"


def test_shipment_status_masks_customer_phone():
    intake = client.post("/api/v1/orders/intake", json=_intake_payload())
    order_id = intake.json()["order_id"]

    response = client.get(f"/api/v1/shipments/status?order_id={order_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["shipments"][0]["customer_phone"] == "******3210"


def _revenue_payload():
    return {
        "order_id": str(uuid4()),
        "user_id": "finance-manager-1",
        "invoice_generation_user_id": "finance-executive-1",
        "invoice_approval_user_id": "finance-manager-1",
        "principal_agent_status": "AGENT",
        "revenue_presentation": "NET_COMMISSION",
        "gross_freight_amount": 50000,
        "driver_payable_amount": 45000,
        "commission_amount": 5000,
        "platform_fee_amount": 0,
        "gst_amount": 900,
        "accounting_policy_version": "ASC606-BROKER-2026-05",
        "idempotency_key": f"rev-{uuid4()}",
        "performance_obligation": {
            "vehicle_assigned": True,
            "trip_completed": True,
            "pod_uploaded": True,
            "pod_verified": True,
            "otp_verified": True,
            "cancellation_hold": False,
            "fraud_hold": False,
            "dispute_hold": False,
            "claim_hold": False,
        },
    }


def test_revenue_recognition_allows_completed_broker_obligation():
    response = client.post("/api/v1/revenue/recognize", json=_revenue_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["recognition_status"] == "recognized"
    assert data["revenue_amount"] == 5000


def test_revenue_recognition_blocks_incomplete_performance_obligation():
    payload = _revenue_payload()
    payload["performance_obligation"]["otp_verified"] = False

    response = client.post("/api/v1/revenue/recognize", json=payload)

    assert response.status_code == 409


def test_revenue_recognition_blocks_invoice_sod_violation():
    payload = _revenue_payload()
    payload["invoice_approval_user_id"] = payload["invoice_generation_user_id"]

    response = client.post("/api/v1/revenue/recognize", json=payload)

    assert response.status_code == 409
