/**
 * Pure helper functions for creating, transforming, and filtering Todo items.
 *
 * Every function in this module is side-effect-free (apart from the
 * non-deterministic id/timestamp generation in `generateId` and `createTodo`).
 */

import { Todo, TodoFilter } from '../types/todo';

/**
 * Generate a unique string identifier.
 *
 * Combines the current timestamp (base-36) with a random suffix to
 * produce ids that are practically collision-free for client-side use.
 *
 * @returns A unique string id.
 */
export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 9);
}

/**
 * Create a new Todo from the given text.
 *
 * The returned todo is always incomplete (`completed: false`) and has
 * its `createdAt` set to the current time.
 *
 * @param text - The user-facing content of the todo.
 * @returns A fully populated Todo object.
 */
export function createTodo(text: string): Todo {
  return {
    id: generateId(),
    text,
    completed: false,
    createdAt: Date.now(),
  };
}

/**
 * Return a copy of the given todo with `completed` flipped.
 *
 * The original todo is not mutated.
 *
 * @param todo - The todo to toggle.
 * @returns A new Todo with the opposite completion state.
 */
export function toggleTodo(todo: Todo): Todo {
  return {
    ...todo,
    completed: !todo.completed,
  };
}

/**
 * Return the subset of `todos` that match the given `filter`.
 *
 * - `'all'`       → every todo
 * - `'active'`    → only incomplete todos
 * - `'completed'` → only completed todos
 *
 * The input array is never mutated.
 *
 * @param todos  - The full list of todos. Defaults to an empty array.
 * @param filter - Which subset to return.
 * @returns A (possibly empty) array of matching todos.
 */
export function filterTodos(
  todos: Todo[] = [],
  filter: TodoFilter,
): Todo[] {
  switch (filter) {
    case 'active':
      return todos.filter((todo) => !todo.completed);
    case 'completed':
      return todos.filter((todo) => todo.completed);
    case 'all':
    default:
      return todos;
  }
}
