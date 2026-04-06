import React, { useState, useEffect, useCallback } from "react";

export interface Tag {
  id: number;
  name: string;
  color: string;
}

export interface CardFormData {
  title: string;
  description: string;
  tagIds: number[];
}

export interface CardFormModalProps {
  /** Whether the modal is visible */
  isOpen: boolean;
  /** Callback to close the modal */
  onClose: () => void;
  /** Callback when the form is submitted with valid data */
  onSubmit: (data: CardFormData) => void;
  /** Pre-populated data for edit mode; omit for create mode */
  initialData?: Partial<CardFormData>;
  /** Available tags to choose from */
  availableTags?: Tag[];
  /** Modal title override; defaults to "Create Card" or "Edit Card" */
  modalTitle?: string;
}

const CardFormModal: React.FC<CardFormModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  availableTags = [],
  modalTitle,
}) => {
  const isEditMode = Boolean(initialData);
  const resolvedTitle = modalTitle ?? (isEditMode ? "Edit Card" : "Create Card");

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);
  const [errors, setErrors] = useState<{ title?: string }>({});

  useEffect(() => {
    if (isOpen) {
      setTitle(initialData?.title ?? "");
      setDescription(initialData?.description ?? "");
      setSelectedTagIds(initialData?.tagIds ?? []);
      setErrors({});
    }
  }, [isOpen, initialData]);

  const toggleTag = useCallback((tagId: number) => {
    setSelectedTagIds((prev) =>
      prev.includes(tagId) ? prev.filter((id) => id !== tagId) : [...prev, tagId]
    );
  }, []);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      const trimmedTitle = title.trim();
      if (!trimmedTitle) {
        setErrors({ title: "Title is required" });
        return;
      }
      setErrors({});
      onSubmit({
        title: trimmedTitle,
        description: description.trim(),
        tagIds: selectedTagIds,
      });
    },
    [title, description, selectedTagIds, onSubmit]
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
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      data-testid="card-form-modal-overlay"
      onClick={handleOverlayClick}
      role="dialog"
      aria-modal="true"
      aria-label={resolvedTitle}
    >
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl" data-testid="card-form-modal">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900" data-testid="modal-title">
            {resolvedTitle}
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            aria-label="Close modal"
            data-testid="modal-close-button"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} data-testid="card-form">
          <div className="mb-4">
            <label htmlFor="card-title" className="mb-1 block text-sm font-medium text-gray-700">
              Title
            </label>
            <input
              id="card-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className={`w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 ${
                errors.title ? "border-red-500 focus:ring-red-300" : "border-gray-300 focus:ring-blue-300"
              }`}
              placeholder="Enter card title"
              data-testid="card-title-input"
            />
            {errors.title && (
              <p className="mt-1 text-xs text-red-600" data-testid="title-error">
                {errors.title}
              </p>
            )}
          </div>

          <div className="mb-4">
            <label htmlFor="card-description" className="mb-1 block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="card-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
              placeholder="Enter card description"
              rows={3}
              data-testid="card-description-input"
            />
          </div>

          {availableTags.length > 0 && (
            <div className="mb-4">
              <span className="mb-2 block text-sm font-medium text-gray-700">Tags</span>
              <div className="flex flex-wrap gap-2" data-testid="tag-selection">
                {availableTags.map((tag) => {
                  const isSelected = selectedTagIds.includes(tag.id);
                  return (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => toggleTag(tag.id)}
                      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium transition-all ${
                        isSelected
                          ? "ring-2 ring-offset-1"
                          : "opacity-60 hover:opacity-100"
                      }`}
                      style={{
                        backgroundColor: tag.color + "20",
                        color: tag.color,
                        borderColor: tag.color,
                        ...(isSelected ? { ringColor: tag.color } : {}),
                      }}
                      data-testid={`tag-badge-${tag.id}`}
                      aria-pressed={isSelected}
                    >
                      {tag.name}
                      {isSelected && <span className="ml-1">✓</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
              data-testid="cancel-button"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
              data-testid="submit-button"
            >
              {isEditMode ? "Save Changes" : "Create Card"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CardFormModal;
