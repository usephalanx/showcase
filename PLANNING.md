# React Native Todo App — Architecture Plan

## Tech Stack

| Layer           | Technology                                              |
| --------------- | ------------------------------------------------------- |
| Framework       | React Native (Expo SDK 51)                              |
| Language        | TypeScript (strict mode)                                |
| Navigation      | @react-navigation/native + @react-navigation/native-stack |
| Persistence     | @react-native-async-storage/async-storage               |
| ID Generation   | expo-crypto (`randomUUID`) or `uuid` (lightweight)      |
| Testing         | Jest + React Native Testing Library                     |

## Data Model

```typescript
export interface Todo {
  /** Universally unique identifier (v4 UUID). */
  id: string;
  /** Short description of the task. */
  title: string;
  /** Whether the task has been completed. */
  completed: boolean;
  /** ISO 8601 timestamp created with `new Date().toISOString()`. */
  createdAt: string;
}
```

### Notes

- `createdAt` is always generated via `new Date().toISOString()` for consistency.
- UUID generation MUST use `expo-crypto` or the `uuid` library — never `Math.random()`.
- AsyncStorage has a practical limit of ~6 MB on some platforms. For very large
  todo lists, consider pagination or periodic cleanup of completed items.

## Component Hierarchy

```
App
└── NavigationContainer
    └── NativeStackNavigator
        └── HomeScreen
            ├── TodoInput          (text input + "Add" button)
            └── TodoList           (FlatList of TodoItem)
                └── TodoItem[]     (single row: title, checkbox, delete)
```

## File / Folder Structure

```
/
├── App.tsx                         # Entry point; wraps NavigationContainer
├── src/
│   ├── components/
│   │   ├── TodoInput.tsx           # Controlled text input + Add button
│   │   ├── TodoItem.tsx            # Single todo row (toggle / delete)
│   │   └── TodoList.tsx            # FlatList wrapper around TodoItem[]
│   ├── screens/
│   │   └── HomeScreen.tsx          # Main screen composing Input + List
│   ├── hooks/
│   │   └── useTodos.ts             # Custom hook: CRUD + loading state
│   ├── services/
│   │   └── storage.ts              # AsyncStorage helpers (get/save/add/toggle/delete)
│   ├── types/
│   │   └── Todo.ts                 # Todo interface
│   └── navigation/
│       └── AppNavigator.tsx        # Stack navigator definition
├── PLANNING.md                     # This file
├── RUNNING.md                      # Setup & run instructions
└── package.json
```

## Storage Layer — `src/services/storage.ts`

| Function      | Signature                                       | Purpose                          |
| ------------- | ----------------------------------------------- | -------------------------------- |
| getTodos      | `() => Promise<Todo[]>`                          | Read all todos from AsyncStorage |
| saveTodos     | `(todos: Todo[]) => Promise<void>`               | Overwrite the full list          |
| addTodo       | `(title: string) => Promise<Todo>`               | Append a new todo and persist    |
| toggleTodo    | `(id: string) => Promise<Todo[]>`                | Flip `completed` and persist     |
| deleteTodo    | `(id: string) => Promise<Todo[]>`                | Remove a todo and persist        |

### Concurrency / Race Condition

Multiple rapid `addTodo`/`deleteTodo` calls can cause data loss because
each function reads → mutates → writes the full list independently.
Mitigation strategies:

1. **Sequential queue** — wrap all storage mutations behind an async queue
   (e.g. `p-queue` with concurrency 1).
2. **Optimistic updates with reconciliation** — update UI state immediately,
   persist in background, and reconcile on error.

The initial implementation will use a sequential queue inside `useTodos`.

## Custom Hook — `src/hooks/useTodos.ts`

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
};
```

- On mount, calls `getTodos()` and sets `loading = false` when done.
- Each mutation updates local state optimistically, then persists.

## Screen Specifications — HomeScreen

| Interaction        | Behaviour                                      |
| ------------------ | ---------------------------------------------- |
| Add button / enter | Call `addTodo(trimmedTitle)`. Reject empty.     |
| Press todo row     | Toggle `completed` status.                     |
| Long-press / swipe | Delete the todo (with optional confirmation).   |

## Navigation

Single-stack navigator with `HomeScreen` as the only route. The stack is
designed to be extended with additional screens (e.g. TodoDetailScreen) in
future iterations.

## Edge Cases

- **Empty input**: `TodoInput` trims whitespace and silently rejects empty strings.
- **Duplicate titles**: Allowed — each todo has a unique UUID.
- **AsyncStorage 6 MB limit**: Monitor list size; implement cleanup for completed
  items older than a configurable threshold.
- **Rapid mutations**: Handled via sequential async queue (see above).

## Testing Strategy

| Layer       | Tool                             | Focus                                  |
| ----------- | -------------------------------- | -------------------------------------- |
| Components  | Jest + RNTL                      | Render, user interaction, callbacks    |
| Hooks       | `@testing-library/react-hooks`   | State transitions, async flow          |
| Services    | Jest (mock AsyncStorage)         | Serialisation, error handling          |
| Integration | Detox (future)                   | End-to-end flows on real device / sim  |
