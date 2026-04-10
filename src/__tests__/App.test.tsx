import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "../App";

describe("App component", () => {
  it("renders 'yellow world' text", () => {
    render(<App />);
    const heading = screen.getByText("yellow world");
    expect(heading).toBeInTheDocument();
  });

  it("renders the app container with correct class", () => {
    render(<App />);
    const container = screen.getByTestId("app-container");
    expect(container).toBeInTheDocument();
    expect(container).toHaveClass("container");
  });

  it("renders heading with correct class", () => {
    render(<App />);
    const heading = screen.getByText("yellow world");
    expect(heading).toHaveClass("heading");
  });

  it("heading is an h1 element", () => {
    render(<App />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toHaveTextContent("yellow world");
  });
});
