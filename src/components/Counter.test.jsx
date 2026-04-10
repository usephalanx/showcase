import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from './Counter';

describe('Counter component', () => {
  it('renders initial count of 0', () => {
    render(<Counter />);
    const countElement = screen.getByTestId('count');
    expect(countElement).toHaveTextContent('0');
  });

  it('increments count when increment button is clicked', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementButton);
    expect(screen.getByTestId('count')).toHaveTextContent('1');
  });

  it('decrements count when decrement button is clicked', () => {
    render(<Counter />);
    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(decrementButton);
    expect(screen.getByTestId('count')).toHaveTextContent('-1');
  });

  it('handles multiple increments correctly', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementButton);
    fireEvent.click(incrementButton);
    fireEvent.click(incrementButton);
    expect(screen.getByTestId('count')).toHaveTextContent('3');
  });

  it('handles mixed increment and decrement clicks', () => {
    render(<Counter />);
    const incrementButton = screen.getByRole('button', { name: /increment/i });
    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(incrementButton);
    fireEvent.click(incrementButton);
    fireEvent.click(decrementButton);
    expect(screen.getByTestId('count')).toHaveTextContent('1');
  });

  it('displays the Counter heading', () => {
    render(<Counter />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
  });
});
