import React from 'react';
import { Todo } from '../types';
import TodoItem from './TodoItem';

/**
 * Props for the TodoList component.
 */
interface TodoListProps {
  todos: Todo[];
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

/**
 * Renders the list of todo items, or a message if the list is empty.
 */
const TodoList: React.FC<TodoListProps> = ({ todos, toggleTodo, deleteTodo }) => {
  if (todos.length === 0) {
    return <p className="todo-list-empty">No todos yet. Add one above!</p>;
  }

  return (
    <div className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          toggleTodo={toggleTodo}
          deleteTodo={deleteTodo}
        />
      ))}
    </div>
  );
};

export default TodoList;
