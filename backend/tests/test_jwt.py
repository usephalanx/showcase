"""Tests for JWT utility functions."""

from __future__ import annotations

from datetime import timedelta

import pytest
from fastapi import HTTPException

from app.auth import create_access_token, decode_token


def test_create_and_decode_token() -> None:
    """A token should be decodable and contain the original claims."""
    token = create_access_token({"sub": "42"})
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert "exp" in payload


def test_expired_token() -> None:
    """An expired token should raise HTTPException with 401."""
    token = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(HTTPException) as exc_info:
        decode_token(token)
    assert exc_info.value.status_code == 401


def test_invalid_token() -> None:
    """A garbage token should raise HTTPException with 401."""
    with pytest.raises(HTTPException) as exc_info:
        decode_token("not.a.valid.token")
    assert exc_info.value.status_code == 401
