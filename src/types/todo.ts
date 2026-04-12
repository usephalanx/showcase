/**
 * Todo item type definition.
 *
 * Represents a single todo entry persisted in AsyncStorage.
 */
export interface Todo {
  /** Unique identifier for the todo item (UUID string). */
  id: string;

  /** Title / description of the todo item. */
  title: string;

  /** Whether the todo has been completed. */
  completed: boolean;

  /** ISO 8601 date string indicating when the todo was created. */
  createdAt: string;
}
