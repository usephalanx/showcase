import type { Todo, FilterType } from '../types/todo';

/**
 * Generate a unique identifier string.
 *
 * Uses `crypto.randomUUID()` when available (modern browsers / Node 19+),
 * falling back to a timestamp + random-number approach.
 *
 * @returns A unique string suitable for use as a Todo id.
 */
export function generateId(): string {
  if (
    typeof crypto !== 'undefined' &&
    typeof crypto.randomUUID === 'function'
  ) {
    return crypto.randomUUID();
  }
  // Fallback for environments without crypto.randomUUID
  return `${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Create a new Todo object from the given text.
 *
 * The new todo is incomplete by default and stamped with the current time.
 *
 * @param text - The display text for the todo. Will be trimmed.
 * @returns A fully-formed Todo object.
 * @throws {Error} If text is empty or whitespace-only after trimming.
 */
export function createTodo(text: string): Todo {
  const trimmed = text.trim();
  if (trimmed.length === 0) {
    throw new Error('Todo text must not be empty');
  }
  return {
    id: generateId(),
    text: trimmed,
    completed: false,
    createdAt: Date.now(),
  };
}

/**
 * Return a new Todo with the `completed` field toggled.
 *
 * This is a pure function — the original todo is not mutated.
 *
 * @param todo - The todo to toggle.
 * @returns A new Todo object with `completed` flipped.
 */
export function toggleTodo(todo: Todo): Todo {
  return { ...todo, completed: !todo.completed };
}

/**
 * Filter an array of todos by the given filter type.
 *
 * - `'all'`       → returns every todo.
 * - `'active'`    → returns only todos where `completed` is `false`.
 * - `'completed'` → returns only todos where `completed` is `true`.
 *
 * This is a pure function — the original array is not mutated.
 *
 * @param todos  - The full list of todos.  Defaults to `[]` if not provided.
 * @param filter - The filter mode to apply.  Defaults to `'all'`.
 * @returns A new array containing only the matching todos.
 */
export function filterTodos(
  todos: Todo[] = [],
  filter: FilterType = 'all',
): Todo[] {
  switch (filter) {
    case 'active':
      return todos.filter((todo) => !todo.completed);
    case 'completed':
      return todos.filter((todo) => todo.completed);
    case 'all':
    default:
      return [...todos];
  }
}
