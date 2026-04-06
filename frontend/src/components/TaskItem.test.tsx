import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TaskItem, { Task, TaskItemProps } from "./TaskItem";

// Minimal StatusBadge mock so TaskItem can render without the real dependency
vi.mock("./StatusBadge", () => ({
  __esModule: true,
  default: ({ status }: { status: string }) => (
    <span data-testid="status-badge">{status}</span>
  ),
}));

const baseTask: Task = {
  id: 42,
  title: "Write unit tests",
  status: "todo",
  due_date: "2025-03-15",
};

function renderTaskItem(overrides: Partial<TaskItemProps> = {}) {
  const defaultProps: TaskItemProps = {
    task: baseTask,
    onEdit: vi.fn(),
    onDelete: vi.fn(),
    onStatusChange: vi.fn(),
    ...overrides,
  };
  return { ...render(<TaskItem {...defaultProps} />), props: defaultProps };
}

describe("TaskItem", () => {
  it("renders without crashing", () => {
    renderTaskItem();
    expect(screen.getByTestId("task-item-42")).toBeTruthy();
  });

  it("displays the task title", () => {
    renderTaskItem();
    expect(screen.getByTestId("task-title").textContent).toBe(
      "Write unit tests"
    );
  });

  it("displays a formatted due date", () => {
    renderTaskItem();
    const dueDateEl = screen.getByTestId("task-due-date");
    // Expect "Mar 15, 2025" (en-US short format)
    expect(dueDateEl.textContent).toBe("Mar 15, 2025");
  });

  it('displays "No due date" when due_date is null', () => {
    const taskNoDue: Task = { ...baseTask, due_date: null };
    renderTaskItem({ task: taskNoDue });
    expect(screen.getByTestId("task-due-date").textContent).toBe(
      "No due date"
    );
  });

  it("renders the StatusBadge with correct status", () => {
    renderTaskItem();
    expect(screen.getByTestId("status-badge").textContent).toBe("todo");
  });

  it("renders a status dropdown with the current value selected", () => {
    renderTaskItem();
    const select = screen.getByTestId(
      "task-status-select"
    ) as HTMLSelectElement;
    expect(select.value).toBe("todo");
  });

  it("calls onStatusChange when the status dropdown value changes", () => {
    const onStatusChange = vi.fn();
    renderTaskItem({ onStatusChange });
    const select = screen.getByTestId("task-status-select");
    fireEvent.change(select, { target: { value: "done" } });
    expect(onStatusChange).toHaveBeenCalledTimes(1);
    expect(onStatusChange).toHaveBeenCalledWith(42, "done");
  });

  it("calls onEdit with the task when the edit button is clicked", () => {
    const onEdit = vi.fn();
    renderTaskItem({ onEdit });
    fireEvent.click(screen.getByTestId("task-edit-btn"));
    expect(onEdit).toHaveBeenCalledTimes(1);
    expect(onEdit).toHaveBeenCalledWith(baseTask);
  });

  it("calls onDelete with the task id when the delete button is clicked", () => {
    const onDelete = vi.fn();
    renderTaskItem({ onDelete });
    fireEvent.click(screen.getByTestId("task-delete-btn"));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith(42);
  });

  it("renders all three status options in the dropdown", () => {
    renderTaskItem();
    const select = screen.getByTestId("task-status-select");
    const options = select.querySelectorAll("option");
    expect(options).toHaveLength(3);
    expect(options[0].value).toBe("todo");
    expect(options[1].value).toBe("in-progress");
    expect(options[2].value).toBe("done");
  });

  it("reflects a different task status in both badge and dropdown", () => {
    const inProgressTask: Task = { ...baseTask, status: "in-progress" };
    renderTaskItem({ task: inProgressTask });
    expect(screen.getByTestId("status-badge").textContent).toBe("in-progress");
    const select = screen.getByTestId(
      "task-status-select"
    ) as HTMLSelectElement;
    expect(select.value).toBe("in-progress");
  });

  it("has accessible labels on buttons and select", () => {
    renderTaskItem();
    expect(screen.getByLabelText("Edit task")).toBeTruthy();
    expect(screen.getByLabelText("Delete task")).toBeTruthy();
    expect(screen.getByLabelText("Change task status")).toBeTruthy();
  });
});
