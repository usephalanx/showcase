"""Tests for authentication endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_register_success(client: TestClient) -> None:
    """Registration should return 201 with a JWT token."""
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client: TestClient) -> None:
    """Registering the same email twice should return 409."""
    payload = {"email": "dupe@example.com", "password": "secret123"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409


def test_register_short_password(client: TestClient) -> None:
    """Password shorter than 6 chars should be rejected."""
    response = client.post(
        "/auth/register",
        json={"email": "short@example.com", "password": "abc"},
    )
    assert response.status_code == 422


def test_login_success(client: TestClient) -> None:
    """Login with correct credentials should return a JWT."""
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client: TestClient) -> None:
    """Login with wrong password should return 401."""
    client.post(
        "/auth/register",
        json={"email": "wrong@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    """Login with a non-existent email should return 401."""
    response = client.post(
        "/auth/login",
        json={"email": "noone@example.com", "password": "secret123"},
    )
    assert response.status_code == 401
