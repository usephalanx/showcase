import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.jsx';

describe('Counter component', () => {
  it('renders initial count of 0', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('0');
  });

  it('increments count when increment button is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementBtn);
    expect(screen.getByTestId('count-display')).toHaveTextContent('1');
  });

  it('decrements count when decrement button is clicked', () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId('count-display')).toHaveTextContent('-1');
  });

  it('handles multiple increments correctly', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    expect(screen.getByTestId('count-display')).toHaveTextContent('3');
  });

  it('handles multiple decrements correctly', () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId('count-display')).toHaveTextContent('-2');
  });

  it('handles mixed increment and decrement clicks', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    expect(screen.getByTestId('count-display')).toHaveTextContent('1');
  });

  it('renders the count display centered (text-align: center)', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display.style.textAlign).toBe('center');
  });

  it('renders the counter container with centered alignment', () => {
    const { container } = render(<Counter />);
    const counterDiv = container.querySelector('.counter');
    expect(counterDiv).not.toBeNull();
    expect(counterDiv.style.alignItems).toBe('center');
  });
});
