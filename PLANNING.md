# PLANNING — React Native Todo App

## Tech Stack

- **Framework**: React Native (Expo SDK 51)
- **Language**: TypeScript (strict mode)
- **Storage**: AsyncStorage (`@react-native-async-storage/async-storage`)
- **Navigation**: React Navigation (`@react-navigation/native` + `@react-navigation/native-stack`)
- **Testing**: Jest + React Native Testing Library

## Data Model

```typescript
interface Todo {
  id: string;          // Generated via Date.now().toString()
  title: string;       // Non-empty, trimmed
  completed: boolean;  // Toggle state
  createdAt: string;   // ISO 8601 via new Date().toISOString()
}
```

## File / Folder Structure

```
src/
  types/
    Todo.ts                 # Todo interface definition
  services/
    storageService.ts       # AsyncStorage get/save helpers
  hooks/
    useTodos.ts             # Custom hook: full todo CRUD state
  components/
    TodoInput.tsx           # Text input + add button
    TodoItem.tsx            # Single todo row (toggle/delete)
    TodoList.tsx            # FlatList of TodoItem components
  screens/
    HomeScreen.tsx          # Main screen composing TodoInput + TodoList
  navigation/
    AppNavigator.tsx        # NativeStackNavigator setup
App.tsx                     # Root: NavigationContainer + AppNavigator
```

## Component Hierarchy

```
App
  └─ NavigationContainer
       └─ NativeStackNavigator
            └─ HomeScreen
                 ├─ TodoInput
                 └─ TodoList
                      └─ TodoItem[]
```

## Storage Layer

- **Key**: `@todos`
- **Format**: JSON-serialised `Todo[]`
- **Functions**:
  - `getTodos(): Promise<Todo[]>` — read & parse from AsyncStorage
  - `saveTodos(todos: Todo[]): Promise<void>` — serialise & write

### Notes

- AsyncStorage has a ~6 MB limit on some platforms. For large lists,
  consider pagination or periodic cleanup of completed items.
- Rapid sequential mutations (e.g. addTodo called twice before the
  first persist completes) can cause data loss because each mutation
  reads from the stale closure state. The current implementation uses
  React state as the source of truth and persists after each update,
  which is sufficient for typical usage. For high-frequency mutations,
  consider a sequential async queue or `useReducer` with middleware.

## Custom Hook: `useTodos`

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}
```

- Loads todos from `storageService.getTodos()` on mount via `useEffect`.
- Each mutation updates local `useState` and persists via `saveTodos`.
- `addTodo` trims whitespace and rejects empty strings.
- IDs are generated with `Date.now().toString()`.
- `createdAt` is generated with `new Date().toISOString()`.

## Screen Specifications

### HomeScreen

- Renders `TodoInput` at the top and `TodoList` below.
- `TodoList` uses `FlatList` for efficient rendering.
- **Toggle**: press a todo item to toggle its `completed` status.
- **Delete**: long press or swipe to delete.
- Shows a loading indicator while `useTodos` is loading.

## Navigation Structure

- Single-stack navigator with `HomeScreen` as the only route.
- Extensible for future screens (e.g. TodoDetailScreen).

## Testing Strategy

- **Unit tests**: `storageService` functions with mocked AsyncStorage.
- **Hook tests**: `useTodos` with `@testing-library/react-hooks`.
- **Component tests**: React Native Testing Library for TodoInput,
  TodoItem, TodoList, HomeScreen.
- **Snapshot tests**: optional, for UI regression detection.
