import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import HelloWorld from './HelloWorld';

describe('HelloWorld', () => {
  it('renders an <h1> element with the text "Hello World"', () => {
    render(<HelloWorld />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading).toBeDefined();
    expect(heading.tagName).toBe('H1');
    expect(heading.textContent).toBe('Hello World');
  });

  it('applies the CSS module heading class', () => {
    render(<HelloWorld />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading.className).toBeTruthy();
    expect(heading.className.length).toBeGreaterThan(0);
    expect(heading.className).toContain('heading');
  });

  it('renders exactly one heading element', () => {
    const { container } = render(<HelloWorld />);
    const headings = container.querySelectorAll('h1');
    expect(headings.length).toBe(1);
  });

  it('heading is accessible via role', () => {
    render(<HelloWorld />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeDefined();
    expect(heading.textContent).toBe('Hello World');
  });
});
