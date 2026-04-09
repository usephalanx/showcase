import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the Hello World heading', () => {
    render(<App />);
    const heading = screen.getByTestId('hello-heading');
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });
});
