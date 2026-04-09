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
├── requirements-test.txt
├── RUNNING.md
├── PLAN.md
├── src/
│   ├── main.tsx
│   ├── types/
│   │   └── todo.ts
│   └── components/
│       ├── App/
│       │   ├── App.tsx
│       │   ├── App.module.css
│       │   └── App.test.tsx
│       ├── TodoInput/
│       │   ├── TodoInput.tsx
│       │   ├── TodoInput.module.css
│       │   └── TodoInput.test.tsx
│       ├── TodoList/
│       │   ├── TodoList.tsx
│       │   ├── TodoList.module.css
│       │   └── TodoList.test.tsx
│       └── TodoItem/
│           ├── TodoItem.tsx
│           ├── TodoItem.module.css
│           └── TodoItem.test.tsx
└── tests/
    └── test_file_structure.py
```

---

## Data Model

Defined in `src/types/todo.ts`:

```ts
export interface Todo {
  id: string;        // Generated via crypto.randomUUID()
  text: string;      // The todo content — must not be empty
  completed: boolean; // Whether the todo is done
}
```

- **id** — `string` — unique identifier produced by `crypto.randomUUID()`.
- **text** — `string` — the user-visible text of the todo item.
- **completed** — `boolean` — tracks whether the item has been completed.

---

## Component Hierarchy

```
App
├── TodoInput
└── TodoList
    └── TodoItem (one per todo)
```

### App (`src/components/App/App.tsx`)

Root component. Owns the todo state.

**State:**

```ts
const [todos, setTodos] = useState<Todo[]>([]);
```

The todos array starts **empty** — no pre-populated sample data.

**Functions:**

| Function       | Signature                             | Description                                  |
| -------------- | ------------------------------------- | -------------------------------------------- |
| `addTodo`      | `(text: string) => void`              | Creates a new Todo and appends it to state   |
| `toggleTodo`   | `(id: string) => void`                | Flips the `completed` flag of the given todo |
| `deleteTodo`   | `(id: string) => void`                | Removes the todo with the given id           |

**Renders:**

- An `<h1>` heading (e.g. "Todo App")
- `<TodoInput onAdd={addTodo} />`
- `<TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />`

---

### TodoInput (`src/components/TodoInput/TodoInput.tsx`)

**Props:**

```ts
interface TodoInputProps {
  onAdd: (text: string) => void;
}
```

**State:**

```ts
const [text, setText] = useState<string>('');
```

**Behaviour:**

- Wraps the input and button in a `<form>` element with an `onSubmit` handler.
- On submit (button click **or** Enter key):
  1. Trims the input text.
  2. If the trimmed text is empty, does **not** call `onAdd` (validation).
  3. Otherwise calls `onAdd(trimmedText)` and clears the input.
- Prevents the default form submission.

---

### TodoList (`src/components/TodoList/TodoList.tsx`)

**Props:**

```ts
interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

**Behaviour:**

- When `todos` is empty, renders an empty-state message (e.g. "No todos yet").
- Otherwise renders a `<ul>` with one `<TodoItem>` per todo.

---

### TodoItem (`src/components/TodoItem/TodoItem.tsx`)

**Props:**

```ts
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}
```

**Behaviour:**

- Renders a checkbox whose `checked` state reflects `todo.completed`.
- Clicking the checkbox calls `onToggle(todo.id)`.
- Renders the todo text; applies `text-decoration: line-through` when completed.
- Renders a delete button that calls `onDelete(todo.id)`.

---

## State Management

- **`useState` only** — no external state libraries.
- All state lives in the `App` component.
- Child components receive data and callbacks via props.

### CRUD Operations

| Operation  | Implementation                                                                                           |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| **Create** | `addTodo`: creates `{ id: crypto.randomUUID(), text, completed: false }` and appends to `todos`          |
| **Read**   | `todos` state array is passed down to `TodoList`                                                         |
| **Update** | `toggleTodo`: maps over `todos`, flipping `completed` for the matching id                                |
| **Delete** | `deleteTodo`: filters `todos` to exclude the matching id                                                 |

---

## Styling Strategy

- **CSS Modules** — each component has a co-located `.module.css` file.
- No global CSS framework; plain CSS with scoped class names.
- Completed todos receive a `line-through` text decoration.

---

## Testing Strategy

### Unit / Component Tests (Vitest + React Testing Library)

| Test File                                          | Test Name                                        |
| -------------------------------------------------- | ------------------------------------------------ |
| `src/components/App/App.test.tsx`                  | renders the app with heading                     |
| `src/components/App/App.test.tsx`                  | adds a new todo                                  |
| `src/components/App/App.test.tsx`                  | toggles a todo completed state                   |
| `src/components/App/App.test.tsx`                  | deletes a todo                                   |
| `src/components/App/App.test.tsx`                  | shows empty state when no todos                  |
| `src/components/TodoInput/TodoInput.test.tsx`      | renders input field and add button               |
| `src/components/TodoInput/TodoInput.test.tsx`      | calls onAdd with input text when submitted       |
| `src/components/TodoInput/TodoInput.test.tsx`      | clears input after submission                    |
| `src/components/TodoInput/TodoInput.test.tsx`      | does not call onAdd when input is empty          |
| `src/components/TodoList/TodoList.test.tsx`        | renders a list of todos                          |
| `src/components/TodoList/TodoList.test.tsx`        | renders empty state when todos array is empty    |
| `src/components/TodoItem/TodoItem.test.tsx`        | renders todo text                                |
| `src/components/TodoItem/TodoItem.test.tsx`        | renders checkbox reflecting completed state      |
| `src/components/TodoItem/TodoItem.test.tsx`        | calls onToggle when checkbox clicked             |
| `src/components/TodoItem/TodoItem.test.tsx`        | calls onDelete when delete button clicked        |
| `src/components/TodoItem/TodoItem.test.tsx`        | applies line-through style when completed        |

### File-Structure Tests (pytest)

Located in `tests/test_file_structure.py`. Validates that all expected files exist at the correct paths.

---

## Edge Cases & Validation

- **Empty todos are rejected:** `TodoInput` trims whitespace and refuses to call `onAdd` for empty strings.
- **Unique IDs:** `crypto.randomUUID()` is used — never `Math.random()` or incrementing integers.
- **No pre-populated data:** The `todos` array starts empty.
- **Keyboard accessibility:** The `<form>` element with `onSubmit` ensures both Enter key and button click trigger submission.
