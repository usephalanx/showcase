import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

/**
 * Test suite for the App component.
 *
 * Verifies that the main App component renders correctly,
 * displays the expected 'Hello World' text, and applies
 * scoped CSS module styles.
 */
describe('App', () => {
  it('renders Hello World text', () => {
    render(<App />);
    const heading = screen.getByText('Hello World');
    expect(heading).toBeInTheDocument();
  });

  it('renders Hello World inside an h1 element', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('applies CSS module class to the container', () => {
    const { container } = render(<App />);
    const wrapper = container.firstChild;
    expect(wrapper).toBeDefined();
    expect(wrapper.className).toBeTruthy();
  });

  it('applies CSS module class to the heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.className).toBeTruthy();
  });
});
