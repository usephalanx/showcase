import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "../App";

/**
 * Unit tests for the App component.
 *
 * Verifies that the component renders the expected text and applies
 * the correct yellow-themed CSS module classes.
 */
describe("App", () => {
  it("renders 'yellow world' text", () => {
    render(<App />);
    const heading = screen.getByText("yellow world");
    expect(heading).toBeInTheDocument();
  });

  it("renders the heading as an h1 element", () => {
    render(<App />);
    const heading = screen.getByText("yellow world");
    expect(heading.tagName).toBe("H1");
  });

  it("applies container class to the wrapper div", () => {
    render(<App />);
    const container = screen.getByTestId("app-container");
    expect(container).toHaveClass("container");
  });

  it("applies heading class to the h1 element", () => {
    render(<App />);
    const heading = screen.getByText("yellow world");
    expect(heading).toHaveClass("heading");
  });

  it("has a data-testid attribute on the container", () => {
    render(<App />);
    const container = screen.getByTestId("app-container");
    expect(container).toBeInTheDocument();
  });
});
