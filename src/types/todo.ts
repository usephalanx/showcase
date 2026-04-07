/**
 * Core Todo item interface used throughout the application.
 */
export interface Todo {
  /** Unique identifier for the todo item. */
  id: string;
  /** The display text of the todo item. */
  text: string;
  /** Whether the todo has been completed. */
  completed: boolean;
  /** Timestamp (ms since epoch) when the todo was created. */
  createdAt: number;
}

/**
 * Union type representing the available filter modes for the todo list.
 */
export type FilterType = 'all' | 'active' | 'completed';
