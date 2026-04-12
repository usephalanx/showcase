# Todo App — Architecture & Planning

## Overview

A cross-platform mobile Todo application built with React Native and Expo.
Users can create, complete, and delete todo items. All data is persisted
locally on-device using AsyncStorage.

---

## Tech Stack

| Layer | Technology | Version / Notes |
|---|---|---|
| Framework | React Native (Expo SDK 51) | Managed workflow |
| Language | TypeScript | Strict mode enabled |
| Navigation | `@react-navigation/native` + `@react-navigation/native-stack` | Single-stack navigator |
| Persistence | `@react-native-async-storage/async-storage` | Key-value local storage |
| Testing | Jest + React Native Testing Library | Unit & component tests |

---

## Data Model

### `Todo` Interface

```typescript
interface Todo {
  id: string;          // UUID — generated with expo-crypto or a lightweight uuid library
  title: string;       // Non-empty, whitespace-trimmed
  completed: boolean;  // Toggled on press
  createdAt: string;   // ISO 8601 — generated with new Date().toISOString()
}
```

### Storage Key

```
@todo-app/todos
```

Todos are serialised as a JSON array under a single AsyncStorage key.

> **Note:** AsyncStorage has a ~6 MB limit on some platforms. For large
> todo lists, consider pagination or periodic cleanup of completed items.

---

## Component Hierarchy

```
App
└── NavigationContainer
    └── NativeStackNavigator
        └── HomeScreen
            ├── TodoInput          (TextInput + Add button)
            └── TodoList           (FlatList wrapper)
                └── TodoItem[]     (Single todo row — tap to toggle, long-press to delete)
```

---

## File / Folder Structure

```
.
├── App.tsx                        # Entry point — sets up NavigationContainer & stack navigator
├── app.json                       # Expo configuration
├── tsconfig.json                  # TypeScript configuration
├── package.json                   # Dependencies & scripts
│
├── src/
│   ├── types/
│   │   └── todo.ts                # Todo interface definition
│   │
│   ├── services/
│   │   └── storage.ts             # AsyncStorage CRUD helpers (getTodos, saveTodos, addTodo, toggleTodo, deleteTodo)
│   │
│   ├── hooks/
│   │   └── useTodos.ts            # Custom hook: { todos, loading, addTodo, toggleTodo, deleteTodo }
│   │
│   ├── components/
│   │   ├── TodoInput.tsx          # Text input + add button; trims whitespace, rejects empty strings
│   │   ├── TodoList.tsx           # FlatList rendering TodoItem components
│   │   └── TodoItem.tsx           # Single todo row with toggle (onPress) and delete (onLongPress)
│   │
│   └── screens/
│       └── HomeScreen.tsx         # Composes TodoInput + TodoList; consumes useTodos hook
│
├── __tests__/
│   ├── storage.test.ts            # Unit tests for services/storage.ts
│   ├── useTodos.test.ts           # Hook tests with renderHook
│   ├── TodoInput.test.tsx         # Component tests
│   ├── TodoItem.test.tsx          # Component tests
│   └── HomeScreen.test.tsx        # Integration-level component tests
│
├── PLANNING.md                    # This file
└── RUNNING.md                     # Setup & run instructions
```

---

## Screen Definitions

### HomeScreen

| Element | Behaviour |
|---|---|
| **TodoInput** | Text field + "Add" button. Trims whitespace; rejects empty strings. Clears input on successful add. |
| **TodoList** | `FlatList` of `TodoItem` components. Shows a placeholder message when the list is empty. |
| **TodoItem** | Displays title with a strike-through when completed. **Tap** toggles completion. **Long-press** triggers a confirmation dialog, then deletes. |
| **Loading state** | A spinner is shown while todos are being loaded from AsyncStorage on first mount. |

---

## Storage Layer — `services/storage.ts`

```typescript
// All functions are async and operate on the @todo-app/todos key.

getTodos(): Promise<Todo[]>
saveTodos(todos: Todo[]): Promise<void>
addTodo(title: string): Promise<Todo[]>
toggleTodo(id: string): Promise<Todo[]>
deleteTodo(id: string): Promise<Todo[]>
```

Each mutating function (add, toggle, delete) reads the current list,
applies the change, writes back, and returns the updated list.

> **Race condition note:** Multiple rapid calls to add/toggle/delete
> could cause data loss because each call reads → modifies → writes
> independently. Mitigations:
> 1. Use a sequential async queue (recommended) to serialise writes.
> 2. Use optimistic UI updates in the hook and reconcile on write
>    completion.

---

## Custom Hook — `hooks/useTodos.ts`

```typescript
function useTodos(): {
  todos: Todo[];
  loading: boolean;
  addTodo: (title: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}
```

- On mount, calls `getTodos()` and sets `loading = false` when complete.
- Each action updates local state optimistically, then persists.

---

## Navigation Structure

```typescript
type RootStackParamList = {
  Home: undefined;
  // Extensible — add Detail, Settings, etc. here later.
};
```

Single-stack navigator with `HomeScreen` as the initial (and currently only) route.

---

## ID Generation

Use `expo-crypto` (`Crypto.randomUUID()`) or a lightweight library such
as `uuid` (v4). **Do not** use `Math.random()` — it does not produce
cryptographically unique identifiers and may collide.

---

## Edge Cases & Constraints

| Concern | Handling |
|---|---|
| Empty / whitespace-only title | `TodoInput` trims input and disables the add button when empty |
| AsyncStorage 6 MB limit | Recommend cleanup of old completed items for very large lists |
| Rapid concurrent mutations | Sequential async queue or optimistic updates with reconciliation |
| `createdAt` consistency | Always generated via `new Date().toISOString()` |
| UUID generation | Use `expo-crypto` or `uuid` — never `Math.random()` |

---

## Testing Strategy

| Scope | Tool | What is tested |
|---|---|---|
| Unit | Jest | `services/storage.ts` — mock AsyncStorage, verify CRUD logic |
| Hook | Jest + `@testing-library/react-hooks` | `useTodos` — loading state, add/toggle/delete flows |
| Component | Jest + React Native Testing Library | `TodoInput`, `TodoItem`, `HomeScreen` — rendering, user interaction |
| Manual / E2E | Expo Go on device | Full workflow: add → toggle → delete → restart app → verify persistence |
