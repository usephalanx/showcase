import React, { useState, useEffect, FormEvent, ChangeEvent } from "react";

/**
 * Allowed status values for a task, mirroring the backend TaskStatus enum.
 */
export type TaskStatus = "todo" | "in-progress" | "done";

/**
 * Shape of data submitted by the form – mirrors backend TaskCreate schema.
 */
export interface TaskCreate {
  title: string;
  status: TaskStatus;
  due_date: string | null;
}

/**
 * Props accepted by the TaskForm component.
 */
export interface TaskFormProps {
  /** Pre-populated data when editing an existing task. */
  initialData?: Partial<TaskCreate>;
  /** Callback invoked with validated form data on submission. */
  onSubmit: (data: TaskCreate) => void;
  /** Callback invoked when the user cancels the form. */
  onCancel: () => void;
  /** Optional label for the submit button. Defaults to "Save". */
  submitLabel?: string;
}

const STATUS_OPTIONS: { value: TaskStatus; label: string }[] = [
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

/**
 * A form component for creating or editing a task.
 *
 * Validates that the title field is non-empty before allowing submission.
 */
export default function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = "Save",
}: TaskFormProps) {
  const [title, setTitle] = useState<string>(initialData?.title ?? "");
  const [status, setStatus] = useState<TaskStatus>(initialData?.status ?? "todo");
  const [dueDate, setDueDate] = useState<string>(initialData?.due_date ?? "");
  const [titleError, setTitleError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);

  // Sync with initialData changes (e.g. switching between edit targets)
  useEffect(() => {
    setTitle(initialData?.title ?? "");
    setStatus(initialData?.status ?? "todo");
    setDueDate(initialData?.due_date ?? "");
    setTitleError(null);
    setSubmitted(false);
  }, [initialData]);

  const validate = (): boolean => {
    const trimmed = title.trim();
    if (trimmed.length === 0) {
      setTitleError("Title is required");
      return false;
    }
    setTitleError(null);
    return true;
  };

  const handleTitleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setTitle(e.target.value);
    if (submitted) {
      // Re-validate on change after first submit attempt
      if (e.target.value.trim().length > 0) {
        setTitleError(null);
      } else {
        setTitleError("Title is required");
      }
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitted(true);

    if (!validate()) {
      return;
    }

    onSubmit({
      title: title.trim(),
      status,
      due_date: dueDate === "" ? null : dueDate,
    });
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
          aria-describedby={titleError ? "task-title-error" : undefined}
        />
        {titleError && (
          <span id="task-title-error" role="alert" style={{ color: "red" }}>
            {titleError}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="task-status">Status</label>
        <select
          id="task-status"
          value={status}
          onChange={(e) => setStatus(e.target.value as TaskStatus)}
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
          onChange={(e) => setDueDate(e.target.value)}
        />
      </div>

      <div>
        <button type="submit">{submitLabel}</button>
        <button type="button" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}
