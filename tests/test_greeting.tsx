/**
 * Tests for the Greeting component.
 */
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Greeting from "../src/components/Greeting";

describe("Greeting", () => {
  it("renders with default name 'World'", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Hello World");
  });

  it("renders with a custom name", () => {
    render(<Greeting name="Vite" />);
    const heading = screen.getByTestId("greeting");
    expect(heading).toHaveTextContent("Hello Vite");
  });

  it("renders an h1 element", () => {
    render(<Greeting />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
  });
});
