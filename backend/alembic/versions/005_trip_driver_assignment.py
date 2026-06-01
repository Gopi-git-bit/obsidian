"""Add driver assignment to trips.

Revision ID: 005_trip_driver_assignment
Revises: 004_auth_rbac_foundation
Create Date: 2026-06-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "005_trip_driver_assignment"
down_revision = "004_auth_rbac_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("trips", sa.Column("driver_id", sa.String(length=80), nullable=True))
    op.create_index("ix_trips_driver_id", "trips", ["driver_id"])


def downgrade() -> None:
    op.drop_index("ix_trips_driver_id", table_name="trips")
    op.drop_column("trips", "driver_id")
