"""Application configuration and settings.

Loads configuration from environment variables with sensible defaults
for development. In production, set AUTH_SECRET_KEY to a strong random
value.
"""

from __future__ import annotations

import os


class Settings:
    """Centralised application settings loaded from environment variables."""

    # JWT / Auth
    AUTH_SECRET_KEY: str = os.getenv(
        "AUTH_SECRET_KEY",
        "change-me-in-production-use-a-long-random-string",
    )
    AUTH_ALGORITHM: str = os.getenv("AUTH_ALGORITHM", "HS256")
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()
