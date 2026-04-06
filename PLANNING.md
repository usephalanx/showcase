# Kanban Website with SEO & Taxonomy — Architecture Plan

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite via SQLAlchemy 2.0 (async with aiosqlite)
- **ORM**: SQLAlchemy with Alembic for migrations
- **Validation**: Pydantic v2 schemas
- **Server**: Uvicorn (ASGI)
- **Testing**: pytest + httpx (async test client)

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Routing**: React Router DOM v6
- **SEO**: React Helmet Async (per-page meta tags, Open Graph, JSON-LD structured data)
- **Drag & Drop**: @dnd-kit/core + @dnd-kit/sortable
- **State Management**: React Context + useReducer for board state; React Query (TanStack Query) for server state
- **Styling**: CSS Modules (no external UI library)
- **Testing**: Vitest + React Testing Library

### DevOps
- **Containerization**: Docker + Docker Compose
- **Proxy**: Vite dev server proxies `/api` to FastAPI backend
- **Linting**: ESLint + Prettier (frontend), Ruff (backend)

## Project Structure

```
/
├── PLANNING.md
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── board.py
│   │   │   ├── column.py
│   │   │   ├── card.py
│   │   │   ├── category.py
│   │   │   └── tag.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── board.py
│   │   │   ├── column.py
│   │   │   ├── card.py
│   │   │   ├── category.py
│   │   │   └── tag.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── boards.py
│   │   │   ├── columns.py
│   │   │   ├── cards.py
│   │   │   ├── categories.py
│   │   │   └── tags.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── board_service.py
│   │   │   ├── column_service.py
│   │   │   ├── card_service.py
│   │   │   ├── category_service.py
│   │   │   └── tag_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── slug.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_boards.py
│       ├── test_columns.py
│       ├── test_cards.py
│       ├── test_categories.py
│       └── test_tags.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── public/
│   │   ├── favicon.ico
│   │   └── og-default.png
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── App.module.css
│       ├── vite-env.d.ts
│       ├── types/
│       │   ├── index.ts
│       │   ├── board.ts
│       │   ├── column.ts
│       │   ├── card.ts
│       │   ├── category.ts
│       │   └── tag.ts
│       ├── api/
│       │   ├── client.ts
│       │   ├── boards.ts
│       │   ├── columns.ts
│       │   ├── cards.ts
│       │   ├── categories.ts
│       │   └── tags.ts
│       ├── hooks/
│       │   ├── useBoards.ts
│       │   ├── useBoard.ts
│       │   ├── useCards.ts
│       │   ├── useCategories.ts
│       │   └── useTags.ts
│       ├── context/
│       │   ├── BoardContext.tsx
│       │   └── ThemeContext.tsx
│       ├── pages/
│       │   ├── HomePage.tsx
│       │   ├── BoardPage.tsx
│       │   ├── BoardListPage.tsx
│       │   ├── CategoryPage.tsx
│       │   ├── CategoryListPage.tsx
│       │   ├── TagPage.tsx
│       │   ├── TagListPage.tsx
│       │   └── NotFoundPage.tsx
│       ├── components/
│       │   ├── layout/
│       │   │   ├── Header.tsx
│       │   │   ├── Footer.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   └── PageLayout.tsx
│       │   ├── board/
│       │   │   ├── BoardCard.tsx
│       │   │   ├── BoardForm.tsx
│       │   │   ├── BoardHeader.tsx
│       │   │   └── BoardEmptyState.tsx
│       │   ├── column/
│       │   │   ├── Column.tsx
│       │   │   ├── ColumnHeader.tsx
│       │   │   ├── ColumnForm.tsx
│       │   │   └── ColumnList.tsx
│       │   ├── card/
│       │   │   ├── Card.tsx
│       │   │   ├── CardDetail.tsx
│       │   │   ├── CardForm.tsx
│       │   │   └── CardList.tsx
│       │   ├── category/
│       │   │   ├── CategoryTree.tsx
│       │   │   ├── CategoryBadge.tsx
│       │   │   └── CategoryForm.tsx
│       │   ├── tag/
│       │   │   ├── TagBadge.tsx
│       │   │   ├── TagList.tsx
│       │   │   └── TagForm.tsx
│       │   ├── seo/
│       │   │   ├── SEOHead.tsx
│       │   │   └── JsonLd.tsx
│       │   └── common/
│       │       ├── Button.tsx
│       │       ├── Modal.tsx
│       │       ├── ConfirmDialog.tsx
│       │       ├── LoadingSpinner.tsx
│       │       ├── ErrorBoundary.tsx
│       │       └── EmptyState.tsx
│       └── utils/
│           ├── slug.ts
│           ├── constants.ts
│           └── helpers.ts
└── scripts/
    └── validate_planning.py
```

