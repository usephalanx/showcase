app_type: web-api
coverage_applies: true
coverage_source: app
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install -r requirements.txt
lint_tool: ruff check .
notes: Verify GET /hello returns 200 with correct JSON containing 'message' and valid
  ISO 8601 'timestamp', 404 for non-existent routes, and 405 for wrong HTTP methods.
stack: Python/FastAPI
test_files:
- tests/test_hello.py
- tests/test_main.py
- tests/test_models.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/ -v
workspace: /tmp/forge-repos/hello-world-micro-api-c74aba96
