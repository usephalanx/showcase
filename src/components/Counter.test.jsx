import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Counter from "./Counter";

describe("Counter component", () => {
  it("renders with initial count of 0", () => {
    render(<Counter />);
    const display = screen.getByTestId("count-display");
    expect(display).toHaveTextContent("0");
  });

  it("increments the count when Increment button is clicked", () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole("button", { name: /increment/i });
    const display = screen.getByTestId("count-display");

    fireEvent.click(incrementBtn);
    expect(display).toHaveTextContent("1");

    fireEvent.click(incrementBtn);
    expect(display).toHaveTextContent("2");
  });

  it("decrements the count when Decrement button is clicked", () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole("button", { name: /decrement/i });
    const display = screen.getByTestId("count-display");

    fireEvent.click(decrementBtn);
    expect(display).toHaveTextContent("-1");

    fireEvent.click(decrementBtn);
    expect(display).toHaveTextContent("-2");
  });

  it("handles rapid increment and decrement clicks correctly", () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole("button", { name: /increment/i });
    const decrementBtn = screen.getByRole("button", { name: /decrement/i });
    const display = screen.getByTestId("count-display");

    for (let i = 0; i < 5; i++) {
      fireEvent.click(incrementBtn);
    }
    expect(display).toHaveTextContent("5");

    for (let i = 0; i < 3; i++) {
      fireEvent.click(decrementBtn);
    }
    expect(display).toHaveTextContent("2");
  });

  it("renders Increment and Decrement buttons", () => {
    render(<Counter />);
    expect(screen.getByRole("button", { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /decrement/i })).toBeInTheDocument();
  });
});
