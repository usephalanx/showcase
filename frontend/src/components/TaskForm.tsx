import React, { useState, FormEvent, ChangeEvent } from "react";

/**
 * Represents the data submitted by the TaskForm.
 */
export interface TaskFormData {
  title: string;
  status: "todo" | "in-progress" | "done";
  due_date: string;
}

/**
 * Props for the TaskForm component.
 */
export interface TaskFormProps {
  /** Callback invoked with form data on valid submission. */
  onSubmit: (data: TaskFormData) => void;
  /** Optional initial values to pre-populate the form (edit mode). */
  initialValues?: Partial<TaskFormData>;
}

const STATUS_OPTIONS: { value: TaskFormData["status"]; label: string }[] = [
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

/**
 * A form component for creating or editing tasks.
 *
 * When `initialValues` is provided the form operates in edit mode and
 * the submit button reads "Update Task"; otherwise it reads "Add Task".
 */
export default function TaskForm({
  onSubmit,
  initialValues,
}: TaskFormProps): React.ReactElement {
  const isEditMode = initialValues !== undefined;

  const [title, setTitle] = useState<string>(initialValues?.title ?? "");
  const [status, setStatus] = useState<TaskFormData["status"]>(
    initialValues?.status ?? "todo"
  );
  const [dueDate, setDueDate] = useState<string>(
    initialValues?.due_date ?? ""
  );
  const [titleError, setTitleError] = useState<string>("");

  const validate = (): boolean => {
    if (!title.trim()) {
      setTitleError("Title is required");
      return false;
    }
    setTitleError("");
    return true;
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    if (!validate()) {
      return;
    }
    onSubmit({
      title: title.trim(),
      status,
      due_date: dueDate,
    });
  };

  const handleTitleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setTitle(e.target.value);
    if (titleError && e.target.value.trim()) {
      setTitleError("");
    }
  };

  const handleStatusChange = (e: ChangeEvent<HTMLSelectElement>): void => {
    setStatus(e.target.value as TaskFormData["status"]);
  };

  const handleDueDateChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setDueDate(e.target.value);
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Task form">
      <div>
        <label htmlFor="task-title">Title</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={handleTitleChange}
          placeholder="Enter task title"
          aria-required="true"
          aria-invalid={titleError ? "true" : "false"}
          aria-describedby={titleError ? "title-error" : undefined}
        />
        {titleError && (
          <span id="title-error" role="alert" style={{ color: "red" }}>
            {titleError}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="task-status">Status</label>
        <select
          id="task-status"
          value={status}
          onChange={handleStatusChange}
        >
          {STATUS_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="task-due-date">Due Date</label>
        <input
          id="task-due-date"
          type="date"
          value={dueDate}
          onChange={handleDueDateChange}
        />
      </div>

      <button type="submit">
        {isEditMode ? "Update Task" : "Add Task"}
      </button>
    </form>
  );
}
