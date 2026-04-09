import React from "react";
import { Todo } from "../../types/todo";

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback fired when the todo's completion status should be toggled. */
  onToggle: (id: string) => void;
  /** Callback fired when the todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * Renders a single todo item with a checkbox, text label, and delete button.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <li className="todo-item" data-testid="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        aria-label={`Toggle ${todo.text}`}
      />
      <span
        style={{
          textDecoration: todo.completed ? "line-through" : "none",
        }}
      >
        {todo.text}
      </span>
      <button onClick={() => onDelete(todo.id)} aria-label={`Delete ${todo.text}`}>
        Delete
      </button>
    </li>
  );
};

export default TodoItem;
