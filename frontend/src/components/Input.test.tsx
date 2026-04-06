import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Input from "./Input";

describe("Input", () => {
  it("renders without crashing with no props", () => {
    const { container } = render(<Input />);
    const input = container.querySelector("input");
    expect(input).toBeTruthy();
  });

  it("renders label text when provided", () => {
    render(<Input label="Email Address" />);
    expect(screen.getByText("Email Address")).toBeTruthy();
  });

  it("associates label with input via htmlFor", () => {
    render(<Input label="Username" id="username-field" />);
    const label = screen.getByText("Username");
    expect(label.getAttribute("for")).toBe("username-field");
    const input = screen.getByRole("textbox");
    expect(input.getAttribute("id")).toBe("username-field");
  });

  it("renders placeholder text", () => {
    render(<Input placeholder="Enter your name" />);
    expect(screen.getByPlaceholderText("Enter your name")).toBeTruthy();
  });

  it("displays required asterisk when required is true", () => {
    render(<Input label="Name" required />);
    expect(screen.getByText("*")).toBeTruthy();
  });

  it("does not display asterisk when required is false", () => {
    render(<Input label="Name" />);
    expect(screen.queryByText("*")).toBeNull();
  });

  it("renders helper text when provided and no error", () => {
    render(<Input helperText="Must be at least 3 characters" />);
    expect(screen.getByText("Must be at least 3 characters")).toBeTruthy();
  });

  it("renders error message and hides helper text when error is set", () => {
    render(
      <Input
        error="This field is required"
        helperText="Optional helper"
      />
    );
    expect(screen.getByText("This field is required")).toBeTruthy();
    expect(screen.queryByText("Optional helper")).toBeNull();
  });

  it("applies role=alert to error message", () => {
    render(<Input error="Invalid input" />);
    const errorEl = screen.getByRole("alert");
    expect(errorEl.textContent).toBe("Invalid input");
  });

  it("sets aria-invalid when error is present", () => {
    render(<Input error="Bad value" />);
    const input = screen.getByRole("textbox");
    expect(input.getAttribute("aria-invalid")).toBe("true");
  });

  it("sets aria-invalid to false when no error", () => {
    render(<Input />);
    const input = screen.getByRole("textbox");
    expect(input.getAttribute("aria-invalid")).toBe("false");
  });

  it("calls onChange with the new value on user input", () => {
    const handleChange = vi.fn();
    render(<Input onChange={handleChange} />);
    const input = screen.getByRole("textbox");
    fireEvent.change(input, { target: { value: "hello" } });
    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("hello");
  });

  it("renders as disabled when disabled prop is true", () => {
    render(<Input disabled />);
    const input = screen.getByRole("textbox") as HTMLInputElement;
    expect(input.disabled).toBe(true);
  });

  it("renders controlled value", () => {
    render(<Input value="controlled" onChange={() => {}} />);
    const input = screen.getByRole("textbox") as HTMLInputElement;
    expect(input.value).toBe("controlled");
  });

  it("does not render bottom text when neither error nor helperText", () => {
    const { container } = render(<Input />);
    const description = container.querySelector("p");
    expect(description).toBeNull();
  });
});
