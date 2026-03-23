"""Shared FastAPI dependencies.

Re-exports the database session dependency for convenience and provides
the ``get_current_user`` dependency for protecting routes with JWT
authentication.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency that extracts and validates the current user from a JWT.

    Reads the ``Authorization: Bearer <token>`` header, decodes the JWT,
    and looks up the corresponding user in the database.

    Args:
        token: The JWT access token extracted from the request header.
        db: The database session provided by the ``get_db`` dependency.

    Returns:
        The authenticated :class:`~app.models.user.User` instance.

    Raises:
        HTTPException: 401 if the token is invalid, expired, or the
            user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


__all__ = ["get_db", "get_current_user", "oauth2_scheme"]
