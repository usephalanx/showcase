import React from "react";
import { Todo } from "../types/Todo";

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback invoked with the todo id when the user toggles completion. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo id when the user deletes the item. */
  onDelete: (id: string) => void;
}

/**
 * Renders a single todo item with toggle and delete controls.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <li className="todo-item" data-testid={`todo-item-${todo.id}`}>
      <label
        style={{
          textDecoration: todo.completed ? "line-through" : "none",
          cursor: "pointer",
          flex: 1,
        }}
      >
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          aria-label={`Toggle ${todo.text}`}
        />
        <span>{todo.text}</span>
      </label>
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
