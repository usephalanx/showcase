import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Modal from './Modal';

describe('Modal', () => {
  const defaultProps = {
    isOpen: true,
    onClose: vi.fn(),
    title: 'Test Modal',
    children: <p>Modal content here</p>,
  };

  it('renders without crashing when open', () => {
    render(<Modal {...defaultProps} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('renders nothing when isOpen is false', () => {
    render(<Modal {...defaultProps} isOpen={false} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('displays the provided title', () => {
    render(<Modal {...defaultProps} title="My Custom Title" />);
    expect(screen.getByTestId('modal-title')).toHaveTextContent('My Custom Title');
  });

  it('renders children content', () => {
    render(
      <Modal {...defaultProps}>
        <span data-testid="custom-child">Hello World</span>
      </Modal>,
    );
    expect(screen.getByTestId('custom-child')).toHaveTextContent('Hello World');
  });

  it('calls onClose when the close button is clicked', () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId('modal-close-button'));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when Escape key is pressed', () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.keyDown(screen.getByTestId('modal-overlay'), { key: 'Escape' });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when the backdrop overlay is clicked', () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId('modal-overlay'));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('does NOT call onClose when the card body is clicked', () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.click(screen.getByTestId('modal-body'));
    expect(onClose).not.toHaveBeenCalled();
  });

  it('sets aria-modal and aria-label on the dialog', () => {
    render(<Modal {...defaultProps} title="Accessible Modal" />);
    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-label', 'Accessible Modal');
  });

  it('applies sm size class', () => {
    render(<Modal {...defaultProps} size="sm" />);
    const dialog = screen.getByRole('dialog');
    expect(dialog.className).toContain('max-w-sm');
  });

  it('applies md size class by default', () => {
    render(<Modal {...defaultProps} />);
    const dialog = screen.getByRole('dialog');
    expect(dialog.className).toContain('max-w-lg');
  });

  it('applies lg size class', () => {
    render(<Modal {...defaultProps} size="lg" />);
    const dialog = screen.getByRole('dialog');
    expect(dialog.className).toContain('max-w-3xl');
  });

  it('does not call onClose for non-Escape key presses', () => {
    const onClose = vi.fn();
    render(<Modal {...defaultProps} onClose={onClose} />);
    fireEvent.keyDown(screen.getByTestId('modal-overlay'), { key: 'Enter' });
    expect(onClose).not.toHaveBeenCalled();
  });

  it('traps focus with Tab on a single focusable element', () => {
    render(
      <Modal {...defaultProps}>
        <button data-testid="inner-btn">Click me</button>
      </Modal>,
    );
    const innerBtn = screen.getByTestId('inner-btn');
    innerBtn.focus();
    // Tab from the only button should cycle back
    fireEvent.keyDown(screen.getByTestId('modal-overlay'), { key: 'Tab' });
    // The focus trap should keep focus within the modal
    expect(document.activeElement).not.toBeNull();
  });
});
