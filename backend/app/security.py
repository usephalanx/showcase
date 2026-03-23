"""Security utilities: password hashing and JWT token management.

Uses ``passlib`` with bcrypt for password hashing and ``python-jose``
for JWT creation / validation.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash for the given plain-text password.

    Args:
        plain_password: The plain-text password to hash.

    Returns:
        The hashed password string.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash.

    Args:
        plain_password: The plain-text password provided by the user.
        hashed_password: The stored bcrypt hash.

    Returns:
        ``True`` if the password matches, ``False`` otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT token creation / validation
# ---------------------------------------------------------------------------


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: The claims to encode in the token.  Must include ``sub``.
        expires_delta: Optional custom token lifetime.  Falls back to
            the configured ``AUTH_ACCESS_TOKEN_EXPIRE_MINUTES``.

    Returns:
        An encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.AUTH_SECRET_KEY,
        algorithm=settings.AUTH_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token and return the ``sub`` claim.

    Args:
        token: The encoded JWT string.

    Returns:
        The ``sub`` (subject / username) claim, or ``None`` if the token
        is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )
        username: Optional[str] = payload.get("sub")
        return username
    except JWTError:
        return None
