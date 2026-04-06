/**
 * TypeScript type definitions for the Todo application.
 *
 * These types mirror the backend Pydantic schemas and database model,
 * ensuring type-safe communication between frontend and API.
 */

/** Allowed status values for a task. */
export type TaskStatus = 'todo' | 'in-progress' | 'done';

/** A task as returned by the API (all fields present). */
export interface Task {
  /** Unique identifier (primary key). */
  id: number;
  /** Short description of the task. */
  title: string;
  /** Current workflow status. */
  status: TaskStatus;
  /** Optional due date in ISO-8601 date format (YYYY-MM-DD), or null. */
  due_date: string | null;
  /** ISO-8601 datetime when the task was created. */
  created_at: string;
  /** ISO-8601 datetime when the task was last updated. */
  updated_at: string;
}

/** Payload for creating a new task. */
export interface TaskCreate {
  /** Short description of the task. */
  title: string;
  /** Initial workflow status. Defaults to 'todo' on the backend if omitted. */
  status?: TaskStatus;
  /** Optional due date in ISO-8601 date format (YYYY-MM-DD). */
  due_date?: string | null;
}

/** Payload for updating an existing task (all fields optional). */
export interface TaskUpdate {
  /** Updated title. */
  title?: string;
  /** Updated workflow status. */
  status?: TaskStatus;
  /** Updated due date, or null to clear it. */
  due_date?: string | null;
}
