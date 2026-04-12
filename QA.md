app_type: web-api
coverage_applies: true
coverage_source: .
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install -r /tmp/forge-repos/mobile-app-for-todos-9ca0fc6d/requirements.txt
- pip install pytest httpx pytest-cov ruff
lint_tool: ruff check .
notes: Verify that the Python/FastAPI test suite for the Todo app passes, covering
  storage, models, routes, database, and healthcheck endpoints with at least 70% coverage.
stack: Python/FastAPI
test_files:
- tests/__init__.py
- tests/conftest.py
- tests/test_storage_service.py
- tests/test_database.py
- tests/test_models.py
- tests/test_routes.py
- tests/test_healthcheck_endpoints.py
- tests/test_main.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/ -v
workspace: /tmp/forge-repos/mobile-app-for-todos-9ca0fc6d
