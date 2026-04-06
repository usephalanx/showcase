import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Modal from "./Modal";

describe("Modal", () => {
  const defaultProps = {
    isOpen: true,
    onClose: vi.fn(),
    title: "Test Modal Title",
    children: <p>Modal body content</p>,
  };

  it("renders without crashing when open", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-panel")).toBeTruthy();
  });

  it("displays the provided title", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-title")).toHaveTextContent(
      "Test Modal Title"
    );
  });

  it("renders children in the body", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-body")).toHaveTextContent(
      "Modal body content"
    );
  });

  it("does not render content when isOpen is false", () => {
    render(<Modal {...defaultProps} isOpen={false} />);
    expect(screen.queryByTestId("modal-panel")).toBeNull();
  });

  it("calls onClose when the close button is clicked", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId("modal-close-button"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("close button has accessible label", () => {
    render(<Modal {...defaultProps} />);
    const btn = screen.getByTestId("modal-close-button");
    expect(btn).toHaveAttribute("aria-label", "Close");
  });

  it("applies sm size class", () => {
    render(<Modal {...defaultProps} size="sm" />);
    const panel = screen.getByTestId("modal-panel");
    expect(panel.className).toContain("sm:max-w-sm");
  });

  it("applies md size class by default", () => {
    render(<Modal {...defaultProps} />);
    const panel = screen.getByTestId("modal-panel");
    expect(panel.className).toContain("sm:max-w-md");
  });

  it("applies lg size class", () => {
    render(<Modal {...defaultProps} size="lg" />);
    const panel = screen.getByTestId("modal-panel");
    expect(panel.className).toContain("sm:max-w-lg");
  });

  it("renders the dialog with role=dialog", () => {
    render(<Modal {...defaultProps} />);
    const dialog = screen.getByRole("dialog");
    expect(dialog).toBeTruthy();
  });

  it("renders a backdrop element", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-backdrop")).toBeTruthy();
  });

  it("renders different children correctly", () => {
    render(
      <Modal {...defaultProps}>
        <span data-testid="custom-child">Custom content</span>
      </Modal>
    );
    expect(screen.getByTestId("custom-child")).toHaveTextContent(
      "Custom content"
    );
  });

  it("renders with a different title", () => {
    render(<Modal {...defaultProps} title="Another Title" />);
    expect(screen.getByTestId("modal-title")).toHaveTextContent("Another Title");
  });
});
