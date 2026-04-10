/**
 * Core Todo item type used throughout the application.
 */
export interface Todo {
  /** Unique identifier generated via crypto.randomUUID(). */
  id: string;
  /** The text content of the todo item. */
  text: string;
  /** Whether the todo has been completed. */
  completed: boolean;
}
