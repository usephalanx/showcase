"""Database configuration and session management.

Provides SQLAlchemy engine, session factory, and base class for
declarative models. Uses SQLite as the backing store.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use.

    Intended for use as a FastAPI dependency.

    Yields:
        Session: An active SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all database tables defined by the ORM models.

    This imports the models module to ensure all model classes are
    registered with ``Base.metadata`` before calling ``create_all``.
    """
    # Import models so they are registered on Base.metadata
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
