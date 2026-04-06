/**
 * Tests for TypeScript types defined in src/types.ts.
 *
 * These are compile-time and runtime shape-validation tests that verify
 * the type definitions are correct and usable.
 */

import { describe, it, expect } from "vitest";
import type { Task, TaskCreate, TaskUpdate, StatusType } from "../src/types";

describe("StatusType", () => {
  it("should accept valid status values", () => {
    const statuses: StatusType[] = ["todo", "in-progress", "done"];
    expect(statuses).toHaveLength(3);
    expect(statuses).toContain("todo");
    expect(statuses).toContain("in-progress");
    expect(statuses).toContain("done");
  });
});

describe("Task interface", () => {
  it("should allow construction of a valid Task object", () => {
    const task: Task = {
      id: 1,
      title: "Write tests",
      status: "todo",
      due_date: "2025-12-31",
      created_at: "2025-01-01T00:00:00Z",
    };

    expect(task.id).toBe(1);
    expect(task.title).toBe("Write tests");
    expect(task.status).toBe("todo");
    expect(task.due_date).toBe("2025-12-31");
    expect(task.created_at).toBe("2025-01-01T00:00:00Z");
  });

  it("should allow null due_date", () => {
    const task: Task = {
      id: 2,
      title: "No deadline",
      status: "in-progress",
      due_date: null,
      created_at: "2025-06-15T12:00:00Z",
    };

    expect(task.due_date).toBeNull();
  });

  it("should have all required fields", () => {
    const task: Task = {
      id: 3,
      title: "Check fields",
      status: "done",
      due_date: null,
      created_at: "2025-01-01T00:00:00Z",
    };

    const keys = Object.keys(task);
    expect(keys).toContain("id");
    expect(keys).toContain("title");
    expect(keys).toContain("status");
    expect(keys).toContain("due_date");
    expect(keys).toContain("created_at");
  });
});

describe("TaskCreate interface", () => {
  it("should allow creation with only title", () => {
    const payload: TaskCreate = {
      title: "New task",
    };

    expect(payload.title).toBe("New task");
    expect(payload.status).toBeUndefined();
    expect(payload.due_date).toBeUndefined();
  });

  it("should allow creation with all fields", () => {
    const payload: TaskCreate = {
      title: "Full task",
      status: "in-progress",
      due_date: "2025-06-01",
    };

    expect(payload.title).toBe("Full task");
    expect(payload.status).toBe("in-progress");
    expect(payload.due_date).toBe("2025-06-01");
  });

  it("should allow null due_date explicitly", () => {
    const payload: TaskCreate = {
      title: "Nullable date",
      due_date: null,
    };

    expect(payload.due_date).toBeNull();
  });
});

describe("TaskUpdate interface", () => {
  it("should allow an empty update object", () => {
    const payload: TaskUpdate = {};
    expect(Object.keys(payload)).toHaveLength(0);
  });

  it("should allow partial updates with only title", () => {
    const payload: TaskUpdate = {
      title: "Updated title",
    };

    expect(payload.title).toBe("Updated title");
    expect(payload.status).toBeUndefined();
    expect(payload.due_date).toBeUndefined();
  });

  it("should allow partial updates with only status", () => {
    const payload: TaskUpdate = {
      status: "done",
    };

    expect(payload.status).toBe("done");
  });

  it("should allow setting due_date to null", () => {
    const payload: TaskUpdate = {
      due_date: null,
    };

    expect(payload.due_date).toBeNull();
  });

  it("should allow all fields at once", () => {
    const payload: TaskUpdate = {
      title: "Complete update",
      status: "todo",
      due_date: "2025-12-25",
    };

    expect(payload.title).toBe("Complete update");
    expect(payload.status).toBe("todo");
    expect(payload.due_date).toBe("2025-12-25");
  });
});
