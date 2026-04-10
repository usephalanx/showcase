# Architecture — Mini React Todo App

This document describes the complete architecture of the Mini React Todo App,
a client-side single-page application built with React, TypeScript, and Vite.

## Overview

The application lets users create, complete, and delete todo items. All state
lives in the browser — there is no backend persistence. The UI is composed of
a small tree of React functional components that communicate via props and
callback functions following a strict unidirectional data-flow pattern.

## Type Definitions

The core domain type is defined in `src/types/Todo.ts`:

```ts
export interface Todo {
  id: string;        // Unique identifier (crypto.randomUUID())
  text: string;      // The todo's display text
  completed: boolean; // Whether the todo has been marked as done
}
```

- **id** (`string`): Generated via `crypto.randomUUID()` to avoid collisions.
- **text** (`string`): The user-provided description of the todo.
- **completed** (`boolean`): Toggled by the user; defaults to `false`.

## Component Tree

```
App
├── TodoInput
└── TodoList
    ├── TodoItem
    ├── TodoItem
    └── …
```

- `App` is the root component that owns all application state.
- `TodoInput` is a controlled form for adding new todos.
- `TodoList` renders the array of todos (or handles the empty-list case).
- `TodoItem` renders a single todo with toggle and delete controls.

## Component Responsibilities

### App

- **File:** `src/App.tsx`
- **State:** Owns the single source of truth via `useState<Todo[]>([])`.
- **Functions defined here:**
  - `addTodo(text: string): void` — Creates a new `Todo` object (using `crypto.randomUUID()` for the id, the supplied text, and `completed: false`) and prepends it to the list.
  - `toggleTodo(id: string): void` — Flips the `completed` flag of the todo with the matching id.
  - `deleteTodo(id: string): void` — Removes the todo with the matching id from the list.
- Renders `<TodoInput>` and `<TodoList>`, passing state and callbacks as props.

### TodoInput

- **File:** `src/components/TodoInput.tsx`
- **Props:**
  ```ts
  interface TodoInputProps {
    onAdd: (text: string) => void;
  }
  ```
- Manages its own local `useState<string>("")` for the input field.
- On form submission:
  1. Trims the input value.
  2. If the trimmed value is empty, does **nothing** (prevents adding empty/whitespace-only todos).
  3. Otherwise calls `onAdd(trimmedText)` and clears the input.

### TodoList

- **File:** `src/components/TodoList.tsx`
- **Props:**
  ```ts
  interface TodoListProps {
    todos: Todo[];
    onToggle: (id: string) => void;
    onDelete: (id: string) => void;
  }
  ```
- If `todos.length === 0`, renders a friendly empty-state message (e.g. "No todos yet").
- Otherwise maps over `todos` and renders a `<TodoItem>` for each, passing the individual todo and the callbacks.

### TodoItem

- **File:** `src/components/TodoItem.tsx`
- **Props:**
  ```ts
  interface TodoItemProps {
    todo: Todo;
    onToggle: (id: string) => void;
    onDelete: (id: string) => void;
  }
  ```
- Renders the todo text, a checkbox/button to toggle completion, and a delete button.
- Applies a visual style (e.g. strikethrough) when `todo.completed` is `true`.

## Data Flow

The application follows the standard React unidirectional data-flow pattern:

1. **Props down:** `App` passes the `todos` array and callback functions (`onAdd`, `onToggle`, `onDelete`) as props to child components.
2. **Callbacks up:** Child components invoke the callbacks when the user interacts with the UI (e.g. submitting the input form, clicking a checkbox, clicking a delete button).
3. **State update:** The callback in `App` calls the `useState` setter, which triggers a re-render of the component tree with the updated state.

There is no prop drilling beyond two levels, and no need for React Context or any external state library.

## State Management

State management uses **only React `useState`** — no external state management libraries (Redux, Zustand, MobX, Jotai, etc.) are used.

- `App` holds `const [todos, setTodos] = useState<Todo[]>([]);`
- `TodoInput` holds `const [text, setText] = useState<string>("");`

These two pieces of state are the only state in the entire application.

## File Structure

```
src/
├── main.tsx                  # ReactDOM.createRoot entry point
├── App.tsx                   # Root component — state owner
├── App.css                   # Styles for the App component
├── index.css                 # Global/base styles
├── types/
│   └── Todo.ts               # Todo interface definition
└── components/
    ├── TodoInput.tsx          # Controlled input form component
    ├── TodoList.tsx           # List renderer (handles empty state)
    └── TodoItem.tsx           # Single todo row with toggle & delete
```

Supporting project-root files:

```
index.html                    # Vite HTML entry point
package.json                  # Dependencies and npm scripts
tsconfig.json                 # TypeScript compiler configuration
vite.config.ts                # Vite build configuration
```

## Edge Cases & Design Decisions

| Concern | Decision |
|---|---|
| Empty/whitespace todo text | `TodoInput` trims input and silently rejects empty strings |
| Empty todo list | `TodoList` renders a placeholder message when `todos.length === 0` |
| Unique IDs | `crypto.randomUUID()` is used — supported in all modern browsers |
| Persistence | **None** — no `localStorage`, no backend. Todos are lost on page refresh |
| Styling | Plain CSS; no CSS-in-JS or utility framework required |
| Testing | Component behaviour is tested via pytest against the built output |
