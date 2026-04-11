import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders Hello World heading', () => {
    render(<App />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeDefined();
    expect(heading.textContent).toBe('Hello World');
  });

  it('centers heading with white background', () => {
    const { container } = render(<App />);
    const wrapper = container.firstElementChild as HTMLElement;
    expect(wrapper).toBeDefined();
    expect(wrapper.style.display).toBe('flex');
    expect(wrapper.style.justifyContent).toBe('center');
    expect(wrapper.style.alignItems).toBe('center');
    expect(wrapper.style.backgroundColor).toBe('#ffffff');
  });
});
