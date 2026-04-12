# Todo Mobile App — Architecture Plan

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | React Native (Expo SDK 51) |
| Language | TypeScript |
| Persistence | AsyncStorage (`@react-native-async-storage/async-storage`) |
| Navigation | React Navigation (`@react-navigation/native` + `@react-navigation/native-stack`) |
| ID Generation | `expo-crypto` (`randomUUID`) or lightweight `uuid` library |
| Testing | Jest + React Native Testing Library |

## Data Model

### Todo

```typescript
interface Todo {
  id: string;         // UUID v4
  title: string;      // Non-empty, trimmed
  completed: boolean;
  createdAt: string;  // ISO 8601 via new Date().toISOString()
}
```

## File / Folder Structure

```
src/
  types/
    todo.ts                 # Todo interface definition
  services/
    storageService.ts       # AsyncStorage read/write (getTodos, saveTodos)
  hooks/
    useTodos.ts             # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
  components/
    TodoInput.tsx           # Text input + Add button
    TodoItem.tsx            # Single todo row (tap to toggle, long-press to delete)
    TodoList.tsx            # FlatList wrapper
  screens/
    HomeScreen.tsx          # Main screen composing TodoInput + TodoList
  navigation/
    AppNavigator.tsx        # NativeStackNavigator with HomeScreen
App.tsx                     # Entry point: NavigationContainer + AppNavigator
```

## Component Hierarchy

```
App
 └── NavigationContainer
      └── NativeStackNavigator
           └── HomeScreen
                ├── TodoInput
                └── TodoList
                     └── TodoItem[]
```

## Storage Layer

All persistence goes through `src/services/storageService.ts`:

| Function | Signature | Description |
|---|---|---|
| `getTodos` | `() => Promise<Todo[]>` | Load & deserialize todos; returns `[]` on error |
| `saveTodos` | `(todos: Todo[]) => Promise<void>` | Serialize & persist full list |

Storage key: `TODOS_STORAGE_KEY`.

## Custom Hook — `useTodos()`

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

Internally loads todos on mount, calls `saveTodos` after every mutation.

## Screen Specifications

### HomeScreen

- **TodoInput**: text field with "Add" button. Trims whitespace; rejects empty strings.
- **TodoList**: `FlatList` rendering `TodoItem` components.
- **TodoItem**: tap toggles `completed`; long-press deletes.

## Navigation

Single-stack navigator with `HomeScreen` as the sole route. Extensible for future detail/edit screens.

## Edge Cases & Notes

1. **AsyncStorage size limit**: ~6 MB on some platforms. For very large lists, consider pagination or periodic cleanup.
2. **UUID generation**: Use `expo-crypto.randomUUID()` or the `uuid` package — never `Math.random()`.
3. **Date consistency**: Always generate `createdAt` with `new Date().toISOString()`.
4. **Input validation**: `TodoInput` must `.trim()` input and reject empty strings before creating a todo.
5. **Race conditions**: Rapid sequential `addTodo`/`deleteTodo` calls could cause data loss if they read stale state. Mitigate by serializing async operations (queue) or using optimistic updates with reconciliation against the stored state.

## Testing Strategy

- **Unit tests** for `storageService.ts` (mock AsyncStorage).
- **Unit tests** for `useTodos` hook.
- **Component tests** for `TodoInput`, `TodoItem`, `TodoList`, `HomeScreen` via React Native Testing Library.
