"""Add supervisor exception cases and holds.

Revision ID: 007_supervisor_exception_holds
Revises: 006_transport_company_ownership
Create Date: 2026-06-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "007_supervisor_exception_holds"
down_revision = "006_transport_company_ownership"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'SUPERVISOR'")

    op.create_table(
        "exception_cases",
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=True),
        sa.Column("trip_id", sa.Uuid(), nullable=True),
        sa.Column("settlement_id", sa.Uuid(), nullable=True),
        sa.Column("case_type", sa.String(length=60), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="open", nullable=False),
        sa.Column("severity", sa.String(length=20), server_default="medium", nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.trip_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["settlement_id"], ["settlement_records.settlement_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("case_id"),
    )
    op.create_index("ix_exception_cases_status", "exception_cases", ["status"])
    op.create_index("ix_exception_cases_case_type", "exception_cases", ["case_type"])
    op.create_index("ix_exception_cases_order_id", "exception_cases", ["order_id"])
    op.create_index("ix_exception_cases_trip_id", "exception_cases", ["trip_id"])

    op.create_table(
        "fraud_holds",
        sa.Column("hold_id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=True),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("placed_by", sa.String(length=80), nullable=False),
        sa.Column("released_by", sa.String(length=80), nullable=True),
        sa.Column("placed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["case_id"], ["exception_cases.case_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("hold_id"),
    )
    op.create_index("ix_fraud_holds_order_id", "fraud_holds", ["order_id"])
    op.create_index("ix_fraud_holds_is_active", "fraud_holds", ["is_active"])

    op.create_table(
        "settlement_holds",
        sa.Column("hold_id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=True),
        sa.Column("settlement_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("placed_by", sa.String(length=80), nullable=False),
        sa.Column("released_by", sa.String(length=80), nullable=True),
        sa.Column("placed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["case_id"], ["exception_cases.case_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["settlement_id"], ["settlement_records.settlement_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("hold_id"),
    )
    op.create_index("ix_settlement_holds_settlement_id", "settlement_holds", ["settlement_id"])
    op.create_index("ix_settlement_holds_is_active", "settlement_holds", ["is_active"])

    op.create_table(
        "supervisor_decisions",
        sa.Column("decision_id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("decision", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("decided_by", sa.String(length=80), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["case_id"], ["exception_cases.case_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("decision_id"),
    )
    op.create_index("ix_supervisor_decisions_case_id", "supervisor_decisions", ["case_id"])


def downgrade() -> None:
    op.drop_index("ix_supervisor_decisions_case_id", table_name="supervisor_decisions")
    op.drop_table("supervisor_decisions")
    op.drop_index("ix_settlement_holds_is_active", table_name="settlement_holds")
    op.drop_index("ix_settlement_holds_settlement_id", table_name="settlement_holds")
    op.drop_table("settlement_holds")
    op.drop_index("ix_fraud_holds_is_active", table_name="fraud_holds")
    op.drop_index("ix_fraud_holds_order_id", table_name="fraud_holds")
    op.drop_table("fraud_holds")
    op.drop_index("ix_exception_cases_trip_id", table_name="exception_cases")
    op.drop_index("ix_exception_cases_order_id", table_name="exception_cases")
    op.drop_index("ix_exception_cases_case_type", table_name="exception_cases")
    op.drop_index("ix_exception_cases_status", table_name="exception_cases")
    op.drop_table("exception_cases")
