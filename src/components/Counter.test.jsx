/**
 * Unit tests for the Counter component.
 * Verifies initial render, increment, and decrement behavior.
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter', () => {
  it('renders with an initial count of 0', () => {
    render(<Counter />);
    const countElement = screen.getByTestId('count');
    expect(countElement).toHaveTextContent('0');
  });

  it('increments the count when the Increment button is clicked', () => {
    render(<Counter />);
    const incrementButton = screen.getByText('Increment');
    const countElement = screen.getByTestId('count');

    fireEvent.click(incrementButton);
    expect(countElement).toHaveTextContent('1');

    fireEvent.click(incrementButton);
    expect(countElement).toHaveTextContent('2');
  });

  it('decrements the count when the Decrement button is clicked', () => {
    render(<Counter />);
    const decrementButton = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    fireEvent.click(decrementButton);
    expect(countElement).toHaveTextContent('-1');

    fireEvent.click(decrementButton);
    expect(countElement).toHaveTextContent('-2');
  });

  it('handles rapid increment and decrement clicks correctly', () => {
    render(<Counter />);
    const incrementButton = screen.getByText('Increment');
    const decrementButton = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    // Increment 5 times
    for (let i = 0; i < 5; i++) {
      fireEvent.click(incrementButton);
    }
    expect(countElement).toHaveTextContent('5');

    // Decrement 3 times
    for (let i = 0; i < 3; i++) {
      fireEvent.click(decrementButton);
    }
    expect(countElement).toHaveTextContent('2');
  });

  it('displays the Increment and Decrement buttons', () => {
    render(<Counter />);
    expect(screen.getByText('Increment')).toBeInTheDocument();
    expect(screen.getByText('Decrement')).toBeInTheDocument();
  });
});
