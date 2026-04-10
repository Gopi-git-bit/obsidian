"""
Vehicle Models SQLAlchemy Model
"""

from sqlalchemy import (
    Column,
    String,
    Numeric,
    Boolean,
    Integer,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class VehicleModel(Base):
    """Vehicle model database table"""

    __tablename__ = "vehicle_models"

    # Table constraints
    __table_args__ = (
        CheckConstraint(
            "category IN ('LCV', 'ICV', 'HCV', 'Tipper', 'Tractor')",
            name="valid_category",
        ),
        CheckConstraint(
            "body_type IN ('open', 'closed', 'tipper', 'tanker', 'trailer')",
            name="valid_body_type",
        ),
    )

    # Columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    manufacturer = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    variant = Column(String(50))
    category = Column(String(30), nullable=False)
    body_type = Column(String(20), nullable=False)

    # Weight specs
    gvw_kg = Column(Numeric(10, 2))  # Gross Vehicle Weight
    payload_kg = Column(Numeric(10, 2))
    tonnage_class = Column(String(20))

    # Dimensions (mm)
    length_mm = Column(Numeric(10, 2))
    width_mm = Column(Numeric(10, 2))
    height_mm = Column(Numeric(10, 2))
    wheelbase_mm = Column(Numeric(10, 2))
    loading_length_mm = Column(Numeric(10, 2))
    loading_width_mm = Column(Numeric(10, 2))
    loading_height_mm = Column(Numeric(10, 2))

    # Engine specs
    engine_cc = Column(Numeric(10, 2))
    engine_cylinders = Column(Integer)
    power_hp = Column(Numeric(10, 2))
    torque_nm = Column(Numeric(10, 2))
    fuel_tank_ltr = Column(Numeric(10, 2))
    mileage_kmpl = Column(Numeric(5, 2))
    emission_norm = Column(String(10))

    # Configuration
    axle_config = Column(String(20))
    tyres = Column(Integer)
    price_ex_showroom = Column(Numeric(15, 2))

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (
        CheckConstraint(
            "category IN ('LCV', 'ICV', 'HCV', 'Tipper', 'Tractor')",
            name="valid_category",
        ),
        CheckConstraint(
            "body_type IN ('open', 'closed', 'tipper', 'tanker', 'trailer')",
            name="valid_body_type",
        ),
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<VehicleModel {self.manufacturer} {self.model_name} {self.variant}>"
