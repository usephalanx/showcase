import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "./App";

/**
 * Unit tests for the root App component.
 */
describe("App", () => {
  it("renders the Hello World heading", () => {
    render(<App />);
    const heading = screen.getByTestId("hello-heading");
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Hello World");
  });

  it("renders an h1 element", () => {
    render(<App />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
  });
});
