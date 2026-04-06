import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CardForm, { CategoryOption, CardFormValues } from './CardForm';

// Minimal stub components in case the real ones are not available in test env
vi.mock('./Button', () => ({
  default: ({ children, ...props }: React.PropsWithChildren<React.ButtonHTMLAttributes<HTMLButtonElement>>) => (
    <button {...props}>{children}</button>
  ),
}));

vi.mock('./Input', () => ({
  default: (props: React.InputHTMLAttributes<HTMLInputElement>) => <input {...props} />,
}));

vi.mock('./Badge', () => ({
  default: ({ children }: React.PropsWithChildren<{ color?: string }>) => (
    <span data-testid="badge">{children}</span>
  ),
}));

const defaultCategories: CategoryOption[] = [
  { id: 1, name: 'Bug', slug: 'bug', color: '#ef4444' },
  { id: 2, name: 'Feature', slug: 'feature', color: '#3b82f6' },
  { id: 3, name: 'Chore', slug: 'chore', color: '#22c55e' },
];

const renderForm = (overrides: Partial<React.ComponentProps<typeof CardForm>> = {}) => {
  const onSubmit = vi.fn();
  const onCancel = vi.fn();
  const utils = render(
    <CardForm
      categories={defaultCategories}
      onSubmit={onSubmit}
      onCancel={onCancel}
      {...overrides}
    />,
  );
  return { ...utils, onSubmit, onCancel };
};

describe('CardForm', () => {
  it('renders without crashing', () => {
    renderForm();
    expect(screen.getByTestId('card-form')).toBeInTheDocument();
  });

  it('renders title and description fields', () => {
    renderForm();
    expect(screen.getByLabelText('Title')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
  });

  it('renders all provided categories', () => {
    renderForm();
    expect(screen.getByText('Bug')).toBeInTheDocument();
    expect(screen.getByText('Feature')).toBeInTheDocument();
    expect(screen.getByText('Chore')).toBeInTheDocument();
  });

  it('shows empty state when no categories provided', () => {
    renderForm({ categories: [] });
    expect(screen.getByTestId('no-categories')).toBeInTheDocument();
  });

  it('populates fields from initialValues', () => {
    renderForm({
      initialValues: {
        title: 'Existing Card',
        description: 'Some description',
        categoryIds: [2],
      },
    });
    expect(screen.getByLabelText('Title')).toHaveValue('Existing Card');
    expect(screen.getByLabelText('Description')).toHaveValue('Some description');
    expect(screen.getByTestId('category-toggle-2')).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByTestId('category-toggle-1')).toHaveAttribute('aria-pressed', 'false');
  });

  it('validates that title is required', async () => {
    const { onSubmit } = renderForm();
    fireEvent.click(screen.getByTestId('card-form-submit'));
    expect(await screen.findByRole('alert')).toHaveTextContent('Title is required');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('submits with correct values', async () => {
    const user = userEvent.setup();
    const { onSubmit } = renderForm();

    await user.type(screen.getByLabelText('Title'), 'New Card');
    await user.type(screen.getByLabelText('Description'), 'A description');
    await user.click(screen.getByTestId('category-toggle-1'));
    await user.click(screen.getByTestId('category-toggle-3'));

    fireEvent.submit(screen.getByTestId('card-form'));

    expect(onSubmit).toHaveBeenCalledTimes(1);
    const submitted: CardFormValues = onSubmit.mock.calls[0][0];
    expect(submitted.title).toBe('New Card');
    expect(submitted.description).toBe('A description');
    expect(submitted.categoryIds).toEqual([1, 3]);
  });

  it('toggles category selection on and off', async () => {
    const user = userEvent.setup();
    renderForm();

    const toggle = screen.getByTestId('category-toggle-2');
    expect(toggle).toHaveAttribute('aria-pressed', 'false');

    await user.click(toggle);
    expect(toggle).toHaveAttribute('aria-pressed', 'true');

    await user.click(toggle);
    expect(toggle).toHaveAttribute('aria-pressed', 'false');
  });

  it('calls onCancel when cancel button is clicked', async () => {
    const user = userEvent.setup();
    const { onCancel } = renderForm();
    await user.click(screen.getByTestId('card-form-cancel'));
    expect(onCancel).toHaveBeenCalledTimes(1);
  });

  it('renders custom submit label', () => {
    renderForm({ submitLabel: 'Create Card' });
    expect(screen.getByTestId('card-form-submit')).toHaveTextContent('Create Card');
  });

  it('shows submitting state', () => {
    renderForm({ isSubmitting: true });
    const submitBtn = screen.getByTestId('card-form-submit');
    expect(submitBtn).toBeDisabled();
    expect(submitBtn).toHaveTextContent('Saving…');
  });

  it('trims whitespace from title and description on submit', async () => {
    const user = userEvent.setup();
    const { onSubmit } = renderForm();

    await user.type(screen.getByLabelText('Title'), '  Padded Title  ');
    await user.type(screen.getByLabelText('Description'), '  Padded Desc  ');

    fireEvent.submit(screen.getByTestId('card-form'));

    const submitted: CardFormValues = onSubmit.mock.calls[0][0];
    expect(submitted.title).toBe('Padded Title');
    expect(submitted.description).toBe('Padded Desc');
  });

  it('rejects whitespace-only title', () => {
    const user = userEvent.setup();
    const { onSubmit } = renderForm();

    // Set title to spaces only via fireEvent (synchronous)
    fireEvent.change(screen.getByLabelText('Title'), { target: { value: '   ' } });
    fireEvent.submit(screen.getByTestId('card-form'));

    expect(screen.getByRole('alert')).toHaveTextContent('Title is required');
    expect(onSubmit).not.toHaveBeenCalled();
  });
});
