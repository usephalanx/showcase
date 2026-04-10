import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders Hello World', () => {
    render(<App />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });

  it('renders Hello World inside an h1 element', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });

  it('applies container class to the root div', () => {
    const { container } = render(<App />);
    const rootDiv = container.firstChild;
    expect(rootDiv).toHaveClass('container');
  });

  it('applies title class to the heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveClass('title');
  });
});
