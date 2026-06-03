"""Local development auth endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.config import is_development
from app.database import get_db
from app.models.auth_model import UserAccount, UserRole

router = APIRouter()


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=120)
    password: str = Field(..., min_length=1, max_length=120)


class DevLoginRequest(LoginRequest):
    role: UserRole = UserRole.OPS_ADMIN


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    username: str


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserAccount).filter(UserAccount.username == payload.username).first()
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return TokenResponse(
        access_token=create_access_token(user),
        role=user.role,
        username=user.username,
    )


@router.post("/auth/dev-login", response_model=TokenResponse)
async def dev_login(payload: DevLoginRequest, db: Session = Depends(get_db)):
    """Create/update a local dev user and return a JWT.

    This intentionally avoids OAuth while keeping browser tests and local
    operator workflows on the same Authorization header path as production.
    """
    if not is_development():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    user = db.query(UserAccount).filter(UserAccount.username == payload.username).first()
    if user:
        user.password_hash = hash_password(payload.password)
        user.role = payload.role
        user.is_active = True
    else:
        user = UserAccount(
            username=payload.username,
            password_hash=hash_password(payload.password),
            role=payload.role,
            is_active=True,
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(
        access_token=create_access_token(user),
        role=user.role,
        username=user.username,
    )
