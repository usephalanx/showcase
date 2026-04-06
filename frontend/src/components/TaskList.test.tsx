import { describe, it, expect, vi } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskList from "./TaskList";
import type { Task, TaskStatus } from "./TaskList";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const makeTasks = (count: number): Task[] =>
  Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    title: `Task ${i + 1}`,
    status: "todo" as TaskStatus,
    due_date: i % 2 === 0 ? "2025-12-31" : null,
    created_at: "2025-01-01T00:00:00Z",
    updated_at: "2025-01-01T00:00:00Z",
  }));

const noop = () => {};

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("TaskList", () => {
  it("renders without crashing with an empty task array", () => {
    const { container } = render(
      <TaskList
        tasks={[]}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(container).toBeTruthy();
  });

  it("shows the default empty state message when there are no tasks", () => {
    render(
      <TaskList
        tasks={[]}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(
      screen.getByText("No tasks yet. Create one to get started!"),
    ).toBeInTheDocument();
  });

  it("shows a custom empty state message when provided", () => {
    render(
      <TaskList
        tasks={[]}
        emptyMessage="Nothing to do!"
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(screen.getByText("Nothing to do!")).toBeInTheDocument();
  });

  it("does not show empty state when tasks exist", () => {
    render(
      <TaskList
        tasks={makeTasks(1)}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(
      screen.queryByText("No tasks yet. Create one to get started!"),
    ).not.toBeInTheDocument();
  });

  it("renders one TaskCard per task", () => {
    const tasks = makeTasks(3);
    render(
      <TaskList
        tasks={tasks}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    tasks.forEach((task) => {
      expect(screen.getByText(task.title)).toBeInTheDocument();
    });
  });

  it("renders a <ul> with role='list' when tasks are present", () => {
    render(
      <TaskList
        tasks={makeTasks(2)}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(screen.getByRole("list")).toBeInTheDocument();
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });

  it("forwards onEdit to TaskCard when Edit button is clicked", async () => {
    const user = userEvent.setup();
    const onEdit = vi.fn();
    const tasks = makeTasks(1);

    render(
      <TaskList
        tasks={tasks}
        onEdit={onEdit}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );

    await user.click(screen.getByRole("button", { name: /edit task 1/i }));
    expect(onEdit).toHaveBeenCalledTimes(1);
    expect(onEdit).toHaveBeenCalledWith(tasks[0]);
  });

  it("forwards onDelete to TaskCard when Delete button is clicked", async () => {
    const user = userEvent.setup();
    const onDelete = vi.fn();
    const tasks = makeTasks(1);

    render(
      <TaskList
        tasks={tasks}
        onEdit={noop}
        onDelete={onDelete}
        onStatusChange={noop}
      />,
    );

    await user.click(screen.getByRole("button", { name: /delete task 1/i }));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete).toHaveBeenCalledWith(tasks[0].id);
  });

  it("forwards onStatusChange to TaskCard when status select changes", async () => {
    const user = userEvent.setup();
    const onStatusChange = vi.fn();
    const tasks = makeTasks(1);

    render(
      <TaskList
        tasks={tasks}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={onStatusChange}
      />,
    );

    const select = screen.getByRole("combobox", {
      name: /change status of task 1/i,
    });
    await user.selectOptions(select, "done");

    expect(onStatusChange).toHaveBeenCalledTimes(1);
    expect(onStatusChange).toHaveBeenCalledWith(tasks[0].id, "done");
  });

  it("renders TaskCards with correct test-ids", () => {
    const tasks = makeTasks(2);
    render(
      <TaskList
        tasks={tasks}
        onEdit={noop}
        onDelete={noop}
        onStatusChange={noop}
      />,
    );
    expect(screen.getByTestId("task-card-1")).toBeInTheDocument();
    expect(screen.getByTestId("task-card-2")).toBeInTheDocument();
  });
});
