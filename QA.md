app_type: web-api
coverage_applies: true
coverage_source: app
coverage_threshold: 70
coverage_tool: pytest-cov
install_steps:
- pip install -r /tmp/forge-repos/hello-world-micro-api-02986f67/requirements.txt
- pip install ruff
lint_tool: ruff check .
notes: Verify that GET /hello returns 200 with 'message' equal to 'hello world' and
  a valid ISO 8601 'timestamp', and that a non-existent route returns 404.
stack: Python/FastAPI
test_files:
- tests/test_hello.py
- tests/test_main.py
- tests/test_models.py
- tests/test_storage.py
- tests/test_todos.py
test_runner: pytest tests/ -v --tb=short
workspace: /tmp/forge-repos/hello-world-micro-api-02986f67
