import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Hi text', () => {
    render(<App />);
    expect(screen.getByText('Hi')).toBeInTheDocument();
  });
});
