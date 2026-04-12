/**
 * Storage service for persisting todos to AsyncStorage.
 *
 * Provides getTodos and saveTodos functions that serialise/deserialise
 * the todo list as JSON under a single AsyncStorage key.
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Todo } from '../types/Todo';

const STORAGE_KEY = '@todos';

/**
 * Load all todos from AsyncStorage.
 *
 * @returns A promise that resolves to an array of Todo items.
 *          Returns an empty array when no data is stored or on error.
 */
export const getTodos = async (): Promise<Todo[]> => {
  try {
    const json = await AsyncStorage.getItem(STORAGE_KEY);
    if (json !== null) {
      return JSON.parse(json) as Todo[];
    }
    return [];
  } catch {
    return [];
  }
};

/**
 * Persist the full todo list to AsyncStorage.
 *
 * @param todos - The complete array of Todo items to save.
 */
export const saveTodos = async (todos: Todo[]): Promise<void> => {
  try {
    const json = JSON.stringify(todos);
    await AsyncStorage.setItem(STORAGE_KEY, json);
  } catch {
    // Silently fail — callers can add error handling if needed.
  }
};
