"""Application configuration settings.

Centralises all configuration values, reading from environment variables
where appropriate, with sensible defaults for local development.
"""

from __future__ import annotations

import os


DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./taskboard.db")

SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 7
