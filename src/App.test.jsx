/**
 * Unit tests for the App component.
 *
 * Verifies that the App renders the Counter component successfully.
 */
import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App component", () => {
  it("renders the Counter component", () => {
    render(<App />);
    expect(screen.getByTestId("count-display")).toBeInTheDocument();
  });

  it("renders Increment and Decrement buttons via Counter", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /decrement/i })).toBeInTheDocument();
  });
});
