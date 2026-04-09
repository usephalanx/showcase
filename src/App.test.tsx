import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders a Hello World heading", () => {
    render(<App />);
    const heading = screen.getByTestId("hello-heading");
    expect(heading).toBeInTheDocument();
    expect(heading.tagName).toBe("H1");
    expect(heading).toHaveTextContent("Hello World");
  });

  it("applies centered flexbox styles to the container div", () => {
    const { container } = render(<App />);
    const wrapper = container.firstElementChild as HTMLElement;
    expect(wrapper).toBeInTheDocument();
    expect(wrapper.style.display).toBe("flex");
    expect(wrapper.style.justifyContent).toBe("center");
    expect(wrapper.style.alignItems).toBe("center");
    expect(wrapper.style.height).toBe("100vh");
    expect(wrapper.style.margin).toBe("0");
  });

  it("renders exactly one h1 element", () => {
    const { container } = render(<App />);
    const headings = container.querySelectorAll("h1");
    expect(headings).toHaveLength(1);
  });

  it("exports a default function component", () => {
    expect(typeof App).toBe("function");
  });
});
