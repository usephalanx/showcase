/**
 * Smoke test for the root App component.
 *
 * Verifies that App renders without crashing and displays the
 * expected heading from the TodoPage placeholder.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../src/App';

describe('App', () => {
  it('renders the todo app heading', () => {
    render(<App />);
    expect(screen.getByText('Todo App')).toBeInTheDocument();
  });

  it('renders the placeholder message', () => {
    render(<App />);
    expect(screen.getByText('Start adding your todos!')).toBeInTheDocument();
  });
});
