import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders hello-world text', () => {
    render(<App />);
    expect(screen.getByText('hello-world')).toBeInTheDocument();
  });

  it('returns a div element', () => {
    const { container } = render(<App />);
    const div = container.firstChild as HTMLElement;
    expect(div.tagName).toBe('DIV');
  });
});
