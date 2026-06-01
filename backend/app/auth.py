"""JWT authentication and role dependencies."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Iterable
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.auth_model import UserAccount, UserRole


JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-zippy-logistics-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "480"))

ADMIN_ROLES = {
    UserRole.SUPERVISOR.value,
    UserRole.SUPPORT_ADMIN.value,
    UserRole.OPS_ADMIN.value,
    UserRole.FINANCE_ADMIN.value,
    UserRole.SUPER_ADMIN.value,
}
SUPERVISOR_ROLES = {UserRole.SUPERVISOR.value, UserRole.SUPER_ADMIN.value}
OPS_ADMIN_ROLES = {UserRole.OPS_ADMIN.value, UserRole.SUPER_ADMIN.value}
FINANCE_ADMIN_ROLES = {UserRole.FINANCE_ADMIN.value, UserRole.SUPER_ADMIN.value}
SUPPORT_READ_ROLES = {
    UserRole.SUPPORT_ADMIN.value,
    UserRole.OPS_ADMIN.value,
    UserRole.FINANCE_ADMIN.value,
    UserRole.SUPER_ADMIN.value,
}
VERIFICATION_ROLES = {
    UserRole.OPS_ADMIN.value,
    UserRole.SUPERVISOR.value,
    UserRole.SUPER_ADMIN.value,
}
CUSTOMER_ORDER_ROLES = {UserRole.CUSTOMER.value, *ADMIN_ROLES}
DRIVER_TRIP_ROLES = {UserRole.DRIVER.value, *ADMIN_ROLES}
TRANSPORT_COMPANY_ROLES = {UserRole.TRANSPORT_COMPANY.value, *ADMIN_ROLES}

password_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_access_token(user: UserAccount) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value,
        "exp": expires_at,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserAccount:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        user_id = UUID(str(payload.get("sub")))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing account",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(roles: Iterable[str]):
    allowed = set(roles)

    def dependency(user: UserAccount = Depends(get_current_user)) -> UserAccount:
        if user.role.value not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return user

    return dependency
