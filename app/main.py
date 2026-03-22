"""Application entry-point — creates the FastAPI app and registers routers."""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers.patients import router as patients_router

# Create tables (for development / SQLite; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dentist Office Management API",
    version="0.1.0",
    description="RESTful API for managing a dental practice.",
)

app.include_router(patients_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}
