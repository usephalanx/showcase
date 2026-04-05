/**
 * Tests for the HomePage component.
 */
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import HomePage from "../src/pages/HomePage";

describe("HomePage", () => {
  it("renders the Greeting component inside a main element", () => {
    render(<HomePage />);
    const main = screen.getByRole("main");
    expect(main).toBeInTheDocument();
  });

  it("displays the default greeting", () => {
    render(<HomePage />);
    const heading = screen.getByTestId("greeting");
    expect(heading).toHaveTextContent("Hello World");
  });
});
