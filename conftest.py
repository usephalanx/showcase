"""Root-level pytest configuration.

Registers the --timeout option so that pytest does not fail with
'unrecognized arguments' when pytest-timeout is not installed.
"""


def pytest_addoption(parser):
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
