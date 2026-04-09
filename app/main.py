"""FastAPI application entry point.

Defines the Hello World API with a health-check endpoint and a
hello-world greeting endpoint.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic response models
# ---------------------------------------------------------------------------


class HelloResponse(BaseModel):
    """Response body for the /hello endpoint."""

    message: str = Field(..., description="Greeting message")


class HealthResponse(BaseModel):
    """Response body for the / health-check endpoint."""

    status: str = Field(..., description="Service health status")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Hello World API",
    description="A minimal API that returns a hello-world greeting.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    """Return the service health status."""
    return HealthResponse(status="ok")


@app.get("/hello", response_model=HelloResponse, tags=["greeting"])
async def get_hello() -> HelloResponse:
    """Return a hello-world greeting message."""
    return HelloResponse(message="hello-world")
