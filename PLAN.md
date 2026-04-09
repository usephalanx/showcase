# React Todo App — Architecture Plan

This document is the single source of truth for the React + Vite + TypeScript Todo application.

---

## File Structure

```
/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── vite-env.d.ts
├── PLAN.md
├── RUNNING.md
└── src/
    ├── main.tsx
    ├── types/
    │   └── todo.ts
    └── components/
        ├── App/
        │   ├── App.tsx
        │   ├── App.module.css
        │   └── App.test.tsx
        ├── TodoInput/
        │   ├── TodoInput.tsx
        │   ├── TodoInput.module.css
        │   └── TodoInput.test.tsx
        ├── TodoList/
        │   ├── TodoList.tsx
        │   ├── TodoList.module.css
        │   └── TodoList.test.tsx
        └── TodoItem/
            ├── TodoItem.tsx
            ├── TodoItem.module.css
            └── TodoItem.test.tsx
```

---

## Data Model

Defined in `src/types/todo.ts`:

```typescript
export interface Todo {
  id: string;
  text: string;
  completed: boolean;
}
```

- **id** (`string`): Unique identifier generated via `crypto.randomUUID()`.
- **text** (`string`): The content / description of the todo item.
- **completed** (`boolean`): Whether the todo has been marked as done.

---

## Component Hierarchy

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

### App (`src/components/App/App.tsx`)

- **State:**
  - `todos: Todo[]` — managed with `useState<Todo[]>([])`.
  - The todos array starts **empty** (no pre-populated sample data).
- **CRUD Functions:**
  - `addTodo(text: string): void` — creates a new `Todo` with `crypto.randomUUID()` as `id`, the supplied `text`, and `completed: false`, then prepends it to the `todos` array.
  - `toggleTodo(id: string): void` — toggles the `completed` boolean of the todo matching `id`.
  - `deleteTodo(id: string): void` — removes the todo matching `id` from the array.
- **Renders:** A heading (`<h1>Todo App</h1>`), a `<TodoInput>` component, and a `<TodoList>` component.

### TodoInput (`src/components/TodoInput/TodoInput.tsx`)

- **Props interface:**
  ```typescript
  interface TodoInputProps {
    onAdd: (text: string) => void;
  }
  ```
- **Internal state:** `inputValue: string` via `useState<string>("")` for the controlled input.
- **Behaviour:**
  - Uses a `<form>` element with an `onSubmit` handler, ensuring both button click and **Enter key** trigger submission.
  - On submit, trims the input. If the trimmed value is **empty**, the function returns early without calling `onAdd` (empty-string validation).
  - Otherwise calls `props.onAdd(trimmedText)` and clears the input field.
- **Renders:** A `<form>` containing an `<input type="text">` and a `<button type="submit">Add</button>`.

### TodoList (`src/components/TodoList/TodoList.tsx`)

- **Props interface:**
  ```typescript
  interface TodoListProps {
    todos: Todo[];
    onToggle: (id: string) => void;
    onDelete: (id: string) => void;
  }
  ```
- **Behaviour:**
  - If `todos` is empty, renders an empty-state message: `<p>No todos yet</p>`.
  - Otherwise renders a `<ul>` with one `<TodoItem>` per todo.
- **Renders:** A `<ul>` (or empty-state `<p>`).

### TodoItem (`src/components/TodoItem/TodoItem.tsx`)

- **Props interface:**
  ```typescript
  interface TodoItemProps {
    todo: Todo;
    onToggle: (id: string) => void;
    onDelete: (id: string) => void;
  }
  ```
- **Behaviour:**
  - Renders a checkbox reflecting `todo.completed`.
  - Clicking the checkbox calls `onToggle(todo.id)`.
  - Renders the todo text in a `<span>`. When `completed` is `true`, applies `text-decoration: line-through` style.
  - Renders a delete `<button>` that calls `onDelete(todo.id)`.
- **Renders:** An `<li>` containing a checkbox, a text span, and a delete button.

---

## State Management

- **Approach:** React `useState` only — no external libraries.
- **State location:** All state lives in `App`. Child components receive data and callbacks via props.
- **State variables in App:**
  - `const [todos, setTodos] = useState<Todo[]>([]);`

---

## Styling Strategy

- **CSS Modules** — each component has a co-located `.module.css` file.
- Class names are imported as objects (e.g. `import styles from './App.module.css'`).
- No global CSS framework required.

---

## Edge Cases & Validation

1. **Empty todo prevention:** `TodoInput` trims whitespace and rejects empty strings before calling `onAdd`.
2. **ID generation:** Uses `crypto.randomUUID()` for globally unique, collision-free IDs.
3. **Empty initial state:** The `todos` array starts as `[]` — no pre-populated sample data.
4. **Keyboard accessibility:** `TodoInput` uses a `<form>` with `onSubmit`, so pressing Enter in the input field triggers submission.

---

## Testing Strategy

Test files are co-located with their components. Tests use React Testing Library and Vitest.

### `src/components/App/App.test.tsx`

- `renders the app with heading`
- `adds a new todo`
- `toggles a todo completed state`
- `deletes a todo`
- `shows empty state when no todos`

### `src/components/TodoInput/TodoInput.test.tsx`

- `renders input field and add button`
- `calls onAdd with input text when submitted`
- `clears input after submission`
- `does not call onAdd when input is empty`

### `src/components/TodoList/TodoList.test.tsx`

- `renders a list of todos`
- `renders empty state when todos array is empty`

### `src/components/TodoItem/TodoItem.test.tsx`

- `renders todo text`
- `renders checkbox reflecting completed state`
- `calls onToggle when checkbox clicked`
- `calls onDelete when delete button clicked`
- `applies line-through style when completed`
