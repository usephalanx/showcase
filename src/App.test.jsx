import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App component', () => {
  it('renders the Counter component', () => {
    render(<App />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
  });

  it('renders the count display', () => {
    render(<App />);
    expect(screen.getByTestId('count')).toBeInTheDocument();
  });

  it('renders increment and decrement buttons', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /decrement/i })).toBeInTheDocument();
  });
});
