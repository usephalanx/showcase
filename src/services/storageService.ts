/**
 * AsyncStorage-based persistence service for Todo items.
 *
 * Provides functions to load and save the full todo list,
 * handling JSON serialization/deserialization with error handling.
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Todo } from '../types/todo';

/** Key used to store the todo list in AsyncStorage. */
const TODOS_STORAGE_KEY = 'TODOS_STORAGE_KEY';

/**
 * Retrieve all todos from AsyncStorage.
 *
 * Reads the JSON string stored under TODOS_STORAGE_KEY, deserializes it,
 * and returns the resulting array. Returns an empty array when no data
 * has been stored yet or when deserialization fails.
 *
 * @returns A promise that resolves to an array of Todo items.
 */
export async function getTodos(): Promise<Todo[]> {
  try {
    const json: string | null = await AsyncStorage.getItem(TODOS_STORAGE_KEY);
    if (json === null) {
      return [];
    }
    const parsed: unknown = JSON.parse(json);
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed as Todo[];
  } catch (error) {
    console.error('storageService.getTodos: failed to load todos', error);
    return [];
  }
}

/**
 * Persist the given todo list to AsyncStorage.
 *
 * Serializes the array to JSON and writes it under TODOS_STORAGE_KEY.
 * Logs an error to the console if the write fails.
 *
 * @param todos - The complete array of Todo items to persist.
 * @returns A promise that resolves when the data has been saved.
 */
export async function saveTodos(todos: Todo[]): Promise<void> {
  try {
    const json: string = JSON.stringify(todos);
    await AsyncStorage.setItem(TODOS_STORAGE_KEY, json);
  } catch (error) {
    console.error('storageService.saveTodos: failed to save todos', error);
  }
}
