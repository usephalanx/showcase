# Kanban Website — Architecture Plan

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0 (async-compatible, used synchronously with SQLite)
- **Database**: SQLite (file-based, `kanban.db`)
- **Migrations**: Alembic
- **Slug Generation**: python-slugify
- **Validation**: Pydantic v2

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **SEO**: React Helmet Async
- **Styling**: TailwindCSS
- **Drag & Drop**: @dnd-kit/core

## Project Structure

```
/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── database.py          # Engine, session factory, Base
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── main.py               # FastAPI app, lifespan, route includes
│   ├── routers/
│   │   ├── boards.py
│   │   ├── columns.py
│   │   ├── cards.py
│   │   └── categories.py
│   ├── services/
│   │   ├── board_service.py
│   │   ├── column_service.py
│   │   ├── card_service.py
│   │   └── category_service.py
│   ├── utils/
│   │   └── slug.py           # Slug generation with collision handling
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── board/
│   │   │   │   ├── BoardList.tsx
│   │   │   │   ├── BoardCard.tsx
│   │   │   │   ├── BoardDetail.tsx
│   │   │   │   ├── BoardForm.tsx
│   │   │   │   └── BoardEmptyState.tsx
│   │   │   ├── column/
│   │   │   │   ├── ColumnContainer.tsx
│   │   │   │   ├── ColumnHeader.tsx
│   │   │   │   └── ColumnForm.tsx
│   │   │   ├── card/
│   │   │   │   ├── CardItem.tsx
│   │   │   │   ├── CardDetail.tsx
│   │   │   │   ├── CardForm.tsx
│   │   │   │   └── CardModal.tsx
│   │   │   ├── category/
│   │   │   │   ├── CategoryTree.tsx
│   │   │   │   ├── CategoryBadge.tsx
│   │   │   │   └── CategoryFilter.tsx
│   │   │   ├── seo/
│   │   │   │   ├── MetaTags.tsx
│   │   │   │   └── JsonLd.tsx
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── ErrorBoundary.tsx
│   │   │       ├── ConfirmDialog.tsx
│   │   │       └── Breadcrumbs.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── BoardPage.tsx
│   │   │   ├── CardPage.tsx
│   │   │   ├── CategoryPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   ├── hooks/
│   │   │   ├── useBoards.ts
│   │   │   ├── useCards.ts
│   │   │   └── useCategories.ts
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── tests/
│   ├── test_models.py
│   ├── test_database.py
│   ├── test_slug.py
│   └── conftest.py
├── PLANNING.md
├── README.md
└── docker-compose.yml
```

## Data Models

### Board
| Field            | Type         | Constraints                        |
|------------------|--------------|------------------------------------|
| id               | Integer      | PK, autoincrement                  |
| title            | String(255)  | NOT NULL                           |
| slug             | String(280)  | NOT NULL, UNIQUE, indexed          |
| description      | Text         | nullable                           |
| meta_title       | String(255)  | nullable                           |
| meta_description | String(500)  | nullable                           |
| created_at       | DateTime     | NOT NULL, default=utcnow           |
| updated_at       | DateTime     | NOT NULL, default=utcnow, onupdate |

Relationships: `columns` → Column (one-to-many, cascade delete)

### Column
| Field    | Type        | Constraints                        |
|----------|-------------|------------------------------------|
| id       | Integer     | PK, autoincrement                  |
| board_id | Integer     | FK → boards.id, NOT NULL, indexed  |
| title    | String(255) | NOT NULL                           |
| position | Integer     | NOT NULL, default=0                |

Relationships: `board` → Board (many-to-one), `cards` → Card (one-to-many, cascade delete)
Constraints: UniqueConstraint(board_id, position)

