import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App component', () => {
  it('renders the app heading', () => {
    render(<App />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      'Mini React Counter App'
    );
  });

  it('renders the Counter component', () => {
    render(<App />);
    expect(screen.getByTestId('count-display')).toBeInTheDocument();
  });

  it('renders increment and decrement buttons via Counter', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /decrement/i })).toBeInTheDocument();
  });

  it('shows initial count of 0 via Counter', () => {
    render(<App />);
    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 0');
  });
});
