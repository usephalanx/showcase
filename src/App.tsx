import { useState } from "react";
import type { JSX } from "react";
import type { Todo } from "./types/todo";
import TodoInput from "./components/TodoInput/TodoInput";
import TodoList from "./components/TodoList/TodoList";
import "./App.css";

/**
 * Root application component.
 *
 * Manages the full todo list state using useState<Todo[]>.
 * Provides addTodo, toggleTodo, and deleteTodo handlers
 * that are passed down to child components.
 */
function App(): JSX.Element {
  const [todos, setTodos] = useState<Todo[]>([]);

  /**
   * Add a new todo with a unique id generated via crypto.randomUUID().
   */
  const addTodo = (text: string): void => {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      text,
      completed: false,
    };
    setTodos((prev) => [...prev, newTodo]);
  };

  /**
   * Toggle the completed state of a todo by its id.
   */
  const toggleTodo = (id: string): void => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  /**
   * Delete a todo by its id.
   */
  const deleteTodo = (id: string): void => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <div className="app">
      <h1 className="app-heading">Todo App</h1>
      <TodoInput onAdd={addTodo} />
      <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </div>
  );
}

export default App;
