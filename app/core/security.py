"""Security utilities for password hashing and JWT token management.

Provides functions for hashing and verifying passwords with bcrypt via
passlib, and for creating and decoding JWT access tokens using
python-jose.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash of the given plain-text password.

    Args:
        plain_password: The plain-text password to hash.

    Returns:
        The hashed password string.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: The plain-text password to check.
        hashed_password: The stored bcrypt hash.

    Returns:
        ``True`` if the password matches the hash, ``False`` otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload data to encode into the token.  Must include a
            ``sub`` key with the username.
        expires_delta: Optional custom expiration timedelta.  Defaults
            to :data:`ACCESS_TOKEN_EXPIRE_MINUTES` from config.

    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT access token.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded payload dictionary, or ``None`` if the token is
        invalid or expired.
    """
    try:
        payload: dict[str, Any] = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
