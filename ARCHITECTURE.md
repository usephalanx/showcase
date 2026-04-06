# Kanban Board — Architecture Document

This document defines the complete architecture for the Kanban website, including all data models, API contracts, URL structure, SEO strategy, component hierarchy, and tech stack decisions.

---

## 1. Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** SQLite via SQLAlchemy 2.0 + aiosqlite (WAL mode enabled)
- **Migrations:** Alembic
- **Validation:** Pydantic v2
- **Server:** Uvicorn

### Frontend
- **Framework:** React 18 + TypeScript
- **Bundler:** Vite 5
- **Routing:** react-router-dom v6
- **SEO:** react-helmet-async
- **Drag & Drop:** @hello-pangea/dnd
- **HTTP Client:** axios
- **Styling:** TailwindCSS 3.4
- **UI Primitives:** @headlessui/react

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Reverse Proxy:** Vite dev proxy (development), Nginx (production)

---

## 2. Data Models

### Board
| Field       | Type         | Constraints                              |
|-------------|-------------|------------------------------------------|
| id          | INTEGER     | PRIMARY KEY, AUTOINCREMENT               |
| title       | VARCHAR(255)| NOT NULL                                 |
| slug        | VARCHAR(255)| NOT NULL, UNIQUE, INDEX                  |
| description | TEXT        | NULLABLE                                 |
| created_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |
| updated_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |

### Column
| Field       | Type         | Constraints                              |
|-------------|-------------|------------------------------------------|
| id          | INTEGER     | PRIMARY KEY, AUTOINCREMENT               |
| board_id    | INTEGER     | NOT NULL, FOREIGN KEY → boards(id) ON DELETE CASCADE |
| title       | VARCHAR(255)| NOT NULL                                 |
| position    | INTEGER     | NOT NULL, DEFAULT 0                      |
| created_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |
| updated_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |

**Index:** `(board_id, position)`

### Card
| Field       | Type         | Constraints                              |
|-------------|-------------|------------------------------------------|
| id          | INTEGER     | PRIMARY KEY, AUTOINCREMENT               |
| column_id   | INTEGER     | NOT NULL, FOREIGN KEY → columns(id) ON DELETE CASCADE |
| title       | VARCHAR(255)| NOT NULL                                 |
| slug        | VARCHAR(255)| NOT NULL, UNIQUE, INDEX                  |
| description | TEXT        | NULLABLE                                 |
| position    | INTEGER     | NOT NULL, DEFAULT 0                      |
| created_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |
| updated_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |

**Index:** `(column_id, position)`

### Tag
| Field       | Type         | Constraints                              |
|-------------|-------------|------------------------------------------|
| id          | INTEGER     | PRIMARY KEY, AUTOINCREMENT               |
| name        | VARCHAR(100)| NOT NULL, UNIQUE                         |
| color       | VARCHAR(7)  | NOT NULL, DEFAULT '#6b7280'              |
| created_at  | DATETIME    | NOT NULL, DEFAULT CURRENT_TIMESTAMP      |

### CardTag (Junction)
| Field       | Type         | Constraints                              |
|-------------|-------------|------------------------------------------|
| card_id     | INTEGER     | NOT NULL, FOREIGN KEY → cards(id) ON DELETE CASCADE |
| tag_id      | INTEGER     | NOT NULL, FOREIGN KEY → tags(id) ON DELETE CASCADE  |

**Primary Key:** `(card_id, tag_id)`

### Slug Generation Strategy
1. Convert title to lowercase.
2. Replace non-alphanumeric characters with hyphens.
3. Collapse consecutive hyphens.
4. Trim leading/trailing hyphens.
5. If the slug already exists, append `-2`, `-3`, etc., incrementing until unique.

### Card Reordering Algorithm
Positions use integer values with initial gaps of 1000 (e.g., 1000, 2000, 3000).
When inserting between two cards, the new position = `(prev_position + next_position) / 2`.
When the gap becomes < 1, renumber all cards in the column sequentially with gaps of 1000.

### Tag Deletion Strategy
Tags use CASCADE delete on the `card_tags` junction table. Deleting a tag removes all associations but does not delete the cards themselves.

---

## 3. API Endpoints

Base path: `/api`

### Boards
| Method | Path                    | Description              | Status Codes      |
|--------|------------------------|--------------------------|-------------------|
| GET    | /api/boards            | List all boards          | 200               |
| POST   | /api/boards            | Create a board           | 201, 422          |
| GET    | /api/boards/:id        | Get board with columns & cards | 200, 404   |
| PUT    | /api/boards/:id        | Update board             | 200, 404, 422     |
| DELETE | /api/boards/:id        | Delete board (cascades)  | 204, 404          |

