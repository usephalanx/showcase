"""Seed the database with sample projects and tasks.

The :func:`seed_data` function is idempotent: it only inserts rows when
both the ``projects`` and ``tasks`` tables are empty.
"""

from __future__ import annotations

import datetime
import logging

from sqlalchemy.orm import Session

from backend.app.models import Project, Task

logger = logging.getLogger(__name__)


def seed_data(db: Session) -> None:
    """Populate the database with sample data if tables are empty.

    Inserts 2 projects and 5 tasks (3 for the first project, 2 for the
    second) only when both tables contain zero rows.

    Args:
        db: An active SQLAlchemy session.
    """
    project_count: int = db.query(Project).count()
    task_count: int = db.query(Task).count()

    if project_count > 0 or task_count > 0:
        logger.info(
            "Database already contains data (projects=%d, tasks=%d). "
            "Skipping seed.",
            project_count,
            task_count,
        )
        return

    logger.info("Seeding database with sample projects and tasks.")

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------
    project_1 = Project(
        name="Website Redesign",
        description="Redesign the company website with modern UI/UX",
        status="active",
    )
    project_2 = Project(
        name="Mobile App Launch",
        description="Develop and launch the mobile application",
        status="active",
    )
    db.add_all([project_1, project_2])
    db.flush()  # Populate auto-generated IDs before referencing them.

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------
    tasks = [
        Task(
            project_id=project_1.id,
            title="Create wireframes",
            status="done",
            priority="high",
            due_date=datetime.date(2025, 1, 15),
        ),
        Task(
            project_id=project_1.id,
            title="Design homepage mockup",
            status="in_progress",
            priority="high",
            due_date=datetime.date(2025, 2, 1),
        ),
        Task(
            project_id=project_1.id,
            title="Implement responsive CSS",
            status="todo",
            priority="medium",
            due_date=datetime.date(2025, 2, 15),
        ),
        Task(
            project_id=project_2.id,
            title="Set up React Native project",
            status="done",
            priority="high",
            due_date=datetime.date(2025, 1, 20),
        ),
        Task(
            project_id=project_2.id,
            title="Build authentication flow",
            status="in_progress",
            priority="high",
            due_date=datetime.date(2025, 2, 10),
        ),
    ]
    db.add_all(tasks)
    db.commit()

    logger.info(
        "Seed complete: %d projects, %d tasks.",
        len([project_1, project_2]),
        len(tasks),
    )
