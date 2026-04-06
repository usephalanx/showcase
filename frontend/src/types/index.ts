/**
 * TypeScript interfaces matching all backend schemas for the Kanban application.
 *
 * These types mirror the Pydantic models defined on the FastAPI backend and are
 * used throughout the frontend to ensure type-safe API communication.
 */

// ---------------------------------------------------------------------------
// Tag
// ---------------------------------------------------------------------------

/** Tag as returned by the API. */
export interface Tag {
  id: number;
  name: string;
  slug: string;
  color: string;
  created_at: string;
}

/** Request body for creating a new tag. */
export interface TagCreate {
  name: string;
  color?: string;
}

// ---------------------------------------------------------------------------
// Card
// ---------------------------------------------------------------------------

/** Card as returned by the API. */
export interface Card {
  id: number;
  title: string;
  slug: string;
  description: string;
  position: number;
  column_id: number;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

/** Request body for creating a new card. */
export interface CardCreate {
  title: string;
  description?: string;
  column_id: number;
  position?: number;
}

/** Request body for updating an existing card. */
export interface CardUpdate {
  title?: string;
  description?: string;
}

/** Request body for moving a card to a (possibly different) column / position. */
export interface CardMove {
  column_id: number;
  position: number;
}

/** Request body for assigning or removing a tag on a card. */
export interface CardTagAction {
  tag_id: number;
}

// ---------------------------------------------------------------------------
// Column
// ---------------------------------------------------------------------------

/** Column as returned by the API. */
export interface Column {
  id: number;
  title: string;
  position: number;
  board_id: number;
  cards: Card[];
  created_at: string;
  updated_at: string;
}

/** Request body for creating a new column. */
export interface ColumnCreate {
  title: string;
  board_id: number;
  position?: number;
}

/** Request body for updating an existing column. */
export interface ColumnUpdate {
  title?: string;
}

/** Request body for reordering columns within a board. */
export interface ColumnReorder {
  column_ids: number[];
}

// ---------------------------------------------------------------------------
// Board
// ---------------------------------------------------------------------------

/** Board as returned by the API (list view — without nested columns). */
export interface Board {
  id: number;
  name: string;
  slug: string;
  description: string;
  created_at: string;
  updated_at: string;
}

/** Board with fully nested columns (and their cards). */
export interface BoardDetail extends Board {
  columns: Column[];
}

/** Request body for creating a new board. */
export interface BoardCreate {
  name: string;
  description?: string;
}

/** Request body for updating an existing board. */
export interface BoardUpdate {
  name?: string;
  description?: string;
}

// ---------------------------------------------------------------------------
// Generic API response wrappers
// ---------------------------------------------------------------------------

/** Wrapper returned by paginated list endpoints. */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

/** Standard error body returned by the backend. */
export interface ApiError {
  detail: string;
}

/** Generic delete-confirmation response. */
export interface DeleteResponse {
  detail: string;
}
