"""Shared pytest fixtures for API tests.

Adds the project root to sys.path so that application modules (main,
routes, models, storage) can be imported directly, and provides a
pre-configured TestClient fixture.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from starlette.testclient import TestClient

# Ensure the project root is importable.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from main import app  # noqa: E402
from routes import store  # noqa: E402


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Yield a TestClient for the FastAPI application.

    The in-memory todo store is reset before each test to guarantee
    isolation.
    """
    store.reset()
    with TestClient(app) as c:
        yield c
