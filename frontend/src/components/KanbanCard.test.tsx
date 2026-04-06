import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { DragDropContext, Droppable } from "react-beautiful-dnd";
import KanbanCard, { Card } from "./KanbanCard";

/**
 * Helper: wraps a KanbanCard in the required react-beautiful-dnd context.
 */
function renderInDndContext(
  card: Card,
  index: number = 0,
  props: Partial<React.ComponentProps<typeof KanbanCard>> = {}
) {
  return render(
    <DragDropContext onDragEnd={() => {}}>
      <Droppable droppableId="test-column">
        {(provided) => (
          <div ref={provided.innerRef} {...provided.droppableProps}>
            <KanbanCard card={card} index={index} {...props} />
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}

const baseCard: Card = {
  id: 1,
  title: "Implement auth",
  description: "Set up OAuth 2.0 with Google and GitHub providers for the application.",
  slug: "implement-auth",
  tags: [
    { id: 10, name: "backend", color: "#ef4444" },
    { id: 20, name: "security" },
  ],
};

describe("KanbanCard", () => {
  it("renders without crashing", () => {
    renderInDndContext(baseCard);
    expect(screen.getByTestId("kanban-card-implement-auth")).toBeInTheDocument();
  });

  it("displays the card title", () => {
    renderInDndContext(baseCard);
    expect(screen.getByTestId("kanban-card-title")).toHaveTextContent(
      "Implement auth"
    );
  });

  it("displays the card description", () => {
    renderInDndContext(baseCard);
    expect(screen.getByTestId("kanban-card-description")).toBeInTheDocument();
    expect(screen.getByTestId("kanban-card-description").textContent).toContain(
      "Set up OAuth 2.0"
    );
  });

  it("does not render description element when description is undefined", () => {
    const card: Card = { ...baseCard, description: undefined };
    renderInDndContext(card);
    expect(screen.queryByTestId("kanban-card-description")).not.toBeInTheDocument();
  });

  it("truncates a long description", () => {
    const longDesc = "A".repeat(200);
    const card: Card = { ...baseCard, description: longDesc };
    renderInDndContext(card, 0, { descriptionMaxLength: 50 });
    const descEl = screen.getByTestId("kanban-card-description");
    // Should be truncated: 50 chars max + ellipsis
    expect(descEl.textContent!.length).toBeLessThanOrEqual(52);
    expect(descEl.textContent).toContain("…");
  });

  it("does not truncate a short description", () => {
    const shortDesc = "Short desc.";
    const card: Card = { ...baseCard, description: shortDesc };
    renderInDndContext(card);
    expect(screen.getByTestId("kanban-card-description")).toHaveTextContent(
      shortDesc
    );
  });

  it("renders tag badges", () => {
    renderInDndContext(baseCard);
    expect(screen.getByTestId("kanban-card-tags")).toBeInTheDocument();
    expect(screen.getByTestId("kanban-card-tag-10")).toHaveTextContent("backend");
    expect(screen.getByTestId("kanban-card-tag-20")).toHaveTextContent("security");
  });

  it("applies explicit tag color as background", () => {
    renderInDndContext(baseCard);
    const tagEl = screen.getByTestId("kanban-card-tag-10");
    expect(tagEl).toHaveStyle({ backgroundColor: "#ef4444" });
  });

  it("applies default color when tag has no explicit color", () => {
    renderInDndContext(baseCard);
    const tagEl = screen.getByTestId("kanban-card-tag-20");
    // second tag, index 1 → DEFAULT_TAG_COLORS[1] = "#8b5cf6"
    expect(tagEl).toHaveStyle({ backgroundColor: "#8b5cf6" });
  });

  it("does not render tags container when there are no tags", () => {
    const card: Card = { ...baseCard, tags: [] };
    renderInDndContext(card);
    expect(screen.queryByTestId("kanban-card-tags")).not.toBeInTheDocument();
  });

  it("calls onClick when the card is clicked", () => {
    const handleClick = vi.fn();
    renderInDndContext(baseCard, 0, { onClick: handleClick });
    fireEvent.click(screen.getByTestId("kanban-card-implement-auth"));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(baseCard);
  });

  it("calls onClick on Enter key press", () => {
    const handleClick = vi.fn();
    renderInDndContext(baseCard, 0, { onClick: handleClick });
    const cardEl = screen.getByTestId("kanban-card-implement-auth");
    fireEvent.keyDown(cardEl, { key: "Enter" });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("calls onClick on Space key press", () => {
    const handleClick = vi.fn();
    renderInDndContext(baseCard, 0, { onClick: handleClick });
    const cardEl = screen.getByTestId("kanban-card-implement-auth");
    fireEvent.keyDown(cardEl, { key: " " });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("does not throw when clicked without an onClick handler", () => {
    renderInDndContext(baseCard);
    expect(() => {
      fireEvent.click(screen.getByTestId("kanban-card-implement-auth"));
    }).not.toThrow();
  });

  it("uses the card slug as the draggableId", () => {
    renderInDndContext(baseCard);
    const cardEl = screen.getByTestId("kanban-card-implement-auth");
    // react-beautiful-dnd sets data-rbd-draggable-id
    expect(cardEl.getAttribute("data-rbd-draggable-id")).toBe("implement-auth");
  });

  it("sets the description as title attribute for full-text tooltip", () => {
    renderInDndContext(baseCard);
    const descEl = screen.getByTestId("kanban-card-description");
    expect(descEl.getAttribute("title")).toBe(baseCard.description);
  });
});
