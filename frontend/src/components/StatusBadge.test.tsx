import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import StatusBadge, { TaskStatus } from "./StatusBadge";

describe("StatusBadge", () => {
  it("renders without crashing", () => {
    const { container } = render(<StatusBadge status="todo" />);
    expect(container).toBeTruthy();
  });

  it('renders "Todo" label for status "todo"', () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.textContent).toBe("Todo");
    expect(badge.getAttribute("data-status")).toBe("todo");
  });

  it('renders "In Progress" label for status "in-progress"', () => {
    render(<StatusBadge status="in-progress" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.textContent).toBe("In Progress");
    expect(badge.getAttribute("data-status")).toBe("in-progress");
  });

  it('renders "Done" label for status "done"', () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.textContent).toBe("Done");
    expect(badge.getAttribute("data-status")).toBe("done");
  });

  it("applies a grey/slate background for todo status", () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.backgroundColor).toBe("rgb(226, 232, 240)");
    expect(badge.style.color).toBe("rgb(51, 65, 85)");
  });

  it("applies an amber/yellow background for in-progress status", () => {
    render(<StatusBadge status="in-progress" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.backgroundColor).toBe("rgb(254, 243, 199)");
    expect(badge.style.color).toBe("rgb(146, 64, 14)");
  });

  it("applies a green background for done status", () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.backgroundColor).toBe("rgb(209, 250, 229)");
    expect(badge.style.color).toBe("rgb(6, 95, 70)");
  });

  it("renders as an inline pill with border-radius", () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.borderRadius).toBe("9999px");
    expect(badge.style.display).toBe("inline-flex");
  });

  it.each<TaskStatus>(["todo", "in-progress", "done"])(
    "renders a <span> element for status \"%s\"",
    (status) => {
      render(<StatusBadge status={status} />);
      const badge = screen.getByTestId("status-badge");
      expect(badge.tagName).toBe("SPAN");
    }
  );
});
