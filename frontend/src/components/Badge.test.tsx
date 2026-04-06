import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Badge from "./Badge";

describe("Badge", () => {
  it("renders without crashing", () => {
    render(<Badge label="Design" />);
    expect(screen.getByTestId("badge")).toBeTruthy();
  });

  it("displays the label text", () => {
    render(<Badge label="Frontend" />);
    expect(screen.getByTestId("badge-label").textContent).toBe("Frontend");
  });

  it("does not show remove button by default", () => {
    render(<Badge label="Bug" />);
    expect(screen.queryByTestId("badge-remove")).toBeNull();
  });

  it("shows remove button when removable is true", () => {
    render(<Badge label="Bug" removable />);
    expect(screen.getByTestId("badge-remove")).toBeTruthy();
  });

  it("calls onRemove when remove button is clicked", () => {
    const onRemove = vi.fn();
    render(<Badge label="Bug" removable onRemove={onRemove} />);
    fireEvent.click(screen.getByTestId("badge-remove"));
    expect(onRemove).toHaveBeenCalledTimes(1);
  });

  it("applies explicit color to the text", () => {
    render(<Badge label="Urgent" color="#e11d48" />);
    const badge = screen.getByTestId("badge");
    expect(badge.style.color).toBe("#e11d48");
  });

  it("auto-generates consistent color from label when no color prop", () => {
    const { unmount } = render(<Badge label="Taxonomy" />);
    const color1 = screen.getByTestId("badge").style.color;
    unmount();
    render(<Badge label="Taxonomy" />);
    const color2 = screen.getByTestId("badge").style.color;
    expect(color1).toBe(color2);
  });

  it("generates different colors for different labels", () => {
    const { unmount } = render(<Badge label="Alpha" />);
    const colorA = screen.getByTestId("badge").style.color;
    unmount();
    render(<Badge label="Omega" />);
    const colorB = screen.getByTestId("badge").style.color;
    expect(colorA).not.toBe(colorB);
  });

  it("renders in small size", () => {
    render(<Badge label="Small" size="sm" />);
    const badge = screen.getByTestId("badge");
    expect(badge.style.fontSize).toBe("0.7rem");
  });

  it("renders in medium size by default", () => {
    render(<Badge label="Medium" />);
    const badge = screen.getByTestId("badge");
    expect(badge.style.fontSize).toBe("0.8rem");
  });

  it("has pill shape (large border-radius)", () => {
    render(<Badge label="Pill" />);
    const badge = screen.getByTestId("badge");
    expect(badge.style.borderRadius).toBe("9999px");
  });

  it("has subtle (low-opacity) background color", () => {
    render(<Badge label="Subtle" color="#3b82f6" />);
    const badge = screen.getByTestId("badge");
    // Background should contain rgba with 0.15 opacity
    expect(badge.style.backgroundColor).toContain("0.15");
  });

  it("applies custom className", () => {
    render(<Badge label="Custom" className="my-custom-class" />);
    const badge = screen.getByTestId("badge");
    expect(badge.className).toContain("my-custom-class");
  });

  it("remove button has correct aria-label", () => {
    render(<Badge label="Feature" removable />);
    const btn = screen.getByTestId("badge-remove");
    expect(btn.getAttribute("aria-label")).toBe("Remove Feature");
  });

  it("does not crash when removable is true but onRemove is undefined", () => {
    render(<Badge label="Safe" removable />);
    expect(() => {
      fireEvent.click(screen.getByTestId("badge-remove"));
    }).not.toThrow();
  });
});
