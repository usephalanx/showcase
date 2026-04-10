# Mini React Todo App — Architecture

## Overview

A client-side Todo application built with React, TypeScript, and Vite. All state
is managed in-memory on the client — there is no backend or persistence layer.

## Type Definitions

```typescript
// src/types/Todo.ts
export interface Todo {
  id: string;        // Generated via crypto.randomUUID()
  text: string;      // The todo content
  completed: boolean; // Whether the todo is done
}
```

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

## Component Responsibilities

### App (`src/App.tsx`)

- Owns the single source of truth: `useState<Todo[]>`.
- Defines three state-mutation functions:
  - **addTodo(text: string)** — creates a `Todo` with `crypto.randomUUID()`,
    prepends it to the list.
  - **toggleTodo(id: string)** — flips the `completed` boolean of the matching todo.
  - **deleteTodo(id: string)** — removes the todo with the given id.
- Renders `<TodoInput>` and `<TodoList>`, passing data and callbacks as props.
- Imports `App.css` for application-wide styling.

### TodoInput (`src/components/TodoInput.tsx`)

- Manages its own local `useState<string>` for the text field.
- On form submit, trims the input; ignores empty/whitespace-only strings.
- Calls `props.onAdd(trimmedText)` and clears the field.

### TodoList (`src/components/TodoList.tsx`)

- Receives `todos`, `onToggle`, and `onDelete` as props.
- When `todos.length === 0`, renders an empty-state message.
- Otherwise maps over `todos` and renders a `<TodoItem>` for each.

### TodoItem (`src/components/TodoItem.tsx`)

- Receives a single `todo`, `onToggle`, and `onDelete` as props.
- Renders a checkbox (bound to `todo.completed`), the text, and a Delete button.
- Applies a `completed` CSS class when the item is done (line-through style).

## Data Flow

The app follows the standard React unidirectional data-flow pattern:

1. **Props down** — `App` passes the `todos` array and callback functions
   (`onAdd`, `onToggle`, `onDelete`) to child components.
2. **Callbacks up** — child components invoke the callbacks to request state
   changes; `App` updates its `useState` accordingly, triggering a re-render.

No events are emitted sideways between sibling components.

## State Management

Only React's built-in `useState` hook is used. No external state management
libraries (Redux, Zustand, Jotai, MobX, etc.) are part of this project.

- `App` holds `useState<Todo[]>([])` — the single authoritative list.
- `TodoInput` holds `useState<string>('')` — the controlled input value.

## File Structure

```
src/
├── types/
│   └── Todo.ts              # Todo interface definition
├── components/
│   ├── TodoInput.tsx         # New-todo input form
│   ├── TodoList.tsx          # Renders the list of TodoItems
│   └── TodoItem.tsx          # Single todo row
├── App.tsx                   # Root component with state management
├── App.css                   # Application styles
└── main.tsx                  # Vite entry point (renders <App />)
```

## Edge Cases

- **Empty list**: `TodoList` renders a friendly empty-state message.
- **Whitespace-only input**: `TodoInput` trims and rejects empty strings.
- **ID collisions**: `crypto.randomUUID()` produces v4 UUIDs with negligible
  collision probability.
- **No persistence**: Refreshing the page clears all todos. No `localStorage`
  or server sync is included in this version.
