"""Pytest configuration for healthcheck tests.

Adds the healthcheck application directory to sys.path so that
'import database' and 'import main' resolve correctly.
"""

import sys
from pathlib import Path

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)
