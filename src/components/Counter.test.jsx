import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.jsx';
import App from '../App.jsx';

describe('Counter component', () => {
  it('renders with an initial count of 0', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('0');
  });

  it('renders the heading text "Counter"', () => {
    render(<Counter />);
    const heading = screen.getByRole('heading', { name: /counter/i });
    expect(heading).toBeInTheDocument();
  });

  it('renders increment and decrement buttons', () => {
    render(<Counter />);
    const incrementBtn = screen.getByTestId('increment-button');
    const decrementBtn = screen.getByTestId('decrement-button');
    expect(incrementBtn).toBeInTheDocument();
    expect(decrementBtn).toBeInTheDocument();
  });

  it('increments the count when increment button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);
    const incrementBtn = screen.getByTestId('increment-button');
    const display = screen.getByTestId('count-display');

    await user.click(incrementBtn);
    expect(display).toHaveTextContent('1');

    await user.click(incrementBtn);
    expect(display).toHaveTextContent('2');
  });

  it('decrements the count when decrement button is clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);
    const decrementBtn = screen.getByTestId('decrement-button');
    const display = screen.getByTestId('count-display');

    await user.click(decrementBtn);
    expect(display).toHaveTextContent('-1');

    await user.click(decrementBtn);
    expect(display).toHaveTextContent('-2');
  });

  it('handles a mix of increment and decrement clicks correctly', async () => {
    const user = userEvent.setup();
    render(<Counter />);
    const incrementBtn = screen.getByTestId('increment-button');
    const decrementBtn = screen.getByTestId('decrement-button');
    const display = screen.getByTestId('count-display');

    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(incrementBtn);
    expect(display).toHaveTextContent('3');

    await user.click(decrementBtn);
    expect(display).toHaveTextContent('2');

    await user.click(decrementBtn);
    await user.click(decrementBtn);
    expect(display).toHaveTextContent('0');
  });

  it('allows count to go negative', async () => {
    const user = userEvent.setup();
    render(<Counter />);
    const decrementBtn = screen.getByTestId('decrement-button');
    const display = screen.getByTestId('count-display');

    await user.click(decrementBtn);
    await user.click(decrementBtn);
    await user.click(decrementBtn);
    expect(display).toHaveTextContent('-3');
  });

  it('handles rapid clicks correctly', async () => {
    const user = userEvent.setup();
    render(<Counter />);
    const incrementBtn = screen.getByTestId('increment-button');
    const display = screen.getByTestId('count-display');

    // Rapid-fire 10 clicks
    for (let i = 0; i < 10; i++) {
      await user.click(incrementBtn);
    }
    expect(display).toHaveTextContent('10');
  });

  it('has accessible button labels', () => {
    render(<Counter />);
    const incrementBtn = screen.getByRole('button', { name: /increment/i });
    const decrementBtn = screen.getByRole('button', { name: /decrement/i });
    expect(incrementBtn).toBeInTheDocument();
    expect(decrementBtn).toBeInTheDocument();
  });

  it('has an aria-live region for the count display', () => {
    render(<Counter />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveAttribute('aria-live', 'polite');
  });

  it('count display is centered within the counter wrapper (text-align)', () => {
    render(<Counter />);
    const wrapper = screen.getByTestId('counter-wrapper');
    expect(wrapper).toHaveClass('counter-wrapper');
    // The counter-wrapper class applies text-align: center and align-items: center
    // Verify the wrapper element has the centering class applied
    const display = screen.getByTestId('count-display');
    expect(display).toHaveClass('count-display');
  });
});

describe('App component', () => {
  it('renders the Counter component inside a centered container', () => {
    render(<App />);
    const appContainer = screen.getByTestId('app-container');
    expect(appContainer).toBeInTheDocument();
    expect(appContainer).toHaveClass('app-container');
  });

  it('displays the Counter inside the App', () => {
    render(<App />);
    const counterWrapper = screen.getByTestId('counter-wrapper');
    expect(counterWrapper).toBeInTheDocument();
  });

  it('shows initial count of 0 when App renders', () => {
    render(<App />);
    const display = screen.getByTestId('count-display');
    expect(display).toHaveTextContent('0');
  });

  it('increment and decrement work through the App', async () => {
    const user = userEvent.setup();
    render(<App />);
    const incrementBtn = screen.getByTestId('increment-button');
    const decrementBtn = screen.getByTestId('decrement-button');
    const display = screen.getByTestId('count-display');

    await user.click(incrementBtn);
    await user.click(incrementBtn);
    expect(display).toHaveTextContent('2');

    await user.click(decrementBtn);
    expect(display).toHaveTextContent('1');
  });

  it('app container uses flex centering class', () => {
    render(<App />);
    const appContainer = screen.getByTestId('app-container');
    // Verify the container has the app-container class which provides
    // display:flex, justify-content:center, align-items:center
    expect(appContainer).toHaveClass('app-container');
  });
});
