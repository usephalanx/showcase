import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App.jsx';

describe('App', () => {
  it('renders the Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { name: /hello world/i });
    expect(heading).toBeInTheDocument();
  });

  it('renders Hello World as text content', () => {
    render(<App />);
    const element = screen.getByText('Hello World');
    expect(element).toBeInTheDocument();
  });

  it('renders exactly one heading element', () => {
    const { container } = render(<App />);
    const headings = container.querySelectorAll('h1');
    expect(headings).toHaveLength(1);
  });

  it('heading contains the exact text Hello World', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });
});
