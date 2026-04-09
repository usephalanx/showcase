# React Todo App — Architecture Plan

## Overview

A client-side Todo application built with React, TypeScript, and Vite.
State is managed exclusively with `useState`. Styling uses CSS Modules.

## File Structure

```
index.html
src/
  main.tsx
  index.css
  types/
    todo.ts
  components/
    App/
      App.tsx
      App.module.css
      App.test.tsx
    TodoInput/
      TodoInput.tsx
      TodoInput.module.css
      TodoInput.test.tsx
    TodoList/
      TodoList.tsx
      TodoList.module.css
      TodoList.test.tsx
    TodoItem/
      TodoItem.tsx
      TodoItem.module.css
      TodoItem.test.tsx
tests/
  test_static_files.py
```

## Data Model

Defined in `src/types/todo.ts`:

```typescript
export interface Todo {
  id: string;        // Generated via crypto.randomUUID()
  text: string;      // The todo item text
  completed: boolean; // Whether the item is done
}
```

## Component Hierarchy

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

## State Management

- **App** owns `const [todos, setTodos] = useState<Todo[]>([])`
- The todos array starts **empty** — no pre-populated sample data.
- CRUD operations (`addTodo`, `toggleTodo`, `deleteTodo`) are defined in App
  and passed as callbacks to child components.

### Operations

| Operation    | Signature                          | Description                          |
| ------------ | ---------------------------------- | ------------------------------------ |
| `addTodo`    | `(text: string) => void`           | Creates a new Todo with `crypto.randomUUID()` as id |
| `toggleTodo` | `(id: string) => void`             | Flips `completed` for the matching todo |
| `deleteTodo` | `(id: string) => void`             | Removes the todo from the array      |

## Component Props

### TodoInput

```typescript
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

- Uses a `<form>` element with `onSubmit` to handle both button click and Enter key.
- Empty-string todos must **not** be added (trims and validates before calling `onAdd`).
- Clears the input field after successful submission.

### TodoList

```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- Renders an empty-state message when `todos.length === 0`.

### TodoItem

```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- Renders a checkbox, the todo text, and a delete button.
- Applies `text-decoration: line-through` when `completed` is true.

## Styling Strategy

CSS Modules (`.module.css` files co-located with each component).
Global reset and base styles live in `src/index.css`.

## Testing Strategy

### Test Files and Cases

**App.test.tsx**
- renders the app with heading
- adds a new todo
- toggles a todo completed state
- deletes a todo
- shows empty state when no todos

**TodoInput.test.tsx**
- renders input field and add button
- calls onAdd with input text when submitted
- clears input after submission
- does not call onAdd when input is empty

**TodoList.test.tsx**
- renders a list of todos
- renders empty state when todos array is empty

**TodoItem.test.tsx**
- renders todo text
- renders checkbox reflecting completed state
- calls onToggle when checkbox clicked
- calls onDelete when delete button clicked
- applies line-through style when completed
