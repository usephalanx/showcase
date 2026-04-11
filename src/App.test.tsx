import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders the HelloWorld component inside the app', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('has an app container with the correct CSS module class', () => {
    render(<App />);
    const container = screen.getByTestId('app-container');
    expect(container).toBeInTheDocument();
    expect(container.className).toContain('container');
  });
});
