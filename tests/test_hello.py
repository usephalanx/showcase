"""Comprehensive test suite for the /hello endpoint.

Verifies correct behaviour of the FastAPI application's GET /hello
endpoint, including status codes, response payloads, headers, and
error handling for unsupported methods and non-existent routes.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client: TestClient = TestClient(app)


class TestHelloEndpoint:
    """Tests for the GET /hello endpoint."""

    def test_hello_returns_200(self) -> None:
        """GET /hello should return HTTP 200 status code."""
        response = client.get("/hello")
        assert response.status_code == 200

    def test_hello_returns_correct_json(self) -> None:
        """GET /hello should return {'message': 'Hello, World!'}."""
        response = client.get("/hello")
        assert response.json() == {"message": "Hello, World!"}

    def test_hello_content_type_is_json(self) -> None:
        """GET /hello should return a JSON content-type header."""
        response = client.get("/hello")
        assert "application/json" in response.headers["content-type"]

    def test_hello_message_key_present(self) -> None:
        """GET /hello response must contain the 'message' key."""
        response = client.get("/hello")
        data = response.json()
        assert "message" in data

    def test_hello_message_value(self) -> None:
        """GET /hello 'message' value must be exactly 'Hello, World!'."""
        response = client.get("/hello")
        data = response.json()
        assert data["message"] == "Hello, World!"

    def test_hello_response_has_single_key(self) -> None:
        """GET /hello response should contain exactly one key."""
        response = client.get("/hello")
        data = response.json()
        assert len(data) == 1


class TestHelloMethodNotAllowed:
    """Tests verifying that unsupported HTTP methods return 405."""

    def test_post_hello_returns_405(self) -> None:
        """POST /hello should return HTTP 405 Method Not Allowed."""
        response = client.post("/hello")
        assert response.status_code == 405

    def test_put_hello_returns_405(self) -> None:
        """PUT /hello should return HTTP 405 Method Not Allowed."""
        response = client.put("/hello")
        assert response.status_code == 405

    def test_delete_hello_returns_405(self) -> None:
        """DELETE /hello should return HTTP 405 Method Not Allowed."""
        response = client.delete("/hello")
        assert response.status_code == 405

    def test_patch_hello_returns_405(self) -> None:
        """PATCH /hello should return HTTP 405 Method Not Allowed."""
        response = client.patch("/hello")
        assert response.status_code == 405


class TestNonExistentRoutes:
    """Tests verifying that requests to unknown paths return 404."""

    def test_unknown_path_returns_404(self) -> None:
        """GET /nonexistent should return HTTP 404 Not Found."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_root_path_returns_404(self) -> None:
        """GET / should return HTTP 404 when no root route is defined."""
        response = client.get("/")
        assert response.status_code == 404


class TestHelloIdempotency:
    """Tests verifying that repeated calls return consistent results."""

    def test_multiple_calls_return_same_result(self) -> None:
        """Consecutive GET /hello calls should return identical responses."""
        response1 = client.get("/hello")
        response2 = client.get("/hello")
        assert response1.json() == response2.json()
        assert response1.status_code == response2.status_code
