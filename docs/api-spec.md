# API Specification

Base URL: `/`

---

## Authentication

### POST /auth/register

Create a new user account.

**Request Body:**
```json
{
  "username": "alice",
  "password": "strongpass123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "alice",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

**Errors:**
- `409` – Username already registered
- `422` – Validation error

---

### POST /auth/login

Obtain a JWT access token.

**Request Body:**
```json
{
  "username": "alice",
  "password": "strongpass123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Errors:**
- `401` – Invalid username or password

---

## Projects (require `Authorization: Bearer <token>`)

### GET /api/projects

**Query Params:** `skip` (int, default 0), `limit` (int, default 100)

**Response (200):** `ProjectResponse[]`

### POST /api/projects

**Request Body:** `ProjectCreate` (`name`, `description`)

**Response (201):** `ProjectResponse`

### GET /api/projects/{id}

**Response (200):** `ProjectDetailResponse` (includes `tasks`)

**Errors:** `404` – Project not found

### DELETE /api/projects/{id}

**Response:** `204 No Content`

**Errors:** `404` – Project not found

---

## Tasks (require `Authorization: Bearer <token>`)

### GET /api/projects/{id}/tasks

**Query Params:** `status` (optional filter)

**Response (200):** `TaskResponse[]`

### POST /api/projects/{id}/tasks

**Request Body:** `TaskCreate` (`title`, `description`, `status`, `priority`, `due_date`)

**Response (201):** `TaskResponse`

### PATCH /api/tasks/{id}

**Request Body:** `TaskUpdate` (partial fields)

**Response (200):** `TaskResponse`

**Errors:** `404` – Task not found

### DELETE /api/tasks/{id}

**Response:** `204 No Content`

**Errors:** `404` – Task not found

---

## Schemas

### UserCreate
| Field | Type | Constraints |
|---|---|---|
| username | string | min 3, max 50 |
| password | string | min 6, max 128 |

### UserResponse
| Field | Type |
|---|---|
| id | integer |
| username | string |
| is_active | boolean |
| created_at | datetime |

### TokenResponse
| Field | Type |
|---|---|
| access_token | string |
| token_type | string ("bearer") |

### LoginRequest
| Field | Type |
|---|---|
| username | string |
| password | string |

### ProjectCreate
| Field | Type | Constraints |
|---|---|---|
| name | string | min 1, max 100 |
| description | string? | max 2000 |

### ProjectResponse
| Field | Type |
|---|---|
| id | integer |
| name | string |
| description | string? |
| created_at | datetime |

### ProjectDetailResponse
Same as ProjectResponse plus `tasks: TaskResponse[]`.

### TaskCreate
| Field | Type | Default |
|---|---|---|
| title | string (max 200) | required |
| description | string? | "" |
| status | TaskStatus | "todo" |
| priority | TaskPriority | "medium" |
| due_date | date? | null |

### TaskUpdate
All fields optional.

### TaskResponse
| Field | Type |
|---|---|
| id | integer |
| project_id | integer |
| title | string |
| description | string? |
| status | TaskStatus |
| priority | TaskPriority |
| due_date | date? |
| created_at | datetime |

### Error Response
```json
{"detail": "Error description"}
```
