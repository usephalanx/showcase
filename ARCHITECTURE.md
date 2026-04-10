# Architecture — Mini React Todo App

This document describes the complete architecture of the Mini React Todo App,
a single-page application built with React, TypeScript, and Vite.

## Overview

A lightweight, client-side todo application that allows users to add, toggle,
and delete todo items. All state lives in the browser — there is no backend
or persistence layer.

## Type Definitions

The core data model is defined in `src/types.ts`:

```typescript
export interface Todo {
  id: string;       // Unique identifier (crypto.randomUUID())
  text: string;     // The todo item text
  completed: boolean; // Whether the item has been completed
}
```

- **id** (`string`): Generated via `crypto.randomUUID()` to avoid collisions.
- **text** (`string`): User-supplied description of the task.
- **completed** (`boolean`): Toggled between `true` and `false`.

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem  (one per todo)
```

- **App** → **TodoInput**: passes `addTodo` callback.
- **App** → **TodoList**: passes `todos`, `toggleTodo`, and `deleteTodo`.
- **TodoList** → **TodoItem**: passes individual `todo`, `toggleTodo`, and `deleteTodo`.

## Component Responsibilities

### App (`src/App.tsx`)

- Owns application state via `useState<Todo[]>`.
- Defines three state-mutation functions:
  - `addTodo(text: string): void` — creates a new `Todo` with `crypto.randomUUID()` and prepends it.
  - `toggleTodo(id: string): void` — flips the `completed` flag of the matching todo.
  - `deleteTodo(id: string): void` — removes the matching todo from the list.
- Renders `<TodoInput>` and `<TodoList>` with appropriate props.

### TodoInput (`src/components/TodoInput.tsx`)

- Maintains local `useState<string>` for the input field value.
- On form submission:
  - Trims whitespace; if the result is empty, does **not** call `addTodo`.
  - Otherwise calls `addTodo(trimmedText)` and clears the input.
- Props: `{ addTodo: (text: string) => void }`.

### TodoList (`src/components/TodoList.tsx`)

- Receives the full `todos` array, `toggleTodo`, and `deleteTodo` as props.
- Maps over `todos` and renders a `<TodoItem>` for each entry.
- Handles the empty-list case gracefully (renders a helpful message when `todos.length === 0`).
- Props: `{ todos: Todo[]; toggleTodo: (id: string) => void; deleteTodo: (id: string) => void }`.

### TodoItem (`src/components/TodoItem.tsx`)

- Renders a single todo with:
  - A checkbox bound to `todo.completed` that calls `toggleTodo(todo.id)` on change.
  - The todo text, visually struck through when completed.
  - A delete button that calls `deleteTodo(todo.id)`.
- Props: `{ todo: Todo; toggleTodo: (id: string) => void; deleteTodo: (id: string) => void }`.

## Data Flow

The application follows a strict **unidirectional data flow**:

1. **State** lives exclusively in `App` via `useState<Todo[]>`.
2. **Props down**: `App` passes `todos` and callback functions down to children.
3. **Callbacks up**: Child components invoke callbacks (`addTodo`, `toggleTodo`,
   `deleteTodo`) which update state in `App`, triggering a re-render.

No child component mutates state directly.

## State Management

Only **React `useState`** is used for state management. No external state
libraries (Redux, Zustand, Jotai, MobX, etc.) are used. The entire
application state is a single `Todo[]` array held in the `App` component.

## File Structure

```
/
├── index.html                  # Vite HTML entry point
├── package.json                # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
├── RUNNING.md                  # Setup / run instructions
├── ARCHITECTURE.md             # This file
└── src/
    ├── main.tsx                # React DOM entry point
    ├── App.tsx                 # Root component with state
    ├── App.css                 # Application styles
    ├── types.ts                # Todo interface definition
    ├── vite-env.d.ts           # Vite client type references
    └── components/
        ├── TodoInput.tsx       # Input form component
        ├── TodoItem.tsx        # Single todo row component
        └── TodoList.tsx        # List container component
```

## Edge Cases

- **Empty input**: `TodoInput` trims whitespace and prevents adding empty todos.
- **Empty list**: `TodoList` renders a fallback message when there are no todos.
- **ID collisions**: `crypto.randomUUID()` provides sufficient uniqueness.
- **No persistence**: State resets on page reload — localStorage is not included
  in this base implementation.
