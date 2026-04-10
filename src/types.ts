/**
 * Core type definitions for the Mini React Todo App.
 */

/**
 * Represents a single Todo item.
 */
export interface Todo {
  /** Unique identifier generated via crypto.randomUUID(). */
  id: string;

  /** The text description of the todo item. */
  text: string;

  /** Whether the todo item has been completed. */
  completed: boolean;
}
