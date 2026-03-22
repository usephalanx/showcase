"""Smoke test for the health endpoint."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Health endpoint should return 200 with status ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
