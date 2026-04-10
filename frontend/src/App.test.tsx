import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Hello World', () => {
    render(<App />);
    const heading = screen.getByText('Hello World');
    expect(heading).toBeInTheDocument();
  });

  it('renders an h1 element', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });
});
