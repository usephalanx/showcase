# Database Schema

Backend: **SQLite** via **SQLAlchemy 2.0** (declarative mapping).

---

## Tables

### users

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| username | VARCHAR(50) | UNIQUE NOT NULL, INDEX |
| hashed_password | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | NOT NULL DEFAULT TRUE |
| created_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP |

### projects

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | VARCHAR(100) | NOT NULL |
| description | TEXT | NULLABLE, DEFAULT '' |
| owner_id | INTEGER | FK → users.id ON DELETE SET NULL, NULLABLE |
| created_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP |

### tasks

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| project_id | INTEGER | FK → projects.id ON DELETE CASCADE, NOT NULL |
| title | VARCHAR(200) | NOT NULL |
| description | TEXT | NULLABLE, DEFAULT '' |
| status | ENUM('todo','in_progress','done') | NOT NULL DEFAULT 'todo' |
| priority | ENUM('low','medium','high') | NOT NULL DEFAULT 'medium' |
| due_date | DATE | NULLABLE |
| created_at | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP |

---

## Relationships

```
users 1 ──< projects (owner_id)
projects 1 ──< tasks (project_id)
```

- Deleting a user sets `projects.owner_id` to NULL.
- Deleting a project cascades to delete all its tasks.

---

## SQLAlchemy Models

Defined in `backend/app/models.py`:

- `User` → `users` table
- `Project` → `projects` table
- `Task` → `tasks` table

All models inherit from `Base` (a `DeclarativeBase` subclass defined in
`backend/app/database.py`).
