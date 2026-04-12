/**
 * todoStorage — AsyncStorage-backed persistence for todo items.
 *
 * Provides functions to load, save, and generate IDs for todos.
 * Uses @react-native-async-storage/async-storage as the storage backend.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

import { Todo } from '../types/Todo';

/** AsyncStorage key for the persisted todo list. */
const STORAGE_KEY = '@todos';

/**
 * Load all todos from AsyncStorage.
 *
 * @returns A promise that resolves to the array of saved todos,
 *          or an empty array if nothing is stored.
 */
export async function loadTodos(): Promise<Todo[]> {
  const json = await AsyncStorage.getItem(STORAGE_KEY);
  if (json === null) {
    return [];
  }
  try {
    const parsed = JSON.parse(json);
    if (Array.isArray(parsed)) {
      return parsed as Todo[];
    }
    return [];
  } catch {
    return [];
  }
}

/**
 * Save the full todo list to AsyncStorage.
 *
 * @param todos - The complete array of todos to persist.
 */
export async function saveTodos(todos: Todo[]): Promise<void> {
  const json = JSON.stringify(todos);
  await AsyncStorage.setItem(STORAGE_KEY, json);
}

/**
 * Generate a unique ID string suitable for use as a todo identifier.
 *
 * Uses a combination of timestamp and random hex characters to produce
 * a reasonably unique identifier without requiring external dependencies.
 *
 * @returns A unique string identifier.
 */
export function generateId(): string {
  const timestamp = Date.now().toString(36);
  const randomPart = Math.random().toString(36).substring(2, 10);
  return `${timestamp}-${randomPart}`;
}
