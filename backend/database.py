"""SQLite database layer using SQLAlchemy.

Provides engine creation, session management, and schema initialisation
for the tasks table.  Uses a file-based SQLite database (tasks.db) by
default; the database URL can be overridden for testing.

Design decisions
----------------
- SQLAlchemy is used with synchronous SQLite for simplicity and broad
  compatibility.  ``check_same_thread=False`` is passed via connect_args
  so the connection can be reused across ASGI worker threads.
- ``DATETIME`` column uses SQLAlchemy's DateTime type, which SQLite
  stores as a TEXT ISO-8601 string (SQLite has no native datetime).
- Status is constrained at the application / schema layer rather than
  via a CHECK constraint so that the validation error messages are
  user-friendly (Pydantic handles this).
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.engine import Engine

DATABASE_URL: str = "sqlite:///./tasks.db"

engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def init_db() -> None:
    """Create all tables defined by ORM models if they do not already exist.

    This imports :mod:`backend.models` to ensure the Task model is
    registered on :data:`Base.metadata` before calling
    ``create_all``.
    """
    # Import here to ensure models are registered on Base.metadata
    import backend.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db() -> Session:  # type: ignore[misc]
    """Yield a SQLAlchemy database session.

    Intended to be used as a FastAPI dependency.  The session is
    automatically closed when the request finishes.

    Yields:
        Session: A SQLAlchemy ORM session bound to the engine.
    """
    db = SessionLocal()
    try:
        yield db  # type: ignore[misc]
    finally:
        db.close()
