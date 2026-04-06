import React, { useState, useEffect, useCallback } from 'react';
import Button from './Button';
import Input from './Input';
import Badge from './Badge';

export interface CategoryOption {
  id: number;
  name: string;
  slug: string;
  color?: string;
}

export interface CardFormValues {
  title: string;
  description: string;
  categoryIds: number[];
}

export interface CardFormProps {
  /** Pre-filled values for editing; omit for create mode */
  initialValues?: Partial<CardFormValues>;
  /** Available categories to choose from */
  categories: CategoryOption[];
  /** Called with form values on submit */
  onSubmit: (values: CardFormValues) => void;
  /** Called when the user cancels */
  onCancel: () => void;
  /** Label for the submit button (defaults to "Save") */
  submitLabel?: string;
  /** Whether the form is in a loading/submitting state */
  isSubmitting?: boolean;
}

const CardForm: React.FC<CardFormProps> = ({
  initialValues,
  categories,
  onSubmit,
  onCancel,
  submitLabel = 'Save',
  isSubmitting = false,
}) => {
  const [title, setTitle] = useState(initialValues?.title ?? '');
  const [description, setDescription] = useState(initialValues?.description ?? '');
  const [selectedCategoryIds, setSelectedCategoryIds] = useState<number[]>(
    initialValues?.categoryIds ?? [],
  );
  const [errors, setErrors] = useState<{ title?: string }>({});

  useEffect(() => {
    setTitle(initialValues?.title ?? '');
    setDescription(initialValues?.description ?? '');
    setSelectedCategoryIds(initialValues?.categoryIds ?? []);
    setErrors({});
  }, [initialValues]);

  const toggleCategory = useCallback((categoryId: number) => {
    setSelectedCategoryIds((prev) =>
      prev.includes(categoryId)
        ? prev.filter((id) => id !== categoryId)
        : [...prev, categoryId],
    );
  }, []);

  const validate = (): boolean => {
    const newErrors: { title?: string } = {};
    if (!title.trim()) {
      newErrors.title = 'Title is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    onSubmit({
      title: title.trim(),
      description: description.trim(),
      categoryIds: selectedCategoryIds,
    });
  };

  return (
    <form onSubmit={handleSubmit} data-testid="card-form" noValidate>
      <div style={{ marginBottom: '16px' }}>
        <label htmlFor="card-title" style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}>
          Title
        </label>
        <Input
          id="card-title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter card title"
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? 'card-title-error' : undefined}
        />
        {errors.title && (
          <span id="card-title-error" role="alert" style={{ color: '#ef4444', fontSize: '0.875rem' }}>
            {errors.title}
          </span>
        )}
      </div>

      <div style={{ marginBottom: '16px' }}>
        <label htmlFor="card-description" style={{ display: 'block', marginBottom: '4px', fontWeight: 600 }}>
          Description
        </label>
        <textarea
          id="card-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter card description"
          rows={4}
          style={{
            width: '100%',
            padding: '8px 12px',
            borderRadius: '6px',
            border: '1px solid #d1d5db',
            fontSize: '0.875rem',
            fontFamily: 'inherit',
            resize: 'vertical',
            boxSizing: 'border-box',
          }}
          data-testid="card-description"
        />
      </div>

      <div style={{ marginBottom: '16px' }}>
        <span style={{ display: 'block', marginBottom: '8px', fontWeight: 600 }}>
          Categories
        </span>
        {categories.length === 0 && (
          <span data-testid="no-categories" style={{ color: '#9ca3af', fontSize: '0.875rem' }}>
            No categories available
          </span>
        )}
        <div
          style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}
          role="group"
          aria-label="Category selection"
        >
          {categories.map((category) => {
            const isSelected = selectedCategoryIds.includes(category.id);
            return (
              <button
                key={category.id}
                type="button"
                onClick={() => toggleCategory(category.id)}
                data-testid={`category-toggle-${category.id}`}
                aria-pressed={isSelected}
                style={{
                  cursor: 'pointer',
                  background: 'none',
                  border: 'none',
                  padding: 0,
                  opacity: isSelected ? 1 : 0.5,
                  transition: 'opacity 150ms',
                }}
              >
                <Badge color={category.color}>{category.name}</Badge>
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', paddingTop: '8px' }}>
        <Button type="button" onClick={onCancel} data-testid="card-form-cancel">
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting} data-testid="card-form-submit">
          {isSubmitting ? 'Saving…' : submitLabel}
        </Button>
      </div>
    </form>
  );
};

export default CardForm;
