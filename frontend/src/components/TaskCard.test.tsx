import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TaskCard, { Task, TaskStatus } from "./TaskCard";

const baseTask: Task = {
  id: 42,
  title: "Write unit tests",
  status: "todo",
  due_date: "2025-03-15",
  created_at: "2025-01-01T00:00:00Z",
  updated_at: "2025-01-01T00:00:00Z",
};

function renderCard(
  taskOverrides: Partial<Task> = {},
  handlers: {
    onEdit?: (t: Task) => void;
    onDelete?: (t: Task) => void;
    onStatusChange?: (t: Task, s: TaskStatus) => void;
  } = {},
) {
  const task = { ...baseTask, ...taskOverrides };
  const onEdit = handlers.onEdit ?? vi.fn();
  const onDelete = handlers.onDelete ?? vi.fn();
  const onStatusChange = handlers.onStatusChange ?? vi.fn();

  return {
    task,
    onEdit,
    onDelete,
    onStatusChange,
    ...render(
      <TaskCard
        task={task}
        onEdit={onEdit}
        onDelete={onDelete}
        onStatusChange={onStatusChange}
      />,
    ),
  };
}

describe("TaskCard", () => {
  it("renders without crashing", () => {
    renderCard();
    expect(screen.getByTestId("task-card-42")).toBeTruthy();
  });

  it("displays the task title", () => {
    renderCard({ title: "My Important Task" });
    expect(screen.getByText("My Important Task")).toBeTruthy();
  });

  it("displays the StatusBadge with correct status text", () => {
    renderCard({ status: "in-progress" });
    expect(screen.getByTestId("status-badge").textContent).toBe("In Progress");
  });

  it("displays a formatted due date when provided", () => {
    renderCard({ due_date: "2025-03-15" });
    // The formatted date should contain "Mar" and "2025" at minimum
    const dueLine = screen.getByText(/Due:/);
    expect(dueLine.textContent).toContain("Mar");
    expect(dueLine.textContent).toContain("2025");
  });

  it("displays an em-dash when due_date is null", () => {
    renderCard({ due_date: null });
    const dueLine = screen.getByText(/Due:/);
    expect(dueLine.textContent).toContain("\u2014");
  });

  it("calls onEdit with the task when Edit is clicked", () => {
    const onEdit = vi.fn();
    const { task } = renderCard({}, { onEdit });
    fireEvent.click(screen.getByRole("button", { name: /edit task/i }));
    expect(onEdit).toHaveBeenCalledTimes(1);
    expect(onEdit).toHaveBeenCalledWith(task);
  });

  it("calls onDelete with the task when Delete is clicked", () => {
    const onDelete = vi.fn();
    const { task } = renderCard({}, { onDelete });
    fireEvent.click(screen.getByRole("button", { name: /delete task/i }));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith(task);
  });

  it("calls onStatusChange with task and next status when status button is clicked (todo -> in-progress)", () => {
    const onStatusChange = vi.fn();
    const { task } = renderCard({ status: "todo" }, { onStatusChange });
    fireEvent.click(screen.getByRole("button", { name: /start task/i }));
    expect(onStatusChange).toHaveBeenCalledTimes(1);
    expect(onStatusChange).toHaveBeenCalledWith(task, "in-progress");
  });

  it("cycles status in-progress -> done with 'Complete' label", () => {
    const onStatusChange = vi.fn();
    const { task } = renderCard({ status: "in-progress" }, { onStatusChange });
    const btn = screen.getByRole("button", { name: /complete task/i });
    expect(btn.textContent).toBe("Complete");
    fireEvent.click(btn);
    expect(onStatusChange).toHaveBeenCalledWith(task, "done");
  });

  it("cycles status done -> todo with 'Reopen' label", () => {
    const onStatusChange = vi.fn();
    const { task } = renderCard({ status: "done" }, { onStatusChange });
    const btn = screen.getByRole("button", { name: /reopen task/i });
    expect(btn.textContent).toBe("Reopen");
    fireEvent.click(btn);
    expect(onStatusChange).toHaveBeenCalledWith(task, "todo");
  });

  it("renders the StatusBadge for 'done' status", () => {
    renderCard({ status: "done" });
    expect(screen.getByTestId("status-badge").textContent).toBe("Done");
  });

  it("renders the StatusBadge for 'todo' status", () => {
    renderCard({ status: "todo" });
    expect(screen.getByTestId("status-badge").textContent).toBe("Todo");
  });

  it("uses the task id in the data-testid attribute", () => {
    renderCard({ id: 99 });
    expect(screen.getByTestId("task-card-99")).toBeTruthy();
  });
});
