# Todo App — Architecture & Planning

## Tech Stack

- **Runtime**: React Native (Expo SDK 51)
- **Language**: TypeScript (strict mode)
- **Navigation**: React Navigation v6 (`@react-navigation/native`, `@react-navigation/native-stack`)
- **Storage**: AsyncStorage (`@react-native-async-storage/async-storage`)
- **Testing**: Jest + React Native Testing Library

## Data Model

```typescript
interface Todo {
  id: string;          // UUID (generated via expo-crypto or lightweight uuid lib)
  title: string;       // Non-empty, trimmed
  completed: boolean;
  createdAt: string;   // ISO 8601 via new Date().toISOString()
}
```

### Edge Cases

- **Storage limit**: AsyncStorage may have a ~6 MB limit on some platforms. For large todo lists, consider pagination or periodic cleanup.
- **UUID generation**: Use `expo-crypto` or a lightweight uuid library rather than `Math.random`-based approaches.
- **Timestamps**: Always generate `createdAt` with `new Date().toISOString()` for consistency.
- **Input validation**: `TodoInput` must trim whitespace and reject empty strings before creating a todo.
- **Race conditions**: Multiple rapid `addTodo`/`deleteTodo` calls could cause data loss. Use a sequential async queue or optimistic updates with reconciliation.

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
/
├── App.tsx                              # Root component: StatusBar + NavigationContainer + AppNavigator
├── src/
│   ├── navigation/
│   │   ├── AppNavigator.tsx             # Native stack navigator definition
│   │   └── types.ts                     # Navigation type definitions (RootStackParamList)
│   ├── screens/
│   │   └── HomeScreen.tsx               # Main screen with todo list and input
│   ├── components/
│   │   ├── TodoInput.tsx                # Text input + add button
│   │   ├── TodoList.tsx                 # FlatList wrapper for todos
│   │   └── TodoItem.tsx                 # Single todo row (toggle on press, delete on long press)
│   ├── hooks/
│   │   └── useTodos.ts                  # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
│   ├── services/
│   │   └── todoStorage.ts              # AsyncStorage service: getTodos, saveTodos, addTodo, toggleTodo, deleteTodo
│   └── types/
│       └── todo.ts                      # Todo interface definition
├── PLANNING.md
├── RUNNING.md
└── package.json
```

## Screen Specifications

### HomeScreen

- **Title**: "Todo App" (set via navigation options)
- **Layout**: `TodoInput` at the top, `TodoList` filling the remaining space
- **Interactions**:
  - Type text and tap Add to create a todo
  - Tap a todo to toggle its completed status
  - Long press a todo to delete it
- **State**: Managed via `useTodos()` custom hook
- **Loading**: Show an ActivityIndicator while todos load from AsyncStorage

## Navigation Structure

- Single native stack navigator with `HomeScreen` as the only route
- Structured with `RootStackParamList` type for type-safe navigation
- Extensible: add new screens by extending the param list and adding `Stack.Screen` entries

## Storage Layer

All functions in `todoStorage.ts` operate on the `@todos` AsyncStorage key:

- `getTodos(): Promise<Todo[]>` — read and parse stored todos
- `saveTodos(todos: Todo[]): Promise<void>` — serialize and write todos
- `addTodo(title: string): Promise<Todo>` — create, append, save, return new todo
- `toggleTodo(id: string): Promise<Todo[]>` — flip completed, save, return updated list
- `deleteTodo(id: string): Promise<Todo[]>` — remove by id, save, return updated list

## Custom Hook: useTodos

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}
```

## Testing Strategy

- **Unit tests**: `todoStorage.ts` functions with mocked AsyncStorage
- **Component tests**: `TodoInput`, `TodoItem`, `TodoList` with React Native Testing Library
- **Screen tests**: `HomeScreen` integration tests with mocked storage
- **Navigation tests**: Verify `AppNavigator` renders `HomeScreen` with correct title
