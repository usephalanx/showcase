# Architecture — React Todo Application

## Overview

A single-page Todo application built with React, TypeScript, and Vite.
State is managed locally via React hooks with optional `localStorage`
persistence. There is no backend dependency for the frontend — it runs
entirely in the browser.

---

## File Structure

```
src/
├── main.tsx                        # Entry point — mounts <App />
├── App.tsx                         # Root shell — renders <TodoPage />
├── index.css                       # Global reset & base styles
├── setupTests.ts                   # Vitest / jest-dom setup
├── types/
│   └── todo.ts                     # Todo interface & FilterType
├── hooks/
│   ├── useTodos.ts                 # Core todo state + CRUD operations
│   ├── useLocalStorage.ts          # Generic localStorage hook
│   └── __tests__/
│       └── useTodos.test.ts        # Unit tests for useTodos
├── components/
│   ├── TodoItem.tsx                # Single todo row
│   ├── TodoInput.tsx               # New-todo text input + add button
│   ├── TodoList.tsx                # Renders list of TodoItem (or empty state)
│   ├── TodoFilter.tsx              # Filter buttons (all / active / completed)
│   └── __tests__/
│       ├── TodoItem.test.tsx        # TodoItem unit tests
│       ├── TodoInput.test.tsx       # TodoInput unit tests
│       ├── TodoList.test.tsx        # TodoList unit tests
│       └── TodoFilter.test.tsx      # TodoFilter unit tests
└── pages/
    ├── TodoPage.tsx                # Main page assembler
    └── __tests__/
        └── TodoPage.test.tsx       # Integration test for full flow
```

---

## Data Model

### `Todo` Interface

```typescript
export interface Todo {
  /** Unique identifier generated via crypto.randomUUID(). */
  id: string;
  /** The todo item text content. */
  text: string;
  /** Whether the todo has been completed. */
  completed: boolean;
  /** Unix-epoch timestamp (ms) when the todo was created. */
  createdAt: number;
}
```

### `FilterType`

```typescript
export type FilterType = 'all' | 'active' | 'completed';
```

---

## Component Tree

```
<App>
  └── <TodoPage>
        ├── <TodoInput onAdd={addTodo} />
        ├── <TodoFilter
        │     currentFilter={filter}
        │     onFilterChange={setFilter}
        │     counts={{ all, active, completed }}
        │   />
        └── <TodoList
              todos={filteredTodos}
              onToggle={toggleTodo}
              onDelete={deleteTodo}
            />
              └── <TodoItem
                    todo={todo}
                    onToggle={onToggle}
                    onDelete={onDelete}
                  /> (× N)
```

---

## Component Props Interfaces

### `TodoInput`

```typescript
export interface TodoInputProps {
  /** Callback invoked with trimmed text when the user submits a new todo. */
  onAdd: (text: string) => void;
}
```

**Behaviour:**
- Trims whitespace before submission.
- Rejects empty strings (does not call `onAdd`).
- Clears the input field after successful submission.
- Submits on Enter key press or button click.

### `TodoItem`

```typescript
export interface TodoItemProps {
  /** The todo to render. */
  todo: Todo;
  /** Callback invoked with the todo id when the checkbox is toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo id when the delete button is clicked. */
  onDelete: (id: string) => void;
}
```

**Behaviour:**
- Completed todos display text with a line-through style.
- Checkbox reflects `todo.completed`.

### `TodoList`

```typescript
export interface TodoListProps {
  /** Array of todos to display. Defaults to []. */
  todos?: Todo[];
  /** Callback forwarded to each TodoItem for toggling. */
  onToggle: (id: string) => void;
  /** Callback forwarded to each TodoItem for deletion. */
  onDelete: (id: string) => void;
}
```

**Behaviour:**
- When `todos` is empty, renders a friendly empty-state message: "No todos yet. Add one above!"
- Maps over `todos` (defaulting to `[]`) and renders a `<TodoItem>` for each.

### `TodoFilter`

```typescript
export interface FilterCounts {
  all: number;
  active: number;
  completed: number;
}

export interface TodoFilterProps {
  /** The currently selected filter. */
  currentFilter: FilterType;
  /** Callback invoked when the user selects a different filter. */
  onFilterChange: (filter: FilterType) => void;
  /** Count of todos in each category. */
  counts: FilterCounts;
}
```

**Behaviour:**
- Renders three buttons: All, Active, Completed.
- Visually highlights the active filter button.
- Displays count next to each label.

---

## State Management

### `useTodos` Hook

```typescript
interface UseTodosReturn {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

function useTodos(): UseTodosReturn;
```

**Implementation details:**
- Stores todos in `useState<Todo[]>`.
- Persists to `localStorage` via `useLocalStorage` hook.
- `addTodo` **prepends** new todos (most recent first).
- Uses `crypto.randomUUID()` for id generation.

### `useLocalStorage` Hook

```typescript
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void];
```

**Edge cases:**
- If `localStorage.getItem` throws (private browsing, quota exceeded), falls back to `initialValue`.
- If `localStorage.setItem` throws, state still updates in-memory (logs warning to console).
- Parses stored JSON; falls back to `initialValue` on parse errors.

---

## Data Flow

1. `TodoPage` calls `useTodos()` to get `todos` and mutation functions.
2. `TodoPage` manages `filter` state via `useState<FilterType>('all')`.
3. `TodoPage` derives `filteredTodos` from `todos` + `filter`.
4. `TodoPage` computes `counts` for `TodoFilter`.
5. Child components receive data and callbacks via props — no prop drilling beyond one level.

---

## Styling Approach

- Plain CSS in `src/index.css` (global styles) plus component-level CSS as needed.
- No CSS-in-JS library — keeps dependencies minimal.
- Responsive layout with max-width container centered on the page.

---

## Test Strategy

| File | Key Tests |
|---|---|
| `TodoItem.test.tsx` | Renders text, checkbox calls onToggle, delete calls onDelete, completed has line-through |
| `TodoInput.test.tsx` | Renders input+button, calls onAdd with trimmed text, clears after submit, rejects empty, Enter key submits |
| `TodoList.test.tsx` | Renders all todos, shows empty message when no todos |
| `TodoFilter.test.tsx` | Renders three buttons, highlights active filter, calls onFilterChange, displays counts |
| `useTodos.test.ts` | addTodo adds to list, toggleTodo flips completed, deleteTodo removes |
| `TodoPage.test.tsx` | Full integration flow: add → toggle → delete → filter |

All tests use **Vitest** + **@testing-library/react** + **@testing-library/jest-dom**.
