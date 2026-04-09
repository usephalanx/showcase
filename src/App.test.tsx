/**
 * Unit tests for the App component.
 *
 * Verifies the Hello World heading renders, the counter starts at zero,
 * and clicking the button increments the displayed count.
 */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });

  it('counter starts at zero', () => {
    render(<App />);
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent('Count: 0');
  });

  it('increments count on click', () => {
    render(<App />);
    const button = screen.getByRole('button');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 1');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 2');
  });
});
