"""Local account model for JWT-backed RBAC."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, String, Uuid
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    TRANSPORT_COMPANY = "transport_company"
    SUPERVISOR = "supervisor"
    SUPPORT_ADMIN = "support_admin"
    OPS_ADMIN = "ops_admin"
    FINANCE_ADMIN = "finance_admin"
    SUPER_ADMIN = "super_admin"


class UserAccount(Base):
    """Minimal local user account for development and service RBAC."""

    __tablename__ = "user_accounts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
