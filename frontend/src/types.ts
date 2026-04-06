/**
 * Represents a task in the Todo application.
 *
 * Maps to the backend Task model returned by the API.
 */
export interface Task {
  /** Unique identifier for the task. */
  id: number;

  /** Short summary of the task. */
  title: string;

  /** Current status of the task. */
  status: 'pending' | 'in_progress' | 'completed';

  /** Optional deadline for the task (ISO-8601 date string or null). */
  due_date: string | null;
}
