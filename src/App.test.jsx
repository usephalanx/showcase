import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App component', () => {
  it('renders the app heading', () => {
    render(<App />);
    expect(screen.getByText('Mini React Counter App')).toBeInTheDocument();
  });

  it('renders the Counter component within the App', () => {
    render(<App />);
    expect(screen.getByText('Counter')).toBeInTheDocument();
    expect(screen.getByTestId('count')).toBeInTheDocument();
    expect(screen.getByText('Increment')).toBeInTheDocument();
    expect(screen.getByText('Decrement')).toBeInTheDocument();
  });

  it('Counter inside App is functional', () => {
    render(<App />);
    const incrementBtn = screen.getByText('Increment');
    const countElement = screen.getByTestId('count');

    expect(countElement).toHaveTextContent('0');
    incrementBtn.click();
    expect(countElement).toHaveTextContent('1');
  });
});
