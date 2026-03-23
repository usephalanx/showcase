"""Tests to validate Docker configuration files exist and contain expected content."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pytest

# Root of the repository
ROOT_DIR = Path(__file__).resolve().parent.parent


class TestBackendDockerfile:
    """Tests for backend/Dockerfile."""

    @pytest.fixture()
    def dockerfile_content(self) -> str:
        """Read backend Dockerfile content."""
        path = ROOT_DIR / "backend" / "Dockerfile"
        assert path.exists(), "backend/Dockerfile does not exist"
        return path.read_text(encoding="utf-8")

    def test_uses_python_311_slim(self, dockerfile_content: str) -> None:
        """Verify the Dockerfile uses python:3.11-slim as base."""
        assert "python:3.11-slim" in dockerfile_content

    def test_installs_requirements(self, dockerfile_content: str) -> None:
        """Verify requirements.txt is copied and installed."""
        assert "requirements.txt" in dockerfile_content
        assert "pip install" in dockerfile_content

    def test_exposes_port_8000(self, dockerfile_content: str) -> None:
        """Verify port 8000 is exposed."""
        assert "EXPOSE 8000" in dockerfile_content

    def test_runs_uvicorn(self, dockerfile_content: str) -> None:
        """Verify uvicorn is used to run the app."""
        assert "uvicorn" in dockerfile_content
        assert "app.main:app" in dockerfile_content


class TestFrontendDockerfile:
    """Tests for frontend/Dockerfile."""

    @pytest.fixture()
    def dockerfile_content(self) -> str:
        """Read frontend Dockerfile content."""
        path = ROOT_DIR / "frontend" / "Dockerfile"
        assert path.exists(), "frontend/Dockerfile does not exist"
        return path.read_text(encoding="utf-8")

    def test_uses_node_18_for_build(self, dockerfile_content: str) -> None:
        """Verify the build stage uses Node 18."""
        assert "node:18" in dockerfile_content

    def test_uses_nginx_for_serve(self, dockerfile_content: str) -> None:
        """Verify the serve stage uses nginx."""
        assert "nginx" in dockerfile_content.lower()

    def test_multi_stage_build(self, dockerfile_content: str) -> None:
        """Verify multi-stage build is used."""
        from_count = dockerfile_content.lower().count("from ")
        assert from_count >= 2, "Expected at least 2 FROM statements for multi-stage build"

    def test_exposes_port_80(self, dockerfile_content: str) -> None:
        """Verify port 80 is exposed."""
        assert "EXPOSE 80" in dockerfile_content

    def test_copies_built_assets(self, dockerfile_content: str) -> None:
        """Verify built assets are copied from build stage."""
        assert "--from=build" in dockerfile_content


class TestDockerCompose:
    """Tests for docker-compose.yml."""

    @pytest.fixture()
    def compose_content(self) -> str:
        """Read docker-compose.yml content."""
        path = ROOT_DIR / "docker-compose.yml"
        assert path.exists(), "docker-compose.yml does not exist"
        return path.read_text(encoding="utf-8")

    def test_has_backend_service(self, compose_content: str) -> None:
        """Verify backend service is defined."""
        assert "backend:" in compose_content

    def test_has_frontend_service(self, compose_content: str) -> None:
        """Verify frontend service is defined."""
        assert "frontend:" in compose_content

    def test_backend_port_8000(self, compose_content: str) -> None:
        """Verify backend is mapped to port 8000."""
        assert "8000:8000" in compose_content

    def test_frontend_port_mapping(self, compose_content: str) -> None:
        """Verify frontend port mapping exists."""
        assert "3000:80" in compose_content

    def test_network_defined(self, compose_content: str) -> None:
        """Verify a shared network is defined."""
        assert "networks:" in compose_content

    def test_depends_on(self, compose_content: str) -> None:
        """Verify frontend depends on backend."""
        assert "depends_on:" in compose_content

    def test_environment_variables(self, compose_content: str) -> None:
        """Verify environment variables reference is present."""
        assert "SECRET_KEY" in compose_content
        assert "DATABASE_URL" in compose_content


class TestNginxConf:
    """Tests for frontend/nginx.conf."""

    @pytest.fixture()
    def nginx_content(self) -> str:
        """Read nginx.conf content."""
        path = ROOT_DIR / "frontend" / "nginx.conf"
        assert path.exists(), "frontend/nginx.conf does not exist"
        return path.read_text(encoding="utf-8")

    def test_proxies_auth_to_backend(self, nginx_content: str) -> None:
        """Verify /auth/ is proxied to the backend."""
        assert "location /auth/" in nginx_content
        assert "proxy_pass http://backend:8000" in nginx_content

    def test_proxies_boards_to_backend(self, nginx_content: str) -> None:
        """Verify /boards/ is proxied to the backend."""
        assert "location /boards/" in nginx_content

    def test_proxies_cards_to_backend(self, nginx_content: str) -> None:
        """Verify /cards/ is proxied to the backend."""
        assert "location /cards/" in nginx_content

    def test_spa_fallback(self, nginx_content: str) -> None:
        """Verify SPA fallback to index.html."""
        assert "try_files" in nginx_content
        assert "index.html" in nginx_content

    def test_listens_on_port_80(self, nginx_content: str) -> None:
        """Verify nginx listens on port 80."""
        assert "listen 80" in nginx_content


class TestDockerignoreFiles:
    """Tests for .dockerignore files."""

    def test_backend_dockerignore_exists(self) -> None:
        """Verify backend .dockerignore exists."""
        path = ROOT_DIR / "backend" / ".dockerignore"
        assert path.exists(), "backend/.dockerignore does not exist"

    def test_backend_dockerignore_excludes_pycache(self) -> None:
        """Verify backend .dockerignore excludes __pycache__."""
        path = ROOT_DIR / "backend" / ".dockerignore"
        content = path.read_text(encoding="utf-8")
        assert "__pycache__" in content

    def test_backend_dockerignore_excludes_venv(self) -> None:
        """Verify backend .dockerignore excludes virtual environments."""
        path = ROOT_DIR / "backend" / ".dockerignore"
        content = path.read_text(encoding="utf-8")
        assert ".venv" in content or "venv" in content

    def test_frontend_dockerignore_exists(self) -> None:
        """Verify frontend .dockerignore exists."""
        path = ROOT_DIR / "frontend" / ".dockerignore"
        assert path.exists(), "frontend/.dockerignore does not exist"

    def test_frontend_dockerignore_excludes_node_modules(self) -> None:
        """Verify frontend .dockerignore excludes node_modules."""
        path = ROOT_DIR / "frontend" / ".dockerignore"
        content = path.read_text(encoding="utf-8")
        assert "node_modules" in content


class TestEnvExample:
    """Tests for .env.example."""

    @pytest.fixture()
    def env_content(self) -> str:
        """Read .env.example content."""
        path = ROOT_DIR / ".env.example"
        assert path.exists(), ".env.example does not exist"
        return path.read_text(encoding="utf-8")

    def test_has_jwt_secret(self, env_content: str) -> None:
        """Verify JWT_SECRET is documented."""
        assert "JWT_SECRET" in env_content

    def test_has_database_url(self, env_content: str) -> None:
        """Verify DATABASE_URL is documented."""
        assert "DATABASE_URL" in env_content

    def test_no_real_secrets(self, env_content: str) -> None:
        """Verify no real secrets are hardcoded in the example file."""
        # The example file should contain placeholder values, not real secrets
        assert "change-me" in env_content.lower() or "change" in env_content.lower()


class TestRunningMd:
    """Tests for RUNNING.md."""

    @pytest.fixture()
    def running_content(self) -> str:
        """Read RUNNING.md content."""
        path = ROOT_DIR / "RUNNING.md"
        assert path.exists(), "RUNNING.md does not exist"
        return path.read_text(encoding="utf-8")

    def test_has_clone_command(self, running_content: str) -> None:
        """Verify git clone instructions exist."""
        assert "git clone" in running_content

    def test_has_docker_compose_up(self, running_content: str) -> None:
        """Verify docker compose up command exists."""
        assert "docker compose up --build" in running_content

    def test_has_access_urls(self, running_content: str) -> None:
        """Verify access URLs are documented."""
        assert "localhost:3000" in running_content
        assert "localhost:8000" in running_content

    def test_has_demo_credentials(self, running_content: str) -> None:
        """Verify demo credentials are documented."""
        assert "demo@phalanx.dev" in running_content
        assert "demo1234" in running_content

    def test_has_stop_instructions(self, running_content: str) -> None:
        """Verify stop instructions exist."""
        assert "docker compose down" in running_content

    def test_has_reset_instructions(self, running_content: str) -> None:
        """Verify reset instructions exist."""
        assert "docker compose down -v" in running_content