### Columns
| Method | Path                           | Description              | Status Codes      |
|--------|-------------------------------|--------------------------|-------------------|
| POST   | /api/boards/:board_id/columns | Create a column          | 201, 404, 422     |
| PUT    | /api/columns/:id              | Update column            | 200, 404, 422     |
| DELETE | /api/columns/:id              | Delete column (cascades) | 204, 404          |
| PUT    | /api/columns/:id/move         | Reorder column           | 200, 404, 422     |

### Cards
| Method | Path                             | Description                | Status Codes      |
|--------|--------------------------------|----------------------------|-------------------|
| POST   | /api/columns/:column_id/cards  | Create a card              | 201, 404, 422     |
| GET    | /api/cards/:id                 | Get card detail            | 200, 404          |
| PUT    | /api/cards/:id                 | Update card                | 200, 404, 422     |
| DELETE | /api/cards/:id                 | Delete card                | 204, 404          |
| PUT    | /api/cards/:id/move            | Move card (column & position) | 200, 404, 422 |

### Tags
| Method | Path                           | Description              | Status Codes      |
|--------|-------------------------------|--------------------------|-------------------|
| GET    | /api/tags                     | List all tags            | 200               |
| POST   | /api/tags                     | Create a tag             | 201, 422          |
| DELETE | /api/tags/:id                 | Delete a tag             | 204, 404          |
| POST   | /api/cards/:card_id/tags      | Attach tag to card       | 200, 404          |
| DELETE | /api/cards/:card_id/tags/:tag_id | Detach tag from card  | 204, 404          |

### SEO
| Method | Path                    | Description              | Status Codes      |
|--------|------------------------|--------------------------|-------------------|
| GET    | /api/sitemap.xml       | Generated XML sitemap    | 200               |
| GET    | /robots.txt            | Robots file              | 200               |

### Request/Response Schemas (Examples)

**Create Board Request:**
```json
{
  "title": "My Project",
  "description": "Optional description"
}
```

**Board Response:**
```json
{
  "id": 1,
  "title": "My Project",
  "slug": "my-project",
  "description": "Optional description",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "columns": []
}
```

**Move Card Request:**
```json
{
  "column_id": 2,
  "position": 1500
}
```

---

## 4. URL Structure & Routing

### Frontend Routes
| Path                     | Page Component    | Description                    |
|--------------------------|-------------------|--------------------------------|
| `/`                      | HomePage          | Lists all boards               |
| `/boards/:slug`          | BoardPage         | Full Kanban board view         |
| `/cards/:slug`           | CardDetailPage    | Individual card detail view    |
| `*`                      | NotFoundPage      | 404 page for invalid routes    |

### SEO URLs
- All routes use human-readable slugs.
- Canonical URLs are absolute (e.g., `https://example.com/boards/my-project`).
- `sitemap.xml` is generated dynamically from the database listing all boards and cards.
- `robots.txt` allows all crawlers with sitemap reference.

### 404 Handling
- Frontend: react-router catch-all route renders `NotFoundPage` with proper meta tags (`<meta name="robots" content="noindex" />`).
- API: Returns `{ "detail": "Not found" }` with HTTP 404 for invalid slugs/IDs.

---

## 5. Meta Tag Strategy

### Per-Page Templates

**Home Page:**
- Title: `Kanban Board — Organize Your Projects`
- Description: `Create and manage Kanban boards to organize your tasks and projects with drag-and-drop.`
- OG Type: `website`

**Board Page:**
- Title: `{board.title} — Kanban Board`
- Description: `{board.description}` (truncated to 160 characters, with ellipsis if needed)
- OG Type: `article`
- Canonical: `/boards/{board.slug}`

**Card Detail Page:**
- Title: `{card.title} — Kanban Board`
- Description: `{card.description}` (truncated to 160 characters)
- OG Type: `article`
- Canonical: `/cards/{card.slug}`

**Not Found Page:**
- Title: `Page Not Found — Kanban Board`
- Meta robots: `noindex, nofollow`

### Description Truncation Strategy
If the source text exceeds 160 characters, truncate at the last complete word boundary before 157 characters and append `...`.

### Open Graph & Twitter Cards
All pages include:
- `og:title`, `og:description`, `og:url`, `og:type`
- `twitter:card` = `summary_large_image`
- `twitter:title`, `twitter:description`

### JSON-LD Structured Data
Board pages include `CollectionPage` schema. Card pages include `Article` schema with `datePublished` and `dateModified`.

---

## 6. Frontend Component Tree

