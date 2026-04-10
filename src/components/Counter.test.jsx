/**
 * Unit tests for the Counter component.
 *
 * Verifies initial count display, increment, and decrement behaviour.
 */
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter component', () => {
  it('renders the initial count of 0 by default', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('0');
  });

  it('renders a custom initial count when provided', () => {
    render(<Counter initialCount={5} />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('5');
  });

  it('increments the count when the increment button is clicked', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    const incrementBtn = screen.getByRole('button', { name: /increment/i });

    fireEvent.click(incrementBtn);
    expect(display).toHaveTextContent('1');

    fireEvent.click(incrementBtn);
    expect(display).toHaveTextContent('2');
  });

  it('decrements the count when the decrement button is clicked', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });

    fireEvent.click(decrementBtn);
    expect(display).toHaveTextContent('-1');
  });

  it('handles rapid increment and decrement clicks correctly', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });

    for (let i = 0; i < 10; i++) {
      fireEvent.click(incrementBtn);
    }
    expect(display).toHaveTextContent('10');

    for (let i = 0; i < 3; i++) {
      fireEvent.click(decrementBtn);
    }
    expect(display).toHaveTextContent('7');
  });

  it('displays the Counter heading', () => {
    render(<Counter />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
  });
});
