import type { JSX } from "react";
import type { Todo } from "../../types/todo";

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback invoked with the todo id when the checkbox is toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo id when the delete button is clicked. */
  onDelete: (id: string) => void;
}

/**
 * TodoItem renders a single todo with a checkbox, text, and delete button.
 */
function TodoItem({ todo, onToggle, onDelete }: TodoItemProps): JSX.Element {
  return (
    <li className="todo-item">
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        className="todo-checkbox"
      />
      <span
        className="todo-text"
        style={{ textDecoration: todo.completed ? "line-through" : "none" }}
      >
        {todo.text}
      </span>
      <button
        onClick={() => onDelete(todo.id)}
        className="todo-delete-button"
      >
        Delete
      </button>
    </li>
  );
}

export default TodoItem;
