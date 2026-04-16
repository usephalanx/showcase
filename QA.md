app_type: web-api
coverage_applies: true
coverage_source: app
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install -r /tmp/forge-repos/hello-world-fastapi-v2-0006d299/requirements.txt
lint_tool: ruff check .
notes: Verify that all tests pass, linting is clean, and test coverage for the app
  package is at least 70%.
stack: Python/FastAPI
test_files:
- tests/__init__.py
- tests/conftest.py
- tests/test_main.py
- tests/test_models.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/ -v
workspace: /tmp/forge-repos/hello-world-fastapi-v2-0006d299
