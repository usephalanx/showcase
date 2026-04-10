/**
 * Unit tests for the App component.
 * Verifies that the Counter component is rendered within App.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the Counter component', () => {
    render(<App />);
    // The Counter component renders a heading with text "Counter"
    expect(screen.getByText('Counter')).toBeInTheDocument();
  });

  it('renders the count display', () => {
    render(<App />);
    expect(screen.getByTestId('count')).toBeInTheDocument();
  });

  it('renders increment and decrement buttons', () => {
    render(<App />);
    expect(screen.getByText('Increment')).toBeInTheDocument();
    expect(screen.getByText('Decrement')).toBeInTheDocument();
  });
});
