"""Shared pytest fixtures for the Todo API test suite."""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Yield a ``TestClient`` with a clean storage for each test."""
    storage.clear()
    with TestClient(app) as tc:
        yield tc
    storage.clear()
