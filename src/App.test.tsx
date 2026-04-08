import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  /**
   * Verify that the App component renders an h1 heading with the
   * expected "Hello World" text content.
   */
  it('renders a Hello World heading', () => {
    render(<App />);

    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });

  /**
   * Verify that the rendered heading element is visible in the DOM.
   */
  it('heading is visible', () => {
    render(<App />);

    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeVisible();
  });
});
