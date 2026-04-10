# Mini React Todo App — Architecture

## Overview

A lightweight todo application built with React, TypeScript, and Vite. The app
follows a unidirectional data-flow pattern with all state owned by the root
`App` component and passed down via props.

## Type Definitions

The core data type lives in `src/types/Todo.ts`:

```typescript
export interface Todo {
  id: string;        // Unique identifier (generated via crypto.randomUUID())
  text: string;      // The todo item text
  completed: boolean; // Whether the item is done
}
```

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem   (one per todo)
```

- **App** is the root component that owns the `Todo[]` state.
- **TodoInput** captures new todo text from the user.
- **TodoList** receives the array of todos and renders a `TodoItem` for each.
- **TodoItem** renders a single todo with toggle and delete controls.

## Component Responsibilities

### App (`src/App.tsx`)

- Owns application state via `useState<Todo[]>`.
- Defines three handler functions:
  - `addTodo(text: string)` — creates a new `Todo` with `crypto.randomUUID()`,
    prepends it to the array.
  - `toggleTodo(id: string)` — flips the `completed` flag of the matching todo.
  - `deleteTodo(id: string)` — removes the todo with the given id from state.
- Passes `addTodo` to `TodoInput`, and `todos`, `toggleTodo`, `deleteTodo` to
  `TodoList`.

### TodoInput (`src/components/TodoInput.tsx`)

- Renders a text input and an "Add" button.
- Maintains local `useState<string>` for the input value.
- On submit, trims the input; if non-empty, calls `onAdd(text)` and clears
  the field. Empty or whitespace-only input is rejected (no-op).

### TodoList (`src/components/TodoList.tsx`)

- Receives `todos: Todo[]`, `onToggle`, and `onDelete` as props.
- Maps over `todos` rendering a `TodoItem` for each, keyed by `todo.id`.
- When `todos.length === 0`, renders a friendly empty-state message.

### TodoItem (`src/components/TodoItem.tsx`)

- Receives a single `todo: Todo`, `onToggle(id: string)`, and
  `onDelete(id: string)` as props.
- Renders a checkbox bound to `todo.completed` that calls `onToggle(todo.id)`
  on change.
- Renders `todo.text` with `text-decoration: line-through` when `completed`
  is `true`.
- Renders a "Delete" button that calls `onDelete(todo.id)` on click.
- Pure presentational — contains no internal state.

## Data Flow

The app follows the standard React unidirectional data-flow pattern:

1. **Props down** — `App` passes the `todos` array and callback functions down
   through `TodoList` and `TodoInput`.
2. **Callbacks up** — Child components invoke callbacks (`onAdd`, `onToggle`,
   `onDelete`) to request state changes.
3. **State update** — `App` updates its `useState` hook, triggering a re-render
   that flows new props back down the tree.

No events are emitted sideways between siblings; all communication goes through
the parent.

## State Management

The application uses **only React `useState`** for state management. No external
state libraries (Redux, Zustand, MobX, etc.) are used. The single
`useState<Todo[]>` in `App` is the sole source of truth.

## File Structure

```
src/
├── App.tsx                       # Root component, state owner
├── main.tsx                      # Vite entry point, renders <App />
├── types/
│   └── Todo.ts                   # Todo interface definition
└── components/
    ├── TodoInput.tsx              # New-todo input form
    ├── TodoList.tsx               # List container
    └── TodoItem.tsx               # Single todo row
```

## Edge Cases

- **Empty list** — `TodoList` gracefully renders an empty-state message when
  `todos` has length 0.
- **Blank input** — `TodoInput` prevents adding empty or whitespace-only todos.
- **ID collisions** — IDs are generated with `crypto.randomUUID()`, which
  provides sufficient uniqueness for a client-side app.
- **No persistence** — Todos live only in React state; refreshing the page
  clears all data. No `localStorage` or backend persistence is included in
  the base plan.
