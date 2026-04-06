import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TaskCard, { Task, TaskStatus } from "./TaskCard";

// Provide a minimal StatusBadge mock so TaskCard renders independently
vi.mock("./StatusBadge", () => ({
  default: ({ status }: { status: string }) => (
    <span data-testid="status-badge">{status}</span>
  ),
}));

const makeTask = (overrides: Partial<Task> = {}): Task => ({
  id: 1,
  title: "Write unit tests",
  status: "todo" as TaskStatus,
  due_date: "2025-03-15",
  created_at: "2025-01-01T00:00:00",
  updated_at: "2025-01-01T00:00:00",
  ...overrides,
});

describe("TaskCard", () => {
  it("renders without crashing", () => {
    render(
      <TaskCard
        task={makeTask()}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    expect(screen.getByTestId("task-card-1")).toBeDefined();
  });

  it("displays the task title", () => {
    render(
      <TaskCard
        task={makeTask({ title: "My Important Task" })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    expect(screen.getByTestId("task-title").textContent).toBe(
      "My Important Task",
    );
  });

  it("displays a formatted due date", () => {
    render(
      <TaskCard
        task={makeTask({ due_date: "2025-12-25" })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    expect(screen.getByTestId("task-due-date").textContent).toBe(
      "Dec 25, 2025",
    );
  });

  it("displays 'No due date' when due_date is null", () => {
    render(
      <TaskCard
        task={makeTask({ due_date: null })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    expect(screen.getByTestId("task-due-date").textContent).toBe(
      "No due date",
    );
  });

  it("renders the StatusBadge with the correct status", () => {
    render(
      <TaskCard
        task={makeTask({ status: "in-progress" })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    expect(screen.getByTestId("status-badge").textContent).toBe("in-progress");
  });

  it("calls onEdit with the task when the edit button is clicked", () => {
    const onEdit = vi.fn();
    const task = makeTask();
    render(
      <TaskCard
        task={task}
        onEdit={onEdit}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    fireEvent.click(screen.getByTestId("edit-button"));
    expect(onEdit).toHaveBeenCalledTimes(1);
    expect(onEdit).toHaveBeenCalledWith(task);
  });

  it("calls onDelete with the task id when the delete button is clicked", () => {
    const onDelete = vi.fn();
    const task = makeTask({ id: 42 });
    render(
      <TaskCard
        task={task}
        onEdit={() => {}}
        onDelete={onDelete}
        onStatusChange={() => {}}
      />,
    );
    fireEvent.click(screen.getByTestId("delete-button"));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith(42);
  });

  it("calls onStatusChange with next status when status badge is clicked (todo -> in-progress)", () => {
    const onStatusChange = vi.fn();
    const task = makeTask({ id: 7, status: "todo" });
    render(
      <TaskCard
        task={task}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={onStatusChange}
      />,
    );
    fireEvent.click(screen.getByLabelText(`Change status of ${task.title}`));
    expect(onStatusChange).toHaveBeenCalledTimes(1);
    expect(onStatusChange).toHaveBeenCalledWith(7, "in-progress");
  });

  it("cycles status from in-progress to done", () => {
    const onStatusChange = vi.fn();
    const task = makeTask({ id: 3, status: "in-progress" });
    render(
      <TaskCard
        task={task}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={onStatusChange}
      />,
    );
    fireEvent.click(screen.getByLabelText(`Change status of ${task.title}`));
    expect(onStatusChange).toHaveBeenCalledWith(3, "done");
  });

  it("cycles status from done to todo", () => {
    const onStatusChange = vi.fn();
    const task = makeTask({ id: 5, status: "done" });
    render(
      <TaskCard
        task={task}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={onStatusChange}
      />,
    );
    fireEvent.click(screen.getByLabelText(`Change status of ${task.title}`));
    expect(onStatusChange).toHaveBeenCalledWith(5, "todo");
  });

  it("applies line-through styling for done tasks", () => {
    render(
      <TaskCard
        task={makeTask({ status: "done" })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    const title = screen.getByTestId("task-title");
    expect(title.style.textDecoration).toBe("line-through");
  });

  it("does not apply line-through styling for non-done tasks", () => {
    render(
      <TaskCard
        task={makeTask({ status: "todo" })}
        onEdit={() => {}}
        onDelete={() => {}}
        onStatusChange={() => {}}
      />,
    );
    const title = screen.getByTestId("task-title");
    expect(title.style.textDecoration).toBe("none");
  });
});
