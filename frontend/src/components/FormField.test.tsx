import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Input, TextArea } from './FormField';

// ---------------------------------------------------------------------------
// Input tests
// ---------------------------------------------------------------------------
describe('Input', () => {
  it('renders without crashing', () => {
    render(<Input label="Email" value="" onChange={() => {}} />);
    expect(screen.getByTestId('input-wrapper')).toBeTruthy();
  });

  it('renders the label text', () => {
    render(<Input label="Username" value="" onChange={() => {}} />);
    expect(screen.getByText('Username')).toBeTruthy();
  });

  it('associates label with input via htmlFor', () => {
    render(<Input label="Username" id="user" value="" onChange={() => {}} />);
    const input = screen.getByLabelText('Username');
    expect(input).toBeTruthy();
    expect(input.getAttribute('id')).toBe('user');
  });

  it('renders the placeholder', () => {
    render(<Input label="Name" placeholder="Enter name" value="" onChange={() => {}} />);
    expect(screen.getByPlaceholderText('Enter name')).toBeTruthy();
  });

  it('renders the controlled value', () => {
    render(<Input label="Name" value="Alice" onChange={() => {}} />);
    const input = screen.getByLabelText('Name') as HTMLInputElement;
    expect(input.value).toBe('Alice');
  });

  it('calls onChange with the new value on input', () => {
    const handleChange = vi.fn();
    render(<Input label="Name" value="" onChange={handleChange} />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Bob' } });
    expect(handleChange).toHaveBeenCalledWith('Bob');
  });

  it('uses the correct input type', () => {
    render(<Input label="Password" type="password" value="" onChange={() => {}} />);
    const input = screen.getByLabelText('Password') as HTMLInputElement;
    expect(input.type).toBe('password');
  });

  it('defaults to type text', () => {
    render(<Input label="Field" value="" onChange={() => {}} />);
    const input = screen.getByLabelText('Field') as HTMLInputElement;
    expect(input.type).toBe('text');
  });

  it('displays error message when error prop is set', () => {
    render(<Input label="Email" value="" onChange={() => {}} error="Required" />);
    expect(screen.getByRole('alert')).toBeTruthy();
    expect(screen.getByText('Required')).toBeTruthy();
  });

  it('sets aria-invalid when error is present', () => {
    render(<Input label="Email" value="" onChange={() => {}} error="Invalid" />);
    const input = screen.getByLabelText('Email');
    expect(input.getAttribute('aria-invalid')).toBe('true');
  });

  it('does not display error when error prop is undefined', () => {
    render(<Input label="Email" value="" onChange={() => {}} />);
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('renders disabled input', () => {
    render(<Input label="Read Only" value="fixed" onChange={() => {}} disabled />);
    const input = screen.getByLabelText('Read Only') as HTMLInputElement;
    expect(input.disabled).toBe(true);
  });

  it('renders required indicator', () => {
    render(<Input label="Email" value="" onChange={() => {}} required />);
    expect(screen.getByText('*')).toBeTruthy();
  });

  it('calls onBlur when the input loses focus', () => {
    const handleBlur = vi.fn();
    render(<Input label="Name" value="" onChange={() => {}} onBlur={handleBlur} />);
    fireEvent.focus(screen.getByLabelText('Name'));
    fireEvent.blur(screen.getByLabelText('Name'));
    expect(handleBlur).toHaveBeenCalledTimes(1);
  });

  it('passes the name attribute', () => {
    render(<Input label="Field" name="my_field" value="" onChange={() => {}} />);
    const input = screen.getByLabelText('Field') as HTMLInputElement;
    expect(input.name).toBe('my_field');
  });
});

// ---------------------------------------------------------------------------
// TextArea tests
// ---------------------------------------------------------------------------
describe('TextArea', () => {
  it('renders without crashing', () => {
    render(<TextArea label="Description" value="" onChange={() => {}} />);
    expect(screen.getByTestId('textarea-wrapper')).toBeTruthy();
  });

  it('renders the label text', () => {
    render(<TextArea label="Bio" value="" onChange={() => {}} />);
    expect(screen.getByText('Bio')).toBeTruthy();
  });

  it('associates label with textarea', () => {
    render(<TextArea label="Notes" id="notes" value="" onChange={() => {}} />);
    const textarea = screen.getByLabelText('Notes');
    expect(textarea.tagName.toLowerCase()).toBe('textarea');
  });

  it('renders the controlled value', () => {
    render(<TextArea label="Notes" value="Hello world" onChange={() => {}} />);
    const textarea = screen.getByLabelText('Notes') as HTMLTextAreaElement;
    expect(textarea.value).toBe('Hello world');
  });

  it('calls onChange with the new value on input', () => {
    const handleChange = vi.fn();
    render(<TextArea label="Notes" value="" onChange={handleChange} />);
    fireEvent.change(screen.getByLabelText('Notes'), { target: { value: 'Updated' } });
    expect(handleChange).toHaveBeenCalledWith('Updated');
  });

  it('sets rows attribute', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} rows={8} />);
    const textarea = screen.getByLabelText('Notes') as HTMLTextAreaElement;
    expect(textarea.rows).toBe(8);
  });

  it('defaults to 4 rows', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} />);
    const textarea = screen.getByLabelText('Notes') as HTMLTextAreaElement;
    expect(textarea.rows).toBe(4);
  });

  it('displays error message when error prop is set', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} error="Too short" />);
    expect(screen.getByRole('alert')).toBeTruthy();
    expect(screen.getByText('Too short')).toBeTruthy();
  });

  it('sets aria-invalid when error is present', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} error="Bad" />);
    const textarea = screen.getByLabelText('Notes');
    expect(textarea.getAttribute('aria-invalid')).toBe('true');
  });

  it('does not display error when error prop is undefined', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} />);
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('renders disabled textarea', () => {
    render(<TextArea label="Notes" value="locked" onChange={() => {}} disabled />);
    const textarea = screen.getByLabelText('Notes') as HTMLTextAreaElement;
    expect(textarea.disabled).toBe(true);
  });

  it('renders required indicator', () => {
    render(<TextArea label="Notes" value="" onChange={() => {}} required />);
    expect(screen.getByText('*')).toBeTruthy();
  });

  it('renders placeholder', () => {
    render(<TextArea label="Notes" placeholder="Write here..." value="" onChange={() => {}} />);
    expect(screen.getByPlaceholderText('Write here...')).toBeTruthy();
  });

  it('calls onBlur when the textarea loses focus', () => {
    const handleBlur = vi.fn();
    render(<TextArea label="Notes" value="" onChange={() => {}} onBlur={handleBlur} />);
    fireEvent.focus(screen.getByLabelText('Notes'));
    fireEvent.blur(screen.getByLabelText('Notes'));
    expect(handleBlur).toHaveBeenCalledTimes(1);
  });
});
