import React, { useState } from 'react';
import { Todo } from './types/Todo';
import TodoInput from './components/TodoInput';
import TodoList from './components/TodoList';
import './App.css';

/**
 * Root application component.
 *
 * Owns the todo list state and provides addTodo, toggleTodo, and deleteTodo
 * callbacks that are passed down to child components via props.
 */
function App(): React.JSX.Element {
  const [todos, setTodos] = useState<Todo[]>([]);

  /**
   * Add a new todo with the given text.
   * Generates a unique id using crypto.randomUUID().
   */
  const addTodo = (text: string): void => {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      text,
      completed: false,
    };
    setTodos((prev) => [newTodo, ...prev]);
  };

  /**
   * Toggle the completed boolean of the todo with the given id.
   */
  const toggleTodo = (id: string): void => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  /**
   * Delete the todo with the given id.
   */
  const deleteTodo = (id: string): void => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <div className="app-container">
      <h1>Todo App</h1>
      <TodoInput onAdd={addTodo} />
      <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </div>
  );
}

export default App;
