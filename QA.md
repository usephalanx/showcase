app_type: web-api
coverage_applies: true
coverage_source: app
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install -r requirements.txt
lint_tool: ruff check .
notes: Verify that all endpoint tests in tests/test_endpoints.py pass and endpoints
  return the expected JSON responses.
stack: Python/FastAPI
test_files:
- tests/__init__.py
- tests/conftest.py
- tests/test_endpoints.py
- tests/test_main.py
- tests/test_models.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/
workspace: /tmp/forge-repos/hello-world-fastapi-v4-c3a1e3ed
