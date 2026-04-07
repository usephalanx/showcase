import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Logo from './Logo';

describe('Logo', () => {
  it('renders without crashing', () => {
    render(<Logo />);
    const svg = screen.getByTestId('logo-svg');
    expect(svg).toBeDefined();
  });

  it('renders the main text "Maddie"', () => {
    render(<Logo />);
    const text = screen.getByTestId('logo-text');
    expect(text.textContent).toBe('Maddie');
  });

  it('renders the subtitle "REAL ESTATE"', () => {
    render(<Logo />);
    const subtitle = screen.getByTestId('logo-subtitle');
    expect(subtitle.textContent).toBe('REAL ESTATE');
  });

  it('renders the house/key icon group', () => {
    render(<Logo />);
    const icon = screen.getByTestId('logo-icon');
    expect(icon).toBeDefined();
  });

  it('has correct aria-label for accessibility', () => {
    render(<Logo />);
    const svg = screen.getByRole('img');
    expect(svg.getAttribute('aria-label')).toBe('Maddie Real Estate logo');
  });

  it('defaults to sm size variant', () => {
    render(<Logo />);
    const svg = screen.getByTestId('logo-svg');
    expect(svg.getAttribute('width')).toBe('140');
    expect(svg.getAttribute('height')).toBe('36');
  });

  it('renders lg size variant with larger dimensions', () => {
    render(<Logo size="lg" />);
    const svg = screen.getByTestId('logo-svg');
    expect(svg.getAttribute('width')).toBe('260');
    expect(svg.getAttribute('height')).toBe('64');
  });

  it('applies custom className', () => {
    render(<Logo className="my-custom-class" />);
    const svg = screen.getByTestId('logo-svg');
    expect(svg.classList.contains('my-custom-class')).toBe(true);
  });

  it('does not apply className when not provided', () => {
    render(<Logo />);
    const svg = screen.getByTestId('logo-svg');
    // className should be empty string by default
    expect(svg.getAttribute('class')).toBe('');
  });

  it('contains a <title> element for SEO and accessibility', () => {
    render(<Logo />);
    const svg = screen.getByTestId('logo-svg');
    const titleEl = svg.querySelector('title');
    expect(titleEl).not.toBeNull();
    expect(titleEl!.textContent).toBe('Maddie Real Estate');
  });

  it('uses the gold color (#C9A84C) in the house path fill', () => {
    render(<Logo />);
    const icon = screen.getByTestId('logo-icon');
    const path = icon.querySelector('path');
    expect(path).not.toBeNull();
    expect(path!.getAttribute('fill')).toBe('#C9A84C');
  });

  it('uses the slate color (#334155) for the main text', () => {
    render(<Logo />);
    const text = screen.getByTestId('logo-text');
    expect(text.getAttribute('fill')).toBe('#334155');
  });

  it('uses the gold color (#C9A84C) for the subtitle', () => {
    render(<Logo />);
    const subtitle = screen.getByTestId('logo-subtitle');
    expect(subtitle.getAttribute('fill')).toBe('#C9A84C');
  });
});
