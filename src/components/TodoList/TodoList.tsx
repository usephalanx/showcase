import type { JSX } from "react";
import type { Todo } from "../../types/todo";
import TodoItem from "../TodoItem/TodoItem";

/**
 * Props for the TodoList component.
 */
export interface TodoListProps {
  /** Array of todos to display. */
  todos: Todo[];
  /** Callback invoked when a todo's completed state should be toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked when a todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * TodoList renders a list of TodoItem components, or an empty-state message.
 */
function TodoList({ todos, onToggle, onDelete }: TodoListProps): JSX.Element {
  if (todos.length === 0) {
    return <p className="todo-empty">No todos yet</p>;
  }

  return (
    <ul className="todo-list">
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
}

export default TodoList;
