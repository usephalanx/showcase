import React, { useState, useEffect, useCallback } from "react";

/**
 * Data shape for board form fields.
 */
export interface BoardFormData {
  title: string;
  description: string;
  meta_title: string;
  meta_description: string;
}

/**
 * Props for the BoardFormModal component.
 */
export interface BoardFormModalProps {
  /** Whether the modal is currently visible. */
  isOpen: boolean;
  /** Callback invoked to close the modal. */
  onClose: () => void;
  /** Callback invoked with form data on successful submission. */
  onSubmit: (data: BoardFormData) => void;
  /** Optional initial data to pre-populate the form (edit mode). */
  initialData?: Partial<BoardFormData>;
}

const EMPTY_FORM: BoardFormData = {
  title: "",
  description: "",
  meta_title: "",
  meta_description: "",
};

const META_TITLE_MAX = 70;
const META_DESCRIPTION_MAX = 160;

/**
 * A modal form for creating or editing a Kanban board.
 *
 * Includes fields for title, description, and SEO metadata
 * (meta_title, meta_description) with character-count indicators.
 */
export default function BoardFormModal({
  isOpen,
  onClose,
  onSubmit,
  initialData,
}: BoardFormModalProps): React.ReactElement | null {
  const [formData, setFormData] = useState<BoardFormData>(EMPTY_FORM);
  const [errors, setErrors] = useState<Partial<Record<keyof BoardFormData, string>>>({});

  const isEditMode = Boolean(initialData && initialData.title !== undefined);

  useEffect(() => {
    if (isOpen) {
      setFormData({
        title: initialData?.title ?? "",
        description: initialData?.description ?? "",
        meta_title: initialData?.meta_title ?? "",
        meta_description: initialData?.meta_description ?? "",
      });
      setErrors({});
    }
  }, [isOpen, initialData]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    },
    []
  );

  const validate = useCallback((): boolean => {
    const newErrors: Partial<Record<keyof BoardFormData, string>> = {};

    if (!formData.title.trim()) {
      newErrors.title = "Title is required";
    }

    if (formData.meta_title.length > META_TITLE_MAX) {
      newErrors.meta_title = `Meta title must be ${META_TITLE_MAX} characters or fewer`;
    }

    if (formData.meta_description.length > META_DESCRIPTION_MAX) {
      newErrors.meta_description = `Meta description must be ${META_DESCRIPTION_MAX} characters or fewer`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (validate()) {
        onSubmit({
          title: formData.title.trim(),
          description: formData.description.trim(),
          meta_title: formData.meta_title.trim(),
          meta_description: formData.meta_description.trim(),
        });
      }
    },
    [formData, validate, onSubmit]
  );

  const handleOverlayClick = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (e.target === e.currentTarget) {
        onClose();
      }
    },
    [onClose]
  );

  if (!isOpen) return null;

  return (
    <div
      className="board-form-modal-overlay"
      data-testid="board-form-modal-overlay"
      onClick={handleOverlayClick}
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div
        className="board-form-modal"
        data-testid="board-form-modal"
        role="dialog"
        aria-modal="true"
        aria-label={isEditMode ? "Edit Board" : "Create Board"}
        style={{
          backgroundColor: "#fff",
          borderRadius: "8px",
          padding: "24px",
          width: "100%",
          maxWidth: "520px",
          maxHeight: "90vh",
          overflowY: "auto",
        }}
      >
        <h2 data-testid="board-form-modal-title" style={{ margin: "0 0 16px" }}>
          {isEditMode ? "Edit Board" : "Create Board"}
        </h2>

        <form onSubmit={handleSubmit} data-testid="board-form">
          {/* Title */}
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="board-title" style={{ display: "block", fontWeight: 600, marginBottom: "4px" }}>
              Title <span aria-hidden="true">*</span>
            </label>
            <input
              id="board-title"
              name="title"
              type="text"
              data-testid="input-title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter board title"
              aria-required="true"
              aria-invalid={!!errors.title}
              style={{ width: "100%", padding: "8px", boxSizing: "border-box" }}
            />
            {errors.title && (
              <span data-testid="error-title" role="alert" style={{ color: "red", fontSize: "0.85em" }}>
                {errors.title}
              </span>
            )}
          </div>

          {/* Description */}
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="board-description" style={{ display: "block", fontWeight: 600, marginBottom: "4px" }}>
              Description
            </label>
            <textarea
              id="board-description"
              name="description"
              data-testid="input-description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter board description"
              rows={3}
              style={{ width: "100%", padding: "8px", boxSizing: "border-box", resize: "vertical" }}
            />
          </div>

          {/* Meta Title (SEO) */}
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="board-meta-title" style={{ display: "block", fontWeight: 600, marginBottom: "4px" }}>
              Meta Title (SEO)
            </label>
            <input
              id="board-meta-title"
              name="meta_title"
              type="text"
              data-testid="input-meta-title"
              value={formData.meta_title}
              onChange={handleChange}
              placeholder="SEO title (max 70 characters)"
              style={{ width: "100%", padding: "8px", boxSizing: "border-box" }}
            />
            <span data-testid="meta-title-count" style={{ fontSize: "0.8em", color: formData.meta_title.length > META_TITLE_MAX ? "red" : "#666" }}>
              {formData.meta_title.length}/{META_TITLE_MAX}
            </span>
            {errors.meta_title && (
              <span data-testid="error-meta-title" role="alert" style={{ color: "red", fontSize: "0.85em", display: "block" }}>
                {errors.meta_title}
              </span>
            )}
          </div>

          {/* Meta Description (SEO) */}
          <div style={{ marginBottom: "16px" }}>
            <label htmlFor="board-meta-description" style={{ display: "block", fontWeight: 600, marginBottom: "4px" }}>
              Meta Description (SEO)
            </label>
            <textarea
              id="board-meta-description"
              name="meta_description"
              data-testid="input-meta-description"
              value={formData.meta_description}
              onChange={handleChange}
              placeholder="SEO description (max 160 characters)"
              rows={2}
              style={{ width: "100%", padding: "8px", boxSizing: "border-box", resize: "vertical" }}
            />
            <span data-testid="meta-description-count" style={{ fontSize: "0.8em", color: formData.meta_description.length > META_DESCRIPTION_MAX ? "red" : "#666" }}>
              {formData.meta_description.length}/{META_DESCRIPTION_MAX}
            </span>
            {errors.meta_description && (
              <span data-testid="error-meta-description" role="alert" style={{ color: "red", fontSize: "0.85em", display: "block" }}>
                {errors.meta_description}
              </span>
            )}
          </div>

          {/* Actions */}
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px" }}>
            <button
              type="button"
              data-testid="btn-cancel"
              onClick={onClose}
              style={{ padding: "8px 16px", cursor: "pointer" }}
            >
              Cancel
            </button>
            <button
              type="submit"
              data-testid="btn-submit"
              style={{ padding: "8px 16px", cursor: "pointer", fontWeight: 600 }}
            >
              {isEditMode ? "Save Changes" : "Create Board"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
