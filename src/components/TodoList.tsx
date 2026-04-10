import React from 'react';
import { Todo } from '../types/Todo';
import TodoItem from './TodoItem';

/**
 * Props for the TodoList component.
 */
interface TodoListProps {
  /** Array of todo items to display. */
  todos: Todo[];
  /** Callback to toggle a todo's completed status by id. */
  onToggle: (id: string) => void;
  /** Callback to delete a todo by id. */
  onDelete: (id: string) => void;
}

/**
 * Renders the list of todo items.
 *
 * Displays a message when the list is empty.
 */
function TodoList({ todos, onToggle, onDelete }: TodoListProps): React.JSX.Element {
  if (todos.length === 0) {
    return <p className="todo-empty">No todos yet. Add one above!</p>;
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
