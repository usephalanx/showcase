/**
 * Represents a single todo item in the application.
 */
export interface Todo {
  /** Unique identifier generated via Date.now().toString(). */
  id: string;
  /** The title/text of the todo item. */
  title: string;
  /** Whether the todo has been completed. */
  completed: boolean;
  /** ISO 8601 timestamp of when the todo was created. */
  createdAt: string;
}
