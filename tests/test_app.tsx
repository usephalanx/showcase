/**
 * Tests for the root App component.
 */
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "../src/App";

describe("App", () => {
  it("renders the home page with a greeting", () => {
    render(<App />);
    const heading = screen.getByTestId("greeting");
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Hello World");
  });

  it("contains a main landmark", () => {
    render(<App />);
    const main = screen.getByRole("main");
    expect(main).toBeInTheDocument();
  });
});
