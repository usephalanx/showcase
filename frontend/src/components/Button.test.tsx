import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Button from "./Button";

describe("Button", () => {
  it("renders without crashing", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeDefined();
  });

  it("renders children text correctly", () => {
    render(<Button>Save Changes</Button>);
    expect(screen.getByRole("button").textContent).toBe("Save Changes");
  });

  // --- Variant tests ---

  it("applies primary variant classes by default", () => {
    render(<Button>Primary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("bg-blue-600");
    expect(btn.className).toContain("text-white");
  });

  it("applies secondary variant classes", () => {
    render(<Button variant="secondary">Secondary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("bg-gray-100");
    expect(btn.className).toContain("text-gray-800");
  });

  it("applies danger variant classes", () => {
    render(<Button variant="danger">Delete</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("bg-red-600");
    expect(btn.className).toContain("text-white");
  });

  it("applies ghost variant classes", () => {
    render(<Button variant="ghost">Ghost</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("bg-transparent");
    expect(btn.className).toContain("text-gray-700");
  });

  // --- Size tests ---

  it("applies sm size classes", () => {
    render(<Button size="sm">Small</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("px-3");
    expect(btn.className).toContain("py-1.5");
    expect(btn.className).toContain("text-sm");
  });

  it("applies md size classes by default", () => {
    render(<Button>Medium</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("px-4");
    expect(btn.className).toContain("py-2");
    expect(btn.className).toContain("text-base");
  });

  it("applies lg size classes", () => {
    render(<Button size="lg">Large</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("px-6");
    expect(btn.className).toContain("py-3");
    expect(btn.className).toContain("text-lg");
  });

  // --- Disabled state ---

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    expect(btn.className).toContain("opacity-50");
    expect(btn.className).toContain("cursor-not-allowed");
  });

  it("does not fire onClick when disabled", () => {
    const handleClick = vi.fn();
    render(
      <Button disabled onClick={handleClick}>
        Disabled
      </Button>
    );
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).not.toHaveBeenCalled();
  });

  // --- Loading state ---

  it("shows spinner when loading", () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByTestId("button-spinner")).toBeDefined();
  });

  it("is disabled when loading", () => {
    render(<Button loading>Loading</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    expect(btn.className).toContain("opacity-50");
  });

  it("sets aria-busy when loading", () => {
    render(<Button loading>Loading</Button>);
    const btn = screen.getByRole("button");
    expect(btn.getAttribute("aria-busy")).toBe("true");
  });

  it("does not show spinner when not loading", () => {
    render(<Button>Not Loading</Button>);
    expect(screen.queryByTestId("button-spinner")).toBeNull();
  });

  it("does not fire onClick when loading", () => {
    const handleClick = vi.fn();
    render(
      <Button loading onClick={handleClick}>
        Loading
      </Button>
    );
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).not.toHaveBeenCalled();
  });

  // --- onClick ---

  it("fires onClick when clicked", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // --- className ---

  it("appends custom className", () => {
    render(<Button className="mt-4 w-full">Custom</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("mt-4");
    expect(btn.className).toContain("w-full");
  });

  // --- type ---

  it("defaults to type button", () => {
    render(<Button>Default Type</Button>);
    expect(screen.getByRole("button").getAttribute("type")).toBe("button");
  });

  it("supports type submit", () => {
    render(<Button type="submit">Submit</Button>);
    expect(screen.getByRole("button").getAttribute("type")).toBe("submit");
  });

  // --- Transition classes ---

  it("includes transition utility classes", () => {
    render(<Button>Transitions</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("transition-all");
    expect(btn.className).toContain("duration-150");
    expect(btn.className).toContain("ease-in-out");
  });

  // --- Focus ring ---

  it("includes focus ring classes", () => {
    render(<Button>Focus</Button>);
    const btn = screen.getByRole("button");
    expect(btn.className).toContain("focus:ring-2");
    expect(btn.className).toContain("focus:ring-offset-2");
  });

  // --- Renders JSX children ---

  it("renders JSX children", () => {
    render(
      <Button>
        <span data-testid="icon">★</span> Star
      </Button>
    );
    expect(screen.getByTestId("icon")).toBeDefined();
    expect(screen.getByRole("button").textContent).toContain("Star");
  });
});
