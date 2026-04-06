/**
 * Shared TypeScript types for the Todo application.
 *
 * These types mirror the backend Pydantic schemas defined in
 * `backend/app/schemas.py` and provide compile-time safety for
 * all API interactions on the frontend.
 */

/** Valid status values for a task. */
export type StatusType = "todo" | "in-progress" | "done";

/**
 * A persisted task as returned by the API.
 *
 * Maps to the backend `TaskResponse` Pydantic schema.
 */
export interface Task {
  /** Auto-incrementing primary key. */
  id: number;
  /** Short description of the task. */
  title: string;
  /** Current workflow status. */
  status: StatusType;
  /** Optional target completion date (ISO 8601 date string, e.g. "2025-03-15"). */
  due_date: string | null;
  /** Timestamp of row creation (ISO 8601 datetime string). */
  created_at: string;
}

/**
 * Request body for creating a new task.
 *
 * Maps to the backend `TaskCreate` Pydantic schema.
 */
export interface TaskCreate {
  /** Task title (1–255 characters). */
  title: string;
  /** Initial task status. Defaults to "todo" on the backend if omitted. */
  status?: StatusType;
  /** Optional target completion date (ISO 8601 date string). */
  due_date?: string | null;
}

/**
 * Request body for updating an existing task.
 *
 * All fields are optional — only supplied fields are updated (PATCH semantics).
 * Maps to the backend `TaskPatch` Pydantic schema.
 */
export interface TaskUpdate {
  /** Updated task title (1–255 characters). */
  title?: string;
  /** Updated task status. */
  status?: StatusType;
  /** Updated target completion date, or null to clear. */
  due_date?: string | null;
}
