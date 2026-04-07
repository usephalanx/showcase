/**
 * Core domain types for the Todo application.
 */

/**
 * Represents a single todo item in the application.
 */
export interface Todo {
  /** Unique identifier for the todo. */
  id: string;
  /** The user-facing text content of the todo. */
  text: string;
  /** Whether this todo has been marked as done. */
  completed: boolean;
  /** Unix timestamp (ms) of when the todo was created. */
  createdAt: number;
}

/**
 * The three possible filter states for viewing todos.
 * - 'all': show every todo
 * - 'active': show only incomplete todos
 * - 'completed': show only completed todos
 */
export type TodoFilter = 'all' | 'active' | 'completed';
