# React Todo App — Architecture Plan

## Overview

A simple, single-page Todo application built with React, TypeScript, and Vite.
State is managed with `useState` only (no external state libraries).
Styling uses CSS Modules.

---

## File Structure

```
src/
  types/
    todo.ts                        # Todo interface
  components/
    App/
      App.tsx                      # Root component — state lives here
      App.module.css
      App.test.tsx
    TodoInput/
      TodoInput.tsx                # Text input + add button (form)
      TodoInput.module.css
      TodoInput.test.tsx
    TodoList/
      TodoList.tsx                 # Renders list of TodoItem components
      TodoList.module.css
      TodoList.test.tsx
    TodoItem/
      TodoItem.tsx                 # Single todo: checkbox, text, delete
      TodoItem.module.css
      TodoItem.test.tsx
  main.tsx                         # ReactDOM.createRoot entry point
  index.css                        # Global / reset styles
index.html                         # Vite HTML entry
package.json
tsconfig.json
vite.config.ts
```

---

## Data Model

```typescript
// src/types/todo.ts
export interface Todo {
  id: string;        // Generated via crypto.randomUUID()
  text: string;      // User-entered todo text
  completed: boolean; // Toggle-able completion state
}
```

---

## Component Hierarchy

```
App
├── TodoInput        (onAdd: (text: string) => void)
└── TodoList         (todos: Todo[], onToggle, onDelete)
    └── TodoItem     (todo: Todo, onToggle, onDelete)   × N
```

---

## State Management

All state is kept in `App` via a single `useState<Todo[]>` hook.

| Operation  | Function       | Signature                          |
|------------|----------------|------------------------------------|
| Add        | `addTodo`      | `(text: string) => void`           |
| Toggle     | `toggleTodo`   | `(id: string) => void`             |
| Delete     | `deleteTodo`   | `(id: string) => void`             |

### Rules

- Empty or whitespace-only text must **not** create a todo.
- `crypto.randomUUID()` is used for id generation.
- The `todos` array starts **empty** (no sample data).

---

## Component Props

### TodoInput

```typescript
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

- Uses a `<form>` with `onSubmit` to handle both Enter key and button click.
- Clears the input field after successful submission.

### TodoList

```typescript
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- Renders an empty-state message when `todos` is empty.

### TodoItem

```typescript
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

- Checkbox `checked` bound to `todo.completed`; `onChange` calls `onToggle(todo.id)`.
- Text displayed in a `<span>` with `textDecoration: "line-through"` when completed.
- Delete `<button>` calls `onDelete(todo.id)` on click.

---

## Styling Strategy

- **CSS Modules** (`*.module.css`) for component-scoped styles.
- Inline `style` for dynamic properties (e.g., `textDecoration` on TodoItem text).
- A single `index.css` for global resets / base typography.

---

## Testing Strategy

Python-based structural tests (`pytest`) validate source files:

| Test File                  | Key Tests                                              |
|----------------------------|--------------------------------------------------------|
| `tests/test_todo_item.py`  | renders todo text, checkbox reflects completed state,  |
|                            | calls onToggle on checkbox click, calls onDelete on    |
|                            | delete button click, applies line-through when done    |

Future JS-based tests (Vitest + React Testing Library) will cover
runtime behaviour once the full app is assembled.

---

## Accessibility

- `aria-label` attributes on checkbox and delete button.
- Form submission via Enter key in TodoInput (native `<form>`).
- Semantic HTML: `<ul>` / `<li>` for the todo list.
