# React Native Todo App — Architecture Plan

## Tech Stack

- **Framework**: React Native (Expo SDK 51)
- **Language**: TypeScript (strict mode)
- **Storage**: AsyncStorage (`@react-native-async-storage/async-storage`)
- **Navigation**: React Navigation (`@react-navigation/native` + `@react-navigation/native-stack`)
- **Testing**: Jest + React Native Testing Library

## Data Model

```typescript
interface Todo {
  id: string;          // Unique ID (timestamp + random hex)
  title: string;       // Todo title text
  completed: boolean;  // Completion status
  createdAt: string;   // ISO 8601 timestamp
}
```

### Notes on Data Model

- `id` is generated using `Date.now().toString(36)` combined with random hex characters. For production, consider `expo-crypto` (`randomUUID()`) for cryptographically strong UUIDs.
- `createdAt` is generated via `new Date().toISOString()` for consistency across time zones.
- AsyncStorage has a ~6MB limit on some platforms. For very large todo lists, consider pagination or periodic cleanup of completed/old items.

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

## File Structure

```
src/
├── components/
│   ├── TodoInput.tsx      # Text input + Add button
│   ├── TodoItem.tsx       # Single todo row (toggle + delete)
│   └── TodoList.tsx       # FlatList of TodoItems with empty state
├── hooks/
│   └── useTodos.ts        # Custom hook: state + CRUD + persistence
├── screens/
│   └── HomeScreen.tsx     # Main screen composing TodoInput + TodoList
├── services/
│   └── todoStorage.ts     # AsyncStorage load/save/generateId
└── types/
    └── Todo.ts            # Todo interface definition
```

## Screen Specifications

### HomeScreen

- Uses `useTodos()` hook for all state management
- Renders `SafeAreaView` container with flex: 1
- Displays "My Todos" header (large, bold text)
- Shows `ActivityIndicator` while `loading` is true
- Renders `TodoInput` wired to `addTodo`
- Renders `TodoList` wired to `todos`, `toggleTodo`, `deleteTodo`

## Storage Layer

- `loadTodos()`: Read from AsyncStorage, parse JSON, return `Todo[]` (empty array on failure)
- `saveTodos(todos)`: Serialize and write full list to AsyncStorage
- `generateId()`: Timestamp + random hex ID generation

## Custom Hook: `useTodos()`

Returns:
- `todos: Todo[]` — current list
- `loading: boolean` — true during initial load
- `addTodo(title: string): Promise<void>` — trims whitespace, rejects empty
- `toggleTodo(id: string): Promise<void>` — flips `completed`
- `deleteTodo(id: string): Promise<void>` — removes from list

All mutations use optimistic state updates followed by async persistence.

## Edge Cases & Design Decisions

1. **Empty input**: `TodoInput` trims whitespace and silently rejects empty strings.
2. **Race conditions**: Mutations use React's functional `setState` form (`setTodos(prev => ...)`) to avoid stale-state bugs with rapid successive calls. `saveTodos` is called inside the updater to capture the latest state.
3. **Storage limits**: AsyncStorage may have a ~6MB limit. For large lists, implement pagination or cleanup.
4. **ID generation**: Uses timestamp + random for simplicity. Upgrade to `expo-crypto.randomUUID()` for production.
5. **Error handling**: Storage load failures fall back to an empty list. Save failures are silent (fire-and-forget) to keep the UI responsive.

## Navigation Structure

Single-stack navigator with `HomeScreen` as the only route. Extensible for future screens (e.g., TodoDetailScreen, SettingsScreen).

## Testing Strategy

- **Component tests**: Jest + React Native Testing Library for TodoInput, TodoItem, TodoList, HomeScreen
- **Hook tests**: `renderHook` for useTodos with mocked AsyncStorage
- **Service tests**: Unit tests for todoStorage functions with mocked AsyncStorage
- **Coverage target**: 70%+
