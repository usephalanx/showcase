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
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const countDisplay = screen.getByTestId('count-display');

    fireEvent.click(incrementBtn);
    expect(countDisplay).toHaveTextContent('1');

    fireEvent.click(incrementBtn);
    expect(countDisplay).toHaveTextContent('2');
  });

  it('decrements count when decrement button is clicked', () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    const countDisplay = screen.getByTestId('count-display');

    fireEvent.click(decrementBtn);
    expect(countDisplay).toHaveTextContent('-1');

    fireEvent.click(decrementBtn);
    expect(countDisplay).toHaveTextContent('-2');
  });

  it('handles rapid increment and decrement clicks correctly', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    const countDisplay = screen.getByTestId('count-display');

    // Click increment 5 times
    for (let i = 0; i < 5; i++) {
      fireEvent.click(incrementBtn);
    }
    expect(countDisplay).toHaveTextContent('5');

    // Click decrement 3 times
    for (let i = 0; i < 3; i++) {
      fireEvent.click(decrementBtn);
    }
    expect(countDisplay).toHaveTextContent('2');
  });

  it('renders the counter container with centered alignment', () => {
    render(<Counter />);
    const container = screen.getByTestId('counter-container');
    expect(container).toBeInTheDocument();
  });

  it('renders the Counter title', () => {
    render(<Counter />);
    const title = screen.getByText('Counter');
    expect(title).toBeInTheDocument();
  });

  it('renders both increment and decrement buttons', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    expect(incrementBtn).toBeInTheDocument();
    expect(decrementBtn).toBeInTheDocument();
  });

  it('allows count to go negative', () => {
    render(<Counter />);
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    const countDisplay = screen.getByTestId('count-display');

    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    expect(countDisplay).toHaveTextContent('-3');
  });
});
