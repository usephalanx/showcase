import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import EmptyState, { EmptyStateProps } from "./EmptyState";

const baseProps: EmptyStateProps = {
  icon: "📋",
  title: "No boards yet",
  description: "Create your first board to get started organizing tasks.",
};

describe("EmptyState", () => {
  it("renders without crashing", () => {
    render(<EmptyState {...baseProps} />);
    expect(screen.getByTestId("empty-state")).toBeTruthy();
  });

  it("displays the provided icon", () => {
    render(<EmptyState {...baseProps} />);
    const iconEl = screen.getByTestId("empty-state-icon");
    expect(iconEl.textContent).toBe("📋");
  });

  it("displays the provided title", () => {
    render(<EmptyState {...baseProps} />);
    expect(screen.getByTestId("empty-state-title").textContent).toBe(
      "No boards yet"
    );
  });

  it("displays the provided description", () => {
    render(<EmptyState {...baseProps} />);
    expect(screen.getByTestId("empty-state-description").textContent).toBe(
      "Create your first board to get started organizing tasks."
    );
  });

  it("does not render the action button when actionLabel is omitted", () => {
    render(<EmptyState {...baseProps} />);
    expect(screen.queryByTestId("empty-state-action")).toBeNull();
  });

  it("does not render the action button when onAction is omitted", () => {
    render(<EmptyState {...baseProps} actionLabel="Create Board" />);
    expect(screen.queryByTestId("empty-state-action")).toBeNull();
  });

  it("renders the action button when both actionLabel and onAction are provided", () => {
    const onAction = vi.fn();
    render(
      <EmptyState
        {...baseProps}
        actionLabel="Create Board"
        onAction={onAction}
      />
    );
    const button = screen.getByTestId("empty-state-action");
    expect(button).toBeTruthy();
    expect(button.textContent).toBe("Create Board");
  });

  it("calls onAction when the action button is clicked", () => {
    const onAction = vi.fn();
    render(
      <EmptyState
        {...baseProps}
        actionLabel="Create Board"
        onAction={onAction}
      />
    );
    const button = screen.getByTestId("empty-state-action");
    fireEvent.click(button);
    expect(onAction).toHaveBeenCalledTimes(1);
  });

  it("calls onAction multiple times on multiple clicks", () => {
    const onAction = vi.fn();
    render(
      <EmptyState
        {...baseProps}
        actionLabel="Add Tag"
        onAction={onAction}
      />
    );
    const button = screen.getByTestId("empty-state-action");
    fireEvent.click(button);
    fireEvent.click(button);
    fireEvent.click(button);
    expect(onAction).toHaveBeenCalledTimes(3);
  });

  it("renders a React node as the icon (not just strings)", () => {
    const svgIcon = (
      <svg data-testid="svg-icon" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" />
      </svg>
    );
    render(
      <EmptyState
        icon={svgIcon}
        title="No cards"
        description="This column is empty."
      />
    );
    expect(screen.getByTestId("svg-icon")).toBeTruthy();
  });

  it("renders with different prop values for tags scenario", () => {
    render(
      <EmptyState
        icon="🏷️"
        title="No tags found"
        description="Tags help you categorize and filter cards."
        actionLabel="Create Tag"
        onAction={() => {}}
      />
    );
    expect(screen.getByTestId("empty-state-title").textContent).toBe(
      "No tags found"
    );
    expect(screen.getByTestId("empty-state-description").textContent).toBe(
      "Tags help you categorize and filter cards."
    );
    expect(screen.getByTestId("empty-state-action").textContent).toBe(
      "Create Tag"
    );
  });

  it("has centered layout styles on the container", () => {
    render(<EmptyState {...baseProps} />);
    const container = screen.getByTestId("empty-state");
    expect(container.style.textAlign).toBe("center");
    expect(container.style.display).toBe("flex");
    expect(container.style.flexDirection).toBe("column");
    expect(container.style.alignItems).toBe("center");
    expect(container.style.justifyContent).toBe("center");
  });
});
