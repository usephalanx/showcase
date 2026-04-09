"""Root-level pytest configuration.

Registers the --timeout option so that pytest does not fail with
'unrecognized arguments' when pytest-timeout is not installed.

Also ensures the project root is on sys.path for correct imports.
"""

import sys
from pathlib import Path

# Ensure project root is importable
_PROJECT_ROOT = str(Path(__file__).resolve().parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def pytest_addoption(parser):  # type: ignore[no-untyped-def]
    """Register --timeout so pytest doesn't choke when the plugin is absent."""
    try:
        parser.addoption(
            "--timeout",
            action="store",
            default=None,
            help="Stub for pytest-timeout compatibility",
        )
    except ValueError:
        # Already registered (pytest-timeout is installed)
        pass
