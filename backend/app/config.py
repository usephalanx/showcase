"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os

# JWT settings
SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

# Database
DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./kanban.db")

# CORS
CORS_ORIGINS: list[str] = os.environ.get(
    "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")
