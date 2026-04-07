import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TodoInput from './TodoInput';

describe('TodoInput', () => {
  it('renders an input and an Add button', () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    expect(screen.getByRole('textbox', { name: /todo text/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add/i })).toBeInTheDocument();
  });

  it('updates the input value when typing', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const input = screen.getByRole('textbox', { name: /todo text/i });
    await userEvent.type(input, 'Buy groceries');

    expect(input).toHaveValue('Buy groceries');
  });

  it('calls onAdd with trimmed text when the Add button is clicked', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const input = screen.getByRole('textbox', { name: /todo text/i });
    const button = screen.getByRole('button', { name: /add/i });

    await userEvent.type(input, '  Buy groceries  ');
    await userEvent.click(button);

    expect(onAdd).toHaveBeenCalledTimes(1);
    expect(onAdd).toHaveBeenCalledWith('Buy groceries');
  });

  it('calls onAdd with trimmed text when Enter is pressed', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const input = screen.getByRole('textbox', { name: /todo text/i });

    await userEvent.type(input, '  Walk the dog  ');
    await userEvent.type(input, '{Enter}');

    expect(onAdd).toHaveBeenCalledTimes(1);
    expect(onAdd).toHaveBeenCalledWith('Walk the dog');
  });

  it('clears the input after a successful submit', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const input = screen.getByRole('textbox', { name: /todo text/i });
    const button = screen.getByRole('button', { name: /add/i });

    await userEvent.type(input, 'Read a book');
    await userEvent.click(button);

    expect(input).toHaveValue('');
  });

  it('does not call onAdd when text is empty', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const button = screen.getByRole('button', { name: /add/i });
    await userEvent.click(button);

    expect(onAdd).not.toHaveBeenCalled();
  });

  it('does not call onAdd when text is only whitespace', async () => {
    const onAdd = vi.fn();
    render(<TodoInput onAdd={onAdd} />);

    const input = screen.getByRole('textbox', { name: /todo text/i });
    const button = screen.getByRole('button', { name: /add/i });

    await userEvent.type(input, '    ');
    await userEvent.click(button);

    expect(onAdd).not.toHaveBeenCalled();
    expect(input).toHaveValue('    ');
  });
});
