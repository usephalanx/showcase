# Architecture

## 1. Project Overview

Monorepo structure:
- `/backend` — Python 3.12 / FastAPI / SQLAlchemy / SQLite
- `/frontend` — React / TypeScript / Vite (future)

## 2. Database Schema Design

SQLite database with four tables:

### 2.1 users
```sql
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT    UNIQUE NOT NULL,
    hashed_password TEXT    NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

### 2.2 boards
```sql
CREATE TABLE boards (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_boards_user_id ON boards(user_id);
```

### 2.3 columns
```sql
CREATE TABLE columns (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT    NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    board_id INTEGER NOT NULL REFERENCES boards(id) ON DELETE CASCADE
);
CREATE INDEX idx_columns_board_id ON columns(board_id);
```

### 2.4 cards
```sql
CREATE TABLE cards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    position    INTEGER NOT NULL DEFAULT 0,
    column_id   INTEGER NOT NULL REFERENCES columns(id) ON DELETE CASCADE,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX idx_cards_column_id ON cards(column_id);
```

## 3. Frontend Component Hierarchy

```
App
└── AuthProvider
    ├── AuthPages
    │   ├── LoginForm
    │   └── RegisterForm
    └── AppLayout
        ├── BoardList
        └── BoardView
            └── Column
                └── Card
```

## 4. Drag-and-Drop Strategy

- Library: `@dnd-kit/core` + `@dnd-kit/sortable`
- DndContext wraps BoardView
- Each Column is a SortableContext with useDroppable
- Each Card uses useSortable
- Sensors: PointerSensor with activationConstraint distance: 8
- Collision detection: closestCorners

### 4.1 Event Handlers
- `onDragStart` — set activeCard state for DragOverlay
- `onDragOver` — move card between columns optimistically
- `onDragEnd` — finalize position, call `POST /cards/{id}/move`

## 5. Data Flow for Card Movement

1. User drags card
2. `onDragEnd` fires
3. Optimistic state update (reorder cards array in React state)
4. `POST /cards/{id}/move` with `{column_id, position}`
5. On success: no-op (already updated)
6. On failure: rollback to previous state and show toast error

### 5.1 Position Recalculation

Cards are ordered by position integer. On move, server reindexes all
positions in affected column(s) sequentially (0, 1, 2, …). Client sends
target `column_id` and target `position` index.

## 6. Docker Strategy

- Backend Dockerfile: python:3.12-slim, pip install, uvicorn
- Frontend Dockerfile: node:20-alpine multi-stage (build then nginx:alpine)
- docker-compose.yml with backend (port 8000), frontend (port 5173)
