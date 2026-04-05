import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Greeting from "./Greeting";

describe("Greeting", () => {
  it("renders without crashing", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading).toBeDefined();
  });

  it("renders 'Hello World' by default", () => {
    render(<Greeting />);
    expect(screen.getByText("Hello World")).toBeDefined();
  });

  it("renders 'Hello World' text content in an h1 element", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading.tagName).toBe("H1");
    expect(heading.textContent).toBe("Hello World");
  });

  it("renders a custom name when the name prop is provided", () => {
    render(<Greeting name="Alice" />);
    expect(screen.getByText("Hello Alice")).toBeDefined();
  });

  it("renders with an empty string name prop", () => {
    render(<Greeting name="" />);
    const heading = screen.getByTestId("greeting");
    expect(heading.textContent).toBe("Hello ");
  });

  it("applies centered text styling", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading.style.textAlign).toBe("center");
  });

  it("applies the correct font size", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading.style.fontSize).toBe("2.5rem");
  });

  it("applies the subtle color styling", () => {
    render(<Greeting />);
    const heading = screen.getByTestId("greeting");
    expect(heading.style.color).toBe("#334155");
  });
});
