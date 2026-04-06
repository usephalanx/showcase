/**
 * Tests for the API service module (src/api.ts).
 *
 * Uses a mocked global fetch to verify correct URL construction,
 * HTTP methods, request bodies, and error handling for every
 * API function.
 */

import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  fetchBoards,
  fetchBoardBySlug,
  createBoard,
  updateBoard,
  deleteBoard,
  fetchColumns,
  createColumn,
  updateColumn,
  reorderColumn,
  deleteColumn,
  fetchCards,
  createCard,
  updateCard,
  moveCard,
  deleteCard,
  fetchCategories,
  fetchCategoryBySlug,
  createCategory,
  updateCategory,
  deleteCategory,
  fetchSeoMeta,
  ApiError,
} from "../src/api";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Create a minimal successful Response mock. */
function mockResponse(body: unknown, status = 200): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    statusText: status === 200 ? "OK" : "Error",
    json: () => Promise.resolve(body),
    headers: new Headers(),
    redirected: false,
    type: "basic" as ResponseType,
    url: "",
    clone: () => mockResponse(body, status) as Response,
    body: null,
    bodyUsed: false,
    arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
    blob: () => Promise.resolve(new Blob()),
    formData: () => Promise.resolve(new FormData()),
    text: () => Promise.resolve(JSON.stringify(body)),
    bytes: () => Promise.resolve(new Uint8Array()),
  } as Response;
}

function mock204Response(): Response {
  return {
    ok: true,
    status: 204,
    statusText: "No Content",
    json: () => Promise.reject(new Error("No body")),
    headers: new Headers(),
    redirected: false,
    type: "basic" as ResponseType,
    url: "",
    clone: () => mock204Response() as Response,
    body: null,
    bodyUsed: false,
    arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
    blob: () => Promise.resolve(new Blob()),
    formData: () => Promise.resolve(new FormData()),
    text: () => Promise.resolve(""),
    bytes: () => Promise.resolve(new Uint8Array()),
  } as Response;
}

// ---------------------------------------------------------------------------
// Setup
// ---------------------------------------------------------------------------

beforeEach(() => {
  vi.restoreAllMocks();
});

// ---------------------------------------------------------------------------
// Board tests
// ---------------------------------------------------------------------------

describe("Board API", () => {
  it("fetchBoards sends GET to /boards", async () => {
    const boards = [{ id: 1, title: "Test", slug: "test" }];
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(boards));

    const result = await fetchBoards();

    expect(spy).toHaveBeenCalledTimes(1);
    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards");
    expect(opts?.method).toBeUndefined(); // GET is default
    expect(result).toEqual(boards);
  });

  it("fetchBoardBySlug sends GET to /boards/:slug", async () => {
    const board = { id: 1, title: "Test", slug: "my-board" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(board));

    const result = await fetchBoardBySlug("my-board");

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board");
    expect(result).toEqual(board);
  });

  it("fetchBoardBySlug encodes special characters in slug", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse({}));

    await fetchBoardBySlug("slug with spaces");

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/slug%20with%20spaces");
  });

  it("createBoard sends POST with body", async () => {
    const created = { id: 1, title: "New Board", slug: "new-board" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(created));

    const payload = { title: "New Board", description: "A description" };
    const result = await createBoard(payload);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards");
    expect(opts?.method).toBe("POST");
    expect(JSON.parse(opts?.body as string)).toEqual(payload);
    expect(result).toEqual(created);
  });

  it("updateBoard sends PATCH to /boards/:slug", async () => {
    const updated = { id: 1, title: "Updated", slug: "my-board" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(updated));

    const payload = { title: "Updated" };
    const result = await updateBoard("my-board", payload);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board");
    expect(opts?.method).toBe("PATCH");
    expect(JSON.parse(opts?.body as string)).toEqual(payload);
    expect(result).toEqual(updated);
  });

  it("deleteBoard sends DELETE to /boards/:slug", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mock204Response());

    await deleteBoard("my-board");

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board");
    expect(opts?.method).toBe("DELETE");
  });
});

// ---------------------------------------------------------------------------
// Column tests
// ---------------------------------------------------------------------------

