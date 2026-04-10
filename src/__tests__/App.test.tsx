import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

/**
 * Test suite for the App component.
 *
 * Verifies that the 'yellow world' text is rendered in the DOM and
 * that the correct yellow-themed CSS module class names are applied
 * to the container and heading elements.
 */
describe('App Component', () => {
  it('renders the yellow world text', () => {
    render(<App />);
    const heading = screen.getByText('yellow world');
    expect(heading).toBeInTheDocument();
  });

  it('renders the yellow world text in an h1 element', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('yellow world');
  });

  it('applies the container CSS module class to the wrapper div', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container).toBeInTheDocument();
    expect(container.className).toContain('container');
  });

  it('applies the heading CSS module class to the h1 element', () => {
    render(<App />);
    const heading = screen.getByTestId('app-heading');
    expect(heading).toBeInTheDocument();
    expect(heading.className).toContain('heading');
  });

  it('renders the heading inside the container', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    const heading = screen.getByTestId('app-heading');
    expect(container).toContainElement(heading);
  });

  it('renders exactly one h1 element', () => {
    const { container } = render(<App />);
    const headings = container.querySelectorAll('h1');
    expect(headings).toHaveLength(1);
  });

  it('has the correct text content without extra whitespace', () => {
    render(<App />);
    const heading = screen.getByTestId('app-heading');
    expect(heading.textContent?.trim()).toBe('yellow world');
  });

  it('container and heading have distinct CSS module classes', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    const heading = screen.getByTestId('app-heading');
    expect(container.className).not.toBe(heading.className);
  });

  it('container element is a div', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container.tagName).toBe('DIV');
  });

  it('heading element is an h1', () => {
    render(<App />);
    const heading = screen.getByTestId('app-heading');
    expect(heading.tagName).toBe('H1');
  });
});
