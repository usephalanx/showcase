import React from "react";
import type { Todo } from "../../types/todo";
import styles from "./TodoItem.module.css";

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo item to display. */
  todo: Todo;
  /** Callback invoked with the todo's id when the checkbox is toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo's id when the delete button is clicked. */
  onDelete: (id: string) => void;
}

/**
 * Displays a single todo item with a checkbox to toggle completion,
 * the todo text (with line-through styling when completed), and a
 * delete button.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <li className={styles.todoItem} data-testid={`todo-item-${todo.id}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        aria-label={`Toggle ${todo.text}`}
      />
      <span
        className={styles.todoText}
        style={{ textDecoration: todo.completed ? "line-through" : "none" }}
      >
        {todo.text}
      </span>
      <button
        onClick={() => onDelete(todo.id)}
        aria-label={`Delete ${todo.text}`}
        className={styles.deleteButton}
      >
        Delete
      </button>
    </li>
  );
};

export default TodoItem;
