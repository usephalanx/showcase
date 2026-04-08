"""Pytest configuration for tests/ directory.

Ensures the project root is on sys.path so application modules
(main, routes, models, storage) can be imported by test files.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
