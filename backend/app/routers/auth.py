"""Authentication router: user registration and login.

Mounts under ``/auth`` and exposes:
- POST /auth/register – create a new user account
- POST /auth/login    – obtain a JWT access token
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Create a new user account.

    Raises 409 Conflict if the username is already taken.
    """
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Obtain an access token",
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate with username/password and receive a JWT access token.

    Raises 401 Unauthorized if the credentials are invalid.
    """
    user: User | None = (
        db.query(User).filter(User.username == payload.username).first()
    )
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token)
