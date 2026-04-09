import { useState, type FormEvent, type JSX } from "react";

/**
 * Props for the TodoInput component.
 */
export interface TodoInputProps {
  /** Callback invoked with the trimmed text when a new todo is submitted. */
  onAdd: (text: string) => void;
}

/**
 * TodoInput renders a form with a text input and submit button.
 * It validates that the input is non-empty before calling onAdd.
 */
function TodoInput({ onAdd }: TodoInputProps): JSX.Element {
  const [text, setText] = useState<string>("");

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
    <form onSubmit={handleSubmit} className="todo-input-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new todo..."
        className="todo-input"
      />
      <button type="submit" className="todo-input-button">
        Add
      </button>
    </form>
  );
}

export default TodoInput;