### Card
| Field       | Type         | Constraints                        |
|-------------|--------------|------------------------------------|
| id          | Integer      | PK, autoincrement                  |
| column_id   | Integer      | FK → columns.id, NOT NULL, indexed |
| title       | String(255)  | NOT NULL                           |
| description | Text         | nullable                           |
| slug        | String(280)  | NOT NULL, UNIQUE, indexed          |
| position    | Integer      | NOT NULL, default=0                |
| created_at  | DateTime     | NOT NULL, default=utcnow           |
| updated_at  | DateTime     | NOT NULL, default=utcnow, onupdate |

Relationships: `column` → Column (many-to-one), `categories` → Category (many-to-many via CardCategory)

### Category
| Field       | Type         | Constraints                             |
|-------------|--------------|------------------------------------------|
| id          | Integer      | PK, autoincrement                        |
| name        | String(255)  | NOT NULL                                 |
| slug        | String(280)  | NOT NULL, UNIQUE, indexed                |
| description | Text         | nullable                                 |
| parent_id   | Integer      | FK → categories.id, nullable, indexed    |

Relationships: `parent` → Category (self-referential), `children` → Category (one-to-many), `cards` → Card (many-to-many via CardCategory)
Max nesting depth: 5 levels (enforced at application layer)

### CardCategory (Junction Table)
| Field       | Type    | Constraints                          |
|-------------|---------|--------------------------------------|
| card_id     | Integer | FK → cards.id, PK                   |
| category_id | Integer | FK → categories.id, PK              |

Cascade: DELETE on both foreign keys

## API Endpoints

### Boards
- `GET    /api/v1/boards`                    — List all boards
- `POST   /api/v1/boards`                    — Create a board
- `GET    /api/v1/boards/{slug}`             — Get board by slug
- `PUT    /api/v1/boards/{slug}`             — Update board
- `DELETE /api/v1/boards/{slug}`             — Delete board
- `GET    /api/v1/boards/{slug}/columns`     — List columns for a board

### Columns
- `POST   /api/v1/boards/{slug}/columns`    — Create column in board
- `GET    /api/v1/columns/{id}`              — Get column by ID
- `PUT    /api/v1/columns/{id}`              — Update column
- `DELETE /api/v1/columns/{id}`              — Delete column
- `PATCH  /api/v1/columns/{id}/move`         — Reorder column

### Cards
- `GET    /api/v1/columns/{id}/cards`        — List cards in column
- `POST   /api/v1/columns/{id}/cards`        — Create card in column
- `GET    /api/v1/cards/{slug}`              — Get card by slug
- `PUT    /api/v1/cards/{slug}`              — Update card
- `DELETE /api/v1/cards/{slug}`              — Delete card
- `PATCH  /api/v1/cards/{slug}/move`         — Move card to column/position
- `POST   /api/v1/cards/{slug}/categories`   — Add category to card
- `DELETE /api/v1/cards/{slug}/categories/{category_id}` — Remove category

### Categories
- `GET    /api/v1/categories`                — List all (flat or tree)
- `POST   /api/v1/categories`                — Create category
- `GET    /api/v1/categories/{slug}`         — Get category by slug
- `PUT    /api/v1/categories/{slug}`         — Update category
- `DELETE /api/v1/categories/{slug}`         — Delete category
- `GET    /api/v1/categories/{slug}/cards`   — Cards in category

## URL Structure

### Frontend Routes (SEO-friendly)
- `/`                          — Home / board listing
- `/boards/:slug`              — Board detail (Kanban view)
- `/cards/:slug`               — Card detail page
- `/categories`                — Category listing
- `/categories/:slug`          — Category detail with cards

### Canonical URLs
Every page has a `<link rel="canonical">` pointing to its SEO URL.
Slugs are generated from titles using python-slugify with collision appending (-1, -2, etc.).

## Frontend Components

See Project Structure above for the full component tree. Key page-level components:

