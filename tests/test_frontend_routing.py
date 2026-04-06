"""Tests for frontend main entry point and routing configuration.

Validates that main.tsx and App.tsx exist with the correct structure,
all required page components exist, and routes are properly defined.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

FRONTEND_SRC = Path(__file__).resolve().parent.parent / "frontend" / "src"


def _read_file(relative_path: str) -> str:
    """Read a file relative to the frontend src directory.

    Args:
        relative_path: Path relative to frontend/src.

    Returns:
        The file content as a string.
    """
    file_path = FRONTEND_SRC / relative_path
    assert file_path.exists(), f"Expected file not found: {file_path}"
    return file_path.read_text(encoding="utf-8")


class TestMainTsx:
    """Tests for main.tsx entry point."""

    def test_main_tsx_exists(self) -> None:
        """main.tsx must exist in frontend/src/."""
        assert (FRONTEND_SRC / "main.tsx").exists()

    def test_main_tsx_imports_react(self) -> None:
        """main.tsx must import React."""
        content = _read_file("main.tsx")
        assert "import React" in content

    def test_main_tsx_imports_react_dom(self) -> None:
        """main.tsx must import ReactDOM."""
        content = _read_file("main.tsx")
        assert "react-dom/client" in content

    def test_main_tsx_imports_browser_router(self) -> None:
        """main.tsx must import BrowserRouter from react-router-dom."""
        content = _read_file("main.tsx")
        assert "BrowserRouter" in content
        assert "react-router-dom" in content

    def test_main_tsx_imports_helmet_provider(self) -> None:
        """main.tsx must import HelmetProvider from react-helmet-async."""
        content = _read_file("main.tsx")
        assert "HelmetProvider" in content
        assert "react-helmet-async" in content

    def test_main_tsx_uses_strict_mode(self) -> None:
        """main.tsx must wrap the app in React.StrictMode."""
        content = _read_file("main.tsx")
        assert "<React.StrictMode>" in content
        assert "</React.StrictMode>" in content

    def test_main_tsx_uses_helmet_provider(self) -> None:
        """main.tsx must wrap the app in HelmetProvider."""
        content = _read_file("main.tsx")
        assert "<HelmetProvider>" in content
        assert "</HelmetProvider>" in content

    def test_main_tsx_uses_browser_router(self) -> None:
        """main.tsx must wrap the app in BrowserRouter."""
        content = _read_file("main.tsx")
        assert "<BrowserRouter>" in content
        assert "</BrowserRouter>" in content

    def test_main_tsx_nesting_order(self) -> None:
        """StrictMode must wrap HelmetProvider, which wraps BrowserRouter."""
        content = _read_file("main.tsx")
        strict_pos = content.index("<React.StrictMode>")
        helmet_pos = content.index("<HelmetProvider>")
        router_pos = content.index("<BrowserRouter>")
        assert strict_pos < helmet_pos < router_pos

    def test_main_tsx_imports_app(self) -> None:
        """main.tsx must import the App component."""
        content = _read_file("main.tsx")
        assert "import App from" in content

    def test_main_tsx_renders_app(self) -> None:
        """main.tsx must render the App component."""
        content = _read_file("main.tsx")
        assert "<App />" in content or "<App/>" in content

    def test_main_tsx_imports_css(self) -> None:
        """main.tsx must import index.css."""
        content = _read_file("main.tsx")
        assert "./index.css" in content

    def test_main_tsx_root_element_error(self) -> None:
        """main.tsx must throw an error if root element is not found."""
        content = _read_file("main.tsx")
        assert "getElementById('root')" in content or 'getElementById("root")' in content
        assert "throw new Error" in content


class TestAppTsx:
    """Tests for App.tsx routing configuration."""

    def test_app_tsx_exists(self) -> None:
        """App.tsx must exist in frontend/src/."""
        assert (FRONTEND_SRC / "App.tsx").exists()

    def test_app_tsx_imports_routes(self) -> None:
        """App.tsx must import Routes and Route from react-router-dom."""
        content = _read_file("App.tsx")
        assert "Routes" in content
        assert "Route" in content
        assert "react-router-dom" in content

    def test_app_tsx_imports_helmet(self) -> None:
        """App.tsx must import Helmet from react-helmet-async."""
        content = _read_file("App.tsx")
        assert "Helmet" in content
        assert "react-helmet-async" in content

    def test_app_tsx_has_home_route(self) -> None:
        """App.tsx must define a route for '/' (home/board list)."""
        content = _read_file("App.tsx")
        assert 'path="/"' in content

    def test_app_tsx_has_board_detail_route(self) -> None:
        """App.tsx must define a route for '/boards/:slug' (board detail)."""
        content = _read_file("App.tsx")
        assert 'path="/boards/:slug"' in content

    def test_app_tsx_has_tag_list_route(self) -> None:
        """App.tsx must define a route for '/tags' (tag list)."""
        content = _read_file("App.tsx")
        assert 'path="/tags"' in content

    def test_app_tsx_has_tag_detail_route(self) -> None:
        """App.tsx must define a route for '/tags/:slug' (tag detail)."""
        content = _read_file("App.tsx")
        assert 'path="/tags/:slug"' in content

    def test_app_tsx_has_catch_all_route(self) -> None:
        """App.tsx must define a catch-all route for 404 handling."""
        content = _read_file("App.tsx")
        assert 'path="*"' in content

    def test_app_tsx_has_global_meta_title(self) -> None:
        """App.tsx must set a global default page title."""
        content = _read_file("App.tsx")
        assert "<title>" in content or "<title>Kanban Board</title>" in content

    def test_app_tsx_has_global_meta_description(self) -> None:
        """App.tsx must set a global meta description."""
        content = _read_file("App.tsx")
        assert 'name="description"' in content

    def test_app_tsx_exports_default(self) -> None:
        """App.tsx must have a default export."""
        content = _read_file("App.tsx")
        assert "export default App" in content

    def test_app_tsx_has_docstring(self) -> None:
        """App component must have a JSDoc comment or docstring."""
        content = _read_file("App.tsx")
        assert "/**" in content


class TestPageComponents:
    """Tests for individual page components."""

    def test_home_page_exists(self) -> None:
        """HomePage component must exist."""
        assert (FRONTEND_SRC / "pages" / "HomePage.tsx").exists()

    def test_board_detail_page_exists(self) -> None:
        """BoardDetailPage component must exist."""
        assert (FRONTEND_SRC / "pages" / "BoardDetailPage.tsx").exists()

    def test_tag_list_page_exists(self) -> None:
        """TagListPage component must exist."""
        assert (FRONTEND_SRC / "pages" / "TagListPage.tsx").exists()

    def test_tag_detail_page_exists(self) -> None:
        """TagDetailPage component must exist."""
        assert (FRONTEND_SRC / "pages" / "TagDetailPage.tsx").exists()

    def test_not_found_page_exists(self) -> None:
        """NotFoundPage component must exist."""
        assert (FRONTEND_SRC / "pages" / "NotFoundPage.tsx").exists()

    def test_home_page_has_helmet(self) -> None:
        """HomePage must use Helmet for SEO meta tags."""
        content = _read_file("pages/HomePage.tsx")
        assert "Helmet" in content
        assert "<title>" in content

    def test_board_detail_page_uses_slug_param(self) -> None:
        """BoardDetailPage must use the slug URL parameter."""
        content = _read_file("pages/BoardDetailPage.tsx")
        assert "useParams" in content
        assert "slug" in content

    def test_board_detail_page_has_helmet(self) -> None:
        """BoardDetailPage must use Helmet for SEO meta tags."""
        content = _read_file("pages/BoardDetailPage.tsx")
        assert "Helmet" in content
        assert "<title>" in content

    def test_tag_list_page_has_helmet(self) -> None:
        """TagListPage must use Helmet for SEO meta tags."""
        content = _read_file("pages/TagListPage.tsx")
        assert "Helmet" in content
        assert "<title>" in content

    def test_tag_detail_page_uses_slug_param(self) -> None:
        """TagDetailPage must use the slug URL parameter."""
        content = _read_file("pages/TagDetailPage.tsx")
        assert "useParams" in content
        assert "slug" in content

    def test_tag_detail_page_has_helmet(self) -> None:
        """TagDetailPage must use Helmet for SEO meta tags."""
        content = _read_file("pages/TagDetailPage.tsx")
        assert "Helmet" in content
        assert "<title>" in content

    def test_not_found_page_has_helmet(self) -> None:
        """NotFoundPage must use Helmet with noindex directive."""
        content = _read_file("pages/NotFoundPage.tsx")
        assert "Helmet" in content
        assert "noindex" in content

    def test_not_found_page_has_link_home(self) -> None:
        """NotFoundPage must contain a link back to home."""
        content = _read_file("pages/NotFoundPage.tsx")
        assert "Link" in content
        assert 'to="/"' in content

    def test_home_page_has_canonical(self) -> None:
        """HomePage must have a canonical link tag."""
        content = _read_file("pages/HomePage.tsx")
        assert "canonical" in content

    def test_board_detail_page_has_canonical(self) -> None:
        """BoardDetailPage must have a canonical link tag."""
        content = _read_file("pages/BoardDetailPage.tsx")
        assert "canonical" in content

    def test_tag_list_page_has_canonical(self) -> None:
        """TagListPage must have a canonical link tag."""
        content = _read_file("pages/TagListPage.tsx")
        assert "canonical" in content

    def test_tag_detail_page_has_canonical(self) -> None:
        """TagDetailPage must have a canonical link tag."""
        content = _read_file("pages/TagDetailPage.tsx")
        assert "canonical" in content


class TestRouteSlugsAreSeoFriendly:
    """Tests ensuring routes use SEO-friendly slug-based URLs."""

    def test_board_route_uses_slug_not_id(self) -> None:
        """Board detail route must use :slug, not :id."""
        content = _read_file("App.tsx")
        assert ':slug' in content
        # Ensure we're not using numeric IDs in the board route
        assert 'path="/boards/:id"' not in content

    def test_tag_route_uses_slug_not_id(self) -> None:
        """Tag detail route must use :slug, not :id."""
        content = _read_file("App.tsx")
        # Ensure we're not using numeric IDs in the tag route
        assert 'path="/tags/:id"' not in content
        assert 'path="/tags/:slug"' in content

    def test_all_route_paths_are_lowercase(self) -> None:
        """All route paths should be lowercase."""
        content = _read_file("App.tsx")
        import re
        paths = re.findall(r'path="([^"]+)"', content)
        for path in paths:
            # Remove dynamic segments for case check
            static_parts = re.sub(r':[a-zA-Z]+', '', path)
            assert static_parts == static_parts.lower(), (
                f"Route path '{path}' contains uppercase characters in static segments"
            )
