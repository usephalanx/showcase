import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TextArea from "./TextArea";

describe("TextArea", () => {
  it("renders without crashing with no props", () => {
    const { container } = render(<TextArea />);
    const textarea = container.querySelector("textarea");
    expect(textarea).toBeTruthy();
  });

  it("renders label text when provided", () => {
    render(<TextArea label="Description" />);
    expect(screen.getByText("Description")).toBeTruthy();
  });

  it("associates label with textarea via htmlFor", () => {
    render(<TextArea label="Bio" id="bio-field" />);
    const label = screen.getByText("Bio");
    expect(label.getAttribute("for")).toBe("bio-field");
    const textarea = screen.getByRole("textbox");
    expect(textarea.getAttribute("id")).toBe("bio-field");
  });

  it("renders placeholder text", () => {
    render(<TextArea placeholder="Tell us about yourself" />);
    expect(screen.getByPlaceholderText("Tell us about yourself")).toBeTruthy();
  });

  it("displays required asterisk when required is true", () => {
    render(<TextArea label="Notes" required />);
    expect(screen.getByText("*")).toBeTruthy();
  });

  it("does not display asterisk when required is false", () => {
    render(<TextArea label="Notes" />);
    expect(screen.queryByText("*")).toBeNull();
  });

  it("renders helper text when provided and no error", () => {
    render(<TextArea helperText="Max 500 characters" />);
    expect(screen.getByText("Max 500 characters")).toBeTruthy();
  });

  it("renders error message and hides helper text when error is set", () => {
    render(
      <TextArea
        error="Description is required"
        helperText="Some helper"
      />
    );
    expect(screen.getByText("Description is required")).toBeTruthy();
    expect(screen.queryByText("Some helper")).toBeNull();
  });

  it("applies role=alert to error message", () => {
    render(<TextArea error="Too short" />);
    const errorEl = screen.getByRole("alert");
    expect(errorEl.textContent).toBe("Too short");
  });

  it("sets aria-invalid when error is present", () => {
    render(<TextArea error="Error here" />);
    const textarea = screen.getByRole("textbox");
    expect(textarea.getAttribute("aria-invalid")).toBe("true");
  });

  it("sets aria-invalid to false when no error", () => {
    render(<TextArea />);
    const textarea = screen.getByRole("textbox");
    expect(textarea.getAttribute("aria-invalid")).toBe("false");
  });

  it("calls onChange with the new value on user input", () => {
    const handleChange = vi.fn();
    render(<TextArea onChange={handleChange} />);
    const textarea = screen.getByRole("textbox");
    fireEvent.change(textarea, { target: { value: "new text" } });
    expect(handleChange).toHaveBeenCalledTimes(1);
    expect(handleChange).toHaveBeenCalledWith("new text");
  });

  it("renders as disabled when disabled prop is true", () => {
    render(<TextArea disabled />);
    const textarea = screen.getByRole("textbox") as HTMLTextAreaElement;
    expect(textarea.disabled).toBe(true);
  });

  it("renders controlled value", () => {
    render(<TextArea value="controlled text" onChange={() => {}} />);
    const textarea = screen.getByRole("textbox") as HTMLTextAreaElement;
    expect(textarea.value).toBe("controlled text");
  });

  it("defaults to 4 rows", () => {
    const { container } = render(<TextArea />);
    const textarea = container.querySelector("textarea");
    expect(textarea?.getAttribute("rows")).toBe("4");
  });

  it("uses custom rows prop", () => {
    const { container } = render(<TextArea rows={8} />);
    const textarea = container.querySelector("textarea");
    expect(textarea?.getAttribute("rows")).toBe("8");
  });

  it("does not render bottom text when neither error nor helperText", () => {
    const { container } = render(<TextArea />);
    const description = container.querySelector("p");
    expect(description).toBeNull();
  });
});
