/**
 * Tests for the API service module (src/api/tasks.ts).
 *
 * These tests mock axios to verify that each function sends the
 * correct HTTP method, URL, and payload without making real network
 * requests.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import type { AxiosResponse, InternalAxiosRequestConfig, AxiosHeaders } from "axios";

/**
 * Helper to create a minimal AxiosResponse for mocking purposes.
 */
function mockAxiosResponse<T>(data: T, status = 200): AxiosResponse<T> {
  return {
    data,
    status,
    statusText: "OK",
    headers: {},
    config: {
      headers: {} as AxiosHeaders,
    } as InternalAxiosRequestConfig,
  };
}

// We dynamically import the module under test after mocking, so declare
// variables at module scope.
let apiClient: ReturnType<typeof import("axios")["default"]["create"]>;
let getTasks: typeof import("../src/api/tasks").getTasks;
let createTask: typeof import("../src/api/tasks").createTask;
let updateTask: typeof import("../src/api/tasks").updateTask;
let deleteTask: typeof import("../src/api/tasks").deleteTask;

// Mock axios at the module level.
vi.mock("axios", async () => {
  const mockInstance = {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
    put: vi.fn(),
    interceptors: {
      request: { use: vi.fn(), eject: vi.fn(), clear: vi.fn() },
      response: { use: vi.fn(), eject: vi.fn(), clear: vi.fn() },
    },
    defaults: {
      headers: {
        common: {},
        get: {},
        post: {},
        put: {},
        patch: {},
        delete: {},
      },
    },
  };

  return {
    default: {
      create: vi.fn(() => mockInstance),
      isAxiosError: vi.fn(),
    },
    __mockInstance: mockInstance,
  };
});

beforeEach(async () => {
  vi.clearAllMocks();

  // Re-import to get fresh references bound to the mocked axios.
  const axiosMod = await import("axios");
  const mockInstance = (axiosMod as unknown as { __mockInstance: typeof apiClient })
    .__mockInstance;
  apiClient = mockInstance;

  const tasksModule = await import("../src/api/tasks");
  getTasks = tasksModule.getTasks;
  createTask = tasksModule.createTask;
  updateTask = tasksModule.updateTask;
  deleteTask = tasksModule.deleteTask;
});

describe("getTasks", () => {
  it("should call GET /api/tasks and return the data", async () => {
    const mockTasks = [
      {
        id: 1,
        title: "Test task",
        status: "todo" as const,
        due_date: null,
        created_at: "2025-01-01T00:00:00Z",
      },
    ];

    (apiClient.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(mockTasks),
    );

    const result = await getTasks();

    expect(apiClient.get).toHaveBeenCalledWith("/api/tasks");
    expect(apiClient.get).toHaveBeenCalledTimes(1);
    expect(result).toEqual(mockTasks);
  });

  it("should return an empty array when no tasks exist", async () => {
    (apiClient.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse([]),
    );

    const result = await getTasks();

    expect(result).toEqual([]);
  });

  it("should propagate errors from the API", async () => {
    const error = new Error("Network Error");
    (apiClient.get as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    await expect(getTasks()).rejects.toThrow("Network Error");
  });
});

describe("createTask", () => {
  it("should call POST /api/tasks with the payload and return created task", async () => {
    const payload = { title: "New task" };
    const created = {
      id: 1,
      title: "New task",
      status: "todo" as const,
      due_date: null,
      created_at: "2025-01-01T00:00:00Z",
    };

    (apiClient.post as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(created, 201),
    );

    const result = await createTask(payload);

    expect(apiClient.post).toHaveBeenCalledWith("/api/tasks", payload);
    expect(apiClient.post).toHaveBeenCalledTimes(1);
    expect(result).toEqual(created);
  });

  it("should send optional fields when provided", async () => {
    const payload = {
      title: "Full task",
      status: "in-progress" as const,
      due_date: "2025-12-31",
    };
    const created = {
      id: 2,
      title: "Full task",
      status: "in-progress" as const,
      due_date: "2025-12-31",
      created_at: "2025-01-01T00:00:00Z",
    };

    (apiClient.post as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(created, 201),
    );

    const result = await createTask(payload);

    expect(apiClient.post).toHaveBeenCalledWith("/api/tasks", payload);
    expect(result.status).toBe("in-progress");
    expect(result.due_date).toBe("2025-12-31");
  });

  it("should propagate validation errors", async () => {
    const error = new Error("Request failed with status code 422");
    (apiClient.post as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    await expect(createTask({ title: "" })).rejects.toThrow("422");
  });
});

describe("updateTask", () => {
  it("should call PATCH /api/tasks/:id with the payload", async () => {
    const updatePayload = { title: "Updated title" };
    const updated = {
      id: 5,
      title: "Updated title",
      status: "todo" as const,
      due_date: null,
      created_at: "2025-01-01T00:00:00Z",
    };

    (apiClient.patch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(updated),
    );

    const result = await updateTask(5, updatePayload);

    expect(apiClient.patch).toHaveBeenCalledWith("/api/tasks/5", updatePayload);
    expect(apiClient.patch).toHaveBeenCalledTimes(1);
    expect(result).toEqual(updated);
  });

  it("should handle status-only updates", async () => {
    const updatePayload = { status: "done" as const };
    const updated = {
      id: 3,
      title: "Existing",
      status: "done" as const,
      due_date: null,
      created_at: "2025-01-01T00:00:00Z",
    };

    (apiClient.patch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(updated),
    );

    const result = await updateTask(3, updatePayload);

    expect(apiClient.patch).toHaveBeenCalledWith("/api/tasks/3", updatePayload);
    expect(result.status).toBe("done");
  });

  it("should propagate 404 errors for non-existent tasks", async () => {
    const error = new Error("Request failed with status code 404");
    (apiClient.patch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    await expect(updateTask(999, { title: "Nope" })).rejects.toThrow("404");
  });
});

describe("deleteTask", () => {
  it("should call DELETE /api/tasks/:id", async () => {
    (apiClient.delete as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse({ detail: "Task deleted successfully" }),
    );

    await deleteTask(7);

    expect(apiClient.delete).toHaveBeenCalledWith("/api/tasks/7");
    expect(apiClient.delete).toHaveBeenCalledTimes(1);
  });

  it("should return void on success", async () => {
    (apiClient.delete as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockAxiosResponse(null, 204),
    );

    const result = await deleteTask(1);

    expect(result).toBeUndefined();
  });

  it("should propagate 404 errors for non-existent tasks", async () => {
    const error = new Error("Request failed with status code 404");
    (apiClient.delete as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    await expect(deleteTask(999)).rejects.toThrow("404");
  });
});
