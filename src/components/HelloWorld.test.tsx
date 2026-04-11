import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import HelloWorld from './HelloWorld';

describe('HelloWorld', () => {
  it('renders a heading with "Hello World" text', () => {
    render(<HelloWorld />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading).toBeDefined();
    expect(heading.textContent).toBe('Hello World');
  });

  it('renders as an h1 element', () => {
    render(<HelloWorld />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading.tagName).toBe('H1');
  });

  it('has a CSS module class applied', () => {
    render(<HelloWorld />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading.className).toBeTruthy();
    expect(heading.className.length).toBeGreaterThan(0);
  });
});
