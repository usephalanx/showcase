import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CardFormModal, { Tag } from "./CardFormModal";

const mockTags: Tag[] = [
  { id: 1, name: "Bug", color: "#ef4444" },
  { id: 2, name: "Feature", color: "#3b82f6" },
  { id: 3, name: "Urgent", color: "#f59e0b" },
];

const defaultProps = {
  isOpen: true,
  onClose: vi.fn(),
  onSubmit: vi.fn(),
  availableTags: mockTags,
};

describe("CardFormModal", () => {
  it("renders nothing when isOpen is false", () => {
    const { container } = render(
      <CardFormModal {...defaultProps} isOpen={false} />
    );
    expect(container.innerHTML).toBe("");
  });

  it("renders the modal when isOpen is true", () => {
    render(<CardFormModal {...defaultProps} />);
    expect(screen.getByTestId("card-form-modal")).toBeInTheDocument();
  });

  // --- Create mode tests ---

  it('displays "Create Card" title in create mode', () => {
    render(<CardFormModal {...defaultProps} />);
    expect(screen.getByTestId("modal-title")).toHaveTextContent("Create Card");
  });

  it('displays "Create Card" on the submit button in create mode', () => {
    render(<CardFormModal {...defaultProps} />);
    expect(screen.getByTestId("submit-button")).toHaveTextContent("Create Card");
  });

  it("starts with empty fields in create mode", () => {
    render(<CardFormModal {...defaultProps} />);
    const titleInput = screen.getByTestId("card-title-input") as HTMLInputElement;
    const descInput = screen.getByTestId("card-description-input") as HTMLTextAreaElement;
    expect(titleInput.value).toBe("");
    expect(descInput.value).toBe("");
  });

  it("shows validation error when title is empty on submit", async () => {
    const onSubmit = vi.fn();
    render(<CardFormModal {...defaultProps} onSubmit={onSubmit} />);
    fireEvent.click(screen.getByTestId("submit-button"));
    expect(screen.getByTestId("title-error")).toHaveTextContent("Title is required");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits form data in create mode", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<CardFormModal {...defaultProps} onSubmit={onSubmit} />);

    await user.type(screen.getByTestId("card-title-input"), "New Card");
    await user.type(screen.getByTestId("card-description-input"), "A description");
    await user.click(screen.getByTestId("tag-badge-1"));
    await user.click(screen.getByTestId("submit-button"));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(onSubmit).toHaveBeenCalledWith({
      title: "New Card",
      description: "A description",
      tagIds: [1],
    });
  });

  // --- Edit mode tests ---

  it('displays "Edit Card" title in edit mode', () => {
    render(
      <CardFormModal
        {...defaultProps}
        initialData={{ title: "Existing", description: "Desc", tagIds: [2] }}
      />
    );
    expect(screen.getByTestId("modal-title")).toHaveTextContent("Edit Card");
  });

  it('displays "Save Changes" on the submit button in edit mode', () => {
    render(
      <CardFormModal
        {...defaultProps}
        initialData={{ title: "Existing", description: "Desc", tagIds: [] }}
      />
    );
    expect(screen.getByTestId("submit-button")).toHaveTextContent("Save Changes");
  });

  it("pre-fills fields with initialData in edit mode", () => {
    render(
      <CardFormModal
        {...defaultProps}
        initialData={{ title: "Existing Card", description: "Existing desc", tagIds: [1, 3] }}
      />
    );
    const titleInput = screen.getByTestId("card-title-input") as HTMLInputElement;
    const descInput = screen.getByTestId("card-description-input") as HTMLTextAreaElement;
    expect(titleInput.value).toBe("Existing Card");
    expect(descInput.value).toBe("Existing desc");
  });

  it("pre-selects tags from initialData", () => {
    render(
      <CardFormModal
        {...defaultProps}
        initialData={{ title: "Card", description: "", tagIds: [1, 3] }}
      />
    );
    expect(screen.getByTestId("tag-badge-1")).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByTestId("tag-badge-2")).toHaveAttribute("aria-pressed", "false");
    expect(screen.getByTestId("tag-badge-3")).toHaveAttribute("aria-pressed", "true");
  });

  it("submits updated data in edit mode", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(
      <CardFormModal
        {...defaultProps}
        onSubmit={onSubmit}
        initialData={{ title: "Old Title", description: "Old desc", tagIds: [1] }}
      />
    );

    const titleInput = screen.getByTestId("card-title-input");
    await user.clear(titleInput);
    await user.type(titleInput, "Updated Title");
    await user.click(screen.getByTestId("tag-badge-1")); // deselect tag 1
    await user.click(screen.getByTestId("tag-badge-2")); // select tag 2
    await user.click(screen.getByTestId("submit-button"));

    expect(onSubmit).toHaveBeenCalledWith({
      title: "Updated Title",
      description: "Old desc",
      tagIds: [2],
    });
  });

  // --- Tag toggle tests ---

  it("toggles tag selection on click", async () => {
    const user = userEvent.setup();
    render(<CardFormModal {...defaultProps} />);

    const tagBadge = screen.getByTestId("tag-badge-2");
    expect(tagBadge).toHaveAttribute("aria-pressed", "false");

    await user.click(tagBadge);
    expect(tagBadge).toHaveAttribute("aria-pressed", "true");

    await user.click(tagBadge);
    expect(tagBadge).toHaveAttribute("aria-pressed", "false");
  });

  // --- Close / Cancel tests ---

  it("calls onClose when close button is clicked", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(<CardFormModal {...defaultProps} onClose={onClose} />);
    await user.click(screen.getByTestId("modal-close-button"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when cancel button is clicked", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(<CardFormModal {...defaultProps} onClose={onClose} />);
    await user.click(screen.getByTestId("cancel-button"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when overlay is clicked", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(<CardFormModal {...defaultProps} onClose={onClose} />);
    await user.click(screen.getByTestId("card-form-modal-overlay"));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("does not call onClose when modal content is clicked", async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(<CardFormModal {...defaultProps} onClose={onClose} />);
    await user.click(screen.getByTestId("card-form-modal"));
    expect(onClose).not.toHaveBeenCalled();
  });

  // --- Custom modal title ---

  it("renders a custom modal title when provided", () => {
    render(
      <CardFormModal {...defaultProps} modalTitle="Add Task" />
    );
    expect(screen.getByTestId("modal-title")).toHaveTextContent("Add Task");
  });

  // --- No tags ---

  it("does not render tag section when availableTags is empty", () => {
    render(<CardFormModal {...defaultProps} availableTags={[]} />);
    expect(screen.queryByTestId("tag-selection")).not.toBeInTheDocument();
  });

  // --- Whitespace-only title ---

  it("shows validation error for whitespace-only title", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<CardFormModal {...defaultProps} onSubmit={onSubmit} />);
    await user.type(screen.getByTestId("card-title-input"), "   ");
    await user.click(screen.getByTestId("submit-button"));
    expect(screen.getByTestId("title-error")).toHaveTextContent("Title is required");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  // --- Trims whitespace ---

  it("trims title and description before submitting", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<CardFormModal {...defaultProps} onSubmit={onSubmit} />);
    await user.type(screen.getByTestId("card-title-input"), "  My Card  ");
    await user.type(screen.getByTestId("card-description-input"), "  Some desc  ");
    await user.click(screen.getByTestId("submit-button"));
    expect(onSubmit).toHaveBeenCalledWith({
      title: "My Card",
      description: "Some desc",
      tagIds: [],
    });
  });

  // --- ARIA attributes ---

  it("has correct ARIA attributes on the dialog", () => {
    render(<CardFormModal {...defaultProps} />);
    const overlay = screen.getByTestId("card-form-modal-overlay");
    expect(overlay).toHaveAttribute("role", "dialog");
    expect(overlay).toHaveAttribute("aria-modal", "true");
  });
});
