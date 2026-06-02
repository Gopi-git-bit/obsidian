"""Add deterministic policy kernel tables.

Revision ID: 010_policy_kernel
Revises: 009_event_outbox
Create Date: 2026-06-02
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from uuid import UUID


revision = "010_policy_kernel"
down_revision = "009_event_outbox"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "policy_registry",
        sa.Column("policy_id", sa.Uuid(), nullable=False),
        sa.Column("policy_code", sa.String(length=80), nullable=False),
        sa.Column("policy_version", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="active", nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("effective_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("policy_id"),
        sa.UniqueConstraint("policy_code", name="uq_policy_registry_policy_code"),
    )
    op.create_index("ix_policy_registry_status", "policy_registry", ["status"])

    op.create_table(
        "policy_decisions",
        sa.Column("decision_id", sa.Uuid(), nullable=False),
        sa.Column("agent_code", sa.String(length=40), nullable=False),
        sa.Column("entity_type", sa.String(length=60), nullable=False),
        sa.Column("entity_id", sa.String(length=120), nullable=False),
        sa.Column("requested_action", sa.String(length=120), nullable=False),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("trace_id", sa.String(length=120), nullable=True),
        sa.Column("idempotency_key", sa.String(length=180), nullable=True),
        sa.Column("confidence_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("evidence_refs", sa.JSON(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("policy_version", sa.String(length=40), nullable=False),
        sa.Column("result", sa.String(length=30), nullable=False),
        sa.Column("reason_code", sa.String(length=80), nullable=False),
        sa.Column("requires_human_review", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("decision_id"),
        sa.UniqueConstraint("idempotency_key", name="uq_policy_decisions_idempotency_key"),
    )
    op.create_index("ix_policy_decisions_agent_code", "policy_decisions", ["agent_code"])
    op.create_index("ix_policy_decisions_entity", "policy_decisions", ["entity_type", "entity_id"])
    op.create_index("ix_policy_decisions_result", "policy_decisions", ["result"])
    op.create_index("ix_policy_decisions_trace_id", "policy_decisions", ["trace_id"])

    op.create_table(
        "route_zone_policy",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("route_zone", sa.String(length=80), nullable=False),
        sa.Column("min_gross_margin_pct", sa.Numeric(6, 2), nullable=False),
        sa.Column("max_allowable_delay_mins", sa.Integer(), nullable=False),
        sa.Column("compliance_required", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("vehicle_supply_threshold_pct", sa.Numeric(6, 2), nullable=False),
        sa.Column("crisis_margin_buffer_pct", sa.Numeric(6, 2), server_default="0", nullable=False),
        sa.Column("policy_version", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("route_zone", name="uq_route_zone_policy_route_zone"),
    )

    op.create_table(
        "compliance_document_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("shipment_type", sa.String(length=60), nullable=False),
        sa.Column("route_type", sa.String(length=60), nullable=False),
        sa.Column("document_name", sa.String(length=120), nullable=False),
        sa.Column("mandatory", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("validation_endpoint", sa.String(length=160), nullable=True),
        sa.Column("policy_version", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_compliance_rules_lookup", "compliance_document_rules", ["shipment_type", "route_type"])

    op.create_table(
        "confidence_thresholds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("decision_category", sa.String(length=60), nullable=False),
        sa.Column("minimum_confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("below_threshold_action", sa.String(length=80), nullable=False),
        sa.Column("policy_version", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("decision_category", name="uq_confidence_thresholds_category"),
    )

    op.bulk_insert(
        sa.table(
            "policy_registry",
            sa.column("policy_id", sa.Uuid()),
            sa.column("policy_code", sa.String()),
            sa.column("policy_version", sa.String()),
            sa.column("status", sa.String()),
            sa.column("description", sa.Text()),
        ),
        [
            {
                "policy_id": UUID("00000000-0000-0000-0000-000000000010"),
                "policy_code": "zippy-agent-policy-framework",
                "policy_version": "1.0",
                "status": "active",
                "description": "Minimal deterministic policy kernel for MVP agent recommendations.",
            }
        ],
    )
    op.bulk_insert(
        sa.table(
            "route_zone_policy",
            sa.column("id", sa.Uuid()),
            sa.column("route_zone", sa.String()),
            sa.column("min_gross_margin_pct", sa.Numeric()),
            sa.column("max_allowable_delay_mins", sa.Integer()),
            sa.column("compliance_required", sa.Boolean()),
            sa.column("vehicle_supply_threshold_pct", sa.Numeric()),
            sa.column("crisis_margin_buffer_pct", sa.Numeric()),
            sa.column("policy_version", sa.String()),
        ),
        [
            {"id": UUID("00000000-0000-0000-0000-000000000101"), "route_zone": "TN_TO_KA", "min_gross_margin_pct": 12, "max_allowable_delay_mins": 180, "compliance_required": True, "vehicle_supply_threshold_pct": 15, "crisis_margin_buffer_pct": 3, "policy_version": "1.0"},
            {"id": UUID("00000000-0000-0000-0000-000000000102"), "route_zone": "INTRA_TN", "min_gross_margin_pct": 10, "max_allowable_delay_mins": 120, "compliance_required": False, "vehicle_supply_threshold_pct": 10, "crisis_margin_buffer_pct": 3, "policy_version": "1.0"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "confidence_thresholds",
            sa.column("id", sa.Uuid()),
            sa.column("decision_category", sa.String()),
            sa.column("minimum_confidence", sa.Numeric()),
            sa.column("below_threshold_action", sa.String()),
            sa.column("policy_version", sa.String()),
        ),
        [
            {"id": UUID("00000000-0000-0000-0000-000000000201"), "decision_category": "financial", "minimum_confidence": 0.85, "below_threshold_action": "human_review", "policy_version": "1.0"},
            {"id": UUID("00000000-0000-0000-0000-000000000202"), "decision_category": "compliance", "minimum_confidence": 0.95, "below_threshold_action": "human_review", "policy_version": "1.0"},
            {"id": UUID("00000000-0000-0000-0000-000000000203"), "decision_category": "operational", "minimum_confidence": 0.75, "below_threshold_action": "human_review", "policy_version": "1.0"},
            {"id": UUID("00000000-0000-0000-0000-000000000204"), "decision_category": "communication", "minimum_confidence": 0.70, "below_threshold_action": "human_review", "policy_version": "1.0"},
        ],
    )
    op.bulk_insert(
        sa.table(
            "compliance_document_rules",
            sa.column("id", sa.Uuid()),
            sa.column("shipment_type", sa.String()),
            sa.column("route_type", sa.String()),
            sa.column("document_name", sa.String()),
            sa.column("mandatory", sa.Boolean()),
            sa.column("validation_endpoint", sa.String()),
            sa.column("policy_version", sa.String()),
        ),
        [
            {"id": UUID("00000000-0000-0000-0000-000000000301"), "shipment_type": "FTL", "route_type": "INTER_STATE", "document_name": "E-Way Bill", "mandatory": True, "validation_endpoint": "/rag/ocr/validate", "policy_version": "1.0"},
            {"id": UUID("00000000-0000-0000-0000-000000000302"), "shipment_type": "FTL", "route_type": "INTRA_STATE", "document_name": "Lorry Receipt", "mandatory": True, "validation_endpoint": "/rag/ocr/validate", "policy_version": "1.0"},
        ],
    )


def downgrade() -> None:
    op.drop_table("confidence_thresholds")
    op.drop_index("ix_compliance_rules_lookup", table_name="compliance_document_rules")
    op.drop_table("compliance_document_rules")
    op.drop_table("route_zone_policy")
    op.drop_index("ix_policy_decisions_trace_id", table_name="policy_decisions")
    op.drop_index("ix_policy_decisions_result", table_name="policy_decisions")
    op.drop_index("ix_policy_decisions_entity", table_name="policy_decisions")
    op.drop_index("ix_policy_decisions_agent_code", table_name="policy_decisions")
    op.drop_table("policy_decisions")
    op.drop_index("ix_policy_registry_status", table_name="policy_registry")
    op.drop_table("policy_registry")
