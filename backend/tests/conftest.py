"""Test database bootstrap.

Tests must exercise the same schema path used by production: Alembic
migrations. SQLAlchemy ``create_all`` is intentionally not used here.
"""

from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
TEST_DB = BACKEND_DIR / ".pytest_alembic.db"

if TEST_DB.exists():
    TEST_DB.unlink()

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"

alembic_cfg = Config(str(BACKEND_DIR / "alembic.ini"))
alembic_cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
alembic_cfg.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
command.upgrade(alembic_cfg, "head")


def auth_headers(
    client: TestClient,
    role: str = "super_admin",
    username: str | None = None,
) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/dev-login",
        json={
            "username": username or f"test-{role}",
            "password": "dev-password",
            "role": role,
        },
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
