import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

/**
 * Unit tests for the App component.
 */
describe('App', () => {
  it('renders the Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });

  it('counter starts at zero', () => {
    render(<App />);
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent('Count: 0');
  });

  it('increments the counter on click', () => {
    render(<App />);
    const button = screen.getByRole('button');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 1');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 2');
  });
});
