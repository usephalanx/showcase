# React Native Todo App — Architecture Plan

## Tech Stack

| Layer          | Technology                                                                 |
| -------------- | -------------------------------------------------------------------------- |
| Framework      | React Native (Expo SDK 51)                                                 |
| Language       | TypeScript (strict mode)                                                   |
| Storage        | AsyncStorage (`@react-native-async-storage/async-storage`)                 |
| Navigation     | React Navigation (`@react-navigation/native` + `@react-navigation/native-stack`) |
| Testing        | Jest + React Native Testing Library                                        |
| ID Generation  | `expo-crypto` (`randomUUID`) or lightweight `uuid` library                 |

## Data Model

```typescript
interface Todo {
  id: string;        // UUID v4
  title: string;     // non-empty, trimmed
  completed: boolean;
  createdAt: string; // ISO 8601 via new Date().toISOString()
}
```

### Edge-case notes

- **AsyncStorage limit**: ~6 MB on some platforms. For very large lists consider pagination or periodic cleanup of completed items.
- **UUID generation**: Use `expo-crypto` or a dedicated `uuid` library — **never** `Math.random()`.
- **Timestamps**: Always generate with `new Date().toISOString()` for consistency.
- **Input validation**: `TodoInput` must `.trim()` input and reject empty strings.
- **Race conditions**: Multiple rapid `addTodo`/`deleteTodo` calls can interleave reads and writes to AsyncStorage, causing data loss. Mitigate by queuing operations sequentially (e.g. a promise chain or mutex) or using optimistic UI updates with reconciliation.

## Component Hierarchy

```
App
└── NavigationContainer
    └── NativeStackNavigator
        └── HomeScreen
            ├── TodoInput          (text input + add button)
            └── TodoList            (FlatList wrapper)
                └── TodoItem[]     (single todo row)
```

## File / Folder Structure

```
src/
├── types/
│   └── Todo.ts              # Todo interface
├── components/
│   ├── TodoItem.tsx          # Single todo row (toggle + delete)
│   ├── TodoInput.tsx         # Text input + add button
│   └── TodoList.tsx          # FlatList of TodoItem components
├── screens/
│   └── HomeScreen.tsx        # Main screen composing TodoInput + TodoList
├── hooks/
│   └── useTodos.ts           # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
├── services/
│   └── todoStorage.ts        # AsyncStorage CRUD: getTodos, saveTodos, addTodo, toggleTodo, deleteTodo
└── navigation/
    └── AppNavigator.tsx       # NativeStackNavigator with HomeScreen route
App.tsx                        # Entry point — wraps AppNavigator in NavigationContainer
```

## Storage Layer (`src/services/todoStorage.ts`)

| Function        | Signature                                    | Description                               |
| --------------- | -------------------------------------------- | ----------------------------------------- |
| `getTodos`      | `() => Promise<Todo[]>`                      | Read all todos from AsyncStorage          |
| `saveTodos`     | `(todos: Todo[]) => Promise<void>`           | Persist the full todo list                |
| `addTodo`       | `(title: string) => Promise<Todo>`           | Create, persist, and return a new todo    |
| `toggleTodo`    | `(id: string) => Promise<Todo[]>`            | Toggle `completed` and persist            |
| `deleteTodo`    | `(id: string) => Promise<Todo[]>`            | Remove by id and persist                  |

## Custom Hook (`src/hooks/useTodos.ts`)

Returns:

```typescript
{
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}
```

Loads todos on mount via `useEffect`. Each mutator calls the corresponding storage function and updates local state.

## Screen Specifications

### HomeScreen

- Renders `TodoInput` at the top and `TodoList` below.
- Consumes `useTodos()` hook.
- `TodoList` is a `FlatList` of `TodoItem` components.
- Pressing the checkbox on a `TodoItem` calls `toggleTodo(id)`.
- Pressing the delete button on a `TodoItem` calls `deleteTodo(id)`.

## Navigation

Single-stack navigator with one route (`Home`). Structure is intentionally extensible for future screens (e.g. `TodoDetail`).

## Testing Strategy

| Target              | Tool                          | Scope                                      |
| ------------------- | ----------------------------- | ------------------------------------------ |
| Components          | Jest + RNTL                   | Render, user interaction, conditional styles |
| Storage service     | Jest (mock AsyncStorage)      | CRUD correctness, empty-state handling      |
| Custom hook         | `renderHook` from RNTL        | State transitions, loading flag             |
| Navigation          | Jest + RNTL                   | Screen renders inside navigator             |
