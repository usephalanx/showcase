# Architecture – React Todo Application

This document describes the component tree, TypeScript interfaces, file
structure, state management strategy, and data flow for the React + Vite +
TypeScript Todo single-page application.

---

## File Structure

```
src/
├── App.tsx                          # Root shell – renders TodoPage
├── main.tsx                         # Vite entry point – mounts <App />
├── vite-env.d.ts                    # Vite client type declarations
├── index.css                        # Global styles
│
├── types/
│   └── todo.ts                      # Todo interface & FilterType union
│
├── hooks/
│   ├── useTodos.ts                  # Custom hook – CRUD + localStorage
│   └── __tests__/
│       └── useTodos.test.ts         # Hook unit tests
│
├── components/
│   ├── TodoInput.tsx                # Text input + Add button
│   ├── TodoItem.tsx                 # Single todo row (checkbox, text, delete)
│   ├── TodoList.tsx                 # Renders list of TodoItem or empty state
│   ├── TodoFilter.tsx               # All / Active / Completed filter buttons
│   └── __tests__/
│       ├── TodoInput.test.tsx
│       ├── TodoItem.test.tsx
│       ├── TodoList.test.tsx
│       └── TodoFilter.test.tsx
│
└── pages/
    ├── TodoPage.tsx                 # Main assembler – owns state, composes UI
    └── __tests__/
        └── TodoPage.test.tsx
```

---

## TypeScript Interfaces

### `Todo` (src/types/todo.ts)

```ts
export interface Todo {
  /** Unique identifier – generated via crypto.randomUUID(). */
  id: string;
  /** User-supplied text for the todo item. */
  text: string;
  /** Whether the item has been completed. */
  completed: boolean;
  /** Unix-epoch millisecond timestamp of creation. */
  createdAt: number;
}
```

### `FilterType` (src/types/todo.ts)

```ts
export type FilterType = 'all' | 'active' | 'completed';
```

---

## Component Tree

```
<App>
  └── <TodoPage>               ← owns todos[] and filter state
        ├── <TodoInput />      ← calls onAdd(text)
        ├── <TodoFilter />     ← calls onFilterChange(filter)
        └── <TodoList>         ← receives filtered todos[]
              └── <TodoItem /> ← calls onToggle(id), onDelete(id)
```

---

## Component Props Interfaces

### TodoInput

```ts
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

- Trims whitespace before calling `onAdd`.
- Rejects empty / whitespace-only strings.
- Clears the input field after successful submission.
- Submits on Enter key press or button click.

### TodoItem

```ts
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- Renders a checkbox bound to `todo.completed`.
- Applies `text-decoration: line-through` when completed.
- Provides a Delete button.

### TodoList

```ts
interface TodoListProps {
  todos: Todo[];              // defaults to [] internally
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- When `todos` is empty, renders an informational empty-state message.
- Maps over `todos` rendering a `<TodoItem>` for each.

### TodoFilter

```ts
interface TodoFilterProps {
  currentFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  counts: {
    all: number;
    active: number;
    completed: number;
  };
}
```

- Renders three buttons: All, Active, Completed.
- Highlights the currently active filter.
- Displays counts beside each label.

---

## State Management

All application state lives in `TodoPage` via React `useState` hooks:

| State      | Type          | Initial Value                     |
| ---------- | ------------- | --------------------------------- |
| `todos`    | `Todo[]`      | Loaded from localStorage or `[]`  |
| `filter`   | `FilterType`  | `'all'`                           |

### Custom Hook – `useTodos`

Encapsulates CRUD operations and localStorage persistence:

```ts
function useTodos(): {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}
```

- **addTodo** – prepends (most recent first) a new `Todo` with
  `crypto.randomUUID()` id.
- **toggleTodo** – flips the `completed` boolean for the given id.
- **deleteTodo** – removes the todo with the given id.
- On every state change, persists `todos` to `localStorage`.
- On initialisation, reads from `localStorage`; falls back to `[]` if
  storage is unavailable or data is corrupt.

### localStorage Resilience

`localStorage` may throw in the following scenarios:
- Quota exceeded (especially in Safari private browsing).
- Security restrictions (iframe sandboxing, certain enterprise policies).

The `useTodos` hook wraps all `localStorage` calls in try/catch and
gracefully falls back to in-memory-only state. No error is surfaced to
the user.

---

## Data Flow

1. User types in `<TodoInput>` and presses Enter / clicks Add.
2. `TodoInput` trims the text and calls `onAdd(trimmedText)`.
3. `TodoPage` (via `useTodos.addTodo`) prepends a new `Todo` to state.
4. React re-renders; `TodoPage` filters `todos` by `filter` and passes
   the result to `<TodoList>`.
5. `<TodoList>` maps over filtered todos, rendering `<TodoItem>` for each.
6. User interactions (checkbox toggle, delete button) propagate back up
   via `onToggle` / `onDelete` callbacks.
7. After every state mutation, `useEffect` persists `todos` to
   `localStorage`.

---

## Styling Approach

Plain CSS via `src/index.css`. No CSS-in-JS library or CSS modules are
required for this scope. Class names follow a flat BEM-lite convention:

- `.todo-page`
- `.todo-input`
- `.todo-list`
- `.todo-item`
- `.todo-item.completed`
- `.todo-filters`
- `.todo-filters .active`
- `.empty-message`

---

## Edge Cases

| Scenario                        | Behaviour                                     |
| ------------------------------- | --------------------------------------------- |
| Empty todo list                 | `<TodoList>` shows "No todos to show."        |
| Whitespace-only input           | `<TodoInput>` rejects silently (no-op)        |
| localStorage unavailable        | Falls back to in-memory state                 |
| localStorage data corrupt       | Discards stored data, starts with `[]`        |
| `crypto.randomUUID` unavailable | Fallback: `Date.now() + Math.random()` suffix |

---

## Test Plan

All tests use **Vitest** + **React Testing Library**.

| Test File                                  | Key Cases                                                   |
| ------------------------------------------ | ----------------------------------------------------------- |
| `src/components/__tests__/TodoItem.test`   | Renders text, checkbox calls onToggle, delete calls onDelete, completed has line-through |
| `src/components/__tests__/TodoInput.test`  | Renders input+button, calls onAdd trimmed, clears after submit, rejects empty, Enter submits |
| `src/components/__tests__/TodoList.test`   | Renders all todos, shows empty message when none            |
| `src/components/__tests__/TodoFilter.test` | Renders 3 buttons, highlights active, calls onFilterChange, shows counts |
| `src/hooks/__tests__/useTodos.test`        | addTodo adds, toggleTodo flips, deleteTodo removes          |
| `src/pages/__tests__/TodoPage.test`        | Full flow: add → toggle → delete → filter                   |
