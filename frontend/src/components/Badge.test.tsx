import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Badge from './Badge';
import type { BadgeVariant } from './Badge';

describe('Badge', () => {
  it('renders without crashing', () => {
    render(<Badge text="Test" />);
    expect(screen.getByTestId('badge')).toBeInTheDocument();
  });

  it('displays the provided text', () => {
    render(<Badge text="Featured" />);
    expect(screen.getByText('Featured')).toBeInTheDocument();
  });

  it('applies default variant styles when no variant is specified', () => {
    render(<Badge text="Default" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('bg-gray-100');
    expect(badge.className).toContain('text-gray-800');
  });

  it('applies featured variant styles', () => {
    render(<Badge text="Featured" variant="featured" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('bg-amber-100');
    expect(badge.className).toContain('text-amber-800');
  });

  it('applies new variant styles', () => {
    render(<Badge text="New" variant="new" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('bg-emerald-100');
    expect(badge.className).toContain('text-emerald-800');
  });

  it('applies sale variant styles', () => {
    render(<Badge text="For Sale" variant="sale" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('bg-blue-100');
    expect(badge.className).toContain('text-blue-800');
  });

  it('applies rent variant styles', () => {
    render(<Badge text="For Rent" variant="rent" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('bg-purple-100');
    expect(badge.className).toContain('text-purple-800');
  });

  it('uses rounded-full pill style', () => {
    render(<Badge text="Pill" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('rounded-full');
  });

  it('merges additional className prop', () => {
    render(<Badge text="Custom" className="mt-4 shadow-lg" />);
    const badge = screen.getByTestId('badge');
    expect(badge.className).toContain('mt-4');
    expect(badge.className).toContain('shadow-lg');
  });

  it('does not add extra space when className is empty', () => {
    render(<Badge text="No Extra" className="" />);
    const badge = screen.getByTestId('badge');
    // Ensure no trailing space
    expect(badge.className).not.toMatch(/\s$/);
  });

  it('renders all variant types without errors', () => {
    const variants: BadgeVariant[] = ['featured', 'new', 'sale', 'rent', 'default'];
    variants.forEach((variant) => {
      const { unmount } = render(<Badge text={`Test ${variant}`} variant={variant} />);
      expect(screen.getByText(`Test ${variant}`)).toBeInTheDocument();
      unmount();
    });
  });

  it('renders as an inline-flex span element', () => {
    render(<Badge text="Span" />);
    const badge = screen.getByTestId('badge');
    expect(badge.tagName).toBe('SPAN');
    expect(badge.className).toContain('inline-flex');
  });
});
