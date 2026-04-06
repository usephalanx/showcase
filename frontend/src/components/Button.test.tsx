import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders without crashing', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('renders children correctly', () => {
    render(<Button>Submit Form</Button>);
    expect(screen.getByText('Submit Form')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(
      <Button onClick={handleClick} disabled>
        Disabled
      </Button>
    );
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies disabled attribute', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('defaults to type="button"', () => {
    render(<Button>Default Type</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('type', 'button');
  });

  it('accepts type="submit"', () => {
    render(<Button type="submit">Submit</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('type', 'submit');
  });

  it('accepts type="reset"', () => {
    render(<Button type="reset">Reset</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('type', 'reset');
  });

  it('applies primary variant classes by default', () => {
    render(<Button>Primary</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('bg-indigo-700');
    expect(button.className).toContain('text-white');
  });

  it('applies secondary variant classes', () => {
    render(<Button variant="secondary">Secondary</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('border-2');
    expect(button.className).toContain('border-indigo-700');
    expect(button.className).toContain('text-indigo-700');
  });

  it('applies ghost variant classes', () => {
    render(<Button variant="ghost">Ghost</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('bg-transparent');
    expect(button.className).toContain('text-indigo-700');
    expect(button.className).not.toContain('border-2');
  });

  it('applies sm size classes', () => {
    render(<Button size="sm">Small</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('px-3');
    expect(button.className).toContain('py-1.5');
    expect(button.className).toContain('text-sm');
  });

  it('applies md size classes by default', () => {
    render(<Button>Medium</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('px-5');
    expect(button.className).toContain('py-2.5');
    expect(button.className).toContain('text-base');
  });

  it('applies lg size classes', () => {
    render(<Button size="lg">Large</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('px-7');
    expect(button.className).toContain('py-3.5');
    expect(button.className).toContain('text-lg');
  });

  it('appends custom className', () => {
    render(<Button className="mt-4 w-full">Custom Class</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('mt-4');
    expect(button.className).toContain('w-full');
  });

  it('renders JSX children', () => {
    render(
      <Button>
        <span data-testid="icon">★</span> Star
      </Button>
    );
    expect(screen.getByTestId('icon')).toBeInTheDocument();
    expect(screen.getByText('Star')).toBeInTheDocument();
  });

  it('includes transition classes for hover/focus states', () => {
    render(<Button>Animated</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('transition-all');
    expect(button.className).toContain('duration-200');
  });

  it('includes focus ring classes on primary variant', () => {
    render(<Button variant="primary">Focus</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('focus:ring-2');
    expect(button.className).toContain('focus:ring-indigo-500');
  });

  it('includes focus ring classes on secondary variant', () => {
    render(<Button variant="secondary">Focus</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('focus:ring-2');
    expect(button.className).toContain('focus:ring-indigo-500');
  });

  it('includes focus ring classes on ghost variant', () => {
    render(<Button variant="ghost">Focus</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('focus:ring-2');
    expect(button.className).toContain('focus:ring-indigo-500');
  });
});
