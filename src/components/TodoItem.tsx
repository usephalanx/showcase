import React from 'react';
import { Todo } from '../types/Todo';

/**
 * Props for the TodoItem component.
 */
interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback to toggle the completed status of this todo. */
  onToggle: (id: string) => void;
  /** Callback to delete this todo. */
  onDelete: (id: string) => void;
}

/**
 * Renders a single todo item with a checkbox, text, and delete button.
 *
 * Completed items are displayed with a line-through style.
 */
function TodoItem({ todo, onToggle, onDelete }: TodoItemProps): React.JSX.Element {
  return (
    <li className={`todo-item${todo.completed ? ' completed' : ''}`}>
      <label className="todo-label">
        <input
          type="checkbox"
          className="todo-checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
        />
        <span className="todo-text">{todo.text}</span>
      </label>
      <button
        type="button"
        className="todo-delete-btn"
        onClick={() => onDelete(todo.id)}
      >
        Delete
      </button>
    </li>
  );
}

export default TodoItem;
