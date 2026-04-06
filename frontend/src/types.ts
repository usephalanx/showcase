/**
 * TypeScript interfaces matching the backend SQLAlchemy models and API schemas.
 *
 * These types are used throughout the frontend application to ensure
 * type safety when communicating with the Kanban REST API.
 */

// ---------------------------------------------------------------------------
// Category
// ---------------------------------------------------------------------------

/** A hierarchical taxonomy category for cards (self-referential). */
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  parent_id: number | null;
  meta_title: string | null;
  meta_description: string | null;
  created_at: string;
  updated_at: string;
  children?: Category[];
}

/** Payload for creating a new category. */
export interface CategoryCreate {
  name: string;
  description?: string | null;
  parent_id?: number | null;
  meta_title?: string | null;
  meta_description?: string | null;
}

/** Payload for updating an existing category. */
export interface CategoryUpdate {
  name?: string;
  description?: string | null;
  parent_id?: number | null;
  meta_title?: string | null;
  meta_description?: string | null;
}

// ---------------------------------------------------------------------------
// Card
// ---------------------------------------------------------------------------

/** A task card within a column. */
export interface Card {
  id: number;
  column_id: number;
  title: string;
  description: string | null;
  position: number;
  created_at: string;
  updated_at: string;
  categories?: Category[];
}

/** Payload for creating a new card. */
export interface CardCreate {
  title: string;
  description?: string | null;
  position?: number;
  category_ids?: number[];
}

/** Payload for updating an existing card. */
export interface CardUpdate {
  title?: string;
  description?: string | null;
  position?: number;
  category_ids?: number[];
}

/** Payload for moving a card between columns or reordering. */
export interface CardMove {
  column_id: number;
  position: number;
}

// ---------------------------------------------------------------------------
// Column
// ---------------------------------------------------------------------------

/** A column within a Kanban board. */
export interface Column {
  id: number;
  board_id: number;
  title: string;
  position: number;
  created_at?: string;
  updated_at?: string;
  cards?: Card[];
}

/** Payload for creating a new column. */
export interface ColumnCreate {
  title: string;
  position?: number;
}

/** Payload for updating an existing column. */
export interface ColumnUpdate {
  title?: string;
  position?: number;
}

/** Payload for reordering a column within a board. */
export interface ColumnReorder {
  position: number;
}

// ---------------------------------------------------------------------------
// Board
// ---------------------------------------------------------------------------

/** A Kanban board containing columns. */
export interface Board {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  meta_title: string | null;
  meta_description: string | null;
  created_at: string;
  updated_at: string;
  columns?: Column[];
}

/** Payload for creating a new board. */
export interface BoardCreate {
  title: string;
  description?: string | null;
  meta_title?: string | null;
  meta_description?: string | null;
}

/** Payload for updating an existing board. */
export interface BoardUpdate {
  title?: string;
  description?: string | null;
  meta_title?: string | null;
  meta_description?: string | null;
}

// ---------------------------------------------------------------------------
// SEO Meta
// ---------------------------------------------------------------------------

/** SEO metadata returned for a resource. */
export interface SeoMeta {
  title: string;
  description: string;
  canonical_url: string;
  og_title: string;
  og_description: string;
  og_type: string;
  og_url: string;
  og_image: string | null;
  json_ld: Record<string, unknown> | null;
}

// ---------------------------------------------------------------------------
// API Error
// ---------------------------------------------------------------------------

/** Standard error response from the API. */
export interface ApiError {
  detail: string;
}

// ---------------------------------------------------------------------------
// Paginated response (for future use)
// ---------------------------------------------------------------------------

/** A paginated list response. */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
