/**
 * Core Todo data model used throughout the application.
 */
export interface Todo {
  /** Unique identifier (UUID). */
  id: string;
  /** Title text of the todo item. */
  title: string;
  /** Whether the todo has been completed. */
  completed: boolean;
  /** ISO 8601 timestamp of when the todo was created. */
  createdAt: string;
}
