import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskForm from "./TaskForm";

describe("TaskForm", () => {
  const defaultProps = {
    onSubmit: vi.fn(),
    onCancel: vi.fn(),
  };

  it("renders without crashing", () => {
    render(<TaskForm {...defaultProps} />);
    expect(screen.getByLabelText("Title")).toBeInTheDocument();
    expect(screen.getByLabelText("Status")).toBeInTheDocument();
    expect(screen.getByLabelText("Due Date")).toBeInTheDocument();
  });

  it('displays "Create Task" button when no initialValues provided', () => {
    render(<TaskForm {...defaultProps} />);
    expect(screen.getByRole("button", { name: "Create Task" })).toBeInTheDocument();
  });

  it('displays "Update Task" button when initialValues are provided', () => {
    render(
      <TaskForm
        {...defaultProps}
        initialValues={{ title: "Existing task", status: "done", due_date: "2025-12-31" }}
      />,
    );
    expect(screen.getByRole("button", { name: "Update Task" })).toBeInTheDocument();
  });

  it("pre-fills fields with initialValues", () => {
    render(
      <TaskForm
        {...defaultProps}
        initialValues={{ title: "My Task", status: "in-progress", due_date: "2025-06-15" }}
      />,
    );
    expect(screen.getByLabelText("Title")).toHaveValue("My Task");
    expect(screen.getByLabelText("Status")).toHaveValue("in-progress");
    expect(screen.getByLabelText("Due Date")).toHaveValue("2025-06-15");
  });

  it("defaults status to 'todo' when no initialValues", () => {
    render(<TaskForm {...defaultProps} />);
    expect(screen.getByLabelText("Status")).toHaveValue("todo");
  });

  it("shows validation error when submitting with empty title", async () => {
    render(<TaskForm {...defaultProps} />);
    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Title is required");
    expect(defaultProps.onSubmit).not.toHaveBeenCalled();
  });

  it("shows validation error when title is only whitespace", async () => {
    render(<TaskForm {...defaultProps} />);
    const titleInput = screen.getByLabelText("Title");
    await userEvent.type(titleInput, "   ");
    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Title is required");
    expect(defaultProps.onSubmit).not.toHaveBeenCalled();
  });

  it("calls onSubmit with form values on valid submission", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} onCancel={vi.fn()} />);

    await userEvent.type(screen.getByLabelText("Title"), "New task");
    await userEvent.selectOptions(screen.getByLabelText("Status"), "in-progress");
    fireEvent.change(screen.getByLabelText("Due Date"), {
      target: { value: "2025-08-01" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledTimes(1);
      expect(onSubmit).toHaveBeenCalledWith({
        title: "New task",
        status: "in-progress",
        due_date: "2025-08-01",
      });
    });
  });

  it("calls onCancel when Cancel button is clicked", async () => {
    const onCancel = vi.fn();
    render(<TaskForm onSubmit={vi.fn()} onCancel={onCancel} />);
    fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it("does not call onSubmit when Cancel is clicked", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    fireEvent.click(screen.getByRole("button", { name: "Cancel" }));
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("clears validation error once a valid title is entered", async () => {
    render(<TaskForm {...defaultProps} />);
    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));
    expect(await screen.findByRole("alert")).toBeInTheDocument();

    await userEvent.type(screen.getByLabelText("Title"), "Valid title");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("sets aria-invalid on title input when validation fails", async () => {
    render(<TaskForm {...defaultProps} />);
    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));
    await waitFor(() => {
      expect(screen.getByLabelText("Title")).toHaveAttribute("aria-invalid", "true");
    });
  });

  it("renders all three status options", () => {
    render(<TaskForm {...defaultProps} />);
    const options = screen.getByLabelText("Status").querySelectorAll("option");
    expect(options).toHaveLength(3);
    expect(options[0]).toHaveValue("todo");
    expect(options[1]).toHaveValue("in-progress");
    expect(options[2]).toHaveValue("done");
  });

  it("submits without due_date when left empty", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} onCancel={vi.fn()} />);
    await userEvent.type(screen.getByLabelText("Title"), "No date task");
    fireEvent.click(screen.getByRole("button", { name: "Create Task" }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        title: "No date task",
        status: "todo",
        due_date: "",
      });
    });
  });

  it("has an accessible form role", () => {
    render(<TaskForm {...defaultProps} />);
    expect(screen.getByRole("form", { name: "Task form" })).toBeInTheDocument();
  });
});
