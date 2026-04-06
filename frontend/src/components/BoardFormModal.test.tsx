import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import BoardFormModal, { BoardFormModalProps, BoardFormData } from "./BoardFormModal";

const defaultProps: BoardFormModalProps = {
  isOpen: true,
  onClose: vi.fn(),
  onSubmit: vi.fn(),
};

function renderModal(overrides: Partial<BoardFormModalProps> = {}) {
  const props = { ...defaultProps, ...overrides };
  return render(<BoardFormModal {...props} />);
}

describe("BoardFormModal", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders nothing when isOpen is false", () => {
    renderModal({ isOpen: false });
    expect(screen.queryByTestId("board-form-modal")).not.toBeInTheDocument();
  });

  it("renders the modal when isOpen is true", () => {
    renderModal();
    expect(screen.getByTestId("board-form-modal")).toBeInTheDocument();
  });

  it("displays 'Create Board' title when no initialData is provided", () => {
    renderModal();
    expect(screen.getByTestId("board-form-modal-title")).toHaveTextContent("Create Board");
    expect(screen.getByTestId("btn-submit")).toHaveTextContent("Create Board");
  });

  it("displays 'Edit Board' title when initialData is provided", () => {
    renderModal({
      initialData: {
        title: "Existing Board",
        description: "A description",
        meta_title: "SEO Title",
        meta_description: "SEO Desc",
      },
    });
    expect(screen.getByTestId("board-form-modal-title")).toHaveTextContent("Edit Board");
    expect(screen.getByTestId("btn-submit")).toHaveTextContent("Save Changes");
  });

  it("pre-populates fields with initialData", () => {
    renderModal({
      initialData: {
        title: "My Board",
        description: "Desc here",
        meta_title: "SEO",
        meta_description: "SEO desc",
      },
    });

    expect(screen.getByTestId("input-title")).toHaveValue("My Board");
    expect(screen.getByTestId("input-description")).toHaveValue("Desc here");
    expect(screen.getByTestId("input-meta-title")).toHaveValue("SEO");
    expect(screen.getByTestId("input-meta-description")).toHaveValue("SEO desc");
  });

  it("renders all form fields", () => {
    renderModal();
    expect(screen.getByTestId("input-title")).toBeInTheDocument();
    expect(screen.getByTestId("input-description")).toBeInTheDocument();
    expect(screen.getByTestId("input-meta-title")).toBeInTheDocument();
    expect(screen.getByTestId("input-meta-description")).toBeInTheDocument();
  });

  it("shows validation error when title is empty on submit", async () => {
    const onSubmit = vi.fn();
    renderModal({ onSubmit });

    fireEvent.click(screen.getByTestId("btn-submit"));

    expect(await screen.findByTestId("error-title")).toHaveTextContent("Title is required");
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("calls onSubmit with trimmed form data when valid", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    renderModal({ onSubmit });

    await user.type(screen.getByTestId("input-title"), "  New Board  ");
    await user.type(screen.getByTestId("input-description"), "  A description  ");
    await user.type(screen.getByTestId("input-meta-title"), "  Meta  ");
    await user.type(screen.getByTestId("input-meta-description"), "  Meta Desc  ");

    fireEvent.click(screen.getByTestId("btn-submit"));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    const submitted: BoardFormData = onSubmit.mock.calls[0][0];
    expect(submitted.title).toBe("New Board");
    expect(submitted.description).toBe("A description");
    expect(submitted.meta_title).toBe("Meta");
    expect(submitted.meta_description).toBe("Meta Desc");
  });

  it("calls onClose when cancel button is clicked", () => {
    const onClose = vi.fn();
    renderModal({ onClose });

    fireEvent.click(screen.getByTestId("btn-cancel"));

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onClose when overlay is clicked", () => {
    const onClose = vi.fn();
    renderModal({ onClose });

    fireEvent.click(screen.getByTestId("board-form-modal-overlay"));

    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it("does NOT call onClose when clicking inside the modal content", () => {
    const onClose = vi.fn();
    renderModal({ onClose });

    fireEvent.click(screen.getByTestId("board-form-modal"));

    expect(onClose).not.toHaveBeenCalled();
  });

  it("displays character count for meta_title", async () => {
    const user = userEvent.setup();
    renderModal();

    expect(screen.getByTestId("meta-title-count")).toHaveTextContent("0/70");

    await user.type(screen.getByTestId("input-meta-title"), "Hello");

    expect(screen.getByTestId("meta-title-count")).toHaveTextContent("5/70");
  });

  it("displays character count for meta_description", async () => {
    const user = userEvent.setup();
    renderModal();

    expect(screen.getByTestId("meta-description-count")).toHaveTextContent("0/160");

    await user.type(screen.getByTestId("input-meta-description"), "Test");

    expect(screen.getByTestId("meta-description-count")).toHaveTextContent("4/160");
  });

  it("shows error when meta_title exceeds 70 characters", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    renderModal({ onSubmit });

    await user.type(screen.getByTestId("input-title"), "Valid Title");
    const longMeta = "a".repeat(71);
    await user.type(screen.getByTestId("input-meta-title"), longMeta);

    fireEvent.click(screen.getByTestId("btn-submit"));

    expect(await screen.findByTestId("error-meta-title")).toHaveTextContent(
      "Meta title must be 70 characters or fewer"
    );
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("shows error when meta_description exceeds 160 characters", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    renderModal({ onSubmit });

    await user.type(screen.getByTestId("input-title"), "Valid Title");
    const longDesc = "b".repeat(161);
    await user.type(screen.getByTestId("input-meta-description"), longDesc);

    fireEvent.click(screen.getByTestId("btn-submit"));

    expect(await screen.findByTestId("error-meta-description")).toHaveTextContent(
      "Meta description must be 160 characters or fewer"
    );
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("clears validation errors when user types in a field", async () => {
    const user = userEvent.setup();
    renderModal();

    // Trigger title error
    fireEvent.click(screen.getByTestId("btn-submit"));
    expect(await screen.findByTestId("error-title")).toBeInTheDocument();

    // Type in the title field to clear the error
    await user.type(screen.getByTestId("input-title"), "A");
    expect(screen.queryByTestId("error-title")).not.toBeInTheDocument();
  });

  it("has correct aria attributes on the dialog", () => {
    renderModal();
    const dialog = screen.getByTestId("board-form-modal");
    expect(dialog).toHaveAttribute("role", "dialog");
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(dialog).toHaveAttribute("aria-label", "Create Board");
  });

  it("has aria-label 'Edit Board' in edit mode", () => {
    renderModal({ initialData: { title: "Existing" } });
    const dialog = screen.getByTestId("board-form-modal");
    expect(dialog).toHaveAttribute("aria-label", "Edit Board");
  });

  it("marks the title input as aria-required", () => {
    renderModal();
    expect(screen.getByTestId("input-title")).toHaveAttribute("aria-required", "true");
  });

  it("resets form data when modal reopens", () => {
    const { rerender } = render(
      <BoardFormModal isOpen={true} onClose={vi.fn()} onSubmit={vi.fn()} />
    );

    // Type something
    fireEvent.change(screen.getByTestId("input-title"), { target: { value: "Typed" } });
    expect(screen.getByTestId("input-title")).toHaveValue("Typed");

    // Close
    rerender(
      <BoardFormModal isOpen={false} onClose={vi.fn()} onSubmit={vi.fn()} />
    );

    // Reopen — fields should be empty again
    rerender(
      <BoardFormModal isOpen={true} onClose={vi.fn()} onSubmit={vi.fn()} />
    );
    expect(screen.getByTestId("input-title")).toHaveValue("");
  });
});
