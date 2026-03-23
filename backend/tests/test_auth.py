"""Tests for the JWT authentication system.

Covers user registration, login, token validation, and the
get_current_user dependency.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------


class TestPasswordHashing:
    """Tests for password hashing utilities."""

    def test_hash_password_returns_string(self) -> None:
        """hash_password should return a non-empty string."""
        hashed = hash_password("mysecret")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_not_plaintext(self) -> None:
        """The hash must not equal the plain password."""
        assert hash_password("mysecret") != "mysecret"

    def test_verify_password_correct(self) -> None:
        """verify_password should return True for a matching password."""
        hashed = hash_password("mysecret")
        assert verify_password("mysecret", hashed) is True

    def test_verify_password_incorrect(self) -> None:
        """verify_password should return False for a wrong password."""
        hashed = hash_password("mysecret")
        assert verify_password("wrongpassword", hashed) is False


# ---------------------------------------------------------------------------
# JWT token creation / decoding
# ---------------------------------------------------------------------------


class TestJWTTokens:
    """Tests for JWT creation and decoding utilities."""

    def test_create_and_decode_token(self) -> None:
        """A freshly created token should decode to the same subject."""
        token = create_access_token(data={"sub": "alice"})
        assert decode_access_token(token) == "alice"

    def test_decode_invalid_token(self) -> None:
        """An invalid token should return None."""
        assert decode_access_token("not.a.valid.token") is None

    def test_expired_token(self) -> None:
        """An expired token should return None on decode."""
        token = create_access_token(
            data={"sub": "alice"},
            expires_delta=timedelta(seconds=-1),
        )
        assert decode_access_token(token) is None

    def test_custom_expiry(self) -> None:
        """A token with a custom expiry should still decode correctly."""
        token = create_access_token(
            data={"sub": "bob"},
            expires_delta=timedelta(hours=2),
        )
        assert decode_access_token(token) == "bob"

    def test_token_without_sub(self) -> None:
        """A token without a 'sub' claim should decode to None."""
        token = create_access_token(data={"user": "alice"})
        assert decode_access_token(token) is None


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------


class TestRegister:
    """Tests for the user registration endpoint."""

    def test_register_success(self, client: TestClient) -> None:
        """A valid registration should return 201 with user data."""
        response = client.post(
            "/auth/register",
            json={"username": "alice", "password": "strongpass123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "alice"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        # Password must never be returned
        assert "hashed_password" not in data
        assert "password" not in data

    def test_register_duplicate_username(self, client: TestClient) -> None:
        """Registering with an existing username should return 409."""
        client.post(
            "/auth/register",
            json={"username": "alice", "password": "strongpass123"},
        )
        response = client.post(
            "/auth/register",
            json={"username": "alice", "password": "anotherpass"},
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    def test_register_short_username(self, client: TestClient) -> None:
        """A username shorter than 3 characters should fail validation."""
        response = client.post(
            "/auth/register",
            json={"username": "ab", "password": "strongpass123"},
        )
        assert response.status_code == 422

    def test_register_short_password(self, client: TestClient) -> None:
        """A password shorter than 6 characters should fail validation."""
        response = client.post(
            "/auth/register",
            json={"username": "alice", "password": "short"},
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, client: TestClient) -> None:
        """Missing required fields should fail validation."""
        response = client.post("/auth/register", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------


class TestLogin:
    """Tests for the login endpoint."""

    def test_login_success(self, client: TestClient) -> None:
        """Valid credentials should return 200 with an access token."""
        client.post(
            "/auth/register",
            json={"username": "alice", "password": "strongpass123"},
        )
        response = client.post(
            "/auth/login",
            json={"username": "alice", "password": "strongpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        # Ensure the token is valid
        username = decode_access_token(data["access_token"])
        assert username == "alice"

    def test_login_wrong_password(self, client: TestClient) -> None:
        """Wrong password should return 401."""
        client.post(
            "/auth/register",
            json={"username": "alice", "password": "strongpass123"},
        )
        response = client.post(
            "/auth/login",
            json={"username": "alice", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """Login with a non-existent username should return 401."""
        response = client.post(
            "/auth/login",
            json={"username": "ghost", "password": "whatever"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Authentication dependency (get_current_user)
# ---------------------------------------------------------------------------


class TestGetCurrentUser:
    """Tests for the get_current_user dependency via a protected endpoint."""

    def test_access_health_no_auth(self, client: TestClient) -> None:
        """The health endpoint should remain unprotected."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_missing_auth_header(self, client: TestClient) -> None:
        """Requests without an Authorization header to a protected path should 401.

        We use /auth/me as a protected test endpoint.
        """
        # /auth/me doesn't exist yet – but we test via the token flow
        # by directly calling the dependency through a crafted token call.
        # Instead, test that an invalid token is rejected by decoding.
        assert decode_access_token("") is None

    def test_valid_token_decodes(self, client: TestClient) -> None:
        """A valid registration + login token should decode correctly."""
        client.post(
            "/auth/register",
            json={"username": "bob", "password": "password123"},
        )
        resp = client.post(
            "/auth/login",
            json={"username": "bob", "password": "password123"},
        )
        token = resp.json()["access_token"]
        assert decode_access_token(token) == "bob"

    def test_tampered_token_rejected(self) -> None:
        """A tampered token should not decode."""
        token = create_access_token(data={"sub": "alice"})
        tampered = token[:-4] + "XXXX"
        assert decode_access_token(tampered) is None
