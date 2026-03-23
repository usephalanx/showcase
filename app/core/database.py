"""Database engine, session factory, and base model.

Provides the SQLAlchemy engine configured for SQLite, a scoped session
factory, a declarative Base class, and a FastAPI dependency that yields
a database session per request.
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session.

    Yields a :class:`sqlalchemy.orm.Session` and ensures it is closed
    after the request completes, regardless of success or failure.

    Yields:
        Session: An active SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined on :data:`Base` if they do not exist.

    This imports all model modules to ensure they are registered on the
    Base metadata before calling ``create_all``.
    """
    # Import models so they register with Base.metadata
    import app.models.project  # noqa: F401
    import app.models.task  # noqa: F401

    Base.metadata.create_all(bind=engine)
