"""Tests for backend/main.py — auth endpoints, JWT, password hashing."""

from __future__ import annotations

import os
import sys
import tempfile
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import database
from main import app, create_access_token, decode_access_token, hash_password, verify_password


@pytest.fixture(autouse=True)
def _use_temp_db() -> Generator[None, None, None]:
    """Redirect the database to a temporary file for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    database.DATABASE_PATH = path
    database.init_db()
    yield
    os.unlink(path)


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI TestClient."""
    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Password hashing tests
# ---------------------------------------------------------------------------


def test_hash_and_verify_password() -> None:
    """hash_password + verify_password should round-trip correctly."""
    hashed = hash_password("mysecretpassword")
    assert hashed != "mysecretpassword"
    assert verify_password("mysecretpassword", hashed) is True
    assert verify_password("wrongpassword", hashed) is False


# ---------------------------------------------------------------------------
# JWT tests
# ---------------------------------------------------------------------------


def test_create_and_decode_token() -> None:
    """create_access_token and decode_access_token should round-trip."""
    token = create_access_token({"sub": 42})
    payload = decode_access_token(token)
    assert payload["sub"] == 42
    assert "exp" in payload


def test_decode_invalid_token() -> None:
    """decode_access_token should raise on an invalid token."""
    from jose import JWTError

    with pytest.raises(JWTError):
        decode_access_token("invalid.token.string")


# ---------------------------------------------------------------------------
# POST /auth/register tests
# ---------------------------------------------------------------------------


def test_register_success(client: TestClient) -> None:
    """Registration with valid data should return 201 and a JWT."""
    resp = client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["user"]["username"] == "alice"
    assert body["user"]["email"] == "alice@example.com"
    assert "id" in body["user"]


def test_register_duplicate_username(client: TestClient) -> None:
    """Registering with an existing username should return 400."""
    client.post(
        "/auth/register",
        json={"username": "bob", "email": "bob@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/register",
        json={"username": "bob", "email": "bob2@example.com", "password": "secret456"},
    )
    assert resp.status_code == 400
    assert "Username already registered" in resp.json()["detail"]


def test_register_duplicate_email(client: TestClient) -> None:
    """Registering with an existing email should return 400."""
    client.post(
        "/auth/register",
        json={"username": "carol", "email": "carol@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/register",
        json={"username": "carol2", "email": "carol@example.com", "password": "secret456"},
    )
    assert resp.status_code == 400
    assert "Email already registered" in resp.json()["detail"]


def test_register_short_username(client: TestClient) -> None:
    """Registration with a too-short username should return 422."""
    resp = client.post(
        "/auth/register",
        json={"username": "ab", "email": "ab@example.com", "password": "secret123"},
    )
    assert resp.status_code == 422


def test_register_short_password(client: TestClient) -> None:
    """Registration with a too-short password should return 422."""
    resp = client.post(
        "/auth/register",
        json={"username": "dave", "email": "dave@example.com", "password": "short"},
    )
    assert resp.status_code == 422


def test_register_invalid_email(client: TestClient) -> None:
    """Registration with an invalid email should return 422."""
    resp = client.post(
        "/auth/register",
        json={"username": "emma", "email": "not-an-email", "password": "secret123"},
    )
    assert resp.status_code == 422


def test_register_missing_fields(client: TestClient) -> None:
    """Registration with missing fields should return 422."""
    resp = client.post("/auth/register", json={"username": "frank"})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /auth/login tests
# ---------------------------------------------------------------------------


def test_login_success(client: TestClient) -> None:
    """Login with valid credentials should return 200 and a JWT."""
    client.post(
        "/auth/register",
        json={"username": "grace", "email": "grace@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/login",
        json={"username": "grace", "password": "secret123"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["user"]["username"] == "grace"


def test_login_wrong_password(client: TestClient) -> None:
    """Login with a wrong password should return 401."""
    client.post(
        "/auth/register",
        json={"username": "hank", "email": "hank@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/login",
        json={"username": "hank", "password": "wrongpassword"},
    )
    assert resp.status_code == 401
    assert "Invalid" in resp.json()["detail"]


def test_login_nonexistent_user(client: TestClient) -> None:
    """Login with a username that doesn't exist should return 401."""
    resp = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "secret123"},
    )
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# GET /auth/me (protected endpoint) tests
# ---------------------------------------------------------------------------


def test_me_with_valid_token(client: TestClient) -> None:
    """GET /auth/me with a valid token should return user info."""
    reg_resp = client.post(
        "/auth/register",
        json={"username": "ivan", "email": "ivan@example.com", "password": "secret123"},
    )
    token = reg_resp.json()["access_token"]
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "ivan"


def test_me_without_token(client: TestClient) -> None:
    """GET /auth/me without a token should return 403 (HTTPBearer returns 403 by default)."""
    resp = client.get("/auth/me")
    assert resp.status_code == 403


def test_me_with_invalid_token(client: TestClient) -> None:
    """GET /auth/me with an invalid token should return 401."""
    resp = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert resp.status_code == 401


def test_me_with_expired_token(client: TestClient) -> None:
    """GET /auth/me with an expired token should return 401."""
    from datetime import timedelta

    token = create_access_token({"sub": 999}, expires_delta=timedelta(seconds=-1))
    resp = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401


def test_me_with_token_for_deleted_user(client: TestClient) -> None:
    """GET /auth/me with a token referencing a non-existent user should return 401."""
    token = create_access_token({"sub": 999999})
    resp = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# CORS tests
# ---------------------------------------------------------------------------


def test_cors_allowed_origin(client: TestClient) -> None:
    """Preflight from localhost:5173 should be allowed."""
    resp = client.options(
        "/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert resp.status_code == 200
    assert "http://localhost:5173" in resp.headers.get("access-control-allow-origin", "")


def test_cors_disallowed_origin(client: TestClient) -> None:
    """Preflight from a disallowed origin should not echo the origin."""
    resp = client.options(
        "/auth/login",
        headers={
            "Origin": "http://evil.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    # FastAPI CORS will not set the allow-origin header for disallowed origins
    allow_origin = resp.headers.get("access-control-allow-origin", "")
    assert "evil.com" not in allow_origin


# ---------------------------------------------------------------------------
# Token returned on register is usable
# ---------------------------------------------------------------------------


def test_register_token_is_usable(client: TestClient) -> None:
    """The JWT returned from registration should work to access /auth/me."""
    reg_resp = client.post(
        "/auth/register",
        json={"username": "judy", "email": "judy@example.com", "password": "secret123"},
    )
    token = reg_resp.json()["access_token"]
    me_resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "judy"


def test_login_token_is_usable(client: TestClient) -> None:
    """The JWT returned from login should work to access /auth/me."""
    client.post(
        "/auth/register",
        json={"username": "kim", "email": "kim@example.com", "password": "secret123"},
    )
    login_resp = client.post(
        "/auth/login",
        json={"username": "kim", "password": "secret123"},
    )
    token = login_resp.json()["access_token"]
    me_resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "kim"
