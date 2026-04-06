import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskForm, { TaskFormProps, TaskCreate } from "./TaskForm";

function renderForm(overrides: Partial<TaskFormProps> = {}) {
  const defaultProps: TaskFormProps = {
    onSubmit: vi.fn(),
    onCancel: vi.fn(),
    ...overrides,
  };
  render(<TaskForm {...defaultProps} />);
  return defaultProps;
}

describe("TaskForm", () => {
  it("renders without crashing", () => {
    renderForm();
    expect(screen.getByRole("form", { name: /task form/i })).toBeInTheDocument();
  });

  it("renders all form fields", () => {
    renderForm();
    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/due date/i)).toBeInTheDocument();
  });

  it("renders submit and cancel buttons", () => {
    renderForm();
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /cancel/i })).toBeInTheDocument();
  });

  it("uses custom submitLabel when provided", () => {
    renderForm({ submitLabel: "Create Task" });
    expect(screen.getByRole("button", { name: /create task/i })).toBeInTheDocument();
  });

  it("populates fields from initialData", () => {
    renderForm({
      initialData: {
        title: "My Task",
        status: "in-progress",
        due_date: "2025-12-31",
      },
    });
    expect(screen.getByLabelText(/title/i)).toHaveValue("My Task");
    expect(screen.getByLabelText(/status/i)).toHaveValue("in-progress");
    expect(screen.getByLabelText(/due date/i)).toHaveValue("2025-12-31");
  });

  it("defaults status to 'todo' when no initialData is given", () => {
    renderForm();
    expect(screen.getByLabelText(/status/i)).toHaveValue("todo");
  });

  it("shows validation error when title is empty on submit", async () => {
    const props = renderForm();
    const submitBtn = screen.getByRole("button", { name: /save/i });

    await userEvent.click(submitBtn);

    expect(screen.getByRole("alert")).toHaveTextContent("Title is required");
    expect(props.onSubmit).not.toHaveBeenCalled();
  });

  it("shows validation error when title is only whitespace", async () => {
    const props = renderForm();
    const titleInput = screen.getByLabelText(/title/i);

    await userEvent.type(titleInput, "   ");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    expect(screen.getByRole("alert")).toHaveTextContent("Title is required");
    expect(props.onSubmit).not.toHaveBeenCalled();
  });

  it("clears validation error when user types a valid title after failed submit", async () => {
    renderForm();

    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    expect(screen.getByRole("alert")).toBeInTheDocument();

    await userEvent.type(screen.getByLabelText(/title/i), "A");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("calls onSubmit with correct data on valid submission", async () => {
    const onSubmit = vi.fn();
    renderForm({ onSubmit });

    await userEvent.type(screen.getByLabelText(/title/i), "Buy groceries");
    await userEvent.selectOptions(screen.getByLabelText(/status/i), "done");
    fireEvent.change(screen.getByLabelText(/due date/i), {
      target: { value: "2025-06-15" },
    });

    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    const submittedData: TaskCreate = onSubmit.mock.calls[0][0];
    expect(submittedData.title).toBe("Buy groceries");
    expect(submittedData.status).toBe("done");
    expect(submittedData.due_date).toBe("2025-06-15");
  });

  it("sends due_date as null when no date is selected", async () => {
    const onSubmit = vi.fn();
    renderForm({ onSubmit });

    await userEvent.type(screen.getByLabelText(/title/i), "No due date task");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit.mock.calls[0][0].due_date).toBeNull();
  });

  it("trims the title before submitting", async () => {
    const onSubmit = vi.fn();
    renderForm({ onSubmit });

    await userEvent.type(screen.getByLabelText(/title/i), "  Trimmed  ");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    expect(onSubmit.mock.calls[0][0].title).toBe("Trimmed");
  });

  it("calls onCancel when cancel button is clicked", async () => {
    const onCancel = vi.fn();
    renderForm({ onCancel });

    await userEvent.click(screen.getByRole("button", { name: /cancel/i }));

    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("does not call onSubmit when cancel is clicked", async () => {
    const onSubmit = vi.fn();
    renderForm({ onSubmit });

    await userEvent.click(screen.getByRole("button", { name: /cancel/i }));

    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("renders all three status options", () => {
    renderForm();
    const select = screen.getByLabelText(/status/i);
    const options = select.querySelectorAll("option");

    expect(options).toHaveLength(3);
    const values = Array.from(options).map((o) => o.getAttribute("value"));
    expect(values).toEqual(["todo", "in-progress", "done"]);
  });

  it("sets aria-invalid on title when there is a validation error", async () => {
    renderForm();

    const titleInput = screen.getByLabelText(/title/i);
    expect(titleInput).toHaveAttribute("aria-invalid", "false");

    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    expect(titleInput).toHaveAttribute("aria-invalid", "true");
  });
});
