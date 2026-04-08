"""Root-level conftest for pytest.

Ensures the project root is on sys.path so that imports like
``from models import TodoCreate`` resolve correctly when running
tests from any working directory.
"""
