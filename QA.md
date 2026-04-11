app_type: web-api
coverage_applies: true
coverage_source: app
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install --upgrade pip
- pip install -r /tmp/forge-repos/hello-world-fastapi-1ca57c11/requirements.txt
lint_tool: ruff check .
notes: Verify that all tests in tests/ pass, code coverage for app/ is at least 70%,
  and ruff reports no lint errors.
stack: Python/FastAPI
test_files:
- tests/__init__.py
- tests/conftest.py
- tests/test_hello.py
- tests/test_main.py
- tests/test_models.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/
workspace: /tmp/forge-repos/hello-world-fastapi-1ca57c11
