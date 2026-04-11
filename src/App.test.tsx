import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('centers heading with white background', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    const container = heading.parentElement as HTMLElement;
    expect(container).toBeDefined();
    expect(container.style.display).toBe('flex');
    expect(container.style.justifyContent).toBe('center');
    expect(container.style.alignItems).toBe('center');
    expect(container.style.minHeight).toBe('100vh');
    expect(container.style.backgroundColor).toBe('#ffffff');
  });
});
