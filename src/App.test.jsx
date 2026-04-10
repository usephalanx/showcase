import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App component", () => {
  it("renders the application heading", () => {
    render(<App />);
    expect(screen.getByText("Mini React Counter App")).toBeInTheDocument();
  });

  it("renders the Counter component", () => {
    render(<App />);
    expect(screen.getByText("Counter")).toBeInTheDocument();
    expect(screen.getByTestId("count-display")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /decrement/i })).toBeInTheDocument();
  });

  it("renders the count display starting at 0", () => {
    render(<App />);
    expect(screen.getByTestId("count-display")).toHaveTextContent("0");
  });
});
