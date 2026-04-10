import React from 'react';
import { Todo } from '../types';

/**
 * Props for the TodoItem component.
 */
interface TodoItemProps {
  todo: Todo;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

/**
 * Renders a single todo item with a checkbox, text, and delete button.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, toggleTodo, deleteTodo }) => {
  return (
    <div className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
        aria-label={`Toggle ${todo.text}`}
      />
      <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
        {todo.text}
      </span>
      <button
        className="delete-btn"
        onClick={() => deleteTodo(todo.id)}
        aria-label={`Delete ${todo.text}`}
      >
        ✕
      </button>
    </div>
  );
};

export default TodoItem;
