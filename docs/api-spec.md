# REST API Specification

Base URL: `/api`

---

## Authentication

### `POST /api/auth/register`

Register a new user account.

**Request Body**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response** – `201 Created`

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00"
}
```

**Errors**: `409 Conflict` if username/email already exists.

---

### `POST /api/auth/login`

Authenticate and receive an access token.

**Request Body**

```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response** – `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errors**: `401 Unauthorized` if credentials are invalid.

---

## Projects

All project endpoints require `Authorization: Bearer <token>`.

### `GET /api/projects`

List all projects for the authenticated user.

| Query Param | Type | Default | Description       |
| ----------- | ---- | ------- | ----------------- |
| `skip`      | int  | 0       | Pagination offset |
| `limit`     | int  | 100     | Max items         |

**Response** – `200 OK`

```json
[
  {
    "id": 1,
    "name": "My Project",
    "description": "A sample project",
    "created_at": "2025-01-01T00:00:00"
  }
]
```

---

### `POST /api/projects`

Create a new project.

**Request Body** (`ProjectCreate`)

```json
{
  "name": "New Project",
  "description": "Optional description"
}
```

**Response** – `201 Created` (`ProjectResponse`)

```json
{
  "id": 2,
  "name": "New Project",
  "description": "Optional description",
  "created_at": "2025-01-01T12:00:00"
}
```

---

### `GET /api/projects/{id}`

Get a single project with its tasks.

**Response** – `200 OK` (`ProjectDetailResponse`)

```json
{
  "id": 1,
  "name": "My Project",
  "description": "desc",
  "created_at": "2025-01-01T00:00:00",
  "tasks": [
    {
      "id": 1,
      "project_id": 1,
      "title": "First task",
      "description": "",
      "status": "todo",
      "priority": "medium",
      "due_date": null,
      "created_at": "2025-01-01T00:00:00"
    }
  ]
}
```

**Errors**: `404 Not Found`.

---

### `DELETE /api/projects/{id}`

Delete a project and all its tasks.

**Response** – `204 No Content`

**Errors**: `404 Not Found`.

---

## Tasks

All task endpoints require `Authorization: Bearer <token>`.

### `GET /api/projects/{id}/tasks`

List tasks for a given project.

| Query Param | Type   | Default | Description    |
| ----------- | ------ | ------- | -------------- |
| `status`    | string | (all)   | Filter by status (`todo`, `in_progress`, `done`) |

**Response** – `200 OK`

```json
[
  {
    "id": 1,
    "project_id": 1,
    "title": "Task title",
    "description": "",
    "status": "todo",
    "priority": "medium",
    "due_date": "2025-06-15",
    "created_at": "2025-01-01T00:00:00"
  }
]
```

---

### `POST /api/projects/{id}/tasks`

Create a new task in a project.

**Request Body** (`TaskCreate`)

```json
{
  "title": "Implement feature",
  "description": "Details here",
  "status": "todo",
  "priority": "high",
  "due_date": "2025-06-15"
}
```

**Response** – `201 Created` (`TaskResponse`)

---

### `PATCH /api/tasks/{id}`

Partially update a task.

**Request Body** (`TaskUpdate`) – all fields optional:

```json
{
  "status": "done",
  "priority": "low"
}
```

**Response** – `200 OK` (`TaskResponse`)

**Errors**: `404 Not Found`.

---

### `DELETE /api/tasks/{id}`

Delete a task.

**Response** – `204 No Content`

**Errors**: `404 Not Found`.

---

## Schema Definitions

### `ProjectCreate`
| Field         | Type   | Required | Constraints        |
| ------------- | ------ | -------- | ------------------ |
| `name`        | string | Yes      | 1–100 characters   |
| `description` | string | No       | Max 2000 chars     |

### `ProjectResponse`
| Field        | Type     |
| ------------ | -------- |
| `id`         | integer  |
| `name`       | string   |
| `description`| string?  |
| `created_at` | datetime |

### `ProjectDetailResponse`
Same as `ProjectResponse` plus:
| Field   | Type             |
| ------- | ---------------- |
| `tasks` | TaskResponse[]   |

### `TaskCreate`
| Field         | Type   | Required | Default    |
| ------------- | ------ | -------- | ---------- |
| `title`       | string | Yes      | —          |
| `description` | string | No       | `""`       |
| `status`      | enum   | No       | `todo`     |
| `priority`    | enum   | No       | `medium`   |
| `due_date`    | date   | No       | `null`     |

### `TaskUpdate`
All fields from `TaskCreate` but every field is optional.

### `TaskResponse`
| Field        | Type     |
| ------------ | -------- |
| `id`         | integer  |
| `project_id` | integer  |
| `title`      | string   |
| `description`| string?  |
| `status`     | enum     |
| `priority`   | enum     |
| `due_date`   | date?    |
| `created_at` | datetime |

### Error Response
```json
{
  "detail": "Human-readable error message"
}
```