```
App
├── Helmet (global defaults)
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   └── Navigation
│   └── Main (outlet)
│       ├── HomePage
│       │   ├── Helmet (page meta)
│       │   ├── BoardList
│       │   │   ├── BoardCard (× N)
│       │   │   └── EmptyState (when no boards)
│       │   └── CreateBoardDialog
│       ├── BoardPage
│       │   ├── Helmet (page meta)
│       │   ├── BoardHeader
│       │   │   ├── BoardTitle (editable)
│       │   │   └── BoardActions
│       │   ├── DragDropContext
│       │   │   └── ColumnList
│       │   │       ├── Column (× N)
│       │   │       │   ├── ColumnHeader (editable title)
│       │   │       │   ├── Droppable
│       │   │       │   │   ├── CardItem (× N, Draggable)
│       │   │       │   │   │   ├── CardTitle
│       │   │       │   │   │   ├── TagBadge (× N)
│       │   │       │   │   │   └── CardActions
│       │   │       │   │   └── EmptyColumnState
│       │   │       │   └── AddCardButton
│       │   │       └── AddColumnButton
│       │   └── EmptyBoardState (when no columns)
│       ├── CardDetailPage
│       │   ├── Helmet (page meta)
│       │   ├── CardHeader
│       │   ├── CardDescription (editable)
│       │   ├── TagManager
│       │   │   ├── TagBadge (× N)
│       │   │   └── AddTagPopover
│       │   └── CardMetadata
│       └── NotFoundPage
│           └── Helmet (noindex)
└── Shared Components
    ├── Dialog (Headless UI wrapper)
    ├── Popover (Headless UI wrapper)
    ├── ConfirmDialog
    ├── LoadingSpinner
    ├── ErrorBoundary
    └── TagBadge
```

---

## 7. Database Schema

```sql
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE boards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_boards_slug ON boards(slug);

CREATE TABLE columns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    position INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
);

CREATE INDEX idx_columns_board_position ON columns(board_id, position);

CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    column_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    position INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE
);

CREATE INDEX idx_cards_slug ON cards(slug);
CREATE INDEX idx_cards_column_position ON cards(column_id, position);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    color VARCHAR(7) NOT NULL DEFAULT '#6b7280',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE card_tags (
    card_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (card_id, tag_id),
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

---

## 8. Directory Structure

```
project-root/
├── ARCHITECTURE.md
├── RUNNING.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI app factory
│       ├── config.py            # Settings via pydantic-settings
│       ├── database.py          # SQLAlchemy engine & session
│       ├── models.py            # SQLAlchemy ORM models
│       ├── schemas.py           # Pydantic request/response schemas
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── boards.py
│       │   ├── columns.py
│       │   ├── cards.py
│       │   ├── tags.py
│       │   └── seo.py
│       └── services/
│           ├── __init__.py
│           ├── board_service.py
│           ├── column_service.py
│           ├── card_service.py
│           ├── tag_service.py
│           └── slug_service.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   ├── public/
│   │   └── vite.svg
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css
│       ├── vite-env.d.ts
│       ├── api/
│       │   └── client.ts         # Axios instance
│       ├── types/
│       │   └── index.ts          # TypeScript interfaces
│       ├── hooks/
│       │   └── useBoards.ts      # Data fetching hooks
│       ├── components/
│       │   ├── Layout.tsx
│       │   ├── Header.tsx
│       │   ├── BoardCard.tsx
│       │   ├── Column.tsx
│       │   ├── CardItem.tsx
│       │   ├── TagBadge.tsx
│       │   ├── EmptyState.tsx
│       │   ├── LoadingSpinner.tsx
│       │   └── ConfirmDialog.tsx
│       └── pages/
│           ├── HomePage.tsx
│           ├── BoardPage.tsx
│           ├── CardDetailPage.tsx
│           └── NotFoundPage.tsx
└── tests/
    ├── test_architecture.py
    └── ...
```

---

## 9. Deployment & Performance

### SQLite Considerations
- **WAL mode** is enabled for concurrent read support.
- Single-writer limitation is acknowledged; this architecture targets small-to-medium team usage.
- Database file is stored in a Docker volume for persistence.

### Caching Strategy
- API responses include `Cache-Control` headers: boards list = 60s, board detail = 30s.
- Static assets use content-hash filenames (Vite default) with far-future `Cache-Control`.

### Production Build
- Frontend: `vite build` produces optimized static assets.
- Backend serves the SPA for non-API routes (or Nginx handles routing).
- Gzip/Brotli compression via Nginx reverse proxy.

### Pre-rendering Considerations
- For SEO, a future enhancement could use a pre-rendering service (e.g., Rendertron) or SSR via a lightweight Node server.
- Current architecture relies on client-side rendering with `react-helmet-async` for dynamic meta tags.
- Search engine crawlers that execute JavaScript (Googlebot) will index content correctly.