## Data Models

### Board
| Field        | Type         | Constraints                          |
|-------------|-------------|--------------------------------------|
| id          | Integer     | Primary Key, Auto-increment          |
| title       | String(255) | NOT NULL                             |
| slug        | String(280) | NOT NULL, UNIQUE, INDEX              |
| description | Text        | nullable                             |
| position    | Integer     | NOT NULL, DEFAULT 0                  |
| created_at  | DateTime    | NOT NULL, DEFAULT utcnow             |
| updated_at  | DateTime    | NOT NULL, DEFAULT utcnow, ON UPDATE  |

Relationships:
- `columns`: One-to-Many → Column (cascade delete)

### Column
| Field      | Type         | Constraints                          |
|-----------|-------------|--------------------------------------|
| id        | Integer     | Primary Key, Auto-increment          |
| board_id  | Integer     | Foreign Key → boards.id, NOT NULL    |
| title     | String(255) | NOT NULL                             |
| position  | Float       | NOT NULL, DEFAULT 0                  |
| color     | String(7)   | nullable (hex color, e.g., #FF5733)  |
| created_at| DateTime    | NOT NULL, DEFAULT utcnow             |
| updated_at| DateTime    | NOT NULL, DEFAULT utcnow, ON UPDATE  |

Relationships:
- `board`: Many-to-One → Board
- `cards`: One-to-Many → Card (cascade delete)

Note on `position` as Float: We use fractional positioning for efficient drag-and-drop reordering. When a column is moved between two others with positions 1.0 and 2.0, its new position becomes 1.5. Reindexing (normalizing back to integers) occurs when the gap between adjacent positions falls below 0.001.

### Card
| Field       | Type         | Constraints                          |
|------------|-------------|--------------------------------------|
| id         | Integer     | Primary Key, Auto-increment          |
| column_id  | Integer     | Foreign Key → columns.id, NOT NULL   |
| category_id| Integer     | Foreign Key → categories.id, nullable|
| title      | String(255) | NOT NULL                             |
| slug       | String(280) | NOT NULL, UNIQUE, INDEX              |
| description| Text        | nullable                             |
| position   | Float       | NOT NULL, DEFAULT 0                  |
| priority   | String(20)  | nullable (low, medium, high, urgent) |
| due_date   | DateTime    | nullable                             |
| created_at | DateTime    | NOT NULL, DEFAULT utcnow             |
| updated_at | DateTime    | NOT NULL, DEFAULT utcnow, ON UPDATE  |

Relationships:
- `column`: Many-to-One → Column
- `category`: Many-to-One → Category (SET NULL on delete)
- `tags`: Many-to-Many → Tag (via card_tags association table)

### Category
| Field      | Type         | Constraints                          |
|-----------|-------------|--------------------------------------|
| id        | Integer     | Primary Key, Auto-increment          |
| parent_id | Integer     | Foreign Key → categories.id, nullable|
| name      | String(255) | NOT NULL                             |
| slug      | String(280) | NOT NULL, UNIQUE, INDEX              |
| description| Text        | nullable                             |
| color     | String(7)   | nullable (hex color)                 |
| created_at| DateTime    | NOT NULL, DEFAULT utcnow             |
| updated_at| DateTime    | NOT NULL, DEFAULT utcnow, ON UPDATE  |

Relationships:
- `parent`: Many-to-One → Category (self-referential)
- `children`: One-to-Many → Category (cascade delete)
- `cards`: One-to-Many → Card

Max nesting depth: 5 levels. Enforced at the API/service layer, not database. When creating/updating a category with a parent_id, the service walks up the parent chain and rejects if depth exceeds 5.

### Tag
| Field      | Type         | Constraints                          |
|-----------|-------------|--------------------------------------|
| id        | Integer     | Primary Key, Auto-increment          |
| name      | String(100) | NOT NULL, UNIQUE                     |
| slug      | String(120) | NOT NULL, UNIQUE, INDEX              |
| color     | String(7)   | nullable (hex color)                 |
| created_at| DateTime    | NOT NULL, DEFAULT utcnow             |

Relationships:
- `cards`: Many-to-Many → Card (via card_tags association table)

### card_tags (Association Table)
| Field   | Type    | Constraints                       |
|--------|---------|-----------------------------------|
| card_id| Integer | Foreign Key → cards.id, PK        |
| tag_id | Integer | Foreign Key → tags.id, PK         |

Composite primary key on (card_id, tag_id). CASCADE delete on both foreign keys.

## API Endpoints

All endpoints are prefixed with `/api/v1`.

### Boards
| Method | Path                         | Description                  | Status Codes     |
|--------|------------------------------|------------------------------|------------------|
| GET    | /api/v1/boards               | List all boards              | 200              |
| POST   | /api/v1/boards               | Create a new board           | 201, 422         |
| GET    | /api/v1/boards/{board_slug}  | Get board by slug            | 200, 404         |
| PUT    | /api/v1/boards/{board_slug}  | Update board                 | 200, 404, 422    |
| DELETE | /api/v1/boards/{board_slug}  | Delete board + cascades      | 204, 404         |
| PATCH  | /api/v1/boards/reorder       | Reorder boards               | 200, 422         |

### Columns
| Method | Path                                              | Description                  | Status Codes     |
|--------|---------------------------------------------------|------------------------------|------------------|
| GET    | /api/v1/boards/{board_slug}/columns               | List columns for board       | 200, 404         |
| POST   | /api/v1/boards/{board_slug}/columns               | Create column in board       | 201, 404, 422    |
| GET    | /api/v1/boards/{board_slug}/columns/{column_id}   | Get column by ID             | 200, 404         |
| PUT    | /api/v1/boards/{board_slug}/columns/{column_id}   | Update column                | 200, 404, 422    |
| DELETE | /api/v1/boards/{board_slug}/columns/{column_id}   | Delete column + cascade cards| 204, 404         |
| PATCH  | /api/v1/boards/{board_slug}/columns/reorder       | Reorder columns              | 200, 422         |

### Cards
| Method | Path                                              | Description                          | Status Codes     |
|--------|---------------------------------------------------|--------------------------------------|------------------|
| GET    | /api/v1/cards                                     | List all cards (with filters)        | 200              |
| POST   | /api/v1/columns/{column_id}/cards                 | Create card in column                | 201, 404, 422    |
| GET    | /api/v1/cards/{card_slug}                         | Get card by slug                     | 200, 404         |
| PUT    | /api/v1/cards/{card_slug}                         | Update card                          | 200, 404, 422    |
| DELETE | /api/v1/cards/{card_slug}                         | Delete card                          | 204, 404         |
| PATCH  | /api/v1/cards/{card_slug}/move                    | Move card to another column          | 200, 404, 422    |
| PATCH  | /api/v1/columns/{column_id}/cards/reorder         | Reorder cards within column          | 200, 422         |
| POST   | /api/v1/cards/{card_slug}/tags/{tag_id}           | Add tag to card                      | 200, 404         |
| DELETE | /api/v1/cards/{card_slug}/tags/{tag_id}           | Remove tag from card                 | 200, 404         |

### Categories
| Method | Path                                    | Description                          | Status Codes     |
|--------|-----------------------------------------|--------------------------------------|------------------|
| GET    | /api/v1/categories                      | List categories (flat or tree)       | 200              |
| POST   | /api/v1/categories                      | Create category                      | 201, 422         |
| GET    | /api/v1/categories/{category_slug}      | Get category by slug                 | 200, 404         |
| PUT    | /api/v1/categories/{category_slug}      | Update category                      | 200, 404, 422    |
| DELETE | /api/v1/categories/{category_slug}      | Delete category (children cascade)   | 204, 404         |
| GET    | /api/v1/categories/{category_slug}/cards| List cards in category               | 200, 404         |

### Tags
| Method | Path                          | Description                  | Status Codes     |
|--------|-------------------------------|------------------------------|------------------|
| GET    | /api/v1/tags                  | List all tags                | 200              |
| POST   | /api/v1/tags                  | Create tag                   | 201, 422         |
| GET    | /api/v1/tags/{tag_slug}       | Get tag by slug              | 200, 404         |
| PUT    | /api/v1/tags/{tag_slug}       | Update tag                   | 200, 404, 422    |
| DELETE | /api/v1/tags/{tag_slug}       | Delete tag                   | 204, 404         |
| GET    | /api/v1/tags/{tag_slug}/cards | List cards with tag          | 200, 404         |

**Total: 26 API endpoints**

### Query Parameters (for GET list endpoints)
- `?search=<term>` — full-text search on title/description
- `?category=<slug>` — filter by category
- `?tag=<slug>` — filter by tag
- `?priority=<level>` — filter by priority
- `?sort=<field>` — sort by field (created_at, updated_at, position, title)
- `?order=asc|desc` — sort direction
- `?page=<n>&per_page=<n>` — pagination (default: page=1, per_page=50)

### Request/Response Schema Examples

**POST /api/v1/boards — Request:**
```json
{
  "title": "Sprint 42",
  "description": "Two-week sprint starting Jan 15"
}
```

**POST /api/v1/boards — Response (201):**
```json
{
  "id": 1,
  "title": "Sprint 42",
  "slug": "sprint-42",
  "description": "Two-week sprint starting Jan 15",
  "position": 0,
  "created_at": "2024-01-15T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z",
  "columns": []
}
```

**PATCH /api/v1/cards/{card_slug}/move — Request:**
```json
{
  "target_column_id": 5,
  "position": 2.5
}
```

## URL Structure

### Frontend Routes (SEO-friendly)
| Route                        | Page Component      | Description                      |
|------------------------------|---------------------|----------------------------------|
| `/`                          | HomePage            | Landing page, featured boards    |
| `/boards`                    | BoardListPage       | List of all boards               |
| `/boards/:boardSlug`         | BoardPage           | Kanban board view                |
| `/categories`                | CategoryListPage    | List/tree of categories          |
| `/categories/:categorySlug`  | CategoryPage        | Category detail with cards       |
| `/tags`                      | TagListPage         | List of all tags                 |
| `/tags/:tagSlug`             | TagPage             | Tag detail with cards            |
| `*`                          | NotFoundPage        | 404 page                         |

### Canonical URL Strategy
- Every page sets a `<link rel="canonical">` via React Helmet
- Board pages: `https://domain.com/boards/sprint-42`
- Card detail modals use the board URL as canonical (cards don't have standalone pages)
- Categories: `https://domain.com/categories/engineering`
- Tags: `https://domain.com/tags/frontend`

## Frontend Components

Complete component file listing with their paths:

1. `src/App.tsx` — Root application component with route definitions
2. `src/main.tsx` — Entry point with BrowserRouter, HelmetProvider
3. `src/pages/HomePage.tsx` — Landing page with board overview
4. `src/pages/BoardPage.tsx` — Full kanban board view
5. `src/pages/BoardListPage.tsx` — Grid/list of all boards
6. `src/pages/CategoryPage.tsx` — Category detail page
7. `src/pages/CategoryListPage.tsx` — Category tree/list page
8. `src/pages/TagPage.tsx` — Tag detail with associated cards
9. `src/pages/TagListPage.tsx` — All tags overview
10. `src/pages/NotFoundPage.tsx` — 404 error page
11. `src/components/layout/Header.tsx` — Top navigation bar
12. `src/components/layout/Footer.tsx` — Site footer
13. `src/components/layout/Sidebar.tsx` — Category/tag navigation sidebar
14. `src/components/layout/PageLayout.tsx` — Shared page layout wrapper
15. `src/components/board/BoardCard.tsx` — Board preview card for list views
16. `src/components/board/BoardForm.tsx` — Create/edit board form
17. `src/components/board/BoardHeader.tsx` — Board page header with title/actions
18. `src/components/board/BoardEmptyState.tsx` — Empty board placeholder
19. `src/components/column/Column.tsx` — Single column container (droppable)
20. `src/components/column/ColumnHeader.tsx` — Column title bar with actions
21. `src/components/column/ColumnForm.tsx` — Create/edit column form
22. `src/components/column/ColumnList.tsx` — Horizontal column layout (sortable)
23. `src/components/card/Card.tsx` — Single card (draggable)
24. `src/components/card/CardDetail.tsx` — Card detail modal/panel
25. `src/components/card/CardForm.tsx` — Create/edit card form
26. `src/components/card/CardList.tsx` — Vertical card list within column
27. `src/components/category/CategoryTree.tsx` — Recursive category tree
28. `src/components/category/CategoryBadge.tsx` — Inline category label
29. `src/components/category/CategoryForm.tsx` — Create/edit category form
30. `src/components/tag/TagBadge.tsx` — Inline tag pill/chip
31. `src/components/tag/TagList.tsx` — Horizontal tag list
32. `src/components/tag/TagForm.tsx` — Create/edit tag form
33. `src/components/seo/SEOHead.tsx` — Reusable Helmet wrapper for meta tags
34. `src/components/seo/JsonLd.tsx` — JSON-LD structured data injector
35. `src/components/common/Button.tsx` — Reusable button component
36. `src/components/common/Modal.tsx` — Modal dialog
37. `src/components/common/ConfirmDialog.tsx` — Confirmation dialog
38. `src/components/common/LoadingSpinner.tsx` — Loading indicator
39. `src/components/common/ErrorBoundary.tsx` — React error boundary
40. `src/components/common/EmptyState.tsx` — Generic empty state placeholder

### Component Props Interfaces (Key Components)

```typescript
interface SEOHeadProps {
  title: string;
  description?: string;
  canonicalUrl?: string;
  ogType?: 'website' | 'article';
  ogImage?: string;
  jsonLd?: Record<string, unknown>;
}

interface ColumnProps {
  column: ColumnType;
  boardSlug: string;
  onCardMove: (cardId: number, targetColumnId: number, position: number) => void;
  onCardCreate: (columnId: number, data: CardCreateInput) => void;
}

interface CardProps {
  card: CardType;
  isDragging?: boolean;
  onClick: (card: CardType) => void;
}

interface CategoryTreeProps {
  categories: CategoryType[];
  selectedSlug?: string;
  maxDepth?: number; // default: 5
  onSelect: (category: CategoryType) => void;
}

interface BoardFormProps {
  initialData?: BoardType;
  onSubmit: (data: BoardCreateInput | BoardUpdateInput) => void;
  onCancel: () => void;
}
```

## Meta Tag Strategy

### Per-Page Title Templates
- **Home**: `Kanban Board — Organize Your Projects`
- **Board List**: `All Boards — Kanban Board`
- **Board Detail**: `{board.title} — Kanban Board`
- **Category List**: `Categories — Kanban Board`
- **Category Detail**: `{category.name} — Categories — Kanban Board`
- **Tag List**: `Tags — Kanban Board`
- **Tag Detail**: `{tag.name} — Tags — Kanban Board`
- **404**: `Page Not Found — Kanban Board`

### Open Graph Tags
Every page includes:
```html
<meta property="og:title" content="{page title}" />
<meta property="og:description" content="{page description}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical URL}" />
<meta property="og:image" content="{og image or default}" />
<meta property="og:site_name" content="Kanban Board" />
```

Default `og:image` falls back to `/og-default.png` (a branded 1200×630 image stored in `public/`).

### Canonical URLs
Every page sets `<link rel="canonical" href="{full URL}" />` via React Helmet Async.

### Description Generation
- **Board**: First 160 characters of `board.description`, or auto-generated: `"Kanban board '{board.title}' with {columnCount} columns and {cardCount} cards."`
- **Category**: First 160 characters of `category.description`, or `"Browse {cardCount} cards in the {category.name} category."`
- **Tag**: `"Cards tagged with '{tag.name}' — {cardCount} cards."`

### JSON-LD Structured Data

Board pages emit `CollectionPage` structured data:
```json
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Sprint 42",
  "description": "Two-week sprint starting Jan 15",
  "url": "https://domain.com/boards/sprint-42",
  "numberOfItems": 24,
  "dateCreated": "2024-01-15T00:00:00Z",
  "dateModified": "2024-01-20T12:00:00Z"
}
```

Category pages emit `ItemList` structured data for cards within the category.

### SEO for Client-Side Rendering
Since this is an SPA rendered with React, we rely on React Helmet Async for meta tag injection. Modern search engine crawlers (Googlebot, Bingbot) execute JavaScript and can read Helmet-injected tags. For social media crawlers (Facebook, Twitter) that may not execute JS, we document a future enhancement path:
- **Phase 1 (current)**: React Helmet Async — sufficient for Google/Bing indexing
- **Phase 2 (future)**: Optional prerendering via `prerender-spa-plugin` or a lightweight SSR proxy for social media previews

## State Management

### Server State (TanStack Query / React Query)
- All API data fetched and cached via React Query
- Query keys follow convention: `['boards']`, `['boards', slug]`, `['boards', slug, 'columns']`, etc.
- Stale time: 30 seconds for lists, 60 seconds for detail views
- Mutations use `useMutation` with optimistic updates and rollback on error

### Client State (React Context + useReducer)
- **BoardContext**: Manages the currently viewed board state, drag-and-drop state, active card selection
- **ThemeContext**: Light/dark mode preference (persisted to localStorage)

### Drag-and-Drop State Management
- @dnd-kit provides drag state management internally
- On drag end, the handler:
  1. Computes new position using fractional positioning (average of neighbors)
  2. Optimistically updates local state
  3. Fires API mutation (PATCH reorder or move endpoint)
  4. On error, rolls back to previous state via React Query cache invalidation

### Optimistic Update Conflict Resolution
- Each entity includes an `updated_at` timestamp
- On PUT/PATCH, the client sends `If-Unmodified-Since` header with last known `updated_at`
- Server returns 409 Conflict if the entity was modified since that timestamp
- Client shows a conflict dialog: "This item was modified by another session. Reload to see changes?"

## Database Indexes

### boards
- PRIMARY KEY on `id`
- UNIQUE INDEX on `slug`
- INDEX on `position` (for ordered listing)

### columns
- PRIMARY KEY on `id`
- INDEX on `board_id` (foreign key lookups)
- COMPOSITE INDEX on `(board_id, position)` (ordered column listing per board)

### cards
- PRIMARY KEY on `id`
- UNIQUE INDEX on `slug`
- INDEX on `column_id` (foreign key lookups)
- INDEX on `category_id` (category filtering)
- COMPOSITE INDEX on `(column_id, position)` (ordered card listing per column)
- INDEX on `priority` (priority filtering)
- INDEX on `due_date` (due date filtering/sorting)
- INDEX on `created_at` (date sorting)

### categories
- PRIMARY KEY on `id`
- UNIQUE INDEX on `slug`
- INDEX on `parent_id` (tree traversal)

### tags
- PRIMARY KEY on `id`
- UNIQUE INDEX on `slug`
- UNIQUE INDEX on `name`

### card_tags
- COMPOSITE PRIMARY KEY on `(card_id, tag_id)`
- INDEX on `tag_id` (reverse lookups: cards by tag)

## Slug Generation Strategy

Slugs are auto-generated from the `title` (or `name` for categories/tags) field:

1. Convert to lowercase
2. Replace spaces and special characters with hyphens
3. Remove consecutive hyphens
4. Trim leading/trailing hyphens
5. Truncate to 255 characters

### Collision Handling
When a slug already exists in the database:
1. Append `-1` to the slug
2. If `-1` exists, try `-2`, `-3`, etc.
3. Query: `SELECT slug FROM {table} WHERE slug LIKE '{base_slug}%'`
4. Find highest existing suffix number, use next

Example: `sprint-42`, `sprint-42-1`, `sprint-42-2`

Slugs are regenerated on title update. Old slugs are NOT preserved (no redirect table in v1).

## Cascade Behaviors

| Parent Deleted | Child Behavior                                    |
|---------------|---------------------------------------------------|
| Board         | All columns deleted → all cards in those columns deleted → card_tags entries deleted |
| Column        | All cards in column deleted → card_tags entries deleted |
| Card          | card_tags entries deleted                          |
| Category      | Children categories deleted (recursive cascade). Cards in deleted category: category_id SET NULL |
| Tag           | card_tags entries for this tag deleted. Cards themselves are NOT deleted |

## Performance Limits

| Resource               | Maximum | Enforcement       |
|-----------------------|---------|--------------------|
| Boards                | 100     | API validation     |
| Columns per board     | 20      | API validation     |
| Cards per column      | 500     | API validation     |
| Cards per board       | 5000    | API validation     |
| Categories (total)    | 500     | API validation     |
| Category nesting depth| 5       | Service layer      |
| Tags (total)          | 1000    | API validation     |
| Tags per card         | 20      | API validation     |
| Title length          | 255     | Schema validation  |
| Description length    | 10000   | Schema validation  |

## Docker Setup

### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - sqlite-data:/app/data
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./data/kanban.db
      - CORS_ORIGINS=http://localhost:5173

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend/src:/app/src
    depends_on:
      - backend

volumes:
  sqlite-data:
```

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Frontend Dockerfile
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "run", "dev", "--", "--host"]
```

### Production Considerations
- Frontend built as static files (`npm run build`) and served via Nginx or from FastAPI's StaticFiles
- SQLite suitable for single-server deployment; for multi-server, migrate to PostgreSQL
- Environment variables for all configuration (no hardcoded secrets)
- Health check endpoint: `GET /api/v1/health` → `{"status": "ok"}`
