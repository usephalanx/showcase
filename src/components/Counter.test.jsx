import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Counter from './Counter';

describe('Counter component', () => {
  it('renders with initial count of 0', () => {
    render(<Counter />);
    const countElement = screen.getByTestId('count');
    expect(countElement).toHaveTextContent('0');
  });

  it('renders the Counter heading', () => {
    render(<Counter />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
  });

  it('renders Increment and Decrement buttons', () => {
    render(<Counter />);
    expect(screen.getByText('Increment')).toBeInTheDocument();
    expect(screen.getByText('Decrement')).toBeInTheDocument();
  });

  it('increments the count when Increment button is clicked', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const countElement = screen.getByTestId('count');

    fireEvent.click(incrementBtn);
    expect(countElement).toHaveTextContent('1');

    fireEvent.click(incrementBtn);
    expect(countElement).toHaveTextContent('2');
  });

  it('decrements the count when Decrement button is clicked', () => {
    render(<Counter />);
    const decrementBtn = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    fireEvent.click(decrementBtn);
    expect(countElement).toHaveTextContent('-1');

    fireEvent.click(decrementBtn);
    expect(countElement).toHaveTextContent('-2');
  });

  it('handles mixed increment and decrement clicks correctly', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const decrementBtn = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    expect(countElement).toHaveTextContent('2');
  });

  it('handles rapid clicking correctly', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const countElement = screen.getByTestId('count');

    for (let i = 0; i < 10; i++) {
      fireEvent.click(incrementBtn);
    }
    expect(countElement).toHaveTextContent('10');
  });

  it('can display negative numbers with no lower bound', () => {
    render(<Counter />);
    const decrementBtn = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    for (let i = 0; i < 5; i++) {
      fireEvent.click(decrementBtn);
    }
    expect(countElement).toHaveTextContent('-5');
  });

  it('returns to zero after equal increments and decrements', () => {
    render(<Counter />);
    const incrementBtn = screen.getByText('Increment');
    const decrementBtn = screen.getByText('Decrement');
    const countElement = screen.getByTestId('count');

    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(incrementBtn);
    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    fireEvent.click(decrementBtn);
    expect(countElement).toHaveTextContent('0');
  });
});
