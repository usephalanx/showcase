import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders without crashing', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('renders children text correctly', () => {
    render(<Button>Get Started</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Get Started');
  });

  it('renders as a <button> element by default', () => {
    render(<Button>Test</Button>);
    const el = screen.getByRole('button');
    expect(el.tagName).toBe('BUTTON');
  });

  it('renders as an <a> element when href is provided', () => {
    render(<Button href="https://example.com">Link</Button>);
    const el = screen.getByRole('button');
    expect(el.tagName).toBe('A');
    expect(el).toHaveAttribute('href', 'https://example.com');
  });

  it('applies primary variant classes by default', () => {
    render(<Button>Primary</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('bg-gold');
    expect(el.className).toContain('text-slate-900');
  });

  it('applies secondary variant classes', () => {
    render(<Button variant="secondary">Secondary</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('border-gold');
    expect(el.className).toContain('bg-transparent');
  });

  it('applies outline variant classes', () => {
    render(<Button variant="outline">Outline</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('border-slate-500');
    expect(el.className).toContain('bg-transparent');
  });

  it('includes hover scale animation class', () => {
    render(<Button>Hover me</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('hover:scale-105');
  });

  it('includes focus-visible ring classes for accessibility', () => {
    render(<Button>Focus me</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('focus-visible:ring-2');
    expect(el.className).toContain('focus-visible:ring-gold');
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('calls onClick on anchor variant when clicked', () => {
    const handleClick = vi.fn((e: React.MouseEvent) => e.preventDefault());
    render(
      <Button href="#section" onClick={handleClick}>
        Nav Link
      </Button>
    );
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies custom className', () => {
    render(<Button className="mt-4 custom-class">Styled</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('mt-4');
    expect(el.className).toContain('custom-class');
  });

  it('renders disabled state correctly', () => {
    render(<Button disabled>Disabled</Button>);
    const el = screen.getByRole('button') as HTMLButtonElement;
    expect(el).toBeDisabled();
    expect(el.className).toContain('disabled:opacity-50');
  });

  it('renders as button (not anchor) when disabled even with href', () => {
    render(
      <Button href="https://example.com" disabled>
        Disabled Link
      </Button>
    );
    const el = screen.getByRole('button');
    expect(el.tagName).toBe('BUTTON');
    expect(el).toBeDisabled();
  });

  it('applies aria-label when provided', () => {
    render(<Button aria-label="Close dialog">X</Button>);
    const el = screen.getByRole('button');
    expect(el).toHaveAttribute('aria-label', 'Close dialog');
  });

  it('sets button type attribute', () => {
    render(<Button type="submit">Submit</Button>);
    const el = screen.getByRole('button') as HTMLButtonElement;
    expect(el.type).toBe('submit');
  });

  it('defaults button type to "button"', () => {
    render(<Button>Default Type</Button>);
    const el = screen.getByRole('button') as HTMLButtonElement;
    expect(el.type).toBe('button');
  });

  it('includes transition classes for smooth animation', () => {
    render(<Button>Animated</Button>);
    const el = screen.getByRole('button');
    expect(el.className).toContain('transition-all');
    expect(el.className).toContain('duration-300');
    expect(el.className).toContain('transform');
  });
});
