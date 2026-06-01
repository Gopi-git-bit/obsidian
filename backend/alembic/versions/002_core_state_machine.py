"""Add canonical order state machine, audit log, reservations, and DLQ.

Revision ID: 002_core_state_machine
Revises: 001
Create Date: 2026-05-30
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "002_core_state_machine"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return column_name in {column["name"] for column in inspector.get_columns(table_name)}


def _add_column_if_missing(table_name: str, column: sa.Column) -> None:
    if not _has_column(table_name, column.name):
        op.add_column(table_name, column)


def _has_index(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return index_name in {index["name"] for index in inspector.get_indexes(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    _add_column_if_missing("orders", sa.Column("customer_id", sa.String(length=80)))
    _add_column_if_missing("orders", sa.Column("vehicle_id", sa.Uuid()))
    _add_column_if_missing(
        "orders",
        sa.Column("material_type", sa.String(length=60), server_default="general_goods", nullable=False),
    )
    _add_column_if_missing(
        "orders",
        sa.Column("body_type_required", sa.String(length=30), server_default="open", nullable=False),
    )
    _add_column_if_missing(
        "orders",
        sa.Column("payment_mode", sa.String(length=20), server_default="advance", nullable=False),
    )
    _add_column_if_missing(
        "orders",
        sa.Column(
            "topay_consent_status",
            sa.String(length=30),
            server_default="not_required",
            nullable=False,
        ),
    )
    _add_column_if_missing(
        "orders",
        sa.Column("current_state", sa.String(length=60), server_default="CREATED", nullable=False),
    )
    _add_column_if_missing(
        "orders",
        sa.Column("payload_metadata", sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    )

    if _has_column("orders", "status"):
        op.execute(
            """
            UPDATE orders
            SET current_state = CASE UPPER(status)
                WHEN 'CREATED' THEN 'CREATED'
                WHEN 'PENDING_MATCH' THEN 'CONFIRMED'
                WHEN 'BIDDING' THEN 'RINGING'
                WHEN 'MATCHED' THEN 'ASSIGNED'
                WHEN 'BID_ACCEPTED' THEN 'ASSIGNED'
                WHEN 'IN_TRANSIT' THEN 'DEPARTED_FOR_DELIVERY'
                WHEN 'DELIVERED' THEN 'COMPLETED'
                WHEN 'CANCELLED' THEN 'CANCELLED'
                ELSE current_state
            END
            """
        )
        if _has_index("orders", "idx_order_status"):
            op.drop_index("idx_order_status", table_name="orders")
        with op.batch_alter_table("orders") as batch_op:
            batch_op.drop_column("status")

    op.create_index("idx_order_current_state", "orders", ["current_state"], unique=False)
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"], unique=False)
    op.create_index("ix_orders_vehicle_id", "orders", ["vehicle_id"], unique=False)

    op.create_table(
        "state_audit_logs",
        sa.Column("log_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("from_state", sa.String(length=60), nullable=False),
        sa.Column("to_state", sa.String(length=60), nullable=False),
        sa.Column("event_name", sa.String(length=80), nullable=False),
        sa.Column("actor_role", sa.String(length=40), nullable=False),
        sa.Column("actor_id", sa.String(length=80)),
        sa.Column("idempotency_key", sa.Uuid(), nullable=False),
        sa.Column("trace_id", sa.String(length=120), nullable=False),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=False),
        sa.Column("cached_response", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("log_id"),
    )
    op.create_index("idx_state_audit_order_timestamp", "state_audit_logs", ["order_id", "timestamp"])
    op.create_index(
        "idx_state_audit_idempotency_timestamp",
        "state_audit_logs",
        ["idempotency_key", "timestamp"],
    )
    op.create_index("ix_state_audit_logs_trace_id", "state_audit_logs", ["trace_id"])

    op.create_table(
        "vehicle_reservations",
        sa.Column("reservation_id", sa.Uuid(), nullable=False),
        sa.Column("vehicle_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("reservation_id"),
    )
    op.create_index("ix_vehicle_reservations_vehicle_id", "vehicle_reservations", ["vehicle_id"])
    op.create_index("ix_vehicle_reservations_order_id", "vehicle_reservations", ["order_id"])
    where_clause = sa.text("is_active = true" if dialect == "postgresql" else "is_active = 1")
    op.create_index(
        "uq_vehicle_reservations_active_vehicle",
        "vehicle_reservations",
        ["vehicle_id"],
        unique=True,
        postgresql_where=where_clause,
        sqlite_where=where_clause,
    )

    op.create_table(
        "agent_dlq_messages",
        sa.Column("message_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid()),
        sa.Column("event_name", sa.String(length=80), nullable=False),
        sa.Column("actor_role", sa.String(length=40), nullable=False),
        sa.Column("idempotency_key", sa.String(length=120)),
        sa.Column("trace_id", sa.String(length=120)),
        sa.Column("error_code", sa.String(length=40), nullable=False),
        sa.Column("error_detail", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("retry_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("topic", sa.String(length=80), server_default="agent.dlq", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("message_id"),
    )
    op.create_index("idx_agent_dlq_created", "agent_dlq_messages", ["created_at"])
    op.create_index("idx_agent_dlq_trace", "agent_dlq_messages", ["trace_id"])


def downgrade() -> None:
    op.drop_index("idx_agent_dlq_trace", table_name="agent_dlq_messages")
    op.drop_index("idx_agent_dlq_created", table_name="agent_dlq_messages")
    op.drop_table("agent_dlq_messages")

    op.drop_index("uq_vehicle_reservations_active_vehicle", table_name="vehicle_reservations")
    op.drop_index("ix_vehicle_reservations_order_id", table_name="vehicle_reservations")
    op.drop_index("ix_vehicle_reservations_vehicle_id", table_name="vehicle_reservations")
    op.drop_table("vehicle_reservations")

    op.drop_index("ix_state_audit_logs_trace_id", table_name="state_audit_logs")
    op.drop_index("idx_state_audit_idempotency_timestamp", table_name="state_audit_logs")
    op.drop_index("idx_state_audit_order_timestamp", table_name="state_audit_logs")
    op.drop_table("state_audit_logs")

    op.drop_index("ix_orders_vehicle_id", table_name="orders")
    op.drop_index("ix_orders_customer_id", table_name="orders")
    op.drop_index("idx_order_current_state", table_name="orders")
    if not _has_column("orders", "status"):
        op.add_column(
            "orders",
            sa.Column("status", sa.String(length=20), server_default="CREATED", nullable=False),
        )
        op.execute(
            """
            UPDATE orders
            SET status = CASE UPPER(current_state)
                WHEN 'CONFIRMED' THEN 'PENDING_MATCH'
                WHEN 'RINGING' THEN 'BIDDING'
                WHEN 'ASSIGNED' THEN 'MATCHED'
                WHEN 'DEPARTED_FOR_DELIVERY' THEN 'IN_TRANSIT'
                WHEN 'COMPLETED' THEN 'DELIVERED'
                ELSE current_state
            END
            """
        )
        op.create_index("idx_order_status", "orders", ["status"], unique=False)
    for column_name in (
        "payload_metadata",
        "current_state",
        "topay_consent_status",
        "payment_mode",
        "body_type_required",
        "material_type",
        "vehicle_id",
        "customer_id",
    ):
        if _has_column("orders", column_name):
            op.drop_column("orders", column_name)
