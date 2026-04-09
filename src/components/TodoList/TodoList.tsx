import React from "react";
import { Todo } from "../../types/todo";
import TodoItem from "../TodoItem/TodoItem";

/**
 * Props for the TodoList component.
 */
export interface TodoListProps {
  /** Array of todo items to display. */
  todos: Todo[];
  /** Callback fired when a todo's completion status should be toggled. */
  onToggle: (id: string) => void;
  /** Callback fired when a todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * Renders a list of TodoItem components.
 *
 * When the todos array is empty, displays a "No todos yet" message.
 * Otherwise, maps over the array and renders a TodoItem for each entry.
 */
const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete }) => {
  if (todos.length === 0) {
    return <p data-testid="empty-message">No todos yet</p>;
  }

  return (
    <ul data-testid="todo-list">
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
