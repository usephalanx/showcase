import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import BoardCard, { Board } from "./BoardCard";

const mockBoard: Board = {
  title: "Project Alpha",
  slug: "project-alpha",
  description: "A board for tracking Project Alpha tasks and milestones.",
  columnCount: 4,
  cardCount: 23,
};

describe("BoardCard", () => {
  it("renders without crashing", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card")).toBeTruthy();
  });

  it("displays the board title", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-title").textContent).toBe(
      "Project Alpha"
    );
  });

  it("displays the board description", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-description").textContent).toBe(
      "A board for tracking Project Alpha tasks and milestones."
    );
  });

  it("does not render description when it is undefined", () => {
    const boardNoDesc: Board = {
      title: "No Desc Board",
      slug: "no-desc-board",
      columnCount: 1,
      cardCount: 0,
    };
    render(<BoardCard board={boardNoDesc} />);
    expect(screen.queryByTestId("board-card-description")).toBeNull();
  });

  it("displays the correct column count with plural", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toContain(
      "4 columns"
    );
  });

  it("displays singular 'column' when count is 1", () => {
    const singleCol: Board = {
      title: "Single Col",
      slug: "single-col",
      columnCount: 1,
      cardCount: 5,
    };
    render(<BoardCard board={singleCol} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toContain(
      "1 column"
    );
    expect(
      screen.getByTestId("board-card-column-count").textContent
    ).not.toContain("columns");
  });

  it("displays the correct card count with plural", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-card-count").textContent).toContain(
      "23 cards"
    );
  });

  it("displays singular 'card' when count is 1", () => {
    const singleCard: Board = {
      title: "Single Card",
      slug: "single-card",
      columnCount: 2,
      cardCount: 1,
    };
    render(<BoardCard board={singleCard} />);
    expect(screen.getByTestId("board-card-card-count").textContent).toContain(
      "1 card"
    );
    expect(
      screen.getByTestId("board-card-card-count").textContent
    ).not.toContain("cards");
  });

  it("links to /boards/:slug", () => {
    render(<BoardCard board={mockBoard} />);
    const link = screen.getByTestId("board-card-link") as HTMLAnchorElement;
    expect(link.getAttribute("href")).toBe("/boards/project-alpha");
  });

  it("renders the gradient accent border element", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-accent")).toBeTruthy();
  });

  it("handles zero counts correctly", () => {
    const emptyBoard: Board = {
      title: "Empty Board",
      slug: "empty-board",
      description: "Nothing here yet.",
      columnCount: 0,
      cardCount: 0,
    };
    render(<BoardCard board={emptyBoard} />);
    expect(screen.getByTestId("board-card-column-count").textContent).toContain(
      "0 columns"
    );
    expect(screen.getByTestId("board-card-card-count").textContent).toContain(
      "0 cards"
    );
  });

  it("renders the stats section", () => {
    render(<BoardCard board={mockBoard} />);
    expect(screen.getByTestId("board-card-stats")).toBeTruthy();
  });
});
