/**
 * Test suite for the App component.
 *
 * Verifies that the main SPA component renders the expected
 * 'hello-world' text content.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders hello-world text in the document', () => {
    render(<App />);
    const element = screen.getByText('hello-world');
    expect(element).toBeInTheDocument();
  });

  it('renders hello-world inside a div element', () => {
    const { container } = render(<App />);
    const div = container.querySelector('div');
    expect(div).not.toBeNull();
    expect(div!.textContent).toBe('hello-world');
  });

  it('renders exactly the text hello-world with no extra content', () => {
    render(<App />);
    const element = screen.getByText('hello-world');
    expect(element.textContent).toBe('hello-world');
  });
});
