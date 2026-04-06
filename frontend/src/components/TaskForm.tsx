import React, { useState, FormEvent, ChangeEvent } from "react";

export interface TaskFormValues {
  title: string;
  status: "todo" | "in-progress" | "done";
  due_date: string;
}

export interface TaskFormProps {
  /** Pre-filled values for edit mode. All fields optional. */
  initialValues?: Partial<TaskFormValues>;
  /** Called with form values when valid form is submitted. */
  onSubmit: (values: TaskFormValues) => void;
  /** Called when the user cancels the form. */
  onCancel: () => void;
}

const STATUS_OPTIONS: { value: TaskFormValues["status"]; label: string }[] = [
  { value: "todo", label: "Todo" },
  { value: "in-progress", label: "In Progress" },
  { value: "done", label: "Done" },
];

const defaultValues: TaskFormValues = {
  title: "",
  status: "todo",
  due_date: "",
};

export default function TaskForm({
  initialValues,
  onSubmit,
  onCancel,
}: TaskFormProps) {
  const [values, setValues] = useState<TaskFormValues>({
    ...defaultValues,
    ...initialValues,
  });
  const [errors, setErrors] = useState<{ title?: string }>({});
  const [touched, setTouched] = useState<{ title?: boolean }>({});

  const validate = (vals: TaskFormValues): { title?: string } => {
    const errs: { title?: string } = {};
    if (!vals.title.trim()) {
      errs.title = "Title is required";
    }
    return errs;
  };

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    const next = { ...values, [name]: value };
    setValues(next);
    if (touched[name as keyof typeof touched]) {
      setErrors(validate(next));
    }
  };

  const handleBlur = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    setErrors(validate(values));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const validationErrors = validate(values);
    setErrors(validationErrors);
    setTouched({ title: true });
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(values);
    }
  };

  const isEdit = Boolean(initialValues);

  return (
    <form onSubmit={handleSubmit} aria-label="Task form">
      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="task-title" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>
          Title
        </label>
        <input
          id="task-title"
          name="title"
          type="text"
          value={values.title}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-invalid={Boolean(errors.title)}
          aria-describedby={errors.title ? "title-error" : undefined}
          style={{
            width: "100%",
            padding: "0.5rem",
            border: errors.title ? "1px solid #e53e3e" : "1px solid #cbd5e0",
            borderRadius: "4px",
            boxSizing: "border-box",
          }}
        />
        {errors.title && (
          <span id="title-error" role="alert" style={{ color: "#e53e3e", fontSize: "0.875rem" }}>
            {errors.title}
          </span>
        )}
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="task-status" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>
          Status
        </label>
        <select
          id="task-status"
          name="status"
          value={values.status}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{
            width: "100%",
            padding: "0.5rem",
            border: "1px solid #cbd5e0",
            borderRadius: "4px",
            boxSizing: "border-box",
          }}
        >
          {STATUS_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label htmlFor="task-due-date" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 600 }}>
          Due Date
        </label>
        <input
          id="task-due-date"
          name="due_date"
          type="date"
          value={values.due_date}
          onChange={handleChange}
          onBlur={handleBlur}
          style={{
            width: "100%",
            padding: "0.5rem",
            border: "1px solid #cbd5e0",
            borderRadius: "4px",
            boxSizing: "border-box",
          }}
        />
      </div>

      <div style={{ display: "flex", gap: "0.75rem" }}>
        <button
          type="submit"
          style={{
            padding: "0.5rem 1.25rem",
            backgroundColor: "#3182ce",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          {isEdit ? "Update Task" : "Create Task"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          style={{
            padding: "0.5rem 1.25rem",
            backgroundColor: "#e2e8f0",
            color: "#2d3748",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
