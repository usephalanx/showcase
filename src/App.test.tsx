import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders the Hello World heading", () => {
    render(<App />);
    const heading = screen.getByTestId("hello-heading");
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Hello World");
  });

  it("renders the heading as an h1 element", () => {
    render(<App />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Hello World");
  });

  it("applies the expected heading styles", () => {
    render(<App />);
    const heading = screen.getByTestId("hello-heading");
    expect(heading).toHaveStyle({ fontSize: "3rem", color: "#333" });
  });

  it("applies the expected container styles", () => {
    render(<App />);
    const heading = screen.getByTestId("hello-heading");
    const container = heading.parentElement;
    expect(container).toHaveStyle({
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
    });
  });
});
