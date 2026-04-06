import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskForm from "./TaskForm";
import type { TaskFormData } from "./TaskForm";

describe("TaskForm", () => {
  it("renders without crashing", () => {
    render(<TaskForm onSubmit={() => {}} />);
    expect(screen.getByLabelText("Title")).toBeInTheDocument();
    expect(screen.getByLabelText("Status")).toBeInTheDocument();
    expect(screen.getByLabelText("Due Date")).toBeInTheDocument();
  });

  it('displays "Add Task" button in create mode', () => {
    render(<TaskForm onSubmit={() => {}} />);
    expect(screen.getByRole("button", { name: "Add Task" })).toBeInTheDocument();
  });

  it('displays "Update Task" button in edit mode', () => {
    render(
      <TaskForm
        onSubmit={() => {}}
        initialValues={{ title: "Existing", status: "done", due_date: "2025-12-31" }}
      />
    );
    expect(screen.getByRole("button", { name: "Update Task" })).toBeInTheDocument();
  });

  it("pre-fills fields with initialValues in edit mode", () => {
    render(
      <TaskForm
        onSubmit={() => {}}
        initialValues={{ title: "My Task", status: "in-progress", due_date: "2025-06-15" }}
      />
    );
    expect(screen.getByLabelText("Title")).toHaveValue("My Task");
    expect(screen.getByLabelText("Status")).toHaveValue("in-progress");
    expect(screen.getByLabelText("Due Date")).toHaveValue("2025-06-15");
  });

  it("shows validation error when title is empty on submit", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    expect(screen.getByRole("alert")).toHaveTextContent("Title is required");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("shows validation error when title is whitespace-only", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    const titleInput = screen.getByLabelText("Title");
    await userEvent.type(titleInput, "   ");
    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    expect(screen.getByRole("alert")).toHaveTextContent("Title is required");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("clears validation error when user types a valid title", async () => {
    render(<TaskForm onSubmit={() => {}} />);

    // Trigger the error first
    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));
    expect(screen.getByRole("alert")).toBeInTheDocument();

    // Type a valid title
    await userEvent.type(screen.getByLabelText("Title"), "Fix bug");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("calls onSubmit with correct data on valid submission", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText("Title"), "Write tests");
    await userEvent.selectOptions(screen.getByLabelText("Status"), "in-progress");

    const dueDateInput = screen.getByLabelText("Due Date");
    fireEvent.change(dueDateInput, { target: { value: "2025-09-01" } });

    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith({
      title: "Write tests",
      status: "in-progress",
      due_date: "2025-09-01",
    } satisfies TaskFormData);
  });

  it("defaults status to 'todo' in create mode", () => {
    render(<TaskForm onSubmit={() => {}} />);
    expect(screen.getByLabelText("Status")).toHaveValue("todo");
  });

  it("renders all three status options", () => {
    render(<TaskForm onSubmit={() => {}} />);
    const options = screen.getAllByRole("option");
    expect(options).toHaveLength(3);
    expect(options[0]).toHaveTextContent("Todo");
    expect(options[1]).toHaveTextContent("In Progress");
    expect(options[2]).toHaveTextContent("Done");
  });

  it("calls onSubmit with trimmed title", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText("Title"), "  padded title  ");
    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ title: "padded title" })
    );
  });

  it("submits with empty due_date when not provided", async () => {
    const onSubmit = vi.fn();
    render(<TaskForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText("Title"), "No deadline");
    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ due_date: "" })
    );
  });

  it("has proper aria attributes for accessibility", () => {
    render(<TaskForm onSubmit={() => {}} />);
    const titleInput = screen.getByLabelText("Title");
    expect(titleInput).toHaveAttribute("aria-required", "true");
    expect(titleInput).toHaveAttribute("aria-invalid", "false");
  });

  it("sets aria-invalid to true when title validation fails", async () => {
    render(<TaskForm onSubmit={() => {}} />);

    await userEvent.click(screen.getByRole("button", { name: "Add Task" }));

    const titleInput = screen.getByLabelText("Title");
    expect(titleInput).toHaveAttribute("aria-invalid", "true");
  });
});
