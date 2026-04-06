import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import BoardCard, { type BoardCardProps } from "./BoardCard";

const defaultProps: BoardCardProps = {
  title: "Project Alpha",
  slug: "project-alpha",
  description: "A board for tracking project alpha tasks and deliverables.",
  columnCount: 3,
  cardCount: 12,
};

describe("BoardCard", () => {
  it("renders without crashing", () => {
    render(<BoardCard {...defaultProps} />);
    expect(screen.getByTestId("board-card")).toBeDefined();
  });

  it("displays the board title", () => {
    render(<BoardCard {...defaultProps} />);
    expect(screen.getByTestId("board-card-title").textContent).toBe(
      "Project Alpha"
    );
  });

  it("displays the board description when provided", () => {
    render(<BoardCard {...defaultProps} />);
    expect(screen.getByTestId("board-card-description").textContent).toBe(
      "A board for tracking project alpha tasks and deliverables."
    );
  });

  it("does not render description when it is null", () => {
    render(<BoardCard {...defaultProps} description={null} />);
    expect(screen.queryByTestId("board-card-description")).toBeNull();
  });

  it("does not render description when it is undefined", () => {
    const { description: _, ...propsWithoutDesc } = defaultProps;
    render(<BoardCard {...propsWithoutDesc} />);
    expect(screen.queryByTestId("board-card-description")).toBeNull();
  });

  it("displays the correct column count with plural", () => {
    render(<BoardCard {...defaultProps} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toBe(
      "3 columns"
    );
  });

  it("displays singular 'column' when count is 1", () => {
    render(<BoardCard {...defaultProps} columnCount={1} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toBe(
      "1 column"
    );
  });

  it("displays the correct card count with plural", () => {
    render(<BoardCard {...defaultProps} />);
    expect(screen.getByTestId("board-card-card-count").textContent).toBe(
      "12 cards"
    );
  });

  it("displays singular 'card' when count is 1", () => {
    render(<BoardCard {...defaultProps} cardCount={1} />);
    expect(screen.getByTestId("board-card-card-count").textContent).toBe(
      "1 card"
    );
  });

  it("displays 0 columns and 0 cards correctly", () => {
    render(<BoardCard {...defaultProps} columnCount={0} cardCount={0} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toBe(
      "0 columns"
    );
    expect(screen.getByTestId("board-card-card-count").textContent).toBe(
      "0 cards"
    );
  });

  it("links to /boards/:slug", () => {
    render(<BoardCard {...defaultProps} />);
    const link = screen.getByTestId("board-card") as HTMLAnchorElement;
    expect(link.getAttribute("href")).toBe("/boards/project-alpha");
  });

  it("calls onClick with slug when onClick is provided", () => {
    const handleClick = vi.fn();
    render(<BoardCard {...defaultProps} onClick={handleClick} />);
    fireEvent.click(screen.getByTestId("board-card"));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith("project-alpha");
  });

  it("does not call onClick when not provided", () => {
    render(<BoardCard {...defaultProps} />);
    // Should not throw when clicked without onClick handler
    fireEvent.click(screen.getByTestId("board-card"));
  });

  it("renders as an anchor element", () => {
    render(<BoardCard {...defaultProps} />);
    const el = screen.getByTestId("board-card");
    expect(el.tagName).toBe("A");
  });

  it("handles a different slug correctly", () => {
    render(<BoardCard {...defaultProps} slug="my-board-2" title="My Board" />);
    const link = screen.getByTestId("board-card") as HTMLAnchorElement;
    expect(link.getAttribute("href")).toBe("/boards/my-board-2");
    expect(screen.getByTestId("board-card-title").textContent).toBe("My Board");
  });
});
