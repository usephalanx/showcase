import React, { useState } from 'react';

/**
 * Props for the TodoInput component.
 */
interface TodoInputProps {
  /** Callback invoked with the trimmed text when the user submits a new todo. */
  onAdd: (text: string) => void;
}

/**
 * Input component that allows users to type and submit new todo items.
 *
 * Prevents adding empty or whitespace-only todos.
 */
function TodoInput({ onAdd }: TodoInputProps): React.JSX.Element {
  const [text, setText] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed.length === 0) {
      return;
    }
    onAdd(trimmed);
    setText('');
  };

  return (
    <form className="todo-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="todo-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new todo..."
      />
      <button type="submit" className="todo-add-btn">
        Add
      </button>
    </form>
  );
}

export default TodoInput;
