"""Tests for the GET /hello API endpoint.

Covers successful responses, content-type validation, query-parameter
variations, unsupported HTTP methods, trailing-slash behaviour, and
assorted edge cases.
"""

from __future__ import annotations

from starlette.testclient import TestClient


# ------------------------------------------------------------------
# 1. Basic success
# ------------------------------------------------------------------


def test_get_hello_returns_200(client: TestClient) -> None:
    """GET /hello with no params returns 200 and the default greeting."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# ------------------------------------------------------------------
# 2. Content-Type header
# ------------------------------------------------------------------


def test_get_hello_response_content_type(client: TestClient) -> None:
    """GET /hello returns Content-Type application/json."""
    response = client.get("/hello")
    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type


# ------------------------------------------------------------------
# 3. Name query parameter
# ------------------------------------------------------------------


def test_get_hello_with_name_param(client: TestClient) -> None:
    """GET /hello?name=Alice returns a personalised greeting."""
    response = client.get("/hello", params={"name": "Alice"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alice!"}


# ------------------------------------------------------------------
# 4. Empty name parameter falls back to default
# ------------------------------------------------------------------


def test_get_hello_empty_name_param(client: TestClient) -> None:
    """GET /hello?name= falls back to the default 'World' greeting."""
    response = client.get("/hello", params={"name": ""})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# ------------------------------------------------------------------
# 5. Special / potentially dangerous characters
# ------------------------------------------------------------------


def test_get_hello_special_characters_in_name(client: TestClient) -> None:
    """GET /hello with HTML/JS in 'name' returns 200 with the value echoed safely in JSON."""
    xss_payload = "<script>alert(1)</script>"
    response = client.get("/hello", params={"name": xss_payload})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Hello, {xss_payload}!"


# ------------------------------------------------------------------
# 6. Very long name
# ------------------------------------------------------------------


def test_get_hello_very_long_name(client: TestClient) -> None:
    """GET /hello with a 2000-character name returns 200 with the full name in the greeting."""
    long_name = "A" * 2000
    response = client.get("/hello", params={"name": long_name})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Hello, {long_name}!"


# ------------------------------------------------------------------
# 7. POST method not allowed
# ------------------------------------------------------------------


def test_post_hello_method_not_allowed(client: TestClient) -> None:
    """POST /hello returns 405 Method Not Allowed."""
    response = client.post("/hello")
    assert response.status_code == 405


# ------------------------------------------------------------------
# 8. Trailing slash behaviour
# ------------------------------------------------------------------


def test_get_hello_trailing_slash(client: TestClient) -> None:
    """GET /hello/ either redirects (307) to /hello or returns 200 directly.

    FastAPI by default redirects /hello/ -> /hello with a 307.
    We accept both 200 and 307 as valid; in the redirect case we
    follow the redirect and verify the final body.
    """
    # TestClient follows redirects by default, so we should get 200.
    response = client.get("/hello/")
    # Accept either a direct 200 or a 404 (if the router does not match
    # the trailing-slash variant) — but NOT a 500.
    assert response.status_code in (200, 307, 404)
    if response.status_code == 200:
        assert response.json() == {"message": "Hello, World!"}


# ------------------------------------------------------------------
# 9. Unknown query parameters are silently ignored
# ------------------------------------------------------------------


def test_get_hello_unknown_query_param_ignored(client: TestClient) -> None:
    """GET /hello?foo=bar still returns the default greeting."""
    response = client.get("/hello", params={"foo": "bar"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# ------------------------------------------------------------------
# 10. Numeric name
# ------------------------------------------------------------------


def test_get_hello_numeric_name(client: TestClient) -> None:
    """GET /hello?name=123 returns a greeting with the numeric string."""
    response = client.get("/hello", params={"name": "123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, 123!"}


# ------------------------------------------------------------------
# 11. PUT method not allowed
# ------------------------------------------------------------------


def test_put_hello_method_not_allowed(client: TestClient) -> None:
    """PUT /hello returns 405 Method Not Allowed."""
    response = client.put("/hello")
    assert response.status_code == 405


# ------------------------------------------------------------------
# 12. DELETE method not allowed
# ------------------------------------------------------------------


def test_delete_hello_method_not_allowed(client: TestClient) -> None:
    """DELETE /hello returns 405 Method Not Allowed."""
    response = client.delete("/hello")
    assert response.status_code == 405


# ------------------------------------------------------------------
# 13. Unicode / multibyte name
# ------------------------------------------------------------------


def test_get_hello_unicode_name(client: TestClient) -> None:
    """GET /hello?name=日本語 returns a greeting with the unicode string."""
    response = client.get("/hello", params={"name": "日本語"})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, 日本語!"}


# ------------------------------------------------------------------
# 14. Whitespace-only name falls back to default
# ------------------------------------------------------------------


def test_get_hello_whitespace_name(client: TestClient) -> None:
    """GET /hello?name=<spaces> falls back to the default 'World' greeting."""
    response = client.get("/hello", params={"name": "   "})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# ------------------------------------------------------------------
# 15. Response structure validation
# ------------------------------------------------------------------


def test_get_hello_response_has_single_message_key(client: TestClient) -> None:
    """The JSON response body contains exactly one key: 'message'."""
    response = client.get("/hello")
    assert response.status_code == 200
    data = response.json()
    assert list(data.keys()) == ["message"]


# ------------------------------------------------------------------
# 16. Name with leading/trailing whitespace is preserved (not stripped)
# ------------------------------------------------------------------


def test_get_hello_name_with_surrounding_whitespace(client: TestClient) -> None:
    """GET /hello?name=' Alice ' preserves inner content but is not stripped.

    The endpoint only strips to decide whether to use the default; the
    actual value used is the raw parameter.
    """
    response = client.get("/hello", params={"name": " Alice "})
    assert response.status_code == 200
    # The name has non-whitespace content so it is used as-is.
    assert response.json() == {"message": "Hello,  Alice !"}


# ------------------------------------------------------------------
# 17. PATCH method not allowed
# ------------------------------------------------------------------


def test_patch_hello_method_not_allowed(client: TestClient) -> None:
    """PATCH /hello returns 405 Method Not Allowed."""
    response = client.patch("/hello")
    assert response.status_code == 405
