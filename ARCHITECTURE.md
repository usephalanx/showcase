# Mini React Todo App — Architecture

## Overview

A lightweight, client-side todo application built with **React 18**, **TypeScript**, and **Vite**. All state lives in-memory inside the React component tree — there is no backend, no database, and no `localStorage` persistence in the base implementation.

## Type Definitions

A single shared type is used across all components:

```typescript
// src/types/Todo.ts
export interface Todo {
  id: string;        // generated via crypto.randomUUID()
  text: string;      // user-supplied todo text
  completed: boolean; // toggled by the user
}
```

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem   (rendered once per todo)
```

- **App** is the root component that owns all state.
- **TodoInput** is a sibling of **TodoList**, both are direct children of **App**.
- **TodoItem** is rendered by **TodoList** for every item in the `todos` array.

## Component Responsibilities

### App (`src/App.tsx`)

- Owns the single piece of application state: `const [todos, setTodos] = useState<Todo[]>([]);`
- Defines three mutator functions:
  - `addTodo(text: string): void` — creates a new `Todo` with `crypto.randomUUID()`, prepends it to state.
  - `toggleTodo(id: string): void` — flips the `completed` flag of the matching todo.
  - `deleteTodo(id: string): void` — removes the matching todo from state.
- Renders `<TodoInput onAdd={addTodo} />` and `<TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />`.

### TodoInput (`src/components/TodoInput.tsx`)

- Props: `{ onAdd: (text: string) => void }`
- Maintains local state for the input field value.
- On form submit, trims the input; if non-empty, calls `onAdd(text)` and clears the field.
- Prevents adding empty or whitespace-only todos.

### TodoList (`src/components/TodoList.tsx`)

- Props: `{ todos: Todo[]; onToggle: (id: string) => void; onDelete: (id: string) => void }`
- When `todos.length === 0`, renders a "No todos yet" message.
- Otherwise maps over `todos` and renders a `<TodoItem>` for each, passing through `onToggle` and `onDelete`.

### TodoItem (`src/components/TodoItem.tsx`)

- Props: `{ todo: Todo; onToggle: (id: string) => void; onDelete: (id: string) => void }`
- Renders a checkbox bound to `todo.completed`, the todo text, and a delete button.
- Checkbox change calls `onToggle(todo.id)`.
- Delete button click calls `onDelete(todo.id)`.

## Data Flow

The application follows the standard React **unidirectional data flow** (props-down, callbacks-up):

1. **State** lives exclusively in `App` via `useState<Todo[]>`.
2. **Props flow down**: `App` passes `todos` to `TodoList`, which passes individual `todo` objects to each `TodoItem`.
3. **Callbacks flow up**: `App` passes `addTodo`, `toggleTodo`, and `deleteTodo` as callback props. Child components invoke these callbacks in response to user events (form submit, checkbox change, button click).
4. When a callback updates state, React re-renders the affected subtree.

## State Management

Only React's built-in `useState` hook is used for state management. No external state libraries (Redux, Zustand, Jotai, MobX, etc.) are used. The todo array is the single source of truth, owned by `App`.

## File Structure

```
src/
├── App.tsx                       # Root component, state owner
├── main.tsx                      # Vite entry point, renders <App />
├── types/
│   └── Todo.ts                   # Todo interface definition
└── components/
    ├── TodoInput.tsx              # Text input + add button
    ├── TodoList.tsx               # List container, empty-state handling
    └── TodoItem.tsx               # Single todo row with toggle & delete
```

## ID Generation

Todo IDs are generated using `crypto.randomUUID()`, which produces RFC 4122 v4 UUIDs. This avoids collisions without needing an auto-increment counter or external library.

## Persistence

No persistence mechanism (localStorage, IndexedDB, backend API) is included in the base plan. All data is lost on page refresh.

## Edge Cases

| Scenario | Handling |
|---|---|
| Empty todo list | `TodoList` renders "No todos yet" message |
| Whitespace-only input | `TodoInput` trims and rejects empty strings |
| Rapid toggles | State updates are functional (`setTodos(prev => ...)`) to avoid stale closures |
| Duplicate text | Allowed — each todo has a unique UUID regardless of text content |
