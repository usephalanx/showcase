"""Database engine and session configuration for the Kanban application.

Provides SQLAlchemy engine, session factory, Base declarative class,
and dependency injection helper for FastAPI routes.
"""

from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///kanban.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for use as a FastAPI dependency.

    The session is automatically closed after the request completes.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined in the ORM models.

    Imports models to ensure they are registered with the Base metadata
    before calling ``create_all``.
    """
    import models as _models  # noqa: F401 — ensure models are registered

    Base.metadata.create_all(bind=engine)
