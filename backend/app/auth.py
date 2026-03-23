"""Authentication dependencies for FastAPI.

Provides ``get_current_user`` which extracts and validates a JWT from
the ``Authorization: Bearer <token>`` header and returns the
corresponding ``User`` ORM instance.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Validate the JWT and return the authenticated user.

    This is intended for use as a FastAPI dependency on any endpoint
    that requires authentication.

    Args:
        token: The bearer token extracted from the Authorization header.
        db: An active database session.

    Returns:
        The ``User`` ORM instance for the authenticated user.

    Raises:
        HTTPException: 401 if the token is invalid/expired or the user
            does not exist or is inactive.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = decode_access_token(token)
    if username is None:
        raise credentials_exception

    user: User | None = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
