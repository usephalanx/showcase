"""Database initialisation script.

Run this script directly to create all tables defined by the SQLAlchemy
ORM models in the configured SQLite database:

    python init_db.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the backend package is importable when running the script
# directly from the backend/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import init_db  # noqa: E402


def main() -> None:
    """Create all database tables and print confirmation."""
    print("Initialising database …")
    init_db()
    print("Done – all tables created.")


if __name__ == "__main__":
    main()
