/**
 * Smoke tests for the App component.
 *
 * Verifies that the App renders and includes the Counter component.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App component', () => {
  it('renders the Counter component', () => {
    render(<App />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
    expect(screen.getByTestId('count-display')).toBeInTheDocument();
  });

  it('renders increment and decrement buttons', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /decrement/i })).toBeInTheDocument();
  });
});
