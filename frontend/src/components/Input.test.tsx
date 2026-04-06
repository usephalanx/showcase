import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Input from './Input';

describe('Input', () => {
  it('renders without crashing', () => {
    render(
      <Input label="Name" value="" onChange={() => {}} />
    );
    expect(screen.getByLabelText('Name')).toBeInTheDocument();
  });

  it('renders a label with the provided text', () => {
    render(
      <Input label="Email Address" value="" onChange={() => {}} />
    );
    expect(screen.getByText('Email Address')).toBeInTheDocument();
  });

  it('displays the placeholder text', () => {
    render(
      <Input
        label="Phone"
        placeholder="Enter your phone"
        value=""
        onChange={() => {}}
      />
    );
    expect(screen.getByPlaceholderText('Enter your phone')).toBeInTheDocument();
  });

  it('calls onChange when user types', () => {
    const handleChange = vi.fn();
    render(
      <Input label="Username" value="" onChange={handleChange} />
    );
    const input = screen.getByLabelText('Username');
    fireEvent.change(input, { target: { value: 'hello' } });
    expect(handleChange).toHaveBeenCalledWith('hello');
  });

  it('renders the controlled value', () => {
    render(
      <Input label="City" value="Portland" onChange={() => {}} />
    );
    expect(screen.getByLabelText('City')).toHaveValue('Portland');
  });

  it('renders an error message when error prop is provided', () => {
    render(
      <Input
        label="Email"
        value=""
        onChange={() => {}}
        error="Email is required"
      />
    );
    const errorMsg = screen.getByRole('alert');
    expect(errorMsg).toHaveTextContent('Email is required');
  });

  it('applies aria-invalid when error is present', () => {
    render(
      <Input
        label="Email"
        value=""
        onChange={() => {}}
        error="Invalid email"
      />
    );
    expect(screen.getByLabelText(/Email/)).toHaveAttribute('aria-invalid', 'true');
  });

  it('does not render error element when no error', () => {
    render(
      <Input label="Name" value="" onChange={() => {}} />
    );
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('renders a textarea when type is textarea', () => {
    render(
      <Input
        label="Message"
        value=""
        onChange={() => {}}
        type="textarea"
      />
    );
    const textarea = screen.getByLabelText('Message');
    expect(textarea.tagName).toBe('TEXTAREA');
  });

  it('renders an input with correct type for email', () => {
    render(
      <Input label="Email" value="" onChange={() => {}} type="email" />
    );
    const input = screen.getByLabelText('Email');
    expect(input).toHaveAttribute('type', 'email');
  });

  it('renders an input with correct type for tel', () => {
    render(
      <Input label="Phone" value="" onChange={() => {}} type="tel" />
    );
    const input = screen.getByLabelText('Phone');
    expect(input).toHaveAttribute('type', 'tel');
  });

  it('renders an input with correct type for number', () => {
    render(
      <Input label="Age" value="" onChange={() => {}} type="number" />
    );
    const input = screen.getByLabelText('Age');
    expect(input).toHaveAttribute('type', 'number');
  });

  it('shows the required asterisk when required is true', () => {
    render(
      <Input label="Full Name" value="" onChange={() => {}} required />
    );
    expect(screen.getByText('*')).toBeInTheDocument();
  });

  it('does not show the required asterisk when required is false', () => {
    render(
      <Input label="Nickname" value="" onChange={() => {}} />
    );
    expect(screen.queryByText('*')).not.toBeInTheDocument();
  });

  it('sets the HTML required attribute when required', () => {
    render(
      <Input label="Name" value="" onChange={() => {}} required />
    );
    expect(screen.getByLabelText(/Name/)).toBeRequired();
  });

  it('applies additional className', () => {
    const { container } = render(
      <Input
        label="Test"
        value=""
        onChange={() => {}}
        className="mt-4"
      />
    );
    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper.className).toContain('mt-4');
  });

  it('sets the name attribute on the input', () => {
    render(
      <Input label="Email" value="" onChange={() => {}} name="email" />
    );
    expect(screen.getByLabelText('Email')).toHaveAttribute('name', 'email');
  });

  it('disables the input when disabled is true', () => {
    render(
      <Input label="Disabled" value="" onChange={() => {}} disabled />
    );
    expect(screen.getByLabelText('Disabled')).toBeDisabled();
  });

  it('calls onChange for textarea type', () => {
    const handleChange = vi.fn();
    render(
      <Input
        label="Bio"
        value=""
        onChange={handleChange}
        type="textarea"
      />
    );
    const textarea = screen.getByLabelText('Bio');
    fireEvent.change(textarea, { target: { value: 'My bio' } });
    expect(handleChange).toHaveBeenCalledWith('My bio');
  });
});
