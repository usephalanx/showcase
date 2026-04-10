/**
 * Tests for the App component.
 *
 * Verifies that the main App component renders correctly with
 * the expected "Hello World" heading.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });

  it('renders inside an element with class "app"', () => {
    const { container } = render(<App />);
    const appDiv = container.querySelector('.app');
    expect(appDiv).toBeInTheDocument();
  });

  it('renders an h1 element', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });
});
