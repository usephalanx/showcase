import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import HelloWorld from './HelloWorld';

describe('HelloWorld', () => {
  it('renders without crashing', () => {
    render(<HelloWorld />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeDefined();
  });

  it('renders the default "Hello World" text when no text prop is provided', () => {
    render(<HelloWorld />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toBe('Hello World');
  });

  it('renders custom text when the text prop is provided', () => {
    render(<HelloWorld text="Greetings, Universe" />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toBe('Greetings, Universe');
  });

  it('applies the className prop to the h1 element', () => {
    render(<HelloWorld className="custom-class" />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.className).toBe('custom-class');
  });

  it('renders without a className when none is provided', () => {
    render(<HelloWorld />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.className).toBe('');
  });

  it('renders an empty string when text prop is an empty string', () => {
    render(<HelloWorld text="" />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toBe('');
  });
});
