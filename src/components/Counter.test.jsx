/**
 * Unit tests for the Counter component.
 *
 * Verifies initial render, increment behaviour, decrement behaviour,
 * and support for negative numbers.
 */
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Counter from "./Counter";

describe("Counter component", () => {
  it("renders with an initial count of 0", () => {
    render(<Counter />);
    const display = screen.getByTestId("count-display");
    expect(display).toHaveTextContent("0");
  });

  it("increments the count when Increment button is clicked", () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole("button", { name: /increment/i });
    fireEvent.click(incrementBtn);
    expect(screen.getByTestId("count-display")).toHaveTextContent("1");
  });

  it("decrements the count when Decrement button is clicked", () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole("button", { name: /decrement/i });
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId("count-display")).toHaveTextContent("-1");
  });

  it("handles multiple increments correctly", () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole("button", { name: /increment/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    expect(screen.getByTestId("count-display")).toHaveTextContent("3");
  });

  it("handles multiple decrements correctly", () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole("button", { name: /decrement/i });
    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId("count-display")).toHaveTextContent("-2");
  });

  it("handles mixed increment and decrement clicks", () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole("button", { name: /increment/i });
    const decrementBtn = screen.getByRole("button", { name: /decrement/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId("count-display")).toHaveTextContent("1");
  });

  it("renders both Increment and Decrement buttons", () => {
    render(<Counter />);
    expect(screen.getByRole("button", { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /decrement/i })).toBeInTheDocument();
  });
});
