"""FastAPI application for the Kanban board backend.

Exposes authentication endpoints (register/login) with JWT tokens and
bcrypt password hashing.  Includes CORS middleware for the frontend
dev server at localhost:5173.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any, AsyncIterator, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
import bcrypt as _bcrypt
from pydantic import BaseModel, EmailStr, Field

import database

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SECRET_KEY: str = os.environ.get("KANBAN_SECRET_KEY", "super-secret-dev-key-change-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS: int = 24

# ---------------------------------------------------------------------------
# Security utilities
# ---------------------------------------------------------------------------


security_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password.

    Returns:
        The bcrypt hash string.
    """
    return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash.

    Args:
        plain_password: The plain-text password to check.
        hashed_password: The stored bcrypt hash.

    Returns:
        True if the password matches, False otherwise.
    """
    return _bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Args:
        data: The payload data to encode (must include 'sub').
        expires_delta: Optional custom expiry duration.

    Returns:
        An encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT access token.

    Args:
        token: The encoded JWT string.

    Returns:
        The decoded payload dictionary.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> Dict[str, Any]:
    """FastAPI dependency that extracts and validates a JWT from the Authorization header.

    Args:
        credentials: The bearer token credentials extracted by HTTPBearer.

    Returns:
        A dictionary of user data for the authenticated user.

    Raises:
        HTTPException: 401 if token is missing, invalid, expired, or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(credentials.credentials)
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = database.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception

    return user


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class RegisterRequest(BaseModel):
    """Request body for user registration."""

    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Unique email address")
    password: str = Field(..., min_length=6, max_length=128, description="Plain-text password")


class LoginRequest(BaseModel):
    """Request body for user login."""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Plain-text password")


class TokenResponse(BaseModel):
    """Response body containing a JWT access token."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user information returned alongside auth responses."""

    id: int
    username: str
    email: str
    created_at: str


class AuthResponse(BaseModel):
    """Response body for authentication endpoints."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialise the database on application startup."""
    database.init_db()
    yield


app = FastAPI(
    title="Kanban Board API",
    description="A Kanban board REST API with JWT authentication.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------


@app.post(
    "/auth/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
async def register(payload: RegisterRequest) -> AuthResponse:
    """Register a new user account.

    Validates that both the username and email are unique, hashes the
    password, stores the user, and returns a JWT access token.
    """
    # Check uniqueness
    if database.get_user_by_username(payload.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if database.get_user_by_email(payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed = hash_password(payload.password)
    try:
        user = database.create_user(payload.username, payload.email, hashed)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    token = create_access_token({"sub": user["id"]})
    return AuthResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            created_at=str(user["created_at"]),
        ),
    )


@app.post(
    "/auth/login",
    response_model=AuthResponse,
    tags=["auth"],
)
async def login(payload: LoginRequest) -> AuthResponse:
    """Authenticate a user and return a JWT access token."""
    user = database.get_user_by_username(payload.username)
    if user is None or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token({"sub": user["id"]})
    return AuthResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            created_at=str(user["created_at"]),
        ),
    )


# ---------------------------------------------------------------------------
# Protected test route (useful for verifying auth works)
# ---------------------------------------------------------------------------


@app.get("/auth/me", response_model=UserResponse, tags=["auth"])
async def get_me(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> UserResponse:
    """Return the currently authenticated user's information."""
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        created_at=str(current_user["created_at"]),
    )


# ---------------------------------------------------------------------------
# Boards
# ---------------------------------------------------------------------------

class BoardCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

class CardCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""

class CardMove(BaseModel):
    column_id: int
    position: int = 0

@app.get("/boards", tags=["boards"])
async def list_boards(current_user: Dict[str, Any] = Depends(get_current_user)):
    boards = database.get_boards_by_user(current_user["id"])
    return boards

@app.post("/boards", tags=["boards"], status_code=201)
async def create_board(payload: BoardCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    board = database.create_board(current_user["id"], payload.title)
    return board

@app.delete("/boards/{board_id}", tags=["boards"])
async def delete_board(board_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    conn = database.get_db_connection()
    conn.execute("DELETE FROM boards WHERE id = ? AND user_id = ?", (board_id, current_user["id"]))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/boards/{board_id}", tags=["boards"])
async def get_board(board_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    board = database.get_board_by_id(board_id)
    if not board or board["user_id"] != current_user["id"]:
        raise HTTPException(status_code=404, detail="Board not found")
    columns = database.get_columns_by_board(board_id)
    for col in columns:
        col["cards"] = database.get_cards_by_column(col["id"])
    board["columns"] = columns
    return board

# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

@app.post("/columns/{column_id}/cards", tags=["cards"], status_code=201)
async def create_card(column_id: int, payload: CardCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    conn = database.get_db_connection()
    cursor = conn.execute(
        "SELECT COUNT(*) as cnt FROM cards WHERE column_id = ?", (column_id,)
    )
    pos = cursor.fetchone()["cnt"]
    cursor = conn.execute(
        "INSERT INTO cards (column_id, title, description, position) VALUES (?,?,?,?) RETURNING *",
        (column_id, payload.title, payload.description, pos),
    )
    card = dict(cursor.fetchone())
    conn.commit()
    conn.close()
    return card

@app.patch("/cards/{card_id}/move", tags=["cards"])
async def move_card(card_id: int, payload: CardMove, current_user: Dict[str, Any] = Depends(get_current_user)):
    conn = database.get_db_connection()
    conn.execute(
        "UPDATE cards SET column_id = ?, position = ? WHERE id = ?",
        (payload.column_id, payload.position, card_id),
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@app.delete("/cards/{card_id}", tags=["cards"])
async def delete_card(card_id: int, current_user: Dict[str, Any] = Depends(get_current_user)):
    conn = database.get_db_connection()
    conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
