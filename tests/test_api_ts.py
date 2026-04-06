"""Tests validating the structure and content of src/api.ts.

Since these are backend-side structural tests (no Node/TS toolchain
required), we simply read the file and assert on its textual content.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

API_TS_PATH: Path = Path(__file__).resolve().parent.parent / "src" / "api.ts"


@pytest.fixture()
def api_ts_content() -> str:
    """Read and return the full text of src/api.ts."""
    assert API_TS_PATH.exists(), f"{API_TS_PATH} does not exist"
    return API_TS_PATH.read_text(encoding="utf-8")


class TestApiTsExists:
    """Ensure src/api.ts is present in the repository."""

    def test_file_exists(self) -> None:
        """src/api.ts must exist."""
        assert API_TS_PATH.exists()

    def test_file_is_not_empty(self, api_ts_content: str) -> None:
        """src/api.ts must not be empty."""
        assert len(api_ts_content.strip()) > 0


class TestAxiosInstance:
    """Verify that an axios instance is configured correctly."""

    def test_imports_axios(self, api_ts_content: str) -> None:
        """The file must import from axios."""
        assert "import axios" in api_ts_content or "from \"axios\"" in api_ts_content

    def test_creates_instance(self, api_ts_content: str) -> None:
        """The file must call axios.create."""
        assert "axios.create" in api_ts_content

    def test_base_url_configured(self, api_ts_content: str) -> None:
        """The axios instance must reference a baseURL."""
        assert "baseURL" in api_ts_content

    def test_references_localhost_8000(self, api_ts_content: str) -> None:
        """The file must mention http://localhost:8000 as a development URL."""
        assert "http://localhost:8000" in api_ts_content

    def test_references_api_prefix(self, api_ts_content: str) -> None:
        """The axios instance or helper must use the /api prefix."""
        assert "/api" in api_ts_content


class TestCrudFunctions:
    """Ensure all four CRUD helper functions are exported."""

    @pytest.mark.parametrize(
        "fn_name",
        ["getTasks", "createTask", "updateTask", "deleteTask"],
    )
    def test_function_exported(self, api_ts_content: str, fn_name: str) -> None:
        """Each CRUD function must be an exported async function."""
        assert f"export async function {fn_name}" in api_ts_content

    def test_get_tasks_accepts_optional_status(self, api_ts_content: str) -> None:
        """getTasks must accept an optional status parameter."""
        assert "status?" in api_ts_content or "status ?:" in api_ts_content

    def test_create_task_accepts_data(self, api_ts_content: str) -> None:
        """createTask must accept a data parameter."""
        assert "createTask(data" in api_ts_content or "createTask(\n" in api_ts_content

    def test_update_task_accepts_id_and_data(self, api_ts_content: str) -> None:
        """updateTask must accept both id and data parameters."""
        # Just verify both 'id' and 'data' appear in the function signature line
        assert "updateTask(" in api_ts_content
        # Find the signature
        idx = api_ts_content.index("updateTask(")
        # Look at the next 200 chars to capture multi-line signatures
        signature_area = api_ts_content[idx : idx + 200]
        assert "id" in signature_area
        assert "data" in signature_area

    def test_delete_task_accepts_id(self, api_ts_content: str) -> None:
        """deleteTask must accept an id parameter."""
        assert "deleteTask(" in api_ts_content
        idx = api_ts_content.index("deleteTask(")
        signature_area = api_ts_content[idx : idx + 100]
        assert "id" in signature_area


class TestHttpMethods:
    """Verify that the correct HTTP methods are used for each operation."""

    def test_get_method_used(self, api_ts_content: str) -> None:
        """getTasks must use a GET request."""
        assert "apiClient.get" in api_ts_content or ".get(" in api_ts_content

    def test_post_method_used(self, api_ts_content: str) -> None:
        """createTask must use a POST request."""
        assert "apiClient.post" in api_ts_content or ".post(" in api_ts_content

    def test_put_method_used(self, api_ts_content: str) -> None:
        """updateTask must use a PUT request."""
        assert "apiClient.put" in api_ts_content or ".put(" in api_ts_content

    def test_delete_method_used(self, api_ts_content: str) -> None:
        """deleteTask must use a DELETE request."""
        assert "apiClient.delete" in api_ts_content or ".delete(" in api_ts_content


class TestTypeDefinitions:
    """Verify that TypeScript interfaces/types are defined."""

    def test_task_interface(self, api_ts_content: str) -> None:
        """A Task interface must be exported."""
        assert "export interface Task" in api_ts_content

    def test_task_create_data_interface(self, api_ts_content: str) -> None:
        """A TaskCreateData interface must be exported."""
        assert "export interface TaskCreateData" in api_ts_content

    def test_task_update_data_interface(self, api_ts_content: str) -> None:
        """A TaskUpdateData interface must be exported."""
        assert "export interface TaskUpdateData" in api_ts_content

    def test_task_status_type(self, api_ts_content: str) -> None:
        """A TaskStatus type must be exported."""
        assert "export type TaskStatus" in api_ts_content

    def test_task_has_id_field(self, api_ts_content: str) -> None:
        """The Task interface must include an id field."""
        assert "id:" in api_ts_content or "id :" in api_ts_content

    def test_task_has_title_field(self, api_ts_content: str) -> None:
        """The Task interface must include a title field."""
        assert "title:" in api_ts_content or "title :" in api_ts_content

    def test_task_has_status_field(self, api_ts_content: str) -> None:
        """The Task interface must include a status field."""
        assert "status:" in api_ts_content or "status :" in api_ts_content
