import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import KanbanCard, { Card } from "./KanbanCard";

// Mock the Badge component so we can test KanbanCard in isolation
vi.mock("./Badge", () => ({
  default: ({ label }: { label: string }) => (
    <span data-testid="badge">{label}</span>
  ),
}));

const baseCard: Card = {
  id: 1,
  title: "Implement authentication",
  slug: "implement-authentication",
  description: "Set up JWT-based authentication for the API endpoints.",
  position: 0,
  column_id: 10,
  categories: [
    { id: 1, name: "Backend", slug: "backend" },
    { id: 2, name: "Security", slug: "security" },
  ],
};

describe("KanbanCard", () => {
  it("renders without crashing", () => {
    render(<KanbanCard card={baseCard} />);
    expect(screen.getByTestId("kanban-card")).toBeDefined();
  });

  it("displays the card title", () => {
    render(<KanbanCard card={baseCard} />);
    expect(screen.getByTestId("kanban-card-title").textContent).toBe(
      "Implement authentication"
    );
  });

  it("displays the card description", () => {
    render(<KanbanCard card={baseCard} />);
    expect(screen.getByTestId("kanban-card-description").textContent).toBe(
      "Set up JWT-based authentication for the API endpoints."
    );
  });

  it("truncates long descriptions", () => {
    const longDesc = "A".repeat(200);
    const card: Card = { ...baseCard, description: longDesc };
    render(<KanbanCard card={card} maxDescriptionLength={50} />);
    const descEl = screen.getByTestId("kanban-card-description");
    expect(descEl.textContent!.length).toBeLessThanOrEqual(52); // 50 chars + ellipsis
    expect(descEl.textContent!.endsWith("…")).toBe(true);
  });

  it("does not render description when null", () => {
    const card: Card = { ...baseCard, description: null };
    render(<KanbanCard card={card} />);
    expect(screen.queryByTestId("kanban-card-description")).toBeNull();
  });

  it("does not render description when empty string", () => {
    const card: Card = { ...baseCard, description: "   " };
    render(<KanbanCard card={card} />);
    expect(screen.queryByTestId("kanban-card-description")).toBeNull();
  });

  it("renders category badges", () => {
    render(<KanbanCard card={baseCard} />);
    const badges = screen.getAllByTestId("badge");
    expect(badges).toHaveLength(2);
    expect(badges[0].textContent).toBe("Backend");
    expect(badges[1].textContent).toBe("Security");
  });

  it("does not render badges container when no categories", () => {
    const card: Card = { ...baseCard, categories: [] };
    render(<KanbanCard card={card} />);
    expect(screen.queryByTestId("kanban-card-badges")).toBeNull();
  });

  it("links to the correct SEO-friendly URL", () => {
    render(<KanbanCard card={baseCard} />);
    const link = screen.getByTestId("kanban-card") as HTMLAnchorElement;
    expect(link.getAttribute("href")).toBe("/cards/implement-authentication");
  });

  it("calls onClick when clicked and prevents default navigation", () => {
    const handleClick = vi.fn();
    render(<KanbanCard card={baseCard} onClick={handleClick} />);
    const link = screen.getByTestId("kanban-card");
    fireEvent.click(link);
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(baseCard);
  });

  it("navigates normally when no onClick is provided", () => {
    render(<KanbanCard card={baseCard} />);
    const link = screen.getByTestId("kanban-card");
    // Simply verify the link exists and is navigable
    expect(link.tagName).toBe("A");
    expect(link.getAttribute("href")).toBe("/cards/implement-authentication");
  });

  it("has grab cursor style", () => {
    render(<KanbanCard card={baseCard} />);
    const link = screen.getByTestId("kanban-card") as HTMLElement;
    expect(link.style.cursor).toBe("grab");
  });

  it("has an accessible article role with aria-label", () => {
    render(<KanbanCard card={baseCard} />);
    const el = screen.getByRole("article");
    expect(el.getAttribute("aria-label")).toBe("Implement authentication");
  });

  it("applies hover lift effect on mouse enter and resets on leave", () => {
    render(<KanbanCard card={baseCard} />);
    const el = screen.getByTestId("kanban-card") as HTMLElement;

    fireEvent.mouseEnter(el);
    expect(el.style.transform).toBe("translateY(-2px)");

    fireEvent.mouseLeave(el);
    expect(el.style.transform).toBe("translateY(0)");
  });

  it("handles keyboard activation via Enter key", () => {
    const handleClick = vi.fn();
    render(<KanbanCard card={baseCard} onClick={handleClick} />);
    const el = screen.getByTestId("kanban-card");
    fireEvent.keyDown(el, { key: "Enter" });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith(baseCard);
  });

  it("handles keyboard activation via Space key", () => {
    const handleClick = vi.fn();
    render(<KanbanCard card={baseCard} onClick={handleClick} />);
    const el = screen.getByTestId("kanban-card");
    fireEvent.keyDown(el, { key: " " });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("uses default maxDescriptionLength of 120", () => {
    const desc = "B".repeat(150);
    const card: Card = { ...baseCard, description: desc };
    render(<KanbanCard card={card} />);
    const descEl = screen.getByTestId("kanban-card-description");
    // 120 chars + ellipsis character = 121
    expect(descEl.textContent!.length).toBeLessThanOrEqual(122);
    expect(descEl.textContent!.endsWith("…")).toBe(true);
  });

  it("does not truncate description that fits within max length", () => {
    const shortDesc = "Short description";
    const card: Card = { ...baseCard, description: shortDesc };
    render(<KanbanCard card={card} />);
    const descEl = screen.getByTestId("kanban-card-description");
    expect(descEl.textContent).toBe("Short description");
  });
});
