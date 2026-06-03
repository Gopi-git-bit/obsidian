"""Runtime environment configuration."""

from __future__ import annotations

import os
from functools import lru_cache


VALID_APP_ENVS = {"development", "pilot", "production"}


def _normalize_app_env(value: str | None) -> str:
    env = (value or "development").strip().lower()
    if env not in VALID_APP_ENVS:
        raise ValueError(f"APP_ENV must be one of: {', '.join(sorted(VALID_APP_ENVS))}")
    return env


@lru_cache
def app_env() -> str:
    return _normalize_app_env(os.getenv("APP_ENV"))


def is_development() -> bool:
    return app_env() == "development"


@lru_cache
def cors_allowed_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "*")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["*"]
