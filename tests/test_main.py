"""Tests for the /health endpoint of the FastAPI application."""

from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_health() -> None:
    """GET /health returns 200 with {"status": "ok"} JSON body."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
