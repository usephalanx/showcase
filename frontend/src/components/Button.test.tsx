import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Button from "./Button";

describe("Button", () => {
  it("renders without crashing", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeDefined();
  });

  it("renders children text correctly", () => {
    render(<Button>Hello World</Button>);
    expect(screen.getByRole("button").textContent).toContain("Hello World");
  });

  // --- Variant tests ---
  it("renders with primary variant styling", () => {
    render(<Button variant="primary">Primary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.backgroundColor).toBe("rgb(37, 99, 235)");
    expect(btn.style.color).toBe("rgb(255, 255, 255)");
  });

  it("renders with secondary variant styling", () => {
    render(<Button variant="secondary">Secondary</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.backgroundColor).toBe("rgb(255, 255, 255)");
    expect(btn.style.color).toBe("rgb(31, 41, 55)");
  });

  it("renders with ghost variant styling", () => {
    render(<Button variant="ghost">Ghost</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.backgroundColor).toBe("transparent");
  });

  it("renders with danger variant styling", () => {
    render(<Button variant="danger">Danger</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.backgroundColor).toBe("rgb(220, 38, 38)");
    expect(btn.style.color).toBe("rgb(255, 255, 255)");
  });

  // --- Size tests ---
  it("renders sm size with correct padding", () => {
    render(<Button size="sm">Small</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.padding).toBe("4px 12px");
    expect(btn.style.fontSize).toBe("13px");
  });

  it("renders md size by default", () => {
    render(<Button>Medium</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.padding).toBe("8px 16px");
    expect(btn.style.fontSize).toBe("14px");
  });

  it("renders lg size with correct padding", () => {
    render(<Button size="lg">Large</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.padding).toBe("12px 24px");
    expect(btn.style.fontSize).toBe("16px");
  });

  // --- Disabled tests ---
  it("renders as disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
    expect(btn.getAttribute("aria-disabled")).toBe("true");
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

  // --- Loading tests ---
  it("shows spinner when loading", () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByTestId("button-spinner")).toBeDefined();
  });

  it("is disabled when loading", () => {
    render(<Button loading>Loading</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toBeDisabled();
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

  it("sets aria-label to loadingText when loading", () => {
    render(
      <Button loading loadingText="Please wait…">
        Submit
      </Button>
    );
    const btn = screen.getByRole("button");
    expect(btn.getAttribute("aria-label")).toBe("Please wait…");
  });

  // --- onClick tests ---
  it("fires onClick handler when clicked", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  // --- Type tests ---
  it("defaults to type=button", () => {
    render(<Button>Btn</Button>);
    expect(screen.getByRole("button").getAttribute("type")).toBe("button");
  });

  it("accepts type=submit", () => {
    render(<Button type="submit">Submit</Button>);
    expect(screen.getByRole("button").getAttribute("type")).toBe("submit");
  });

  // --- className passthrough ---
  it("passes className to the button element", () => {
    render(<Button className="custom-class">Styled</Button>);
    expect(screen.getByRole("button").classList.contains("custom-class")).toBe(true);
  });

  // --- Default variant ---
  it("defaults to primary variant when no variant is specified", () => {
    render(<Button>Default</Button>);
    const btn = screen.getByRole("button");
    expect(btn.style.backgroundColor).toBe("rgb(37, 99, 235)");
  });
});
