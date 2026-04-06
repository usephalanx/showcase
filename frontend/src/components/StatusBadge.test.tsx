import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import StatusBadge, { TaskStatus } from "./StatusBadge";

describe("StatusBadge", () => {
  it("renders without crashing", () => {
    const { unmount } = render(<StatusBadge status="todo" />);
    expect(screen.getByTestId("status-badge")).toBeDefined();
    unmount();
  });

  describe("renders correct label and colours for each status", () => {
    const cases: { status: TaskStatus; label: string; bgColor: string; textColor: string }[] = [
      { status: "todo", label: "Todo", bgColor: "#e2e8f0", textColor: "#475569" },
      { status: "in-progress", label: "In Progress", bgColor: "#dbeafe", textColor: "#1d4ed8" },
      { status: "done", label: "Done", bgColor: "#dcfce7", textColor: "#16a34a" },
    ];

    cases.forEach(({ status, label, bgColor, textColor }) => {
      it(`renders "${label}" for status "${status}"`, () => {
        render(<StatusBadge status={status} />);
        const badge = screen.getByTestId("status-badge");

        expect(badge.textContent).toBe(label);
        expect(badge.getAttribute("data-status")).toBe(status);
        expect(badge.style.backgroundColor).toBe(bgColor);
        expect(badge.style.color).toBe(textColor);
      });
    });
  });

  it("renders as a <span> when no onClick is provided", () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.tagName).toBe("SPAN");
  });

  it("renders as a <button> when onClick is provided", () => {
    const handler = vi.fn();
    render(<StatusBadge status="todo" onClick={handler} />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.tagName).toBe("BUTTON");
  });

  it("calls onClick with the current status when clicked", () => {
    const handler = vi.fn();
    render(<StatusBadge status="in-progress" onClick={handler} />);
    const badge = screen.getByTestId("status-badge");

    fireEvent.click(badge);

    expect(handler).toHaveBeenCalledTimes(1);
    expect(handler).toHaveBeenCalledWith("in-progress");
  });

  it("does not throw when clicked without an onClick handler", () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");

    expect(() => fireEvent.click(badge)).not.toThrow();
  });

  it("has cursor pointer when onClick is provided", () => {
    const handler = vi.fn();
    render(<StatusBadge status="todo" onClick={handler} />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.cursor).toBe("pointer");
  });

  it("has cursor default when onClick is not provided", () => {
    render(<StatusBadge status="todo" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.cursor).toBe("default");
  });

  it("has correct aria-label for accessibility", () => {
    render(<StatusBadge status="in-progress" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.getAttribute("aria-label")).toBe("Status: In Progress");
  });

  it("applies pill-shaped border radius", () => {
    render(<StatusBadge status="done" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge.style.borderRadius).toBe("9999px");
  });
});
