"""Initial schema - vehicle_models, orders, bids, matches

Revision ID: 001_initial
Revises: None
Create Date: 2026-04-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vehicle_models",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("manufacturer", sa.String(50), nullable=False),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("variant", sa.String(50)),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("body_type", sa.String(20), nullable=False),
        sa.Column("gvw_kg", sa.Numeric(10, 2)),
        sa.Column("payload_kg", sa.Numeric(10, 2)),
        sa.Column("tonnage_class", sa.String(20)),
        sa.Column("length_mm", sa.Numeric(10, 2)),
        sa.Column("width_mm", sa.Numeric(10, 2)),
        sa.Column("height_mm", sa.Numeric(10, 2)),
        sa.Column("wheelbase_mm", sa.Numeric(10, 2)),
        sa.Column("loading_length_mm", sa.Numeric(10, 2)),
        sa.Column("loading_width_mm", sa.Numeric(10, 2)),
        sa.Column("loading_height_mm", sa.Numeric(10, 2)),
        sa.Column("engine_cc", sa.Numeric(10, 2)),
        sa.Column("engine_cylinders", sa.Integer()),
        sa.Column("power_hp", sa.Numeric(10, 2)),
        sa.Column("torque_nm", sa.Numeric(10, 2)),
        sa.Column("fuel_tank_ltr", sa.Numeric(10, 2)),
        sa.Column("mileage_kmpl", sa.Numeric(5, 2)),
        sa.Column("emission_norm", sa.String(10)),
        sa.Column("axle_config", sa.String(20)),
        sa.Column("tyres", sa.Integer()),
        sa.Column("price_ex_showroom", sa.Numeric(15, 2)),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.CheckConstraint(
            "category IN ('LCV', 'ICV', 'HCV', 'Tipper', 'Tractor')",
            name="valid_category",
        ),
        sa.CheckConstraint(
            "body_type IN ('open', 'closed', 'tipper', 'tanker', 'trailer')",
            name="valid_body_type",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "orders",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("shipper_name", sa.String(150), nullable=False),
        sa.Column("shipper_phone", sa.String(15), nullable=False),
        sa.Column("shipper_email", sa.String(255)),
        sa.Column("origin_city", sa.String(100), nullable=False),
        sa.Column("origin_state", sa.String(50), nullable=False),
        sa.Column("origin_pincode", sa.String(10)),
        sa.Column("origin_lat", sa.Numeric(9, 6)),
        sa.Column("origin_lng", sa.Numeric(9, 6)),
        sa.Column("destination_city", sa.String(100), nullable=False),
        sa.Column("destination_state", sa.String(50), nullable=False),
        sa.Column("destination_pincode", sa.String(10)),
        sa.Column("destination_lat", sa.Numeric(9, 6)),
        sa.Column("destination_lng", sa.Numeric(9, 6)),
        sa.Column("cargo_type", sa.String(20), nullable=False),
        sa.Column("cargo_description", sa.Text()),
        sa.Column("weight_kg", sa.Numeric(10, 2), nullable=False),
        sa.Column("volume_cbm", sa.Numeric(10, 2)),
        sa.Column("num_packages", sa.Integer(), server_default="1"),
        sa.Column("vehicle_category_preference", sa.String(30)),
        sa.Column("is_interstate", sa.Boolean(), server_default="false"),
        sa.Column("is_festival_period", sa.Boolean(), server_default="false"),
        sa.Column("is_remote_location", sa.Boolean(), server_default="false"),
        sa.Column("is_hill_area", sa.Boolean(), server_default="false"),
        sa.Column("estimated_distance_km", sa.Numeric(10, 2)),
        sa.Column("estimated_duration_hours", sa.Numeric(6, 2)),
        sa.Column("offered_price", sa.Numeric(12, 2)),
        sa.Column("negotiated_price", sa.Numeric(12, 2)),
        sa.Column("pickup_datetime", sa.DateTime(timezone=True)),
        sa.Column("delivery_deadline", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.CheckConstraint("weight_kg > 0", name="positive_weight"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_order_status", "orders", ["status"])
    op.create_index(
        "idx_order_origin_dest", "orders", ["origin_city", "destination_city"]
    )
    op.create_index("idx_order_created", "orders", ["created_at"])

    op.create_table(
        "bids",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("driver_name", sa.String(150), nullable=False),
        sa.Column("driver_phone", sa.String(15), nullable=False),
        sa.Column("bid_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("counter_amount", sa.Numeric(12, 2)),
        sa.Column("estimated_eta_hours", sa.Numeric(6, 2)),
        sa.Column("estimated_arrival_hours", sa.Numeric(6, 2)),
        sa.Column("vehicle_available_at", sa.DateTime(timezone=True)),
        sa.Column("notes", sa.Text()),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.CheckConstraint("bid_amount > 0", name="positive_bid"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle_models.id"]),
    )
    op.create_index("idx_bid_order_status", "bids", ["order_id", "status"])

    op.create_table(
        "matches",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bid_id", postgresql.UUID(as_uuid=True)),
        sa.Column("match_score", sa.Numeric(5, 2)),
        sa.Column("utilization_percent", sa.Numeric(5, 2)),
        sa.Column("efficiency_score", sa.Numeric(5, 2)),
        sa.Column("agreed_price", sa.Numeric(12, 2)),
        sa.Column("platform_fee", sa.Numeric(10, 2)),
        sa.Column("gst_amount", sa.Numeric(10, 2)),
        sa.Column("total_amount", sa.Numeric(12, 2)),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column(
            "matched_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.Column("accepted_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicle_models.id"]),
        sa.ForeignKeyConstraint(["bid_id"], ["bids.id"]),
    )
    op.create_index("idx_match_status", "matches", ["status"])
    op.create_index("idx_match_order_vehicle", "matches", ["order_id", "vehicle_id"])


def downgrade() -> None:
    op.drop_table("matches")
    op.drop_table("bids")
    op.drop_table("orders")
    op.drop_table("vehicle_models")
