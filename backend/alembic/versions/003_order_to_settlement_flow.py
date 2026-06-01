"""Add durable order-to-settlement flow records.

Revision ID: 003_order_to_settlement_flow
Revises: 002_core_state_machine
Create Date: 2026-06-01
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "003_order_to_settlement_flow"
down_revision = "002_core_state_machine"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "quote_records",
        sa.Column("quote_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("base_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("platform_fee", sa.Numeric(12, 2), nullable=False),
        sa.Column("gst_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="generated", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("quote_id"),
    )
    op.create_index("ix_quote_records_order_id", "quote_records", ["order_id"])

    op.create_table(
        "trips",
        sa.Column("trip_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("vehicle_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=40), server_default="created", nullable=False),
        sa.Column("otp_verified", sa.String(length=10), server_default="false", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle_models.id"]),
        sa.PrimaryKeyConstraint("trip_id"),
        sa.UniqueConstraint("order_id"),
    )

    op.create_table(
        "payment_records",
        sa.Column("payment_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("trip_id", sa.Uuid()),
        sa.Column("payment_type", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="recorded", nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("provider_ref", sa.String(length=120)),
        sa.Column("idempotency_key", sa.String(length=120), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.trip_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("payment_id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_payment_records_order_id", "payment_records", ["order_id"])

    op.create_table(
        "trip_documents",
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("trip_id", sa.Uuid(), nullable=False),
        sa.Column("document_type", sa.String(length=40), nullable=False),
        sa.Column("document_url", sa.Text(), nullable=False),
        sa.Column("verification_status", sa.String(length=30), server_default="uploaded", nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("verified_at", sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.trip_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("document_id"),
    )
    op.create_index("ix_trip_documents_order_id", "trip_documents", ["order_id"])
    op.create_index("ix_trip_documents_trip_id", "trip_documents", ["trip_id"])
    op.create_index("idx_trip_documents_type_status", "trip_documents", ["document_type", "verification_status"])

    op.create_table(
        "trip_milestones",
        sa.Column("milestone_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("trip_id", sa.Uuid(), nullable=False),
        sa.Column("milestone_type", sa.String(length=60), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="recorded", nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=120), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.trip_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("milestone_id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_trip_milestones_order_id", "trip_milestones", ["order_id"])
    op.create_index("ix_trip_milestones_trip_id", "trip_milestones", ["trip_id"])

    op.create_table(
        "settlement_records",
        sa.Column("settlement_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("trip_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="released", nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("idempotency_key", sa.String(length=120), nullable=False),
        sa.Column("released_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.trip_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("settlement_id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_settlement_records_order_id", "settlement_records", ["order_id"])
    op.create_index("ix_settlement_records_trip_id", "settlement_records", ["trip_id"])

    op.create_table(
        "journal_entries",
        sa.Column("journal_entry_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("settlement_id", sa.Uuid(), nullable=False),
        sa.Column("debit_ledger", sa.String(length=120), nullable=False),
        sa.Column("credit_ledger", sa.String(length=120), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("idempotency_key", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["settlement_id"], ["settlement_records.settlement_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("journal_entry_id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_journal_entries_order_id", "journal_entries", ["order_id"])

    op.create_table(
        "gst_invoice_records",
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("settlement_id", sa.Uuid(), nullable=False),
        sa.Column("invoice_number", sa.String(length=80), nullable=False),
        sa.Column("taxable_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("gst_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="created", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["settlement_id"], ["settlement_records.settlement_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("invoice_id"),
        sa.UniqueConstraint("invoice_number"),
    )
    op.create_index("ix_gst_invoice_records_order_id", "gst_invoice_records", ["order_id"])


def downgrade() -> None:
    op.drop_index("ix_gst_invoice_records_order_id", table_name="gst_invoice_records")
    op.drop_table("gst_invoice_records")
    op.drop_index("ix_journal_entries_order_id", table_name="journal_entries")
    op.drop_table("journal_entries")
    op.drop_index("ix_settlement_records_trip_id", table_name="settlement_records")
    op.drop_index("ix_settlement_records_order_id", table_name="settlement_records")
    op.drop_table("settlement_records")
    op.drop_index("ix_trip_milestones_trip_id", table_name="trip_milestones")
    op.drop_index("ix_trip_milestones_order_id", table_name="trip_milestones")
    op.drop_table("trip_milestones")
    op.drop_index("idx_trip_documents_type_status", table_name="trip_documents")
    op.drop_index("ix_trip_documents_trip_id", table_name="trip_documents")
    op.drop_index("ix_trip_documents_order_id", table_name="trip_documents")
    op.drop_table("trip_documents")
    op.drop_index("ix_payment_records_order_id", table_name="payment_records")
    op.drop_table("payment_records")
    op.drop_table("trips")
    op.drop_index("ix_quote_records_order_id", table_name="quote_records")
    op.drop_table("quote_records")
