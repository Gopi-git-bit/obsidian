"""Migration parity checks for the canonical order lifecycle schema."""

from __future__ import annotations

import importlib.util
import sqlite3
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from conftest import auth_headers


client = TestClient(app)
client.headers.update(auth_headers(client, "super_admin"))
DB_PATH = Path(__file__).resolve().parents[1] / ".pytest_alembic.db"
MIGRATIONS_PATH = Path(__file__).resolve().parents[1] / "alembic" / "versions"


def _order_payload() -> dict:
    return {
        "shipper_name": "Migration Parity",
        "shipper_phone": "9876543210",
        "shipper_email": "parity@example.com",
        "origin_city": "Tiruppur",
        "origin_state": "Tamil Nadu",
        "destination_city": "Chennai",
        "destination_state": "Tamil Nadu",
        "cargo_type": "general",
        "weight_kg": 1200.0,
        "num_packages": 10,
        "vehicle_category_preference": "LCV",
        "is_interstate": False,
        "estimated_distance_km": 460.0,
        "offered_price": 18000.0,
    }


def _transition(order_id: str, to_state: str, event: str, *, actor_role: str = "OMS", payload=None):
    return client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_state": to_state,
            "event": event,
            "payload": payload or {},
            "actor_role": actor_role,
            "idempotency_key": str(uuid4()),
            "trace_id": f"migration-parity-{uuid4()}",
        },
    )


def test_alembic_schema_uses_current_state_without_required_status_column():
    with sqlite3.connect(DB_PATH) as conn:
        order_columns = {
            row[1]: {"type": row[2], "not_null": bool(row[3])}
            for row in conn.execute("pragma table_info(orders)").fetchall()
        }
        revision = conn.execute("select version_num from alembic_version").fetchone()

    assert revision is not None
    assert revision[0] == "010_policy_kernel"
    assert "current_state" in order_columns
    assert order_columns["current_state"]["not_null"] is True
    assert "status" not in order_columns


def test_userrole_postgres_enum_reuses_existing_type_without_recreate():
    migration_path = MIGRATIONS_PATH / "004_auth_rbac_foundation.py"
    spec = importlib.util.spec_from_file_location("migration_004_auth_rbac_foundation", migration_path)
    assert spec and spec.loader
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)

    enum_type = migration._user_role_enum(SimpleNamespace(dialect=SimpleNamespace(name="postgresql")))

    assert enum_type.name == "userrole"
    assert enum_type.create_type is False


def test_revision_ids_fit_widened_alembic_version_column():
    revision_ids = []
    for migration_path in MIGRATIONS_PATH.glob("*.py"):
        spec = importlib.util.spec_from_file_location(f"migration_{migration_path.stem}", migration_path)
        assert spec and spec.loader
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        revision_ids.append(migration.revision)

    assert any(len(revision) > 32 for revision in revision_ids)
    assert all(len(revision) <= 80 for revision in revision_ids)


def test_order_creation_and_state_transitions_on_alembic_database():
    created = client.post("/api/v1/orders", json=_order_payload())
    assert created.status_code == 201, created.text
    order = created.json()
    assert order["current_state"] == "CREATED"
    assert order["status"] == "CREATED"

    confirmed = _transition(
        order["id"],
        "CONFIRMED",
        "order_submitted",
        payload={
            "payment_mode": "advance",
            "topay_consent_status": "not_required",
            "material_type": "general_goods",
            "body_type_required": "open",
        },
    )
    assert confirmed.status_code == 200, confirmed.text
    assert confirmed.json()["current_state"] == "CONFIRMED"

    vehicle_id = str(uuid4())
    reserved = _transition(
        order["id"],
        "RINGING",
        "vehicle_reserved",
        actor_role="TMS",
        payload={
            "vehicle_id": vehicle_id,
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
        },
    )
    assert reserved.status_code == 200, reserved.text
    assert reserved.json()["current_state"] == "RINGING"

    assigned = _transition(
        order["id"],
        "ASSIGNED",
        "driver_response",
        actor_role="DRIVER",
        payload={"driver_id": "driver-migration", "vehicle_id": vehicle_id, "action": "ACCEPT"},
    )
    assert assigned.status_code == 200, assigned.text
    assert assigned.json()["current_state"] == "ASSIGNED"
