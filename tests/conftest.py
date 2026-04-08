"""Pytest configuration for the Todo API test suite.

Ensures the project root is on sys.path so that imports of top-level
modules (models, storage, etc.) resolve correctly when tests are
invoked from any working directory.
"""

import sys
from pathlib import Path

# Add project root to sys.path
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
