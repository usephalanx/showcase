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

  it("renders without crashing when isOpen is true", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-overlay")).toBeTruthy();
    expect(screen.getByTestId("modal-panel")).toBeTruthy();
  });

  it("renders nothing when isOpen is false", () => {
    render(<Modal {...defaultProps} isOpen={false} />);
    expect(screen.queryByTestId("modal-overlay")).toBeNull();
    expect(screen.queryByTestId("modal-panel")).toBeNull();
  });

  it("displays the provided title", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-title").textContent).toBe(
      "Test Modal Title",
    );
  });

  it("renders children inside the modal body", () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByTestId("modal-body").textContent).toBe(
      "Modal body content",
    );
  });

  it("calls onClose when the close button is clicked", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId("modal-close-button"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when the overlay is clicked", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId("modal-overlay"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("does NOT call onClose when the panel itself is clicked", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId("modal-panel"));
    expect(onClose).not.toHaveBeenCalled();
  });

  it("calls onClose when the Escape key is pressed", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.keyDown(document, { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("does NOT call onClose for non-Escape key presses", () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.keyDown(document, { key: "Enter" });
    fireEvent.keyDown(document, { key: "Tab" });
    expect(onClose).not.toHaveBeenCalled();
  });

  it("cleans up the keydown listener when closed", () => {
    const onClose = vi.fn();
    const { rerender } = render(<Modal {...defaultProps} onClose={onClose} />);
    // Close the modal
    rerender(
      <Modal {...defaultProps} isOpen={false} onClose={onClose} />,
    );
    fireEvent.keyDown(document, { key: "Escape" });
    expect(onClose).not.toHaveBeenCalled();
  });

  it("has role=dialog and aria-modal=true for accessibility", () => {
    render(<Modal {...defaultProps} />);
    const panel = screen.getByTestId("modal-panel");
    expect(panel.getAttribute("role")).toBe("dialog");
    expect(panel.getAttribute("aria-modal")).toBe("true");
  });

  it("sets aria-label on the dialog to the title prop", () => {
    render(<Modal {...defaultProps} title="Accessible Title" />);
    const panel = screen.getByTestId("modal-panel");
    expect(panel.getAttribute("aria-label")).toBe("Accessible Title");
  });

  it("close button has accessible aria-label", () => {
    render(<Modal {...defaultProps} />);
    const btn = screen.getByTestId("modal-close-button");
    expect(btn.getAttribute("aria-label")).toBe("Close modal");
  });
});
