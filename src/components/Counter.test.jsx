/**
 * Unit tests for the Counter component.
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter component', () => {
  it('renders the initial count of 0', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: 0');
  });

  it('increments the count when Increment button is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementBtn);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: 1');
  });

  it('decrements the count when Decrement button is clicked', () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(decrementBtn);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: -1');
  });

  it('handles multiple increments correctly', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: 3');
  });

  it('handles mixed increment and decrement clicks', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: 1');
  });
});
