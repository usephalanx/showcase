/**
 * Tests for the TodoPage placeholder component.
 *
 * Verifies that the placeholder renders its heading and message.
 * These tests will be expanded when TodoPage gains real functionality.
 */
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import TodoPage from '../src/pages/TodoPage';

describe('TodoPage', () => {
  it('renders the page heading', () => {
    render(<TodoPage />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Todo App');
  });

  it('renders the placeholder text', () => {
    render(<TodoPage />);
    expect(screen.getByText('Start adding your todos!')).toBeInTheDocument();
  });

  it('wraps content in a main element', () => {
    render(<TodoPage />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
    expect(main).toHaveClass('todo-page');
  });
});
