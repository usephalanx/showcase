"""API router for authentication endpoints.

Provides user registration and login (JWT token issuance) endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user.

    Creates a new user with a bcrypt-hashed password.  Returns 409 if
    the username is already taken.

    Args:
        payload: The registration request body.
        db: The database session.

    Returns:
        The newly created user.
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


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> dict:
    """Authenticate a user and return a JWT access token.

    Validates the username and password, then issues a signed JWT.
    Returns 401 if credentials are invalid.

    Args:
        payload: The login request body.
        db: The database session.

    Returns:
        A dictionary containing the access token and token type.
    """
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
