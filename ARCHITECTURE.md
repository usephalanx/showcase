# Kanban Website Architecture

## 1. Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite via SQLAlchemy 2.0 (synchronous)
- **ORM**: SQLAlchemy with declarative base
- **Validation**: Pydantic v2

### Frontend (Future)
- React 18 + Vite + TypeScript
- react-router v6
- react-helmet-async for SEO meta tags
- TailwindCSS for styling
- @dnd-kit for drag-and-drop

## 2. Data Models

### Board
| Field            | Type     | Constraints                          |
|------------------|----------|--------------------------------------|
| id               | INTEGER  | PK, AUTOINCREMENT                    |
| title            | TEXT     | NOT NULL                             |
| slug             | TEXT     | NOT NULL, UNIQUE, INDEXED            |
| description      | TEXT     | NULLABLE                             |
| meta_title       | TEXT     | NULLABLE (max 70 chars)              |
| meta_description | TEXT     | NULLABLE (max 160 chars)             |
| created_at       | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP  |
| updated_at       | DATETIME | NOT NULL, auto-updated on change     |

### Column
| Field    | Type    | Constraints                          |
|----------|---------|--------------------------------------|
| id       | INTEGER | PK, AUTOINCREMENT                    |
| board_id | INTEGER | FK(boards.id), NOT NULL, ON DELETE CASCADE |
| title    | TEXT    | NOT NULL                             |
| position | INTEGER | NOT NULL, DEFAULT 0                  |

### Card
| Field       | Type     | Constraints                          |
|-------------|----------|--------------------------------------|
| id          | INTEGER  | PK, AUTOINCREMENT                    |
| column_id   | INTEGER  | FK(columns.id), NOT NULL, ON DELETE CASCADE |
| title       | TEXT     | NOT NULL                             |
| description | TEXT     | NULLABLE                             |
| slug        | TEXT     | NOT NULL, UNIQUE, INDEXED (globally) |
| position    | INTEGER  | NOT NULL, DEFAULT 0                  |
| created_at  | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP  |
| updated_at  | DATETIME | NOT NULL, auto-updated on change     |

### Tag
| Field | Type    | Constraints               |
|-------|---------|---------------------------|
| id    | INTEGER | PK, AUTOINCREMENT         |
| name  | TEXT    | NOT NULL                  |
| slug  | TEXT    | NOT NULL, UNIQUE, INDEXED |
| color | TEXT    | NOT NULL, DEFAULT #6b7280 |

### card_tags (Association Table)
| Field   | Type    | Constraints                              |
|---------|---------|------------------------------------------|
| card_id | INTEGER | FK(cards.id), PK, ON DELETE CASCADE      |
| tag_id  | INTEGER | FK(tags.id), PK, ON DELETE CASCADE       |

### Slug Generation Strategy
- Slugs are generated from titles using: lowercase, strip, replace spaces with hyphens, remove non-alphanumeric (except hyphens), collapse consecutive hyphens, strip leading/trailing hyphens.
- On collision, append `-2`, `-3`, etc. incrementally until unique.
- Board slugs are globally unique.
- Card slugs are globally unique (cards have their own URL path `/cards/:slug`).
- Tag slugs are globally unique.

### Card Reordering
- Sequential integer positions starting at 0.
- On move within a column: update positions of affected cards.
- On move across columns: remove from source, insert into target, renumber both.

### Tag Deletion
- CASCADE via association table: deleting a tag removes card_tags rows but does not delete cards.

### SQLite Configuration
- WAL mode enabled for better concurrent read performance.
- Foreign keys enforced via `PRAGMA foreign_keys = ON`.

## 3. API Endpoints

### Boards
- `GET    /api/boards`              — List all boards
- `POST   /api/boards`              — Create board
- `GET    /api/boards/{slug}`       — Get board by slug (with columns and cards)
- `PUT    /api/boards/{slug}`       — Update board
- `DELETE /api/boards/{slug}`       — Delete board

### Columns
- `POST   /api/boards/{slug}/columns`          — Add column to board
- `PUT    /api/columns/{id}`                    — Update column
- `DELETE /api/columns/{id}`                    — Delete column
- `PATCH  /api/columns/{id}/move`               — Reorder column

