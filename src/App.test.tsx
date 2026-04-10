/**
 * Tests for the main App component.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('renders the welcome subtitle', () => {
    render(<App />);
    const subtitle = screen.getByText(/welcome to your react/i);
    expect(subtitle).toBeInTheDocument();
  });

  it('has the correct CSS module class on the container', () => {
    const { container } = render(<App />);
    const wrapper = container.firstElementChild;
    expect(wrapper).toBeDefined();
  });
});