describe("Column API", () => {
  it("fetchColumns sends GET to /boards/:slug/columns", async () => {
    const columns = [{ id: 1, board_id: 1, title: "Todo", position: 0 }];
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(columns));

    const result = await fetchColumns("my-board");

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns");
    expect(result).toEqual(columns);
  });

  it("createColumn sends POST to /boards/:slug/columns", async () => {
    const column = { id: 2, board_id: 1, title: "In Progress", position: 1 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(column));

    const payload = { title: "In Progress", position: 1 };
    const result = await createColumn("my-board", payload);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns");
    expect(opts?.method).toBe("POST");
    expect(JSON.parse(opts?.body as string)).toEqual(payload);
    expect(result).toEqual(column);
  });

  it("updateColumn sends PATCH to /boards/:slug/columns/:id", async () => {
    const column = { id: 1, board_id: 1, title: "Done", position: 0 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(column));

    const result = await updateColumn("my-board", 1, { title: "Done" });

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/1");
    expect(opts?.method).toBe("PATCH");
    expect(result).toEqual(column);
  });

  it("reorderColumn sends PUT to /boards/:slug/columns/:id/reorder", async () => {
    const column = { id: 1, board_id: 1, title: "Todo", position: 2 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(column));

    const result = await reorderColumn("my-board", 1, { position: 2 });

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/1/reorder");
    expect(opts?.method).toBe("PUT");
    expect(JSON.parse(opts?.body as string)).toEqual({ position: 2 });
    expect(result).toEqual(column);
  });

  it("deleteColumn sends DELETE to /boards/:slug/columns/:id", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mock204Response());

    await deleteColumn("my-board", 3);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/3");
    expect(opts?.method).toBe("DELETE");
  });
});

// ---------------------------------------------------------------------------
// Card tests
// ---------------------------------------------------------------------------

describe("Card API", () => {
  it("fetchCards sends GET to /boards/:slug/columns/:id/cards", async () => {
    const cards = [{ id: 1, column_id: 1, title: "Task", position: 0 }];
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(cards));

    const result = await fetchCards("my-board", 1);

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/1/cards");
    expect(result).toEqual(cards);
  });

  it("createCard sends POST with body", async () => {
    const card = { id: 1, column_id: 1, title: "New Task", position: 0 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(card));

    const payload = { title: "New Task" };
    const result = await createCard("my-board", 1, payload);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/1/cards");
    expect(opts?.method).toBe("POST");
    expect(JSON.parse(opts?.body as string)).toEqual(payload);
    expect(result).toEqual(card);
  });

  it("updateCard sends PATCH to /boards/:slug/columns/:colId/cards/:cardId", async () => {
    const card = { id: 5, column_id: 2, title: "Updated", position: 1 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(card));

    const result = await updateCard("my-board", 2, 5, { title: "Updated" });

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/2/cards/5");
    expect(opts?.method).toBe("PATCH");
    expect(result).toEqual(card);
  });

  it("moveCard sends PUT to /boards/:slug/cards/:id/move", async () => {
    const card = { id: 5, column_id: 3, title: "Moved", position: 0 };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(card));

    const moveData = { column_id: 3, position: 0 };
    const result = await moveCard("my-board", 5, moveData);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/cards/5/move");
    expect(opts?.method).toBe("PUT");
    expect(JSON.parse(opts?.body as string)).toEqual(moveData);
    expect(result).toEqual(card);
  });

  it("deleteCard sends DELETE to /boards/:slug/columns/:colId/cards/:cardId", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mock204Response());

    await deleteCard("my-board", 2, 10);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/boards/my-board/columns/2/cards/10");
    expect(opts?.method).toBe("DELETE");
  });
});

// ---------------------------------------------------------------------------
// Category tests
// ---------------------------------------------------------------------------

