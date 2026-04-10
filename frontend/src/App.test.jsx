import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

/**
 * Unit tests for the App component.
 */
describe('App', () => {
  it('renders Hello World', () => {
    render(<App />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });
});
