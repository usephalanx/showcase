/**
 * Core Todo data model used throughout the application.
 */
export interface Todo {
  /** Unique identifier for the todo item. */
  id: string;
  /** The text content of the todo item. */
  text: string;
  /** Whether the todo item has been completed. */
  completed: boolean;
}
