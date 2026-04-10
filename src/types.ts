/**
 * Core type definitions for the Todo application.
 */

/**
 * Represents a single todo item in the application.
 */
export interface Todo {
  /** Unique identifier for the todo item. */
  id: string;
  /** The text content of the todo item. */
  text: string;
  /** Whether the todo item has been completed. */
  completed: boolean;
}
