"""Tests for the JWT authentication system.

Covers user registration, login, token validation, protected routes,
password hashing, and edge cases.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User


# ---------------------------------------------------------------------------
# Password hashing unit tests
# ---------------------------------------------------------------------------


class TestPasswordHashing:
    """Tests for password hashing and verification utilities."""

    def test_hash_password_returns_bcrypt_string(self) -> None:
        """hash_password should return a bcrypt hash starting with $2b$."""
        hashed = hash_password("mysecret")
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self) -> None:
        """verify_password should return True for a matching password."""
        hashed = hash_password("mysecret")
        assert verify_password("mysecret", hashed) is True

    def test_verify_password_incorrect(self) -> None:
        """verify_password should return False for a wrong password."""
        hashed = hash_password("mysecret")
        assert verify_password("wrongpassword", hashed) is False

    def test_hash_password_produces_unique_hashes(self) -> None:
        """Two calls to hash_password with the same input should differ (salt)."""
        h1 = hash_password("samepassword")
        h2 = hash_password("samepassword")
        assert h1 != h2


# ---------------------------------------------------------------------------
# JWT token unit tests
# ---------------------------------------------------------------------------


class TestJWTTokens:
    """Tests for JWT token creation and decoding."""

    def test_create_and_decode_access_token(self) -> None:
        """A freshly created token should decode successfully."""
        token = create_access_token(data={"sub": "testuser"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert "exp" in payload

    def test_create_access_token_with_custom_expiry(self) -> None:
        """Token created with custom expiry should decode successfully."""
        token = create_access_token(
            data={"sub": "testuser"}, expires_delta=timedelta(hours=1)
        )
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"

    def test_decode_invalid_token_returns_none(self) -> None:
        """Decoding a garbage string should return None."""
        result = decode_access_token("not.a.valid.token")
        assert result is None

    def test_decode_expired_token_returns_none(self) -> None:
        """An expired token should return None on decode."""
        token = create_access_token(
            data={"sub": "testuser"}, expires_delta=timedelta(seconds=-1)
        )
        result = decode_access_token(token)
        assert result is None


# ---------------------------------------------------------------------------
# Registration endpoint tests
# ---------------------------------------------------------------------------


class TestRegisterEndpoint:
    """Tests for POST /auth/register."""

    def test_register_success(self, client: TestClient) -> None:
        """Successful registration should return 201 with user data."""
        response = client.post(
            "/auth/register",
            json={"username": "newuser", "password": "secret123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "created_at" in data
        # Password should not be in response
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client: TestClient) -> None:
        """Registering with an existing username should return 409."""
        client.post(
            "/auth/register",
            json={"username": "duplicate", "password": "secret123"},
        )
        response = client.post(
            "/auth/register",
            json={"username": "duplicate", "password": "other456"},
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    def test_register_short_username(self, client: TestClient) -> None:
        """Username shorter than 3 chars should be rejected (422)."""
        response = client.post(
            "/auth/register",
            json={"username": "ab", "password": "secret123"},
        )
        assert response.status_code == 422

    def test_register_short_password(self, client: TestClient) -> None:
        """Password shorter than 6 chars should be rejected (422)."""
        response = client.post(
            "/auth/register",
            json={"username": "validuser", "password": "short"},
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, client: TestClient) -> None:
        """Missing required fields should return 422."""
        response = client.post("/auth/register", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Login endpoint tests
# ---------------------------------------------------------------------------


class TestLoginEndpoint:
    """Tests for POST /auth/login."""

    def test_login_success(self, client: TestClient) -> None:
        """Successful login should return 200 with access_token."""
        # Register first
        client.post(
            "/auth/register",
            json={"username": "loginuser", "password": "secret123"},
        )
        response = client.post(
            "/auth/login",
            json={"username": "loginuser", "password": "secret123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        # Verify the token is valid
        payload = decode_access_token(data["access_token"])
        assert payload is not None
        assert payload["sub"] == "loginuser"

    def test_login_wrong_password(self, client: TestClient) -> None:
        """Wrong password should return 401."""
        client.post(
            "/auth/register",
            json={"username": "loginuser2", "password": "secret123"},
        )
        response = client.post(
            "/auth/login",
            json={"username": "loginuser2", "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        """Login with a non-existent username should return 401."""
        response = client.post(
            "/auth/login",
            json={"username": "noexist", "password": "secret123"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Protected route / get_current_user dependency tests
# ---------------------------------------------------------------------------


class TestGetCurrentUser:
    """Tests for the get_current_user dependency (token validation)."""

    def _get_token(self, client: TestClient, username: str = "authuser") -> str:
        """Helper to register a user and get an access token."""
        client.post(
            "/auth/register",
            json={"username": username, "password": "secret123"},
        )
        resp = client.post(
            "/auth/login",
            json={"username": username, "password": "secret123"},
        )
        return resp.json()["access_token"]

    def test_access_protected_route_with_valid_token(
        self, client: TestClient
    ) -> None:
        """A request with a valid token should succeed on protected endpoints."""
        token = self._get_token(client)
        # Use the /auth/me endpoint (we'll add it) to test
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "authuser"

    def test_access_protected_route_without_token(
        self, client: TestClient
    ) -> None:
        """A request without a token should return 401."""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_access_protected_route_with_invalid_token(
        self, client: TestClient
    ) -> None:
        """A request with an invalid token should return 401."""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 401

    def test_access_protected_route_with_expired_token(
        self, client: TestClient, db_session: Session
    ) -> None:
        """A request with an expired token should return 401."""
        # Create user directly
        user = User(
            username="expireduser",
            hashed_password=hash_password("secret123"),
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token(
            data={"sub": "expireduser"}, expires_delta=timedelta(seconds=-1)
        )
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    def test_token_for_deleted_user(
        self, client: TestClient, db_session: Session
    ) -> None:
        """A valid token for a non-existent user should return 401."""
        token = create_access_token(data={"sub": "ghostuser"})
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    def test_token_without_sub_claim(self, client: TestClient) -> None:
        """A token without a 'sub' claim should return 401."""
        token = create_access_token(data={"role": "admin"})
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# User model tests
# ---------------------------------------------------------------------------


class TestUserModel:
    """Tests for the User SQLAlchemy model."""

    def test_user_creation(self, db_session: Session) -> None:
        """A user should be persistable and retrievable."""
        user = User(
            username="modeluser",
            hashed_password=hash_password("test123"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.username == "modeluser"
        assert user.created_at is not None

    def test_user_repr(self, db_session: Session) -> None:
        """User __repr__ should contain id and username."""
        user = User(
            username="repruser",
            hashed_password=hash_password("test123"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        repr_str = repr(user)
        assert "repruser" in repr_str
        assert str(user.id) in repr_str

    def test_username_uniqueness(self, db_session: Session) -> None:
        """Duplicate usernames should raise an integrity error."""
        from sqlalchemy.exc import IntegrityError

        user1 = User(
            username="uniqueuser",
            hashed_password=hash_password("test123"),
        )
        db_session.add(user1)
        db_session.commit()

        user2 = User(
            username="uniqueuser",
            hashed_password=hash_password("test456"),
        )
        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()


# ---------------------------------------------------------------------------
# CORS middleware test
# ---------------------------------------------------------------------------


class TestCORSMiddleware:
    """Tests for CORS middleware configuration."""

    def test_cors_preflight_allowed_origin(self, client: TestClient) -> None:
        """OPTIONS request from an allowed origin should include CORS headers."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert (
            response.headers.get("access-control-allow-origin")
            == "http://localhost:5173"
        )

    def test_cors_simple_request_allowed_origin(self, client: TestClient) -> None:
        """GET request from an allowed origin should include CORS headers."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:5173"},
        )
        assert response.status_code == 200
        assert (
            response.headers.get("access-control-allow-origin")
            == "http://localhost:5173"
        )


# ---------------------------------------------------------------------------
# Seed default user tests
# ---------------------------------------------------------------------------


class TestSeedDefaultUser:
    """Tests for the seed_default_user function."""

    def test_seed_creates_admin_user(self, db_session: Session) -> None:
        """seed_default_user should create an admin user if not present."""
        from app.core.database import seed_default_user

        seed_default_user()

        # Query using a fresh session from the same engine
        from tests.conftest import TestSessionLocal

        check_session = TestSessionLocal()
        try:
            admin = (
                check_session.query(User)
                .filter(User.username == "admin")
                .first()
            )
            assert admin is not None
            assert admin.username == "admin"
            assert verify_password("admin123", admin.hashed_password) is True
        finally:
            check_session.close()

    def test_seed_is_idempotent(self, db_session: Session) -> None:
        """Calling seed_default_user twice should not create duplicates."""
        from app.core.database import seed_default_user

        seed_default_user()
        seed_default_user()

        from tests.conftest import TestSessionLocal

        check_session = TestSessionLocal()
        try:
            admins = (
                check_session.query(User)
                .filter(User.username == "admin")
                .all()
            )
            assert len(admins) == 1
        finally:
            check_session.close()
