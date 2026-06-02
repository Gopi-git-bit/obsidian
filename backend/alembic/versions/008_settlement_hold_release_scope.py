"""Scope settlement holds before and after release.

Revision ID: 008_settlement_hold_release_scope
Revises: 007_supervisor_exception_holds
Create Date: 2026-06-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "008_settlement_hold_release_scope"
down_revision = "007_supervisor_exception_holds"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("settlement_holds") as batch_op:
        batch_op.add_column(sa.Column("order_id", sa.Uuid(), nullable=True))
        batch_op.add_column(sa.Column("trip_id", sa.Uuid(), nullable=True))
        batch_op.alter_column("settlement_id", existing_type=sa.Uuid(), nullable=True)
        batch_op.create_index("ix_settlement_holds_order_id", ["order_id"])
        batch_op.create_index("ix_settlement_holds_trip_id", ["trip_id"])


def downgrade() -> None:
    with op.batch_alter_table("settlement_holds") as batch_op:
        batch_op.drop_index("ix_settlement_holds_trip_id")
        batch_op.drop_index("ix_settlement_holds_order_id")
        batch_op.alter_column("settlement_id", existing_type=sa.Uuid(), nullable=False)
        batch_op.drop_column("trip_id")
        batch_op.drop_column("order_id")