describe("Category API", () => {
  it("fetchCategories sends GET to /categories", async () => {
    const categories = [{ id: 1, name: "Dev", slug: "dev" }];
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(categories));

    const result = await fetchCategories();

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/categories");
    expect(result).toEqual(categories);
  });

  it("fetchCategoryBySlug sends GET to /categories/:slug", async () => {
    const cat = { id: 1, name: "Dev", slug: "dev" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(cat));

    const result = await fetchCategoryBySlug("dev");

    const [url] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/categories/dev");
    expect(result).toEqual(cat);
  });

  it("createCategory sends POST with body", async () => {
    const cat = { id: 2, name: "Design", slug: "design" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(cat));

    const payload = { name: "Design" };
    const result = await createCategory(payload);

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/categories");
    expect(opts?.method).toBe("POST");
    expect(JSON.parse(opts?.body as string)).toEqual(payload);
    expect(result).toEqual(cat);
  });

  it("updateCategory sends PATCH to /categories/:slug", async () => {
    const cat = { id: 1, name: "Development", slug: "dev" };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(cat));

    const result = await updateCategory("dev", { name: "Development" });

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/categories/dev");
    expect(opts?.method).toBe("PATCH");
    expect(result).toEqual(cat);
  });

  it("deleteCategory sends DELETE to /categories/:slug", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mock204Response());

    await deleteCategory("dev");

    const [url, opts] = spy.mock.calls[0];
    expect(url).toBe("/api/v1/categories/dev");
    expect(opts?.method).toBe("DELETE");
  });
});

// ---------------------------------------------------------------------------
// SEO Meta tests
// ---------------------------------------------------------------------------

describe("SEO Meta API", () => {
  it("fetchSeoMeta sends GET to /seo/meta with path query param", async () => {
    const meta = {
      title: "My Board",
      description: "Board description",
      canonical_url: "/boards/my-board",
      og_title: "My Board",
      og_description: "Board description",
      og_type: "website",
      og_url: "/boards/my-board",
      og_image: null,
      json_ld: null,
    };
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse(meta));

    const result = await fetchSeoMeta("/boards/my-board");

    const [url] = spy.mock.calls[0];
    expect(url).toContain("/api/v1/seo/meta");
    expect(url).toContain("path=%2Fboards%2Fmy-board");
    expect(result).toEqual(meta);
  });
});

// ---------------------------------------------------------------------------
// Error handling tests
// ---------------------------------------------------------------------------

describe("API Error Handling", () => {
  it("throws ApiError on 404 response with detail", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      mockResponse({ detail: "Board not found" }, 404),
    );

    await expect(fetchBoardBySlug("nonexistent")).rejects.toThrow(ApiError);
    await expect(fetchBoardBySlug("nonexistent")).rejects.toThrow(
      "Board not found",
    );
  });

  it("throws ApiError on 500 response without JSON body", async () => {
    const response = {
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
      json: () => Promise.reject(new Error("No JSON")),
      headers: new Headers(),
      redirected: false,
      type: "basic" as ResponseType,
      url: "",
      clone: () => response as Response,
      body: null,
      bodyUsed: false,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
      blob: () => Promise.resolve(new Blob()),
      formData: () => Promise.resolve(new FormData()),
      text: () => Promise.resolve(""),
      bytes: () => Promise.resolve(new Uint8Array()),
    } as Response;

    vi.spyOn(globalThis, "fetch").mockResolvedValue(response);

    try {
      await fetchBoards();
      expect.fail("Should have thrown");
    } catch (err) {
      expect(err).toBeInstanceOf(ApiError);
      expect((err as ApiError).status).toBe(500);
      expect((err as ApiError).detail).toBe("Internal Server Error");
    }
  });

  it("ApiError has correct properties", () => {
    const error = new ApiError(422, "Validation failed");
    expect(error.name).toBe("ApiError");
    expect(error.status).toBe(422);
    expect(error.detail).toBe("Validation failed");
    expect(error.message).toBe("Validation failed");
    expect(error).toBeInstanceOf(Error);
  });
});

// ---------------------------------------------------------------------------
// Content-Type header tests
// ---------------------------------------------------------------------------

describe("Request headers", () => {
  it("always sends Content-Type: application/json", async () => {
    const spy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse([]));

    await fetchBoards();

    const [, opts] = spy.mock.calls[0];
    expect((opts?.headers as Record<string, string>)["Content-Type"]).toBe(
      "application/json",
    );
  });
});
