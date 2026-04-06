import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskFilter from "./TaskFilter";

describe("TaskFilter", () => {
  const defaultProps = {
    currentFilter: "all",
    onFilterChange: vi.fn(),
  };

  it("renders without crashing", () => {
    render(<TaskFilter {...defaultProps} />);
    expect(screen.getByRole("group")).toBeInTheDocument();
  });

  it("renders all four filter buttons", () => {
    render(<TaskFilter {...defaultProps} />);
    expect(screen.getByText("All")).toBeInTheDocument();
    expect(screen.getByText("Todo")).toBeInTheDocument();
    expect(screen.getByText("In Progress")).toBeInTheDocument();
    expect(screen.getByText("Done")).toBeInTheDocument();
  });

  it("highlights the active filter with aria-pressed and active class", () => {
    render(<TaskFilter currentFilter="todo" onFilterChange={vi.fn()} />);

    const todoButton = screen.getByText("Todo");
    expect(todoButton).toHaveAttribute("aria-pressed", "true");
    expect(todoButton.className).toContain("task-filter__button--active");

    const allButton = screen.getByText("All");
    expect(allButton).toHaveAttribute("aria-pressed", "false");
    expect(allButton.className).not.toContain("task-filter__button--active");
  });

  it("highlights 'in-progress' filter when currentFilter is 'in-progress'", () => {
    render(<TaskFilter currentFilter="in-progress" onFilterChange={vi.fn()} />);

    const inProgressButton = screen.getByText("In Progress");
    expect(inProgressButton).toHaveAttribute("aria-pressed", "true");
    expect(inProgressButton.className).toContain("task-filter__button--active");
  });

  it("calls onFilterChange with the correct value when a button is clicked", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="all" onFilterChange={handleChange} />);

    await user.click(screen.getByText("Todo"));
    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("todo");
  });

  it("calls onFilterChange when clicking the already-active filter", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="done" onFilterChange={handleChange} />);

    await user.click(screen.getByText("Done"));
    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("done");
  });

  it("calls onFilterChange with different values for each button", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="all" onFilterChange={handleChange} />);

    await user.click(screen.getByText("In Progress"));
    expect(handleChange).toHaveBeenCalledWith("in-progress");

    await user.click(screen.getByText("Done"));
    expect(handleChange).toHaveBeenCalledWith("done");

    await user.click(screen.getByText("All"));
    expect(handleChange).toHaveBeenCalledWith("all");

    expect(handleChange).toHaveBeenCalledTimes(3);
  });

  it("has accessible group role with descriptive label", () => {
    render(<TaskFilter {...defaultProps} />);
    const group = screen.getByRole("group");
    expect(group).toHaveAttribute("aria-label", "Filter tasks by status");
  });

  it("renders buttons with type='button' to prevent form submission", () => {
    render(<TaskFilter {...defaultProps} />);
    const buttons = screen.getAllByRole("button");
    buttons.forEach((button) => {
      expect(button).toHaveAttribute("type", "button");
    });
  });
});
