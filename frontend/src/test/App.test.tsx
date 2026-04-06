import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App";

describe("App", () => {
  it("renders the application header with title", () => {
    render(<App />);
    const heading = screen.getByRole("heading", { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent("Todo App");
  });

  it("renders the subtitle", () => {
    render(<App />);
    expect(
      screen.getByText("Organize your tasks, get things done."),
    ).toBeInTheDocument();
  });

  it("renders the welcome message", () => {
    render(<App />);
    expect(
      screen.getByText("Welcome! Your task list will appear here."),
    ).toBeInTheDocument();
  });

  it("renders a header element", () => {
    render(<App />);
    const header = screen.getByRole("banner");
    expect(header).toBeInTheDocument();
  });

  it("renders a main content area", () => {
    render(<App />);
    const main = screen.getByRole("main");
    expect(main).toBeInTheDocument();
  });

  it("renders a footer with copyright", () => {
    render(<App />);
    const year = new Date().getFullYear().toString();
    expect(
      screen.getByText(new RegExp(`© ${year} Todo App`)),
    ).toBeInTheDocument();
  });

  it("applies the app class to the root wrapper", () => {
    const { container } = render(<App />);
    const appDiv = container.firstChild as HTMLElement;
    expect(appDiv).toHaveClass("app");
  });

  it("contains a card section inside main", () => {
    const { container } = render(<App />);
    const card = container.querySelector(".card");
    expect(card).toBeInTheDocument();
  });
});
