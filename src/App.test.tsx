import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      'Hello World',
    );
  });

  it('counter starts at zero', () => {
    render(<App />);
    expect(screen.getByRole('button')).toHaveTextContent('Count: 0');
  });

  it('increments counter on click', () => {
    render(<App />);
    const button = screen.getByRole('button');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 1');

    fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 2');
  });
});
