"""Tests for the /hello endpoint.

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


class TestHelloEndpoint:
    """Test suite for GET /hello."""

    def test_hello_returns_200(self, client: TestClient) -> None:
        """GET /hello should return HTTP 200."""
        response = client.get("/hello")
        assert response.status_code == 200

    def test_hello_returns_correct_json(self, client: TestClient) -> None:
        """GET /hello should return {"message": "hello world"}."""
        response = client.get("/hello")
        assert response.json() == {"message": "hello world"}

    def test_hello_content_type_is_json(self, client: TestClient) -> None:
        """Response Content-Type must be application/json."""
        response = client.get("/hello")
        assert "application/json" in response.headers["content-type"]

    def test_hello_with_extra_query_params(self, client: TestClient) -> None:
        """Extra query parameters should be ignored; response stays the same."""
        response = client.get("/hello", params={"foo": "bar", "baz": "123"})
        assert response.status_code == 200
        assert response.json() == {"message": "hello world"}

    def test_hello_post_not_allowed(self, client: TestClient) -> None:
        """POST /hello should return 405 Method Not Allowed."""
        response = client.post("/hello")
        assert response.status_code == 405

    def test_hello_put_not_allowed(self, client: TestClient) -> None:
        """PUT /hello should return 405 Method Not Allowed."""
        response = client.put("/hello")
        assert response.status_code == 405

    def test_hello_delete_not_allowed(self, client: TestClient) -> None:
        """DELETE /hello should return 405 Method Not Allowed."""
        response = client.delete("/hello")
        assert response.status_code == 405

    def test_hello_patch_not_allowed(self, client: TestClient) -> None:
        """PATCH /hello should return 405 Method Not Allowed."""
        response = client.patch("/hello")
        assert response.status_code == 405

    def test_hello_response_has_message_key(self, client: TestClient) -> None:
        """The JSON body must contain exactly the 'message' key."""
        data = client.get("/hello").json()
        assert list(data.keys()) == ["message"]

    def test_hello_message_value_type_is_string(self, client: TestClient) -> None:
        """The 'message' value must be a string."""
        data = client.get("/hello").json()
        assert isinstance(data["message"], str)
