/**
 * TodoPage — main page component for the Todo application.
 *
 * Composes TodoInput, TodoFilter, and TodoList into a single page.
 * Manages top-level state for the todo list and active filter.
 */
import React, { useState } from 'react';

import { Todo, FilterType } from '../types/todo';
import { filterTodos } from '../utils/filterTodos';
import TodoInput from '../components/TodoInput';
import TodoFilter from '../components/TodoFilter';
import TodoList from '../components/TodoList';

const TodoPage: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<FilterType>('all');

  const handleAdd = (text: string) => {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      text,
      completed: false,
      createdAt: Date.now(),
    };
    setTodos((prev) => [newTodo, ...prev]);
  };

  const handleToggle = (id: string) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const handleDelete = (id: string) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  const remainingCount = todos.filter((todo) => !todo.completed).length;
  const filteredTodos = filterTodos(todos, filter);

  return (
    <main
      className="todo-page"
      style={{
        maxWidth: 600,
        margin: '0 auto',
        padding: '2rem 1rem',
      }}
    >
      <h1 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Todo App</h1>
      <TodoInput onAdd={handleAdd} />
      <TodoFilter
        currentFilter={filter}
        onFilterChange={setFilter}
        remainingCount={remainingCount}
      />
      <TodoList
        todos={filteredTodos}
        onToggle={handleToggle}
        onDelete={handleDelete}
      />
    </main>
  );
};

export default TodoPage;
