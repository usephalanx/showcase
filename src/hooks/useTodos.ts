/**
 * useTodos — custom React hook for todo state management.
 *
 * Provides CRUD operations for todos backed by AsyncStorage.
 * Returns the current list of todos, a loading flag, and
 * functions to add, toggle, and delete todos.
 */

import { useCallback, useEffect, useState } from 'react';

import { Todo } from '../types/Todo';
import {
  loadTodos,
  saveTodos,
  generateId,
} from '../services/todoStorage';

/** Return type for the useTodos hook. */
export interface UseTodosReturn {
  /** Current list of todos. */
  todos: Todo[];
  /** True while the initial load from storage is in progress. */
  loading: boolean;
  /** Add a new todo with the given title (trims whitespace, rejects empty). */
  addTodo: (title: string) => Promise<void>;
  /** Toggle the completed status of the todo with the given id. */
  toggleTodo: (id: string) => Promise<void>;
  /** Delete the todo with the given id. */
  deleteTodo: (id: string) => Promise<void>;
}

/**
 * Custom hook that manages todo state with AsyncStorage persistence.
 *
 * On mount it loads persisted todos from AsyncStorage. Every mutation
 * (add / toggle / delete) optimistically updates local state and then
 * persists the new list.
 *
 * @returns An object containing todos, loading state, and mutation functions.
 */
export function useTodos(): UseTodosReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let cancelled = false;

    const init = async () => {
      try {
        const stored = await loadTodos();
        if (!cancelled) {
          setTodos(stored);
        }
      } catch {
        // If loading fails, start with empty list.
        if (!cancelled) {
          setTodos([]);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    init();

    return () => {
      cancelled = true;
    };
  }, []);

  const addTodo = useCallback(async (title: string): Promise<void> => {
    const trimmed = title.trim();
    if (trimmed.length === 0) {
      return;
    }

    const newTodo: Todo = {
      id: generateId(),
      title: trimmed,
      completed: false,
      createdAt: new Date().toISOString(),
    };

    setTodos((prev) => {
      const updated = [newTodo, ...prev];
      saveTodos(updated);
      return updated;
    });
  }, []);

  const toggleTodo = useCallback(async (id: string): Promise<void> => {
    setTodos((prev) => {
      const updated = prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo,
      );
      saveTodos(updated);
      return updated;
    });
  }, []);

  const deleteTodo = useCallback(async (id: string): Promise<void> => {
    setTodos((prev) => {
      const updated = prev.filter((todo) => todo.id !== id);
      saveTodos(updated);
      return updated;
    });
  }, []);

  return { todos, loading, addTodo, toggleTodo, deleteTodo };
}
