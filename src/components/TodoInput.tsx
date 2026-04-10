import React, { useState } from "react";

/**
 * Props for the TodoInput component.
 */
interface TodoInputProps {
  /** Callback invoked with the trimmed text when a new todo is submitted. */
  onAdd: (text: string) => void;
}

/**
 * A controlled input with a form that allows adding new todo items.
 *
 * - Calls `onAdd(text)` on form submission with the trimmed input value.
 * - Clears the input field after successful submission.
 * - Prevents adding empty or whitespace-only todos.
 */
const TodoInput: React.FC<TodoInputProps> = ({ onAdd }) => {
  const [text, setText] = useState<string>("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const trimmed = text.trim();
    if (trimmed.length === 0) {
      return;
    }
    onAdd(trimmed);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setText(e.target.value)
        }
        placeholder="Add a new todo"
      />
      <button type="submit">Add</button>
    </form>
  );
};

export default TodoInput;
