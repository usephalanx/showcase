"""Integration tests for the Task Manager API.

Uses an in-memory SQLite database so that the production ``tasks.db``
file is never touched.  The database dependency is overridden per-test
via FastAPI's dependency injection system.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.database import Base, get_db
from backend.main import app

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db() -> Session:  # type: ignore[misc]
    """Yield a test database session."""
    db = TestingSessionLocal()
    try:
        yield db  # type: ignore[misc]
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def _setup_database() -> None:
    """Create all tables before each test and drop them after."""
    import backend.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield  # type: ignore[misc]
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> TestClient:
    """Return a FastAPI TestClient."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------


class TestCreateTask:
    """Tests for the POST /tasks endpoint."""

    def test_create_task_with_title_only(self, client: TestClient) -> None:
        """Creating a task with only a title should succeed."""
        response = client.post("/tasks", json={"title": "Write tests"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Write tests"
        assert data["description"] == ""
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data

    def test_create_task_with_description(self, client: TestClient) -> None:
        """Creating a task with title and description should succeed."""
        response = client.post(
            "/tasks",
            json={"title": "Deploy app", "description": "To production"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Deploy app"
        assert data["description"] == "To production"
        assert data["status"] == "pending"

    def test_create_task_empty_title_rejected(self, client: TestClient) -> None:
        """An empty title should be rejected with 422."""
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_missing_title_rejected(self, client: TestClient) -> None:
        """A missing title should be rejected with 422."""
        response = client.post("/tasks", json={})
        assert response.status_code == 422

    def test_create_task_always_pending(self, client: TestClient) -> None:
        """Even if a status is sent, the created task should be 'pending'."""
        response = client.post(
            "/tasks", json={"title": "Sneaky", "status": "done"}
        )
        assert response.status_code == 201
        assert response.json()["status"] == "pending"


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------


class TestListTasks:
    """Tests for the GET /tasks endpoint."""

    def test_list_empty(self, client: TestClient) -> None:
        """An empty database should return an empty list."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_returns_created_tasks(self, client: TestClient) -> None:
        """Created tasks should appear in the listing."""
        client.post("/tasks", json={"title": "Task A"})
        client.post("/tasks", json={"title": "Task B"})

        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_ordered_by_created_at_desc(self, client: TestClient) -> None:
        """Tasks should be returned newest-first."""
        client.post("/tasks", json={"title": "First"})
        client.post("/tasks", json={"title": "Second"})

        response = client.get("/tasks")
        data = response.json()
        # The second task (created later) should come first
        assert data[0]["title"] == "Second"
        assert data[1]["title"] == "First"


# ---------------------------------------------------------------------------
# PATCH /tasks/{id}
# ---------------------------------------------------------------------------


class TestUpdateTaskStatus:
    """Tests for the PATCH /tasks/{id} endpoint."""

    def test_update_status_to_done(self, client: TestClient) -> None:
        """Marking a task as 'done' should succeed."""
        create_resp = client.post("/tasks", json={"title": "Finish project"})
        task_id = create_resp.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
        assert response.status_code == 200
        assert response.json()["status"] == "done"

    def test_update_status_back_to_pending(self, client: TestClient) -> None:
        """A task can be moved back to 'pending'."""
        create_resp = client.post("/tasks", json={"title": "Reopen me"})
        task_id = create_resp.json()["id"]

        client.patch(f"/tasks/{task_id}", json={"status": "done"})
        response = client.patch(f"/tasks/{task_id}", json={"status": "pending"})
        assert response.status_code == 200
        assert response.json()["status"] == "pending"

    def test_update_nonexistent_task_returns_404(self, client: TestClient) -> None:
        """Updating a task that doesn't exist should return 404."""
        response = client.patch("/tasks/9999", json={"status": "done"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_update_invalid_status_rejected(self, client: TestClient) -> None:
        """An invalid status value should be rejected with 422."""
        create_resp = client.post("/tasks", json={"title": "Validate me"})
        task_id = create_resp.json()["id"]

        response = client.patch(
            f"/tasks/{task_id}", json={"status": "invalid_status"}
        )
        assert response.status_code == 422

    def test_update_missing_status_rejected(self, client: TestClient) -> None:
        """A missing status field should be rejected with 422."""
        create_resp = client.post("/tasks", json={"title": "No status"})
        task_id = create_resp.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------


class TestCORS:
    """Tests to verify CORS middleware is configured."""

    def test_cors_headers_present(self, client: TestClient) -> None:
        """Preflight request should return CORS headers."""
        response = client.options(
            "/tasks",
            headers={
                "Origin": "http://localhost:5500",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_any_origin(self, client: TestClient) -> None:
        """Any origin should be accepted by the CORS policy."""
        response = client.options(
            "/tasks",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers.get("access-control-allow-origin") == "*"
