import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TaskFilter, { TaskFilterStatus } from "./TaskFilter";

describe("TaskFilter", () => {
  const defaultProps = {
    currentFilter: "all" as TaskFilterStatus,
    onFilterChange: vi.fn(),
  };

  it("renders without crashing", () => {
    render(<TaskFilter {...defaultProps} />);
    expect(screen.getByRole("tablist")).toBeInTheDocument();
  });

  it("renders all four filter buttons", () => {
    render(<TaskFilter {...defaultProps} />);
    expect(screen.getByText("All")).toBeInTheDocument();
    expect(screen.getByText("Todo")).toBeInTheDocument();
    expect(screen.getByText("In Progress")).toBeInTheDocument();
    expect(screen.getByText("Done")).toBeInTheDocument();
  });

  it("highlights the active filter with aria-selected=true", () => {
    render(<TaskFilter currentFilter="todo" onFilterChange={vi.fn()} />);

    const todoButton = screen.getByText("Todo");
    const allButton = screen.getByText("All");

    expect(todoButton).toHaveAttribute("aria-selected", "true");
    expect(allButton).toHaveAttribute("aria-selected", "false");
  });

  it("highlights 'In Progress' when currentFilter is 'in-progress'", () => {
    render(<TaskFilter currentFilter="in-progress" onFilterChange={vi.fn()} />);

    const inProgressButton = screen.getByText("In Progress");
    expect(inProgressButton).toHaveAttribute("aria-selected", "true");
  });

  it("highlights 'Done' when currentFilter is 'done'", () => {
    render(<TaskFilter currentFilter="done" onFilterChange={vi.fn()} />);

    const doneButton = screen.getByText("Done");
    expect(doneButton).toHaveAttribute("aria-selected", "true");
  });

  it("calls onFilterChange with 'todo' when Todo button is clicked", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="all" onFilterChange={handleChange} />);

    await user.click(screen.getByText("Todo"));

    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("todo");
  });

  it("calls onFilterChange with 'in-progress' when In Progress button is clicked", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="all" onFilterChange={handleChange} />);

    await user.click(screen.getByText("In Progress"));

    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("in-progress");
  });

  it("calls onFilterChange with 'done' when Done button is clicked", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="all" onFilterChange={handleChange} />);

    await user.click(screen.getByText("Done"));

    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("done");
  });

  it("calls onFilterChange with 'all' when All button is clicked", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(<TaskFilter currentFilter="done" onFilterChange={handleChange} />);

    await user.click(screen.getByText("All"));

    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("all");
  });

  it("applies bold font weight to the active filter button", () => {
    render(<TaskFilter currentFilter="done" onFilterChange={vi.fn()} />);

    const doneButton = screen.getByText("Done");
    expect(doneButton).toHaveStyle({ fontWeight: 700 });

    const allButton = screen.getByText("All");
    expect(allButton).toHaveStyle({ fontWeight: 400 });
  });

  it("applies highlighted background color to the active filter button", () => {
    render(<TaskFilter currentFilter="todo" onFilterChange={vi.fn()} />);

    const todoButton = screen.getByText("Todo");
    expect(todoButton).toHaveStyle({ backgroundColor: "#3b82f6" });
    expect(todoButton).toHaveStyle({ color: "#ffffff" });
  });

  it("applies default background color to inactive filter buttons", () => {
    render(<TaskFilter currentFilter="todo" onFilterChange={vi.fn()} />);

    const allButton = screen.getByText("All");
    expect(allButton).toHaveStyle({ backgroundColor: "#ffffff" });
    expect(allButton).toHaveStyle({ color: "#374151" });
  });

  it("ensures only one filter is active at a time", () => {
    render(<TaskFilter currentFilter="in-progress" onFilterChange={vi.fn()} />);

    const tabs = screen.getAllByRole("tab");
    const activeTabs = tabs.filter(
      (tab) => tab.getAttribute("aria-selected") === "true"
    );

    expect(activeTabs).toHaveLength(1);
    expect(activeTabs[0]).toHaveTextContent("In Progress");
  });
});
