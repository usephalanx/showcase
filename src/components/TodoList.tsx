import React from "react";
import { Todo } from "../types/Todo";
import TodoItem from "./TodoItem";

/**
 * Props for the TodoList component.
 */
export interface TodoListProps {
  /** Array of todo items to display. */
  todos: Todo[];
  /** Callback invoked with a todo's id when the user toggles its completion status. */
  onToggle: (id: string) => void;
  /** Callback invoked with a todo's id when the user deletes it. */
  onDelete: (id: string) => void;
}

/**
 * Renders a list of todo items.
 *
 * Maps over the provided `todos` array and renders a `TodoItem` for each.
 * When the list is empty, displays a "No todos yet" message.
 */
const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete }) => {
  if (todos.length === 0) {
    return <p data-testid="empty-message">No todos yet</p>;
  }

  return (
    <ul className="todo-list" data-testid="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
};

export default TodoList;
