/**
 * Smoke tests for the App component.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App component', () => {
  it('renders the application heading', () => {
    render(<App />);
    const heading = screen.getByText('Mini React Counter');
    expect(heading).toBeInTheDocument();
  });

  it('renders the Counter component', () => {
    render(<App />);
    const countDisplay = screen.getByTestId('count-display');
    expect(countDisplay).toBeInTheDocument();
    expect(countDisplay).toHaveTextContent('Count: 0');
  });

  it('renders increment and decrement buttons', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /decrement/i })).toBeInTheDocument();
  });
});
