import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom/vitest';
import App from './App';

/**
 * Unit tests for the App component.
 */
describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
  });

  it('renders a heading with "Hello World" text by default', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Hello World');
  });

  it('renders a visible heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeVisible();
  });

  it('renders custom title when provided via props', () => {
    render(<App title="Custom Title" />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toHaveTextContent('Custom Title');
  });

  it('does not render hardcoded text when a custom title is passed', () => {
    render(<App title="Goodbye World" />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).not.toHaveTextContent('Hello World');
    expect(heading).toHaveTextContent('Goodbye World');
  });
});
