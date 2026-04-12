# React Native Todo App — Architecture Plan

## Tech Stack

- **Framework**: React Native (Expo SDK 51)
- **Language**: TypeScript (strict mode)
- **Storage**: AsyncStorage (`@react-native-async-storage/async-storage`)
- **Navigation**: React Navigation (`@react-navigation/native` + `@react-navigation/native-stack`)
- **Testing**: Jest + React Native Testing Library
- **ID Generation**: `expo-crypto` (`randomUUID()`) — avoid `Math.random()` for collision safety

## Data Model

```typescript
interface Todo {
  id: string;          // UUID v4 generated via expo-crypto
  title: string;       // Non-empty, whitespace-trimmed
  completed: boolean;  // Toggle state
  createdAt: string;   // ISO 8601 via new Date().toISOString()
}
```

### Edge Cases & Constraints

- **AsyncStorage limit**: ~6 MB on some platforms. For large lists, consider pagination or periodic cleanup of completed todos.
- **UUID generation**: Use `expo-crypto.randomUUID()` rather than `Math.random()`-based approaches for uniqueness guarantees.
- **Timestamps**: Always generate with `new Date().toISOString()` for consistency across time zones.
- **Input validation**: `TodoInput` must `trim()` whitespace and reject empty strings before creating a todo.
- **Race conditions**: Multiple rapid `addTodo`/`deleteTodo` calls could cause data loss with naive read-modify-write patterns. Recommend sequential async queue or optimistic updates with reconciliation against the persisted state.

## Component Hierarchy

```
App
└── NavigationContainer
    └── NativeStackNavigator
        └── HomeScreen
            ├── TodoInput          (text input + add button)
            └── TodoList           (FlatList wrapper)
                └── TodoItem[]     (individual todo rows)
```

## File / Folder Structure

```
src/
├── types/
│   └── Todo.ts                 # Todo interface definition
├── components/
│   ├── TodoItem.tsx            # Single todo row (toggle on tap, delete on long-press or button)
│   ├── TodoList.tsx            # FlatList wrapper with empty state
│   └── TodoInput.tsx           # Text input + add button
├── hooks/
│   └── useTodos.ts             # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
├── services/
│   └── todoStorage.ts          # AsyncStorage CRUD: getTodos, saveTodos, addTodo, toggleTodo, deleteTodo
├── screens/
│   └── HomeScreen.tsx          # Main screen composing TodoInput + TodoList
├── navigation/
│   └── AppNavigator.tsx        # Stack navigator (HomeScreen as sole route, extensible)
App.tsx                          # Entry point mounting NavigationContainer > AppNavigator
```

## Screen Specifications

### HomeScreen

- Renders `TodoInput` at the top and `TodoList` below.
- Consumes the `useTodos()` hook for state management.
- Shows a loading indicator while todos load from AsyncStorage.

### TodoInput

- Controlled `TextInput` with an "Add" button.
- Trims whitespace; disables add when input is empty.
- Clears input on successful add.

### TodoList

- `FlatList` with `keyExtractor` using `todo.id`.
- Renders `TodoItem` for each entry.
- `ListEmptyComponent` shows "No todos yet! Add one above." when list is empty.

### TodoItem

- Displays todo title (line-through when completed).
- Tap to toggle completion.
- Long-press or delete button to remove.

## Storage Layer (`todoStorage.ts`)

```typescript
const STORAGE_KEY = '@todos';

async function getTodos(): Promise<Todo[]>;
async function saveTodos(todos: Todo[]): Promise<void>;
async function addTodo(title: string): Promise<Todo>;
async function toggleTodo(id: string): Promise<Todo[]>;
async function deleteTodo(id: string): Promise<Todo[]>;
```

All functions use a read-modify-write pattern with `AsyncStorage.getItem` / `setItem`.

## Custom Hook (`useTodos.ts`)

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
};
```

- Loads todos on mount via `useEffect`.
- Exposes mutation functions that update both local state and AsyncStorage.
- Uses `useCallback` for stable references.

## Navigation Structure

- Single native-stack navigator with `HomeScreen` as the initial (and currently only) route.
- Extensible: additional screens (e.g. TodoDetailScreen, SettingsScreen) can be added to the stack.

## Testing Strategy

- **Component tests**: Jest + React Native Testing Library
  - `TodoItem`: renders title, applies completed styling, fires onToggle/onDelete.
  - `TodoList`: renders items, shows empty state, uses correct keys.
  - `TodoInput`: validates input, fires add callback, clears on submit.
  - `HomeScreen`: integration test composing all components.
- **Unit tests**: Jest
  - `todoStorage.ts`: mock AsyncStorage, verify CRUD operations.
  - `useTodos.ts`: mock storage, test hook state transitions via `renderHook`.
- **Coverage target**: 70%+ for all logic modules.
