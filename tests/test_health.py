"""Tests for the /health endpoint.

Covers happy-path responses, correct content type, method restrictions,
and behaviour when extra query parameters are supplied.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """Return a TestClient wired to the FastAPI application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test suite for GET /health."""

    def test_health_returns_200(self, client: TestClient) -> None:
        """GET /health should return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_correct_json(self, client: TestClient) -> None:
        """GET /health should return {"status": "ok"}."""
        response = client.get("/health")
        assert response.json() == {"status": "ok"}

    def test_health_content_type_is_json(self, client: TestClient) -> None:
        """Response Content-Type must be application/json."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

    def test_health_with_extra_query_params(self, client: TestClient) -> None:
        """Extra query parameters should be ignored; response stays the same."""
        response = client.get("/health", params={"debug": "true"})
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_post_not_allowed(self, client: TestClient) -> None:
        """POST /health should return 405 Method Not Allowed."""
        response = client.post("/health")
        assert response.status_code == 405

    def test_health_put_not_allowed(self, client: TestClient) -> None:
        """PUT /health should return 405 Method Not Allowed."""
        response = client.put("/health")
        assert response.status_code == 405

    def test_health_delete_not_allowed(self, client: TestClient) -> None:
        """DELETE /health should return 405 Method Not Allowed."""
        response = client.delete("/health")
        assert response.status_code == 405

    def test_health_patch_not_allowed(self, client: TestClient) -> None:
        """PATCH /health should return 405 Method Not Allowed."""
        response = client.patch("/health")
        assert response.status_code == 405

    def test_health_response_has_status_key(self, client: TestClient) -> None:
        """The JSON body must contain exactly the 'status' key."""
        data = client.get("/health").json()
        assert list(data.keys()) == ["status"]

    def test_health_status_value_is_ok(self, client: TestClient) -> None:
        """The 'status' value must be the string 'ok'."""
        data = client.get("/health").json()
        assert data["status"] == "ok"
