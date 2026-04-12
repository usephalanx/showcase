# TodoApp — Architecture & Planning

## Overview

A cross-platform mobile Todo application built with React Native (Expo) and
TypeScript. Data is persisted locally via AsyncStorage. Navigation is handled
by React Navigation (native-stack).

---

## Tech Stack

| Layer          | Technology                                             |
| -------------- | ------------------------------------------------------ |
| Framework      | React Native 0.74 via Expo SDK 51                      |
| Language       | TypeScript 5.3 (strict mode)                           |
| Navigation     | @react-navigation/native + @react-navigation/native-stack |
| Local Storage  | @react-native-async-storage/async-storage              |
| Status Bar     | expo-status-bar                                        |
| Testing        | Jest (jest-expo) + @testing-library/react-native       |

---

## Data Model

```typescript
interface Todo {
  id: string;          // UUID v4 (generated via expo-crypto or lightweight uuid lib)
  title: string;       // Non-empty, whitespace-trimmed
  completed: boolean;  // Toggle on press
  createdAt: string;   // ISO 8601 via new Date().toISOString()
}
```

### Edge Cases

- **AsyncStorage limit**: Some platforms impose a ~6 MB limit. For very large
  todo lists, implement pagination or periodic cleanup of completed items.
- **UUID generation**: Use `expo-crypto` (`randomUUID()`) or a lightweight
  uuid library. Do NOT rely on `Math.random()` for id generation.
- **Timestamps**: Always generate with `new Date().toISOString()` for
  consistency across time zones.
- **Empty input**: `TodoInput` must `.trim()` the title and reject empty
  strings before calling `addTodo`.
- **Race conditions**: Multiple rapid `addTodo`/`deleteTodo` calls can cause
  data loss when concurrent reads and writes hit AsyncStorage. Mitigate with
  a sequential async queue or optimistic state updates with reconciliation
  on the storage layer.

---

## File & Folder Structure

```
mobile/
├── App.tsx                          # Root component, mounts NavigationContainer
├── app.json                         # Expo project config
├── babel.config.js                  # Babel preset for Expo
├── package.json                     # Dependencies & scripts
├── tsconfig.json                    # Strict TS config extending expo base
├── assets/                          # Icons, splash images
├── src/
│   ├── navigation/
│   │   └── AppNavigator.tsx         # NativeStackNavigator with route definitions
│   ├── screens/
│   │   └── HomeScreen.tsx           # Main screen: input + FlatList of todos
│   ├── components/
│   │   ├── TodoInput.tsx            # TextInput + Add button
│   │   ├── TodoList.tsx             # FlatList wrapper
│   │   └── TodoItem.tsx             # Single todo row (toggle, delete)
│   ├── hooks/
│   │   └── useTodos.ts              # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
│   ├── services/
│   │   └── storage.ts               # AsyncStorage CRUD: getTodos, saveTodos, addTodo, toggleTodo, deleteTodo
│   └── types/
│       └── todo.ts                  # Todo interface & related types
└── __tests__/                       # Test files mirroring src/ structure
    ├── services/
    │   └── storage.test.ts
    ├── hooks/
    │   └── useTodos.test.ts
    └── components/
        ├── TodoInput.test.tsx
        ├── TodoItem.test.tsx
        └── HomeScreen.test.tsx
```

---

## Component Hierarchy

```
App
└── NavigationContainer
    └── NativeStackNavigator
        └── HomeScreen
            ├── TodoInput          (TextInput + "Add" button)
            └── TodoList           (FlatList)
                └── TodoItem[]     (title, checkbox, delete affordance)
```

---

## Screen Specifications

### HomeScreen

- **Header**: "My Todos" (via navigation options)
- **Input area**: `TodoInput` component at the top
  - `TextInput` with placeholder "Add a new todo…"
  - "Add" button; disabled when input is empty/whitespace-only
- **List area**: `FlatList` rendering `TodoItem` components
  - **Tap** a `TodoItem` → toggle `completed` status
  - **Long press** a `TodoItem` → delete with confirmation
  - Empty state: centred text "No todos yet. Add one above!"
- **Loading state**: `ActivityIndicator` while `useTodos` loads from storage

---

## Storage Layer (`src/services/storage.ts`)

| Function       | Signature                                      | Description                          |
| -------------- | ---------------------------------------------- | ------------------------------------ |
| `getTodos`     | `() => Promise<Todo[]>`                        | Read & parse from AsyncStorage       |
| `saveTodos`    | `(todos: Todo[]) => Promise<void>`             | Serialise & write to AsyncStorage    |
| `addTodo`      | `(title: string) => Promise<Todo>`             | Create, append, persist, return new  |
| `toggleTodo`   | `(id: string) => Promise<Todo[]>`              | Flip `completed`, persist, return all|
| `deleteTodo`   | `(id: string) => Promise<Todo[]>`              | Remove by id, persist, return all    |

Storage key: `@TodoApp:todos`

---

## Custom Hook (`src/hooks/useTodos.ts`)

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}
```

- Loads todos from storage on mount via `useEffect`.
- Exposes mutation functions that update both local state and storage.
- Handles errors gracefully (console.error + optional user-facing alert).

---

## Navigation Structure

Single stack navigator (extensible for future detail/edit screens):

```typescript
type RootStackParamList = {
  Home: undefined;
  // Future: Detail: { todoId: string };
};
```

---

## Testing Strategy

| Scope         | Tool                                 | Focus                                    |
| ------------- | ------------------------------------ | ---------------------------------------- |
| Unit          | Jest                                 | `storage.ts` functions (mocked AsyncStorage) |
| Hook          | @testing-library/react-native        | `useTodos` state transitions             |
| Component     | @testing-library/react-native        | Render, user interaction, snapshot       |
| Integration   | @testing-library/react-native        | `HomeScreen` end-to-end flow             |

- AsyncStorage is mocked via `@react-native-async-storage/async-storage/jest/async-storage-mock`.
- All tests run with `npm test` (jest-expo preset).

---

## Future Considerations

- Add due dates and priority levels.
- Sync with a remote API (the existing FastAPI backend).
- Add swipe-to-delete gesture via `react-native-gesture-handler`.
- Dark mode support via `useColorScheme`.
