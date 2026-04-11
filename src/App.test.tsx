import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the HelloWorld component with correct text', () => {
    render(<App />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading).toBeDefined();
    expect(heading.textContent).toBe('Hello World');
  });

  it('renders the app container with a CSS module class', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container).toBeDefined();
    expect(container.className).toBeTruthy();
    expect(container.className.length).toBeGreaterThan(0);
  });

  it('app container contains the hello heading', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    const heading = screen.getByTestId('hello-heading');
    expect(container.contains(heading)).toBe(true);
  });
});
