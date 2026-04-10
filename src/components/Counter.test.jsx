import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter component', () => {
  it('renders with initial count of 0', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('Count: 0');
  });

  it('renders increment and decrement buttons', () => {
    render(<Counter />);
    expect(screen.getByRole('button', { name: /increment/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /decrement/i })).toBeInTheDocument();
  });

  it('increments count when Increment button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    await user.click(incrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 1');
  });

  it('decrements count when Decrement button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    await user.click(decrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: -1');
  });

  it('increments multiple times correctly', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(incrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 3');
  });

  it('decrements multiple times correctly', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    await user.click(decrementBtn);
    await user.click(decrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: -2');
  });

  it('handles mixed increment and decrement operations', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });

    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(decrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 2');
  });

  it('returns to zero after equal increments and decrements', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });

    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(decrementBtn);
    await user.click(decrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 0');
  });

  it('allows count to go below zero', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    await user.click(decrementBtn);
    await user.click(decrementBtn);
    await user.click(decrementBtn);

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: -3');
  });

  it('handles rapid clicking correctly', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementBtn = screen.getByRole('button', { name: /increment/i });

    // Rapid clicks
    for (let i = 0; i < 10; i++) {
      await user.click(incrementBtn);
    }

    expect(screen.getByTestId('count-display')).toHaveTextContent('Count: 10');
  });
});
