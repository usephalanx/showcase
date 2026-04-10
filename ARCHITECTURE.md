# Architecture — Mini React Todo App

A client-side Todo application built with React, TypeScript, and Vite.

## Type Definitions

The core data model is defined in `src/types.ts`:

```typescript
export interface Todo {
  id: string;        // Unique identifier (generated via crypto.randomUUID())
  text: string;      // The text content of the todo
  completed: boolean; // Whether the todo has been completed
}
```

## Component Tree

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

- **App** is the root component that owns all state.
- **TodoInput** is a sibling of **TodoList**, both direct children of **App**.
- **TodoItem** is rendered by **TodoList** for each todo in the array.

## Component Responsibilities

### App (`src/App.tsx`)

- Owns the todo state via `useState<Todo[]>`.
- Defines `addTodo`, `toggleTodo`, and `deleteTodo` functions.
- Passes `onAdd` callback to `TodoInput`.
- Passes the `todos` array, `onToggle`, and `onDelete` callbacks to `TodoList`.

### TodoInput (`src/components/TodoInput.tsx`)

- Controlled text input inside a `<form>`.
- Calls `onAdd(text: string)` on form submission.
- Trims input and prevents adding empty or whitespace-only todos.
- Clears the input field after successful submission.

### TodoList (`src/components/TodoList.tsx`)

- Receives `todos: Todo[]`, `onToggle: (id: string) => void`, and `onDelete: (id: string) => void` as props.
- Maps over the `todos` array and renders a `TodoItem` for each entry.
- Handles the empty-list case gracefully (renders nothing or an informational message).

### TodoItem (`src/components/TodoItem.tsx`)

- Receives a single `todo: Todo`, `onToggle: (id: string) => void`, and `onDelete: (id: string) => void` as props.
- Displays the todo text with visual indication of completion status.
- Provides a toggle control (checkbox) and a delete button.

## Data Flow

The application follows a strict **unidirectional data flow** pattern:

1. **Props down**: `App` passes data (the `todos` array) and callbacks (`onAdd`, `onToggle`, `onDelete`) to child components via props.
2. **Callbacks up**: Child components invoke the callback props to signal user actions. The callbacks update state in `App`, which triggers a re-render.

No child component directly mutates the todo state.

## State Management

All application state is managed using React's built-in `useState` hook inside the `App` component. **No external state management libraries** (Redux, Zustand, Jotai, etc.) are used.

State shape:

```typescript
const [todos, setTodos] = useState<Todo[]>([]);
```

Functions defined in App:

- `addTodo(text: string)`: Creates a new `Todo` with `id` from `crypto.randomUUID()`, the given `text`, and `completed: false`. Prepends it to the array.
- `toggleTodo(id: string)`: Toggles the `completed` field of the todo matching the given `id`.
- `deleteTodo(id: string)`: Removes the todo matching the given `id` from the array.

## File Structure

```
src/
├── types.ts                      # Todo interface definition
├── App.tsx                       # Root component with state management
├── App.css                       # App-level styles
├── main.tsx                      # Vite entry point, renders <App />
├── index.css                     # Global styles
└── components/
    ├── TodoInput.tsx             # Controlled input for adding todos
    ├── TodoList.tsx              # Renders list of TodoItem components
    └── TodoItem.tsx              # Single todo display with toggle/delete
```

## Edge Cases

- **Empty todo list**: `TodoList` handles `todos.length === 0` gracefully.
- **Empty/whitespace input**: `TodoInput` trims input and prevents submission of empty strings.
- **ID collisions**: IDs are generated with `crypto.randomUUID()` which provides sufficient uniqueness.
- **No persistence**: There is no localStorage or server-side persistence in the base implementation. Data resets on page refresh.
