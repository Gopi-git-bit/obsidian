"""Add transport company ownership fields.

Revision ID: 006_transport_company_ownership
Revises: 005_trip_driver_assignment
Create Date: 2026-06-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "006_transport_company_ownership"
down_revision = "005_trip_driver_assignment"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("vehicle_models", sa.Column("transport_company_id", sa.String(length=80), nullable=True))
    op.create_index("ix_vehicle_models_transport_company_id", "vehicle_models", ["transport_company_id"])
    op.add_column("matches", sa.Column("transport_company_id", sa.String(length=80), nullable=True))
    op.create_index("ix_matches_transport_company_id", "matches", ["transport_company_id"])
    op.add_column("trips", sa.Column("transport_company_id", sa.String(length=80), nullable=True))
    op.create_index("ix_trips_transport_company_id", "trips", ["transport_company_id"])


def downgrade() -> None:
    op.drop_index("ix_trips_transport_company_id", table_name="trips")
    op.drop_column("trips", "transport_company_id")
    op.drop_index("ix_matches_transport_company_id", table_name="matches")
    op.drop_column("matches", "transport_company_id")
    op.drop_index("ix_vehicle_models_transport_company_id", table_name="vehicle_models")
    op.drop_column("vehicle_models", "transport_company_id")
