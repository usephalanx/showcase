"""SQLite in-memory database configuration using SQLAlchemy.

Provides the database engine, session factory, declarative base, and
a FastAPI-compatible dependency for obtaining database sessions.

- Engine uses ``sqlite://`` (in-memory) with ``check_same_thread=False``
  so that the same connection can be reused across ASGI threads.
- ``SessionLocal`` is a ``sessionmaker`` bound to the engine.
- ``Base`` is the declarative base for all ORM models.
- ``get_db`` is a generator dependency that yields a session and
  ensures it is closed after the request completes.
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL: str = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a SQLAlchemy database session.

    Yields a ``Session`` instance and guarantees it is closed when the
    request finishes, regardless of whether an exception occurred.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
