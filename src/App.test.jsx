/**
 * Tests for the App component.
 *
 * Verifies that the App component renders "Hello World" text.
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App.jsx';

describe('App', () => {
  it('renders Hello World', () => {
    render(<App />);
    expect(screen.getByText('Hello World')).toBeDefined();
  });
});
