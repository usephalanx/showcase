import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TagBadge from "./TagBadge";

describe("TagBadge", () => {
  const baseProps = {
    name: "Bug",
    slug: "bug",
    color: "#e74c3c",
  };

  it("renders without crashing", () => {
    render(<TagBadge {...baseProps} />);
    expect(screen.getByTestId("tag-badge-bug")).toBeInTheDocument();
  });

  it("displays the tag name", () => {
    render(<TagBadge {...baseProps} />);
    expect(screen.getByTestId("tag-badge-name")).toHaveTextContent("Bug");
  });

  it("applies the color as background style", () => {
    render(<TagBadge {...baseProps} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).toHaveStyle({ backgroundColor: "#e74c3c" });
  });

  it("uses white text on dark backgrounds", () => {
    render(<TagBadge {...baseProps} color="#000000" />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).toHaveStyle({ color: "#ffffff" });
  });

  it("uses black text on light backgrounds", () => {
    render(<TagBadge {...baseProps} color="#ffffff" />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).toHaveStyle({ color: "#000000" });
  });

  it("renders at sm size with smaller classes", () => {
    render(<TagBadge {...baseProps} size="sm" />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge.className).toContain("text-xs");
  });

  it("renders at md size by default with md classes", () => {
    render(<TagBadge {...baseProps} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge.className).toContain("text-sm");
  });

  it("does not show remove button by default", () => {
    render(<TagBadge {...baseProps} />);
    expect(screen.queryByTestId("tag-badge-remove-bug")).not.toBeInTheDocument();
  });

  it("shows remove button when removable is true", () => {
    render(<TagBadge {...baseProps} removable />);
    expect(screen.getByTestId("tag-badge-remove-bug")).toBeInTheDocument();
  });

  it("calls onRemove with slug when remove button is clicked", () => {
    const handleRemove = vi.fn();
    render(<TagBadge {...baseProps} removable onRemove={handleRemove} />);
    fireEvent.click(screen.getByTestId("tag-badge-remove-bug"));
    expect(handleRemove).toHaveBeenCalledTimes(1);
    expect(handleRemove).toHaveBeenCalledWith("bug");
  });

  it("calls onClick with slug when badge is clicked", () => {
    const handleClick = vi.fn();
    render(<TagBadge {...baseProps} onClick={handleClick} />);
    fireEvent.click(screen.getByTestId("tag-badge-bug"));
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith("bug");
  });

  it("does not have role=button when onClick is not provided", () => {
    render(<TagBadge {...baseProps} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).not.toHaveAttribute("role");
  });

  it("has role=button when onClick is provided", () => {
    render(<TagBadge {...baseProps} onClick={vi.fn()} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).toHaveAttribute("role", "button");
  });

  it("clicking remove does not trigger onClick", () => {
    const handleClick = vi.fn();
    const handleRemove = vi.fn();
    render(
      <TagBadge
        {...baseProps}
        removable
        onClick={handleClick}
        onRemove={handleRemove}
      />
    );
    fireEvent.click(screen.getByTestId("tag-badge-remove-bug"));
    expect(handleRemove).toHaveBeenCalledTimes(1);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it("triggers onClick on Enter key press", () => {
    const handleClick = vi.fn();
    render(<TagBadge {...baseProps} onClick={handleClick} />);
    const badge = screen.getByTestId("tag-badge-bug");
    fireEvent.keyDown(badge, { key: "Enter" });
    expect(handleClick).toHaveBeenCalledTimes(1);
    expect(handleClick).toHaveBeenCalledWith("bug");
  });

  it("triggers onClick on Space key press", () => {
    const handleClick = vi.fn();
    render(<TagBadge {...baseProps} onClick={handleClick} />);
    const badge = screen.getByTestId("tag-badge-bug");
    fireEvent.keyDown(badge, { key: " " });
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("remove button has correct aria-label", () => {
    render(<TagBadge {...baseProps} removable />);
    const removeBtn = screen.getByTestId("tag-badge-remove-bug");
    expect(removeBtn).toHaveAttribute("aria-label", "Remove tag Bug");
  });

  it("handles 3-char hex color shorthand for contrast calculation", () => {
    // #fff is white → should get black text
    render(<TagBadge {...baseProps} color="#fff" />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge).toHaveStyle({ color: "#000000" });
  });

  it("has cursor-pointer class when clickable", () => {
    render(<TagBadge {...baseProps} onClick={vi.fn()} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge.className).toContain("cursor-pointer");
  });

  it("does not have cursor-pointer class when not clickable", () => {
    render(<TagBadge {...baseProps} />);
    const badge = screen.getByTestId("tag-badge-bug");
    expect(badge.className).not.toContain("cursor-pointer");
  });
});
