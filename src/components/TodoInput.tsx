import React, { useState, FormEvent, ChangeEvent } from "react";

/**
 * Props for the TodoInput component.
 */
export interface TodoInputProps {
  /** Callback invoked with the trimmed text when a non-empty todo is submitted. */
  onAdd: (text: string) => void;
}

/**
 * TodoInput — a controlled input with a form that calls onAdd(text) on submit.
 *
 * Uses local useState for the input value. Clears the input after successful
 * submission. Prevents adding empty (or whitespace-only) todos.
 */
const TodoInput: React.FC<TodoInputProps> = ({ onAdd }) => {
  const [text, setText] = useState<string>("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setText(e.target.value);
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
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
        onChange={handleChange}
        placeholder="Add a new todo"
        aria-label="Todo text"
      />
      <button type="submit">Add</button>
    </form>
  );
};

export default TodoInput;
