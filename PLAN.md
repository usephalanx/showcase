# React Todo App — Architecture Plan

## Overview

A simple Todo application built with React, Vite, and TypeScript. The frontend
consists of a small component hierarchy using `useState` for state management
and CSS Modules for styling.

## File Structure

```
src/
├── main.tsx                          # Application entry point
├── types/
│   └── todo.ts                       # Todo type definition
├── components/
│   ├── App/
│   │   ├── App.tsx                   # Root component, state owner
│   │   └── App.module.css            # App styles
│   ├── TodoInput/
│   │   ├── TodoInput.tsx             # Controlled input form
│   │   └── TodoInput.module.css      # TodoInput styles
│   ├── TodoList/
│   │   ├── TodoList.tsx              # Renders list of TodoItem
│   │   └── TodoList.module.css       # TodoList styles
│   └── TodoItem/
│       ├── TodoItem.tsx              # Single todo row
│       └── TodoItem.module.css       # TodoItem styles
tests/
├── test_todo_input.py                # Tests for TodoInput component
```

## Data Model

Defined in `src/types/todo.ts`:

```typescript
export interface Todo {
  id: string;         // Generated via crypto.randomUUID()
  text: string;       // The todo text content
  completed: boolean; // Whether the todo is done
}
```

- **id**: `string` — generated with `crypto.randomUUID()`
- **text**: `string` — the user-entered todo text
- **completed**: `boolean` — toggled between true/false

## Component Hierarchy

```
App
├── TodoInput        (onAdd callback)
└── TodoList         (todos array, onToggle, onDelete)
    └── TodoItem[]   (single todo, onToggle, onDelete)
```

## State Management

- **useState only** — no external state libraries.
- `App` owns the `todos: Todo[]` state (starts as empty array `[]`).
- `TodoInput` owns local `text: string` state for the controlled input.
- State setters:
  - `addTodo(text: string): void` — creates a new Todo and appends to array
  - `toggleTodo(id: string): void` — flips `completed` for the matching todo
  - `deleteTodo(id: string): void` — removes the todo from the array

## Component Props Interfaces

### TodoInput
```typescript
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

### TodoList
```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

### TodoItem
```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

## Styling Strategy

- CSS Modules (`.module.css` files co-located with components).
- Each component imports its own module for scoped class names.

## Validation Rules

- Empty-string or whitespace-only todos must **not** be added.
- `TodoInput` trims input before validation and submission.
- `TodoInput` uses a `<form>` element with `onSubmit` to handle both button
  click and Enter key submission (keyboard accessible).
- Input is cleared after successful submission.

## ID Generation

- `crypto.randomUUID()` is used for generating unique todo IDs.
- No `Math.random()` or incrementing integers.

## Initial State

- The `todos` array starts **empty** — no pre-populated sample data.

## Testing Strategy

Test files use pytest to validate component source structure:

- `tests/test_todo_input.py`:
  - renders input field and add button
  - calls onAdd with input text when submitted
  - clears input after submission
  - does not call onAdd when input is empty
  - validates controlled input pattern
  - validates form element with onSubmit
  - validates accessibility attributes
