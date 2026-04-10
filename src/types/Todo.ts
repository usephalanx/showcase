/**
 * Represents a single todo item in the application.
 */
export interface Todo {
  /** Unique identifier generated via crypto.randomUUID() */
  id: string;
  /** The text content of the todo */
  text: string;
  /** Whether the todo has been completed */
  completed: boolean;
}
