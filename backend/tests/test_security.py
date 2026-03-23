"""Unit tests for the security module.

Focused tests on password hashing and JWT utilities in isolation,
without any HTTP layer.
"""

from __future__ import annotations

from datetime import timedelta

from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_is_deterministic_different() -> None:
    """Two hashes of the same password should differ (random salt)."""
    h1 = hash_password("samepass")
    h2 = hash_password("samepass")
    assert h1 != h2


def test_verify_works_for_both_hashes() -> None:
    """Both hashes should verify against the same plain password."""
    h1 = hash_password("samepass")
    h2 = hash_password("samepass")
    assert verify_password("samepass", h1) is True
    assert verify_password("samepass", h2) is True


def test_token_roundtrip_with_extra_claims() -> None:
    """Extra claims should not break token creation/decoding."""
    token = create_access_token(data={"sub": "carol", "role": "admin"})
    assert decode_access_token(token) == "carol"


def test_expired_token_returns_none() -> None:
    """An already-expired token should not decode."""
    token = create_access_token(
        data={"sub": "dave"},
        expires_delta=timedelta(seconds=-10),
    )
    assert decode_access_token(token) is None
