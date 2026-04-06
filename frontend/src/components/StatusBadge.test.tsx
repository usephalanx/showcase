import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import StatusBadge from "./StatusBadge";
import type { StatusType } from "./StatusBadge";

describe("StatusBadge", () => {
  it("renders without crashing", () => {
    const { container } = render(<StatusBadge status="todo" />);
    expect(container).toBeTruthy();
  });

  it('renders "Todo" label with gray styling for todo status', () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge).toBeTruthy();
    expect(badge.textContent).toBe("Todo");
    expect(badge.getAttribute("data-status")).toBe("todo");
    expect(badge.style.backgroundColor).toBe("rgb(226, 226, 226)");
    expect(badge.style.color).toBe("rgb(85, 85, 85)");
  });

  it('renders "In Progress" label with blue styling for in-progress status', () => {
    render(<StatusBadge status="in-progress" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.textContent).toBe("In Progress");
    expect(badge.getAttribute("data-status")).toBe("in-progress");
    expect(badge.style.backgroundColor).toBe("rgb(219, 234, 254)");
    expect(badge.style.color).toBe("rgb(29, 78, 216)");
  });

  it('renders "Done" label with green styling for done status', () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.textContent).toBe("Done");
    expect(badge.getAttribute("data-status")).toBe("done");
    expect(badge.style.backgroundColor).toBe("rgb(209, 250, 229)");
    expect(badge.style.color).toBe("rgb(6, 95, 70)");
  });

  it("renders as an inline pill with border-radius", () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.borderRadius).toBe("9999px");
    expect(badge.style.display).toBe("inline-block");
  });

  it("renders correctly for each status type in a loop", () => {
    const statuses: { status: StatusType; expectedLabel: string }[] = [
      { status: "todo", expectedLabel: "Todo" },
      { status: "in-progress", expectedLabel: "In Progress" },
      { status: "done", expectedLabel: "Done" },
    ];

    statuses.forEach(({ status, expectedLabel }) => {
      const { unmount } = render(<StatusBadge status={status} />);
      const badge = screen.getByTestId("status-badge");
      expect(badge.textContent).toBe(expectedLabel);
      expect(badge.getAttribute("data-status")).toBe(status);
      unmount();
    });
  });
});
