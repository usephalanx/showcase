/**
 * Fetch-based API service module for the Kanban application.
 *
 * All functions communicate with the backend REST API using SEO-friendly
 * slug-based URLs where applicable. The base URL is configurable via
 * the VITE_API_BASE_URL environment variable.
 */

import type {
  Board,
  BoardCreate,
  BoardUpdate,
  Card,
  CardCreate,
  CardMove,
  CardUpdate,
  Category,
  CategoryCreate,
  CategoryUpdate,
  Column,
  ColumnCreate,
  ColumnReorder,
  ColumnUpdate,
  SeoMeta,
} from "./types";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

/** Base URL for all API requests. Defaults to /api/v1 for same-origin. */
const API_BASE_URL: string =
  (typeof import.meta !== "undefined" &&
    (import.meta as Record<string, Record<string, string>>).env
      ?.VITE_API_BASE_URL) ||
  "/api/v1";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Custom error class for API responses with non-OK status codes.
 */
export class ApiError extends Error {
  /** HTTP status code returned by the server. */
  public status: number;
  /** Parsed detail string from the response body, if available. */
  public detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Internal helper that performs a fetch request, checks the response
 * status and returns the parsed JSON body.
 *
 * @param path  - URL path relative to API_BASE_URL (e.g. "/boards").
 * @param options - Standard RequestInit options.
 * @returns Parsed JSON response body of type T.
 * @throws {ApiError} When the response status is not OK.
 */
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${path}`;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      if (body && typeof body.detail === "string") {
        detail = body.detail;
      }
    } catch {
      // Response body is not JSON; use statusText.
    }
    throw new ApiError(response.status, detail);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as unknown as T;
  }

  return response.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Board endpoints
// ---------------------------------------------------------------------------

/**
 * Fetch all boards.
 *
 * @returns A promise resolving to an array of Board objects.
 */
export async function fetchBoards(): Promise<Board[]> {
  return request<Board[]>("/boards");
}

/**
 * Fetch a single board by its SEO-friendly slug.
 *
 * @param slug - The unique URL slug of the board.
 * @returns A promise resolving to the Board (including columns and cards).
 */
export async function fetchBoardBySlug(slug: string): Promise<Board> {
  return request<Board>(`/boards/${encodeURIComponent(slug)}`);
}

/**
 * Create a new board.
 *
 * @param data - Board creation payload.
 * @returns A promise resolving to the newly created Board.
 */
export async function createBoard(data: BoardCreate): Promise<Board> {
  return request<Board>("/boards", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing board identified by slug.
 *
 * @param slug - The unique URL slug of the board to update.
 * @param data - Partial board update payload.
 * @returns A promise resolving to the updated Board.
 */
export async function updateBoard(
  slug: string,
  data: BoardUpdate,
): Promise<Board> {
  return request<Board>(`/boards/${encodeURIComponent(slug)}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

/**
 * Delete a board by its slug.
 *
 * @param slug - The unique URL slug of the board to delete.
 * @returns A promise that resolves when the board is deleted.
 */
export async function deleteBoard(slug: string): Promise<void> {
  return request<void>(`/boards/${encodeURIComponent(slug)}`, {
    method: "DELETE",
  });
}

// ---------------------------------------------------------------------------
// Column endpoints
// ---------------------------------------------------------------------------

/**
 * Fetch all columns for a board identified by slug.
 *
 * @param boardSlug - The slug of the parent board.
 * @returns A promise resolving to an array of Column objects.
 */
export async function fetchColumns(boardSlug: string): Promise<Column[]> {
  return request<Column[]>(
    `/boards/${encodeURIComponent(boardSlug)}/columns`,
  );
}

/**
 * Create a new column within a board.
 *
 * @param boardSlug - The slug of the parent board.
 * @param data      - Column creation payload.
 * @returns A promise resolving to the newly created Column.
 */
export async function createColumn(
  boardSlug: string,
  data: ColumnCreate,
): Promise<Column> {
  return request<Column>(
    `/boards/${encodeURIComponent(boardSlug)}/columns`,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Update an existing column.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the column to update.
 * @param data      - Partial column update payload.
 * @returns A promise resolving to the updated Column.
 */
export async function updateColumn(
  boardSlug: string,
  columnId: number,
  data: ColumnUpdate,
): Promise<Column> {
  return request<Column>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}`,
    {
      method: "PATCH",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Reorder a column within its board.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the column to reorder.
 * @param data      - Reorder payload containing the new position.
 * @returns A promise resolving to the updated Column.
 */
export async function reorderColumn(
  boardSlug: string,
  columnId: number,
  data: ColumnReorder,
): Promise<Column> {
  return request<Column>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}/reorder`,
    {
      method: "PUT",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Delete a column by ID within a board.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the column to delete.
 * @returns A promise that resolves when the column is deleted.
 */
export async function deleteColumn(
  boardSlug: string,
  columnId: number,
): Promise<void> {
  return request<void>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}`,
    {
      method: "DELETE",
    },
  );
}

// ---------------------------------------------------------------------------
// Card endpoints
// ---------------------------------------------------------------------------

/**
 * Fetch all cards for a specific column within a board.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the parent column.
 * @returns A promise resolving to an array of Card objects.
 */
export async function fetchCards(
  boardSlug: string,
  columnId: number,
): Promise<Card[]> {
  return request<Card[]>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}/cards`,
  );
}

/**
 * Create a new card within a column.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the parent column.
 * @param data      - Card creation payload.
 * @returns A promise resolving to the newly created Card.
 */
export async function createCard(
  boardSlug: string,
  columnId: number,
  data: CardCreate,
): Promise<Card> {
  return request<Card>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}/cards`,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Update an existing card.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the column containing the card.
 * @param cardId    - The ID of the card to update.
 * @param data      - Partial card update payload.
 * @returns A promise resolving to the updated Card.
 */
export async function updateCard(
  boardSlug: string,
  columnId: number,
  cardId: number,
  data: CardUpdate,
): Promise<Card> {
  return request<Card>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}/cards/${cardId}`,
    {
      method: "PATCH",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Move a card to a different column and/or reorder it.
 *
 * @param boardSlug - The slug of the parent board.
 * @param cardId    - The ID of the card to move.
 * @param data      - Move payload with target column_id and position.
 * @returns A promise resolving to the updated Card.
 */
export async function moveCard(
  boardSlug: string,
  cardId: number,
  data: CardMove,
): Promise<Card> {
  return request<Card>(
    `/boards/${encodeURIComponent(boardSlug)}/cards/${cardId}/move`,
    {
      method: "PUT",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Delete a card by ID.
 *
 * @param boardSlug - The slug of the parent board.
 * @param columnId  - The ID of the column containing the card.
 * @param cardId    - The ID of the card to delete.
 * @returns A promise that resolves when the card is deleted.
 */
export async function deleteCard(
  boardSlug: string,
  columnId: number,
  cardId: number,
): Promise<void> {
  return request<void>(
    `/boards/${encodeURIComponent(boardSlug)}/columns/${columnId}/cards/${cardId}`,
    {
      method: "DELETE",
    },
  );
}

// ---------------------------------------------------------------------------
// Category endpoints
// ---------------------------------------------------------------------------

/**
 * Fetch all categories.
 *
 * @returns A promise resolving to an array of Category objects.
 */
export async function fetchCategories(): Promise<Category[]> {
  return request<Category[]>("/categories");
}

/**
 * Fetch a single category by its slug.
 *
 * @param slug - The unique URL slug of the category.
 * @returns A promise resolving to the Category.
 */
export async function fetchCategoryBySlug(slug: string): Promise<Category> {
  return request<Category>(`/categories/${encodeURIComponent(slug)}`);
}

/**
 * Create a new category.
 *
 * @param data - Category creation payload.
 * @returns A promise resolving to the newly created Category.
 */
export async function createCategory(data: CategoryCreate): Promise<Category> {
  return request<Category>("/categories", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing category by slug.
 *
 * @param slug - The unique URL slug of the category to update.
 * @param data - Partial category update payload.
 * @returns A promise resolving to the updated Category.
 */
export async function updateCategory(
  slug: string,
  data: CategoryUpdate,
): Promise<Category> {
  return request<Category>(`/categories/${encodeURIComponent(slug)}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

/**
 * Delete a category by slug.
 *
 * @param slug - The unique URL slug of the category to delete.
 * @returns A promise that resolves when the category is deleted.
 */
export async function deleteCategory(slug: string): Promise<void> {
  return request<void>(`/categories/${encodeURIComponent(slug)}`, {
    method: "DELETE",
  });
}

// ---------------------------------------------------------------------------
// SEO Meta endpoint
// ---------------------------------------------------------------------------

/**
 * Fetch SEO metadata for a given resource path.
 *
 * The path corresponds to the frontend route, e.g. "/boards/my-board"
 * or "/categories/engineering".
 *
 * @param resourcePath - The resource path to get SEO metadata for.
 * @returns A promise resolving to a SeoMeta object.
 */
export async function fetchSeoMeta(resourcePath: string): Promise<SeoMeta> {
  const params = new URLSearchParams({ path: resourcePath });
  return request<SeoMeta>(`/seo/meta?${params.toString()}`);
}
