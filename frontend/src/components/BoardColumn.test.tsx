import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { DndContext } from "@dnd-kit/core";
import BoardColumn, { ColumnData, ColumnCard } from "./BoardColumn";

/**
 * Helper to wrap component in DndContext since useDroppable requires it.
 */
function renderWithDnd(ui: React.ReactElement) {
  return render(<DndContext>{ui}</DndContext>);
}

const mockCards: ColumnCard[] = [
  { id: 1, title: "Card One", slug: "card-one", position: 0 },
  { id: 2, title: "Card Two", slug: "card-two", position: 1 },
  { id: 3, title: "Card Three", slug: "card-three", position: 2 },
];

const mockColumn: ColumnData = {
  id: 10,
  title: "To Do",
  position: 0,
  color: "#ef4444",
  cards: mockCards,
};

const emptyColumn: ColumnData = {
  id: 20,
  title: "Done",
  position: 2,
  cards: [],
};

describe("BoardColumn", () => {
  it("renders without crashing", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.getByTestId("board-column-10")).toBeInTheDocument();
  });

  it("displays the column title", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.getByTestId("column-title-10")).toHaveTextContent("To Do");
  });

  it("displays the card count", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.getByTestId("column-count-10")).toHaveTextContent("3");
  });

  it("renders all cards in the column", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.getByTestId("card-1")).toHaveTextContent("Card One");
    expect(screen.getByTestId("card-2")).toHaveTextContent("Card Two");
    expect(screen.getByTestId("card-3")).toHaveTextContent("Card Three");
  });

  it("renders the accent bar with the column color", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    const accent = screen.getByTestId("column-accent-10");
    expect(accent).toBeInTheDocument();
    expect(accent.style.backgroundColor).toBe("rgb(239, 68, 68)");
  });

  it("uses default accent color when none provided", () => {
    const columnNoColor: ColumnData = {
      id: 30,
      title: "Backlog",
      position: 0,
      cards: [],
    };
    renderWithDnd(<BoardColumn column={columnNoColor} />);
    const accent = screen.getByTestId("column-accent-30");
    expect(accent.style.backgroundColor).toBe("rgb(99, 102, 241)");
  });

  it("shows empty state when no cards", () => {
    renderWithDnd(<BoardColumn column={emptyColumn} />);
    expect(screen.getByTestId("column-empty-20")).toHaveTextContent("No cards");
    expect(screen.getByTestId("column-count-20")).toHaveTextContent("0");
  });

  it("calls onCardClick when a card is clicked", () => {
    const handleClick = vi.fn();
    renderWithDnd(
      <BoardColumn column={mockColumn} onCardClick={handleClick} />,
    );
    fireEvent.click(screen.getByTestId("card-2"));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockCards[1]);
  });

  it("calls onCardClick when Enter key is pressed on a card", () => {
    const handleClick = vi.fn();
    renderWithDnd(
      <BoardColumn column={mockColumn} onCardClick={handleClick} />,
    );
    fireEvent.keyDown(screen.getByTestId("card-1"), { key: "Enter" });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(mockCards[0]);
  });

  it("renders add button and calls onAddCard with column id", () => {
    const handleAdd = vi.fn();
    renderWithDnd(
      <BoardColumn column={mockColumn} onAddCard={handleAdd} />,
    );
    const addBtn = screen.getByTestId("column-add-btn-10");
    expect(addBtn).toBeInTheDocument();
    fireEvent.click(addBtn);
    expect(handleAdd).toHaveBeenCalledTimes(1);
    expect(handleAdd).toHaveBeenCalledWith(10);
  });

  it("does not render add button when onAddCard is not provided", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.queryByTestId("column-add-btn-10")).not.toBeInTheDocument();
  });

  it("renders the droppable container", () => {
    renderWithDnd(<BoardColumn column={mockColumn} />);
    expect(screen.getByTestId("column-droppable-10")).toBeInTheDocument();
  });

  it("uses custom renderCard when provided", () => {
    const customRender = (card: ColumnCard) => (
      <div data-testid={`custom-card-${card.id}`}>Custom: {card.title}</div>
    );
    renderWithDnd(
      <BoardColumn column={mockColumn} renderCard={customRender} />,
    );
    expect(screen.getByTestId("custom-card-1")).toHaveTextContent(
      "Custom: Card One",
    );
    expect(screen.getByTestId("custom-card-2")).toHaveTextContent(
      "Custom: Card Two",
    );
    // Default cards should not render
    expect(screen.queryByTestId("card-1")).not.toBeInTheDocument();
  });

  it("add button has correct aria-label", () => {
    const handleAdd = vi.fn();
    renderWithDnd(
      <BoardColumn column={mockColumn} onAddCard={handleAdd} />,
    );
    const addBtn = screen.getByTestId("column-add-btn-10");
    expect(addBtn).toHaveAttribute("aria-label", "Add card to To Do");
  });
});
