import React, { useState } from 'react';

/**
 * Props for the TodoInput component.
 */
interface TodoInputProps {
  addTodo: (text: string) => void;
}

/**
 * Input form for creating new todo items.
 *
 * Trims whitespace from the input and prevents adding empty todos.
 */
const TodoInput: React.FC<TodoInputProps> = ({ addTodo }) => {
  const [text, setText] = useState<string>('');

  const handleSubmit = (e: React.FormEvent): void => {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed.length === 0) {
      return;
    }
    addTodo(trimmed);
    setText('');
  };

  return (
    <form className="todo-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new todo..."
        aria-label="Todo text"
      />
      <button type="submit">Add</button>
    </form>
  );
};

export default TodoInput;
