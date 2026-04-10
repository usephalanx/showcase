# Architecture — Mini React Todo App

## Overview

A client-side Todo application built with React, TypeScript, and Vite. The app allows users to add, toggle, and delete todo items. All state is managed in-memory via React's `useState` hook — no backend or persistence layer is included.

## Type Definitions

The core data type is defined in `src/types/Todo.ts`:

```typescript
export interface Todo {
  id: string;
  text: string;
  completed: boolean;
}
```

- **id** (`string`): A unique identifier generated via `crypto.randomUUID()` to avoid collisions.
- **text** (`string`): The user-visible description of the todo item.
- **completed** (`boolean`): Whether the todo has been marked as done.

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

- `App` is the root component that owns all state.
- `TodoInput` captures new todo text from the user.
- `TodoList` renders the list of `TodoItem` components.
- `TodoItem` renders a single todo with toggle and delete controls.

## Component Responsibilities

### App

- Owns the todo state via `useState<Todo[]>([])`.
- Defines three mutation functions:
  - `addTodo(text: string): void` — creates a new `Todo` with `crypto.randomUUID()` and prepends it to the list. Ignores empty/whitespace-only input.
  - `toggleTodo(id: string): void` — flips the `completed` flag of the matching todo.
  - `deleteTodo(id: string): void` — removes the todo with the given id from the list.
- Passes `addTodo` to `TodoInput` and `todos`, `toggleTodo`, `deleteTodo` to `TodoList`.

### TodoInput

- Maintains local state for the input field value via `useState<string>('')`.
- On form submission, calls `props.onAdd(text)` if the trimmed text is non-empty, then clears the input.
- Prevents adding empty or whitespace-only todos.

**Props interface:**
```typescript
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

### TodoList

- Receives the full `todos` array plus callback props.
- Maps over `todos` to render a `TodoItem` for each entry.
- Handles the empty-list case gracefully (renders nothing or a subtle message).

**Props interface:**
```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

### TodoItem

- Renders a single todo's text, a checkbox/toggle for completion, and a delete button.
- Applies a visual style (e.g. line-through) when `completed` is true.

**Props interface:**
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

## Data Flow

The application follows a strict **unidirectional data flow** (props-down, callbacks-up):

1. `App` holds the single source of truth: `todos: Todo[]`.
2. State is passed **down** as props to child components.
3. User interactions in child components invoke callback props (`onAdd`, `onToggle`, `onDelete`) that call functions defined in `App`.
4. Those functions update state via `setTodos`, triggering a re-render that flows new props downward.

No child component directly mutates the todo list.

## State Management

State management uses **only React `useState`**. No external state management libraries (Redux, Zustand, MobX, Jotai, etc.) are used. The single `useState<Todo[]>` in `App` is sufficient for this application's complexity.

## File Structure

```
/
├── index.html                  # HTML shell with root div and script tag
├── package.json                # Project dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
├── ARCHITECTURE.md             # This file
├── RUNNING.md                  # Setup and run instructions
└── src/
    ├── main.tsx                # ReactDOM.createRoot entry point
    ├── App.tsx                 # Root component with state and logic
    ├── vite-env.d.ts           # Vite client type references
    ├── types/
    │   └── Todo.ts             # Todo interface definition
    └── components/
        ├── TodoInput.tsx        # New-todo input form component
        ├── TodoList.tsx         # List container component
        └── TodoItem.tsx         # Single todo row component
```

## Edge Cases

- **Empty todo list**: `TodoList` handles `todos.length === 0` gracefully by rendering an empty container or a placeholder message.
- **Empty/whitespace input**: `TodoInput` trims input and prevents submission of empty or whitespace-only strings.
- **ID collisions**: IDs are generated using `crypto.randomUUID()` which provides sufficient uniqueness.
- **No persistence**: All data is in-memory only. Refreshing the page resets the todo list. No `localStorage` or backend persistence is included in the base plan.
