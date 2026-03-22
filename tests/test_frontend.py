"""Tests validating the frontend static files.

These tests verify that the HTML, CSS, and JS files exist, are well-formed,
and contain the expected structural elements and integration points.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


FRONTEND_DIR: Path = Path(__file__).resolve().parent.parent / "frontend"


class TestFrontendFilesExist:
    """Verify that all required frontend files are present."""

    def test_index_html_exists(self) -> None:
        """index.html should be present in the frontend directory."""
        assert (FRONTEND_DIR / "index.html").is_file()

    def test_style_css_exists(self) -> None:
        """style.css should be present in the frontend directory."""
        assert (FRONTEND_DIR / "style.css").is_file()

    def test_app_js_exists(self) -> None:
        """app.js should be present in the frontend directory."""
        assert (FRONTEND_DIR / "app.js").is_file()


class TestIndexHtmlStructure:
    """Validate critical structural elements in index.html."""

    @pytest.fixture(autouse=True)
    def _load_html(self) -> None:
        """Load index.html content for all tests in this class."""
        self.html: str = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")

    def test_has_doctype(self) -> None:
        """HTML should start with a doctype declaration."""
        assert self.html.strip().lower().startswith("<!doctype html>")

    def test_links_style_css(self) -> None:
        """index.html should reference style.css."""
        assert "style.css" in self.html

    def test_links_app_js(self) -> None:
        """index.html should reference app.js."""
        assert "app.js" in self.html

    def test_has_task_form(self) -> None:
        """index.html should contain a form with id 'task-form'."""
        assert 'id="task-form"' in self.html

    def test_has_title_input(self) -> None:
        """index.html should contain a text input for the task title."""
        assert 'id="task-title"' in self.html

    def test_has_description_textarea(self) -> None:
        """index.html should contain a textarea for the task description."""
        assert 'id="task-description"' in self.html
        assert "<textarea" in self.html

    def test_has_submit_button(self) -> None:
        """index.html should contain a submit button."""
        assert 'id="submit-btn"' in self.html
        assert 'type="submit"' in self.html

    def test_has_task_list_container(self) -> None:
        """index.html should contain a task list element."""
        assert 'id="task-list"' in self.html

    def test_has_error_banner(self) -> None:
        """index.html should contain an error banner element."""
        assert 'id="error-banner"' in self.html

    def test_has_loading_indicator(self) -> None:
        """index.html should contain a loading indicator element."""
        assert 'id="loading-indicator"' in self.html

    def test_has_empty_message(self) -> None:
        """index.html should contain an empty-state message element."""
        assert 'id="empty-message"' in self.html


class TestAppJsIntegration:
    """Validate that app.js contains required integration points."""

    @pytest.fixture(autouse=True)
    def _load_js(self) -> None:
        """Load app.js content for all tests in this class."""
        self.js: str = (FRONTEND_DIR / "app.js").read_text(encoding="utf-8")

    def test_has_configurable_base_url(self) -> None:
        """app.js should reference a configurable base URL."""
        assert "TASK_API_BASE_URL" in self.js

    def test_default_base_url(self) -> None:
        """app.js should default to localhost:8000."""
        assert "http://localhost:8000" in self.js

    def test_uses_fetch_api(self) -> None:
        """app.js should use the fetch API."""
        assert "fetch(" in self.js

    def test_get_tasks_endpoint(self) -> None:
        """app.js should call GET /tasks."""
        assert '"/tasks"' in self.js or "'/tasks'" in self.js

    def test_post_tasks_request(self) -> None:
        """app.js should send POST requests."""
        assert '"POST"' in self.js or "'POST'" in self.js

    def test_patch_tasks_request(self) -> None:
        """app.js should send PATCH requests."""
        assert '"PATCH"' in self.js or "'PATCH'" in self.js

    def test_sends_done_status(self) -> None:
        """app.js should send status 'done' in PATCH requests."""
        assert '"done"' in self.js or "'done'" in self.js

    def test_references_task_form(self) -> None:
        """app.js should reference the task form element."""
        assert "task-form" in self.js

    def test_references_task_list(self) -> None:
        """app.js should reference the task list element."""
        assert "task-list" in self.js

    def test_error_handling_present(self) -> None:
        """app.js should contain error handling logic."""
        assert "showError" in self.js
        assert "catch" in self.js

    def test_mark_done_handler(self) -> None:
        """app.js should have a mark-done handler."""
        assert "Mark Done" in self.js
        assert "handleMarkDone" in self.js or "markTaskDone" in self.js


class TestStyleCssContent:
    """Validate that style.css contains expected selectors."""

    @pytest.fixture(autouse=True)
    def _load_css(self) -> None:
        """Load style.css content for all tests in this class."""
        self.css: str = (FRONTEND_DIR / "style.css").read_text(encoding="utf-8")

    def test_has_task_list_styles(self) -> None:
        """style.css should style the task list."""
        assert ".task-list" in self.css

    def test_has_badge_styles(self) -> None:
        """style.css should style status badges."""
        assert ".badge" in self.css

    def test_has_badge_pending(self) -> None:
        """style.css should have a pending badge variant."""
        assert ".badge-pending" in self.css

    def test_has_badge_done(self) -> None:
        """style.css should have a done badge variant."""
        assert ".badge-done" in self.css

    def test_has_button_styles(self) -> None:
        """style.css should style buttons."""
        assert ".btn" in self.css

    def test_has_done_button_style(self) -> None:
        """style.css should style the mark-done button."""
        assert ".btn-done" in self.css

    def test_has_form_group_styles(self) -> None:
        """style.css should style form groups."""
        assert ".form-group" in self.css

    def test_has_error_banner_styles(self) -> None:
        """style.css should style the error banner."""
        assert ".error-banner" in self.css

    def test_has_responsive_styles(self) -> None:
        """style.css should include responsive media queries."""
        assert "@media" in self.css
