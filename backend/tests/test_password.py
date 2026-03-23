"""Tests for password hashing utilities."""

from __future__ import annotations

from app.auth import hash_password, verify_password


def test_hash_and_verify() -> None:
    """Hashed password should verify correctly."""
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"
    assert verify_password("mypassword", hashed)


def test_wrong_password_fails() -> None:
    """Wrong password should not verify."""
    hashed = hash_password("correct")
    assert not verify_password("wrong", hashed)
