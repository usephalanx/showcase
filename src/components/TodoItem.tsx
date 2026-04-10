import React from "react";
import { Todo } from "../types/Todo";

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo object to render. */
  todo: Todo;
  /** Callback invoked with the todo's id when the checkbox is toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo's id when the delete button is clicked. */
  onDelete: (id: string) => void;
}

/**
 * Presentational component that renders a single todo item.
 *
 * Displays the todo text with a checkbox for toggling completion status
 * and a delete button for removing the item. When the todo is completed,
 * the text is rendered with a line-through style.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <li
      style={{
        display: "flex",
        alignItems: "center",
        gap: "8px",
        padding: "8px 0",
      }}
    >
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        aria-label={`Toggle ${todo.text}`}
      />
      <span
        style={{
          textDecoration: todo.completed ? "line-through" : "none",
          flex: 1,
        }}
      >
        {todo.text}
      </span>
      <button
        onClick={() => onDelete(todo.id)}
        aria-label={`Delete ${todo.text}`}
      >
        Delete
      </button>
    </li>
  );
};

export default TodoItem;
