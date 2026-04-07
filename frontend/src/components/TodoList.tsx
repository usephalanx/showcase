import React from 'react';

export interface Todo {
  id: string;
  text: string;
  completed: boolean;
  createdAt: number;
}

export interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

const TodoList: React.FC<TodoListProps> = ({ todos = [], onToggle, onDelete }) => {
  if (todos.length === 0) {
    return <p data-testid="empty-message">No todos yet!</p>;
  }

  return (
    <ul data-testid="todo-list">
      {todos.map((todo) => (
        <li key={todo.id} data-testid={`todo-item-${todo.id}`}>
          <label
            style={{
              textDecoration: todo.completed ? 'line-through' : 'none',
            }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => onToggle(todo.id)}
              data-testid={`todo-toggle-${todo.id}`}
            />
            <span data-testid={`todo-text-${todo.id}`}>{todo.text}</span>
          </label>
          <button
            onClick={() => onDelete(todo.id)}
            data-testid={`todo-delete-${todo.id}`}
            aria-label={`Delete ${todo.text}`}
          >
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
};

export default TodoList;
