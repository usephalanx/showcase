/**
 * Custom React hook that manages the full todo state.
 *
 * Loads todos from storageService on mount, and exposes addTodo,
 * toggleTodo, and deleteTodo mutations that update both local state
 * and AsyncStorage.
 */
import { useState, useEffect, useCallback } from 'react';
import { Todo } from '../types/Todo';
import { getTodos, saveTodos } from '../services/storageService';

/** Return type for the useTodos hook. */
export interface UseTodosReturn {
  /** The current list of todos. */
  todos: Todo[];
  /** Whether the initial load from storage is in progress. */
  loading: boolean;
  /** Add a new todo with the given title. */
  addTodo: (title: string) => Promise<void>;
  /** Toggle the completed status of the todo with the given id. */
  toggleTodo: (id: string) => Promise<void>;
  /** Delete the todo with the given id. */
  deleteTodo: (id: string) => Promise<void>;
}

/**
 * Hook that manages todo CRUD state backed by AsyncStorage.
 *
 * @returns An object containing the todos array, a loading flag,
 *          and mutation functions (addTodo, toggleTodo, deleteTodo).
 */
export const useTodos = (): UseTodosReturn => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Load todos from storage on mount.
  useEffect(() => {
    let cancelled = false;

    const loadTodos = async (): Promise<void> => {
      try {
        const stored = await getTodos();
        if (!cancelled) {
          setTodos(stored);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadTodos();

    return () => {
      cancelled = true;
    };
  }, []);

  /**
   * Add a new todo item.
   *
   * Trims the title and rejects empty strings. Generates a unique id
   * using Date.now().toString().
   *
   * @param title - The title text for the new todo.
   */
  const addTodo = useCallback(async (title: string): Promise<void> => {
    const trimmed = title.trim();
    if (trimmed.length === 0) {
      return;
    }

    const newTodo: Todo = {
      id: Date.now().toString(),
      title: trimmed,
      completed: false,
      createdAt: new Date().toISOString(),
    };

    const updated = [...todos, newTodo];
    setTodos(updated);
    await saveTodos(updated);
  }, [todos]);

  /**
   * Toggle the completed status of a todo.
   *
   * @param id - The unique identifier of the todo to toggle.
   */
  const toggleTodo = useCallback(async (id: string): Promise<void> => {
    const updated = todos.map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo,
    );
    setTodos(updated);
    await saveTodos(updated);
  }, [todos]);

  /**
   * Delete a todo by its id.
   *
   * @param id - The unique identifier of the todo to delete.
   */
  const deleteTodo = useCallback(async (id: string): Promise<void> => {
    const updated = todos.filter((todo) => todo.id !== id);
    setTodos(updated);
    await saveTodos(updated);
  }, [todos]);

  return { todos, loading, addTodo, toggleTodo, deleteTodo };
};

export default useTodos;
