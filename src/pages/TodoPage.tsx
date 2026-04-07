/**
 * TodoPage – main page component for the Todo application.
 *
 * Manages the full todo lifecycle: adding, toggling, deleting, and
 * filtering todo items.  State is persisted to localStorage when
 * available, with a graceful fallback to in-memory state.
 *
 * This is a self-contained page component. Presentational sub-components
 * (TodoInput, TodoList, TodoItem, TodoFilter) will be extracted in a
 * subsequent task; for now all rendering lives here to ensure the app
 * compiles and runs end-to-end.
 */
import React, { useState, useEffect, useCallback } from 'react';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Represents a single todo item. */
interface Todo {
  /** Unique identifier (crypto.randomUUID or fallback). */
  id: string;
  /** User-supplied text for the todo. */
  text: string;
  /** Whether the todo has been completed. */
  completed: boolean;
  /** Unix-epoch millisecond timestamp of creation. */
  createdAt: number;
}

/** The three possible filter states. */
type FilterType = 'all' | 'active' | 'completed';

// ---------------------------------------------------------------------------
// localStorage helpers
// ---------------------------------------------------------------------------

const STORAGE_KEY = 'todo-app-todos';

/**
 * Attempt to read todos from localStorage.
 *
 * Returns the parsed array on success, or `null` when localStorage is
 * unavailable or the stored value is unparseable.
 */
function loadTodos(): Todo[] | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw === null) return null;
    const parsed: unknown = JSON.parse(raw);
    if (Array.isArray(parsed)) return parsed as Todo[];
    return null;
  } catch {
    return null;
  }
}

/**
 * Persist the given todos array to localStorage.
 *
 * Silently ignores errors (e.g. quota exceeded in private browsing).
 */
function saveTodos(todos: Todo[]): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
  } catch {
    // Graceful fallback – state remains in memory only.
  }
}

// ---------------------------------------------------------------------------
// ID generation helper
// ---------------------------------------------------------------------------

/**
 * Generate a unique id string.
 *
 * Uses `crypto.randomUUID()` when available (modern browsers), falling
 * back to a simple timestamp + random suffix.
 */
function generateId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
}

// ---------------------------------------------------------------------------
// TodoPage component
// ---------------------------------------------------------------------------

/**
 * TodoPage is the top-level page that assembles the entire Todo UI.
 *
 * It owns the `todos` and `filter` state and will eventually delegate
 * rendering to extracted child components.
 */
const TodoPage: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>(() => loadTodos() ?? []);
  const [filter, setFilter] = useState<FilterType>('all');
  const [inputValue, setInputValue] = useState<string>('');

  // Persist todos to localStorage whenever they change.
  useEffect(() => {
    saveTodos(todos);
  }, [todos]);

  // -- Handlers -------------------------------------------------------------

  /** Add a new todo. Trims whitespace and rejects empty strings. */
  const handleAdd = useCallback(() => {
    const trimmed = inputValue.trim();
    if (trimmed.length === 0) return;

    const newTodo: Todo = {
      id: generateId(),
      text: trimmed,
      completed: false,
      createdAt: Date.now(),
    };

    // Prepend – most recent first.
    setTodos((prev) => [newTodo, ...prev]);
    setInputValue('');
  }, [inputValue]);

  /** Toggle the completed flag of a todo by id. */
  const handleToggle = useCallback((id: string) => {
    setTodos((prev) =>
      prev.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t)),
    );
  }, []);

  /** Delete a todo by id. */
  const handleDelete = useCallback((id: string) => {
    setTodos((prev) => prev.filter((t) => t.id !== id));
  }, []);

  /** Handle Enter key in the input field. */
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') handleAdd();
    },
    [handleAdd],
  );

  // -- Derived data ---------------------------------------------------------

  const filteredTodos: Todo[] = todos.filter((t) => {
    if (filter === 'active') return !t.completed;
    if (filter === 'completed') return t.completed;
    return true;
  });

  const activeTodoCount: number = todos.filter((t) => !t.completed).length;
  const completedTodoCount: number = todos.filter((t) => t.completed).length;

  // -- Render ---------------------------------------------------------------

  const filters: FilterType[] = ['all', 'active', 'completed'];

  return (
    <div className="todo-page">
      <h1>Todo App</h1>

      {/* Input */}
      <div className="todo-input">
        <input
          type="text"
          placeholder="What needs to be done?"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="New todo text"
        />
        <button type="button" onClick={handleAdd}>
          Add
        </button>
      </div>

      {/* Filters */}
      <div className="todo-filters" role="group" aria-label="Filter todos">
        {filters.map((f) => (
          <button
            key={f}
            type="button"
            className={filter === f ? 'active' : ''}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
        <span className="todo-counts">
          {activeTodoCount} active / {completedTodoCount} completed
        </span>
      </div>

      {/* List */}
      <ul className="todo-list">
        {filteredTodos.length === 0 ? (
          <li className="empty-message">No todos to show.</li>
        ) : (
          filteredTodos.map((todo) => (
            <li key={todo.id} className={todo.completed ? 'completed' : ''}>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggle(todo.id)}
                aria-label={`Toggle ${todo.text}`}
              />
              <span
                style={{
                  textDecoration: todo.completed ? 'line-through' : 'none',
                }}
              >
                {todo.text}
              </span>
              <button
                type="button"
                onClick={() => handleDelete(todo.id)}
                aria-label={`Delete ${todo.text}`}
              >
                Delete
              </button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default TodoPage;
