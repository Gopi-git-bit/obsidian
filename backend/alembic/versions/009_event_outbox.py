"""Add durable event outbox.

Revision ID: 009_event_outbox
Revises: 008_settlement_hold_release_scope
Create Date: 2026-06-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "009_event_outbox"
down_revision = "008_settlement_hold_release_scope"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_outbox",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("aggregate_type", sa.String(length=60), nullable=False),
        sa.Column("aggregate_id", sa.Uuid(), nullable=False),
        sa.Column("recipient_role", sa.String(length=60), nullable=False),
        sa.Column("recipient_id", sa.String(length=120), nullable=True),
        sa.Column("channel", sa.String(length=30), server_default="in_app", nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="pending", nullable=False),
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=180), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id", name="uq_event_outbox_event_id"),
        sa.UniqueConstraint("idempotency_key", name="uq_event_outbox_idempotency_key"),
    )
    op.create_index("ix_event_outbox_event_type", "event_outbox", ["event_type"])
    op.create_index("ix_event_outbox_aggregate", "event_outbox", ["aggregate_type", "aggregate_id"])
    op.create_index("ix_event_outbox_recipient_role", "event_outbox", ["recipient_role"])
    op.create_index("ix_event_outbox_status", "event_outbox", ["status"])
    op.create_index("ix_event_outbox_created_at", "event_outbox", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_event_outbox_created_at", table_name="event_outbox")
    op.drop_index("ix_event_outbox_status", table_name="event_outbox")
    op.drop_index("ix_event_outbox_recipient_role", table_name="event_outbox")
    op.drop_index("ix_event_outbox_aggregate", table_name="event_outbox")
    op.drop_index("ix_event_outbox_event_type", table_name="event_outbox")
    op.drop_table("event_outbox")
