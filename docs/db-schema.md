# Database Schema

Database engine: **SQLite** via SQLAlchemy 2.0.

---

## Tables

### `projects`

| Column       | Type         | Constraints                        |
| ------------ | ------------ | ---------------------------------- |
| `id`         | INTEGER      | PRIMARY KEY, AUTOINCREMENT         |
| `name`       | VARCHAR(100) | NOT NULL                           |
| `description`| TEXT         | NULLABLE, DEFAULT ''               |
| `created_at` | DATETIME     | NOT NULL, SERVER DEFAULT now()     |

**Indexes**: Primary key on `id`.

---

### `tasks`

| Column       | Type         | Constraints                                   |
| ------------ | ------------ | --------------------------------------------- |
| `id`         | INTEGER      | PRIMARY KEY, AUTOINCREMENT                    |
| `project_id` | INTEGER      | NOT NULL, FK → projects.id ON DELETE CASCADE  |
| `title`      | VARCHAR(200) | NOT NULL                                      |
| `description`| TEXT         | NULLABLE, DEFAULT ''                          |
| `status`     | ENUM         | NOT NULL, DEFAULT 'todo'                      |
|              |              | Values: `todo`, `in_progress`, `done`         |
| `priority`   | ENUM         | NOT NULL, DEFAULT 'medium'                    |
|              |              | Values: `low`, `medium`, `high`               |
| `due_date`   | DATE         | NULLABLE                                      |
| `created_at` | DATETIME     | NOT NULL, SERVER DEFAULT now()                |

**Indexes**: Primary key on `id`. Foreign key index on `project_id`.

---

### `users` (future)

| Column          | Type         | Constraints                        |
| --------------- | ------------ | ---------------------------------- |
| `id`            | INTEGER      | PRIMARY KEY, AUTOINCREMENT         |
| `username`      | VARCHAR(50)  | UNIQUE, NOT NULL                   |
| `email`         | VARCHAR(100) | UNIQUE, NOT NULL                   |
| `hashed_password` | VARCHAR(255) | NOT NULL                         |
| `is_active`     | BOOLEAN      | NOT NULL, DEFAULT TRUE             |
| `created_at`    | DATETIME     | NOT NULL, SERVER DEFAULT now()     |

---

## Relationships

```
projects 1 ──── * tasks
  (id)           (project_id)
```

- A **Project** has zero or more **Tasks**.
- Deleting a Project cascades to delete all of its Tasks.

## SQLAlchemy Model Mapping

```python
class Project(Base):
    __tablename__ = "projects"
    id          = mapped_column(Integer, primary_key=True, autoincrement=True)
    name        = mapped_column(String(100), nullable=False)
    description = mapped_column(Text, nullable=True, default="")
    created_at  = mapped_column(DateTime, nullable=False, server_default=func.now())
    tasks       = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id          = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id  = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    title       = mapped_column(String(200), nullable=False)
    description = mapped_column(Text, nullable=True, default="")
    status      = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.todo)
    priority    = mapped_column(Enum(TaskPriority), nullable=False, default=TaskPriority.medium)
    due_date    = mapped_column(Date, nullable=True)
    created_at  = mapped_column(DateTime, nullable=False, server_default=func.now())
    project     = relationship("Project", back_populates="tasks")
```
