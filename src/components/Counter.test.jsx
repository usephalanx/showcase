/**
 * Unit and UI tests for the Counter component.
 *
 * Tests cover:
 * - Initial count display renders 0
 * - Increment button increases count by 1
 * - Decrement button decreases count by 1
 * - Count display is centered via text-align style
 */
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.jsx';

describe('Counter component', () => {
  it('renders initial count of 0', () => {
    render(<Counter />);
    const countDisplay = screen.getByTestId('count-display');
    expect(countDisplay).toHaveTextContent('0');
  });

  it('increments count when increment button is clicked', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    const countDisplay = screen.getByTestId('count-display');

    fireEvent.click(incrementButton);
    expect(countDisplay).toHaveTextContent('1');

    fireEvent.click(incrementButton);
    expect(countDisplay).toHaveTextContent('2');
  });

  it('decrements count when decrement button is clicked', () => {
    render(<Counter />);
    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    const countDisplay = screen.getByTestId('count-display');

    fireEvent.click(decrementButton);
    expect(countDisplay).toHaveTextContent('-1');

    fireEvent.click(decrementButton);
    expect(countDisplay).toHaveTextContent('-2');
  });

  it('count display is centered via text-align style', () => {
    render(<Counter />);
    const countDisplay = screen.getByTestId('count-display');
    expect(countDisplay).toHaveStyle({ textAlign: 'center' });
  });

  it('handles rapid increment and decrement clicks correctly', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    const countDisplay = screen.getByTestId('count-display');

    // Rapid increments
    for (let i = 0; i < 10; i++) {
      fireEvent.click(incrementButton);
    }
    expect(countDisplay).toHaveTextContent('10');

    // Rapid decrements
    for (let i = 0; i < 5; i++) {
      fireEvent.click(decrementButton);
    }
    expect(countDisplay).toHaveTextContent('5');
  });

  it('renders both increment and decrement buttons', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    expect(incrementButton).toBeInTheDocument();
    expect(decrementButton).toBeInTheDocument();
  });

  it('renders the Counter heading', () => {
    render(<Counter />);
    const heading = screen.getByRole('heading', { name: /counter/i });
    expect(heading).toBeInTheDocument();
  });
});