1. `Layout.tsx` — wrapper with Header, Sidebar, Footer
2. `HomePage.tsx` — board grid with MetaTags
3. `BoardPage.tsx` — Kanban view with drag-and-drop columns/cards
4. `CardPage.tsx` — card detail with categories, breadcrumbs
5. `CategoryPage.tsx` — category tree + filtered cards
6. `NotFoundPage.tsx` — 404 with navigation
7. `MetaTags.tsx` — React Helmet wrapper for per-page meta
8. `JsonLd.tsx` — structured data output
9. `BoardEmptyState.tsx` — shown when board has no columns
10. `CategoryTree.tsx` — recursive tree rendering (max 5 levels displayed)
11. `CardModal.tsx` — quick-view modal for cards
12. `Breadcrumbs.tsx` — navigation breadcrumbs with structured data
13. `ColumnContainer.tsx` — droppable column with card list
14. `CardItem.tsx` — draggable card in column
15. `CategoryBadge.tsx` — pill/badge display of category
16. `ErrorBoundary.tsx` — error boundary wrapper

## Meta Tag Strategy

### Per-Page Titles
- Home: `"Kanban Boards — {AppName}"`
- Board: `"{board.meta_title || board.title} — {AppName}"`
- Card: `"{card.title} — {board.title} — {AppName}"`
- Category: `"{category.name} — Categories — {AppName}"`

### Open Graph Tags
Every page outputs:
- `og:title`, `og:description`, `og:url`, `og:type` (website)
- `og:image` — default fallback to `/og-default.png` if no custom image

### JSON-LD Structured Data
- Board pages: `ItemList` with cards as `ListItem`
- Card pages: `CreativeWork` with category as `about`
- Breadcrumbs: `BreadcrumbList` on every page

### React Helmet Async
Used on every page component to inject `<head>` tags.
For crawlers, React Helmet is sufficient for Google (which renders JS). For social media crawlers, consider adding prerendering middleware later.

### Canonical URLs
Every page includes `<link rel="canonical" href="{full_url}">` via React Helmet.

## State Management

- **Server State**: React Query (TanStack Query) for API data fetching, caching, and invalidation
- **UI State**: React useState/useReducer for local component state
- **Drag & Drop State**: @dnd-kit internal state with optimistic updates
- **Optimistic Updates**: On card move, immediately update UI and send PATCH; on failure, rollback to previous state

## Database Indexes

- `boards.slug` — UNIQUE index
- `boards.created_at` — index for ordering
- `columns.board_id` — index for board lookups
- `columns.(board_id, position)` — unique composite index
- `cards.slug` — UNIQUE index
- `cards.column_id` — index for column lookups
- `cards.created_at` — index for ordering
- `categories.slug` — UNIQUE index
- `categories.parent_id` — index for tree queries
- `card_categories.(card_id, category_id)` — composite PK

## Docker Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - db-data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/kanban.db
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
volumes:
  db-data:
```

## Edge Cases & Decisions

### Slug Collision
When generating a slug, query the database for existing slugs with the same base.
Append `-1`, `-2`, etc. incrementally until a unique slug is found.

### Category Max Depth
Enforced at 5 levels in application code. The API returns 400 if creating a category
that would exceed this depth. The frontend renders up to 5 levels in CategoryTree.

### Cascade Behavior
- Deleting a Board cascades to its Columns and their Cards
- Deleting a Column cascades to its Cards
- Deleting a Card removes CardCategory associations
- Deleting a Category with children: option to reassign children to parent or delete subtree (API parameter)

### Position Strategy
Positions are integer-based. On reorder, affected items are reindexed with position = index * 1000
to leave gaps. If positions run out of gaps, a full reindex of the container is performed.

### Concurrent Editing
Optimistic updates with version checking. Each Card/Column has an `updated_at` timestamp.
On update, if `updated_at` doesn't match the expected value, return 409 Conflict.

### Performance Limits
- Max 100 boards per instance
- Max 20 columns per board
- Max 500 cards per column
- Max 50 categories total
- Enforced at API layer with 422 responses
