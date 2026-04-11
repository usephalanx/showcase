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

  it('app container has the correct CSS module class name', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container.className).toContain('container');
  });

  it('renders the heading as an h1 element inside the app', () => {
    render(<App />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading.tagName).toBe('H1');
  });

  it('app container is a div element', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container.tagName).toBe('DIV');
  });
});