### Cards
- `POST   /api/columns/{id}/cards`              — Add card to column
- `GET    /api/cards/{slug}`                     — Get card by slug
- `PUT    /api/cards/{slug}`                     — Update card
- `DELETE /api/cards/{slug}`                     — Delete card
- `PATCH  /api/cards/{slug}/move`                — Move card (within/across columns)

### Tags
- `GET    /api/tags`                             — List all tags
- `POST   /api/tags`                             — Create tag
- `PUT    /api/tags/{slug}`                      — Update tag
- `DELETE /api/tags/{slug}`                       — Delete tag
- `POST   /api/cards/{slug}/tags/{tag_id}`       — Attach tag to card
- `DELETE /api/cards/{slug}/tags/{tag_id}`       — Detach tag from card

### SEO
- `GET    /sitemap.xml`                          — Generated sitemap
- `GET    /robots.txt`                           — Robots file

## 4. URL Structure & Routing

- `/`                    — Homepage / board listing
- `/boards/:slug`        — Board detail with columns and cards
- `/cards/:slug`         — Card detail page
- `/tags/:slug`          — Cards filtered by tag
- `/sitemap.xml`         — XML sitemap
- `/robots.txt`          — Robots.txt

## 5. Meta Tag Strategy

- **Board pages**: `<title>{board.meta_title or board.title} | Kanban</title>`
- **Card pages**: `<title>{card.title} | Kanban</title>`
- **Tag pages**: `<title>Cards tagged "{tag.name}" | Kanban</title>`
- **meta_description**: Truncated to 160 characters, from model field or auto-generated.
- **Open Graph**: og:title, og:description, og:type, og:url
- **Canonical URLs**: Always set to the slug-based path.
- **JSON-LD**: Organization + WebPage structured data.

## 6. Frontend Component Tree

```
App
├── Layout
│   ├── Header
│   ├── Outlet (react-router)
│   └── Footer
├── BoardListPage
│   ├── SEOHead
│   ├── BoardCard[]
│   └── EmptyState
├── BoardDetailPage
│   ├── SEOHead
│   ├── BoardHeader
│   ├── ColumnList (DndContext)
│   │   ├── Column[]
│   │   │   ├── ColumnHeader
│   │   │   ├── CardList (SortableContext)
│   │   │   │   ├── CardItem[]
│   │   │   │   └── EmptyColumnState
│   │   │   └── AddCardForm
│   │   └── AddColumnButton
│   └── EmptyBoardState
├── CardDetailPage
│   ├── SEOHead
│   ├── CardContent
│   └── TagList
├── TagPage
│   ├── SEOHead
│   └── CardGrid
└── NotFoundPage
    └── SEOHead
```

## 7. Database Schema DDL

See `models.py` for SQLAlchemy declarative models. Equivalent DDL:

```sql
CREATE TABLE boards (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT    NOT NULL,
    slug             TEXT    NOT NULL UNIQUE,
    description      TEXT,
    meta_title       TEXT,
    meta_description TEXT,
    created_at       DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at       DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE columns (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    board_id INTEGER NOT NULL REFERENCES boards(id) ON DELETE CASCADE,
    title    TEXT    NOT NULL,
    position INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE cards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    column_id   INTEGER NOT NULL REFERENCES columns(id) ON DELETE CASCADE,
    title       TEXT    NOT NULL,
    description TEXT,
    slug        TEXT    NOT NULL UNIQUE,
    position    INTEGER NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at  DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE tags (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL,
    slug  TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL DEFAULT '#6b7280'
);

CREATE TABLE card_tags (
    card_id INTEGER NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (card_id, tag_id)
);
```

## 8. Directory Structure

```
/
├── ARCHITECTURE.md
├── RUNNING.md
├── SETUP.md
├── database.py
├── models.py
├── slug.py
├── main.py
├── tests/
│   ├── test_models.py
│   ├── test_slug.py
│   └── test_database.py
└── static/
    └── index.html
```

## 9. Deployment & Performance

- SQLite WAL mode for concurrent reads.
- Single-writer acknowledged; use connection pooling with `StaticPool` for SQLite.
- Frontend: static pre-rendering for SEO-critical pages (future).
- Caching headers on static assets.
- Meta description auto-truncation to 160 characters.
