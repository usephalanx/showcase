"""Tests for the seed_data function."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.app.models import Project, Task
from backend.app.seed import seed_data


class TestSeedData:
    """Verify seeding behaviour."""

    def test_seed_populates_empty_db(self, db: Session) -> None:
        """Seed inserts projects and tasks into an empty database."""
        seed_data(db)
        assert db.query(Project).count() == 2
        assert db.query(Task).count() == 5

    def test_seed_is_idempotent(self, db: Session) -> None:
        """Running seed twice does not duplicate data."""
        seed_data(db)
        seed_data(db)
        assert db.query(Project).count() == 2
        assert db.query(Task).count() == 5

    def test_seed_skips_when_data_exists(self, db: Session) -> None:
        """Seed does nothing when the database already has data."""
        existing = Project(name="Existing", status="active")
        db.add(existing)
        db.commit()
        seed_data(db)
        # Should still have only the manually added project
        assert db.query(Project).count() == 1
        assert db.query(Task).count() == 0
